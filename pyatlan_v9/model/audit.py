# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import json as json_lib
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Generator, Iterable, List, Optional, Set, Union

import msgspec

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.client.protocol import ApiCaller
from pyatlan.errors import ErrorCode, NotFoundError
from pyatlan.model.constants import DELETED_
from pyatlan.model.enums import SortOrder
from pyatlan_v9.model.aggregation import Aggregation
from pyatlan_v9.model.search import DSL, Bool, Query, Range, SortItem, Term

TOTAL_COUNT = "totalCount"

ENTITY_AUDITS = "entityAudits"

ATTRIBUTES = "attributes"

TYPE_NAME = "type_name"

LATEST_FIRST = [SortItem("created", order=SortOrder.DESCENDING)]


class AuditActionType(str, Enum):
    ENTITY_CREATE = "ENTITY_CREATE"
    ENTITY_UPDATE = "ENTITY_UPDATE"
    ENTITY_DELETE = "ENTITY_DELETE"
    CUSTOM_METADATA_UPDATE = "BUSINESS_ATTRIBUTE_UPDATE"
    ATLAN_TAG_ADD = "CLASSIFICATION_ADD"
    PROPAGATED_ATLAN_TAG_ADD = "PROPAGATED_CLASSIFICATION_ADD"
    ATLAN_TAG_DELETE = "CLASSIFICATION_DELETE"
    PROPAGATED_ATLAN_TAG_DELETE = "PROPAGATED_CLASSIFICATION_DELETE"
    ENTITY_IMPORT_CREATE = "ENTITY_IMPORT_CREATE"
    ENTITY_IMPORT_UPDATE = "ENTITY_IMPORT_UPDATE"
    ENTITY_IMPORT_DELETE = "ENTITY_IMPORT_DELETE"
    ATLAN_TAG_UPDATE = "CLASSIFICATION_UPDATE"
    PROPAGATED_ATLAN_TAG_UPDATE = "PROPAGATED_CLASSIFICATION_UPDATE"
    TERM_ADD = "TERM_ADD"
    TERM_DELETE = "TERM_DELETE"


class AuditSearchRequest(msgspec.Struct, kw_only=True):
    """Class from which to configure a search against Atlan's activity log."""

    dsl: DSL
    attributes: List[str] = msgspec.field(default_factory=list)

    def __post_init__(self):
        class_name = self.__class__.__name__
        if self.dsl and isinstance(self.dsl, DSL) and not self.dsl.req_class_name:
            self.dsl = DSL(
                req_class_name=class_name,
                from_=self.dsl.from_,
                size=self.dsl.size,
                aggregations=self.dsl.aggregations,
                track_total_hits=self.dsl.track_total_hits,
                post_filter=self.dsl.post_filter,
                query=self.dsl.query,
                sort=self.dsl.sort,
            )

    def json(
        self,
        by_alias: bool = False,
        exclude_none: bool = False,
        exclude_unset: bool = False,
    ) -> str:
        """Serialize AuditSearchRequest to JSON string."""
        d: Dict[str, Any] = {
            "attributes": self.attributes,
            "dsl": json_lib.loads(
                self.dsl.json(by_alias=by_alias, exclude_none=exclude_none)
            ),
        }
        if exclude_none:
            d = {k: v for k, v in d.items() if v is not None}
        return json_lib.dumps(d)

    @classmethod
    def by_guid(
        cls,
        guid: str,
        *,
        size: int = 10,
        _from: int = 0,
        sort: Union[SortItem, List[SortItem]] = LATEST_FIRST,
    ) -> "AuditSearchRequest":
        """
        Create an audit search request for the last changes to an asset, by its GUID.
        :param guid: unique identifier of the asset for which to retrieve the audit history
        :param size: number of changes to retrieve
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden
        :param sort: sorting criteria for the results. Defaults to LATEST_FIRST(sorting by "created" in desc order).
        :returns: an AuditSearchRequest that can be used to perform the search
        """
        dsl = DSL(
            query=Bool(filter=[Term(field="entityId", value=guid)]),
            sort=sort if LATEST_FIRST else [],
            size=size,
            from_=_from,
        )
        return AuditSearchRequest(dsl=dsl)

    @classmethod
    def by_user(
        cls,
        user: str,
        *,
        size: int = 10,
        _from: int = 0,
        sort: Union[SortItem, List[SortItem]] = LATEST_FIRST,
    ) -> "AuditSearchRequest":
        """
        Create an audit search request for the last changes to an asset, by a given user.
        :param user: the name of the user for which to look for any changes
        :param size: number of changes to retrieve
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden
        :param sort: sorting criteria for the results. Defaults to LATEST_FIRST(sorting by "created" in desc order).
        :returns: an AuditSearchRequest that can be used to perform the search
        """
        dsl = DSL(
            query=Bool(filter=[Term(field="user", value=user)]),
            sort=sort if LATEST_FIRST else [],
            size=size,
            from_=_from,
        )
        return AuditSearchRequest(dsl=dsl)

    @classmethod
    def by_qualified_name(
        cls,
        type_name: str,
        qualified_name: str,
        *,
        size: int = 10,
        _from: int = 0,
        sort: Union[SortItem, List[SortItem]] = LATEST_FIRST,
    ) -> "AuditSearchRequest":
        """
        Create an audit search request for the last changes to an asset, by its qualifiedName.
        :param type_name: the type of asset for which to retrieve the audit history
        :param qualified_name: unique name of the asset for which to retrieve the audit history
        :param size: number of changes to retrieve
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden
        :param sort: sorting criteria for the results. Defaults to LATEST_FIRST(sorting by "created" in desc order).
        :returns: an AuditSearchRequest that can be used to perform the search
        """
        dsl = DSL(
            query=Bool(
                must=[
                    Term(field="entityQualifiedName", value=qualified_name),
                    Term(field="typeName", value=type_name),
                ]
            ),
            sort=sort if LATEST_FIRST else [],
            size=size,
            from_=_from,
        )
        return AuditSearchRequest(dsl=dsl)


class CustomMetadataAttributesAuditDetail(msgspec.Struct, kw_only=True):
    """Capture the attributes and values for custom metadata as tracked through the audit log."""

    type_name: str
    attributes: Dict[str, Any] = msgspec.field(default_factory=dict)
    archived_attributes: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        cm_id = self.type_name
        try:
            self.type_name = CustomMetadataCache.get_name_for_id(self.type_name)
            attributes = {
                CustomMetadataCache.get_attr_name_for_id(cm_id, attr_id): properties
                for attr_id, properties in self.attributes.items()
            }
            archived_attributes = {
                key: value for key, value in attributes.items() if "-archived-" in key
            }
            for key in archived_attributes:
                del attributes[key]
            self.attributes = attributes
            self.archived_attributes = archived_attributes
        except NotFoundError:
            self.type_name = DELETED_
            self.attributes = {}

    @property
    def empty(self) -> bool:
        return not self.attributes or len(self.attributes) == 0


class EntityAudit(msgspec.Struct, kw_only=True):
    """
    Detailed entry in the audit log. These objects should be treated as immutable.
    """

    entity_qualified_name: str
    type_name: str
    entity_id: str
    timestamp: datetime
    created: datetime
    user: str
    action: AuditActionType
    details: Optional[Any] = None
    event_key: str = ""
    entity: Optional[Any] = None
    type: Optional[Any] = None
    detail: Optional[Any] = None
    entity_detail: Optional[Any] = None
    headers: Optional[Dict[str, str]] = None


class AuditSearchResults(Iterable):
    """
    Captures the response from a search against Atlan's activity log.
    """

    _DEFAULT_SIZE = 300
    _MASS_EXTRACT_THRESHOLD = 10000 - _DEFAULT_SIZE

    def __init__(
        self,
        client: ApiCaller,
        criteria: AuditSearchRequest,
        start: int,
        size: int,
        entity_audits: List[EntityAudit],
        count: int,
        bulk: bool = False,
        aggregations: Optional[Aggregation] = None,
    ):
        self._client = client
        self._endpoint = AUDIT_SEARCH
        self._criteria = criteria
        self._start = start
        self._size = size
        self._entity_audits = entity_audits
        self._count = count
        self._approximate_count = count
        self._bulk = bulk
        self._aggregations = aggregations
        self._first_record_creation_time = -2
        self._last_record_creation_time = -2
        self._processed_entity_keys: Set[str] = set()

    @property
    def aggregations(self) -> Optional[Aggregation]:
        return self._aggregations

    @property
    def total_count(self) -> int:
        return self._count

    def current_page(self) -> List[EntityAudit]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._entity_audits

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
            self._processed_entity_keys.update(
                entity.event_key for entity in self._entity_audits
            )
        return self._get_next_page() if self._entity_audits else False

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

        if raw_json := self._get_next_page_json(is_bulk_search):
            self._count = raw_json.get(TOTAL_COUNT, 0)
            return True
        return False

    def _get_next_page_json(self, is_bulk_search: bool = False):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if ENTITY_AUDITS not in raw_json or not raw_json[ENTITY_AUDITS]:
            self._entity_audits = []
            return None

        try:
            self._entity_audits = [
                msgspec.convert(audit, EntityAudit) for audit in raw_json[ENTITY_AUDITS]
            ]
            if is_bulk_search:
                self._filter_processed_entities()
                self._update_first_last_record_creation_times()
            return raw_json
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def _prepare_query_for_timestamp_paging(self, query: Query):
        """
        Adjusts the query to include timestamp filters for audit bulk extraction.
        """
        rewritten_filters = []
        if isinstance(query, Bool):
            for filter_ in query.filter:
                if self._is_paging_timestamp_query(filter_):
                    continue
                rewritten_filters.append(filter_)

        if self._first_record_creation_time != self._last_record_creation_time:
            rewritten_filters.append(
                self._get_paging_timestamp_query(self._last_record_creation_time)
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
                rewritten_filters.append(query)
                rewritten_query = Bool(filter=rewritten_filters)
            self._criteria.dsl.from_ = 0
            self._criteria.dsl.query = rewritten_query
        else:
            if isinstance(query, Bool):
                for filter_ in query.filter:
                    if self._is_paging_timestamp_query(filter_):
                        query.filter.remove(filter_)
            self._criteria.dsl.from_ = len(self._processed_entity_keys)

    @staticmethod
    def _get_paging_timestamp_query(last_timestamp: int) -> Query:
        return Range(field="created", gte=last_timestamp)

    @staticmethod
    def _is_paging_timestamp_query(filter_: Query) -> bool:
        return (
            isinstance(filter_, Range)
            and filter_.field == "created"
            and filter_.gte is not None
        )

    def _update_first_last_record_creation_times(self):
        self._first_record_creation_time = self._last_record_creation_time = -2

        if not isinstance(self._entity_audits, list) or len(self._entity_audits) <= 1:
            return

        first_audit, last_audit = self._entity_audits[0], self._entity_audits[-1]

        if first_audit:
            self._first_record_creation_time = first_audit.created

        if last_audit:
            self._last_record_creation_time = last_audit.created

    def _filter_processed_entities(self):
        """
        Remove entities that have already been processed to avoid duplicates.
        """
        self._entity_audits = [
            entity
            for entity in self._entity_audits
            if entity is not None
            and entity.event_key not in self._processed_entity_keys
        ]

    @staticmethod
    def presorted_by_timestamp(sorts: Optional[List[SortItem]]) -> bool:
        """
        Checks if the sorting options prioritize creation time in ascending order.
        :param sorts: list of sorting options or None.
        :returns: True if sorting is already prioritized by creation time, False otherwise.
        """
        if sorts and isinstance(sorts[0], SortItem):
            return sorts[0].field == "created" and sorts[0].order == SortOrder.ASCENDING
        return False

    @staticmethod
    def sort_by_timestamp_first(sorts: List[SortItem]) -> List[SortItem]:
        """
        Rewrites the sorting options to ensure that
        sorting by creation time, ascending, is the top
        priority.

        :param sorts: list of sorting options
        :returns: sorting options, making sorting by
        creation time in ascending order the top priority
        """
        creation_asc_sort = [SortItem("created", order=SortOrder.ASCENDING)]

        if not sorts:
            return creation_asc_sort

        rewritten_sorts = [
            sort for sort in sorts if (not sort.field) or (sort.field != "__timestamp")
        ]
        return creation_asc_sort + rewritten_sorts

    def __iter__(self) -> Generator[EntityAudit, None, None]:
        """
        Iterates through the results, lazily-fetching each next page until there
        are no more results.

        returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.next_page():
                break
