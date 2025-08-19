# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, List, Optional, Set

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
            self._processed_entity_keys.update(
                entity.event_key for entity in self._entity_audits
            )
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
            self._criteria.dsl.from_ = 0
            self._criteria.dsl.query = rewritten_query
        else:
            # Ensure that when switching to offset-based paging, if the first and last record timestamps are the same,
            # we do not include a created timestamp filter (ie: Range(field='__timestamp', gte=VALUE)) in the query.
            # Instead, ensure the search runs with only SortItem(field='__timestamp', order=<SortOrder.ASCENDING>).
            # Failing to do so can lead to incomplete results (less than the approximate count) when running the search
            # with a small page size.
            if isinstance(query, Bool):
                for filter_ in query.filter:
                    if self._is_paging_timestamp_query(filter_):
                        query.filter.remove(filter_)

            # Always ensure that the offset is set to the length of the processed assets
            # instead of the default (start + size), as the default may skip some assets
            # and result in incomplete results (less than the approximate count)
            self._criteria.dsl.from_ = len(self._processed_entity_keys)

    @staticmethod
    def _get_paging_timestamp_query(last_timestamp: int) -> Query:
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
