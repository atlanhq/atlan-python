# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
import logging
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Callable,
    List,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
    overload,
)

from pydantic.v1 import StrictStr, constr, validate_arguments
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from pyatlan.client.common import (
    AsyncApiCaller,
    DeleteByGuid,
    FindCategoryFastByName,
    FindConnectionsByName,
    FindDomainByName,
    FindGlossaryByName,
    FindPersonasByName,
    FindProductByName,
    FindPurposesByName,
    FindTermFastByName,
    GetByGuid,
    GetByQualifiedName,
    GetHierarchy,
    GetLineageList,
    ManageCustomMetadata,
    ManageTerms,
    ModifyAtlanTags,
    PurgeByGuid,
    RemoveAnnouncement,
    RemoveCertificate,
    RemoveCustomMetadata,
    RestoreAsset,
    Save,
    Search,
    SearchForAssetWithName,
    UpdateAnnouncement,
    UpdateAsset,
    UpdateAssetByAttribute,
    UpdateCertificate,
)
from pyatlan.client.constants import BULK_UPDATE, DELETE_ENTITIES_BY_GUIDS
from pyatlan.errors import ErrorCode, NotFoundError, PermissionError
from pyatlan.model.aio import AsyncIndexSearchResults, AsyncLineageListResults
from pyatlan.model.aio.custom_metadata import (
    AsyncCustomMetadataDict,
    AsyncCustomMetadataRequest,
)
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    DataDomain,
    DataProduct,
    Persona,
    Purpose,
)
from pyatlan.model.core import Announcement, BulkRequest
from pyatlan.model.enums import (
    AtlanConnectorType,
    AtlanDeleteType,
    CertificateStatus,
    SaveSemantic,
)
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.search import IndexSearchRequest, Query

if TYPE_CHECKING:
    from pyatlan.model.search import IndexSearchRequest


A = TypeVar("A", bound=Asset)
LOGGER = logging.getLogger(__name__)


class IndexSearchRequestProvider(Protocol):
    def to_request(self) -> IndexSearchRequest:
        pass


class AsyncAssetClient:
    """
    Async asset client that mirrors sync AssetClient API.

    This client uses shared business logic from core to ensure
    identical behavior with the sync client while providing async support.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    async def search(
        self,
        criteria: IndexSearchRequest,
        bulk=False,
    ) -> AsyncIndexSearchResults:
        """
        Async search that reuses shared business logic via Search.

        :param criteria: search criteria
        :param bulk: whether to use bulk search mode
        :returns: AsyncIndexSearchResults
        """
        INDEX_SEARCH, request_obj = Search.prepare_request(criteria, bulk)
        raw_json = await self._client._call_api(INDEX_SEARCH, request_obj=request_obj)
        response = Search.process_response(raw_json, criteria)

        if Search._check_for_bulk_search(
            criteria, response["count"], bulk, AsyncIndexSearchResults
        ):
            return await self.search(criteria)

        return AsyncIndexSearchResults(
            self._client,  # type: ignore[arg-type]
            criteria,
            0,
            len(response["assets"]),
            response["count"],
            response["assets"],
            response.get("aggregations"),
            bulk,
        )

    async def get_lineage_list(self, lineage_request) -> AsyncLineageListResults:
        """
        Async lineage retrieval using shared business logic.

        :param lineage_request: detailing the lineage query, parameters, and so on to run
        :returns: the results of the lineage request
        :raises InvalidRequestError: if the requested lineage direction is 'BOTH' (unsupported for this operation)
        :raises AtlanError: on any API communication issue
        """
        api_endpoint, request_obj = GetLineageList.prepare_request(lineage_request)
        raw_json = await self._client._call_api(
            api_endpoint, None, request_obj=request_obj
        )
        response = GetLineageList.process_response(raw_json, lineage_request)

        return AsyncLineageListResults(
            client=self._client,
            criteria=lineage_request,
            start=lineage_request.offset or 0,
            size=lineage_request.size or 10,
            has_more=response["has_more"],
            assets=response["assets"],
        )

    @validate_arguments
    async def find_personas_by_name(
        self,
        name: str,
        attributes: Optional[List[str]] = None,
    ) -> List[Persona]:
        """
        Async find personas by name using shared business logic.

        :param name: of the persona
        :param attributes: (optional) collection of attributes to retrieve for the persona
        :returns: all personas with that name, if found
        :raises NotFoundError: if no persona with the provided name exists
        """
        search_request = FindPersonasByName.prepare_request(name, attributes)
        search_results = await self.search(search_request)
        return FindPersonasByName.process_response(
            search_results, name, allow_multiple=True
        )

    @validate_arguments
    async def find_purposes_by_name(
        self,
        name: str,
        attributes: Optional[List[str]] = None,
    ) -> List[Purpose]:
        """
        Async find purposes by name using shared business logic.

        :param name: of the purpose
        :param attributes: (optional) collection of attributes to retrieve for the purpose
        :returns: all purposes with that name, if found
        :raises NotFoundError: if no purpose with the provided name exists
        """
        search_request = FindPurposesByName.prepare_request(name, attributes)
        search_results = await self.search(search_request)
        return FindPurposesByName.process_response(
            search_results, name, allow_multiple=True
        )

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def get_by_qualified_name(
        self,
        qualified_name: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = True,
        attributes: Optional[Union[List[str], List[AtlanField]]] = None,
        related_attributes: Optional[Union[List[str], List[AtlanField]]] = None,
    ) -> A:
        """
        Async retrieval of asset by qualified_name using shared business logic.

        :param qualified_name: qualified_name of the asset to be retrieved
        :param asset_type: type of asset to be retrieved ( must be the actual asset type not a super type)
        :param min_ext_info: whether to minimize extra info (True) or not (False)
        :param ignore_relationships: whether to include relationships (False) or exclude them (True)
        :param attributes: a specific list of attributes to retrieve for the asset
        :param related_attributes: a specific list of relationships attributes to retrieve for the asset
        :returns: the requested asset
        :raises NotFoundError: if the asset does not exist
        :raises AtlanError: on any API communication issue
        """

        # Normalize field inputs
        normalized_attributes = GetByQualifiedName.normalize_search_fields(attributes)
        normalized_related_attributes = GetByQualifiedName.normalize_search_fields(
            related_attributes
        )

        # Use FluentSearch if specific attributes are requested
        if (normalized_attributes and len(normalized_attributes)) or (
            normalized_related_attributes and len(normalized_related_attributes)
        ):
            search = GetByQualifiedName.prepare_fluent_search_request(
                qualified_name,
                asset_type,
                normalized_attributes,
                normalized_related_attributes,
            )
            results = await search.execute_async(client=self._client)  # type: ignore[arg-type]
            return GetByQualifiedName.process_fluent_search_response(
                results, qualified_name, asset_type
            )

        # Use direct API call for simple requests
        endpoint_path, query_params = GetByQualifiedName.prepare_direct_api_request(
            qualified_name, asset_type, min_ext_info, ignore_relationships
        )
        raw_json = await self._client._call_api(endpoint_path, query_params)
        return GetByQualifiedName.process_direct_api_response(
            raw_json, qualified_name, asset_type
        )

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def get_by_guid(
        self,
        guid: str,
        asset_type: Type[A] = Asset,  # type: ignore[assignment]
        min_ext_info: bool = False,
        ignore_relationships: bool = True,
        attributes: Optional[Union[List[str], List[AtlanField]]] = None,
        related_attributes: Optional[Union[List[str], List[AtlanField]]] = None,
    ) -> A:
        """
        Async retrieval of asset by GUID using shared business logic.

        :param guid: unique identifier (GUID) of the asset to retrieve
        :param asset_type: type of asset to be retrieved, defaults to `Asset`
        :param min_ext_info: whether to minimize extra info (True) or not (False)
        :param ignore_relationships: whether to include relationships (False) or exclude them (True)
        :param attributes: a specific list of attributes to retrieve for the asset
        :param related_attributes: a specific list of relationships attributes to retrieve for the asset
        :returns: the requested asset
        :raises NotFoundError: if the asset does not exist, or is not of the type requested
        :raises AtlanError: on any API communication issue
        """

        # Normalize field inputs
        normalized_attributes = GetByQualifiedName.normalize_search_fields(attributes)
        normalized_related_attributes = GetByQualifiedName.normalize_search_fields(
            related_attributes
        )

        # Use FluentSearch if specific attributes are requested
        if (normalized_attributes and len(normalized_attributes)) or (
            normalized_related_attributes and len(normalized_related_attributes)
        ):
            search = GetByGuid.prepare_fluent_search_request(
                guid, asset_type, normalized_attributes, normalized_related_attributes
            )
            results = await search.execute_async(client=self._client)  # type: ignore[arg-type]
            return GetByGuid.process_fluent_search_response(results, guid, asset_type)

        # Use direct API call for simple requests
        endpoint_path, query_params = GetByGuid.prepare_direct_api_request(
            guid, min_ext_info, ignore_relationships
        )
        raw_json = await self._client._call_api(endpoint_path, query_params)
        return GetByGuid.process_direct_api_response(raw_json, guid, asset_type)

    @validate_arguments
    async def retrieve_minimal(
        self,
        guid: str,
        asset_type: Type[A] = Asset,  # type: ignore[assignment]
    ) -> A:
        """
        Async retrieval of asset by GUID without any relationships.

        :param guid: unique identifier (GUID) of the asset to retrieve
        :param asset_type: type of asset to be retrieved, defaults to `Asset`
        :returns: the asset, without any of its relationships
        :raises NotFoundError: if the asset does not exist
        """
        return await self.get_by_guid(
            guid=guid,
            asset_type=asset_type,
            min_ext_info=True,
            ignore_relationships=True,
        )

    @validate_arguments
    async def save(
        self,
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
        append_atlan_tags: bool = False,
    ) -> AssetMutationResponse:
        """
        Async save method - creates or updates assets based on qualified_name.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update
        :param replace_custom_metadata: replaces any custom metadata with non-empty values provided
        :param overwrite_custom_metadata: overwrites any custom metadata, even with empty values
        :param append_atlan_tags: whether to add/update/remove AtlanTags during an update
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        :raises ApiError: if a connection was created and blocking until policies are synced overruns the retry limit
        """

        query_params, request = await Save.prepare_request_async(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
            append_atlan_tags=append_atlan_tags,
            client=self._client,  # type: ignore[arg-type]
        )
        raw_json = await self._client._call_api(BULK_UPDATE, query_params, request)
        response = Save.process_response(raw_json)
        if connections_created := response.assets_created(Connection):
            await self._wait_for_connections_to_be_created(connections_created)
        return response

    async def _wait_for_connections_to_be_created(self, connections_created):
        guids = Save.get_connection_guids_to_wait_for(connections_created)

        @retry(
            retry=retry_if_exception_type(PermissionError),
            wait=wait_exponential(multiplier=1, min=1, max=8),
            stop=stop_after_attempt(10),
            reraise=True,
        )
        async def _retrieve_connection_with_retry(guid):
            """Retry connection retrieval on permission errors."""
            await self.retrieve_minimal(guid=guid, asset_type=Connection)

        # Wait for each connection to be fully created and accessible
        for guid in guids:
            await _retrieve_connection_with_retry(guid)

        Save.log_connections_finished()

    @validate_arguments
    async def save_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        Async save with merging custom metadata.
        If no asset exists, has the same behavior as save(), while also setting
        any custom metadata provided. If an asset does exist, optionally overwrites any Atlan tags.
        Will merge any provided custom metadata with any custom metadata that already exists on the asset.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the created or updated assets
        """
        return await self.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=True,
            overwrite_custom_metadata=False,
        )

    @validate_arguments
    async def update_merging_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        Async update with merging custom metadata.
        If no asset exists, fails with a NotFoundError. Will merge any provided
        custom metadata with any custom metadata that already exists on the asset.
        If an asset does exist, optionally overwrites any Atlan tags.

        :param entity: the asset to update
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the updated asset
        :raises NotFoundError: if the asset does not exist (will not create it)
        """

        # Use async version of validate_asset_exists
        await UpdateAsset.validate_asset_exists_async(
            qualified_name=entity.qualified_name or "",
            asset_type=type(entity),
            get_by_qualified_name_func=self.get_by_qualified_name,
        )
        return await self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    async def save_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        Async save with replacing custom metadata.
        If no asset exists, has the same behavior as save(), while also setting
        any custom metadata provided.
        If an asset does exist, optionally overwrites any Atlan tags.
        Will overwrite all custom metadata on any existing asset with only the custom metadata provided
        (wiping out any other custom metadata on an existing asset that is not provided in the request).

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the created or updated assets
        :raises AtlanError: on any API communication issue
        """

        # Handle entities as list for consistency
        entities: List[Asset] = []
        if isinstance(entity, list):
            entities.extend(entity)
        else:
            entities.append(entity)

        # Flush custom metadata asynchronously for each entity
        for asset in entities:
            await asset.flush_custom_metadata_async(self._client)  # type: ignore[arg-type]
            asset.validate_required()

        # Prepare query params and request without calling sync flush again
        query_params = {
            "replaceClassifications": replace_atlan_tags,
            "replaceBusinessAttributes": True,
            "overwriteBusinessAttributes": True,
        }
        request = BulkRequest[Asset](entities=entities)
        raw_json = await self._client._call_api(BULK_UPDATE, query_params, request)
        return Save.process_response_replacing_cm(raw_json)

    @validate_arguments
    async def update_replacing_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        Async update with replacing custom metadata.
        If no asset exists, fails with a NotFoundError.
        Will overwrite all custom metadata on any existing asset with only the custom metadata provided
        (wiping out any other custom metadata on an existing asset that is not provided in the request).
        If an asset does exist, optionally overwrites any Atlan tags.

        :param entity: the asset to update
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the updated asset
        :raises NotFoundError: if the asset does not exist (will not create it)
        """
        await UpdateAsset.validate_asset_exists_async(
            qualified_name=entity.qualified_name or "",
            asset_type=type(entity),
            get_by_qualified_name_func=self.get_by_qualified_name,
        )
        return await self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    async def get_hierarchy(
        self,
        glossary,
        attributes: Optional[List] = None,
        related_attributes: Optional[List] = None,
    ):
        """
        Async retrieve category hierarchy in this Glossary, in a traversable form.

        :param glossary: the glossary to retrieve the category hierarchy for
        :param attributes: attributes to retrieve for each category in the hierarchy
        :param related_attributes: attributes to retrieve for each related asset in the hierarchy
        :returns: a traversable category hierarchy
        """

        # Validate glossary using shared logic
        GetHierarchy.validate_glossary(glossary)

        # Prepare search request using shared logic
        request = GetHierarchy.prepare_search_request(
            glossary, attributes, related_attributes
        )

        # Execute async search
        response = await self.search(request)

        # Process results using async shared logic
        return await GetHierarchy.process_async_search_results(response, glossary)

    async def process_assets(
        self,
        search: IndexSearchRequestProvider,
        func: Callable[[Asset], Awaitable[None]],
    ) -> int:
        """
        Async process assets matching a search query and apply a processing function to each unique asset.

        This function iteratively searches for assets using the search provider and processes each
        unique asset using the provided callable function. The uniqueness of assets is determined
        based on their GUIDs. If new assets are found in later iterations that haven't been
        processed yet, the process continues until no more new assets are available to process.

        Arguments:
            search: IndexSearchRequestProvider
                The search provider that generates search queries and contains the criteria for
                searching the assets such as a FluentSearch.
            func: Callable[[Asset], Awaitable[None]]
                An async callable function that receives each unique asset as its parameter and performs
                the required operations on it.

        Returns:
            int: The total number of unique assets that have been processed.
        """
        guids_processed: set[str] = set()
        has_assets_to_process: bool = True
        iteration_count = 0
        while has_assets_to_process:
            iteration_count += 1
            has_assets_to_process = False
            response = await self.search(search.to_request())
            LOGGER.debug(
                "Iteration %d found %d assets.", iteration_count, response.count
            )
            async for asset in response:
                if asset.guid not in guids_processed:
                    guids_processed.add(asset.guid)
                    has_assets_to_process = True
                    await func(asset)
        return len(guids_processed)

    @validate_arguments
    async def purge_by_guid(
        self,
        guid: Union[str, List[str]],
        delete_type: AtlanDeleteType = AtlanDeleteType.PURGE,
    ) -> AssetMutationResponse:
        """
        Async purge (permanent delete) assets by GUID.
        Deletes one or more assets by their unique identifier (GUID) using the specified delete type.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to delete
        :param delete_type: type of deletion to perform (PURGE or HARD)
        :returns: details of the deleted asset(s)
        :raises AtlanError: on any API communication issue

        .. warning::
            PURGE and HARD deletions are irreversible operations. Use with caution.
        """

        query_params = PurgeByGuid.prepare_request(guid, delete_type)
        raw_json = await self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        return PurgeByGuid.process_response(raw_json)

    @validate_arguments
    async def delete_by_guid(
        self, guid: Union[str, List[str]]
    ) -> AssetMutationResponse:
        """
        Async soft-delete (archive) assets by GUID.
        This operation can be reversed by updating the asset and its status to ACTIVE.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to soft-delete
        :returns: details of the soft-deleted asset(s)
        :raises AtlanError: on any API communication issue
        :raises ApiError: if the retry limit is overrun waiting for confirmation the asset is deleted
        :raises InvalidRequestError: if an asset does not support archiving
        """

        guids = DeleteByGuid.prepare_request(guid)

        # Validate each asset can be archived
        assets = []
        for single_guid in guids:
            asset = await self.retrieve_minimal(guid=single_guid, asset_type=Asset)
            assets.append(asset)
        DeleteByGuid.validate_assets_can_be_archived(assets)

        # Perform the deletion
        query_params = DeleteByGuid.prepare_delete_request(guids)
        raw_json = await self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        response = DeleteByGuid.process_response(raw_json)

        # Wait for deletion confirmation with async retry logic
        for asset in DeleteByGuid.get_deleted_assets(response):
            await self._wait_till_deleted_async(asset)

        return response

    async def _wait_till_deleted_async(self, asset: Asset):
        """Async version of _wait_till_deleted with retry logic."""

        max_attempts = 20
        for attempt in range(max_attempts):
            try:
                retrieved_asset = await self.retrieve_minimal(
                    guid=asset.guid, asset_type=Asset
                )
                if DeleteByGuid.is_asset_deleted(retrieved_asset):
                    return
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from e
            await asyncio.sleep(1)  # Wait before retry

        # If we reach here, we've exhausted retries
        raise ErrorCode.RETRY_OVERRUN.exception_with_parameters()

    @validate_arguments
    async def restore(self, asset_type: Type[A], qualified_name: str) -> bool:
        """
        Async restore an archived (soft-deleted) asset to active.

        :param asset_type: type of the asset to restore
        :param qualified_name: of the asset to restore
        :returns: True if the asset is now restored, or False if not
        :raises AtlanError: on any API communication issue
        """
        return await self._restore_async(asset_type, qualified_name, 0)

    async def _restore_async(
        self, asset_type: Type[A], qualified_name: str, retries: int
    ) -> bool:
        """Async version of _restore with retry logic."""

        if not RestoreAsset.can_asset_type_be_archived(asset_type):
            return False

        existing = await self.get_by_qualified_name(
            asset_type=asset_type,
            qualified_name=qualified_name,
            ignore_relationships=False,
        )
        if not existing:
            # Nothing to restore, so cannot be restored
            return False
        elif RestoreAsset.is_asset_active(existing):
            # Already active, but could be due to the async nature of delete handlers
            if retries < 10:
                await asyncio.sleep(2)
                return await self._restore_async(
                    asset_type, qualified_name, retries + 1
                )
            else:
                # If we have exhausted the retries, though, we will short-circuit
                return True
        else:
            response = await self._restore_asset_async(existing)
            return RestoreAsset.is_restore_successful(response)

    async def _restore_asset_async(self, asset: Asset) -> AssetMutationResponse:
        """Async version of _restore_asset."""

        query_params, request = RestoreAsset.prepare_restore_request(asset)
        # Flush custom metadata for the restored asset
        for restored_asset in request.entities:
            restored_asset.flush_custom_metadata(self._client)  # type: ignore[arg-type]
        raw_json = await self._client._call_api(BULK_UPDATE, query_params, request)
        return RestoreAsset.process_restore_response(raw_json)

    async def _modify_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
        propagate: bool = False,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = False,
        restrict_propagation_through_hierarchy: bool = False,
        modification_type: str = "add",
        save_parameters: Optional[dict] = None,
    ) -> A:
        """
        Async shared method for tag modifications using shared business logic.

        :param asset_type: type of asset to modify tags for
        :param qualified_name: qualified name of the asset
        :param atlan_tag_names: human-readable names of the Atlan tags
        :param propagate: whether to propagate the Atlan tag
        :param remove_propagation_on_delete: whether to remove propagated tags on deletion
        :param restrict_lineage_propagation: whether to avoid propagating through lineage
        :param restrict_propagation_through_hierarchy: whether to prevent hierarchy propagation
        :param modification_type: type of modification (add, update, remove, replace)
        :param save_parameters: parameters for the save operation
        :returns: the updated asset
        """
        if save_parameters is None:
            save_parameters = {}

        # Retrieve the asset with necessary attributes
        # Add retry mechanism to handle search index eventual consistency
        @retry(
            reraise=True,
            retry=retry_if_exception_type(NotFoundError),
            stop=stop_after_attempt(10),
            wait=wait_exponential(multiplier=1, min=1, max=5),
        )
        async def _get_asset_with_retry():
            return await self.get_by_qualified_name(
                qualified_name=qualified_name,
                asset_type=asset_type,
                attributes=ModifyAtlanTags.get_retrieve_attributes(),
            )

        retrieved_asset = await _get_asset_with_retry()

        # Prepare the asset updater using shared logic
        updated_asset = ModifyAtlanTags.prepare_asset_updater(
            retrieved_asset, asset_type, qualified_name
        )

        # Create AtlanTag objects using shared logic
        atlan_tags = ModifyAtlanTags.create_atlan_tags(
            atlan_tag_names=atlan_tag_names,
            propagate=propagate,
            remove_propagation_on_delete=remove_propagation_on_delete,
            restrict_lineage_propagation=restrict_lineage_propagation,
            restrict_propagation_through_hierarchy=restrict_propagation_through_hierarchy,
        )

        # Apply the tag modification using shared logic
        ModifyAtlanTags.apply_tag_modification(
            updated_asset, atlan_tags, modification_type
        )

        # Save the asset with the provided parameters
        response = await self.save(entity=updated_asset, **save_parameters)

        # Process the response using shared logic
        return ModifyAtlanTags.process_save_response(
            response, asset_type, updated_asset
        )

    @validate_arguments
    async def add_atlan_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
        propagate: bool = False,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = False,
        restrict_propagation_through_hierarchy: bool = False,
    ) -> A:
        """
        Async add one or more Atlan tags to the provided asset.

        :param asset_type: type of asset to which to add the Atlan tags
        :param qualified_name: qualified_name of the asset to which to add the Atlan tags
        :param atlan_tag_names: human-readable names of the Atlan tags to add to the asset
        :param propagate: whether to propagate the Atlan tag (True) or not (False)
        :param remove_propagation_on_delete: whether to remove the propagated Atlan tags
        when the Atlan tag is removed from this asset (True) or not (False)
        :param restrict_lineage_propagation: whether to avoid propagating
        through lineage (True) or do propagate through lineage (False)
        :param restrict_propagation_through_hierarchy: whether to prevent this Atlan tag from
        propagating through hierarchy (True) or allow it to propagate through hierarchy (False)
        :returns: the asset that was updated (note that it will NOT contain details of the added Atlan tags)
        :raises AtlanError: on any API communication issue
        """
        return await self._modify_tags(
            asset_type=asset_type,
            qualified_name=qualified_name,
            atlan_tag_names=atlan_tag_names,
            propagate=propagate,
            remove_propagation_on_delete=remove_propagation_on_delete,
            restrict_lineage_propagation=restrict_lineage_propagation,
            restrict_propagation_through_hierarchy=restrict_propagation_through_hierarchy,
            modification_type="add",
            save_parameters={
                "replace_atlan_tags": False,
                "append_atlan_tags": True,
            },
        )

    @validate_arguments
    async def update_atlan_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
        propagate: bool = False,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = True,
        restrict_propagation_through_hierarchy: bool = False,
    ) -> A:
        """
        Async update one or more Atlan tags to the provided asset.

        :param asset_type: type of asset to which to update the Atlan tags
        :param qualified_name: qualified_name of the asset to which to update the Atlan tags
        :param atlan_tag_names: human-readable names of the Atlan tags to update to the asset
        :param propagate: whether to propagate the Atlan tag (True) or not (False)
        :param remove_propagation_on_delete: whether to remove the propagated Atlan tags
        when the Atlan tag is removed from this asset (True) or not (False)
        :param restrict_lineage_propagation: whether to avoid propagating
        through lineage (True) or do propagate through lineage (False)
        :param restrict_propagation_through_hierarchy: whether to prevent this Atlan tag from
        propagating through hierarchy (True) or allow it to propagate through hierarchy (False)
        :returns: the asset that was updated (note that it will NOT contain details of the updated Atlan tags)
        :raises AtlanError: on any API communication issue
        """
        return await self._modify_tags(
            asset_type=asset_type,
            qualified_name=qualified_name,
            atlan_tag_names=atlan_tag_names,
            propagate=propagate,
            remove_propagation_on_delete=remove_propagation_on_delete,
            restrict_lineage_propagation=restrict_lineage_propagation,
            restrict_propagation_through_hierarchy=restrict_propagation_through_hierarchy,
            modification_type="update",
            save_parameters={
                "replace_atlan_tags": False,
                "append_atlan_tags": True,
            },
        )

    @validate_arguments
    async def remove_atlan_tag(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_name: str,
    ) -> A:
        """
        Async removes a single Atlan tag from the provided asset.

        :param asset_type: type of asset to which to remove the Atlan tag
        :param qualified_name: qualified_name of the asset to which to remove the Atlan tag
        :param atlan_tag_name: human-readable name of the Atlan tag to remove from the asset
        :returns: the asset that was updated (note that it will NOT contain details of the deleted Atlan tag)
        :raises AtlanError: on any API communication issue
        """
        return await self._modify_tags(
            asset_type=asset_type,
            qualified_name=qualified_name,
            atlan_tag_names=[atlan_tag_name],
            modification_type="remove",
            save_parameters={
                "replace_atlan_tags": False,
                "append_atlan_tags": True,
            },
        )

    @validate_arguments
    async def remove_atlan_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
    ) -> A:
        """
        Async removes one or more Atlan tag from the provided asset.

        :param asset_type: type of asset to which to remove the Atlan tags
        :param qualified_name: qualified_name of the asset to which to remove the Atlan tags
        :param atlan_tag_names: human-readable name of the Atlan tag to remove from the asset
        :returns: the asset that was updated (note that it will NOT contain details of the deleted Atlan tags)
        :raises AtlanError: on any API communication issue
        """
        return await self._modify_tags(
            asset_type=asset_type,
            qualified_name=qualified_name,
            atlan_tag_names=atlan_tag_names,
            modification_type="remove",
            save_parameters={
                "replace_atlan_tags": False,
                "append_atlan_tags": True,
            },
        )

    async def _update_asset_by_attribute(
        self, asset: A, asset_type: Type[A], qualified_name: str
    ) -> Optional[A]:
        """
        Async shared method for updating assets by attribute using shared business logic.

        :param asset: the asset to update
        :param asset_type: type of asset being updated
        :param qualified_name: qualified name of the asset
        :returns: updated asset or None if update failed
        """

        # Prepare request parameters using shared logic
        query_params = UpdateAssetByAttribute.prepare_request_params(qualified_name)

        # Flush custom metadata
        asset.flush_custom_metadata(client=self._client)  # type: ignore[arg-type]

        # Prepare request body using shared logic
        request_body = UpdateAssetByAttribute.prepare_request_body(asset)

        # Get API endpoint using shared logic
        endpoint = UpdateAssetByAttribute.get_api_endpoint(asset_type)

        # Make async API call
        raw_json = await self._client._call_api(endpoint, query_params, request_body)

        # Process response using shared logic
        return UpdateAssetByAttribute.process_response(raw_json, asset_type)

    @overload
    async def update_certificate(
        self,
        asset_type: Type[AtlasGlossaryTerm],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        glossary_guid: str,
        message: Optional[str] = None,
    ) -> Optional[AtlasGlossaryTerm]: ...

    @overload
    async def update_certificate(
        self,
        asset_type: Type[AtlasGlossaryCategory],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        glossary_guid: str,
        message: Optional[str] = None,
    ) -> Optional[AtlasGlossaryCategory]: ...

    @overload
    async def update_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        glossary_guid: Optional[str] = None,
        message: Optional[str] = None,
    ) -> Optional[A]: ...

    @validate_arguments
    async def update_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        glossary_guid: Optional[str] = None,
        message: Optional[str] = None,
    ) -> Optional[A]:
        """
        Async update the certificate on an asset.

        :param asset_type: type of asset on which to update the certificate
        :param qualified_name: the qualified_name of the asset on which to update the certificate
        :param name: the name of the asset on which to update the certificate
        :param certificate_status: specific certificate to set on the asset
        :param glossary_guid: unique identifier of the glossary, required
        only when the asset type is `AtlasGlossaryTerm` or `AtlasGlossaryCategory`
        :param message: (optional) message to set (or None for no message)
        :returns: the result of the update, or None if the update failed
        :raises AtlanError: on any API communication issue
        """

        # Prepare asset with certificate using shared logic
        asset = UpdateCertificate.prepare_asset_with_certificate(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            certificate_status=certificate_status,
            message=message,
            glossary_guid=glossary_guid,
        )

        # Execute update using shared logic
        return await self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @overload
    async def remove_certificate(
        self,
        asset_type: Type[AtlasGlossaryTerm],
        qualified_name: str,
        name: str,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryTerm]: ...

    @overload
    async def remove_certificate(
        self,
        asset_type: Type[AtlasGlossaryCategory],
        qualified_name: str,
        name: str,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryCategory]: ...

    @overload
    async def remove_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]: ...

    @validate_arguments
    async def remove_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]:
        """
        Async remove the certificate from an asset.

        :param asset_type: type of asset from which to remove the certificate
        :param qualified_name: the qualified_name of the asset from which to remove the certificate
        :param name: the name of the asset from which to remove the certificate
        :param glossary_guid: unique identifier of the glossary, required
        only when the asset type is `AtlasGlossaryTerm` or `AtlasGlossaryCategory`
        :returns: the result of the removal, or None if the removal failed
        """

        # Prepare asset for certificate removal using shared logic
        asset = RemoveCertificate.prepare_asset_for_certificate_removal(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            glossary_guid=glossary_guid,
        )

        # Execute update using shared logic
        return await self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @overload
    async def update_announcement(
        self,
        asset_type: Type[AtlasGlossaryTerm],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryTerm]: ...

    @overload
    async def update_announcement(
        self,
        asset_type: Type[AtlasGlossaryCategory],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryCategory]: ...

    @overload
    async def update_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]: ...

    @validate_arguments
    async def update_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]:
        """
        Async update the announcement on an asset.

        :param asset_type: type of asset on which to update the announcement
        :param qualified_name: the qualified_name of the asset on which to update the announcement
        :param name: the name of the asset on which to update the announcement
        :param announcement: to apply to the asset
        :param glossary_guid: unique identifier of the glossary, required
        only when the asset type is `AtlasGlossaryTerm` or `AtlasGlossaryCategory`
        :returns: the result of the update, or None if the update failed
        """

        # Prepare asset with announcement using shared logic
        asset = UpdateAnnouncement.prepare_asset_with_announcement(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            announcement=announcement,
            glossary_guid=glossary_guid,
        )

        # Execute update using shared logic
        return await self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @overload
    async def remove_announcement(
        self,
        asset_type: Type[AtlasGlossaryTerm],
        qualified_name: str,
        name: str,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryTerm]: ...

    @overload
    async def remove_announcement(
        self,
        asset_type: Type[AtlasGlossaryCategory],
        qualified_name: str,
        name: str,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryCategory]: ...

    @overload
    async def remove_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]: ...

    @validate_arguments
    async def remove_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]:
        """
        Async remove the announcement from an asset.

        :param asset_type: type of asset from which to remove the announcement
        :param qualified_name: the qualified_name of the asset from which to remove the announcement
        :param glossary_guid: unique identifier of the glossary, required
        only when the asset type is `AtlasGlossaryTerm` or `AtlasGlossaryCategory`
        :returns: the result of the removal, or None if the removal failed
        """

        # Prepare asset for announcement removal using shared logic
        asset = RemoveAnnouncement.prepare_asset_for_announcement_removal(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            glossary_guid=glossary_guid,
        )

        # Execute update using shared logic
        return await self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def update_custom_metadata_attributes(
        self, guid: str, custom_metadata: AsyncCustomMetadataDict
    ):
        """
            ManageCustomMetadata,
            UpdateCustomMetadataAttributes,
        )

        Async update only the provided custom metadata attributes on the asset.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to update, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using async version
        custom_metadata_request = await AsyncCustomMetadataRequest.create(
            custom_metadata
        )

        # Get API endpoint using shared logic
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )

        # Make async API call
        await self._client._call_api(endpoint, None, custom_metadata_request)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def replace_custom_metadata(
        self, guid: str, custom_metadata: AsyncCustomMetadataDict
    ):
        """
        Async replace specific custom metadata on the asset.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to replace, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """

        # Prepare request using async version (includes clear_unset())
        custom_metadata.clear_unset()
        custom_metadata_request = await AsyncCustomMetadataRequest.create(
            custom_metadata
        )

        # Get API endpoint using shared logic
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )

        # Make async API call
        await self._client._call_api(endpoint, None, custom_metadata_request)

    @validate_arguments
    async def remove_custom_metadata(self, guid: str, cm_name: str):
        """
        Async remove specific custom metadata from an asset.

        :param guid: unique identifier (GUID) of the asset
        :param cm_name: human-readable name of the custom metadata to remove
        :raises AtlanError: on any API communication issue
        """

        # Prepare request using shared async logic (includes clear_all())
        custom_metadata_request = await RemoveCustomMetadata.prepare_request_async(
            cm_name, self._client
        )

        # Get API endpoint using shared logic
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )

        # Make async API call
        await self._client._call_api(endpoint, None, custom_metadata_request)

    async def _manage_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        save_semantic: SaveSemantic,
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Async shared method for managing terms using shared business logic.

        :param asset_type: type of the asset
        :param terms: list of terms to manage
        :param save_semantic: semantic for saving terms (APPEND, REPLACE, REMOVE)
        :param guid: unique identifier (GUID) of the asset
        :param qualified_name: qualified name of the asset
        :returns: the updated asset
        """

        # Validate input parameters using shared logic
        ManageTerms.validate_guid_and_qualified_name(guid, qualified_name)

        # Build and execute search using shared logic
        if guid:
            search_query = ManageTerms.build_fluent_search_by_guid(asset_type, guid)
        else:
            if qualified_name is None:
                raise ValueError(
                    "qualified_name cannot be None when guid is not provided"
                )
            search_query = ManageTerms.build_fluent_search_by_qualified_name(
                asset_type, qualified_name
            )

        results = await search_query.execute_async(client=self._client)  # type: ignore[arg-type]

        # Validate search results using shared logic
        first_result = ManageTerms.validate_search_results(
            results, asset_type, guid, qualified_name
        )

        # Create asset updater
        updated_asset = asset_type.updater(
            qualified_name=first_result.qualified_name, name=first_result.name
        )

        # Process terms with save semantic using shared logic
        processed_terms = ManageTerms.process_terms_with_semantic(terms, save_semantic)
        updated_asset.assigned_terms = processed_terms

        # Save and process response using shared logic
        response = await self.save(entity=updated_asset)
        return ManageTerms.process_save_response(response, asset_type, updated_asset)

    @validate_arguments
    async def append_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Async link additional terms to an asset, without replacing existing terms linked to the asset.

        :param asset_type: type of the asset
        :param terms: the list of terms to append to the asset
        :param guid: unique identifier (GUID) of the asset to which to link the terms
        :param qualified_name: the qualified_name of the asset to which to link the terms
        :returns: the asset that was updated (note that it will NOT contain details of the appended terms)
        """
        return await self._manage_terms(
            asset_type=asset_type,
            terms=terms,
            save_semantic=SaveSemantic.APPEND,
            guid=guid,
            qualified_name=qualified_name,
        )

    @validate_arguments
    async def replace_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Async replace the terms linked to an asset.

        :param asset_type: type of the asset
        :param terms: the list of terms to replace on the asset, or an empty list to remove all terms from an asset
        :param guid: unique identifier (GUID) of the asset to which to replace the terms
        :param qualified_name: the qualified_name of the asset to which to replace the terms
        :returns: the asset that was updated (note that it will NOT contain details of the replaced terms)
        """
        return await self._manage_terms(
            asset_type=asset_type,
            terms=terms,
            save_semantic=SaveSemantic.REPLACE,
            guid=guid,
            qualified_name=qualified_name,
        )

    @validate_arguments
    async def remove_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Async remove terms from an asset, without replacing all existing terms linked to the asset.

        :param asset_type: type of the asset
        :param terms: the list of terms to remove from the asset
        :param guid: unique identifier (GUID) of the asset from which to remove the terms
        :param qualified_name: the qualified_name of the asset from which to remove the terms
        :returns: the asset that was updated (note that it will NOT contain details of the resulting terms)
        """
        return await self._manage_terms(
            asset_type=asset_type,
            terms=terms,
            save_semantic=SaveSemantic.REMOVE,
            guid=guid,
            qualified_name=qualified_name,
        )

    async def _search_for_asset_with_name(
        self,
        query: Query,
        name: str,
        asset_type: Type[A],
        attributes: Optional[List],
        allow_multiple: bool = False,
    ) -> List[A]:
        """
        Async shared method for searching assets by name using shared business logic.

        :param query: query to execute
        :param name: name that was searched for (for error messages)
        :param asset_type: expected asset type
        :param attributes: optional collection of attributes to retrieve
        :param allow_multiple: whether multiple results are allowed
        :returns: list of found assets
        """

        # Build search request using shared logic
        search_request = SearchForAssetWithName.build_search_request(query, attributes)

        # Execute async search
        results = await self.search(search_request)

        # Process results using async shared logic
        return await SearchForAssetWithName.process_async_search_results(
            results, name, asset_type, allow_multiple
        )

    @validate_arguments
    async def find_connections_by_name(
        self,
        name: str,
        connector_type: AtlanConnectorType,
        attributes: Optional[List[str]] = None,
    ) -> List[Connection]:
        """
        Async find a connection by its human-readable name and type.

        :param name: of the connection
        :param connector_type: of the connection
        :param attributes: (optional) collection of attributes to retrieve for the connection
        :returns: all connections with that name and type, if found
        :raises NotFoundError: if the connection does not exist
        """
        if attributes is None:
            attributes = []

        # Build query using shared logic
        query = FindConnectionsByName.build_query(name, connector_type)

        # Execute search using shared logic
        return await self._search_for_asset_with_name(
            query=query,
            name=name,
            asset_type=Connection,
            attributes=attributes,
            allow_multiple=True,
        )

    @validate_arguments
    async def find_glossary_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossary:
        """
        Async find a glossary by its human-readable name.

        :param name: of the glossary
        :param attributes: (optional) collection of attributes to retrieve for the glossary
        :returns: the glossary, if found
        :raises NotFoundError: if no glossary with the provided name exists
        """
        if attributes is None:
            attributes = []

        # Build query using shared logic
        query = FindGlossaryByName.build_query(name)

        # Execute search using shared logic
        results = await self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossary, attributes=attributes
        )
        return results[0]

    @validate_arguments
    async def find_category_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(  # type: ignore
            strip_whitespace=True, min_length=1, strict=True
        ),
        attributes: Optional[List[StrictStr]] = None,
    ) -> List[AtlasGlossaryCategory]:
        """
        Async find a category by its human-readable name.

        :param name: of the category
        :param glossary_qualified_name: qualified_name of the glossary in which the category exists
        :param attributes: (optional) collection of attributes to retrieve for the category
        :returns: the category, if found
        :raises NotFoundError: if no category with the provided name exists in the glossary
        """
        if attributes is None:
            attributes = []

        # Build query using shared logic
        query = FindCategoryFastByName.build_query(name, glossary_qualified_name)

        # Execute search using shared logic
        return await self._search_for_asset_with_name(
            query=query,
            name=name,
            asset_type=AtlasGlossaryCategory,
            attributes=attributes,
            allow_multiple=True,
        )

    @validate_arguments
    async def find_category_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> List[AtlasGlossaryCategory]:
        """
        Async find a category by its human-readable name.

        :param name: of the category
        :param glossary_name: human-readable name of the glossary in which the category exists
        :param attributes: (optional) collection of attributes to retrieve for the category
        :returns: the category, if found
        :raises NotFoundError: if no category with the provided name exists in the glossary
        """
        # First find the glossary by name
        glossary = await self.find_glossary_by_name(name=glossary_name)

        # Then find the category in that glossary using the fast method
        return await self.find_category_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )

    @validate_arguments
    async def find_term_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(  # type: ignore
            strip_whitespace=True, min_length=1, strict=True
        ),
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        """
        Async find a term by its human-readable name.

        :param name: of the term
        :param glossary_qualified_name: qualified_name of the glossary in which the term exists
        :param attributes: (optional) collection of attributes to retrieve for the term
        :returns: the term, if found
        :raises NotFoundError: if no term with the provided name exists in the glossary
        """
        if attributes is None:
            attributes = []

        # Build query using shared logic
        query = FindTermFastByName.build_query(name, glossary_qualified_name)

        # Execute search using shared logic
        results = await self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossaryTerm, attributes=attributes
        )
        return results[0]

    @validate_arguments
    async def find_term_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        """
        Async find a term by its human-readable name.

        :param name: of the term
        :param glossary_name: human-readable name of the glossary in which the term exists
        :param attributes: (optional) collection of attributes to retrieve for the term
        :returns: the term, if found
        :raises NotFoundError: if no term with the provided name exists in the glossary
        """
        # First find the glossary by name
        glossary = await self.find_glossary_by_name(name=glossary_name)

        # Then find the term in that glossary using the fast method
        return await self.find_term_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )

    @validate_arguments
    async def find_domain_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> DataDomain:
        """
        Async find a data domain by its human-readable name.

        :param name: of the domain
        :param attributes: (optional) collection of attributes to retrieve for the domain
        :returns: the domain, if found
        :raises NotFoundError: if no domain with the provided name exists
        """
        attributes = attributes or []

        # Build query using shared logic
        query = FindDomainByName.build_query(name)

        # Execute search using shared logic
        results = await self._search_for_asset_with_name(
            query=query, name=name, asset_type=DataDomain, attributes=attributes
        )
        return results[0]

    @validate_arguments
    async def find_product_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> DataProduct:
        """
        Async find a data product by its human-readable name.

        :param name: of the product
        :param attributes: (optional) collection of attributes to retrieve for the product
        :returns: the product, if found
        :raises NotFoundError: if no product with the provided name exists
        """
        attributes = attributes or []

        # Build query using shared logic
        query = FindProductByName.build_query(name)

        # Execute search using shared logic
        results = await self._search_for_asset_with_name(
            query=query, name=name, asset_type=DataProduct, attributes=attributes
        )
        return results[0]

    @validate_arguments
    async def upsert(
        self,
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        """Deprecated async upsert - use save() instead."""
        return await self.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
        )

    @validate_arguments
    async def upsert_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated async upsert_merging_cm - use save_merging_cm() instead."""
        return await self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    async def upsert_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated async upsert_replacing_cm - use save_replacing_cm() instead."""
        return await self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )
