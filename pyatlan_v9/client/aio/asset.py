# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

import asyncio
import json
import logging
from typing import (
    TYPE_CHECKING,
    Awaitable,
    Callable,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    overload,
)
from warnings import warn

import msgspec
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from pyatlan.client.asset import CategoryHierarchy
from pyatlan.client.common import (
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
    PurgeByGuid,
    RemoveAnnouncement,
    RemoveCertificate,
    RemoveCustomMetadata,
    ReplaceCustomMetadata,
    RestoreAsset,
    Search,
    SearchForAssetWithName,
    UpdateAnnouncement,
    UpdateAsset,
    UpdateAssetByAttribute,
    UpdateCertificate,
    UpdateCustomMetadataAttributes,
)
from pyatlan.client.constants import BULK_UPDATE, DELETE_ENTITIES_BY_GUIDS
from pyatlan.errors import ErrorCode, NotFoundError, PermissionError
from pyatlan.model.aio import AsyncIndexSearchResults, AsyncLineageListResults
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.utils import unflatten_custom_metadata_for_entity
from pyatlan_v9.model.aggregation import Aggregations
from pyatlan_v9.model.aio.core import AsyncAtlanRequest
from pyatlan_v9.model.assets import (
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
from pyatlan_v9.model.core import (
    Announcement,
    AtlanRequest,
    AtlanTag,
    AtlanTagName,
    BulkRequest,
)
from pyatlan_v9.model.custom_metadata import CustomMetadataDict
from pyatlan_v9.model.enums import (
    AtlanConnectorType,
    AtlanDeleteType,
    CertificateStatus,
    DataQualityScheduleType,
    EntityStatus,
    SaveSemantic,
    SortOrder,
)
from pyatlan_v9.model.lineage import LineageListRequest
from pyatlan_v9.model.response import AssetMutationResponse, MutatedEntities
from pyatlan_v9.model.search import IndexSearchRequest, Query
from pyatlan_v9.model.transform import from_atlas_format
from pyatlan_v9.validate import validate_arguments

if TYPE_CHECKING:
    pass

LOGGER = logging.getLogger(__name__)

A = TypeVar("A", bound=Asset)


# ---------------------------------------------------------------------------
# v9-native response helpers (raw JSON -> v9 msgspec assets)
# ---------------------------------------------------------------------------


def _custom_metadata_payload(custom_metadata_request):
    """Normalize custom metadata request wrappers to raw payload dictionaries."""
    if hasattr(custom_metadata_request, "to_dict") and callable(
        custom_metadata_request.to_dict
    ):
        return custom_metadata_request.to_dict()
    root_payload = getattr(custom_metadata_request, "__root__", None)
    if root_payload is not None:
        return root_payload
    if hasattr(custom_metadata_request, "dict") and callable(
        custom_metadata_request.dict
    ):
        return custom_metadata_request.dict(by_alias=True, exclude_none=True)
    return custom_metadata_request


def _parse_entities_v9(entities: list, criteria=None) -> list:
    """Parse raw entity dicts into v9 msgspec assets."""
    attributes = getattr(criteria, "attributes", None)
    for entity in entities:
        unflatten_custom_metadata_for_entity(entity=entity, attributes=attributes)
    return [from_atlas_format(e) for e in entities]


def _parse_mutation_response(raw_json: dict) -> AssetMutationResponse:
    """Build a v9 ``AssetMutationResponse`` from raw API JSON."""
    mutated = None
    if me_raw := raw_json.get("mutatedEntities"):
        mutated = MutatedEntities(
            CREATE=(
                _parse_entities_v9(me_raw["CREATE"]) if me_raw.get("CREATE") else None
            ),
            UPDATE=(
                _parse_entities_v9(me_raw["UPDATE"]) if me_raw.get("UPDATE") else None
            ),
            DELETE=(
                _parse_entities_v9(me_raw["DELETE"]) if me_raw.get("DELETE") else None
            ),
            PARTIAL_UPDATE=(
                _parse_entities_v9(me_raw["PARTIAL_UPDATE"])
                if me_raw.get("PARTIAL_UPDATE")
                else None
            ),
        )
    return AssetMutationResponse(
        guid_assignments=raw_json.get("guidAssignments"),
        mutated_entities=mutated,
        partial_updated_entities=(
            _parse_entities_v9(raw_json["partialUpdatedEntities"])
            if raw_json.get("partialUpdatedEntities")
            else None
        ),
    )


def _parse_aggregations_v9(raw: dict) -> Aggregations:
    """Convert raw aggregation JSON into a v9 ``Aggregations`` wrapper."""
    from pyatlan_v9.model.aggregation import (
        AggregationBucketResult,
        AggregationHitsResult,
        AggregationMetricResult,
    )

    def _parse_nested(bucket_dict: dict) -> "Aggregations | None":
        """Parse nested aggregation results inside a bucket, recursively."""
        nested: dict = {}
        known_keys = {
            "key",
            "doc_count",
            "key_as_string",
            "max_matching_length",
            "to",
            "to_as_string",
            "from",
            "from_as_string",
        }
        for k, v in bucket_dict.items():
            if k in known_keys or not isinstance(v, dict):
                continue
            try:
                if "buckets" in v:
                    result = msgspec.convert(v, AggregationBucketResult, strict=False)
                    raw_inner = v.get("buckets", [])
                    for i, inner in enumerate(result.buckets):
                        if i < len(raw_inner):
                            try:
                                inner.nested_results = _parse_nested(raw_inner[i])
                            except Exception:
                                pass
                    nested[k] = result
                elif "hits" in v:
                    nested[k] = msgspec.convert(v, AggregationHitsResult, strict=False)
                elif "value" in v:
                    nested[k] = msgspec.convert(
                        v, AggregationMetricResult, strict=False
                    )
            except Exception:
                pass
        return Aggregations(data=nested) if nested else None

    parsed: dict = {}
    for key, value in raw.items():
        if not isinstance(value, dict):
            continue
        try:
            if "buckets" in value:
                result = msgspec.convert(value, AggregationBucketResult, strict=False)
                raw_buckets = value.get("buckets", [])
                for i, bucket in enumerate(result.buckets):
                    if i < len(raw_buckets):
                        try:
                            bucket.nested_results = _parse_nested(raw_buckets[i])
                        except Exception:
                            pass
                parsed[key] = result
            elif "hits" in value:
                parsed[key] = msgspec.convert(
                    value, AggregationHitsResult, strict=False
                )
            elif "value" in value:
                parsed[key] = msgspec.convert(
                    value, AggregationMetricResult, strict=False
                )
        except Exception:
            pass
    return Aggregations(data=parsed)


def _process_search_response_v9(raw_json: dict, criteria) -> dict:
    """Process a search API response into v9 msgspec assets."""
    if "entities" in raw_json:
        assets = _parse_entities_v9(raw_json["entities"], criteria)
    else:
        assets = []

    aggregations = None
    if "aggregations" in raw_json:
        try:
            aggs = _parse_aggregations_v9(raw_json["aggregations"])
            if aggs._data:
                aggregations = aggs
        except Exception:
            pass

    return {
        "assets": assets,
        "aggregations": aggregations,
        "count": raw_json.get("approximateCount", 0),
    }


def _process_get_response_v9(
    raw_json: dict, identifier: str, asset_type, *, by_guid: bool = False
):
    """Process a get-by-guid/get-by-qualified-name API response into a v9 asset."""
    entity = raw_json["entity"]

    if not by_guid and entity.get("typeName") != asset_type.__name__:
        raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
            asset_type.__name__, identifier
        )

    if entity.get("relationshipAttributes"):
        entity.setdefault("attributes", {}).update(entity["relationshipAttributes"])
    entity["relationshipAttributes"] = {}

    asset = from_atlas_format(entity)
    asset.is_incomplete = False

    if not isinstance(asset, asset_type):
        if by_guid:
            raise ErrorCode.ASSET_NOT_TYPE_REQUESTED.exception_with_parameters(
                identifier, asset_type.__name__
            )
        else:
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                asset_type.__name__, identifier
            )
    return asset


def _process_lineage_response_v9(raw_json: dict, lineage_request) -> dict:
    """Process a lineage list API response into v9 msgspec assets."""
    if "entities" in raw_json:
        assets = _parse_entities_v9(raw_json["entities"], lineage_request)
        has_more = bool(raw_json.get("hasMore", False))
    else:
        assets = []
        has_more = False
    return {"assets": assets, "has_more": has_more}


# ---------------------------------------------------------------------------
# V9-native async search result subclasses
# ---------------------------------------------------------------------------


class V9AsyncIndexSearchResults(AsyncIndexSearchResults):
    """AsyncIndexSearchResults that deserializes pages into v9 msgspec assets."""

    def _process_entities(self, entities):
        self._assets = _parse_entities_v9(entities, self._criteria)


class V9AsyncLineageListResults(AsyncLineageListResults):
    """AsyncLineageListResults that deserializes pages into v9 msgspec assets."""

    async def next_page(self, start=None, size=None) -> bool:
        if not self._has_more:
            return False

        self._start = start or self._start + self._size
        if size:
            self._size = size

        self._criteria.offset = self._start
        self._criteria.size = self._size

        endpoint, request_obj = GetLineageList.prepare_request(self._criteria)
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)

        if "entities" in raw_json:
            self._assets = _parse_entities_v9(raw_json["entities"], self._criteria)
            self._has_more = bool(raw_json.get("hasMore", False))
        else:
            self._assets = []
            self._has_more = False

        return self._has_more


def _make_bulk_request_payload(entities: list, client) -> dict:
    """Serialize a list of Asset entities into an API-ready dict,
    applying AtlanTag retranslation (human names -> internal IDs).
    """
    bulk = BulkRequest(entities=entities)
    request_dict = bulk.to_dict()
    retranslated = AtlanRequest(instance=request_dict, client=client)
    return retranslated.translated


async def _make_bulk_request_payload_async(entities: list, client) -> dict:
    """Async version: serialize entities into API-ready dict with tag retranslation."""
    from pyatlan_v9.client.asset import _normalize_meanings_for_mutation

    bulk = BulkRequest(entities=entities)
    request_dict = bulk.to_dict()
    for entity in request_dict.get("entities", []):
        _normalize_meanings_for_mutation(entity)
    async_request = AsyncAtlanRequest(instance=request_dict, client=client)
    await async_request.retranslate()
    return async_request.translated


def _make_asset_request_payload(asset: Asset, client) -> dict:
    """Serialize a single Asset entity into an API-ready dict,
    applying AtlanTag retranslation.
    """
    asset_dict = {"entity": json.loads(asset.to_json(nested=True))}
    retranslated = AtlanRequest(instance=asset_dict, client=client)
    return retranslated.translated


async def _make_asset_request_payload_async(asset: Asset, client) -> dict:
    """Async version: serialize a single Asset entity into API-ready dict."""
    asset_dict = {"entity": json.loads(asset.to_json(nested=True))}
    async_request = AsyncAtlanRequest(instance=asset_dict, client=client)
    await async_request.retranslate()
    return async_request.translated


# ---------------------------------------------------------------------------
# V9 Async Asset Client (standalone)
# ---------------------------------------------------------------------------


class V9AsyncAssetClient:
    """
    Async asset client for the v9 SDK.

    All methods return v9 msgspec asset types. This is a standalone
    implementation — no wrapping or delegation to the legacy async client.
    """

    def __init__(self, client):
        self._client = client

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    async def search(
        self, criteria: IndexSearchRequest, bulk=False
    ) -> V9AsyncIndexSearchResults:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :param bulk: whether to run the search to retrieve assets that match the supplied criteria,
        for large numbers of results (> ``100,000``), defaults to ``False``.
        :raises InvalidRequestError: if bulk search is enabled and user-specified sorting is found
        :raises AtlanError: on any API communication issue
        :returns: the results of the search
        """
        endpoint, request_obj = Search.prepare_request(criteria, bulk)
        raw_json = await self._client._call_api(
            endpoint,
            request_obj=request_obj,
        )
        response = _process_search_response_v9(raw_json, criteria)

        if Search._check_for_bulk_search(
            criteria, response["count"], bulk, V9AsyncIndexSearchResults
        ):
            return await self.search(criteria)

        return V9AsyncIndexSearchResults(
            self._client,
            criteria,
            criteria.dsl.from_,
            criteria.dsl.size,
            response["count"],
            response["assets"],
            response["aggregations"],
            bulk,
        )

    # ------------------------------------------------------------------
    # Lineage
    # ------------------------------------------------------------------

    async def get_lineage_list(
        self, lineage_request: LineageListRequest
    ) -> V9AsyncLineageListResults:
        """
        Retrieve lineage using the higher-performance "list" API.

        :param lineage_request: detailing the lineage query, parameters, and so on to run
        :returns: the results of the lineage request
        :raises InvalidRequestError: if the requested lineage direction is 'BOTH'
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = GetLineageList.prepare_request(lineage_request)
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        response = _process_lineage_response_v9(raw_json, lineage_request)
        return V9AsyncLineageListResults(
            client=self._client,
            criteria=lineage_request,
            start=lineage_request.offset or 0,
            size=lineage_request.size or 10,
            has_more=response["has_more"],
            assets=response["assets"],
        )

    # ------------------------------------------------------------------
    # Find by name helpers
    # ------------------------------------------------------------------

    def _prepare_fluent_search(
        self,
        wheres: List[Query],
        attributes: Optional[List[str]] = None,
        related_attributes: Optional[List[str]] = None,
    ):
        from pyatlan_v9.model.fluent_search import FluentSearch

        search = FluentSearch()
        for w in wheres:
            search = search.where(w)
        for attr in attributes or []:
            search = search.include_on_results(attr)
        for rel_attr in related_attributes or []:
            search = search.include_on_relations(rel_attr)
        return search

    def _build_find_request(
        self,
        name: str,
        type_name: str,
        attributes: Optional[List[str]] = None,
    ) -> IndexSearchRequest:
        from pyatlan.model.search import Term
        from pyatlan_v9.model.search import DSL as V9DSL

        if attributes is None:
            attributes = []
        query = (
            Term.with_state("ACTIVE")
            + Term.with_type_name(type_name)
            + Term.with_name(name)
        )
        dsl = V9DSL(query=query)
        return IndexSearchRequest(
            dsl=dsl, attributes=attributes, relation_attributes=["name"]
        )

    @validate_arguments
    async def find_personas_by_name(
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
        search_request = self._build_find_request(name, "PERSONA", attributes)
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
        Find a purpose by its human-readable name.

        :param name: of the purpose
        :param attributes: (optional) collection of attributes to retrieve for the purpose
        :returns: all purposes with that name, if found
        :raises NotFoundError: if no purpose with the provided name exists
        """
        search_request = self._build_find_request(name, "PURPOSE", attributes)
        search_results = await self.search(search_request)
        return FindPurposesByName.process_response(
            search_results, name, allow_multiple=True
        )

    # ------------------------------------------------------------------
    # Get by qualified name / GUID
    # ------------------------------------------------------------------

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
        Retrieves an asset by its qualified_name.

        :param qualified_name: qualified_name of the asset to be retrieved
        :param asset_type: type of asset to be retrieved
        :param min_ext_info: whether to minimize extra info (True) or not (False)
        :param ignore_relationships: whether to include relationships (False) or exclude them (True)
        :param attributes: a specific list of attributes to retrieve for the asset
        :param related_attributes: a specific list of relationships attributes to retrieve for the asset
        :returns: the requested asset
        :raises NotFoundError: if the asset does not exist
        :raises AtlanError: on any API communication issue
        """
        normalized_attributes = GetByQualifiedName.normalize_search_fields(attributes)
        normalized_related_attributes = GetByQualifiedName.normalize_search_fields(
            related_attributes
        )

        if (normalized_attributes and len(normalized_attributes)) or (
            normalized_related_attributes and len(normalized_related_attributes)
        ):
            search = self._prepare_fluent_search(
                wheres=[
                    Asset.QUALIFIED_NAME.eq(qualified_name),
                    Asset.TYPE_NAME.eq(asset_type.__name__),
                ],
                attributes=normalized_attributes,
                related_attributes=normalized_related_attributes,
            )
            results = await search.execute_async(client=self._client)
            if results and results.current_page():
                first_result = results.current_page()[0]
                if isinstance(first_result, asset_type):
                    return first_result
                raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                    asset_type.__name__, qualified_name
                )
            raise ErrorCode.ASSET_NOT_FOUND_BY_QN.exception_with_parameters(
                qualified_name, asset_type.__name__
            )

        endpoint_path, query_params = GetByQualifiedName.prepare_direct_api_request(
            qualified_name, asset_type, min_ext_info, ignore_relationships
        )
        raw_json = await self._client._call_api(endpoint_path, query_params)
        return _process_get_response_v9(
            raw_json, qualified_name, asset_type, by_guid=False
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
        Retrieves an asset by its GUID.

        :param guid: unique identifier (GUID) of the asset to retrieve
        :param asset_type: type of asset to be retrieved, defaults to ``Asset``
        :param min_ext_info: whether to minimize extra info (True) or not (False)
        :param ignore_relationships: whether to include relationships (False) or exclude them (True)
        :param attributes: a specific list of attributes to retrieve for the asset
        :param related_attributes: a specific list of relationships attributes to retrieve for the asset
        :returns: the requested asset
        :raises NotFoundError: if the asset does not exist, or is not of the type requested
        :raises AtlanError: on any API communication issue
        """
        normalized_attributes = GetByQualifiedName.normalize_search_fields(attributes)
        normalized_related_attributes = GetByQualifiedName.normalize_search_fields(
            related_attributes
        )

        if (normalized_attributes and len(normalized_attributes)) or (
            normalized_related_attributes and len(normalized_related_attributes)
        ):
            search = self._prepare_fluent_search(
                wheres=[
                    Asset.GUID.eq(guid),
                    Asset.TYPE_NAME.eq(asset_type.__name__),
                ],
                attributes=normalized_attributes,
                related_attributes=normalized_related_attributes,
            )
            results = await search.execute_async(client=self._client)
            if results and results.current_page():
                first_result = results.current_page()[0]
                if isinstance(first_result, asset_type):
                    return first_result
                raise ErrorCode.ASSET_NOT_TYPE_REQUESTED.exception_with_parameters(
                    guid, asset_type.__name__
                )
            raise ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters(guid)

        endpoint_path, query_params = GetByGuid.prepare_direct_api_request(
            guid, min_ext_info, ignore_relationships
        )
        raw_json = await self._client._call_api(endpoint_path, query_params)
        return _process_get_response_v9(raw_json, guid, asset_type, by_guid=True)

    @validate_arguments
    async def retrieve_minimal(
        self,
        guid: str,
        asset_type: Type[A] = Asset,  # type: ignore[assignment]
    ) -> A:
        """
        Retrieves an asset by its GUID, without any of its relationships.

        :param guid: unique identifier (GUID) of the asset to retrieve
        :param asset_type: type of asset to be retrieved, defaults to ``Asset``
        :returns: the asset, without any of its relationships
        :raises NotFoundError: if the asset does not exist
        """
        return await self.get_by_guid(
            guid=guid,
            asset_type=asset_type,
            min_ext_info=True,
            ignore_relationships=True,
        )

    # ------------------------------------------------------------------
    # Save / Upsert
    # ------------------------------------------------------------------

    @validate_arguments
    async def upsert(
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
        return await self.save(
            entity=entity,
            replace_atlan_tags=replace_atlan_tags,
            replace_custom_metadata=replace_custom_metadata,
            overwrite_custom_metadata=overwrite_custom_metadata,
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
        If an asset with the same qualified_name exists, updates the existing asset.
        Otherwise, creates the asset.

        :param entity: one or more assets to save
        :param replace_atlan_tags: whether to replace AtlanTags during an update (True) or not (False)
        :param replace_custom_metadata: replaces any custom metadata with non-empty values provided
        :param overwrite_custom_metadata: overwrites any custom metadata, even with empty values
        :param append_atlan_tags: whether to add/update/remove AtlanTags during an update (True) or not (False)
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
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

        for asset in entities:
            asset.validate_required()
            await asset.flush_custom_metadata_async(client=self._client)

        request_payload = await _make_bulk_request_payload_async(entities, self._client)
        raw_json = await self._client._call_api(
            BULK_UPDATE, query_params, request_payload
        )
        response = _parse_mutation_response(raw_json)

        if connections_created := response.assets_created(Connection):
            await self._wait_for_connections_to_be_created(connections_created)
        return response

    async def _wait_for_connections_to_be_created(self, connections_created):
        guids = [c.guid for c in connections_created]
        LOGGER.debug("Waiting for connections")

        @retry(
            retry=retry_if_exception_type(PermissionError),
            wait=wait_exponential(multiplier=1, min=1, max=8),
            stop=stop_after_attempt(10),
            reraise=True,
        )
        async def _retrieve_connection_with_retry(guid):
            await self.retrieve_minimal(guid=guid, asset_type=Connection)

        for guid in guids:
            await _retrieve_connection_with_retry(guid)

        LOGGER.debug("Finished waiting for connections")

    @validate_arguments
    async def upsert_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use save_merging_cm() instead."""
        warn(
            "This method is deprecated, please use 'save_merging_cm' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    async def save_merging_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
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
        If no asset exists, fails with a NotFoundError. Will merge any provided
        custom metadata with any custom metadata that already exists on the asset.

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
        return await self.save_merging_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    async def upsert_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """Deprecated - use save_replacing_cm() instead."""
        warn(
            "This method is deprecated, please use 'save_replacing_cm' instead, which offers identical functionality.",
            DeprecationWarning,
            stacklevel=2,
        )
        return await self.save_replacing_cm(
            entity=entity, replace_atlan_tags=replace_atlan_tags
        )

    @validate_arguments
    async def save_replacing_cm(
        self, entity: Union[Asset, List[Asset]], replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, has the same behavior as save(), while also setting
        any custom metadata provided.
        If an asset does exist, optionally overwrites any Atlan tags.
        Will overwrite all custom metadata on any existing asset with only the
        custom metadata provided.

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
            await asset.flush_custom_metadata_async(self._client)

        request_payload = await _make_bulk_request_payload_async(entities, self._client)
        raw_json = await self._client._call_api(
            BULK_UPDATE, query_params, request_payload
        )
        return _parse_mutation_response(raw_json)

    @validate_arguments
    async def update_replacing_cm(
        self, entity: Asset, replace_atlan_tags: bool = False
    ) -> AssetMutationResponse:
        """
        If no asset exists, fails with a NotFoundError.
        Will overwrite all custom metadata on any existing asset with only the
        custom metadata provided.

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

    # ------------------------------------------------------------------
    # Delete / Purge / Restore
    # ------------------------------------------------------------------

    @validate_arguments
    async def purge_by_guid(
        self,
        guid: Union[str, List[str]],
        delete_type: AtlanDeleteType = AtlanDeleteType.PURGE,
    ) -> AssetMutationResponse:
        """
        Deletes one or more assets by their unique identifier (GUID) using the specified delete type.

        :param guid: unique identifier(s) (GUIDs) of one or more assets to delete
        :param delete_type: type of deletion to perform (PURGE or HARD)
        :returns: details of the deleted asset(s)
        :raises AtlanError: on any API communication issue
        """
        query_params = PurgeByGuid.prepare_request(guid, delete_type)
        raw_json = await self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        return _parse_mutation_response(raw_json)

    @validate_arguments
    async def delete_by_guid(
        self, guid: Union[str, List[str]]
    ) -> AssetMutationResponse:
        """
        Soft-deletes (archives) one or more assets by their unique identifier (GUID).

        :param guid: unique identifier(s) (GUIDs) of one or more assets to soft-delete
        :returns: details of the soft-deleted asset(s)
        :raises AtlanError: on any API communication issue
        """
        guids = DeleteByGuid.prepare_request(guid)

        assets = []
        for single_guid in guids:
            asset = await self.retrieve_minimal(guid=single_guid, asset_type=Asset)
            assets.append(asset)
        DeleteByGuid.validate_assets_can_be_archived(assets)

        query_params = DeleteByGuid.prepare_delete_request(guids)
        raw_json = await self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        response = _parse_mutation_response(raw_json)

        for asset in response.assets_deleted(asset_type=Asset):
            await self._wait_till_deleted(asset)
        return response

    async def _wait_till_deleted(self, asset: Asset):
        max_attempts = 20
        for attempt in range(max_attempts):
            try:
                retrieved = await self.retrieve_minimal(
                    guid=asset.guid, asset_type=Asset
                )
                if getattr(retrieved, "status", None) == EntityStatus.DELETED:
                    return
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from e
            await asyncio.sleep(1)
        raise ErrorCode.RETRY_OVERRUN.exception_with_parameters()

    @validate_arguments
    async def restore(self, asset_type: Type[A], qualified_name: str) -> bool:
        """
        Restore an archived (soft-deleted) asset to active.

        :param asset_type: type of the asset to restore
        :param qualified_name: of the asset to restore
        :returns: True if the asset is now restored, or False if not
        :raises AtlanError: on any API communication issue
        """
        return await self._restore(asset_type, qualified_name, 0)

    async def _restore(
        self, asset_type: Type[A], qualified_name: str, retries: int
    ) -> bool:
        if not RestoreAsset.can_asset_type_be_archived(asset_type):
            return False

        existing = await self.get_by_qualified_name(
            asset_type=asset_type,
            qualified_name=qualified_name,
            ignore_relationships=False,
        )
        if not existing:
            return False
        elif RestoreAsset.is_asset_active(existing):
            if retries < 10:
                await asyncio.sleep(2)
                return await self._restore(asset_type, qualified_name, retries + 1)
            else:
                return True
        else:
            response = await self._restore_asset(existing)
            return RestoreAsset.is_restore_successful(response)

    async def _restore_asset(self, asset: Asset) -> AssetMutationResponse:
        to_restore = asset.trim_to_required()
        to_restore.status = EntityStatus.ACTIVE

        query_params = {
            "replaceClassifications": False,
            "replaceBusinessAttributes": False,
            "overwriteBusinessAttributes": False,
        }

        entities = [to_restore]
        for restored in entities:
            await restored.flush_custom_metadata_async(self._client)

        request_payload = await _make_bulk_request_payload_async(entities, self._client)
        raw_json = await self._client._call_api(
            BULK_UPDATE, query_params, request_payload
        )
        return _parse_mutation_response(raw_json)

    # ------------------------------------------------------------------
    # Atlan Tags
    # ------------------------------------------------------------------

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
        if save_parameters is None:
            save_parameters = {}

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
                attributes=["anchor"],
            )

        retrieved_asset = await _get_asset_with_retry()

        if asset_type in (AtlasGlossaryTerm, AtlasGlossaryCategory):
            updated_asset = asset_type.updater(
                qualified_name=qualified_name,
                name=retrieved_asset.name,
                glossary_guid=retrieved_asset.anchor.guid,
            )
        else:
            updated_asset = asset_type.updater(
                qualified_name=qualified_name, name=retrieved_asset.name
            )

        tags = [
            AtlanTag(
                type_name=AtlanTagName(display_text=name),
                propagate=propagate,
                remove_propagations_on_entity_delete=remove_propagation_on_delete,
                restrict_propagation_through_lineage=restrict_lineage_propagation,
                restrict_propagation_through_hierarchy=restrict_propagation_through_hierarchy,
            )
            for name in atlan_tag_names
        ]

        if modification_type in ("add", "update"):
            updated_asset.add_or_update_classifications = tags
        elif modification_type == "remove":
            updated_asset.remove_classifications = tags
        elif modification_type == "replace":
            updated_asset.classifications = tags

        response = await self.save(entity=updated_asset, **save_parameters)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return updated_asset

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
        Add one or more Atlan tags to the provided asset.

        :param asset_type: type of asset to which to add the Atlan tags
        :param qualified_name: qualified_name of the asset
        :param atlan_tag_names: human-readable names of the Atlan tags to add
        :param propagate: whether to propagate the Atlan tag
        :param remove_propagation_on_delete: whether to remove propagated tags on deletion
        :param restrict_lineage_propagation: whether to avoid propagating through lineage
        :param restrict_propagation_through_hierarchy: whether to prevent hierarchy propagation
        :returns: the asset that was updated
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
        Update one or more Atlan tags to the provided asset.

        :param asset_type: type of asset to which to update the Atlan tags
        :param qualified_name: qualified_name of the asset
        :param atlan_tag_names: human-readable names of the Atlan tags to update
        :param propagate: whether to propagate the Atlan tag
        :param remove_propagation_on_delete: whether to remove propagated tags on deletion
        :param restrict_lineage_propagation: whether to avoid propagating through lineage
        :param restrict_propagation_through_hierarchy: whether to prevent hierarchy propagation
        :returns: the asset that was updated
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
        Removes a single Atlan tag from the provided asset.

        :param asset_type: type of asset from which to remove the Atlan tag
        :param qualified_name: qualified_name of the asset
        :param atlan_tag_name: human-readable name of the Atlan tag to remove
        :returns: the asset that was updated
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
        Removes one or more Atlan tags from the provided asset.

        :param asset_type: type of asset from which to remove the Atlan tags
        :param qualified_name: qualified_name of the asset
        :param atlan_tag_names: human-readable names of the Atlan tags to remove
        :returns: the asset that was updated
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

    # ------------------------------------------------------------------
    # Update asset by attribute (certificate, announcement, etc.)
    # ------------------------------------------------------------------

    async def _update_asset_by_attribute(
        self, asset: A, asset_type: Type[A], qualified_name: str
    ) -> Optional[A]:
        query_params = UpdateAssetByAttribute.prepare_request_params(qualified_name)
        await asset.flush_custom_metadata_async(client=self._client)
        endpoint = UpdateAssetByAttribute.get_api_endpoint(asset_type)
        asset_dict = {"entity": json.loads(asset.to_json(nested=True))}
        raw_json = await self._client._call_api(endpoint, query_params, asset_dict)
        response = _parse_mutation_response(raw_json)
        if assets := response.assets_partially_updated(asset_type=asset_type):
            return assets[0]
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return None

    # ------------------------------------------------------------------
    # Certificates
    # ------------------------------------------------------------------

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
        Update the certificate on an asset.

        :param asset_type: type of asset on which to update the certificate
        :param qualified_name: the qualified_name of the asset
        :param name: the name of the asset
        :param certificate_status: specific certificate to set on the asset
        :param glossary_guid: unique identifier of the glossary (required for glossary types)
        :param message: (optional) message to set
        :returns: the result of the update, or None if the update failed
        :raises AtlanError: on any API communication issue
        """
        asset = UpdateCertificate.prepare_asset_with_certificate(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            certificate_status=certificate_status,
            message=message,
            glossary_guid=glossary_guid,
        )
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
        Remove the certificate from an asset.

        :param asset_type: type of asset from which to remove the certificate
        :param qualified_name: the qualified_name of the asset
        :param name: the name of the asset
        :param glossary_guid: unique identifier of the glossary (required for glossary types)
        :returns: the result of the removal, or None if the removal failed
        """
        asset = RemoveCertificate.prepare_asset_for_certificate_removal(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            glossary_guid=glossary_guid,
        )
        return await self._update_asset_by_attribute(asset, asset_type, qualified_name)

    # ------------------------------------------------------------------
    # Announcements
    # ------------------------------------------------------------------

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

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def update_announcement(
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
        :param qualified_name: the qualified_name of the asset
        :param name: the name of the asset
        :param announcement: to apply to the asset
        :param glossary_guid: unique identifier of the glossary (required for glossary types)
        :returns: the result of the update, or None if the update failed
        """
        asset = UpdateAnnouncement.prepare_asset_with_announcement(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            announcement=announcement,
            glossary_guid=glossary_guid,
        )
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
        Remove the announcement from an asset.

        :param asset_type: type of asset from which to remove the announcement
        :param qualified_name: the qualified_name of the asset
        :param glossary_guid: unique identifier of the glossary (required for glossary types)
        :returns: the result of the removal, or None if the removal failed
        """
        asset = RemoveAnnouncement.prepare_asset_for_announcement_removal(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            glossary_guid=glossary_guid,
        )
        return await self._update_asset_by_attribute(asset, asset_type, qualified_name)

    # ------------------------------------------------------------------
    # Custom metadata
    # ------------------------------------------------------------------

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def update_custom_metadata_attributes(
        self, guid: str, custom_metadata: CustomMetadataDict
    ):
        """
        Update only the provided custom metadata attributes on the asset.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to update
        :raises AtlanError: on any API communication issue
        """
        custom_metadata_request = UpdateCustomMetadataAttributes.prepare_request(
            custom_metadata
        )
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )
        payload = _custom_metadata_payload(custom_metadata_request)
        await self._client._call_api(endpoint, None, payload)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def replace_custom_metadata(
        self, guid: str, custom_metadata: CustomMetadataDict
    ):
        """
        Replace specific custom metadata on the asset.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to replace
        :raises AtlanError: on any API communication issue
        """
        custom_metadata_request = ReplaceCustomMetadata.prepare_request(custom_metadata)
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )
        payload = _custom_metadata_payload(custom_metadata_request)
        await self._client._call_api(endpoint, None, payload)

    @validate_arguments
    async def remove_custom_metadata(self, guid: str, cm_name: str):
        """
        Remove specific custom metadata from an asset.

        :param guid: unique identifier (GUID) of the asset
        :param cm_name: human-readable name of the custom metadata to remove
        :raises AtlanError: on any API communication issue
        """
        custom_metadata_request = RemoveCustomMetadata.prepare_request(
            cm_name, self._client
        )
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )
        payload = _custom_metadata_payload(custom_metadata_request)
        await self._client._call_api(endpoint, None, payload)

    # ------------------------------------------------------------------
    # Terms management
    # ------------------------------------------------------------------

    async def _search_for_asset_with_name(
        self,
        query: Query,
        name: str,
        asset_type: Type[A],
        attributes: Optional[List],
        allow_multiple: bool = False,
    ) -> List[A]:
        from pyatlan_v9.model.search import DSL as V9DSL

        dsl = V9DSL(query=query)
        search_request = IndexSearchRequest(
            dsl=dsl,
            attributes=attributes or [],
            relation_attributes=["name"],
        )
        results = await self.search(search_request)
        return await SearchForAssetWithName.process_async_search_results(
            results, name, asset_type, allow_multiple
        )

    async def _manage_terms(
        self,
        asset_type: Type[A],
        terms: List[AtlasGlossaryTerm],
        save_semantic: SaveSemantic,
        guid: Optional[str] = None,
        qualified_name: Optional[str] = None,
    ) -> A:
        from pyatlan_v9.model.fluent_search import FluentSearch

        ManageTerms.validate_guid_and_qualified_name(guid, qualified_name)

        if guid:
            search_query = (
                FluentSearch()
                .select()
                .where(Asset.TYPE_NAME.eq(asset_type.__name__))
                .where(asset_type.GUID.eq(guid))
            )
        else:
            if qualified_name is None:
                raise ValueError(
                    "qualified_name cannot be None when guid is not provided"
                )
            search_query = (
                FluentSearch()
                .select()
                .where(Asset.TYPE_NAME.eq(asset_type.__name__))
                .where(asset_type.QUALIFIED_NAME.eq(qualified_name))
            )

        results = await search_query.execute_async(client=self._client)
        first_result = ManageTerms.validate_search_results(
            results, asset_type, guid, qualified_name
        )
        updated_asset = asset_type.updater(
            qualified_name=first_result.qualified_name, name=first_result.name
        )
        processed_terms: list[AtlasGlossaryTerm] = []
        for term in terms:
            if getattr(term, "guid", None):
                processed_terms.append(
                    AtlasGlossaryTerm.ref_by_guid(
                        guid=term.guid, semantic=save_semantic
                    )
                )
            elif getattr(term, "qualified_name", None):
                processed_terms.append(
                    AtlasGlossaryTerm.ref_by_qualified_name(
                        qualified_name=term.qualified_name,
                        semantic=save_semantic,
                    )
                )
        updated_asset.assigned_terms = processed_terms
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
        Link additional terms to an asset, without replacing existing terms.

        :param asset_type: type of the asset
        :param terms: the list of terms to append to the asset
        :param guid: unique identifier (GUID) of the asset
        :param qualified_name: the qualified_name of the asset
        :returns: the asset that was updated
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
        Replace the terms linked to an asset.

        :param asset_type: type of the asset
        :param terms: the list of terms to replace on the asset
        :param guid: unique identifier (GUID) of the asset
        :param qualified_name: the qualified_name of the asset
        :returns: the asset that was updated
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
        Remove terms from an asset, without replacing all existing terms.

        :param asset_type: type of the asset
        :param terms: the list of terms to remove from the asset
        :param guid: unique identifier (GUID) of the asset
        :param qualified_name: the qualified_name of the asset
        :returns: the asset that was updated
        """
        return await self._manage_terms(
            asset_type=asset_type,
            terms=terms,
            save_semantic=SaveSemantic.REMOVE,
            guid=guid,
            qualified_name=qualified_name,
        )

    # ------------------------------------------------------------------
    # Find by name
    # ------------------------------------------------------------------

    @validate_arguments
    async def find_connections_by_name(
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
        query = FindConnectionsByName.build_query(name, connector_type)
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
        name: str,
        attributes: Optional[List[str]] = None,
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
        query = FindGlossaryByName.build_query(name)
        results = await self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossary, attributes=attributes
        )
        return results[0]

    @validate_arguments
    async def find_category_fast_by_name(
        self,
        name: str,
        glossary_qualified_name: str,
        attributes: Optional[List[str]] = None,
    ) -> List[AtlasGlossaryCategory]:
        """
        Find a category by its human-readable name.

        :param name: of the category
        :param glossary_qualified_name: qualified_name of the glossary
        :param attributes: (optional) collection of attributes to retrieve for the category
        :returns: the category, if found
        :raises NotFoundError: if no category with the provided name exists
        """
        if attributes is None:
            attributes = []
        query = FindCategoryFastByName.build_query(name, glossary_qualified_name)
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
        name: str,
        glossary_name: str,
        attributes: Optional[List[str]] = None,
    ) -> List[AtlasGlossaryCategory]:
        """
        Find a category by its human-readable name.

        :param name: of the category
        :param glossary_name: human-readable name of the glossary
        :param attributes: (optional) collection of attributes to retrieve for the category
        :returns: the category, if found
        :raises NotFoundError: if no category with the provided name exists
        """
        glossary = await self.find_glossary_by_name(name=glossary_name)
        return await self.find_category_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )

    @validate_arguments
    async def find_term_fast_by_name(
        self,
        name: str,
        glossary_qualified_name: str,
        attributes: Optional[List[str]] = None,
    ) -> AtlasGlossaryTerm:
        """
        Find a term by its human-readable name.

        :param name: of the term
        :param glossary_qualified_name: qualified_name of the glossary
        :param attributes: (optional) collection of attributes to retrieve for the term
        :returns: the term, if found
        :raises NotFoundError: if no term with the provided name exists
        """
        if attributes is None:
            attributes = []
        query = FindTermFastByName.build_query(name, glossary_qualified_name)
        results = await self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossaryTerm, attributes=attributes
        )
        return results[0]

    @validate_arguments
    async def find_term_by_name(
        self,
        name: str,
        glossary_name: str,
        attributes: Optional[List[str]] = None,
    ) -> AtlasGlossaryTerm:
        """
        Find a term by its human-readable name.

        :param name: of the term
        :param glossary_name: human-readable name of the glossary
        :param attributes: (optional) collection of attributes to retrieve for the term
        :returns: the term, if found
        :raises NotFoundError: if no term with the provided name exists
        """
        glossary = await self.find_glossary_by_name(name=glossary_name)
        return await self.find_term_fast_by_name(
            name=name,
            glossary_qualified_name=glossary.qualified_name,
            attributes=attributes,
        )

    @validate_arguments
    async def find_domain_by_name(
        self,
        name: str,
        attributes: Optional[List[str]] = None,
    ) -> DataDomain:
        """
        Find a data domain by its human-readable name.

        :param name: of the domain
        :param attributes: (optional) collection of attributes to retrieve for the domain
        :returns: the domain, if found
        :raises NotFoundError: if no domain with the provided name exists
        """
        attributes = attributes or []
        query = FindDomainByName.build_query(name)
        results = await self._search_for_asset_with_name(
            query=query, name=name, asset_type=DataDomain, attributes=attributes
        )
        return results[0]

    @validate_arguments
    async def find_product_by_name(
        self,
        name: str,
        attributes: Optional[List[str]] = None,
    ) -> DataProduct:
        """
        Find a data product by its human-readable name.

        :param name: of the product
        :param attributes: (optional) collection of attributes to retrieve for the product
        :returns: the product, if found
        :raises NotFoundError: if no product with the provided name exists
        """
        attributes = attributes or []
        query = FindProductByName.build_query(name)
        results = await self._search_for_asset_with_name(
            query=query, name=name, asset_type=DataProduct, attributes=attributes
        )
        return results[0]

    # ------------------------------------------------------------------
    # Hierarchy
    # ------------------------------------------------------------------

    async def get_hierarchy(
        self,
        glossary: AtlasGlossary,
        attributes: Optional[List[Union[AtlanField, str]]] = None,
        related_attributes: Optional[List[Union[AtlanField, str]]] = None,
    ) -> CategoryHierarchy:
        """
        Retrieve category hierarchy in this Glossary, in a traversable form.

        :param glossary: the glossary to retrieve the category hierarchy for
        :param attributes: attributes to retrieve for each category in the hierarchy
        :param related_attributes: attributes to retrieve for each related asset in the hierarchy
        :returns: a traversable category hierarchy
        """
        from pyatlan.model.search import Term as SearchTerm
        from pyatlan_v9.model.fluent_search import FluentSearch

        GetHierarchy.validate_glossary(glossary)
        if attributes is None:
            attributes = []
        if related_attributes is None:
            related_attributes = []
        search = (
            FluentSearch.select()
            .where(AtlasGlossaryCategory.ANCHOR.eq(glossary.qualified_name))
            .where(SearchTerm.with_type_name("AtlasGlossaryCategory"))
            .include_on_results(AtlasGlossaryCategory.PARENT_CATEGORY)
            .page_size(20)
            .sort(AtlasGlossaryCategory.NAME.order(SortOrder.ASCENDING))
        )
        for field in attributes:
            search = search.include_on_results(field)
        for field in related_attributes:
            search = search.include_on_relations(field)
        request = search.to_request()
        response = await self.search(request)
        return await GetHierarchy.process_async_search_results(response, glossary)

    # ------------------------------------------------------------------
    # Bulk processing
    # ------------------------------------------------------------------

    async def process_assets(
        self,
        search,
        func: Callable[[Asset], Awaitable[None]],
    ) -> int:
        """
        Process assets matching a search query and apply a processing function
        to each unique asset.

        :param search: the search provider that generates search queries
        :param func: an async callable function that processes each unique asset
        :returns: the total number of unique assets that have been processed
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

    # ------------------------------------------------------------------
    # DQ helpers
    # ------------------------------------------------------------------

    @validate_arguments
    async def add_dq_rule_schedule(
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
        :param schedule_crontab: cron expression string defining the schedule
        :param schedule_time_zone: timezone for the schedule
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        """
        updated_asset = asset_type.updater(
            qualified_name=asset_qualified_name, name=asset_name
        )
        updated_asset.asset_d_q_schedule_time_zone = schedule_time_zone
        updated_asset.asset_d_q_schedule_crontab = schedule_crontab
        updated_asset.asset_d_q_schedule_type = DataQualityScheduleType.CRON
        return await self.save(updated_asset)

    @validate_arguments
    async def set_dq_row_scope_filter_column(
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
        :param row_scope_filter_column_qualified_name: the qualified name of the column
        :returns: the result of the save
        :raises AtlanError: on any API communication issue
        """
        updated_asset = asset_type.updater(
            qualified_name=asset_qualified_name, name=asset_name
        )
        updated_asset.asset_d_q_row_scope_filter_column_qualified_name = (
            row_scope_filter_column_qualified_name
        )
        return await self.save(updated_asset)
