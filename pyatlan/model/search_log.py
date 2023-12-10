from datetime import datetime
from typing import Generator, Iterable, Optional

from pydantic import Field, ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import SEARCH_LOG
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import UTMTags
from pyatlan.model.search import (
    DSL,
    Bool,
    Query,
    Range,
    SearchRequest,
    SortItem,
    Term,
    Terms,
)


class SearchLogRequest(SearchRequest):
    """Class from which to configure a search against Atlan's search log."""

    dsl: DSL
    attributes: list[str] = Field(default_factory=list, alias="attributes")

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}

    def _get_dsl_aggs(self, max_users: int) -> dict[str, Aggregation]:
        return {
            "uniqueUsers": {
                "terms": {
                    "field": "userName",
                    "size": max_users,
                    "order": {"latest_timestamp": "desc"},
                },
                "aggs": {"latest_timestamp": {"max": {"field": "timestamp"}}},
            },
            "totalDistinctUsers": {
                "cardinality": {"field": "userName", "precision_threshold": 1000}
            },
        }

    @classmethod
    def most_recent_viewers(
        cls,
        guid: str,
        *,
        size: int = 0,
        from_: int = 0,
        max_users: int = 20,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> "SearchLogRequest":
        """
        Create a search log request to retrieve views of an asset by its GUID.

        :param guid: unique identifier of the asset.
        :param size: number of changes to retrieve. Defaults to 0.
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden.
        :param max_users: maximum number of recent users to consider. Defaults to 20.
        :param start_time: start timestamp (epoch) for the search log range filter.
        :param end_time: end timestamp (epoch) for the search log range filter.

        :returns: A SearchLogRequest that can be used to perform the search.
        """
        query_filters = [
            Terms(
                field="utmTags",
                values=[UTMTags.ACTION_ASSET_VIEWED],
            ),
            Bool(
                should=[
                    Term(field="utmTags", value="ui_profile"),
                    Term(field="utmTags", value="ui_sidebar"),
                ],
                minimum_should_match=1,
            ),
            Term(
                field="entityGuidsAll",
                value=guid,
            ),
        ]
        if start_time and end_time:
            query_filters.append(
                Range(
                    field="timestamp",
                    gte=start_time,
                    lte=end_time,
                )
            )
        dsl = DSL(
            size=size,
            from_=from_,
            sort=[],
            query=Bool(
                filter=[Bool(must=query_filters)],
                must_not=[
                    Terms(
                        field="userName",
                        values=[
                            "atlansupport",
                            "support",
                            "support@atlan.com",
                            "atlansupport@atlan.com",
                            "hello@atlan.com",
                        ],
                    ),
                ],
            ),
            aggregations=cls._get_dsl_aggs(cls, max_users),
        )
        return SearchLogRequest(dsl=dsl)

    @classmethod
    def most_viewed_assets(
        cls,
        max_assets: int = 10,
        *,
        size: int = 0,
        from_: int = 0,
        by_different_user: bool = False,
    ) -> "SearchLogRequest":
        asset_aggs_terms = {
            "field": "entityGuidsAll",
            "size": max_assets,
        }
        if by_different_user:
            asset_aggs_terms.update({"order": {"uniqueUsers": "desc"}})
        query_filters = [
            Term(field="utmTags", value="action_asset_viewed"),
            Bool(
                should=[
                    Term(field="utmTags", value="ui_profile"),
                    Term(field="utmTags", value="ui_sidebar"),
                ],
                minimum_should_match=1,
            ),
        ]
        dsl = DSL(
            size=size,
            from_=from_,
            aggregations={
                "uniqueAssets": {
                    "aggregations": {
                        "uniqueUsers": {
                            "cardinality": {
                                "field": "userName",
                                "precision_threshold": 1000,
                            }
                        }
                    },
                    "terms": asset_aggs_terms,
                },
                "totalDistinctUsers": {
                    "cardinality": {"field": "userName", "precision_threshold": 1000}
                },
            },
            query=Bool(filter=query_filters),
            sort=[SortItem("timestamp", order="asc")],
            track_total_hits=True,
        )
        return SearchLogRequest(dsl=dsl)

    @classmethod
    def views_by_guid(
        cls,
        guid: str,
        *,
        from_: int = 0,
        size: int = 20,
    ) -> "SearchLogRequest":
        """
        Create a search log request to retrieve recent search logs of an assets.

        :param guid: unique identifier of the asset.
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden.
        :param max_logs: number of logs to retrieve from the recent search log. Defaults to 20.

        :returns: A SearchLogRequest that can be used to perform the search.
        """
        dsl = DSL(
            from_=0,
            size=size,
            query=Bool(
                filter=[
                    Term(field="utmTags", value="action_asset_viewed"),
                    Term(field="entityGuidsAll", value=guid, case_insensitive=False),
                    Bool(
                        minimum_should_match="1",
                        should=[
                            Term(field="utmTags", value="ui_profile"),
                            Term(field="utmTags", value="ui_sidebar"),
                        ],
                    ),
                ]
            ),
            sort=[SortItem("timestamp", order="asc")],
            track_total_hits=True,
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
    view_count: str = Field(description="Number of times the user viewed the asset.")
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
    entity_guids_all: list[str] = Field(
        default_factory=list,
        alias="entityGuidsAll",
        description="GUID(s) of asset(s) that were in the results of the search.",
    )
    entity_qf_names_all: list[str] = Field(
        default_factory=list,
        alias="entityQFNamesAll",
        description="Unique name(s) of asset(s) that were in the results of the search.",
    )
    entity_guids_allowed: list[str] = Field(
        default_factory=list,
        alias="entityGuidsAllowed",
        description="GUID(s) of asset(s) that were in the results of the search, that the user is permitted to see.",
    )
    entity_qf_names_allowed: list[str] = Field(
        default_factory=list,
        alias="entityQFNamesAllowed",
        description=(
            "Unique name(s) of asset(s) that were in the "
            "results of the search, that the user is permitted to see."
        ),
    )
    entity_type_names_all: list[str] = Field(
        default_factory=list,
        alias="entityTypeNamesAll",
        description="Name(s) of the types of assets that were in the results of the search.",
    )
    entity_type_names_allowed: list[str] = Field(
        default_factory=list,
        alias="entityTypeNamesAllowed",
        description=(
            "Name(s) of the types of assets that were in "
            "the results of the search, that the user is permitted to see."
        ),
    )
    utm_tags: list[str] = Field(
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
    request_attributes: Optional[list[str]] = Field(
        alias="request.attributes",
        description="List of attribute (names) that were requested as part of the search.",
    )
    request_relation_attributes: Optional[list[str]] = Field(
        alias="request.relationAttributes",
        description="List of relationship attribute (names) that were requested as part of the search.",
    )


class SearchLogViewResults:
    """Captures the response from a search against Atlan's search log views."""

    def __init__(
        self,
        count: int,
        user_views: Optional[list[UserViews]] = None,
        asset_views: Optional[list[AssetViews]] = None,
    ):
        self._count = count
        self._user_views = user_views
        self._asset_views = asset_views

    @property
    def count(self) -> int:
        return self._count

    @property
    def user_views(self) -> int:
        return self._user_views

    @property
    def asset_views(self) -> int:
        return self._asset_views


class SearchLogResults(Iterable):
    """Captures the response from a search against Atlan's recent search logs."""

    def __init__(
        self,
        client: ApiCaller,
        criteria: SearchLogRequest,
        start: int,
        size: int,
        count: int,
        log_enties: list[SearchLogEntry],
        aggregations: dict[str, Aggregation],
    ):
        self._client = client
        self._endpoint = SEARCH_LOG
        self._criteria = criteria
        self._start = start
        self._size = size
        self._count = count
        self._log_enties = log_enties
        self._aggregations = aggregations

    @property
    def count(self) -> int:
        return self._count

    def current_page(self) -> list[SearchLogEntry]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._log_enties

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._log_enties else False

    def _get_next_page(self):
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := self._get_next_page_json():
            self._count = (
                raw_json["approximateCount"] if "approximateCount" in raw_json else 0
            )
            return True
        return False

    def _get_next_page_json(self):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "logs" not in raw_json or not raw_json["logs"]:
            self._log_enties = []
            return None
        try:
            raw_json.get("logs", [])
            self._log_enties = parse_obj_as(list[SearchLogEntry], raw_json["logs"])
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

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
