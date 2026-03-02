# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, AsyncGenerator, List, Optional, Set

import msgspec

from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import SortOrder
from pyatlan_v9.model.audit import AuditSearchRequest, EntityAudit
from pyatlan_v9.model.search import Bool, Query, Range, SortItem

TOTAL_COUNT = "totalCount"
ENTITY_AUDITS = "entityAudits"


class AsyncAuditSearchResults:
    """Async version of AuditSearchResults for paginated audit search."""

    _DEFAULT_SIZE = 300
    _MASS_EXTRACT_THRESHOLD = 10000 - _DEFAULT_SIZE

    def __init__(
        self,
        client: Any,
        criteria: AuditSearchRequest,
        start: int,
        size: int,
        entity_audits: List[EntityAudit],
        count: int,
        bulk: bool = False,
        aggregations: Optional[Any] = None,
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
    def aggregations(self) -> Optional[Any]:
        return self._aggregations

    @property
    def total_count(self) -> int:
        return self._count

    def current_page(self) -> List[EntityAudit]:
        """Retrieve the current page of results."""
        return self._entity_audits

    async def next_page(self, start=None, size=None) -> bool:
        """Indicates whether there is a next page of results."""
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
        return await self._get_next_page() if self._entity_audits else False

    async def _get_next_page(self):
        query = self._criteria.dsl.query
        self._criteria.dsl.size = self._size
        self._criteria.dsl.from_ = self._start
        is_bulk_search = (
            self._bulk or self._approximate_count > self._MASS_EXTRACT_THRESHOLD
        )
        if is_bulk_search:
            self._prepare_query_for_timestamp_paging(query)
        if raw_json := await self._get_next_page_json(is_bulk_search):
            self._count = raw_json.get(TOTAL_COUNT, 0)
            return True
        return False

    async def _get_next_page_json(self, is_bulk_search: bool = False):
        raw_json = await self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if ENTITY_AUDITS not in raw_json or not raw_json[ENTITY_AUDITS]:
            self._entity_audits = []
            return None
        try:
            from pyatlan_v9.client.audit import _normalize_ms_timestamps, _AUDIT_TS_FIELDS

            self._entity_audits = [
                msgspec.convert(
                    _normalize_ms_timestamps(audit, _AUDIT_TS_FIELDS),
                    EntityAudit,
                    strict=False,
                )
                for audit in raw_json[ENTITY_AUDITS]
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
        self._entity_audits = [
            entity
            for entity in self._entity_audits
            if entity is not None
            and entity.event_key not in self._processed_entity_keys
        ]

    @staticmethod
    def presorted_by_timestamp(sorts) -> bool:
        if sorts and isinstance(sorts[0], SortItem):
            return sorts[0].field == "created" and sorts[0].order == SortOrder.ASCENDING
        return False

    @staticmethod
    def sort_by_timestamp_first(sorts) -> List[SortItem]:
        creation_asc_sort = [SortItem("created", order=SortOrder.ASCENDING)]
        if not sorts:
            return creation_asc_sort
        rewritten_sorts = [
            sort for sort in sorts if (not sort.field) or (sort.field != "__timestamp")
        ]
        return creation_asc_sort + rewritten_sorts

    async def __aiter__(self) -> AsyncGenerator[EntityAudit, None]:
        """Iterate through all pages of results."""
        while True:
            for audit in self.current_page():
                yield audit
            if not await self.next_page():
                break
