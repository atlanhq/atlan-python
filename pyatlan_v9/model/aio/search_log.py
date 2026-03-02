# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, AsyncGenerator, Dict, List, Optional

import msgspec

from pyatlan.client.constants import SEARCH_LOG
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import SortOrder
from pyatlan_v9.model.search import Bool, Query, Range, SortItem
from pyatlan_v9.model.search_log import SearchLogEntry, SearchLogRequest


class AsyncSearchLogResults:
    """Async version of SearchLogResults for paginated search log results."""

    _DEFAULT_SIZE = 300
    _MASS_EXTRACT_THRESHOLD = 10000 - _DEFAULT_SIZE

    def __init__(
        self,
        client: Any,
        criteria: SearchLogRequest,
        start: int,
        size: int,
        count: int,
        log_entries: List[SearchLogEntry],
        aggregations: Dict,
        bulk: bool = False,
        processed_log_entries_count: int = 0,
    ):
        self._client = client
        self._endpoint = SEARCH_LOG
        self._criteria = criteria
        self._start = start
        self._size = size
        self._log_entries = log_entries
        self._count = count
        self._approximate_count = count
        self._aggregations = aggregations
        self._bulk = bulk
        self._first_record_creation_time = -2
        self._last_record_creation_time = -2
        self._duplicate_timestamp_page_count: int = 0
        self._processed_log_entries_count: int = processed_log_entries_count

    @property
    def count(self) -> int:
        return self._count

    def current_page(self) -> List[SearchLogEntry]:
        """Retrieve the current page of results."""
        return self._log_entries

    async def next_page(self, start=None, size=None) -> bool:
        """Indicates whether there is a next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._log_entries else False

    async def _get_next_page(self):
        query = self._criteria.dsl.query
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        is_bulk_search = (
            self._bulk or self._approximate_count > self._MASS_EXTRACT_THRESHOLD
        )
        if is_bulk_search:
            self._prepare_query_for_timestamp_paging(query)
        if raw_json := await self._get_next_page_json(is_bulk_search):
            self._count = raw_json.get("approximateCount", 0)
            return True
        return False

    async def _get_next_page_json(self, is_bulk_search: bool = False):
        raw_json = await self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "logs" not in raw_json or not raw_json["logs"]:
            self._log_entries = []
            return None
        try:
            from pyatlan_v9.client.search_log import (
                _normalize_ms_timestamps_copy,
                _LOG_TS_FIELDS,
            )

            self._log_entries = [
                msgspec.convert(
                    _normalize_ms_timestamps_copy(entry, _LOG_TS_FIELDS),
                    SearchLogEntry,
                    strict=False,
                )
                for entry in raw_json["logs"]
            ]
            self._processed_log_entries_count += len(self._log_entries)
            if is_bulk_search:
                self._update_first_last_record_creation_times()
            return raw_json
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def _prepare_query_for_timestamp_paging(self, query: Query):
        self._criteria.dsl.from_ = 0
        rewritten_filters = []
        if isinstance(query, Bool):
            for filter_ in query.filter:
                if self._is_paging_timestamp_query(filter_):
                    continue
                rewritten_filters.append(filter_)

        if self._first_record_creation_time != self._last_record_creation_time:
            self._duplicate_timestamp_page_count = 0
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
            self._criteria.dsl.query = rewritten_query
        else:
            self._criteria.dsl.from_ = self._size * (
                self._duplicate_timestamp_page_count + 1
            )
            self._criteria.dsl.size = self._size
            self._duplicate_timestamp_page_count += 1

    @staticmethod
    def _get_paging_timestamp_query(last_timestamp: int) -> Query:
        return Range(field="createdAt", gt=last_timestamp)

    @staticmethod
    def _is_paging_timestamp_query(filter_: Query) -> bool:
        return (
            isinstance(filter_, Range)
            and filter_.field == "createdAt"
            and filter_.gt is not None
        )

    def _update_first_last_record_creation_times(self):
        self._first_record_creation_time = self._last_record_creation_time = -2
        if not isinstance(self._log_entries, list) or len(self._log_entries) <= 1:
            return
        first_entry, last_entry = self._log_entries[0], self._log_entries[-1]
        if first_entry:
            self._first_record_creation_time = first_entry.created_at
        if last_entry:
            self._last_record_creation_time = last_entry.created_at

    @staticmethod
    def presorted_by_timestamp(sorts: Optional[list]) -> bool:
        if sorts and isinstance(sorts[0], SortItem):
            return (
                sorts[0].field == "createdAt"
                and sorts[0].order == SortOrder.ASCENDING
            )
        return False

    @staticmethod
    def sort_by_timestamp_first(sorts: Optional[list]) -> List[SortItem]:
        from pyatlan_v9.model.search_log import BY_TIMESTAMP

        creation_asc_sort = [SortItem("createdAt", order=SortOrder.ASCENDING)]
        if not sorts:
            return creation_asc_sort
        rewritten_sorts = [
            sort
            for sort in sorts
            if ((not sort.field) or (sort.field != "__timestamp"))
            and (sort not in BY_TIMESTAMP)
        ]
        return creation_asc_sort + rewritten_sorts

    async def __aiter__(self) -> AsyncGenerator[SearchLogEntry, None]:
        """Iterate through all pages of results."""
        while True:
            for entry in self.current_page():
                yield entry
            if not await self.next_page():
                break
