# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import abc
import logging
import time
from abc import ABC
from enum import Enum
from typing import (
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Set,
    Type,
    TypeVar,
    Union,
    overload,
)
from warnings import warn

import requests
from pydantic.v1 import (
    StrictStr,
    ValidationError,
    constr,
    parse_obj_as,
    validate_arguments,
)
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    ADD_BUSINESS_ATTRIBUTE_BY_ID,
    BULK_UPDATE,
    DELETE_ENTITIES_BY_GUIDS,
    DELETE_ENTITY_BY_ATTRIBUTE,
    GET_ENTITY_BY_GUID,
    GET_ENTITY_BY_UNIQUE_ATTRIBUTE,
    GET_LINEAGE,
    GET_LINEAGE_LIST,
    INDEX_SEARCH,
    PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE,
    UPDATE_ENTITY_BY_ATTRIBUTE,
)
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.model.aggregation import Aggregations
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
    DataDomain,
    DataProduct,
    MaterialisedView,
    Persona,
    Purpose,
    Referenceable,
    Schema,
    Table,
    View,
)
from pyatlan.model.core import (
    Announcement,
    AssetRequest,
    AssetResponse,
    AtlanTag,
    AtlanTagName,
    AtlanTags,
    BulkRequest,
    SearchRequest,
)
from pyatlan.model.custom_metadata import CustomMetadataDict, CustomMetadataRequest
from pyatlan.model.enums import (
    AtlanConnectorType,
    AtlanDeleteType,
    CertificateStatus,
    EntityStatus,
    SortOrder,
)
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.lineage import (
    LineageDirection,
    LineageListRequest,
    LineageRequest,
    LineageResponse,
)
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.search import (
    DSL,
    IndexSearchRequest,
    Query,
    Term,
    with_active_category,
    with_active_glossary,
    with_active_term,
)
from pyatlan.utils import API, unflatten_custom_metadata_for_entity

T = TypeVar("T", bound=Referenceable)
A = TypeVar("A", bound=Asset)
Assets = Union[
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Connection,
    Database,
    Schema,
    Table,
    View,
    MaterialisedView,
]
Asset_Types = Union[
    Type[AtlasGlossary],
    Type[AtlasGlossaryCategory],
    Type[AtlasGlossaryTerm],
    Type[Connection],
    Type[Database],
    Type[Schema],
    Type[Table],
    Type[View],
    Type[MaterialisedView],
]

LOGGER = logging.getLogger(__name__)


class AssetClient:
    """
    This class can be used to retrieve information about assets. This class does not need to be instantiated
    directly but can be obtained through the asset property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    # TODO: Try adding @validate_arguments to this method once
    # the issue below is fixed or when we switch to pydantic v2
    # https://github.com/atlanhq/atlan-python/pull/88#discussion_r1260892704
    def search(self, criteria: IndexSearchRequest) -> IndexSearchResults:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :returns: the results of the search
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(
            INDEX_SEARCH,
            request_obj=criteria,
        )
        if "entities" in raw_json:
            try:
                for entity in raw_json["entities"]:
                    unflatten_custom_metadata_for_entity(
                        entity=entity, attributes=criteria.attributes
                    )
                assets = parse_obj_as(List[Asset], raw_json["entities"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            assets = []
        aggregations = self._get_aggregations(raw_json)
        count = raw_json.get("approximateCount", 0)
        return IndexSearchResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            assets=assets,
            aggregations=aggregations,
        )

    def _get_aggregations(self, raw_json) -> Optional[Aggregations]:
        aggregations = None
        if "aggregations" in raw_json:
            try:
                aggregations = Aggregations.parse_obj(raw_json["aggregations"])
            except ValidationError:
                pass
        return aggregations

    # TODO: Try adding @validate_arguments to this method once
    # the issue below is fixed or when we switch to pydantic v2
    # https://github.com/pydantic/pydantic/issues/2901
    def get_lineage(self, lineage_request: LineageRequest) -> LineageResponse:
        """
        Deprecated — this is an older, slower operation to retrieve lineage that will not receive further enhancements.
        Use the get_lineage_list operation instead.

        :param lineage_request: detailing the lineage query, parameters, and so on to run
        :returns: the results of the lineage request
        :raises AtlanError: on any API communication issue
        """
        warn(
            "Lineage retrieval using this method is deprecated, please use 'get_lineage_list' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        raw_json = self._client._call_api(
            GET_LINEAGE, None, lineage_request, exclude_unset=False
        )
        return LineageResponse(**raw_json)

    # TODO: Try adding @validate_arguments to this method once
    # the issue below is fixed or when we switch to pydantic v2
    # https://github.com/pydantic/pydantic/issues/2901
    def get_lineage_list(
        self, lineage_request: LineageListRequest
    ) -> LineageListResults:
        """
        Retrieve lineage using the higher-performance "list" API.

        :param lineage_request: detailing the lineage query, parameters, and so on to run
        :returns: the results of the lineage request
        :raises InvalidRequestError: if the requested lineage direction is 'BOTH' (unsupported for this operation)
        :raises AtlanError: on any API communication issue
        """
        if lineage_request.direction == LineageDirection.BOTH:
            raise ErrorCode.INVALID_LINEAGE_DIRECTION.exception_with_parameters()
        raw_json = self._client._call_api(
            GET_LINEAGE_LIST, None, request_obj=lineage_request, exclude_unset=True
        )
        if "entities" in raw_json:
            try:
                for entity in raw_json["entities"]:
                    unflatten_custom_metadata_for_entity(
                        entity=entity, attributes=lineage_request.attributes
                    )
                assets = parse_obj_as(List[Asset], raw_json["entities"])
                has_more = parse_obj_as(bool, raw_json["hasMore"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            assets = []
            has_more = False
        return LineageListResults(
            client=self._client,
            criteria=lineage_request,
            start=lineage_request.offset or 0,
            size=lineage_request.size or 10,
            has_more=has_more,
            assets=assets,
        )

    @validate_arguments
    def find_personas_by_name(
        self,
        name: str,
        attributes: Optional[List[str]] = None,
    ) -> List[Persona]:
        """
        Find a persona by its human-readable name.

        :param name: of the persona
        :param attributes: (optional) collection of attributes to retrieve for the persona
        :returns: all personas with that name, if found
        :raises NotFoundError: if no persona with the provided name exists
        """
        if attributes is None:
            attributes = []
        query = (
            Term.with_state("ACTIVE")
            + Term.with_type_name("PERSONA")
            + Term.with_name(name)
        )
        return self._search_for_asset_with_name(
            query=query,
            name=name,
            asset_type=Persona,
            attributes=attributes,
            allow_multiple=True,
        )

    @validate_arguments
    def find_purposes_by_name(
        self,
        name: str,
        attributes: Optional[List[str]] = None,
    ) -> List[Purpose]:
        """
        Find a purpose by its human-readable name.

        :param name: of the purpose
        :param attributes: (optional) collection of attributes to retrieve for the purpose
        :returns: all purposes with that name, if found
        :raises NotFoundError: if no purpose with the provided name exists
        """
        if attributes is None:
            attributes = []
        query = (
            Term.with_state("ACTIVE")
            + Term.with_type_name("PURPOSE")
            + Term.with_name(name)
        )
        return self._search_for_asset_with_name(
            query=query,
            name=name,
            asset_type=Purpose,
            attributes=attributes,
            allow_multiple=True,
        )

    @validate_arguments
    def get_by_qualified_name(
        self,
        qualified_name: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> A:
        """
        Retrieves an asset by its qualified_name.

        :param qualified_name: qualified_name of the asset to be retrieved
        :param asset_type: type of asset to be retrieved ( must be the actual asset type not a super type)
        :param min_ext_info: whether to minimize extra info (True) or not (False)
        :param ignore_relationships: whether to include relationships (False) or exclude them (True)
        :returns: the requested asset
        :raises NotFoundError: if the asset does not exist
        :raises AtlanError: on any API communication issue
        """
        query_params = {
            "attr:qualifiedName": qualified_name,
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }
        raw_json = self._client._call_api(
            GET_ENTITY_BY_UNIQUE_ATTRIBUTE.format_path_with_params(asset_type.__name__),
            query_params,
        )
        if raw_json["entity"]["typeName"] != asset_type.__name__:
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                asset_type.__name__, qualified_name
            )
        asset = self._handle_relationships(raw_json)
        if not isinstance(asset, asset_type):
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                asset_type.__name__, qualified_name
            )
        return asset

    @validate_arguments
    def get_by_guid(
        self,
        guid: str,
        asset_type: Type[A] = Asset,  # type: ignore[assignment]
        min_ext_info: bool = False,
        ignore_relationships: bool = False,
    ) -> A:
        """
        Retrieves an asset by its GUID.

        :param guid: unique identifier (GUID) of the asset to retrieve
        :param asset_type: type of asset to be retrieved, defaults to `Asset`
        :param min_ext_info: whether to minimize extra info (True) or not (False)
        :param ignore_relationships: whether to include relationships (False) or exclude them (True)
        :returns: the requested asset
        :raises NotFoundError: if the asset does not exist, or is not of the type requested
        :raises AtlanError: on any API communication issue
        """
        query_params = {
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }

        raw_json = self._client._call_api(
            GET_ENTITY_BY_GUID.format_path_with_params(guid),
            query_params,
        )
        asset = self._handle_relationships(raw_json)
        if not isinstance(asset, asset_type):
            raise ErrorCode.ASSET_NOT_TYPE_REQUESTED.exception_with_parameters(
                guid, asset_type.__name__
            )
        return asset

    def _handle_relationships(self, raw_json):
        if (
            "relationshipAttributes" in raw_json["entity"]
            and raw_json["entity"]["relationshipAttributes"]
        ):
            raw_json["entity"]["attributes"].update(
                raw_json["entity"]["relationshipAttributes"]
            )
        raw_json["entity"]["relationshipAttributes"] = {}
        asset = AssetResponse[A](**raw_json).entity
        asset.is_incomplete = False
        return asset

    @validate_arguments
    def retrieve_minimal(
        self, guid: str, asset_type: Type[A] = Asset  # type: ignore[assignment]
    ) -> A:
        """
        Retrieves an asset by its GUID, without any of its relationships.

        :param guid: unique identifier (GUID) of the asset to retrieve
        :param asset_type: type of asset to be retrieved, defaults to `Asset`
        :returns: the asset, without any of its relationships
        :raises NotFoundError: if the asset does not exist
        """
        return self.get_by_guid(
            guid=guid,
            asset_type=asset_type,
            min_ext_info=True,
            ignore_relationships=True,
        )

    @validate_arguments
    def upsert(
        self,
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        """Deprecated - use save() instead."""
        warn(
            "This method is deprecated, please use 'save' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
        )

    @validate_arguments
    def save(
        self,
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
    ) -> AssetMutationResponse:
        """
        If an asset with the same qualified_name exists, updates the existing asset. Otherwise, creates the asset.
        If an asset does exist, opertionally overwrites any Atlan tags. Custom metadata will either be
        overwritten or merged depending on the options provided.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :param replace_custom_metadata: replaces any custom metadata with non-empty values provided
        :param overwrite_custom_metadata: overwrites any custom metadata, even with empty values
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        :raises ApiError: if a connection was created and blocking until policies are synced overruns the retry limit
        """
        query_params = {
            "replaceClassifications": replace_atlan_tags,
            "replaceBusinessAttributes": replace_custom_metadata,
            "overwriteBusinessAttributes": overwrite_custom_metadata,
        }
        entities: List[Asset] = []
        if isinstance(entity, list):
            entities.extend(entity)
        else:
            entities.append(entity)
        for asset in entities:
            asset.validate_required()
        request = BulkRequest[Asset](entities=entities)
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request)
        response = AssetMutationResponse(**raw_json)
        if connections_created := response.assets_created(Connection):
            self._wait_for_connections_to_be_created(connections_created)
        return response

    def _wait_for_connections_to_be_created(self, connections_created):
        with self._client.max_retries():
            LOGGER.debug("Waiting for connections")
            for connection in connections_created:
                guid = connection.guid
                LOGGER.debug("Attempting to retrieve connection with guid: %s", guid)
                self.retrieve_minimal(guid=guid, asset_type=Connection)
            LOGGER.debug("Finished waiting for connections")

    @validate_arguments
    def upsert_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use save_merging_cm() instead."""
        warn(
            "This method is deprecated, please use 'save_merging_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    def save_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, has the same behavior as the upsert() method, while also setting
        any custom metadata provided. If an asset does exist, optionally overwrites any Atlan tags.
        Will merge any provided custom metadata with any custom metadata that already exists on the asset.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the created or updated assets
        """
        return self.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=True,
            overwrite_custom_metadata=False,
        )

    @validate_arguments
    def update_merging_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, fails with a NotFoundError. Will merge any provided
        custom metadata with any custom metadata that already exists on the asset.
        If an asset does exist, optionally overwrites any Atlan tags.

        :param entity: the asset to update
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the updated asset
        :raises NotFoundError: if the asset does not exist (will not create it)
        """
        self.get_by_qualified_name(
            qualified_name=entity.qualified_name or "",
            asset_type=type(entity),
            min_ext_info=True,
            ignore_relationships=True,
        )  # Allow this to throw the NotFoundError if the entity does not exist
        return self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    def upsert_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tagss: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use save_replacing_cm() instead."""
        warn(
            "This method is deprecated, please use 'save_replacing_cm' instead, which offers identical "
            "functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tagss
        )

    @validate_arguments
    def save_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, has the same behavior as the upsert() method, while also setting
        any custom metadata provided.
        If an asset does exist, optionally overwrites any Atlan tags.
        Will overwrite all custom metadata on any existing asset with only the custom metadata provided
        (wiping out any other custom metadata on an existing asset that is not provided in the request).

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the created or updated assets
        :raises AtlanError: on any API communication issue
        """

        query_params = {
            "replaceClassifications": replace_atlan_tags,
            "replaceBusinessAttributes": True,
            "overwriteBusinessAttributes": True,
        }
        entities: List[Asset] = []
        if isinstance(entity, list):
            entities.extend(entity)
        else:
            entities.append(entity)
        for asset in entities:
            asset.validate_required()
        request = BulkRequest[Asset](entities=entities)
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request)
        return AssetMutationResponse(**raw_json)

    @validate_arguments
    def update_replacing_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, fails with a NotFoundError.
        Will overwrite all custom metadata on any existing asset with only the custom metadata provided
        (wiping out any other custom metadata on an existing asset that is not provided in the request).
        If an asset does exist, optionally overwrites any Atlan tags.

        :param entity: the asset to update
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :returns: details of the updated asset
        :raises NotFoundError: if the asset does not exist (will not create it)
        """

        self.get_by_qualified_name(
            qualified_name=entity.qualified_name or "",
            asset_type=type(entity),
            min_ext_info=True,
            ignore_relationships=True,
        )  # Allow this to throw the NotFoundError if the entity does not exist
        return self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    def purge_by_guid(self, guid: Union[str, List[str]]) -> AssetMutationResponse:
        """
        Hard-deletes (purges) one or more assets by their unique identifier (GUID).
        This operation is irreversible.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to hard-delete
        :returns: details of the hard-deleted asset(s)
        :raises AtlanError: on any API communication issue
        """
        guids: List[str] = []
        if isinstance(guid, list):
            guids.extend(guid)
        else:
            guids.append(guid)
        query_params = {"deleteType": AtlanDeleteType.PURGE.value, "guid": guids}
        raw_json = self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        return AssetMutationResponse(**raw_json)

    @validate_arguments
    def delete_by_guid(self, guid: Union[str, List[str]]) -> AssetMutationResponse:
        """
        Soft-deletes (archives) one or more assets by their unique identifier (GUID).
        This operation can be reversed by updating the asset and its status to ACTIVE.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to soft-delete
        :returns: details of the soft-deleted asset(s)
        :raises AtlanError: on any API communication issue
        :raises ApiError: if the retry limit is overrun waiting for confirmation the asset is deleted
        :raises InvalidRequestError: if an asset does not support archiving
        """
        guids: List[str] = []
        if isinstance(guid, list):
            guids.extend(guid)
        else:
            guids.append(guid)
        for guid in guids:
            asset = self.retrieve_minimal(guid=guid, asset_type=Asset)
            if not asset.can_be_archived():
                raise ErrorCode.ASSET_CAN_NOT_BE_ARCHIVED.exception_with_parameters(
                    guid, asset.type_name
                )
        query_params = {"deleteType": AtlanDeleteType.SOFT.value, "guid": guids}
        raw_json = self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        response = AssetMutationResponse(**raw_json)
        for asset in response.assets_deleted(asset_type=Asset):
            self._wait_till_deleted(asset)
        return response

    @retry(
        reraise=True,
        retry=(retry_if_exception_type(AtlanError)),
        stop=stop_after_attempt(20),
        wait=wait_fixed(1),
    )
    def _wait_till_deleted(self, asset: Asset):
        try:
            asset = self.retrieve_minimal(guid=asset.guid, asset_type=Asset)
            if asset.status == EntityStatus.DELETED:
                return
        except requests.exceptions.RetryError as err:
            raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from err

    @validate_arguments
    def restore(self, asset_type: Type[A], qualified_name: str) -> bool:
        """
        Restore an archived (soft-deleted) asset to active.

        :param asset_type: type of the asset to restore
        :param qualified_name: of the asset to restore
        :returns: True if the asset is now restored, or False if not
        :raises AtlanError: on any API communication issue
        """
        return self._restore(asset_type, qualified_name, 0)

    def _restore(self, asset_type: Type[A], qualified_name: str, retries: int) -> bool:
        if not asset_type.can_be_archived():
            return False
        existing = self.get_by_qualified_name(
            asset_type=asset_type, qualified_name=qualified_name
        )
        if not existing:
            # Nothing to restore, so cannot be restored
            return False
        elif existing.status is EntityStatus.ACTIVE:
            # Already active, but could be due to the async nature of delete handlers
            if retries < 10:
                time.sleep(2)
                return self._restore(asset_type, qualified_name, retries + 1)
            else:
                # If we have exhausted the retries, though, we will short-circuit
                return True
        else:
            response = self._restore_asset(existing)
            return response is not None and response.guid_assignments is not None

    def _restore_asset(self, asset: Asset) -> AssetMutationResponse:
        to_restore = asset.trim_to_required()
        to_restore.status = EntityStatus.ACTIVE
        query_params = {
            "replaceClassifications": False,
            "replaceBusinessAttributes": False,
            "overwriteBusinessAttributes": False,
        }
        request = BulkRequest[Asset](entities=[to_restore])
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request)
        return AssetMutationResponse(**raw_json)

    def _modify_tags(
        self,
        api: API,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
        propagate: bool = True,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = True,
        restrict_propagation_through_hierarchy: bool = False,
    ) -> None:
        atlan_tags = AtlanTags(
            __root__=[
                AtlanTag(
                    type_name=AtlanTagName(display_text=name),
                    propagate=propagate,
                    remove_propagations_on_entity_delete=remove_propagation_on_delete,
                    restrict_propagation_through_lineage=restrict_lineage_propagation,
                    restrict_propagation_through_hierarchy=restrict_propagation_through_hierarchy,
                )
                for name in atlan_tag_names
            ]
        )
        query_params = {"attr:qualifiedName": qualified_name}
        self._client._call_api(
            api.format_path_with_params(asset_type.__name__, "classifications"),
            query_params,
            atlan_tags,
        )

    @validate_arguments
    def add_atlan_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
        propagate: bool = True,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = True,
        restrict_propagation_through_hierarchy: bool = False,
    ) -> None:
        """
        Add one or more Atlan tags to the provided asset.
        Note: if one or more of the provided Atlan tags already exist on the asset, an error
        will be raised. (In other words, this operation is NOT idempotent.)

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
        :raises AtlanError: on any API communication issue
        """
        self._modify_tags(
            UPDATE_ENTITY_BY_ATTRIBUTE,
            asset_type,
            qualified_name,
            atlan_tag_names,
            propagate,
            remove_propagation_on_delete,
            restrict_lineage_propagation,
            restrict_propagation_through_hierarchy,
        )

    @validate_arguments
    def update_atlan_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
        propagate: bool = True,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = True,
        restrict_propagation_through_hierarchy: bool = False,
    ) -> None:
        """
        Update one or more Atlan tags to the provided asset.
        Note: if one or more of the provided Atlan tags already exist on the asset, an error
        will be raised. (In other words, this operation is NOT idempotent.)

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
        :raises AtlanError: on any API communication issue
        """
        self._modify_tags(
            PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE,
            asset_type,
            qualified_name,
            atlan_tag_names,
            propagate,
            remove_propagation_on_delete,
            restrict_lineage_propagation,
            restrict_propagation_through_hierarchy,
        )

    @validate_arguments
    def remove_atlan_tag(
        self, asset_type: Type[A], qualified_name: str, atlan_tag_name: str
    ) -> None:
        """
        Removes a single Atlan tag from the provided asset.
        Note: if the provided Atlan tag does not exist on the asset, an error will be raised.
        (In other words, this operation is NOT idempotent.)

        :param asset_type: type of asset to which to add the Atlan tags
        :param qualified_name: qualified_name of the asset to which to add the Atlan tags
        :param atlan_tag_name: human-readable name of the Atlan tag to remove from the asset
        :raises AtlanError: on any API communication issue
        """
        from pyatlan.cache.atlan_tag_cache import AtlanTagCache

        classification_id = AtlanTagCache.get_id_for_name(atlan_tag_name)
        if not classification_id:
            raise ErrorCode.ATLAN_TAG_NOT_FOUND_BY_NAME.exception_with_parameters(
                atlan_tag_name
            )
        query_params = {"attr:qualifiedName": qualified_name}
        self._client._call_api(
            DELETE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__, "classification", classification_id
            ),
            query_params,
        )

    def _update_asset_by_attribute(
        self, asset: A, asset_type: Type[A], qualified_name: str
    ):
        query_params = {"attr:qualifiedName": qualified_name}
        raw_json = self._client._call_api(
            PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
                asset_type.__name__
            ),
            query_params,
            AssetRequest[Asset](entity=asset),
        )
        response = AssetMutationResponse(**raw_json)
        if assets := response.assets_partially_updated(asset_type=asset_type):
            return assets[0]
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return None

    def _update_glossary_anchor(
        self,
        asset: Union[AtlasGlossaryTerm, AtlasGlossaryCategory],
        asset_type: str,
        glossary_guid: Optional[str] = None,
    ) -> None:
        if not glossary_guid:
            raise ErrorCode.MISSING_GLOSSARY_GUID.exception_with_parameters(asset_type)
        asset.anchor = AtlasGlossary.ref_by_guid(glossary_guid)

    @overload
    def update_certificate(
        self,
        asset_type: Type[AtlasGlossaryTerm],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        glossary_guid: str,
        message: Optional[str] = None,
    ) -> Optional[AtlasGlossaryTerm]: ...

    @overload
    def update_certificate(
        self,
        asset_type: Type[AtlasGlossaryCategory],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        glossary_guid: str,
        message: Optional[str] = None,
    ) -> Optional[AtlasGlossaryCategory]: ...

    @overload
    def update_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        glossary_guid: Optional[str] = None,
        message: Optional[str] = None,
    ) -> Optional[A]: ...

    @validate_arguments
    def update_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        glossary_guid: Optional[str] = None,
        message: Optional[str] = None,
    ) -> Optional[A]:
        """
        Update the certificate on an asset.

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
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.certificate_status = certificate_status
        asset.name = name
        asset.certificate_status_message = message
        if isinstance(asset, (AtlasGlossaryTerm, AtlasGlossaryCategory)):
            self._update_glossary_anchor(asset, asset_type.__name__, glossary_guid)
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @overload
    def remove_certificate(
        self,
        asset_type: Type[AtlasGlossaryTerm],
        qualified_name: str,
        name: str,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryTerm]: ...

    @overload
    def remove_certificate(
        self,
        asset_type: Type[AtlasGlossaryCategory],
        qualified_name: str,
        name: str,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryCategory]: ...

    @overload
    def remove_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]: ...

    @validate_arguments
    def remove_certificate(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]:
        """
        Remove the certificate from an asset.

        :param asset_type: type of asset from which to remove the certificate
        :param qualified_name: the qualified_name of the asset from which to remove the certificate
        :param name: the name of the asset from which to remove the certificate
        :param glossary_guid: unique identifier of the glossary, required
        only when the asset type is `AtlasGlossaryTerm` or `AtlasGlossaryCategory`
        :returns: the result of the removal, or None if the removal failed
        """
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.name = name
        asset.remove_certificate()
        if isinstance(asset, (AtlasGlossaryTerm, AtlasGlossaryCategory)):
            self._update_glossary_anchor(asset, asset_type.__name__, glossary_guid)
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @overload
    def update_announcement(
        self,
        asset_type: Type[AtlasGlossaryTerm],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryTerm]: ...

    @overload
    def update_announcement(
        self,
        asset_type: Type[AtlasGlossaryCategory],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryCategory]: ...

    @overload
    def update_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]: ...

    @validate_arguments
    def update_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]:
        """
        Update the announcement on an asset.

        :param asset_type: type of asset on which to update the announcement
        :param qualified_name: the qualified_name of the asset on which to update the announcement
        :param name: the name of the asset on which to update the announcement
        :param announcement: to apply to the asset
        :param glossary_guid: unique identifier of the glossary, required
        only when the asset type is `AtlasGlossaryTerm` or `AtlasGlossaryCategory`
        :returns: the result of the update, or None if the update failed
        """
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.set_announcement(announcement)
        asset.name = name
        if isinstance(asset, (AtlasGlossaryTerm, AtlasGlossaryCategory)):
            self._update_glossary_anchor(asset, asset_type.__name__, glossary_guid)
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @overload
    def remove_announcement(
        self,
        asset_type: Type[AtlasGlossaryTerm],
        qualified_name: str,
        name: str,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryTerm]: ...

    @overload
    def remove_announcement(
        self,
        asset_type: Type[AtlasGlossaryCategory],
        qualified_name: str,
        name: str,
        glossary_guid: str,
    ) -> Optional[AtlasGlossaryCategory]: ...

    @overload
    def remove_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]: ...

    @validate_arguments
    def remove_announcement(
        self,
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ) -> Optional[A]:
        """
        Remove the announcement from an asset.

        :param asset_type: type of asset from which to remove the announcement
        :param qualified_name: the qualified_name of the asset from which to remove the announcement
        :param glossary_guid: unique identifier of the glossary, required
        only when the asset type is `AtlasGlossaryTerm` or `AtlasGlossaryCategory`
        :returns: the result of the removal, or None if the removal failed
        """
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.name = name
        asset.remove_announcement()
        if isinstance(asset, (AtlasGlossaryTerm, AtlasGlossaryCategory)):
            self._update_glossary_anchor(asset, asset_type.__name__, glossary_guid)
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def update_custom_metadata_attributes(
        self, guid: str, custom_metadata: CustomMetadataDict
    ):
        """
        Update only the provided custom metadata attributes on the asset. This will leave all
        other custom metadata attributes, even within the same named custom metadata, unchanged.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to update, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """
        custom_metadata_request = CustomMetadataRequest.create(
            custom_metadata_dict=custom_metadata
        )
        self._client._call_api(
            ADD_BUSINESS_ATTRIBUTE_BY_ID.format_path(
                {
                    "entity_guid": guid,
                    "bm_id": custom_metadata_request.custom_metadata_set_id,
                }
            ),
            None,
            custom_metadata_request,
        )

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def replace_custom_metadata(self, guid: str, custom_metadata: CustomMetadataDict):
        """
        Replace specific custom metadata on the asset. This will replace everything within the named
        custom metadata, but will not change any of hte other named custom metadata on the asset.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to replace, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """
        # clear unset attributes so that they are removed
        custom_metadata.clear_unset()
        custom_metadata_request = CustomMetadataRequest.create(
            custom_metadata_dict=custom_metadata
        )
        self._client._call_api(
            ADD_BUSINESS_ATTRIBUTE_BY_ID.format_path(
                {
                    "entity_guid": guid,
                    "bm_id": custom_metadata_request.custom_metadata_set_id,
                }
            ),
            None,
            custom_metadata_request,
        )

    @validate_arguments
    def remove_custom_metadata(self, guid: str, cm_name: str):
        """
        Remove specific custom metadata from an asset.

        :param guid: unique identifier (GUID) of the asset
        :param cm_name: human-readable name of the custom metadata to remove
        :raises AtlanError: on any API communication issue
        """
        custom_metadata = CustomMetadataDict(name=cm_name)
        # invoke clear_all so all attributes are set to None and consequently removed
        custom_metadata.clear_all()
        custom_metadata_request = CustomMetadataRequest.create(
            custom_metadata_dict=custom_metadata
        )
        self._client._call_api(
            ADD_BUSINESS_ATTRIBUTE_BY_ID.format_path(
                {
                    "entity_guid": guid,
                    "bm_id": custom_metadata_request.custom_metadata_set_id,
                }
            ),
            None,
            custom_metadata_request,
        )

    @validate_arguments
    def append_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Link additional terms to an asset, without replacing existing terms linked to the asset.
        Note: this operation must make two API calls — one to retrieve the asset's existing terms,
        and a second to append the new terms. (At least one of the GUID or qualified_name must be
        supplied, but both are not necessary.)

        :param asset_type: type of the asset
        :param terms: the list of terms to append to the asset
        :param guid: unique identifier (GUID) of the asset to which to link the terms
        :param qualified_name: the qualified_name of the asset to which to link the terms
        :returns: the asset that was updated (note that it will NOT contain details of the appended terms)
        """
        if guid:
            if qualified_name:
                raise ErrorCode.QN_OR_GUID_NOT_BOTH.exception_with_parameters()
            asset = self.get_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ErrorCode.QN_OR_GUID.exception_with_parameters()
        if not terms:
            return asset
        replacement_terms: List[AtlasGlossaryTerm] = []
        if existing_terms := asset.assigned_terms:
            replacement_terms.extend(
                term for term in existing_terms if term.relationship_status != "DELETED"
            )
        replacement_terms.extend(terms)
        asset.assigned_terms = replacement_terms
        response = self.save(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    @validate_arguments
    def replace_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Replace the terms linked to an asset.
        (At least one of the GUID or qualified_name must be supplied, but both are not necessary.)

        :param asset_type: type of the asset
        :param terms: the list of terms to replace on the asset, or an empty list to remove all terms from an asset
        :param guid: unique identifier (GUID) of the asset to which to replace the terms
        :param qualified_name: the qualified_name of the asset to which to replace the terms
        :returns: the asset that was updated (note that it will NOT contain details of the replaced terms)
        """
        if guid:
            if qualified_name:
                raise ErrorCode.QN_OR_GUID_NOT_BOTH.exception_with_parameters()
            asset = self.get_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ErrorCode.QN_OR_GUID.exception_with_parameters()
        asset.assigned_terms = terms
        response = self.save(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    @validate_arguments
    def remove_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Remove terms from an asset, without replacing all existing terms linked to the asset.
        Note: this operation must make two API calls — one to retrieve the asset's existing terms,
        and a second to remove the provided terms.

        :param asset_type: type of the asset
        :param terms: the list of terms to remove from the asset (note: these must be references by GUID to efficiently
                      remove any existing terms)
        :param guid: unique identifier (GUID) of the asset from which to remove the terms
        :param qualified_name: the qualified_name of the asset from which to remove the terms
        :returns: the asset that was updated (note that it will NOT contain details of the resulting terms)
        """
        if not terms:
            raise ErrorCode.MISSING_TERMS.exception_with_parameters()
        if guid:
            if qualified_name:
                raise ErrorCode.QN_OR_GUID_NOT_BOTH.exception_with_parameters()
            asset = self.get_by_guid(guid=guid, asset_type=asset_type)
        elif qualified_name:
            asset = self.get_by_qualified_name(
                qualified_name=qualified_name, asset_type=asset_type
            )
        else:
            raise ErrorCode.QN_OR_GUID.exception_with_parameters()
        replacement_terms: List[AtlasGlossaryTerm] = []
        guids_to_be_removed = {t.guid for t in terms}
        if existing_terms := asset.assigned_terms:
            replacement_terms.extend(
                term
                for term in existing_terms
                if term.relationship_status != "DELETED"
                and term.guid not in guids_to_be_removed
            )
        asset.assigned_terms = replacement_terms
        response = self.save(entity=asset)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return asset

    @validate_arguments
    def find_connections_by_name(
        self,
        name: str,
        connector_type: AtlanConnectorType,
        attributes: Optional[List[str]] = None,
    ) -> List[Connection]:
        """
        Find a connection by its human-readable name and type.

        :param name: of the connection
        :param connector_type: of the connection
        :param attributes: (optional) collection of attributes to retrieve for the connection
        :returns: all connections with that name and type, if found
        :raises NotFoundError: if the connection does not exist
        """
        if attributes is None:
            attributes = []
        query = (
            Term.with_state("ACTIVE")
            + Term.with_type_name("CONNECTION")
            + Term.with_name(name)
            + Term(field="connectorName", value=connector_type.value)
        )
        return self._search_for_asset_with_name(
            query=query,
            name=name,
            asset_type=Connection,
            attributes=attributes,
            allow_multiple=True,
        )

    @validate_arguments
    def find_glossary_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossary:
        """
        Find a glossary by its human-readable name.

        :param name: of the glossary
        :param attributes: (optional) collection of attributes to retrieve for the glossary
        :returns: the glossary, if found
        :raises NotFoundError: if no glossary with the provided name exists
        """
        if attributes is None:
            attributes = []
        query = with_active_glossary(name=name)
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossary, attributes=attributes
        )[0]

    @validate_arguments
    def find_category_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> List[AtlasGlossaryCategory]:
        """
        Find a category by its human-readable name.
        Note: this operation requires first knowing the qualified_name of the glossary in which the
        category exists. Note that categories are not unique by name, so there may be
        multiple results.

        :param name: of the category
        :param glossary_qualified_name: qualified_name of the glossary in which the category exists
        :param attributes: (optional) collection of attributes to retrieve for the category
        :returns: the category, if found
        :raises NotFoundError: if no category with the provided name exists in the glossary
        """
        if attributes is None:
            attributes = []
        query = with_active_category(
            name=name, glossary_qualified_name=glossary_qualified_name
        )
        return self._search_for_asset_with_name(
            query=query,
            name=name,
            asset_type=AtlasGlossaryCategory,
            attributes=attributes,
            allow_multiple=True,
        )

    @validate_arguments
    def find_category_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> List[AtlasGlossaryCategory]:
        """
        Find a category by its human-readable name.
        Note: this operation must run two separate queries to first resolve the qualified_name of the
        glossary, so will be somewhat slower. If you already have the qualified_name of the glossary, use
        find_category_by_name_fast instead. Note that categories are not unique by name, so there may be
        multiple results.

        :param name: of the category
        :param glossary_name: human-readable name of the glossary in which the category exists
        :param attributes: (optional) collection of attributes to retrieve for the category
        :returns: the category, if found
        :raises NotFoundError: if no category with the provided name exists in the glossary
        """
        glossary = self.find_glossary_by_name(name=glossary_name)
        return self.find_category_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )

    def _search_for_asset_with_name(
        self,
        query: Query,
        name: str,
        asset_type: Type[A],
        attributes: Optional[List[StrictStr]],
        allow_multiple: bool = False,
    ) -> List[A]:
        dsl = DSL(query=query)
        search_request = IndexSearchRequest(
            dsl=dsl, attributes=attributes, relation_attributes=["name"]
        )
        results = self.search(search_request)
        if (
            results
            and results.count > 0
            and (
                # Check for paginated results first;
                # if not paginated, iterate over the results
                assets := [
                    asset
                    for asset in (results.current_page() or results)
                    if isinstance(asset, asset_type)
                ]
            )
        ):
            if not allow_multiple and len(assets) > 1:
                LOGGER.warning(
                    "More than 1 %s found with the name '%s', returning only the first.",
                    asset_type.__name__,
                    name,
                )
            return assets
        raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
            asset_type.__name__, name
        )

    @validate_arguments
    def find_term_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        """
        Find a term by its human-readable name.
        Note: this operation requires first knowing the qualified_name of the glossary in which the
        term exists.

        :param name: of the term
        :param glossary_qualified_name: qualified_name of the glossary in which the term exists
        :param attributes: (optional) collection of attributes to retrieve for the term
        :returns: the term, if found
        :raises NotFoundError: if no term with the provided name exists in the glossary
        """
        if attributes is None:
            attributes = []
        query = with_active_term(
            name=name, glossary_qualified_name=glossary_qualified_name
        )
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossaryTerm, attributes=attributes
        )[0]

    @validate_arguments
    def find_term_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> AtlasGlossaryTerm:
        """
        Find a term by its human-readable name.
        Note: this operation must run two separate queries to first resolve the qualified_name of the
        glossary, so will be somewhat slower. If you already have the qualified_name of the glossary, use
        find_term_by_name_fast instead.

        :param name: of the term
        :param glossary_name: human-readable name of the glossary in which the term exists
        :param attributes: (optional) collection of attributes to retrieve for the term
        :returns: the term, if found
        :raises NotFoundError: if no term with the provided name exists in the glossary
        """
        glossary = self.find_glossary_by_name(name=glossary_name)
        return self.find_term_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )

    @validate_arguments
    def find_domain_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> DataDomain:
        """
        Find a data domain by its human-readable name.

        :param name: of the domain
        :param attributes: (optional) collection of attributes to retrieve for the domain
        :returns: the domain, if found
        :raises NotFoundError: if no domain with the provided name exists
        """
        attributes = attributes or []
        query = Term.with_name(name) + Term.with_type_name("DataDomain")
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=DataDomain, attributes=attributes
        )[0]

    @validate_arguments
    def find_product_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        attributes: Optional[List[StrictStr]] = None,
    ) -> DataProduct:
        """
        Find a data product by its human-readable name.

        :param name: of the product
        :param attributes: (optional) collection of attributes to retrieve for the product
        :returns: the product, if found
        :raises NotFoundError: if no product with the provided name exists
        """
        attributes = attributes or []
        query = Term.with_name(name) + Term.with_type_name("DataProduct")
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=DataProduct, attributes=attributes
        )[0]

    # TODO: Try adding @validate_arguments to this method once
    # the issue below is fixed or when we switch to pydantic v2
    # https://github.com/pydantic/pydantic/issues/2901
    def get_hierarchy(
        self,
        glossary: AtlasGlossary,
        attributes: Optional[List[Union[AtlanField, str]]] = None,
        related_attributes: Optional[List[Union[AtlanField, str]]] = None,
    ) -> CategoryHierarchy:
        """
        Retrieve category hierarchy in this Glossary, in a traversable form. You can traverse in either depth_first
        or breadth_first order. Both return an ordered list of Glossary objects.
        Note: by default, each category will have a minimal set of information (name, GUID, qualifiedName). If you
        want additional details about each category, specify the attributes you want in the attributes parameter
        of this method.

        :param glossary: the glossary to retrieve the category hierarchy for
        :param attributes: attributes to retrieve for each category in the hierarchy
        :param related_attributes: attributes to retrieve for each related asset in the hierarchy
        :returns: a traversable category hierarchy
        """
        from pyatlan.model.fluent_search import FluentSearch

        if not glossary.qualified_name:
            raise ErrorCode.GLOSSARY_MISSING_QUALIFIED_NAME.exception_with_parameters()
        if attributes is None:
            attributes = []
        if related_attributes is None:
            related_attributes = []
        top_categories: Set[str] = set()
        category_dict: Dict[str, AtlasGlossaryCategory] = {}
        search = (
            FluentSearch.select()
            .where(AtlasGlossaryCategory.ANCHOR.eq(glossary.qualified_name))
            .where(Term.with_type_name("AtlasGlossaryCategory"))
            .include_on_results(AtlasGlossaryCategory.PARENT_CATEGORY)
            .page_size(20)
            .sort(AtlasGlossaryCategory.NAME.order(SortOrder.ASCENDING))
        )
        for field in attributes:
            search = search.include_on_results(field)
        for field in related_attributes:
            search = search.include_on_relations(field)
        request = search.to_request()
        response = self.search(request)
        for category in filter(
            lambda a: isinstance(a, AtlasGlossaryCategory), response
        ):
            guid = category.guid
            category_dict[guid] = category
            if category.parent_category is None:
                top_categories.add(guid)

        if not top_categories:
            raise ErrorCode.NO_CATEGORIES.exception_with_parameters(
                glossary.guid, glossary.qualified_name
            )
        return CategoryHierarchy(top_level=top_categories, stub_dict=category_dict)


class SearchResults(ABC, Iterable):
    """
    Abstract class that encapsulates results returned by various searches.
    """

    def __init__(
        self,
        client: ApiCaller,
        endpoint: API,
        criteria: SearchRequest,
        start: int,
        size: int,
        assets: List[Asset],
    ):
        self._client = client
        self._endpoint = endpoint
        self._criteria = criteria
        self._start = start
        self._size = size
        self._assets = assets

    def current_page(self) -> List[Asset]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._assets

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._assets else False

    @abc.abstractmethod
    def _get_next_page(self):
        """
        Abstract method that must be implemented in subclasses, used to
        fetch the next page of results.
        """

    # TODO Rename this here and in `next_page`
    def _get_next_page_json(self):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "entities" not in raw_json:
            self._assets = []
            return None
        try:
            for entity in raw_json["entities"]:
                unflatten_custom_metadata_for_entity(
                    entity=entity, attributes=self._criteria.attributes
                )
            self._assets = parse_obj_as(List[Asset], raw_json["entities"])
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def __iter__(self) -> Generator[Asset, None, None]:
        """
        Iterates through the results, lazily-fetching each next page until there
        are no more results.

        :returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.next_page():
                break


class IndexSearchResults(SearchResults, Iterable):
    """
    Captures the response from a search against Atlan. Also provides the ability to
    iteratively page through results, without needing to track or re-run the original
    query.
    """

    def __init__(
        self,
        client: ApiCaller,
        criteria: IndexSearchRequest,
        start: int,
        size: int,
        count: int,
        assets: List[Asset],
        aggregations: Optional[Aggregations],
    ):
        super().__init__(client, INDEX_SEARCH, criteria, start, size, assets)
        self._count = count
        self._aggregations = aggregations

    @property
    def aggregations(self) -> Optional[Aggregations]:
        return self._aggregations

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := super()._get_next_page_json():
            self._count = raw_json.get("approximateCount", 0)
            return True
        return False

    @property
    def count(self) -> int:
        return self._count


class LineageListResults(SearchResults, Iterable):
    """
    Captures the response from a lineage retrieval against Atlan. Also provides the ability to
    iteratively page through results, without needing to track or re-run the original query.
    """

    def __init__(
        self,
        client: ApiCaller,
        criteria: LineageListRequest,
        start: int,
        size: int,
        has_more: bool,
        assets: List[Asset],
    ):
        super().__init__(client, GET_LINEAGE_LIST, criteria, start, size, assets)
        self._has_more = has_more

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.offset = self._start
        self._criteria.size = self._size
        if raw_json := super()._get_next_page_json():
            self._has_more = parse_obj_as(bool, raw_json.get("hasMore", False))
            return self._has_more
        return False

    @property
    def has_more(self) -> bool:
        return self._has_more

    def __iter__(self) -> Generator[Asset, None, None]:
        """
        Iterates through the results, lazily-fetching
        each next page until there are no more results.

        :returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.has_more:
                break
            self.next_page()


class CustomMetadataHandling(str, Enum):
    IGNORE = "ignore"
    OVERWRITE = "overwrite"
    MERGE = "merge"


class FailedBatch:
    """Internal class to capture batch failures."""

    failed_assets: List[Asset]
    failure_reason: Exception

    def __init__(self, failed_assets: List[Asset], failure_reason: Exception):
        self.failed_assets = failed_assets
        self.failure_reason = failure_reason


class Batch:
    """Utility class for managing bulk updates in batches."""

    def __init__(
        self,
        client: AssetClient,
        max_size: int,
        replace_atlan_tags: bool = False,
        custom_metadata_handling: CustomMetadataHandling = CustomMetadataHandling.IGNORE,
        capture_failures: bool = False,
    ):
        """
        Create a new batch of assets to be bulk-saved.
        :param client: AssetClient to use
        :param max_size: maximum size of each batch that should be processed (per API call)
        :param replace_atlan_tags: if True, all Atlan tags on an existing asset will be overwritten; if False,
        all Atlan tags will be ignored
        :param custom_metadata_handling:  how to handle custom metadata (ignore it, replace it (wiping out
        anything pre-existing), or merge it)
        :param capture_failures: when True, any failed batches will be captured and retained rather than exceptions
         being raised (for large amounts of processing this could cause memory issues!)
        """
        self._client: AssetClient = client
        self._max_size: int = max_size
        self._replace_atlan_tags: bool = replace_atlan_tags
        self._custom_metadata_handling: CustomMetadataHandling = (
            custom_metadata_handling
        )
        self._capture_failures: bool = capture_failures
        self._batch: List[Asset] = []
        self._failures: List[FailedBatch] = []
        self._created: List[Asset] = []
        self._updated: List[Asset] = []

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

    @validate_arguments
    def add(self, single: Asset) -> Optional[AssetMutationResponse]:
        """
        Add an asset to the batch to be processed.

        :param single: the asset to add to a batch
        :returns: an AssetMutationResponse containing the results of the save or None if the batch is still queued.
        """
        self._batch.append(single)
        return self._process()

    def _process(self) -> Optional[AssetMutationResponse]:
        """If the number of entities we have queued up is equal to the batch size, process them and reset our queue;
        otherwise do nothing.

        :returns: an AssetMutationResponse containing the results of the save or None if the batch is still queued.
        """
        return self.flush() if len(self._batch) == self._max_size else None

    def flush(self) -> Optional[AssetMutationResponse]:
        """Flush any remaining assets in the batch.

        :returns: n AssetMutationResponse containing the results of the saving any assets that were flushed
        """
        response: Optional[AssetMutationResponse] = None
        if self._batch:
            try:
                if self._custom_metadata_handling == CustomMetadataHandling.IGNORE:
                    response = self._client.save(
                        self._batch, replace_atlan_tags=self._replace_atlan_tags
                    )
                elif self._custom_metadata_handling == CustomMetadataHandling.OVERWRITE:
                    response = self._client.save_replacing_cm(
                        self._batch, replace_atlan_tags=self._replace_atlan_tags
                    )
                elif self._custom_metadata_handling == CustomMetadataHandling.MERGE:
                    response = self._client.save_merging_cm(
                        self._batch, replace_atlan_tags=self._replace_atlan_tags
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
        if response:
            self._track_response(response=response)
        return response

    def _track_response(self, response: AssetMutationResponse):
        if response and response.mutated_entities:
            if response.mutated_entities.CREATE:
                for asset in response.mutated_entities.CREATE:
                    self._track(self._created, asset)
            if response.mutated_entities.UPDATE:
                for asset in response.mutated_entities.UPDATE:
                    self._track(self._updated, asset)

    @staticmethod
    def _track(tracker: List[Asset], candidate: Asset):
        asset = candidate.trim_to_required()
        asset.name = candidate.name
        tracker.append(asset)


def _bfs(bfs_list: List[AtlasGlossaryCategory], to_add: List[AtlasGlossaryCategory]):
    for nade in to_add:
        bfs_list.extend(nade.children_categories or [])
    for node in to_add:
        _bfs(bfs_list, node.children_categories or [])


def _dfs(dfs_list: List[AtlasGlossaryCategory], to_add: List[AtlasGlossaryCategory]):
    for node in to_add:
        dfs_list.append(node)
        _dfs(dfs_list=dfs_list, to_add=node.children_categories or [])


class CategoryHierarchy:
    def __init__(
        self, top_level: Set[str], stub_dict: Dict[str, AtlasGlossaryCategory]
    ):
        self._top_level = top_level
        self._root_categories: list = []
        self._categories: Dict[str, AtlasGlossaryCategory] = {}
        self._build_category_dict(stub_dict)
        self._bfs_list: List[AtlasGlossaryCategory] = []
        self._dfs_list: List[AtlasGlossaryCategory] = []

    def _build_category_dict(self, stub_dict: Dict[str, AtlasGlossaryCategory]):
        for category in stub_dict.values():
            if parent := category.parent_category:
                parent_guid = parent.guid
                full_parent = self._categories.get(parent_guid, stub_dict[parent_guid])
                children: List[AtlasGlossaryCategory] = (
                    []
                    if full_parent.children_categories is None
                    else full_parent.children_categories.copy()
                )
                if category not in children:
                    children.append(category)
                full_parent.children_categories = children
                self._categories[parent_guid] = full_parent
            self._categories[category.guid] = category

    @validate_arguments
    def get_category(self, guid: str) -> AtlasGlossaryCategory:
        """
        Retrieve a specific category from anywhere in the hierarchy by its unique identifier (GUID).

        :param guid: guid of the category to retrieve
        :returns: the requested category
        """
        return self._categories[guid]

    @property
    def root_categories(self) -> List[AtlasGlossaryCategory]:
        """
        Retrieve only the root-level categories (those with no parents).

        :returns: the root-level categories of the Glossary
        """
        if not self._root_categories:
            self._root_categories = [self._categories[guid] for guid in self._top_level]
        return self._root_categories

    @property
    def breadth_first(self) -> List[AtlasGlossaryCategory]:
        """
        Retrieve all the categories in the hierarchy in breadth-first traversal order.

        :returns: all categories in breadth-first order
        """
        if not self._bfs_list:
            top = self.root_categories
            bfs_list = top.copy()
            _bfs(bfs_list=bfs_list, to_add=top)
            self._bfs_list = bfs_list
        return self._bfs_list

    @property
    def depth_first(self) -> List[AtlasGlossaryCategory]:
        """
        Retrieve all the categories in the hierarchy in depth-first traversal order.

        :returns: all categories in depth-first order
        """
        if not self._dfs_list:
            dfs_list: List[AtlasGlossaryCategory] = []
            _dfs(dfs_list=dfs_list, to_add=self.root_categories)
            self._dfs_list = dfs_list
        return self._dfs_list
