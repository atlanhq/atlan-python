# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, AsyncGenerator, List, Optional, Set, Union

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import AUDIT_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.audit import AuditSearchRequest, EntityAudit
from pyatlan.model.search import DSL, Bool, Query, Range, SortItem

if TYPE_CHECKING:
    from pyatlan.client.protocol import AsyncApiCaller

ENTITY_AUDITS = "entityAudits"
TOTAL_COUNT = "totalCount"


class AsyncAuditSearchResults:
    """
    Async version of AuditSearchResults that captures the response from a search against Atlan's activity log.
    Also provides the ability to iteratively page through results using async/await,
    without needing to track or re-run the original query.
    """

    _DEFAULT_SIZE = DSL.__fields__.get("size").default or 300  # type: ignore[union-attr]
    _MASS_EXTRACT_THRESHOLD = 10000 - _DEFAULT_SIZE

    def __init__(
        self,
        client: AsyncApiCaller,
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
        # See AuditSearchResults: the offset fallback offsets WITHIN a single
        # `created` timestamp bucket (bounded) rather than over the whole result
        # set, so from_ + size can never exceed ES's max_result_window (BLDX-1549).
        self._max_processed_ts: Optional[datetime] = None
        self._count_at_max_ts: int = 0

    @property
    def aggregations(self) -> Optional[Aggregation]:
        return self._aggregations

    @property
    def total_count(self) -> int:
        return self._count

    def current_page(self) -> List[EntityAudit]:
        """
        Retrieve the current page of results.

        :returns: list of entity audits on the current page of results
        """
        return self._entity_audits

    async def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results and fetches it.

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
            # to check if audit `entity.event_key` has already been processed
            # in a previous page of results.
            # If it has,then exclude it from the current results;
            # otherwise, we may encounter duplicate audit entity records.
            for entity in self._entity_audits:
                if entity.event_key in self._processed_entity_keys:
                    continue
                self._processed_entity_keys.add(entity.event_key)
                # Maintain the max-timestamp bucket used by the offset fallback.
                ts = entity.created
                if self._max_processed_ts is None or ts > self._max_processed_ts:
                    self._max_processed_ts = ts
                    self._count_at_max_ts = 1
                elif ts == self._max_processed_ts:
                    self._count_at_max_ts += 1
        return await self._get_next_page() if self._entity_audits else False

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
            self._count = raw_json.get(TOTAL_COUNT, 0)
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
        if ENTITY_AUDITS not in raw_json or not raw_json[ENTITY_AUDITS]:
            self._entity_audits = []
            return None

        try:
            self._entity_audits = parse_obj_as(
                List[EntityAudit], raw_json[ENTITY_AUDITS]
            )
            if is_bulk_search:
                self._filter_processed_entities()
                self._update_first_last_record_creation_times()
            return raw_json
        except ValidationError as err:
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
            # The page spans multiple `created` timestamps: advance the window past
            # the last one and reset the offset — the normal fast path.
            rewritten_filters.append(
                self._get_paging_timestamp_query(self._last_record_creation_time)
            )
            from_ = 0
        else:
            # The page collapsed to a single `created` timestamp (or netted <= 1 new
            # record after dedup), so the window cannot be advanced by timestamp.
            # Keep the timestamp filter pinned to that timestamp and offset only
            # WITHIN its bucket, so `from_` is bounded by the number of audits that
            # share one timestamp — `from_ + size` can never exceed ES's
            # max_result_window. Dedup via `_processed_entity_keys` still guards
            # against boundary overlap.
            #
            # Previously this offset was `len(self._processed_entity_keys)` over the
            # whole result set with the timestamp filter dropped, which Elasticsearch
            # rejected once > 10,000 audits had been processed (BLDX-1549:
            # "Result window is too large ... but was [43504]").
            if self._max_processed_ts is not None:
                rewritten_filters.append(
                    self._get_paging_timestamp_query(self._max_processed_ts)
                )
            from_ = self._count_at_max_ts

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
        self._criteria.dsl.from_ = from_
        self._criteria.dsl.query = rewritten_query

    @staticmethod
    def _get_paging_timestamp_query(last_timestamp: Union[int, datetime]) -> Query:
        """
        Get timestamp query for paging based on the last record's timestamp.

        :param last_timestamp: timestamp of the last record
        :returns: Range query for timestamp filtering
        """
        return Range(field="created", gte=last_timestamp)

    @staticmethod
    def _is_paging_timestamp_query(filter_: Query) -> bool:
        """
        Check if a query is a timestamp paging query.

        :param filter_: the query to check
        :returns: True if this is a timestamp paging query
        """
        return (
            isinstance(filter_, Range)
            and filter_.field == "created"
            and filter_.gte is not None
        )

    def _filter_processed_entities(self):
        """
        Filter out entities that have already been processed in previous pages.
        """
        self._entity_audits = [
            entity
            for entity in self._entity_audits
            if entity is not None
            and entity.event_key not in self._processed_entity_keys
        ]

    def _update_first_last_record_creation_times(self):
        """
        Update the first and last record creation timestamps for bulk paging.
        """
        self._first_record_creation_time = self._last_record_creation_time = -2

        if not isinstance(self._entity_audits, list) or len(self._entity_audits) <= 1:
            return

        first_audit, last_audit = self._entity_audits[0], self._entity_audits[-1]

        if first_audit:
            self._first_record_creation_time = first_audit.created

        if last_audit:
            self._last_record_creation_time = last_audit.created

    async def __aiter__(self) -> AsyncGenerator[EntityAudit, None]:
        """
        Async iterator to work through all pages of results, across all matches for the original query.

        :returns: the next entity audit from the search results
        """
        for entity in self._entity_audits:
            yield entity
        while await self.next_page():
            for entity in self._entity_audits:
                yield entity

    # Static methods mirrored from AuditSearchResults for compatibility
    @staticmethod
    def presorted_by_timestamp(sorts: Optional[List[SortItem]]) -> bool:
        """
        Check if the sorts list is presorted by timestamp.

        :param sorts: list of sort items to check
        :returns: True if presorted by timestamp
        """
        # Import here to avoid circular import
        from pyatlan.model.audit import AuditSearchResults

        return AuditSearchResults.presorted_by_timestamp(sorts)

    @staticmethod
    def sort_by_timestamp_first(sorts: Optional[List[SortItem]]) -> List[SortItem]:
        """
        Ensure timestamp sorting is first in the sort list.

        :param sorts: existing sort items
        :returns: sort items with timestamp first
        """
        # Import here to avoid circular import
        from pyatlan.model.audit import AuditSearchResults

        # Handle None case by providing empty list
        if sorts is None:
            sorts = []

        return AuditSearchResults.sort_by_timestamp_first(sorts)
