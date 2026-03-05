# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

import json
import logging
import time
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    overload,
)
from warnings import warn

import msgspec
from tenacity import (
    RetryError,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
    wait_fixed,
)

# ---------------------------------------------------------------------------
# Re-export legacy utility classes that don't need migration
# (they are plain Python classes, not Pydantic models)
# ---------------------------------------------------------------------------
from pyatlan.client.asset import (  # noqa: F401
    AssetIdentity,
    Batch as _LegacyBatch,
    CategoryHierarchy,
    CustomMetadataHandling,
    FailedBatch,
    IndexSearchResults,
    LineageListResults,
    SearchResults,
)
from pyatlan.client.common import (
    ApiCaller,
    DeleteByGuid,
    FindCategoryFastByName,
    FindConnectionsByName,
    FindDomainByName,
    FindGlossaryByName,
    FindProductByName,
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
    UpdateAnnouncement,
    UpdateAsset,
    UpdateAssetByAttribute,
    UpdateCertificate,
    UpdateCustomMetadataAttributes,
)
from pyatlan.client.constants import BULK_UPDATE, DELETE_ENTITIES_BY_GUIDS
from pyatlan.errors import AtlanError, ErrorCode, NotFoundError, PermissionError
from pyatlan.model.fields.atlan_fields import AtlanField
from pyatlan.utils import unflatten_custom_metadata_for_entity
from pyatlan_v9.model.aggregation import Aggregations
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
    from pyatlan_v9.client.atlan import AtlanClient

LOGGER = logging.getLogger(__name__)

A = TypeVar("A", bound=Asset)


def _custom_metadata_payload(custom_metadata_request: Any) -> Any:
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


_GLOSSARY_ASSET_TYPES = {"AtlasGlossaryTerm", "AtlasGlossaryCategory"}


def _handle_v9_glossary_anchor(asset, asset_type_name: str, glossary_guid):
    """Set glossary anchor on v9 glossary assets.

    The legacy ``ManageAssetAttributes.handle_glossary_anchor`` uses
    ``isinstance`` against legacy Pydantic models, which doesn't recognise v9
    ``msgspec.Struct`` assets.  This helper performs the same check using the
    asset's ``type_name`` attribute so it works regardless of model layer.
    """
    if getattr(asset, "type_name", None) in _GLOSSARY_ASSET_TYPES:
        if not glossary_guid:
            raise ErrorCode.MISSING_GLOSSARY_GUID.exception_with_parameters(
                asset_type_name
            )
        asset.anchor = AtlasGlossary.ref_by_guid(glossary_guid)


def _matches_asset_type(asset, asset_type) -> bool:
    """Check if *asset* matches *asset_type*, supporting both legacy and v9 models."""
    return (
        isinstance(asset, asset_type)
        or getattr(asset, "type_name", None) == asset_type.__name__
    )


def _is_glossary_category(asset) -> bool:
    return (
        isinstance(asset, AtlasGlossaryCategory)
        or getattr(asset, "type_name", None) == "AtlasGlossaryCategory"
    )


def _process_search_results_v9(
    results, name: str, asset_type, allow_multiple: bool = False
):
    """v9-aware replacement for ``SearchForAssetWithName.process_search_results``."""
    if (
        results
        and results.count > 0
        and (
            assets := [
                asset
                for asset in (results.current_page() or results)
                if _matches_asset_type(asset, asset_type)
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


def _process_find_response_v9(
    search_results, name: str, asset_type, allow_multiple: bool = True
):
    """v9-aware replacement for ``FindAssetsByName.process_response``."""
    if (
        search_results
        and search_results.count > 0
        and (
            assets := [
                asset
                for asset in (search_results.current_page() or search_results)
                if _matches_asset_type(asset, asset_type)
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


def _process_hierarchy_v9(response, glossary) -> CategoryHierarchy:
    """v9-aware replacement for ``GetHierarchy.process_search_results``.

    Uses ``type_name`` attribute instead of ``isinstance`` to recognise
    v9 ``msgspec.Struct`` categories.
    """
    top_categories: set = set()
    category_dict = {}

    for category in filter(_is_glossary_category, response):
        guid = category.guid
        if not getattr(category, "children_categories", None):
            category.children_categories = None
        category_dict[guid] = category
        if not category.parent_category:
            top_categories.add(guid)

    if not top_categories:
        raise ErrorCode.NO_CATEGORIES.exception_with_parameters(
            glossary.guid, glossary.qualified_name
        )

    return CategoryHierarchy(top_level=top_categories, stub_dict=category_dict)


# ---------------------------------------------------------------------------
# v9-native response helpers (raw JSON -> v9 msgspec assets)
# ---------------------------------------------------------------------------


def _parse_entities_v9(entities: List[Dict], criteria=None) -> list:
    """Parse raw entity dicts into v9 msgspec assets.

    Applies custom-metadata unflattening (if *criteria* carries an
    ``attributes`` list) and then converts each entity dict via
    ``from_atlas_format``.
    """
    attributes = getattr(criteria, "attributes", None)
    for entity in entities:
        unflatten_custom_metadata_for_entity(entity=entity, attributes=attributes)
    return [from_atlas_format(e) for e in entities]


def _parse_mutation_response(raw_json: Dict) -> AssetMutationResponse:
    """Build a v9 ``AssetMutationResponse`` from raw API JSON.

    Entity lists are parsed directly into v9 msgspec asset types via
    ``from_atlas_format`` -- no Pydantic parsing involved.
    """
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


def _parse_aggregations_v9(raw: Dict) -> Optional[Aggregations]:
    """Convert raw aggregation JSON into a v9 ``Aggregations`` wrapper.

    Each entry is discriminated by its keys: ``buckets`` -> bucket result,
    ``hits`` -> hits result, ``value`` -> metric result.
    Nested aggregations inside buckets are recursively parsed.
    """
    from pyatlan_v9.model.aggregation import (
        AggregationBucketResult,
        AggregationHitsResult,
        AggregationMetricResult,
    )

    def _parse_nested(bucket_dict: dict) -> Optional[Aggregations]:
        """Parse nested aggregation results inside a bucket, recursively."""
        nested: Dict = {}
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
                    raw_inner_buckets = v.get("buckets", [])
                    for i, inner_bucket in enumerate(result.buckets):
                        if i < len(raw_inner_buckets):
                            try:
                                inner_bucket.nested_results = _parse_nested(
                                    raw_inner_buckets[i]
                                )
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

    parsed: Dict = {}
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
    return Aggregations(data=parsed) if parsed else None


def _process_search_response_v9(raw_json: Dict, criteria) -> Dict:
    """Process a search API response into v9 msgspec assets."""
    if "entities" in raw_json:
        assets = _parse_entities_v9(raw_json["entities"], criteria)
    else:
        assets = []

    aggregations = None
    if "aggregations" in raw_json:
        try:
            aggregations = _parse_aggregations_v9(raw_json["aggregations"])
        except Exception:
            pass

    approximate_count = raw_json.get("approximateCount", 0)
    return {
        "assets": assets,
        "aggregations": aggregations,
        "count": approximate_count,
    }


def _process_lineage_response_v9(raw_json: Dict, lineage_request) -> Dict:
    """Process a lineage list API response into v9 msgspec assets."""
    if "entities" in raw_json:
        assets = _parse_entities_v9(raw_json["entities"], lineage_request)
        has_more = bool(raw_json.get("hasMore", False))
    else:
        assets = []
        has_more = False
    return {"assets": assets, "has_more": has_more}


def _process_get_response_v9(
    raw_json: Dict, identifier: str, asset_type, *, by_guid: bool = False
) -> Any:
    """Process a get-by-guid or get-by-qualified-name API response.

    Merges relationship attributes into the entity dict, converts to a
    v9 msgspec asset via ``from_atlas_format``, and validates the result
    type.
    """
    import logging

    LOGGER = logging.getLogger(__name__)

    entity = raw_json["entity"]

    # DEBUG: Log what we received from API
    LOGGER.debug(f"Entity keys from API: {entity.keys()}")
    LOGGER.debug(f"Has meanings: {'meanings' in entity}")
    if "meanings" in entity:
        LOGGER.debug(f"Meanings value: {entity['meanings']}")

    if not by_guid and entity.get("typeName") != asset_type.__name__:
        raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
            asset_type.__name__, identifier
        )

    if entity.get("relationshipAttributes"):
        entity.setdefault("attributes", {}).update(entity["relationshipAttributes"])
    entity["relationshipAttributes"] = {}

    asset = from_atlas_format(entity)
    asset.is_incomplete = False

    # DEBUG: Log what we got after deserialization
    LOGGER.debug(
        f"After deserialization, meanings: {asset.meanings if hasattr(asset, 'meanings') else 'NO ATTR'}"
    )
    LOGGER.debug(
        f"After deserialization, assigned_terms: {asset.assigned_terms if hasattr(asset, 'assigned_terms') else 'NO ATTR'}"
    )

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


# ---------------------------------------------------------------------------
# V9-native search result subclasses (override entity parsing for pagination)
# ---------------------------------------------------------------------------


class V9IndexSearchResults(IndexSearchResults):
    """IndexSearchResults that deserializes pages into v9 msgspec assets."""

    def _process_entities(self, entities):
        self._assets = _parse_entities_v9(entities, self._criteria)


class V9LineageListResults(LineageListResults):
    """LineageListResults that deserializes pages into v9 msgspec assets."""

    def _process_entities(self, entities):
        self._assets = _parse_entities_v9(entities, self._criteria)


def _make_bulk_request_payload(entities: List[Asset], client: "AtlanClient") -> dict:
    """
    Serialize a list of Asset entities into an API-ready dict,
    applying AtlanTag retranslation (human names -> internal IDs).
    """
    bulk = BulkRequest(entities=entities)
    request_dict = bulk.to_dict()
    for entity in request_dict.get("entities", []):
        _normalize_meanings_for_mutation(entity)
    retranslated = AtlanRequest(instance=request_dict, client=client)
    return retranslated.translated


def _make_asset_request_payload(asset: Asset, client: "AtlanClient") -> dict:
    """
    Serialize a single Asset entity into an API-ready dict,
    applying AtlanTag retranslation.
    """
    asset_dict = {"entity": json.loads(asset.to_json(nested=True))}
    _normalize_meanings_for_mutation(asset_dict["entity"])
    retranslated = AtlanRequest(instance=asset_dict, client=client)
    return retranslated.translated


def _normalize_meanings_for_mutation(entity: dict[str, Any]) -> None:
    """
    Normalize term assignment payloads for mutation APIs.

    Legacy API payloads send term links under `attributes.meanings`.
    v9 nested serialization exposes `meanings` as a top-level field, so
    move it into attributes before submission to preserve parity.
    """
    if "meanings" not in entity:
        return
    meanings = entity.pop("meanings")
    if not isinstance(meanings, list):
        meanings = [meanings]

    replace_meanings: list[dict[str, Any]] = []
    append_meanings: list[dict[str, Any]] = []
    remove_meanings: list[dict[str, Any]] = []

    for meaning in meanings:
        if not isinstance(meaning, dict):
            replace_meanings.append(meaning)
            continue
        semantic = meaning.get("semantic")
        normalized = {k: v for k, v in meaning.items() if k != "semantic"}
        if semantic == "APPEND":
            append_meanings.append(normalized)
        elif semantic == "REMOVE":
            remove_meanings.append(normalized)
        else:
            replace_meanings.append(normalized)

    if append_meanings:
        append_rels = entity.get("appendRelationshipAttributes")
        if not isinstance(append_rels, dict):
            append_rels = {}
        append_rels["meanings"] = append_meanings
        entity["appendRelationshipAttributes"] = append_rels

    if remove_meanings:
        remove_rels = entity.get("removeRelationshipAttributes")
        if not isinstance(remove_rels, dict):
            remove_rels = {}
        remove_rels["meanings"] = remove_meanings
        entity["removeRelationshipAttributes"] = remove_rels

    if replace_meanings or (not append_meanings and not remove_meanings):
        attrs = entity.get("attributes")
        if not isinstance(attrs, dict):
            attrs = {}
        attrs["meanings"] = replace_meanings
        entity["attributes"] = attrs


# ---------------------------------------------------------------------------
# V9 Asset Client
# ---------------------------------------------------------------------------


class V9AssetClient:
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

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

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
        response = _process_search_response_v9(raw_json, criteria)
        if Search._check_for_bulk_search(criteria, response["count"], bulk):
            return self.search(criteria)
        return V9IndexSearchResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=response["count"],
            assets=response["assets"],
            aggregations=response["aggregations"],
            bulk=bulk,
        )

    # ------------------------------------------------------------------
    # Lineage
    # ------------------------------------------------------------------

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
        response = _process_lineage_response_v9(raw_json, lineage_request)
        return V9LineageListResults(
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
        search_request = self._build_find_request(name, "PERSONA", attributes)
        search_results = self.search(search_request)
        return _process_find_response_v9(
            search_results, name, Persona, allow_multiple=True
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
        search_request = self._build_find_request(name, "PURPOSE", attributes)
        search_results = self.search(search_request)
        return _process_find_response_v9(
            search_results, name, Purpose, allow_multiple=True
        )

    # ------------------------------------------------------------------
    # Get by qualified name / GUID
    # ------------------------------------------------------------------

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
            results = self.search(search.to_request())
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
        raw_json = self._client._call_api(endpoint_path, query_params)
        return _process_get_response_v9(
            raw_json, qualified_name, asset_type, by_guid=False
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
            results = self.search(search.to_request())
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
        raw_json = self._client._call_api(endpoint_path, query_params)
        return _process_get_response_v9(raw_json, guid, asset_type, by_guid=True)

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

    # ------------------------------------------------------------------
    # Save / Upsert
    # ------------------------------------------------------------------

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
            asset.flush_custom_metadata(client=self._client)

        request_payload = _make_bulk_request_payload(entities, self._client)
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request_payload)
        response = _parse_mutation_response(raw_json)

        if connections_created := response.assets_created(Connection):
            self._wait_for_connections_to_be_created(connections_created)
        return response

    def _wait_for_connections_to_be_created(self, connections_created):
        guids = []
        LOGGER.debug("Waiting for connections")
        for connection in connections_created:
            LOGGER.debug(
                "Attempting to retrieve connection with guid: %s", connection.guid
            )
            guids.append(connection.guid)

        @retry(
            retry=retry_if_exception_type(PermissionError),
            wait=wait_exponential(multiplier=1, min=1, max=8),
            stop=stop_after_attempt(10),
            reraise=True,
        )
        def _retrieve_connection_with_retry(guid):
            self.retrieve_minimal(guid=guid, asset_type=Connection)

        for guid in guids:
            _retrieve_connection_with_retry(guid)

        LOGGER.debug("Finished waiting for connections")

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
            asset.flush_custom_metadata(client=self._client)

        request_payload = _make_bulk_request_payload(entities, self._client)
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request_payload)
        return _parse_mutation_response(raw_json)

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

    # ------------------------------------------------------------------
    # Delete / Purge / Restore
    # ------------------------------------------------------------------

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
        return _parse_mutation_response(raw_json)

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

        assets = []
        for single_guid in guids:
            asset = self.retrieve_minimal(guid=single_guid, asset_type=Asset)
            assets.append(asset)
        DeleteByGuid.validate_assets_can_be_archived(assets)

        query_params = DeleteByGuid.prepare_delete_request(guids)
        raw_json = self._client._call_api(
            DELETE_ENTITIES_BY_GUIDS, query_params=query_params
        )
        response = _parse_mutation_response(raw_json)

        for asset in response.assets_deleted(asset_type=Asset):
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
            return False
        elif RestoreAsset.is_asset_active(existing):
            if retries < 10:
                time.sleep(2)
                return self._restore(asset_type, qualified_name, retries + 1)
            else:
                return True
        else:
            response = self._restore_asset(existing)
            return RestoreAsset.is_restore_successful(response)

    def _restore_asset(self, asset: Asset) -> AssetMutationResponse:
        to_restore = asset.trim_to_required()
        to_restore.status = EntityStatus.ACTIVE

        query_params = {
            "replaceClassifications": False,
            "replaceBusinessAttributes": False,
            "overwriteBusinessAttributes": False,
        }

        entities = [to_restore]
        for restored in entities:
            restored.flush_custom_metadata(self._client)

        request_payload = _make_bulk_request_payload(entities, self._client)
        raw_json = self._client._call_api(BULK_UPDATE, query_params, request_payload)
        return _parse_mutation_response(raw_json)

    # ------------------------------------------------------------------
    # Atlan Tags
    # ------------------------------------------------------------------

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
        if save_parameters is None:
            save_parameters = {}

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
                attributes=["anchor"],
            )

        retrieved_asset = _get_asset_with_retry()

        # Prepare the asset updater using the v9 model directly
        from pyatlan_v9.model.assets import AtlasGlossaryCategory, AtlasGlossaryTerm

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

        # Create v9 msgspec AtlanTag objects directly
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

        # Apply the modification to the v9 entity
        if modification_type in ("add", "update"):
            updated_asset.add_or_update_classifications = tags
        elif modification_type == "remove":
            updated_asset.remove_classifications = tags
        elif modification_type == "replace":
            updated_asset.classifications = tags

        response = self.save(entity=updated_asset, **save_parameters)
        if assets := response.assets_updated(asset_type=asset_type):
            return assets[0]
        return updated_asset

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

    # ------------------------------------------------------------------
    # Update asset by attribute (certificate, announcement, etc.)
    # ------------------------------------------------------------------

    def _update_asset_by_attribute(
        self, asset: A, asset_type: Type[A], qualified_name: str
    ) -> Optional[A]:
        query_params = UpdateAssetByAttribute.prepare_request_params(qualified_name)
        asset.flush_custom_metadata(client=self._client)
        endpoint = UpdateAssetByAttribute.get_api_endpoint(asset_type)
        request_payload = _make_asset_request_payload(asset, self._client)
        raw_json = self._client._call_api(endpoint, query_params, request_payload)
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
        asset = UpdateCertificate.prepare_asset_with_certificate(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            certificate_status=certificate_status,
            message=message,
            glossary_guid=glossary_guid,
        )
        _handle_v9_glossary_anchor(asset, asset_type.__name__, glossary_guid)
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
        asset = RemoveCertificate.prepare_asset_for_certificate_removal(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            glossary_guid=glossary_guid,
        )
        _handle_v9_glossary_anchor(asset, asset_type.__name__, glossary_guid)
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    # ------------------------------------------------------------------
    # Announcements
    # ------------------------------------------------------------------

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

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
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
        asset = UpdateAnnouncement.prepare_asset_with_announcement(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            announcement=announcement,
            glossary_guid=glossary_guid,
        )
        _handle_v9_glossary_anchor(asset, asset_type.__name__, glossary_guid)
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
        asset = RemoveAnnouncement.prepare_asset_for_announcement_removal(
            asset_type=asset_type,
            qualified_name=qualified_name,
            name=name,
            glossary_guid=glossary_guid,
        )
        _handle_v9_glossary_anchor(asset, asset_type.__name__, glossary_guid)
        return self._update_asset_by_attribute(asset, asset_type, qualified_name)

    # ------------------------------------------------------------------
    # Custom metadata
    # ------------------------------------------------------------------

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
        custom_metadata_request = UpdateCustomMetadataAttributes.prepare_request(
            custom_metadata
        )
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )
        payload = _custom_metadata_payload(custom_metadata_request)
        self._client._call_api(endpoint, None, payload)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def replace_custom_metadata(self, guid: str, custom_metadata: CustomMetadataDict):
        """
        Replace specific custom metadata on the asset. This will replace everything within the named
        custom metadata, but will not change any of hte other named custom metadata on the asset.

        :param guid: unique identifier (GUID) of the asset
        :param custom_metadata: custom metadata to replace, as human-readable names mapped to values
        :raises AtlanError: on any API communication issue
        """
        custom_metadata_request = ReplaceCustomMetadata.prepare_request(custom_metadata)
        endpoint = ManageCustomMetadata.get_api_endpoint(
            guid, custom_metadata_request.custom_metadata_set_id
        )
        payload = _custom_metadata_payload(custom_metadata_request)
        self._client._call_api(endpoint, None, payload)

    @validate_arguments
    def remove_custom_metadata(self, guid: str, cm_name: str):
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
        self._client._call_api(endpoint, None, payload)

    # ------------------------------------------------------------------
    # Terms management
    # ------------------------------------------------------------------

    def _search_for_asset_with_name(
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
        results = self.search(search_request)
        return _process_search_results_v9(results, name, asset_type, allow_multiple)

    def _manage_terms(
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

        results = search_query.execute(client=self._client)
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
                        qualified_name=term.qualified_name, semantic=save_semantic
                    )
                )
        updated_asset.assigned_terms = processed_terms
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

    # ------------------------------------------------------------------
    # Find by name
    # ------------------------------------------------------------------

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
        query = FindConnectionsByName.build_query(name, connector_type)
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
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossary, attributes=attributes
        )[0]

    @validate_arguments
    def find_category_fast_by_name(
        self,
        name: str,
        glossary_qualified_name: str,
        attributes: Optional[List[str]] = None,
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
        query = FindCategoryFastByName.build_query(name, glossary_qualified_name)
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
        name: str,
        glossary_name: str,
        attributes: Optional[List[str]] = None,
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

    @validate_arguments
    def find_term_fast_by_name(
        self,
        name: str,
        glossary_qualified_name: str,
        attributes: Optional[List[str]] = None,
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
        query = FindTermFastByName.build_query(name, glossary_qualified_name)
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=AtlasGlossaryTerm, attributes=attributes
        )[0]

    @validate_arguments
    def find_term_by_name(
        self,
        name: str,
        glossary_name: str,
        attributes: Optional[List[str]] = None,
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
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=DataDomain, attributes=attributes
        )[0]

    @validate_arguments
    def find_product_by_name(
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
        return self._search_for_asset_with_name(
            query=query, name=name, asset_type=DataProduct, attributes=attributes
        )[0]

    # ------------------------------------------------------------------
    # Hierarchy
    # ------------------------------------------------------------------

    def get_hierarchy(
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
        response = self.search(request)
        return _process_hierarchy_v9(response, glossary)

    # ------------------------------------------------------------------
    # Bulk processing
    # ------------------------------------------------------------------

    def process_assets(
        self,
        search,
        func: Callable[[Asset], None],
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

    # ------------------------------------------------------------------
    # DQ helpers
    # ------------------------------------------------------------------

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
        return self.save(updated_asset)

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
        return self.save(updated_asset)


# ---------------------------------------------------------------------------
# V9-aware Batch (bypasses Pydantic's _convert_to_real_type_ validator and
# recognises v9 msgspec glossary terms in the tracking logic)
# ---------------------------------------------------------------------------


class Batch(_LegacyBatch):
    """V9 wrapper around the legacy ``Batch`` class.

    Overrides ``add()`` to accept v9 ``msgspec.Struct`` assets without
    going through Pydantic's ``_convert_to_real_type_`` validator, and
    overrides the tracking helper so v9 ``AtlasGlossaryTerm`` instances
    are handled correctly.
    """

    def add(self, single) -> Optional[AssetMutationResponse]:
        self._batch.append(single)
        return self._process()

    @staticmethod
    def __track(tracker, candidate):
        if (
            isinstance(candidate, AtlasGlossaryTerm)
            or getattr(candidate, "type_name", None) == "AtlasGlossaryTerm"
        ):
            asset = cast(Asset, type(candidate).ref_by_guid(candidate.guid))
        else:
            asset = candidate.trim_to_required()
        asset.name = candidate.name
        tracker.append(asset)
