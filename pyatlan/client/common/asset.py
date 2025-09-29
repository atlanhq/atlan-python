# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Type, TypeVar, Union

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import (
    ADD_BUSINESS_ATTRIBUTE_BY_ID,
    GET_ENTITY_BY_GUID,
    GET_ENTITY_BY_UNIQUE_ATTRIBUTE,
    GET_LINEAGE_LIST,
    INDEX_SEARCH,
    PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregations
from pyatlan.model.assets import (
    Asset,
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Persona,
    Purpose,
    Referenceable,
)
from pyatlan.model.core import (
    Announcement,
    AssetRequest,
    AssetResponse,
    AtlanTag,
    AtlanTagName,
    BulkRequest,
)
from pyatlan.model.custom_metadata import CustomMetadataDict, CustomMetadataRequest
from pyatlan.model.enums import (
    AtlanConnectorType,
    AtlanDeleteType,
    CertificateStatus,
    EntityStatus,
    SaveSemantic,
    SortOrder,
)
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.model.lineage import LineageDirection, LineageListRequest
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.search import (
    DSL,
    Bool,
    IndexSearchRequest,
    Query,
    SortItem,
    Term,
    Terms,
    with_active_category,
    with_active_glossary,
    with_active_term,
)
from pyatlan.utils import unflatten_custom_metadata_for_entity

if TYPE_CHECKING:
    from pyatlan.client.aio import AsyncAtlanClient
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.fluent_search import FluentSearch

LOGGER = logging.getLogger(__name__)

A = TypeVar("A", bound=Asset)


class Search:
    """Shared search logic for asset operations."""

    @staticmethod
    def _prepare_sorts_for_bulk_search(
        sorts: List[SortItem], search_results_class=None
    ):
        # Use provided search results class or default to sync version
        if search_results_class is None:
            # Local import to avoid circular dependency
            from pyatlan.client.asset import IndexSearchResults

            search_results_class = IndexSearchResults

        if not search_results_class.presorted_by_timestamp(sorts):
            # Pre-sort by creation time (ascending) for mass-sequential iteration,
            # if not already sorted by creation time first
            return search_results_class.sort_by_timestamp_first(sorts)
        return sorts

    @staticmethod
    def _get_bulk_search_log_message(bulk):
        return (
            (
                "Bulk search option is enabled. "
                if bulk
                else "Result size (%s) exceeds threshold (%s). "
            )
            + "Ignoring requests for offset-based paging and using timestamp-based paging instead."
        )

    @staticmethod
    def _ensure_type_filter_present(criteria: IndexSearchRequest) -> None:
        """
        Ensures that at least one 'typeName' filter is present in both 'must' and 'filter' clauses.
        If missing in either, appends a default filter for 'Referenceable' to that clause.
        """
        if not (
            criteria
            and criteria.dsl
            and criteria.dsl.query
            and isinstance(criteria.dsl.query, Bool)
        ):
            return

        query = criteria.dsl.query
        default_filter = Term.with_super_type_names(Referenceable.__name__)
        type_field = Referenceable.TYPE_NAME.keyword_field_name

        def needs_type_filter(clause: Optional[List]) -> bool:
            return not any(
                isinstance(f, (Term, Terms)) and f.field == type_field
                for f in clause or []
            )

        # Update 'filter' clause if needed
        if needs_type_filter(query.filter):
            if query.filter is None:
                query.filter = []
            query.filter.append(default_filter)

        # Update 'must' clause if needed
        if needs_type_filter(query.must):
            if query.must is None:
                query.must = []
            query.must.append(default_filter)

    @staticmethod
    def _get_aggregations(raw_json) -> Optional[Aggregations]:
        aggregations = None
        if "aggregations" in raw_json:
            try:
                aggregations = Aggregations.parse_obj(raw_json["aggregations"])
            except ValidationError:
                pass
        return aggregations

    @classmethod
    def _check_for_bulk_search(
        cls, criteria, count, bulk=False, search_results_class=None
    ):
        # Use provided search results class or default to sync version
        if search_results_class is None:
            # Local import to avoid circular dependency
            from pyatlan.client.asset import IndexSearchResults

            search_results_class = IndexSearchResults

        if (
            count > search_results_class._MASS_EXTRACT_THRESHOLD
            and not search_results_class.presorted_by_timestamp(criteria.dsl.sort)
        ):
            # If there is any user-specified sorting present in the search request
            if criteria.dsl.sort and len(criteria.dsl.sort) > 1:
                raise ErrorCode.UNABLE_TO_RUN_BULK_WITH_SORTS.exception_with_parameters()
            # Re-fetch the first page results with updated timestamp sorting
            # for bulk search if count > _MASS_EXTRACT_THRESHOLD (100,000 assets)
            criteria.dsl.sort = cls._prepare_sorts_for_bulk_search(
                criteria.dsl.sort, search_results_class
            )
            LOGGER.debug(
                cls._get_bulk_search_log_message(bulk),
                count,
                search_results_class._MASS_EXTRACT_THRESHOLD,
            )
            return True
        else:
            return False

    @classmethod
    def prepare_request(cls, criteria, bulk=False):
        if bulk:
            # If there is any user-specified sorting present in the search request
            if criteria.dsl.sort and len(criteria.dsl.sort) > 1:
                raise ErrorCode.UNABLE_TO_RUN_BULK_WITH_SORTS.exception_with_parameters()
            criteria.dsl.sort = cls._prepare_sorts_for_bulk_search(criteria.dsl.sort)
            LOGGER.debug(cls._get_bulk_search_log_message(bulk))
            cls._ensure_type_filter_present(criteria)
        return INDEX_SEARCH, criteria

    @classmethod
    def process_response(cls, raw_json, criteria) -> Dict[str, Any]:
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
        aggregations = cls._get_aggregations(raw_json)
        approximate_count = raw_json.get("approximateCount", 0)
        return {
            "assets": assets,
            "aggregations": aggregations,
            "count": approximate_count,
        }


class GetLineageList:
    """
    Shared business logic for get_lineage_list operations.

    Provides static methods for prepare_request() and process_response()
    to ensure zero code duplication between sync and async clients.
    """

    @staticmethod
    def prepare_request(lineage_request: LineageListRequest):
        """
        Validates lineage request and prepares it for API call.

        :param lineage_request: the lineage request to validate and prepare
        :returns: tuple of (API_ENDPOINT, request_object)
        :raises InvalidRequestError: if lineage direction is 'BOTH' (unsupported)
        """
        if lineage_request.direction == LineageDirection.BOTH:
            raise ErrorCode.INVALID_LINEAGE_DIRECTION.exception_with_parameters()

        return GET_LINEAGE_LIST, lineage_request

    @staticmethod
    def process_response(
        raw_json: Dict[str, Any], lineage_request: LineageListRequest
    ) -> Dict[str, Any]:
        """
        Processes the raw JSON response from lineage API call.

        :param raw_json: raw JSON response from API
        :param lineage_request: original request for context (attributes, etc.)
        :returns: dictionary containing processed assets and has_more flag
        :raises AtlanError: on JSON validation errors
        """
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

        return {
            "assets": assets,
            "has_more": has_more,
        }


class FindAssetsByName:
    """
    Generic shared business logic for finding assets by name.

    Provides static methods that can be used by specific asset type finders
    to ensure zero code duplication between different asset search operations.
    """

    @staticmethod
    def prepare_request(
        name: str, type_name: str, attributes: Optional[List[str]] = None
    ) -> IndexSearchRequest:
        """
        Prepares search request for finding assets by name and type.

        :param name: name of the asset to search for
        :param type_name: type name of the asset (e.g., "PERSONA", "PURPOSE")
        :param attributes: optional collection of attributes to retrieve
        :returns: prepared IndexSearchRequest
        """
        if attributes is None:
            attributes = []

        query = (
            Term.with_state("ACTIVE")
            + Term.with_type_name(type_name)
            + Term.with_name(name)
        )

        dsl = DSL(query=query)
        return IndexSearchRequest(
            dsl=dsl, attributes=attributes, relation_attributes=["name"]
        )

    @staticmethod
    def process_response(
        search_results, name: str, asset_type: Type[A], allow_multiple: bool = True
    ) -> List[A]:
        """
        Processes search results to extract and validate assets of specific type.

        :param search_results: results from search operation
        :param name: name that was searched for (for error messages)
        :param asset_type: the specific asset class to filter for
        :param allow_multiple: whether to allow multiple results
        :returns: list of found assets of the specified type
        :raises NotFoundError: if no asset with the provided name exists
        """
        if (
            search_results
            and search_results.count > 0
            and (
                # Check for paginated results first;
                # if not paginated, iterate over the results
                assets := [
                    asset
                    for asset in (search_results.current_page() or search_results)
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


class FindPersonasByName:
    """
    Shared business logic for find_personas_by_name operations.

    Delegates to FindAssetsByName for generic functionality.
    """

    @staticmethod
    def prepare_request(
        name: str, attributes: Optional[List[str]] = None
    ) -> IndexSearchRequest:
        """
        Prepares search request for finding personas by name.

        :param name: name of the persona to search for
        :param attributes: optional collection of attributes to retrieve
        :returns: prepared IndexSearchRequest
        """
        return FindAssetsByName.prepare_request(name, "PERSONA", attributes)

    @staticmethod
    def process_response(
        search_results, name: str, allow_multiple: bool = True
    ) -> List[Persona]:
        """
        Processes search results to extract and validate personas.

        :param search_results: results from search operation
        :param name: name that was searched for (for error messages)
        :param allow_multiple: whether to allow multiple results
        :returns: list of found personas
        :raises NotFoundError: if no persona with the provided name exists
        """
        return FindAssetsByName.process_response(
            search_results, name, Persona, allow_multiple
        )


class FindPurposesByName:
    """
    Shared business logic for find_purposes_by_name operations.

    Delegates to FindAssetsByName for generic functionality.
    """

    @staticmethod
    def prepare_request(
        name: str, attributes: Optional[List[str]] = None
    ) -> IndexSearchRequest:
        """
        Prepares search request for finding purposes by name.

        :param name: name of the purpose to search for
        :param attributes: optional collection of attributes to retrieve
        :returns: prepared IndexSearchRequest
        """
        return FindAssetsByName.prepare_request(name, "PURPOSE", attributes)

    @staticmethod
    def process_response(
        search_results, name: str, allow_multiple: bool = True
    ) -> List[Purpose]:
        """
        Processes search results to extract and validate purposes.

        :param search_results: results from search operation
        :param name: name that was searched for (for error messages)
        :param allow_multiple: whether to allow multiple results
        :returns: list of found purposes
        :raises NotFoundError: if no purpose with the provided name exists
        """
        return FindAssetsByName.process_response(
            search_results, name, Purpose, allow_multiple
        )


class GetByQualifiedName:
    """
    Shared business logic for get_by_qualified_name operations.

    Provides static methods for prepare_request() and process_response()
    to ensure zero code duplication between sync and async clients.
    """

    @staticmethod
    def normalize_search_fields(
        fields: Optional[Union[List[str], List[AtlanField]]],
    ) -> List[str]:
        """
        Normalizes search fields to strings.

        :param fields: list of fields (strings or AtlanField objects)
        :returns: list of normalized field names
        """
        if not fields:
            return []
        return [f.atlan_field_name if isinstance(f, AtlanField) else f for f in fields]

    @staticmethod
    def prepare_fluent_search_request(
        qualified_name: str,
        asset_type: Type[A],
        attributes: List[str],
        related_attributes: List[str],
    ) -> "FluentSearch":
        """
        Prepares FluentSearch request when specific attributes are requested.

        :param qualified_name: qualified name of the asset
        :param asset_type: type of asset to retrieve
        :param attributes: attributes to include on results
        :param related_attributes: attributes to include on relations
        :returns: configured FluentSearch object
        """
        from pyatlan.model.fluent_search import FluentSearch

        search = (
            FluentSearch()
            .where(Asset.QUALIFIED_NAME.eq(qualified_name))
            .where(Asset.TYPE_NAME.eq(asset_type.__name__))
        )
        for attribute in attributes:
            search = search.include_on_results(attribute)
        for relation_attribute in related_attributes:
            search = search.include_on_relations(relation_attribute)
        return search

    @staticmethod
    def prepare_direct_api_request(
        qualified_name: str,
        asset_type: Type[A],
        min_ext_info: bool,
        ignore_relationships: bool,
    ) -> tuple[str, Dict[str, Any]]:
        """
        Prepares direct API request when no specific attributes are requested.

        :param qualified_name: qualified name of the asset
        :param asset_type: type of asset to retrieve
        :param min_ext_info: whether to minimize extra info
        :param ignore_relationships: whether to ignore relationships
        :returns: tuple of (endpoint_path, query_params)
        """
        endpoint_path = GET_ENTITY_BY_UNIQUE_ATTRIBUTE.format_path_with_params(
            asset_type.__name__
        )
        query_params = {
            "attr:qualifiedName": qualified_name,
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }
        return endpoint_path, query_params

    @staticmethod
    def handle_relationships(raw_json: Dict[str, Any]) -> Asset:
        """
        Handles relationship attributes in the API response.

        :param raw_json: raw JSON response from API
        :returns: processed asset with relationships handled
        """
        if (
            "relationshipAttributes" in raw_json["entity"]
            and raw_json["entity"]["relationshipAttributes"]
        ):
            raw_json["entity"]["attributes"].update(
                raw_json["entity"]["relationshipAttributes"]
            )
        raw_json["entity"]["relationshipAttributes"] = {}
        asset: Asset = AssetResponse[Asset](**raw_json).entity
        asset.is_incomplete = False
        return asset

    @staticmethod
    def process_fluent_search_response(
        search_results, qualified_name: str, asset_type: Type[A]
    ) -> A:
        """
        Processes FluentSearch results to extract the asset.

        :param search_results: results from FluentSearch
        :param qualified_name: qualified name that was searched for
        :param asset_type: expected asset type
        :returns: the requested asset
        :raises NotFoundError: if asset not found or wrong type
        """
        if search_results and search_results.current_page():
            first_result = search_results.current_page()[0]
            if isinstance(first_result, asset_type):
                return first_result
            else:
                raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                    asset_type.__name__, qualified_name
                )
        else:
            raise ErrorCode.ASSET_NOT_FOUND_BY_QN.exception_with_parameters(
                qualified_name, asset_type.__name__
            )

    @staticmethod
    def process_direct_api_response(
        raw_json: Dict[str, Any], qualified_name: str, asset_type: Type[A]
    ) -> A:
        """
        Processes direct API response to extract the asset.

        :param raw_json: raw JSON response from API
        :param qualified_name: qualified name that was searched for
        :param asset_type: expected asset type
        :returns: the requested asset
        :raises NotFoundError: if asset not found or wrong type
        """
        if raw_json["entity"]["typeName"] != asset_type.__name__:
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                asset_type.__name__, qualified_name
            )
        asset = GetByQualifiedName.handle_relationships(raw_json)
        if not isinstance(asset, asset_type):
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                asset_type.__name__, qualified_name
            )
        return asset


class GetByGuid:
    """
    Shared business logic for get_by_guid operations.

    Provides static methods for prepare_request() and process_response()
    to ensure zero code duplication between sync and async clients.
    """

    @staticmethod
    def prepare_fluent_search_request(
        guid: str,
        asset_type: Type[A],
        attributes: List[str],
        related_attributes: List[str],
    ) -> "FluentSearch":
        """
        Prepares FluentSearch request when specific attributes are requested.

        :param guid: GUID of the asset
        :param asset_type: type of asset to retrieve
        :param attributes: attributes to include on results
        :param related_attributes: attributes to include on relations
        :returns: configured FluentSearch object
        """
        from pyatlan.model.fluent_search import FluentSearch

        search = (
            FluentSearch()
            .where(Asset.GUID.eq(guid))
            .where(Asset.TYPE_NAME.eq(asset_type.__name__))
        )
        for attribute in attributes:
            search = search.include_on_results(attribute)
        for relation_attribute in related_attributes:
            search = search.include_on_relations(relation_attribute)
        return search

    @staticmethod
    def prepare_direct_api_request(
        guid: str,
        min_ext_info: bool,
        ignore_relationships: bool,
    ) -> tuple[str, Dict[str, Any]]:
        """
        Prepares direct API request when no specific attributes are requested.

        :param guid: GUID of the asset
        :param min_ext_info: whether to minimize extra info
        :param ignore_relationships: whether to ignore relationships
        :returns: tuple of (endpoint_path, query_params)
        """
        endpoint_path = GET_ENTITY_BY_GUID.format_path_with_params(guid)
        query_params = {
            "minExtInfo": min_ext_info,
            "ignoreRelationships": ignore_relationships,
        }
        return endpoint_path, query_params

    @staticmethod
    def process_fluent_search_response(
        search_results, guid: str, asset_type: Type[A]
    ) -> A:
        """
        Processes FluentSearch results to extract the asset.

        :param search_results: results from FluentSearch
        :param guid: GUID that was searched for
        :param asset_type: expected asset type
        :returns: the requested asset
        :raises NotFoundError: if asset not found or wrong type
        """
        if search_results and search_results.current_page():
            first_result = search_results.current_page()[0]
            if isinstance(first_result, asset_type):
                return first_result
            else:
                raise ErrorCode.ASSET_NOT_TYPE_REQUESTED.exception_with_parameters(
                    guid, asset_type.__name__
                )
        else:
            raise ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters(guid)

    @staticmethod
    def process_direct_api_response(
        raw_json: Dict[str, Any], guid: str, asset_type: Type[A]
    ) -> A:
        """
        Processes direct API response to extract the asset.

        :param raw_json: raw JSON response from API
        :param guid: GUID that was searched for
        :param asset_type: expected asset type
        :returns: the requested asset
        :raises NotFoundError: if asset not found or wrong type
        """
        asset = GetByQualifiedName.handle_relationships(raw_json)
        if not isinstance(asset, asset_type):
            raise ErrorCode.ASSET_NOT_TYPE_REQUESTED.exception_with_parameters(
                guid, asset_type.__name__
            )
        return asset


class Save:
    @staticmethod
    def prepare_request(
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
        append_atlan_tags: bool = False,
        client: Optional[AtlanClient] = None,
    ) -> tuple[Dict[str, Any], BulkRequest[Asset]]:
        """
        Prepare the request for saving assets.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update
        :param replace_custom_metadata: replaces any custom metadata with non-empty values provided
        :param overwrite_custom_metadata: overwrites any custom metadata, even with empty values
        :param append_atlan_tags: whether to add/update/remove AtlanTags during an update
        :param client: the Atlan client instance for flushing custom metadata
        :returns: tuple of (query_params, bulk_request)
        """
        query_params = {
            "replaceTags": replace_atlan_tags,
            "appendTags": append_atlan_tags,
            "replaceBusinessAttributes": replace_custom_metadata,
            "overwriteBusinessAttributes": overwrite_custom_metadata,
        }

        entities: List[Asset] = []
        if isinstance(entity, list):
            entities.extend(entity)
        else:
            entities.append(entity)

        if not client:
            raise ValueError(
                "AtlanClient instance must be provided to validate and flush cm for assets."
            )
        # Validate and flush entities BEFORE creating the BulkRequest
        Save.validate_and_flush_entities(entities, client)
        return query_params, BulkRequest[Asset](entities=entities)

    @staticmethod
    async def prepare_request_async(
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        replace_custom_metadata: bool = False,
        overwrite_custom_metadata: bool = False,
        append_atlan_tags: bool = False,
        client: Optional[AsyncAtlanClient] = None,
    ) -> tuple[Dict[str, Any], BulkRequest[Asset]]:
        """
        Prepare the request for saving assets.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update
        :param replace_custom_metadata: replaces any custom metadata with non-empty values provided
        :param overwrite_custom_metadata: overwrites any custom metadata, even with empty values
        :param append_atlan_tags: whether to add/update/remove AtlanTags during an update
        :param client: Optional[AsyncAtlanClient] = None,
        :returns: tuple of (query_params, bulk_request)
        """
        query_params = {
            "replaceTags": replace_atlan_tags,
            "appendTags": append_atlan_tags,
            "replaceBusinessAttributes": replace_custom_metadata,
            "overwriteBusinessAttributes": overwrite_custom_metadata,
        }

        entities: List[Asset] = []
        if isinstance(entity, list):
            entities.extend(entity)
        else:
            entities.append(entity)

        if not client:
            raise ValueError(
                "AsyncAtlanClient instance must be provided to validate and flush cm for assets."
            )
        # Validate and flush entities BEFORE creating the BulkRequest
        await Save.validate_and_flush_entities_async(entities, client)
        return query_params, BulkRequest[Asset](entities=entities)

    @staticmethod
    def validate_and_flush_entities(entities: List[Asset], client: AtlanClient) -> None:
        """
        Validate required fields and flush custom metadata for each asset.

        :param entities: list of assets to validate and flush
        :param client: the Atlan client instance
        """
        for asset in entities:
            asset.validate_required()
            asset.flush_custom_metadata(client=client)

    @staticmethod
    async def validate_and_flush_entities_async(
        entities: List[Asset], client: AsyncAtlanClient
    ) -> None:
        """
        Validate required fields and flush custom metadata for each asset.

        :param entities: list of assets to validate and flush
        :param client: the Atlan client instance
        """
        for asset in entities:
            asset.validate_required()
            await asset.flush_custom_metadata_async(client=client)

    @staticmethod
    def process_response(raw_json: Dict[str, Any]) -> AssetMutationResponse:
        """
        Process the API response into an AssetMutationResponse.

        :param raw_json: raw response from the API
        :returns: parsed AssetMutationResponse
        """
        return AssetMutationResponse(**raw_json)

    @staticmethod
    def get_connection_guids_to_wait_for(connections_created):
        """
        Extract connection GUIDs that need to be waited for.
        This is a shared method that returns the list of GUIDs to check.

        :param connections_created: list of Connection assets that were created
        :returns: list of GUIDs to wait for
        """
        LOGGER.debug("Waiting for connections")
        guids = []
        for connection in connections_created:
            guid = connection.guid
            LOGGER.debug("Attempting to retrieve connection with guid: %s", guid)
            guids.append(guid)
        return guids

    @staticmethod
    def log_connections_finished():
        """Log that connection waiting is finished."""
        LOGGER.debug("Finished waiting for connections")

    @staticmethod
    def prepare_request_replacing_cm(
        entity: Union[Asset, List[Asset]],
        replace_atlan_tags: bool = False,
        client: Optional[AtlanClient] = None,
    ) -> tuple[Dict[str, Any], BulkRequest[Asset]]:
        """
        Prepare the request for saving assets with replacing custom metadata.
        This uses different query parameter names than the regular save method.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update
        :param client: the Atlan client instance for flushing custom metadata
        :returns: tuple of (query_params, bulk_request)
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

        if not client:
            raise ValueError(
                "AtlanClient instance must be provided to validate and flush cm for assets."
            )
        # Validate and flush entities BEFORE creating the BulkRequest
        Save.validate_and_flush_entities(entities, client)
        return query_params, BulkRequest[Asset](entities=entities)

    @staticmethod
    def process_response_replacing_cm(
        raw_json: Dict[str, Any],
    ) -> AssetMutationResponse:
        """
        Process the API response for save_replacing_cm into an AssetMutationResponse.
        This method doesn't handle connection waiting like the regular save method.

        :param raw_json: raw response from the API
        :returns: parsed AssetMutationResponse
        """
        return AssetMutationResponse(**raw_json)


class UpdateAsset:
    @staticmethod
    def validate_asset_exists(
        qualified_name: str, asset_type: Type[A], get_by_qualified_name_func
    ) -> None:
        """
        Validate that an asset exists by trying to retrieve it.
        This method will raise NotFoundError if the asset doesn't exist.

        :param qualified_name: the qualified name of the asset to check
        :param asset_type: the type of asset to check
        :param get_by_qualified_name_func: function to call for retrieving asset (sync only)
        :raises NotFoundError: if the asset does not exist
        """
        # This will raise NotFoundError if the asset doesn't exist
        get_by_qualified_name_func(
            qualified_name=qualified_name,
            asset_type=asset_type,
            min_ext_info=True,
            ignore_relationships=True,
        )

    @staticmethod
    async def validate_asset_exists_async(
        qualified_name: str, asset_type: Type[A], get_by_qualified_name_func
    ) -> None:
        """
        Async version of validate_asset_exists.
        This method will raise NotFoundError if the asset doesn't exist.

        :param qualified_name: the qualified name of the asset to check
        :param asset_type: the type of asset to check
        :param get_by_qualified_name_func: async function to call for retrieving asset
        :raises NotFoundError: if the asset does not exist
        """
        # This will raise NotFoundError if the asset doesn't exist
        await get_by_qualified_name_func(
            qualified_name=qualified_name,
            asset_type=asset_type,
            min_ext_info=True,
            ignore_relationships=True,
        )


class PurgeByGuid:
    @staticmethod
    def prepare_request(
        guid: Union[str, List[str]],
        delete_type: AtlanDeleteType = AtlanDeleteType.PURGE,
    ) -> Dict[str, Any]:
        """
        Prepare the request for purging assets by GUID.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to delete
        :param delete_type: type of deletion to perform (PURGE or HARD)
        :returns: query parameters for the API call
        """
        guids: List[str] = []
        if isinstance(guid, list):
            guids.extend(guid)
        else:
            guids.append(guid)
        return {"deleteType": delete_type.value, "guid": guids}

    @staticmethod
    def process_response(raw_json: Dict[str, Any]) -> AssetMutationResponse:
        """
        Process the API response into an AssetMutationResponse.

        :param raw_json: raw response from the API
        :returns: parsed AssetMutationResponse
        """
        return AssetMutationResponse(**raw_json)


class DeleteByGuid:
    @staticmethod
    def prepare_request(guid: Union[str, List[str]]) -> List[str]:
        """
        Prepare the request for soft-deleting assets by GUID.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to soft-delete
        :returns: normalized list of GUIDs
        """
        guids: List[str] = []
        if isinstance(guid, list):
            guids.extend(guid)
        else:
            guids.append(guid)
        return guids

    @staticmethod
    def validate_assets_can_be_archived(assets: List[Asset]) -> None:
        """
        Validate that all assets can be archived (soft-deleted).

        :param assets: list of assets to validate
        :raises AtlanError: if any asset cannot be archived
        """
        for asset in assets:
            if not asset.can_be_archived():
                raise ErrorCode.ASSET_CAN_NOT_BE_ARCHIVED.exception_with_parameters(
                    asset.guid, asset.type_name
                )

    @staticmethod
    def prepare_delete_request(guids: List[str]) -> Dict[str, Any]:
        """
        Prepare the delete request parameters.

        :param guids: list of GUIDs to delete
        :returns: query parameters for the API call
        """
        return {"deleteType": AtlanDeleteType.SOFT.value, "guid": guids}

    @staticmethod
    def process_response(raw_json: Dict[str, Any]) -> AssetMutationResponse:
        """
        Process the API response into an AssetMutationResponse.

        :param raw_json: raw response from the API
        :returns: parsed AssetMutationResponse
        """
        return AssetMutationResponse(**raw_json)

    @staticmethod
    def get_deleted_assets(response: AssetMutationResponse) -> List[Asset]:
        """
        Extract deleted assets from the response for validation.

        :param response: the mutation response
        :returns: list of deleted assets
        """
        return response.assets_deleted(asset_type=Asset)

    @staticmethod
    def is_asset_deleted(asset: Asset) -> bool:
        """
        Check if an asset is in deleted status.

        :param asset: the asset to check
        :returns: True if the asset is deleted
        """
        return asset.status == EntityStatus.DELETED


class RestoreAsset:
    @staticmethod
    def can_asset_type_be_archived(asset_type: Type[A]) -> bool:
        """
        Check if an asset type can be archived.

        :param asset_type: the asset type to check
        :returns: True if the asset type can be archived
        """
        return asset_type.can_be_archived()

    @staticmethod
    def is_asset_active(asset: Asset) -> bool:
        """
        Check if an asset is in active status.

        :param asset: the asset to check
        :returns: True if the asset is active
        """
        return asset.status is EntityStatus.ACTIVE

    @staticmethod
    def prepare_restore_request(
        asset: Asset,
    ) -> tuple[Dict[str, Any], BulkRequest[Asset]]:
        """
        Prepare the request for restoring an asset.

        :param asset: the asset to restore
        :returns: tuple of (query_params, bulk_request)
        """
        to_restore = asset.trim_to_required()
        to_restore.status = EntityStatus.ACTIVE
        query_params = {
            "replaceClassifications": False,
            "replaceBusinessAttributes": False,
            "overwriteBusinessAttributes": False,
        }
        return query_params, BulkRequest[Asset](entities=[to_restore])

    @staticmethod
    def process_restore_response(raw_json: Dict[str, Any]) -> AssetMutationResponse:
        """
        Process the restore API response.

        :param raw_json: raw response from the API
        :returns: parsed AssetMutationResponse
        """
        return AssetMutationResponse(**raw_json)

    @staticmethod
    def is_restore_successful(response: AssetMutationResponse) -> bool:
        """
        Check if the restore operation was successful.

        :param response: the mutation response
        :returns: True if restore was successful
        """
        return response is not None and response.guid_assignments is not None


class ModifyAtlanTags:
    @staticmethod
    def prepare_asset_updater(
        retrieved_asset,
        asset_type: Type[A],
        qualified_name: str,
    ):
        """
        Prepare an asset updater based on the asset type.
        Special handling for glossary terms and categories.

        :param retrieved_asset: the retrieved asset
        :param asset_type: type of asset being updated
        :param qualified_name: qualified name of the asset
        :returns: asset updater instance
        """
        if asset_type in (AtlasGlossaryTerm, AtlasGlossaryCategory):
            return asset_type.updater(
                qualified_name=qualified_name,
                name=retrieved_asset.name,
                glossary_guid=retrieved_asset.anchor.guid,  # type: ignore[attr-defined]
            )
        else:
            return asset_type.updater(
                qualified_name=qualified_name, name=retrieved_asset.name
            )

    @staticmethod
    def create_atlan_tags(
        atlan_tag_names: List[str],
        propagate: bool = False,
        remove_propagation_on_delete: bool = True,
        restrict_lineage_propagation: bool = False,
        restrict_propagation_through_hierarchy: bool = False,
    ) -> List[AtlanTag]:
        """
        Create AtlanTag objects from tag names and configuration.

        :param atlan_tag_names: human-readable names of the Atlan tags
        :param propagate: whether to propagate the Atlan tag
        :param remove_propagation_on_delete: whether to remove propagated tags on deletion
        :param restrict_lineage_propagation: whether to avoid propagating through lineage
        :param restrict_propagation_through_hierarchy: whether to prevent hierarchy propagation
        :returns: list of AtlanTag objects
        """
        return [
            AtlanTag(  # type: ignore[call-arg]
                type_name=AtlanTagName(display_text=name),
                propagate=propagate,
                remove_propagations_on_entity_delete=remove_propagation_on_delete,
                restrict_propagation_through_lineage=restrict_lineage_propagation,
                restrict_propagation_through_hierarchy=restrict_propagation_through_hierarchy,
            )
            for name in atlan_tag_names
        ]

    @staticmethod
    def apply_tag_modification(
        updated_asset,
        atlan_tags: List[AtlanTag],
        type_of_modification: str,
    ):
        """
        Apply the tag modification to the asset updater.

        :param updated_asset: the asset updater instance
        :param atlan_tags: list of AtlanTag objects to apply
        :param type_of_modification: type of modification (add, update, remove, replace)
        """
        if type_of_modification in ("add", "update"):
            updated_asset.add_or_update_classifications = atlan_tags
        elif type_of_modification == "remove":
            updated_asset.remove_classifications = atlan_tags
        elif type_of_modification == "replace":
            updated_asset.classifications = atlan_tags

    @staticmethod
    def get_retrieve_attributes() -> List:
        """
        Get the attributes needed when retrieving the asset for tag modification.

        :returns: list of attributes to retrieve
        """
        return [AtlasGlossaryTerm.ANCHOR]  # type: ignore[arg-type]

    @staticmethod
    def process_save_response(response, asset_type: Type[A], updated_asset):
        """
        Process the save response to extract the updated asset.

        :param response: AssetMutationResponse from save operation
        :param asset_type: type of asset that was updated
        :param updated_asset: the asset updater that was saved
        :returns: the updated asset or the updater if no assets found
        """
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return updated_asset


class ManageAssetAttributes:
    """Shared business logic for managing asset attributes like certificates and announcements."""

    @staticmethod
    def prepare_asset_for_update(
        asset_type: Type[A],
        qualified_name: str,
        name: str,
    ):
        """
        Prepare a basic asset instance for attribute updates.

        :param asset_type: type of asset to create
        :param qualified_name: qualified name of the asset
        :param name: name of the asset
        :returns: prepared asset instance
        """
        asset = asset_type()
        asset.qualified_name = qualified_name
        asset.name = name
        return asset

    @staticmethod
    def handle_glossary_anchor(
        asset, asset_type_name: str, glossary_guid: Optional[str]
    ):
        """
        Handle glossary anchor for glossary terms and categories.

        :param asset: the asset instance
        :param asset_type_name: name of the asset type
        :param glossary_guid: GUID of the glossary
        :raises AtlanError: if glossary_guid is required but missing
        """
        if isinstance(asset, (AtlasGlossaryTerm, AtlasGlossaryCategory)):
            if not glossary_guid:
                raise ErrorCode.MISSING_GLOSSARY_GUID.exception_with_parameters(
                    asset_type_name
                )
            asset.anchor = AtlasGlossary.ref_by_guid(glossary_guid)


class UpdateCertificate:
    """Shared business logic for updating asset certificates."""

    @staticmethod
    def prepare_asset_with_certificate(
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        certificate_status: CertificateStatus,
        message: Optional[str] = None,
        glossary_guid: Optional[str] = None,
    ):
        """
        Prepare an asset with certificate information.

        :param asset_type: type of asset to update
        :param qualified_name: qualified name of the asset
        :param name: name of the asset
        :param certificate_status: certificate status to set
        :param message: optional certificate message
        :param glossary_guid: glossary GUID for glossary assets
        :returns: prepared asset with certificate
        """
        asset = ManageAssetAttributes.prepare_asset_for_update(
            asset_type, qualified_name, name
        )
        asset.certificate_status = certificate_status
        asset.certificate_status_message = message
        ManageAssetAttributes.handle_glossary_anchor(
            asset, asset_type.__name__, glossary_guid
        )
        return asset


class RemoveCertificate:
    """Shared business logic for removing asset certificates."""

    @staticmethod
    def prepare_asset_for_certificate_removal(
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ):
        """
        Prepare an asset for certificate removal.

        :param asset_type: type of asset to update
        :param qualified_name: qualified name of the asset
        :param name: name of the asset
        :param glossary_guid: glossary GUID for glossary assets
        :returns: prepared asset for certificate removal
        """
        asset = ManageAssetAttributes.prepare_asset_for_update(
            asset_type, qualified_name, name
        )
        asset.remove_certificate()
        ManageAssetAttributes.handle_glossary_anchor(
            asset, asset_type.__name__, glossary_guid
        )
        return asset


class UpdateAnnouncement:
    """Shared business logic for updating asset announcements."""

    @staticmethod
    def prepare_asset_with_announcement(
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        announcement: Announcement,
        glossary_guid: Optional[str] = None,
    ):
        """
        Prepare an asset with announcement information.

        :param asset_type: type of asset to update
        :param qualified_name: qualified name of the asset
        :param name: name of the asset
        :param announcement: announcement to set
        :param glossary_guid: glossary GUID for glossary assets
        :returns: prepared asset with announcement
        """
        asset = ManageAssetAttributes.prepare_asset_for_update(
            asset_type, qualified_name, name
        )
        asset.set_announcement(announcement)
        ManageAssetAttributes.handle_glossary_anchor(
            asset, asset_type.__name__, glossary_guid
        )
        return asset


class RemoveAnnouncement:
    """Shared business logic for removing asset announcements."""

    @staticmethod
    def prepare_asset_for_announcement_removal(
        asset_type: Type[A],
        qualified_name: str,
        name: str,
        glossary_guid: Optional[str] = None,
    ):
        """
        Prepare an asset for announcement removal.

        :param asset_type: type of asset to update
        :param qualified_name: qualified name of the asset
        :param name: name of the asset
        :param glossary_guid: glossary GUID for glossary assets
        :returns: prepared asset for announcement removal
        """
        asset = ManageAssetAttributes.prepare_asset_for_update(
            asset_type, qualified_name, name
        )
        asset.remove_announcement()
        ManageAssetAttributes.handle_glossary_anchor(
            asset, asset_type.__name__, glossary_guid
        )
        return asset


class UpdateAssetByAttribute:
    """Shared business logic for updating assets by attribute."""

    @staticmethod
    def prepare_request_params(qualified_name: str) -> dict:
        """
        Prepare query parameters for asset update by attribute.

        :param qualified_name: qualified name of the asset
        :returns: query parameters dict
        """
        return {"attr:qualifiedName": qualified_name}

    @staticmethod
    def prepare_request_body(asset: A) -> AssetRequest[Asset]:
        """
        Prepare the request body for asset update.

        :param asset: the asset to update
        :returns: AssetRequest object
        """
        return AssetRequest[Asset](entity=asset)

    @staticmethod
    def get_api_endpoint(asset_type: Type[A]) -> str:
        """
        Get the API endpoint for partial update by attribute.

        :param asset_type: type of asset being updated
        :returns: formatted API endpoint
        """
        return PARTIAL_UPDATE_ENTITY_BY_ATTRIBUTE.format_path_with_params(
            asset_type.__name__
        )

    @staticmethod
    def process_response(raw_json: dict, asset_type: Type[A]) -> Optional[A]:
        """
        Process the response from asset update by attribute API.

        :param raw_json: raw JSON response from API
        :param asset_type: type of asset that was updated
        :returns: updated asset or None if update failed
        """
        response = AssetMutationResponse(**raw_json)
        if assets := response.assets_partially_updated(asset_type=asset_type):
            return assets[0]
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return None


class ManageCustomMetadata:
    """Shared business logic for custom metadata operations."""

    @staticmethod
    def create_custom_metadata_request(
        custom_metadata: CustomMetadataDict,
    ) -> CustomMetadataRequest:
        """
        Create a CustomMetadataRequest from CustomMetadataDict.

        :param custom_metadata: custom metadata dictionary
        :returns: CustomMetadataRequest object
        """
        return CustomMetadataRequest.create(custom_metadata_dict=custom_metadata)

    @staticmethod
    def get_api_endpoint(guid: str, custom_metadata_set_id: str) -> str:
        """
        Get the API endpoint for custom metadata operations.

        :param guid: asset GUID
        :param custom_metadata_set_id: custom metadata set ID
        :returns: formatted API endpoint
        """
        return ADD_BUSINESS_ATTRIBUTE_BY_ID.format_path(
            {
                "entity_guid": guid,
                "bm_id": custom_metadata_set_id,
            }
        )


class UpdateCustomMetadataAttributes:
    """Shared business logic for updating custom metadata attributes."""

    @staticmethod
    def prepare_request(custom_metadata: CustomMetadataDict) -> CustomMetadataRequest:
        """
        Prepare request for updating custom metadata attributes.

        :param custom_metadata: custom metadata to update
        :returns: CustomMetadataRequest object
        """
        return ManageCustomMetadata.create_custom_metadata_request(custom_metadata)


class ReplaceCustomMetadata:
    """Shared business logic for replacing custom metadata."""

    @staticmethod
    def prepare_request(custom_metadata: CustomMetadataDict) -> CustomMetadataRequest:
        """
        Prepare request for replacing custom metadata.

        :param custom_metadata: custom metadata to replace
        :returns: CustomMetadataRequest object
        """
        # Clear unset attributes so that they are removed
        custom_metadata.clear_unset()
        return ManageCustomMetadata.create_custom_metadata_request(custom_metadata)


class RemoveCustomMetadata:
    """Shared business logic for removing custom metadata."""

    @staticmethod
    def prepare_request(cm_name: str, client) -> CustomMetadataRequest:
        """
        Prepare request for removing custom metadata.

        :param cm_name: human-readable name of the custom metadata to remove
        :param client: Atlan client instance
        :returns: CustomMetadataRequest object
        """
        custom_metadata = CustomMetadataDict(client=client, name=cm_name)  # type: ignore[arg-type]
        # Invoke clear_all so all attributes are set to None and consequently removed
        custom_metadata.clear_all()
        return ManageCustomMetadata.create_custom_metadata_request(custom_metadata)

    @staticmethod
    async def prepare_request_async(cm_name: str, client):
        """
        Async version - prepare request for removing custom metadata.

        :param cm_name: human-readable name of the custom metadata to remove
        :param client: AsyncAtlanClient instance
        :returns: AsyncCustomMetadataRequest object
        """
        from pyatlan.model.aio.custom_metadata import (
            AsyncCustomMetadataDict,
            AsyncCustomMetadataRequest,
        )

        custom_metadata = await AsyncCustomMetadataDict.creator(
            client=client, name=cm_name
        )
        # Invoke clear_all so all attributes are set to None and consequently removed
        custom_metadata.clear_all()
        return await AsyncCustomMetadataRequest.create(custom_metadata)


class ManageTerms:
    """Shared business logic for terms management operations."""

    @staticmethod
    def validate_guid_and_qualified_name(
        guid: Optional[str], qualified_name: Optional[str]
    ):
        """
        Validate that exactly one of GUID or qualified_name is provided.

        :param guid: asset GUID
        :param qualified_name: asset qualified name
        :raises AtlanError: if validation fails
        """
        if guid:
            if qualified_name:
                raise ErrorCode.QN_OR_GUID_NOT_BOTH.exception_with_parameters()
        elif not qualified_name:
            raise ErrorCode.QN_OR_GUID.exception_with_parameters()

    @staticmethod
    def build_fluent_search_by_guid(asset_type: Type[A], guid: str):
        """
        Build FluentSearch query to find asset by GUID.

        :param asset_type: type of asset to search for
        :param guid: GUID to search for
        :returns: FluentSearch query
        """
        from pyatlan.model.fluent_search import FluentSearch

        return (
            FluentSearch()
            .select()
            .where(Asset.TYPE_NAME.eq(asset_type.__name__))
            .where(asset_type.GUID.eq(guid))
        )

    @staticmethod
    def build_fluent_search_by_qualified_name(asset_type: Type[A], qualified_name: str):
        """
        Build FluentSearch query to find asset by qualified name.

        :param asset_type: type of asset to search for
        :param qualified_name: qualified name to search for
        :returns: FluentSearch query
        """
        from pyatlan.model.fluent_search import FluentSearch

        return (
            FluentSearch()
            .select()
            .where(Asset.TYPE_NAME.eq(asset_type.__name__))
            .where(asset_type.QUALIFIED_NAME.eq(qualified_name))
        )

    @staticmethod
    def validate_search_results(
        results, asset_type: Type[A], guid: Optional[str], qualified_name: Optional[str]
    ):
        """
        Validate search results and extract the first asset.

        :param results: search results
        :param asset_type: expected asset type
        :param guid: GUID used for search (if any)
        :param qualified_name: qualified name used for search (if any)
        :returns: first asset from results
        :raises AtlanError: if validation fails
        """
        if results and results.current_page():
            first_result = results.current_page()[0]
            if not isinstance(first_result, asset_type):
                if guid is None:
                    raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                        asset_type.__name__, qualified_name
                    )
                else:
                    raise ErrorCode.ASSET_NOT_TYPE_REQUESTED.exception_with_parameters(
                        guid, asset_type.__name__
                    )
            return first_result
        else:
            if guid is None:
                raise ErrorCode.ASSET_NOT_FOUND_BY_QN.exception_with_parameters(
                    qualified_name, asset_type.__name__
                )
            else:
                raise ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters(guid)

    @staticmethod
    def process_terms_with_semantic(
        terms: List[AtlasGlossaryTerm], semantic: SaveSemantic
    ) -> List[AtlasGlossaryTerm]:
        """
        Process terms list with the specified save semantic.

        :param terms: list of terms to process
        :param semantic: save semantic to apply
        :returns: processed terms list
        """
        processed_terms = []
        for term in terms:
            if hasattr(term, "guid") and term.guid:
                processed_terms.append(
                    AtlasGlossaryTerm.ref_by_guid(guid=term.guid, semantic=semantic)
                )
            elif hasattr(term, "qualified_name") and term.qualified_name:
                processed_terms.append(
                    AtlasGlossaryTerm.ref_by_qualified_name(
                        qualified_name=term.qualified_name, semantic=semantic
                    )
                )
        return processed_terms

    @staticmethod
    def process_save_response(response, asset_type: Type[A], updated_asset: A) -> A:
        """
        Process the save response to extract the updated asset.

        :param response: AssetMutationResponse from save operation
        :param asset_type: type of asset that was updated
        :param updated_asset: the asset updater that was saved
        :returns: the updated asset or the updater if no assets found
        """
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return updated_asset


class SearchForAssetWithName:
    """Shared business logic for searching assets by name."""

    @staticmethod
    def build_search_request(
        query: Query, attributes: Optional[List]
    ) -> IndexSearchRequest:
        """
        Build an IndexSearchRequest from a query and attributes.

        :param query: query to execute
        :param attributes: optional collection of attributes to retrieve
        :returns: IndexSearchRequest object
        """
        dsl = DSL(query=query)
        return IndexSearchRequest(
            dsl=dsl, attributes=attributes, relation_attributes=["name"]
        )

    @staticmethod
    def process_search_results(
        results, name: str, asset_type: Type[A], allow_multiple: bool = False
    ) -> List[A]:
        """
        Process search results and validate the found assets.

        :param results: search results
        :param name: name that was searched for (for error messages)
        :param asset_type: expected asset type
        :param allow_multiple: whether multiple results are allowed
        :returns: list of found assets
        :raises NotFoundError: if no assets found or validation fails
        """
        import logging

        LOGGER = logging.getLogger(__name__)

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

    @staticmethod
    async def process_async_search_results(
        results, name: str, asset_type: Type[A], allow_multiple: bool = False
    ) -> List[A]:
        """
        Async version of process_search_results for handling async search results.

        :param results: async search results
        :param name: name that was searched for (for error messages)
        :param asset_type: expected asset type
        :param allow_multiple: whether multiple results are allowed
        :returns: list of found assets
        :raises NotFoundError: if no assets found or validation fails
        """
        import logging

        LOGGER = logging.getLogger(__name__)

        if results and results.count > 0:
            # For async results, we need to handle iteration differently
            current_page = (
                results.current_page() if hasattr(results, "current_page") else None
            )
            if current_page:
                # Use current page if available
                assets = [
                    asset for asset in current_page if isinstance(asset, asset_type)
                ]
            else:
                # Otherwise, collect from async iterator
                assets = []
                async for asset in results:
                    if isinstance(asset, asset_type):
                        assets.append(asset)

            if assets:
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


class FindConnectionsByName:
    """Shared business logic for finding connections by name."""

    @staticmethod
    def build_query(name: str, connector_type: AtlanConnectorType) -> Query:
        """
        Build query for finding connections by name and connector type.

        :param name: name of the connection
        :param connector_type: type of connector
        :returns: Query object
        """
        return (
            Term.with_state("ACTIVE")
            + Term.with_type_name("CONNECTION")
            + Term.with_name(name)
            + Term(field="connectorName", value=connector_type.value)
        )


class FindGlossaryByName:
    """Shared business logic for finding glossary by name."""

    @staticmethod
    def build_query(name: str) -> Query:
        """
        Build query for finding glossary by name.

        :param name: name of the glossary
        :returns: Query object
        """
        return with_active_glossary(name=name)


class FindCategoryFastByName:
    """Shared business logic for finding category by name (fast version with glossary qualified name)."""

    @staticmethod
    def build_query(name: str, glossary_qualified_name: str) -> Query:
        """
        Build query for finding category by name within a specific glossary.

        :param name: name of the category
        :param glossary_qualified_name: qualified name of the glossary
        :returns: Query object
        """
        return with_active_category(
            name=name, glossary_qualified_name=glossary_qualified_name
        )


class FindTermFastByName:
    """Shared business logic for finding term by name (fast version with glossary qualified name)."""

    @staticmethod
    def build_query(name: str, glossary_qualified_name: str) -> Query:
        """
        Build query for finding term by name within a specific glossary.

        :param name: name of the term
        :param glossary_qualified_name: qualified name of the glossary
        :returns: Query object
        """
        return with_active_term(
            name=name, glossary_qualified_name=glossary_qualified_name
        )


class FindDomainByName:
    """Shared business logic for finding data domain by name."""

    @staticmethod
    def build_query(name: str) -> Query:
        """
        Build query for finding data domain by name.

        :param name: name of the domain
        :returns: Query object
        """
        return (
            Term.with_state("ACTIVE")
            + Term.with_name(name)
            + Term.with_type_name("DataDomain")
        )


class FindProductByName:
    """Shared business logic for finding data product by name."""

    @staticmethod
    def build_query(name: str) -> Query:
        """
        Build query for finding data product by name.

        :param name: name of the product
        :returns: Query object
        """
        return (
            Term.with_state("ACTIVE")
            + Term.with_name(name)
            + Term.with_type_name("DataProduct")
        )


class GetHierarchy:
    """Shared business logic for retrieving category hierarchy in a glossary."""

    @staticmethod
    def validate_glossary(glossary):
        """
        Validate that the glossary has required qualified_name.

        :param glossary: AtlasGlossary to validate
        :raises: ErrorCode.GLOSSARY_MISSING_QUALIFIED_NAME if qualified_name is missing
        """
        if not glossary.qualified_name:
            from pyatlan.errors import ErrorCode

            raise ErrorCode.GLOSSARY_MISSING_QUALIFIED_NAME.exception_with_parameters()

    @staticmethod
    def prepare_search_request(
        glossary,
        attributes: Optional[List] = None,
        related_attributes: Optional[List] = None,
    ):
        """
        Prepare FluentSearch request for category hierarchy.

        :param glossary: AtlasGlossary to get hierarchy for
        :param attributes: attributes to retrieve for each category
        :param related_attributes: attributes to retrieve for related assets
        :returns: search request object
        """
        from pyatlan.model.fluent_search import FluentSearch

        if attributes is None:
            attributes = []
        if related_attributes is None:
            related_attributes = []

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
        return search.to_request()

    @staticmethod
    def process_search_results(response, glossary):
        """
        Process search results to build category hierarchy structure.

        :param response: search response containing categories
        :param glossary: AtlasGlossary for error messages
        :returns: CategoryHierarchy object
        """
        top_categories = set()
        category_dict = {}

        for category in filter(
            lambda a: isinstance(a, AtlasGlossaryCategory), response
        ):
            guid = category.guid
            category_dict[guid] = category
            if category.parent_category is None:
                top_categories.add(guid)

        if not top_categories:
            from pyatlan.errors import ErrorCode

            raise ErrorCode.NO_CATEGORIES.exception_with_parameters(
                glossary.guid, glossary.qualified_name
            )

        # Import CategoryHierarchy locally to avoid circular imports
        from pyatlan.client.asset import CategoryHierarchy

        return CategoryHierarchy(top_level=top_categories, stub_dict=category_dict)

    @staticmethod
    async def process_async_search_results(response, glossary):
        """
        Async version of process_search_results to handle AsyncIndexSearchResults.

        :param response: async search response containing categories
        :param glossary: AtlasGlossary for error messages
        :returns: CategoryHierarchy object
        """
        top_categories = set()
        category_dict = {}

        # Handle async iteration - check if we have current_page() or need async iteration
        if hasattr(response, "current_page") and response.current_page():
            # Use current page if available
            categories = [
                asset
                for asset in response.current_page()
                if isinstance(asset, AtlasGlossaryCategory)
            ]
        else:
            # Collect from async iterator
            categories = []
            async for asset in response:
                if isinstance(asset, AtlasGlossaryCategory):
                    categories.append(asset)

        for category in categories:
            guid = category.guid
            category_dict[guid] = category
            if category.parent_category is None:
                top_categories.add(guid)

        if not top_categories:
            from pyatlan.errors import ErrorCode

            raise ErrorCode.NO_CATEGORIES.exception_with_parameters(
                glossary.guid, glossary.qualified_name
            )

        # Import CategoryHierarchy locally to avoid circular imports
        from pyatlan.client.asset import CategoryHierarchy

        return CategoryHierarchy(top_level=top_categories, stub_dict=category_dict)
