from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import Field

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import SEARCH_LOG
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.core import AtlanObject
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


class SearchLogUtmTags(str, Enum):
    ACTION_ASSET_VIEWED = "action_asset_viewed"


class SearchLogRequest(SearchRequest):
    """Class from which to configure a search against Atlan's activity log."""

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
        _from: int = 0,
        user_size: int = 20,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None
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
                values=[SearchLogUtmTags.ACTION_ASSET_VIEWED],
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
            _from=_from,
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


class SearchLogResults:
    """Captures the response from a search against Atlan's search log."""

    def __init__(
        self,
        client: ApiCaller,
        criteria: SearchLogRequest,
        start: int,
        size: int,
        total_views: int,
        unique_users: list[UniqueUsers],
        aggregations: dict[str, Aggregation],
    ):
        self._client = client
        self._endpoint = SEARCH_LOG
        self._criteria = criteria
        self._start = start
        self._size = size
        self._total_views = total_views
        self._unique_users = unique_users
        self._aggregations = aggregations

    @property
    def total_views(self) -> int:
        return self._total_views

    @property
    def unique_users(self) -> int:
        return self._unique_users
