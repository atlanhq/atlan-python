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

    def _get_dsl_aggs(self, user_size: int) -> dict[str, Aggregation]:
        return {
            "uniqueUsers": {
                "terms": {
                    "field": "userName",
                    "size": user_size,
                    "order": {"latest_timestamp": "desc"},
                },
                "aggs": {"latest_timestamp": {"max": {"field": "timestamp"}}},
            },
            "totalDistinctUsers": {
                "cardinality": {"field": "userName", "precision_threshold": 1000}
            },
        }

    @classmethod
    def by_guid(
        cls,
        guid: str,
        *,
        size: int = 0,
        from_: int = 0,
        user_size: int = 20,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
    ) -> "SearchLogRequest":
        """
        Create a search log request to retrieve views of an asset by its GUID.

        :param guid: unique identifier of the asset.
        :param size: number of changes to retrieve. Defaults to 0.
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden.
        :param user_size: number of users to retrieve from the search log. Defaults to 20.
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
            aggregations=cls._get_dsl_aggs(cls, user_size),
        )
        return SearchLogRequest(dsl=dsl)

    @classmethod
    def get_recent_search(
        cls,
        guid: str,
        *,
        from_: int = 0,
        size: int = 15,
    ) -> "SearchLogRequest":
        """
        Create a search log request to retrieve recent search logs of an assets.

        :param guid: unique identifier of the asset.
        :param _from: starting point for paging. Defaults to 0 (very first result) if not overridden.
        :param max_logs: number of logs to retrieve from the recent search log. Defaults to 15.

        :returns: A SearchLogRequest that can be used to perform the search.
        """
        dsl = DSL(
            size=size,
            from_=from_,
            source=[
                "host",
                "ipAddress",
                "userAgent",
                "userName",
                "timestamp",
                "entityGuidsAll",
                "entityQFNamesAll",
                "entityTypeNamesAll",
            ],
            sort=[SortItem("timestamp", order="desc")],
            query=Bool(
                filter=[
                    Bool(
                        must=[
                            Term(field="entityGuidsAll", value=guid),
                            Term(field="utmTags", value="action_asset_viewed"),
                        ]
                    )
                ]
            ),
        )
        return SearchLogRequest(dsl=dsl)


class UniqueUsers(AtlanObject):
    """
    Represents unique user entry in the search log.
    Instances of this class should be treated as immutable.
    """

    name: str = Field(description="User name of the user who viewed the assets.")
    view_count: str = Field(description="Total view count of the asset for a user.")
    view_timestamp: datetime = Field(
        description="Latest view timestamp (epoch) of the viewed asset."
    )


class AssetLog(AtlanObject):
    """
    Represents an log entry for asset search in the search log.
    Instances of this class should be treated as immutable.
    """

    log_host: str = Field(
        description="The host information associated with the search log."
    )
    log_ipaddress: str = Field(
        description="The IP address associated with the search log."
    )
    log_user_agent: str = Field(
        description="The user agent information associated with the search log."
    )
    log_username: str = Field(
        description="The username of the user who searched for the assets."
    )
    log_guid: str = Field(description="The GUID of the search log asset.")
    log_qualified_name: str = Field(
        description="The unique name of the search log asset."
    )
    log_type_name: str = Field(description="The type name of the search log asset.")

    log_timestamp: datetime = Field(
        description="The timestamp (epoch) when the search occurred, in milliseconds."
    )


class SearchLogViewResults:
    """Captures the response from a search against Atlan's search log views."""

    def __init__(
        self,
        total_views: int,
        unique_users: list[UniqueUsers],
    ):
        self._total_views = total_views
        self._unique_users = unique_users

    @property
    def total_views(self) -> int:
        return self._total_views

    @property
    def unique_users(self) -> int:
        return self._unique_users


class SearchLogResults(Iterable):
    """Captures the response from a search against Atlan's recent search logs."""

    def __init__(
        self,
        client: ApiCaller,
        criteria: SearchLogRequest,
        start: int,
        size: int,
        count: int,
        asset_logs: list[AssetLog],
        aggregations: dict[str, Aggregation],
    ):
        self._client = client
        self._endpoint = SEARCH_LOG
        self._criteria = criteria
        self._start = start
        self._size = size
        self._count = count
        self._asset_logs = asset_logs
        self._aggregations = aggregations

    @property
    def total_count(self) -> int:
        return self._count

    def current_page(self) -> list[AssetLog]:
        """
        Retrieve the current page of results.

        :returns: list of assets on the current page of results
        """
        return self._asset_logs

    def next_page(self, start=None, size=None) -> bool:
        """
        Indicates whether there is a next page of results.

        :returns: True if there is a next page of results, otherwise False
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._asset_logs else False

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

    def _map_logs_to_asset_log(self, log) -> AssetLog:
        """
        Maps a logs from the API response to a search log AssetLog instance.
        """
        # Handle the case where the log is empty or not a dictionary
        if not log or not isinstance(log, dict):
            return None

        return AssetLog(
            log_host=log.get("host", ""),
            log_ipaddress=log.get("ipAddress", ""),
            log_user_agent=log.get("userAgent", ""),
            log_username=log.get("userName", ""),
            log_guid=log.get("entityGuidsAll")[0],
            log_qualified_name=log.get("entityQFNamesAll")[0],
            log_type_name=log.get("entityTypeNamesAll")[0],
            log_timestamp=log.get("timestamp", 0),
        )

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
            self._asset_logs = []
            return None
        try:
            logs = raw_json.get("logs", [])
            self._asset_logs = parse_obj_as(
                list[AssetLog], [self._map_logs_to_asset_log(log) for log in logs]
            )
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    def __iter__(self) -> Generator[AssetLog, None, None]:
        """
        Iterates through the results, lazily-fetching each next page until there
        are no more results.

        :returns: an iterable form of each result, across all pages
        """
        while True:
            yield from self.current_page()
            if not self.next_page():
                break
