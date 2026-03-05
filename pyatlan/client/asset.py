# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import abc
import logging
import time
from abc import ABC
from enum import Enum
from typing import (
    TYPE_CHECKING,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Protocol,
    Set,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)
from warnings import warn

from pydantic.v1 import (
    StrictStr,
    ValidationError,
    constr,
    parse_obj_as,
    validate_arguments,
)
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
)

from pyatlan.client.common import (
    ApiCaller,
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
    ReplaceCustomMetadata,
    RestoreAsset,
    Save,
    Search,
    SearchForAssetWithName,
    UpdateAnnouncement,
    UpdateAsset,
    UpdateAssetByAttribute,
    UpdateCertificate,
    UpdateCustomMetadataAttributes,
)
from pyatlan.client.constants import (
    BULK_UPDATE,
    DELETE_ENTITIES_BY_GUIDS,
    GET_LINEAGE_LIST,
    INDEX_SEARCH,
)
from pyatlan.errors import AtlanError, ErrorCode, NotFoundError, PermissionError
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
from pyatlan.model.core import Announcement, AtlanObject, SearchRequest
from pyatlan.model.custom_metadata import CustomMetadataDict
from pyatlan.model.enums import (
    AssetCreationHandling,
    AtlanConnectorType,
    AtlanDeleteType,
    CertificateStatus,
    DataQualityScheduleType,
    EntityStatus,
    SaveSemantic,
    SortOrder,
)
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.lineage import LineageListRequest
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.search import DSL, Bool, IndexSearchRequest, Query, Range, SortItem
from pyatlan.utils import API, unflatten_custom_metadata_for_entity

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

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


class IndexSearchRequestProvider(Protocol):
    def to_request(self) -> IndexSearchRequest:
        pass


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
    def search(self, criteria: IndexSearchRequest, bulk=False) -> IndexSearchResults:
        """
        Search for assets using the provided criteria.
        `Note:` if the number of results exceeds the predefined threshold
        (100,000 assets) this will be automatically converted into a `bulk` search.

        :param criteria: detailing the search query, parameters, and so on to run
        :param bulk: whether to run the search to retrieve assets that match the supplied criteria,
        for large numbers of results (> `100,000`), defaults to `False`. Note: this will reorder the results
        (based on creation timestamp) in order to iterate through a large number (more than `100,000`) results.
        :raises InvalidRequestError:

            - if bulk search is enabled (`bulk=True`) and any
              user-specified sorting options are found in the search request.
            - if bulk search is disabled (`bulk=False`) and the number of results
              exceeds the predefined threshold (i.e: `100,000` assets)
              and any user-specified sorting options are found in the search request.

        :raises AtlanError: on any API communication issue
        :returns: the results of the search
        """
        endpoint, request_obj = Search.prepare_request(criteria, bulk)
        raw_json = self._client._call_api(
            endpoint,
            request_obj=request_obj,
        )
        response = Search.process_response(raw_json, criteria)
        if Search._check_for_bulk_search(criteria, response["count"], bulk):
            return self.search(criteria)
        return IndexSearchResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=response["count"],
            assets=response["assets"],
            aggregations=response["aggregations"],
            bulk=bulk,
        )

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
        endpoint, request_obj = GetLineageList.prepare_request(lineage_request)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        response = GetLineageList.process_response(raw_json, lineage_request)
        return LineageListResults(
            client=self._client,
            criteria=lineage_request,
            start=lineage_request.offset or 0,
            size=lineage_request.size or 10,
            has_more=response["has_more"],
            assets=response["assets"],
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
        search_request = FindPersonasByName.prepare_request(name, attributes)
        search_results = self.search(search_request)
        return FindPersonasByName.process_response(
            search_results, name, allow_multiple=True
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
        search_request = FindPurposesByName.prepare_request(name, attributes)
        search_results = self.search(search_request)
        return FindPurposesByName.process_response(
            search_results, name, allow_multiple=True
        )

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def get_by_qualified_name(
        self,
        qualified_name: str,
        asset_type: Type[A],
        min_ext_info: bool = False,
        ignore_relationships: bool = True,
        attributes: Optional[Union[List[str], List[AtlanField]]] = None,
        related_attributes: Optional[Union[List[str], List[AtlanField]]] = None,
    ) -> A:
        """
        Retrieves an asset by its qualified_name.

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
            results = search.execute(client=self._client)  # type: ignore[arg-type]
            return GetByQualifiedName.process_fluent_search_response(
                results, qualified_name, asset_type
            )

        # Use direct API call for simple requests
        endpoint_path, query_params = GetByQualifiedName.prepare_direct_api_request(
            qualified_name, asset_type, min_ext_info, ignore_relationships
        )
        raw_json = self._client._call_api(endpoint_path, query_params)
        return GetByQualifiedName.process_direct_api_response(
            raw_json, qualified_name, asset_type
        )

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def get_by_guid(
        self,
        guid: str,
        asset_type: Type[A] = Asset,  # type: ignore[assignment]
        min_ext_info: bool = False,
        ignore_relationships: bool = True,
        attributes: Optional[Union[List[str], List[AtlanField]]] = None,
        related_attributes: Optional[Union[List[str], List[AtlanField]]] = None,
    ) -> A:
        """
        Retrieves an asset by its GUID.

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
            results = search.execute(client=self._client)  # type: ignore[arg-type]
            return GetByGuid.process_fluent_search_response(results, guid, asset_type)

        # Use direct API call for simple requests
        endpoint_path, query_params = GetByGuid.prepare_direct_api_request(
            guid, min_ext_info, ignore_relationships
        )
        raw_json = self._client._call_api(endpoint_path, query_params)
        return GetByGuid.process_direct_api_response(raw_json, guid, asset_type)

    @validate_arguments
    def retrieve_minimal(
        self,
        guid: str,
        asset_type: Type[A] = Asset,  # type: ignore[assignment]
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
        append_atlan_tags: bool = False,
    ) -> AssetMutationResponse:
        """
        If an asset with the same qualified_name exists, updates the existing asset. Otherwise, creates the asset.
        If an asset does exist, opertionally overwrites any Atlan tags. Custom metadata will either be
        overwritten or merged depending on the options provided.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :param replace_custom_metadata: replaces any custom metadata with non-empty values provided
        :param overwrite_custom_metadata: overwrites any custom metadata, even with empty values
        :param append_atlan_tags: whether to add/update/remove AtlanTags during an update (True) or not (False)
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        :raises ApiError: if a connection was created and blocking until policies are synced overruns the retry limit
        """
        query_params, request = Save.prepare_request(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
            append_atlan_tags=append_atlan_tags,
            client=self._client,  # type: ignore[arg-type]
        )
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request)
        response = Save.process_response(raw_json)
        if connections_created := response.assets_created(Connection):
            self._wait_for_connections_to_be_created(connections_created)
        return response

    def _wait_for_connections_to_be_created(self, connections_created):
        guids = Save.get_connection_guids_to_wait_for(connections_created)

        @retry(
            retry=retry_if_exception_type(PermissionError),
            wait=wait_exponential(multiplier=1, min=1, max=8),
            stop=stop_after_attempt(10),
            reraise=True,
        )
        def _retrieve_connection_with_retry(guid):
            """Retry connection retrieval on permission errors."""
            self.retrieve_minimal(guid=guid, asset_type=Connection)

        # Wait for each connection to be fully created and accessible
        for guid in guids:
            _retrieve_connection_with_retry(guid)

        Save.log_connections_finished()

    @validate_arguments
    def upsert_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use save_merging_cm() instead."""
        warn(
            "This method is deprecated, please use 'save_merging_cm' instead, which offers identical functionality.",
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
        UpdateAsset.validate_asset_exists(
            qualified_name=entity.qualified_name or "",
            asset_type=type(entity),
            get_by_qualified_name_func=self.get_by_qualified_name,
        )
        return self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    def upsert_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use save_replacing_cm() instead."""
        warn(
            "This method is deprecated, please use 'save_replacing_cm' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
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
        query_params, request = Save.prepare_request_replacing_cm(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            client=self._client,  # type: ignore[arg-type]
        )
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request)
        return Save.process_response_replacing_cm(raw_json)

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
        UpdateAsset.validate_asset_exists(
            qualified_name=entity.qualified_name or "",
            asset_type=type(entity),
            get_by_qualified_name_func=self.get_by_qualified_name,
        )
        return self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    def purge_by_guid(
        self,
        guid: Union[str, List[str]],
        delete_type: AtlanDeleteType = AtlanDeleteType.PURGE,
    ) -> AssetMutationResponse:
        """
        Deletes one or more assets by their unique identifier (GUID) using the specified delete type.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to delete
        :param delete_type: type of deletion to perform:

            - PURGE: completely removes entity and all audit/history traces (default, irreversible)
            - HARD: physically removes entity but keeps audit history (irreversible)

        :returns: details of the deleted asset(s)
        :raises AtlanError: on any API communication issue

        .. warning::
            PURGE and HARD deletions are irreversible operations. Use with caution.
        """
        query_params = PurgeByGuid.prepare_request(guid, delete_type)
        raw_json = self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        return PurgeByGuid.process_response(raw_json)

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
        guids = DeleteByGuid.prepare_request(guid)

        # Validate each asset can be archived
        assets = []
        for single_guid in guids:
            asset = self.retrieve_minimal(guid=single_guid, asset_type=Asset)
            assets.append(asset)
        DeleteByGuid.validate_assets_can_be_archived(assets)

        # Perform the deletion
        query_params = DeleteByGuid.prepare_delete_request(guids)
        raw_json = self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        response = DeleteByGuid.process_response(raw_json)

        # Wait for deletion confirmation
        for asset in DeleteByGuid.get_deleted_assets(response):
            try:
                self._wait_till_deleted(asset)
            except RetryError as err:
                raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from err
        return response

    @retry(
        reraise=True,
        retry=(retry_if_exception_type(AtlanError)),
        stop=stop_after_attempt(20),
        wait=wait_fixed(1),
    )
    def _wait_till_deleted(self, asset: Asset):
        asset = self.retrieve_minimal(guid=asset.guid, asset_type=Asset)
        if asset.status == EntityStatus.DELETED:
            return

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
        if not RestoreAsset.can_asset_type_be_archived(asset_type):
            return False

        existing = self.get_by_qualified_name(
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
                time.sleep(2)
                return self._restore(asset_type, qualified_name, retries + 1)
            else:
                # If we have exhausted the retries, though, we will short-circuit
                return True
        else:
            response = self._restore_asset(existing)
            return RestoreAsset.is_restore_successful(response)

    def _restore_asset(self, asset: Asset) -> AssetMutationResponse:
        query_params, request = RestoreAsset.prepare_restore_request(asset)
        # Flush custom metadata for the restored asset
        for restored_asset in request.entities:
            restored_asset.flush_custom_metadata(self._client)  # type: ignore[arg-type]
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request)
        return RestoreAsset.process_restore_response(raw_json)

    def _modify_tags(
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
        Shared method for tag modifications using shared business logic.

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
        def _get_asset_with_retry():
            return self.get_by_qualified_name(
                qualified_name=qualified_name,
                asset_type=asset_type,
                attributes=ModifyAtlanTags.get_retrieve_attributes(),
            )

        retrieved_asset = _get_asset_with_retry()

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
        response = self.save(entity=updated_asset, **save_parameters)

        # Process the response using shared logic
        return ModifyAtlanTags.process_save_response(
            response, asset_type, updated_asset
        )

    @validate_arguments
    def add_atlan_tags(
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
        Add one or more Atlan tags to the provided asset.

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
        return self._modify_tags(
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
    def update_atlan_tags(
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
        Update one or more Atlan tags to the provided asset.

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
        return self._modify_tags(
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
    def remove_atlan_tag(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_name: str,
    ) -> A:
        """
        Removes a single Atlan tag from the provided asset.

        :param asset_type: type of asset to which to add the Atlan tags
        :param qualified_name: qualified_name of the asset to which to add the Atlan tags
        :param atlan_tag_name: human-readable name of the Atlan tag to remove from the asset
        :returns: the asset that was updated (note that it will NOT contain details of the deleted Atlan tag)
        :raises AtlanError: on any API communication issue
        """
        return self._modify_tags(
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
    def remove_atlan_tags(
        self,
        asset_type: Type[A],
        qualified_name: str,
        atlan_tag_names: List[str],
    ) -> A:
        """
        Removes one or more Atlan tag from the provided asset.

        :param asset_type: type of asset to which to add the Atlan tags
        :param qualified_name: qualified_name of the asset to which to add the Atlan tags
        :param atlan_tag_names: human-readable name of the Atlan tag to remove from the asset
        :returns: the asset that was updated (note that it will NOT contain details of the deleted Atlan tags)
        :raises AtlanError: on any API communication issue
        """
        return self._modify_tags(
            asset_type=asset_type,
            qualified_name=qualified_name,
            atlan_tag_names=atlan_tag_names,
            modification_type="remove",
            save_parameters={
                "replace_atlan_tags": False,
                "append_atlan_tags": True,
            },
        )

    def _update_asset_by_attribute(
        self, asset: A, asset_type: Type[A], qualified_name: str
    ) -> Optional[A]:
        """
        Shared method for updating assets by attribute using shared business logic.

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

        # Make API call
        raw_json = self._client._call_api(endpoint, query_params, request_body)

        # Process response using shared logic
        return UpdateAssetByAttribute.process_response(raw_json, asset_type)

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

        # Prepare asset for certificate removal using shared logic
        asset = RemoveCertificate.prepare_asset_for_certificate_removal(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            glossary_guid=glossary_guid,
        )

        # Execute update using shared logic
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

        # Prepare asset with announcement using shared logic
        asset = UpdateAnnouncement.prepare_asset_with_announcement(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            announcement=announcement,
            glossary_guid=glossary_guid,
        )

        # Execute update using shared logic
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

        # Prepare asset for announcement removal using shared logic
        asset = RemoveAnnouncement.prepare_asset_for_announcement_removal(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            glossary_guid=glossary_guid,
        )

        # Execute update using shared logic
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def update_custom_metadata_attributes(
        self, guid: str, custom_metadata: CustomMetadataDict
    ):
        """
            ManageCustomMetadata,
            UpdateCustomMetadataAttributes,
        )

        Update only the provided custom metadata attributes on the asset. This will leave all
        other custom metadata attributes, even within the same named custom metadata, unchanged.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to update, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        custom_metadata_request = UpdateCustomMetadataAttributes.prepare_request(
            custom_metadata
        )

        # Get API endpoint using shared logic
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )

        # Make API call
        self._client._call_api(endpoint, None, custom_metadata_request)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def replace_custom_metadata(self, guid: str, custom_metadata: CustomMetadataDict):
        """
        Replace specific custom metadata on the asset. This will replace everything within the named
        custom metadata, but will not change any of hte other named custom metadata on the asset.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to replace, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """

        # Prepare request using shared logic (includes clear_unset())
        custom_metadata_request = ReplaceCustomMetadata.prepare_request(custom_metadata)

        # Get API endpoint using shared logic
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )

        # Make API call
        self._client._call_api(endpoint, None, custom_metadata_request)

    @validate_arguments
    def remove_custom_metadata(self, guid: str, cm_name: str):
        """
        Remove specific custom metadata from an asset.

        :param guid: unique identifier (GUID) of the asset
        :param cm_name: human-readable name of the custom metadata to remove
        :raises AtlanError: on any API communication issue
        """

        # Prepare request using shared logic (includes clear_all())
        custom_metadata_request = RemoveCustomMetadata.prepare_request(
            cm_name, self._client
        )

        # Get API endpoint using shared logic
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )

        # Make API call
        self._client._call_api(endpoint, None, custom_metadata_request)

    def _search_for_asset_with_name(
        self,
        query: Query,
        name: str,
        asset_type: Type[A],
        attributes: Optional[List],
        allow_multiple: bool = False,
    ) -> List[A]:
        """
        Shared method for searching assets by name using shared business logic.

        :param query: query to execute
        :param name: name that was searched for (for error messages)
        :param asset_type: expected asset type
        :param attributes: optional collection of attributes to retrieve
        :param allow_multiple: whether multiple results are allowed
        :returns: list of found assets
        """

        # Build search request using shared logic
        search_request = SearchForAssetWithName.build_search_request(query, attributes)

        # Execute search
        results = self.search(search_request)

        # Process results using shared logic
        return SearchForAssetWithName.process_search_results(
            results, name, asset_type, allow_multiple
        )

    def _manage_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        save_semantic: SaveSemantic,
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        """
        Shared method for managing terms using shared business logic.

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

        results = search_query.execute(client=self._client)  # type: ignore[arg-type]

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
        response = self.save(entity=updated_asset)
        return ManageTerms.process_save_response(response, asset_type, updated_asset)

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
        return self._manage_terms(
            asset_type=asset_type,
            terms=terms,
            save_semantic=SaveSemantic.APPEND,
            guid=guid,
            qualified_name=qualified_name,
        )

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
        return self._manage_terms(
            asset_type=asset_type,
            terms=terms,
            save_semantic=SaveSemantic.REPLACE,
            guid=guid,
            qualified_name=qualified_name,
        )

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
        return self._manage_terms(
            asset_type=asset_type,
            terms=terms,
            save_semantic=SaveSemantic.REMOVE,
            guid=guid,
            qualified_name=qualified_name,
        )

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

        # Build query using shared logic
        query = FindConnectionsByName.build_query(name, connector_type)

        # Execute search using shared logic
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

        # Build query using shared logic
        query = FindGlossaryByName.build_query(name)

        # Execute search using shared logic
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossary, attributes=attributes
        )[0]

    @validate_arguments
    def find_category_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(  # type: ignore
            strip_whitespace=True, min_length=1, strict=True
        ),
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

        # Build query using shared logic
        query = FindCategoryFastByName.build_query(name, glossary_qualified_name)

        # Execute search using shared logic
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
        # First find the glossary by name
        glossary = self.find_glossary_by_name(name=glossary_name)

        # Then find the category in that glossary using the fast method
        return self.find_category_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )

    @validate_arguments
    def find_term_fast_by_name(
        self,
        name: constr(strip_whitespace=True, min_length=1, strict=True),  # type: ignore
        glossary_qualified_name: constr(  # type: ignore
            strip_whitespace=True, min_length=1, strict=True
        ),
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

        # Build query using shared logic
        query = FindTermFastByName.build_query(name, glossary_qualified_name)

        # Execute search using shared logic
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
        # First find the glossary by name
        glossary = self.find_glossary_by_name(name=glossary_name)

        # Then find the term in that glossary using the fast method
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

        # Build query using shared logic
        query = FindDomainByName.build_query(name)

        # Execute search using shared logic
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

        # Build query using shared logic
        query = FindProductByName.build_query(name)

        # Execute search using shared logic
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

        # Validate glossary using shared logic
        GetHierarchy.validate_glossary(glossary)

        # Prepare search request using shared logic
        request = GetHierarchy.prepare_search_request(
            glossary, attributes, related_attributes
        )

        # Execute search
        response = self.search(request)

        # Process results using shared logic
        return GetHierarchy.process_search_results(response, glossary)

    def process_assets(
        self, search: IndexSearchRequestProvider, func: Callable[[Asset], None]
    ) -> int:
        """
        Process assets matching a search query and apply a processing function to each unique asset.

        This function iteratively searches for assets using the search provider and processes each
        unique asset using the provided callable function. The uniqueness of assets is determined
        based on their GUIDs. If new assets are found in later iterations that haven't been
        processed yet, the process continues until no more new assets are available to process.

        Arguments:
            search: IndexSearchRequestProvider
                The search provider that generates search queries and contains the criteria for
                searching the assets such as a FluentSearch.
            func: Callable[[Asset], None]
                A callable function that receives each unique asset as its parameter and performs
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
            response = self.search(search.to_request())
            LOGGER.debug(
                "Iteration %d found %d assets.", iteration_count, response.count
            )
            for asset in response:
                if asset.guid not in guids_processed:
                    guids_processed.add(asset.guid)
                    has_assets_to_process = True
                    func(asset)
        return len(guids_processed)

    @validate_arguments
    def add_dq_rule_schedule(
        self,
        asset_type: Type[A],
        asset_name: str,
        asset_qualified_name: str,
        schedule_crontab: str,
        schedule_time_zone: str,
    ) -> AssetMutationResponse:
        """
        Add a data quality rule schedule to an asset.

        :param asset_type: the type of asset to update (e.g., Table)
        :param asset_name: the name of the asset to update
        :param asset_qualified_name: the qualified name of the asset to update
        :param schedule_crontab: cron expression string defining the schedule for the DQ rules, e.g: `5 4 * * *`.
        :param schedule_time_zone: timezone for the schedule, e.g: `Europe/Paris`.
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        """
        updated_asset = asset_type.updater(
            qualified_name=asset_qualified_name, name=asset_name
        )
        updated_asset.asset_d_q_schedule_time_zone = schedule_time_zone
        updated_asset.asset_d_q_schedule_crontab = schedule_crontab
        updated_asset.asset_d_q_schedule_type = DataQualityScheduleType.CRON
        response = self.save(updated_asset)
        return response

    @validate_arguments
    def set_dq_row_scope_filter_column(
        self,
        asset_type: Type[A],
        asset_name: str,
        asset_qualified_name: str,
        row_scope_filter_column_qualified_name: str,
    ) -> AssetMutationResponse:
        """
        Set the row scope filter column for data quality rules on an asset.

        :param asset_type: the type of asset to update (e.g., Table)
        :param asset_name: the name of the asset to update
        :param asset_qualified_name: the qualified name of the asset to update
        :param row_scope_filter_column_qualified_name: the qualified name of the column to use for row scope filtering
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        """
        updated_asset = asset_type.updater(
            qualified_name=asset_qualified_name, name=asset_name
        )
        updated_asset.asset_d_q_row_scope_filter_column_qualified_name = (
            row_scope_filter_column_qualified_name
        )
        response = self.save(updated_asset)
        return response


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
        self._processed_guids: Set[str] = set()
        self._first_record_creation_time = -2
        self._last_record_creation_time = -2

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
    def _get_next_page_json(self, is_bulk_search: bool = False):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.
        :param is_bulk_search: whether to retrieve results for a bulk search.
        :returns: JSON for the next page of results, as-is
        """
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "entities" not in raw_json:
            self._assets = []
            return
        try:
            self._process_entities(raw_json["entities"])
            if is_bulk_search:
                self._filter_processed_assets()
                self._update_first_last_record_creation_times()
            return raw_json

        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def _process_entities(self, entities):
        for entity in entities:
            unflatten_custom_metadata_for_entity(
                entity=entity, attributes=self._criteria.attributes
            )
        self._assets = parse_obj_as(List[Asset], entities)

    def _update_first_last_record_creation_times(self):
        self._first_record_creation_time = self._last_record_creation_time = -2

        if not isinstance(self._assets, list) or len(self._assets) <= 1:
            return

        first_asset, last_asset = self._assets[0], self._assets[-1]

        if first_asset:
            self._first_record_creation_time = first_asset.create_time

        if last_asset:
            self._last_record_creation_time = last_asset.create_time

    def _filter_processed_assets(self):
        self._assets = [
            asset
            for asset in self._assets
            if asset is not None and asset.guid not in self._processed_guids
        ]

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

    _DEFAULT_SIZE = DSL.__fields__.get("size").default or 300  # type: ignore[union-attr]
    _MASS_EXTRACT_THRESHOLD = 100000 - _DEFAULT_SIZE

    def __init__(
        self,
        client: ApiCaller,
        criteria: IndexSearchRequest,
        start: int,
        size: int,
        count: int,
        assets: List[Asset],
        aggregations: Optional[Aggregations],
        bulk: bool = False,
    ):
        super().__init__(
            client,
            INDEX_SEARCH,
            criteria,
            start,
            size,
            assets,
        )
        self._count = count
        self._approximate_count = count
        self._aggregations = aggregations
        self._bulk = bulk

    @property
    def aggregations(self) -> Optional[Aggregations]:
        return self._aggregations

    def _prepare_query_for_timestamp_paging(self, query: Query):
        rewritten_filters = []
        if isinstance(query, Bool):
            for filter_ in query.filter:
                if self.is_paging_timestamp_query(filter_):
                    continue
                rewritten_filters.append(filter_)

        if self._first_record_creation_time != self._last_record_creation_time:
            rewritten_filters.append(
                self.get_paging_timestamp_query(self._last_record_creation_time)
            )
            if isinstance(query, Bool):
                rewritten_query = Bool(
                    filter=rewritten_filters,
                    must=query.must,
                    must_not=query.must_not,
                    should=query.should,
                    boost=query.boost,
                    minimum_should_match=query.minimum_should_match,
                )
            else:
                # If a Term, Range, etc., query type is found
                # in the DSL, append it to the Bool `filter`.
                rewritten_filters.append(query)
                rewritten_query = Bool(filter=rewritten_filters)
            self._criteria.dsl.from_ = 0  # type: ignore[attr-defined]
            self._criteria.dsl.query = rewritten_query  # type: ignore[attr-defined]
        else:
            # Ensure that when switching to offset-based paging, if the first and last record timestamps are the same,
            # we do not include a created timestamp filter (ie: Range(field='__timestamp', gte=VALUE)) in the query.
            # Instead, ensure the search runs with only SortItem(field='__timestamp', order=<SortOrder.ASCENDING>).
            # Failing to do so can lead to incomplete results (less than the approximate count) when running the search
            # with a small page size.
            if isinstance(query, Bool):
                for filter_ in query.filter:
                    if self.is_paging_timestamp_query(filter_):
                        query.filter.remove(filter_)

            # Always ensure that the offset is set to the length of the processed assets
            # instead of the default (start + size), as the default may skip some assets
            # and result in incomplete results (less than the approximate count)
            self._criteria.dsl.from_ = len(self._processed_guids)  # type: ignore[attr-defined]

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        is_bulk_search = (
            self._bulk or self._approximate_count > self._MASS_EXTRACT_THRESHOLD
        )
        if size:
            self._size = size
        if is_bulk_search:
            # Used in the "timestamp-based" paging approach
            # to check if `asset.guid` has already been processed
            # in a previous page of results.
            # If it has,then exclude it from the current results;
            # otherwise, we may encounter duplicate asset records.
            self._processed_guids.update(
                asset.guid for asset in self._assets if asset is not None
            )
        return self._get_next_page() if self._assets else False

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        query = self._criteria.dsl.query
        self._criteria.dsl.size = self._size
        self._criteria.dsl.from_ = self._start
        is_bulk_search = (
            self._bulk or self._approximate_count > self._MASS_EXTRACT_THRESHOLD
        )

        if is_bulk_search:
            self._prepare_query_for_timestamp_paging(query)
        if raw_json := super()._get_next_page_json(is_bulk_search):
            self._count = raw_json.get("approximateCount", 0)
            return True
        return False

    @property
    def count(self) -> int:
        return self._count

    @staticmethod
    def presorted_by_timestamp(sorts: List[SortItem]) -> bool:
        """
        Indicates whether the sort options prioritize
        creation-time in ascending order as the first
        sorting key (`True`) or anything else (`False`).

        :param sorts: list of sorting options
        :returns: `True` if the sorting options have
        creation time and ascending as the first option
        """
        return (
            isinstance(sorts, list)
            and len(sorts) > 0
            and isinstance(sorts[0], SortItem)
            and sorts[0].field == Asset.CREATE_TIME.internal_field_name
            and sorts[0].order == SortOrder.ASCENDING
        )

    @staticmethod
    def sort_by_timestamp_first(sorts: List[SortItem]) -> List[SortItem]:
        """
        Rewrites the sorting options to ensure that
        sorting by creation time, ascending, is the top
        priority. Adds this condition if it does not
        already exist, or moves it up to the top sorting
        priority if it does already exist in the list.

        :param sorts: list of sorting options
        :returns: sorting options, making sorting by
        creation time in ascending order the top priority
        """
        creation_asc_sort = [Asset.CREATE_TIME.order(SortOrder.ASCENDING)]

        if not sorts:
            return creation_asc_sort

        rewritten_sorts = [
            sort
            for sort in sorts
            if (not sort.field) or (sort.field != Asset.CREATE_TIME.internal_field_name)
        ]
        return creation_asc_sort + rewritten_sorts

    @staticmethod
    def is_paging_timestamp_query(filter_: Query) -> bool:
        return (
            isinstance(filter_, Range)
            and isinstance(filter_.gte, int)
            and filter_.field == Asset.CREATE_TIME.internal_field_name
            and filter_.gte > 0
        )

    @staticmethod
    def get_paging_timestamp_query(last_timestamp: int) -> Query:
        return Asset.CREATE_TIME.gte(last_timestamp)


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

    _TABLE_LEVEL_ASSETS = {
        Table.__name__,
        View.__name__,
        MaterialisedView.__name__,
    }

    def __init__(
        self,
        client: AtlanClient,
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
        Create a new batch of assets to be bulk-saved.

        :param client: AtlanClient to use
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
        self._client: AtlanClient = client
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
        from pyatlan.model.fluent_search import FluentSearch

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
                results = search.page_size(
                    max(self._max_size * 2, DSL.__fields__.get("size").default)  # type: ignore[union-attr]
                ).execute(client=self._client)  # type: ignore[arg-type]

                for asset in results:
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
                        response = self._client.asset.save(
                            revised, replace_atlan_tags=self._replace_atlan_tags
                        )
                    elif (
                        self._custom_metadata_handling
                        == CustomMetadataHandling.OVERWRITE
                    ):
                        response = self._client.asset.save_replacing_cm(
                            revised, replace_atlan_tags=self._replace_atlan_tags
                        )
                    elif self._custom_metadata_handling == CustomMetadataHandling.MERGE:
                        response = self._client.asset.save_merging_cm(
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


class AssetIdentity(AtlanObject):
    """
    Class to uniquely identify an asset by its type and qualifiedName.
    """

    type_name: str
    qualified_name: str

    def __init__(
        self, type_name: str, qualified_name: str, case_insensitive: bool = False
    ):
        """
        Initializes an AssetIdentity.

        :param type_name: type of the asset.
        :param qualified_name: qualified name of the asset.
        :param case_insensitive: Whether the qualified name should be case insensitive.
        """
        if case_insensitive:
            qualified_name = qualified_name.lower()
        super().__init__(type_name=type_name, qualified_name=qualified_name)  # type: ignore[call-arg]

    @staticmethod
    def from_string(combined: str) -> "AssetIdentity":
        """
        Reverse-engineer an asset identity from a string representation.

        :param combined: The combined (serialized) asset identity.
        :return: The actual asset identity.
        """
        tokens = combined.split("::")
        if len(tokens) != 2:
            raise ValueError(f"Invalid asset identity: {combined}")
        return AssetIdentity(type_name=tokens[0], qualified_name=tokens[1])

    def __str__(self) -> str:
        """
        Simplify an asset identity down to a string representation.

        :return: combined (serialized) asset identity.
        """
        return f"{self.type_name}::{self.qualified_name}"


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
