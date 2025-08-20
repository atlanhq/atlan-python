# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, AsyncGenerator, List, Optional, Set

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import INDEX_SEARCH
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregations
from pyatlan.model.assets import Asset
from pyatlan.model.search import (
    DSL,
    Bool,
    IndexSearchRequest,
    Query,
    Range,
    SearchRequest,
    SortItem,
    SortOrder,
)
from pyatlan.utils import API, unflatten_custom_metadata_for_entity

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient
    from pyatlan.client.protocol import AsyncApiCaller


class AsyncSearchResults(abc.ABC):
    """
    Abstract async class that encapsulates results returned by various searches.
    """

    def __init__(
        self,
        client: AsyncApiCaller,
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

    async def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._assets else False

    @abc.abstractmethod
    async def _get_next_page(self):
        """
        Abstract method that must be implemented in subclasses, used to
        fetch the next page of results.
        """

    async def _get_next_page_json(self, is_bulk_search: bool = False):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.
        :param is_bulk_search: whether to retrieve results for a bulk search.
        :returns: JSON for the next page of results, as-is
        """
        raw_json = await self._client._call_api(
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

    async def __aiter__(self) -> AsyncGenerator[Asset, None]:
        """
        Async iterates through the results, lazily-fetching each next page until there
        are no more results.

        :returns: an async iterable form of each result, across all pages
        """
        while True:
            for asset in self.current_page():
                yield asset
            if not await self.next_page():
                break


class AsyncIndexSearchResults(AsyncSearchResults):
    """
    Async version of IndexSearchResults that captures the response from a search against Atlan.
    Also provides the ability to iteratively page through results using async/await,
    without needing to track or re-run the original query.
    """

    _DEFAULT_SIZE = DSL.__fields__.get("size").default or 300  # type: ignore[union-attr]
    _MASS_EXTRACT_THRESHOLD = 100000 - _DEFAULT_SIZE

    def __init__(
        self,
        client: AsyncAtlanClient,
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

    async def next_page(self, start=None, size=None) -> bool:
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
        return await self._get_next_page() if self._assets else False

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
        if raw_json := await super()._get_next_page_json(is_bulk_search):
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
