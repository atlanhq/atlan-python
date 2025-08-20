# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Dict, List, Optional

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import SEARCH_LOG
from pyatlan.errors import ErrorCode
from pyatlan.model.search import DSL, Bool, Query, Range, SortItem
from pyatlan.model.search_log import SearchLogEntry, SearchLogRequest

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient

LOGS = "logs"
APPROXIMATE_COUNT = "approximateCount"


class AsyncSearchLogResults:
    """
    Async version of SearchLogResults that captures the response from a search against Atlan's search log.
    Also provides the ability to iteratively page through results using async/await,
    without needing to track or re-run the original query.
    """

    _DEFAULT_SIZE = DSL.__fields__.get("size").default or 300  # type: ignore[union-attr]
    _MASS_EXTRACT_THRESHOLD = 10000 - _DEFAULT_SIZE

    def __init__(
        self,
        client: AsyncAtlanClient,
        criteria: SearchLogRequest,
        start: int,
        size: int,
        log_entries: List[SearchLogEntry],
        count: int,
        bulk: bool = False,
        aggregations: Optional[Dict] = None,
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
        self._bulk = bulk
        self._aggregations = aggregations or {}
        self._processed_log_entries_count = processed_log_entries_count
        self._first_record_creation_time = -2
        self._last_record_creation_time = -2
        self._duplicate_timestamp_page_count: int = 0

    @property
    def aggregations(self) -> Dict:
        return self._aggregations

    @property
    def count(self) -> int:
        return self._count

    @property
    def total_count(self) -> int:
        return self._count

    def current_page(self) -> List[SearchLogEntry]:
        """
        Retrieve the current page of results.

        :returns: list of search log entries on the current page of results
        """
        return self._log_entries

    async def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results and fetches it.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._log_entries else False

    async def _get_next_page(self):
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

        if raw_json := await self._get_next_page_json(is_bulk_search):
            self._count = raw_json.get(APPROXIMATE_COUNT, 0)
            return True
        return False

    async def _get_next_page_json(self, is_bulk_search: bool = False):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = await self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if LOGS not in raw_json or not raw_json[LOGS]:
            self._log_entries = []
            return None

        try:
            self._log_entries = parse_obj_as(List[SearchLogEntry], raw_json[LOGS])
            if is_bulk_search:
                self._update_first_last_record_creation_times()
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def _prepare_query_for_timestamp_paging(self, query: Query):
        """
        Adjusts the query to include timestamp filters for search log bulk extraction.
        """
        self._criteria.dsl.from_ = 0
        rewritten_filters = []
        if isinstance(query, Bool):
            for filter_ in query.filter:
                if self._is_paging_timestamp_query(filter_):
                    continue
                rewritten_filters.append(filter_)

        if self._first_record_creation_time != self._last_record_creation_time:
            # If the first and last record creation times are different,
            # reset _duplicate_timestamp_page_count to its initial value
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
                # If a Term, Range, etc query type is found
                # in the DSL, append it to the Bool `filter`.
                rewritten_filters.append(query)
                rewritten_query = Bool(filter=rewritten_filters)
            self._criteria.dsl.query = rewritten_query
        else:
            # If the first and last record creation times are the same,
            # we need to switch to offset-based pagination instead of timestamp-based pagination
            # to ensure we get the next set of results without duplicates.
            # We use a page multiplier to skip already-processed records when encountering
            # consecutive pages with identical timestamps, preventing duplicate results.
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
        """
        Update the first and last record creation timestamps for bulk paging.
        """
        self._first_record_creation_time = self._last_record_creation_time = -2

        if not isinstance(self._log_entries, list) or len(self._log_entries) <= 1:
            return

        first_entry, last_entry = self._log_entries[0], self._log_entries[-1]

        if first_entry:
            self._first_record_creation_time = first_entry.created_at

        if last_entry:
            self._last_record_creation_time = last_entry.created_at

    async def __aiter__(self) -> AsyncGenerator[SearchLogEntry, None]:
        """
        Async iterator to work through all pages of results, across all matches for the original query.

        :returns: the next search log entry from the search results
        """
        for entry in self._log_entries:
            yield entry
        while await self.next_page():
            for entry in self._log_entries:
                yield entry

    # Static methods mirrored from SearchLogResults for compatibility
    @staticmethod
    def presorted_by_timestamp(sorts: Optional[List[SortItem]]) -> bool:
        """
        Check if the sorts list is presorted by timestamp.

        :param sorts: list of sort items to check
        :returns: True if presorted by timestamp
        """
        # Import here to avoid circular import
        from pyatlan.model.search_log import SearchLogResults

        return SearchLogResults.presorted_by_timestamp(sorts)

    @staticmethod
    def sort_by_timestamp_first(sorts: Optional[List[SortItem]]) -> List[SortItem]:
        """
        Ensure timestamp sorting is first in the sort list.

        :param sorts: existing sort items
        :returns: sort items with timestamp first
        """
        # Import here to avoid circular import
        from pyatlan.model.search_log import SearchLogResults

        # Handle None case by providing empty list
        if sorts is None:
            sorts = []

        return SearchLogResults.sort_by_timestamp_first(sorts)
