from typing import Optional

from pydantic import ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import SEARCH_LOG
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregations
from pyatlan.model.search_log import SearchLogRequest, SearchLogResults, UniqueUsers

UNIQUE_USERS = "uniqueUsers"


class SearchLogClient:
    """
    This class can be used to configure and run a search against Atlan's searcg log. This class does not need to be
    instantiated directly but can be obtained through the search_log property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def _get_aggregations(self, raw_json) -> Optional[Aggregations]:
        if "aggregations" in raw_json:
            try:
                aggregations = Aggregations.parse_obj(raw_json["aggregations"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            aggregations = None
        return aggregations

    def _map_bucket_to_unique_user(self, bucket) -> UniqueUsers:
        """
        Maps a bucket from the API response to a search log UniqueUsers instance.
        """
        # Handle the case where the bucket is empty or not a dictionary
        if not bucket or not isinstance(bucket, dict):
            return None

        return UniqueUsers(
            name=bucket.get("key", ""),
            view_count=bucket.get("doc_count", 0),
            view_timestamp=bucket.get("latest_timestamp", {}).get("value", 0),
        )

    def search(self, criteria: SearchLogRequest) -> dict:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :returns: the results of the search
        :raises AtlanError: on any API communication issue
        """
        unique_users = []
        raw_json = self._client._call_api(
            SEARCH_LOG,
            request_obj=criteria,
        )
        if UNIQUE_USERS in raw_json["aggregations"]:
            try:
                user_buckets = raw_json["aggregations"][UNIQUE_USERS].get("buckets", [])
                unique_users = parse_obj_as(
                    list[UniqueUsers],
                    [self._map_bucket_to_unique_user(user) for user in user_buckets],
                )
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        aggregations = self._get_aggregations(raw_json)
        total_views = (
            raw_json["approximateCount"] if "approximateCount" in raw_json else 0
        )
        return SearchLogResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            total_views=total_views,
            unique_users=unique_users,
            aggregations=aggregations,
        )
