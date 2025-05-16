from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Generator, Iterable, List, Optional, Set

from pydantic.v1 import Field, ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import SEARCH_LOG
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import UTMTags
from pyatlan.model.search import (
    DSL,
    Bool,
    Query,
    Range,
    SearchRequest,
    SortItem,
    SortOrder,
    Term,
    Terms,
)
from pyatlan.utils import deep_get

BY_TIMESTAMP = [SortItem("timestamp", order=SortOrder.ASCENDING)]


class SearchLogRequest(SearchRequest):
    """Class from which to configure a search against Atlan's search log."""

    dsl: DSL
    attributes: List[str] = Field(default_factory=list, alias="attributes")
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

    def __init__(__pydantic_self__, **data: Any) -> None:
        dsl = data.get("dsl")
        class_name = __pydantic_self__.__class__.__name__
        if dsl and isinstance(dsl, DSL) and not dsl.req_class_name:
            data["dsl"] = DSL(req_class_name=class_name, **dsl.dict(exclude_unset=True))
        super().__init__(**data)

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
                filter=query_filter + cls._BASE_QUERY_FILTER,
                must_not=[
                    Terms(
                        field="userName",
                        values=exclude_users + cls._EXCLUDE_USERS,
                    )
                ],
            ),
        )

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}

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
        aggs_terms = {
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


class AssetViews(AtlanObject):
    """
    Captures a specific aggregate result of assets and the views on that asset.
    Instances of this class should be treated as immutable.
    """

    guid: str = Field(description="GUID of the asset that was viewed.")
    total_views: int = Field(
        description="Number of times the asset has been viewed (in total)."
    )
    distinct_users: int = Field(
        description="Number of distinct users that have viewed the asset."
    )


class UserViews(AtlanObject):
    """
    Represents unique user views entry in the search log.
    Instances of this class should be treated as immutable.
    """

    username: str = Field(description="User name of the user who viewed the assets.")
    view_count: int = Field(description="Number of times the user viewed the asset.")
    most_recent_view: datetime = Field(
        description="When the user most recently viewed the asset (epoch-style), in milliseconds."
    )


class SearchLogEntry(AtlanObject):
    """
    Represents a log entry for asset search in the search log.
    Instances of this class should be treated as immutable.
    """

    user_agent: str = Field(
        description="Details of the browser or other client used to make the request."
    )
    host: str = Field(
        description="Hostname of the tenant against which the search was run."
    )
    ip_address: str = Field(description="IP address from which the search was run.")
    user_name: str = Field(description="Username of the user who ran the search.")
    entity_guids_all: List[str] = Field(
        default_factory=list,
        alias="entityGuidsAll",
        description="GUID(s) of asset(s) that were in the results of the search.",
    )
    entity_qf_names_all: List[str] = Field(
        default_factory=list,
        alias="entityQFNamesAll",
        description="Unique name(s) of asset(s) that were in the results of the search.",
    )
    entity_guids_allowed: List[str] = Field(
        default_factory=list,
        alias="entityGuidsAllowed",
        description="GUID(s) of asset(s) that were in the results of the search, that the user is permitted to see.",
    )
    entity_qf_names_allowed: List[str] = Field(
        default_factory=list,
        alias="entityQFNamesAllowed",
        description=(
            "Unique name(s) of asset(s) that were in the results of the search, that the user is permitted to see."
        ),
    )
    entity_type_names_all: List[str] = Field(
        default_factory=list,
        alias="entityTypeNamesAll",
        description="Name(s) of the types of assets that were in the results of the search.",
    )
    entity_type_names_allowed: List[str] = Field(
        default_factory=list,
        alias="entityTypeNamesAllowed",
        description=(
            "Name(s) of the types of assets that were in the results of the search, that the user is permitted to see."
        ),
    )
    utm_tags: List[str] = Field(
        default_factory=list, description="Tag(s) that were sent in the search request."
    )
    has_result: bool = Field(
        alias="hasResult",
        description="Whether the search had any results (true) or not (false).",
    )
    results_count: int = Field(
        alias="resultsCount", description="Number of results for the search."
    )
    response_time: int = Field(
        alias="responseTime",
        description="Elapsed time to produce the results for the search, in milliseconds.",
    )
    created_at: datetime = Field(
        alias="createdAt",
        description="Time (epoch-style) at which the search was logged, in milliseconds.",
    )
    timestamp: datetime = Field(
        description="Time (epoch-style) at which the search was run, in milliseconds."
    )
    failed: bool = Field(
        description="Whether the search was successful (false) or not (true)."
    )
    request_dsl: dict = Field(
        alias="request.dsl", description="DSL of the full search request that was made."
    )
    request_dsl_text: str = Field(
        alias="request.dslText",
        description="DSL of the full search request that was made, as a string.",
    )
    request_attributes: Optional[List[str]] = Field(
        alias="request.attributes",
        description="List of attribute (names) that were requested as part of the search.",
    )
    request_relation_attributes: Optional[List[str]] = Field(
        alias="request.relationAttributes",
        description="List of relationship attribute (names) that were requested as part of the search.",
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

    _DEFAULT_SIZE = DSL.__fields__.get("size").default or 300  # type: ignore[union-attr]
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
        self._processed_log_entries: Set[str] = set()

    @property
    def count(self) -> int:
        return self._count

    def current_page(self) -> List[SearchLogEntry]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._log_entries

    def _get_sl_unique_key(self, entity: SearchLogEntry) -> Optional[str]:
        """
        Returns a unique key for a `SearchLogEntry` by
        combining `entity_guid` with the timestamp.

        NOTE: This is necessary because the search log API
        does not provide a unique identifier for logs.

        :param: search log entry
        :returns: unique key or None if no valid key is found
        """
        entity_guid = entity.entity_guids_all[0] if entity.entity_guids_all else None

        # If entity_guid is not present, try to extract it from request_dsl; otherwise, return None
        if not entity_guid:
            terms = deep_get(
                entity.request_dsl, "query.function_score.query.bool.filter.bool.must"
            )
            if not terms:
                return None

            if isinstance(terms, list):
                for term in terms:
                    if isinstance(term, dict) and term.get("term", {}).get("__guid"):
                        entity_guid = term["term"]["__guid"]
                        break
            elif isinstance(terms, dict):
                entity_guid = terms.get("term", {}).get("__guid")

        return (
            f"{entity_guid}:{entity.timestamp}"
            if entity_guid and entity_guid != "undefined"
            else None
        )

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
            # Used in the "timestamp-based" paging approach
            # to check if search log with the unique key "_get_sl_unique_key()"
            # has already been processed in a previous page of results.
            # If it has, then exclude it from the current results;
            # otherwise, we may encounter duplicate search log records.
            self._processed_log_entries.update(
                key
                for entity in self._log_entries
                if (key := self._get_sl_unique_key(entity))
            )
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
            self._log_entries = parse_obj_as(List[SearchLogEntry], raw_json["logs"])
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
        Adjusts the query to include timestamp filters for search log bulk extraction.
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
            self._criteria.dsl.from_ = len(self._processed_log_entries)

    @staticmethod
    def _get_paging_timestamp_query(last_timestamp: int) -> Query:
        return Range(field="createdAt", gte=last_timestamp)

    @staticmethod
    def _is_paging_timestamp_query(filter_: Query) -> bool:
        return (
            isinstance(filter_, Range)
            and filter_.field == "createdAt"
            and filter_.gte is not None
        )

    def _filter_processed_entities(self):
        """
        Remove log entries that have already been processed to avoid duplicates.
        """
        self._log_entries = [
            entity
            for entity in self._log_entries
            if entity is not None
            and self._get_sl_unique_key(entity) not in self._processed_log_entries
        ]

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
        priority. Adds this condition if it does not
        already exist, or moves it up to the top sorting
        priority if it does already exist in the list.

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
            # Added a condition to disable "timestamp" sorting when bulk search for logs is enabled,
            # as sorting is already handled based on "createdAt" in this case.
            if (
                (not sort.field)
                or (sort.field != Asset.CREATE_TIME.internal_field_name)
            )
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
