# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import json as json_lib
from datetime import datetime
from typing import Any, Dict, Generator, Iterable, List, Optional

import msgspec

from pyatlan.client.constants import SEARCH_LOG
from pyatlan.client.protocol import ApiCaller
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import SortOrder, UTMTags
from pyatlan_v9.model.aggregation import Aggregation
from pyatlan_v9.model.search import DSL, Bool, Query, Range, SortItem, Term, Terms

BY_TIMESTAMP = [SortItem("timestamp", order=SortOrder.ASCENDING)]


_EXCLUDE_USERS: List[str] = [
    "support",
    "atlansupport",
]
_BASE_QUERY_FILTER: List[Query] = [
    Term(
        field="utmTags",
        value=UTMTags.ACTION_ASSET_VIEWED.value,
    ),
    Bool(
        should=[
            Term(field="utmTags", value=UTMTags.UI_PROFILE.value),
            Term(field="utmTags", value=UTMTags.UI_SIDEBAR.value),
        ],
        minimum_should_match=1,
    ),
]


class SearchLogRequest(msgspec.Struct, kw_only=True):
    """Class from which to configure a search against Atlan's search log."""

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
        """Serialize SearchLogRequest to JSON string."""
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
    def _get_view_dsl_kwargs(
        cls,
        size: int,
        from_: int,
        query_filter: Optional[list] = None,
        sort: Optional[list] = None,
        exclude_users: Optional[List[str]] = None,
    ) -> dict:
        sort = sort or []
        query_filter = query_filter or []
        exclude_users = exclude_users or []
        return dict(
            size=size,
            from_=from_,
            sort=sort + BY_TIMESTAMP,
            query=Bool(
                filter=query_filter + _BASE_QUERY_FILTER,
                must_not=[
                    Terms(
                        field="userName",
                        values=exclude_users + _EXCLUDE_USERS,
                    )
                ],
            ),
        )

    @staticmethod
    def _get_recent_viewers_aggs(max_users: int) -> Dict[str, object]:
        return {
            "uniqueUsers": {
                "terms": {
                    "field": "userName",
                    "size": max_users,
                    "order": [{"latest_timestamp": "desc"}],
                },
                "aggregations": {"latest_timestamp": {"max": {"field": "timestamp"}}},
            },
            "totalDistinctUsers": {
                "cardinality": {"field": "userName", "precision_threshold": 1000}
            },
        }

    @staticmethod
    def _get_most_viewed_assets_aggs(
        max_assets: int, by_diff_user: bool
    ) -> Dict[str, object]:
        aggs_terms: Dict[str, Any] = {
            "field": "entityGuidsAll",
            "size": max_assets,
        }
        if by_diff_user:
            aggs_terms.update({"order": [{"uniqueUsers": "desc"}]})
        return {
            "uniqueAssets": {
                "aggregations": {
                    "uniqueUsers": {
                        "cardinality": {
                            "field": "userName",
                            "precision_threshold": 1000,
                        }
                    }
                },
                "terms": aggs_terms,
            },
            "totalDistinctUsers": {
                "cardinality": {"field": "userName", "precision_threshold": 1000}
            },
        }

    @classmethod
    def most_recent_viewers(
        cls,
        guid: str,
        max_users: int = 20,
        exclude_users: Optional[List[str]] = None,
    ) -> SearchLogRequest:
        """
        Create a search log request to retrieve views of an asset by its GUID.

        :param guid: unique identifier of the asset.
        :param max_users: maximum number of recent users to consider. Defaults to 20.
        :param exclude_users: a list containing usernames to be excluded from the search log results (optional).

        :returns: A SearchLogRequest that can be used to perform the search.
        """
        query_filter = [
            Term(field="entityGuidsAll", value=guid, case_insensitive=False)
        ]
        dsl = DSL(
            **cls._get_view_dsl_kwargs(
                size=0, from_=0, query_filter=query_filter, exclude_users=exclude_users
            ),
            aggregations=cls._get_recent_viewers_aggs(max_users),
        )
        return SearchLogRequest(dsl=dsl)

    @classmethod
    def most_viewed_assets(
        cls,
        max_assets: int = 10,
        by_different_user: bool = False,
        exclude_users: Optional[List[str]] = None,
    ) -> SearchLogRequest:
        """
        Create a search log request to retrieve most viewed assets.

        :param max_assets: maximum number of assets to consider. Defaults to 10.
        :param by_different_user: when True, will consider assets viewed by more users as more
        important than total view count, otherwise will consider total view count most important.
        :param exclude_users: a list containing usernames to be excluded from the search log results (optional).

        :returns: A SearchLogRequest that can be used to perform the search.
        """
        dsl = DSL(
            **cls._get_view_dsl_kwargs(size=0, from_=0, exclude_users=exclude_users),
            aggregations=cls._get_most_viewed_assets_aggs(
                max_assets, by_different_user
            ),
        )
        return SearchLogRequest(dsl=dsl)

    @classmethod
    def views_by_guid(
        cls,
        guid: str,
        size: int = 20,
        from_: int = 0,
        sort: Optional[List[SortItem]] = None,
        exclude_users: Optional[List[str]] = None,
    ) -> SearchLogRequest:
        """
        Create a search log request to retrieve recent search logs of an assets.

        :param guid: unique identifier of the asset.
        :param size: number of results to retrieve per page. Defaults to 20.
        :param from_: starting point for paging. Defaults to 0 (very first result) if not overridden.
        :param sort: properties by which to sort the results (optional).
        :param exclude_users: a list containing usernames to be excluded from the search log results (optional).

        :returns: A SearchLogRequest that can be used to perform the search.
        """
        query_filter = [
            Term(field="entityGuidsAll", value=guid, case_insensitive=False)
        ]
        dsl = DSL(
            **cls._get_view_dsl_kwargs(
                size=size,
                from_=from_,
                query_filter=query_filter,
                sort=sort,
                exclude_users=exclude_users,
            ),
        )
        return SearchLogRequest(dsl=dsl)


class AssetViews(msgspec.Struct, kw_only=True):
    """
    Captures a specific aggregate result of assets and the views on that asset.
    Instances of this class should be treated as immutable.
    """

    guid: str
    total_views: int
    distinct_users: int


class UserViews(msgspec.Struct, kw_only=True):
    """
    Represents unique user views entry in the search log.
    Instances of this class should be treated as immutable.
    """

    username: str
    view_count: int
    most_recent_view: datetime


class SearchLogEntry(msgspec.Struct, kw_only=True):
    """
    Represents a log entry for asset search in the search log.
    Instances of this class should be treated as immutable.
    """

    user_agent: str
    host: str
    ip_address: str
    user_name: str
    entity_guids_all: List[str] = msgspec.field(
        default_factory=list, name="entityGuidsAll"
    )
    entity_qf_names_all: List[str] = msgspec.field(
        default_factory=list, name="entityQFNamesAll"
    )
    entity_guids_allowed: List[str] = msgspec.field(
        default_factory=list, name="entityGuidsAllowed"
    )
    entity_qf_names_allowed: List[str] = msgspec.field(
        default_factory=list, name="entityQFNamesAllowed"
    )
    entity_type_names_all: List[str] = msgspec.field(
        default_factory=list, name="entityTypeNamesAll"
    )
    entity_type_names_allowed: List[str] = msgspec.field(
        default_factory=list, name="entityTypeNamesAllowed"
    )
    utm_tags: List[str] = msgspec.field(default_factory=list)
    has_result: bool = msgspec.field(default=False, name="hasResult")
    results_count: int = msgspec.field(default=0, name="resultsCount")
    response_time: int = msgspec.field(default=0, name="responseTime")
    created_at: datetime = msgspec.field(default_factory=datetime.now, name="createdAt")
    timestamp: datetime = msgspec.field(default_factory=datetime.now)
    failed: bool = False
    request_dsl: Optional[dict] = msgspec.field(default=None, name="request.dsl")
    request_dsl_text: Optional[str] = msgspec.field(
        default=None, name="request.dslText"
    )
    request_attributes: Optional[List[str]] = msgspec.field(
        default=None, name="request.attributes"
    )
    request_relation_attributes: Optional[List[str]] = msgspec.field(
        default=None, name="request.relationAttributes"
    )


class SearchLogViewResults:
    """Captures the response from a search against Atlan's search log views."""

    def __init__(
        self,
        count: int,
        user_views: Optional[List[UserViews]] = None,
        asset_views: Optional[List[AssetViews]] = None,
    ):
        self._count = count
        self._user_views = user_views
        self._asset_views = asset_views

    @property
    def count(self) -> int:
        return self._count

    @property
    def user_views(self) -> Optional[List[UserViews]]:
        return self._user_views

    @property
    def asset_views(self) -> Optional[List[AssetViews]]:
        return self._asset_views


class SearchLogResults(Iterable):
    """Captures the response from a search against Atlan's recent search logs."""

    _DEFAULT_SIZE = 300
    _MASS_EXTRACT_THRESHOLD = 10000 - _DEFAULT_SIZE

    def __init__(
        self,
        client: ApiCaller,
        criteria: SearchLogRequest,
        start: int,
        size: int,
        count: int,
        log_entries: List[SearchLogEntry],
        aggregations: Dict[str, Aggregation],
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
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._log_entries

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._log_entries else False

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        query = self._criteria.dsl.query
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        is_bulk_search = (
            self._bulk or self._approximate_count > self._MASS_EXTRACT_THRESHOLD
        )
        if is_bulk_search:
            self._prepare_query_for_timestamp_paging(query)

        if raw_json := self._get_next_page_json(is_bulk_search):
            self._count = raw_json.get("approximateCount", 0)
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

        if "logs" not in raw_json or not raw_json["logs"]:
            self._log_entries = []
            return None
        try:
            self._log_entries = [
                msgspec.convert(entry, SearchLogEntry) for entry in raw_json["logs"]
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
    def presorted_by_timestamp(sorts: Optional[List[SortItem]]) -> bool:
        """
        Checks if the sorting options prioritize creation time in ascending order.
        :param sorts: list of sorting options or None.
        :returns: True if sorting is already prioritized by creation time, False otherwise.
        """
        if sorts and isinstance(sorts[0], SortItem):
            return (
                sorts[0].field == "createdAt" and sorts[0].order == SortOrder.ASCENDING
            )
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

    def __iter__(self) -> Generator[SearchLogEntry, None, None]:
        """
        Iterates through the results, lazily-fetching each next page until there
        are no more results.

        :returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.next_page():
                break
