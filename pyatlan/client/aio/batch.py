# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import TYPE_CHECKING, Dict, List, Optional, cast

from pydantic.v1 import validate_arguments

from pyatlan.client.asset import (
    AssetCreationHandling,
    AssetIdentity,
    CustomMetadataHandling,
    FailedBatch,
)
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.model.assets import Asset, AtlasGlossaryTerm, MaterialisedView, Table, View
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.search import DSL

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient


class AsyncBatch:
    """Async utility class for managing bulk updates in batches."""

    _TABLE_LEVEL_ASSETS = {
        Table.__name__,
        View.__name__,
        MaterialisedView.__name__,
    }

    def __init__(
        self,
        client: AsyncAtlanClient,
        max_size: int,
        replace_atlan_tags: bool = False,
        custom_metadata_handling: CustomMetadataHandling = CustomMetadataHandling.IGNORE,
        capture_failures: bool = False,
        update_only: bool = False,
        track: bool = False,
        case_insensitive: bool = False,
        table_view_agnostic: bool = False,
        creation_handling: AssetCreationHandling = AssetCreationHandling.FULL,
    ):
        """
        Create a new async batch of assets to be bulk-saved.

        :param client: AsyncAtlanClient to use
        :param max_size: maximum size of each batch
            that should be processed (per API call)
        :param replace_atlan_tags: if True, all Atlan tags on an existing
            asset will be overwritten; if False, all Atlan tags will be ignored
        :param custom_metadata_handling: how to handle custom metadata
            (ignore it, replace it (wiping out anything pre-existing), or merge it)
        :param capture_failures: when True, any failed batches will be
            captured and retained rather than exceptions being raised
            (for large amounts of processing this could cause memory issues!)
        :param update_only: whether to allow assets to be created (False)
            or only allow existing assets to be updated (True)
        :param track: whether to track the basic information about
            every asset that is created or updated (True) or only track counts (False)
        :param case_insensitive: when running with `update_only` as True,
            whether to consider only exact matches (False) or ignore case (True).
        :param table_view_agnostic: whether tables and views should be treated interchangeably
            (an asset in the batch marked as a table will attempt to match a
            view if not found as a table, and vice versa)
        :param creation_handling: when allowing assets to be created,
            how to handle those creations (full assets or partial assets).
        """
        self._client: AsyncAtlanClient = client
        self._max_size: int = max_size
        self._replace_atlan_tags: bool = replace_atlan_tags
        self._custom_metadata_handling: CustomMetadataHandling = (
            custom_metadata_handling
        )
        self._capture_failures: bool = capture_failures
        self._update_only: bool = update_only
        self._track: bool = track
        self._case_insensitive: bool = case_insensitive
        self._table_view_agnostic: bool = table_view_agnostic
        self._creation_handling: AssetCreationHandling = creation_handling
        self._num_created = 0
        self._num_updated = 0
        self._num_restored = 0
        self._num_skipped = 0
        self._resolved_guids: Dict[str, str] = {}
        self._batch: List[Asset] = []
        self._failures: List[FailedBatch] = []
        self._created: List[Asset] = []
        self._updated: List[Asset] = []
        self._restored: List[Asset] = []
        self._skipped: List[Asset] = []
        self._resolved_qualified_names: Dict[str, str] = {}

    @property
    def failures(self) -> List[FailedBatch]:
        """Get information on any failed batches

        :returns: a list of FailedBatch objects that contain information about any batches that may have failed
        an empty list will be returned if there are no failures.
        """
        return self._failures

    @property
    def created(self) -> List[Asset]:
        """Get a list of all the Assets that were created

        :returns: a list of all the Assets that were created
        """
        return self._created

    @property
    def updated(self) -> List[Asset]:
        """Get a list of all the Assets that were updated

        :returns: a list of all the Assets that were updated
        """
        return self._updated

    @property
    def restored(self) -> List[Asset]:
        """Get a list of all the Assets that were potentially
        restored from being archived, or otherwise touched without
        actually being updated (minimal info only).

        :returns: a list of all the Assets that were restored
        """
        return self._restored

    @property
    def skipped(self) -> List[Asset]:
        """Get a list of all the Assets that were skipped.
        when update only is requested and the asset does not exist in Atlan

        :returns: a list of all the Assets that were skipped
        """
        return self._skipped

    @property
    def num_created(self) -> int:
        """
        Number of assets that were created (count only)
        """
        return self._num_created

    @property
    def num_updated(self) -> int:
        """
        Number of assets that were updated (count only)
        """
        return self._num_updated

    @property
    def num_restored(self) -> int:
        """
        Number of assets that were restored (count only)
        """
        return self._num_restored

    @property
    def num_skipped(self) -> int:
        """
        Number of assets that were skipped (count only)
        """
        return self._num_skipped

    @validate_arguments
    async def add(self, single: Asset) -> Optional[AssetMutationResponse]:
        """
        Add an asset to the batch to be processed.

        :param single: the asset to add to a batch
        :returns: an AssetMutationResponse containing the results of the save or None if the batch is still queued.
        """
        self._batch.append(single)
        return await self._process()

    async def _process(self) -> Optional[AssetMutationResponse]:
        """If the number of entities we have queued up is equal to the batch size, process them and reset our queue;
        otherwise do nothing.

        :returns: an AssetMutationResponse containing the results of the save or None if the batch is still queued.
        """
        return await self.flush() if len(self._batch) == self._max_size else None

    async def flush(self) -> Optional[AssetMutationResponse]:
        """Flush any remaining assets in the batch.

        :returns: an AssetMutationResponse containing the results of the saving any assets that were flushed
        """
        revised: list = []
        response: Optional[AssetMutationResponse] = None
        if self._batch:
            fuzzy_match: bool = False
            if self._table_view_agnostic:
                types_in_batch = {asset.type_name for asset in self._batch}
                fuzzy_match = any(
                    type_name in types_in_batch
                    for type_name in self._TABLE_LEVEL_ASSETS
                )
            if (
                self._update_only
                or self._creation_handling != AssetCreationHandling.FULL
                or fuzzy_match
            ):
                found: Dict[str, str] = {}
                qualified_names = [asset.qualified_name or "" for asset in self._batch]
                if self._case_insensitive:
                    search = FluentSearch().select(include_archived=True).min_somes(1)
                    for qn in qualified_names:
                        search = search.where_some(
                            Asset.QUALIFIED_NAME.eq(
                                value=qn or "", case_insensitive=self._case_insensitive
                            )
                        )
                else:
                    search = (
                        FluentSearch()
                        .select(include_archived=True)
                        .where(Asset.QUALIFIED_NAME.within(values=qualified_names))
                    )
                results = await search.page_size(
                    max(self._max_size * 2, DSL.__fields__.get("size").default)  # type: ignore[union-attr]
                ).execute_async(client=self._client)  # type: ignore[arg-type]

                async for asset in results:
                    asset_id = AssetIdentity(
                        type_name=asset.type_name,
                        qualified_name=asset.qualified_name or "",
                        case_insensitive=self._case_insensitive,
                    )
                    found[str(asset_id)] = asset.qualified_name or ""

                for asset in self._batch:
                    asset_id = AssetIdentity(
                        type_name=asset.type_name,
                        qualified_name=asset.qualified_name or "",
                        case_insensitive=self._case_insensitive,
                    )
                    # If found, with a type match, go ahead and update it
                    if str(asset_id) in found:
                        # Replace the actual qualifiedName on the asset before adding it to the batch
                        # in case it matched case-insensitively, we need the proper case-sensitive name we
                        # found to ensure it's an update, not a create)
                        self.add_fuzzy_matched(
                            asset=asset,
                            actual_qn=found.get(str(asset_id), ""),
                            revised=revised,
                        )
                    elif (
                        self._table_view_agnostic
                        and asset.type_name in self._TABLE_LEVEL_ASSETS
                    ):
                        # If found as a different (but acceptable) type, update that instead
                        as_table = AssetIdentity(
                            type_name=Table.__name__,
                            qualified_name=asset.qualified_name or "",
                            case_insensitive=self._case_insensitive,
                        )
                        as_view = AssetIdentity(
                            type_name=View.__name__,
                            qualified_name=asset.qualified_name or "",
                            case_insensitive=self._case_insensitive,
                        )
                        as_materialized_view = AssetIdentity(
                            type_name=MaterialisedView.__name__,
                            qualified_name=asset.qualified_name or "",
                            case_insensitive=self._case_insensitive,
                        )

                        if str(as_table) in found:
                            self.add_fuzzy_matched(
                                asset=asset,
                                actual_qn=found.get(str(as_table), ""),
                                revised=revised,
                                type_name=Table.__name__,
                            )
                        elif str(as_view) in found:
                            self.add_fuzzy_matched(
                                asset=asset,
                                actual_qn=found.get(str(as_view), ""),
                                revised=revised,
                                type_name=View.__name__,
                            )
                        elif str(as_materialized_view) in found:
                            self.add_fuzzy_matched(
                                asset=asset,
                                actual_qn=found.get(str(as_materialized_view), ""),
                                revised=revised,
                                type_name=MaterialisedView.__name__,
                            )
                        elif self._creation_handling == AssetCreationHandling.PARTIAL:
                            # Still create it (partial), if not found
                            # and partial asset creation is allowed
                            self.add_partial_asset(asset, revised)
                        elif self._creation_handling == AssetCreationHandling.FULL:
                            # Still create it (full), if not found
                            # and full asset creation is allowed
                            revised.append(asset)
                        else:
                            # Otherwise, if it still does not match any
                            # fallback and cannot be created, skip it
                            self.__track(self._skipped, asset)
                            self._num_skipped += 1
                    elif self._creation_handling == AssetCreationHandling.PARTIAL:
                        # Append `is_partial=True` onto the asset
                        # before adding it to the batch, to ensure only
                        # a partial (and not a full) asset is created
                        self.add_partial_asset(asset, revised)
                    else:
                        self.__track(self._skipped, asset)
                        self._num_skipped += 1
            else:
                # Otherwise create it (full)
                revised = self._batch.copy()

            if revised:
                try:
                    if self._custom_metadata_handling == CustomMetadataHandling.IGNORE:
                        response = await self._client.asset.save(
                            revised, replace_atlan_tags=self._replace_atlan_tags
                        )
                    elif (
                        self._custom_metadata_handling
                        == CustomMetadataHandling.OVERWRITE
                    ):
                        response = await self._client.asset.save_replacing_cm(
                            revised, replace_atlan_tags=self._replace_atlan_tags
                        )
                    elif self._custom_metadata_handling == CustomMetadataHandling.MERGE:
                        response = await self._client.asset.save_merging_cm(
                            revised, replace_atlan_tags=self._replace_atlan_tags
                        )
                    else:
                        raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                            self._custom_metadata_handling,
                            "CustomMetadataHandling.IGNORE, CustomMetadataHandling.OVERWRITE "
                            "or CustomMetadataHandling.MERGE",
                        )
                except AtlanError as er:
                    if self._capture_failures:
                        self._failures.append(
                            FailedBatch(failed_assets=self._batch, failure_reason=er)
                        )
                    else:
                        raise er
                self._batch = []
                response and self._track_response(response, revised)
        return response

    def _track_response(self, response: AssetMutationResponse, sent: list[Asset]):
        if response:
            if self._track and response.mutated_entities:
                if response.mutated_entities.CREATE:
                    for asset in response.mutated_entities.CREATE:
                        self.__track(self._created, asset)
                if response.mutated_entities.UPDATE:
                    for asset in response.mutated_entities.UPDATE:
                        self.__track(self._updated, asset)

            # Always track the counts and resolved GUIDs...
            if response.mutated_entities and response.mutated_entities.CREATE:
                self._num_created += len(response.mutated_entities.CREATE)
            if response.mutated_entities and response.mutated_entities.UPDATE:
                self._num_updated += len(response.mutated_entities.UPDATE)

            if response.guid_assignments:
                self._resolved_guids.update(response.guid_assignments)
            if sent:
                created_guids, updated_guids = set(), set()
                if response.mutated_entities:
                    if response.mutated_entities.CREATE:
                        created_guids = {
                            asset.guid for asset in response.mutated_entities.CREATE
                        }
                    if response.mutated_entities.UPDATE:
                        updated_guids = {
                            asset.guid for asset in response.mutated_entities.UPDATE
                        }
                for one in sent:
                    guid = one.guid
                    if guid and (
                        not response.guid_assignments
                        or guid not in response.guid_assignments
                    ):
                        # Ensure any assets that were sent with GUIDs
                        # that were used as-is are added to the resolved GUIDs map
                        self._resolved_guids[guid] = guid
                    mapped_guid = self._resolved_guids.get(guid, guid)
                    if (
                        mapped_guid not in created_guids
                        and mapped_guid not in updated_guids
                    ):
                        # Ensure any assets that do not show as either created or updated are still tracked
                        # as possibly restored (and inject the mapped GUID in case it had a placeholder)
                        one.guid = mapped_guid
                        self.__track(self._restored, one)
                        self._num_restored += 1
                    if self._case_insensitive:
                        type_name = one.type_name
                        qualified_name = one.qualified_name or ""
                        id = AssetIdentity(
                            type_name=type_name,
                            qualified_name=qualified_name,
                            case_insensitive=self._case_insensitive,
                        )
                        self._resolved_qualified_names[str(id)] = qualified_name

    @staticmethod
    def __track(tracker: List[Asset], candidate: Asset):
        if isinstance(candidate, AtlasGlossaryTerm):
            # trim_to_required for AtlasGlossaryTerm requires anchor
            # which is not include in AssetMutationResponse
            asset = cast(Asset, AtlasGlossaryTerm.ref_by_guid(candidate.guid))
        else:
            asset = candidate.trim_to_required()
        asset.name = candidate.name
        tracker.append(asset)

    def add_fuzzy_matched(
        self,
        asset: Asset,
        actual_qn: str,
        revised: List[Asset],
        type_name: Optional[str] = None,
    ):
        # Only when asset type in (`Table`, `View` or `MaterializedView`)
        # and `self._table_view_agnostic` is set to `True`
        if type_name:
            asset.type_name = type_name
        asset.qualified_name = actual_qn
        revised.append(asset)

    def add_partial_asset(self, asset: Asset, revised: List[Asset]):
        asset.is_partial = True
        revised.append(asset)
