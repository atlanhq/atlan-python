from typing import List, Union

from pydantic.v1 import ValidationError, parse_obj_as, validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import SEARCH_LOG
from pyatlan.errors import ErrorCode
from pyatlan.model.search_log import (
    AssetViews,
    SearchLogEntry,
    SearchLogRequest,
    SearchLogResults,
    SearchLogViewResults,
    UserViews,
)

UNIQUE_USERS = "uniqueUsers"
UNIQUE_ASSETS = "uniqueAssets"


class SearchLogClient:
    """
    This class can be used to configure and run a search against Atlan's searcg log.
    This class does not need to be instantiated directly but can be obtained
    through the search_log property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def _map_bucket_to_user_view(self, bucket) -> Union[UserViews, None]:
        """
        Maps a bucket from the API response to a search log UserViews instance.
        """
        # Handle the case where the bucket is empty or not a dictionary
        if not bucket or not isinstance(bucket, dict):
            return None

        return UserViews(
            username=bucket.get("key", ""),
            view_count=bucket.get("doc_count", 0),
            most_recent_view=bucket.get("latest_timestamp", {}).get("value", 0),
        )

    def _map_bucket_to_asset_view(self, bucket) -> Union[AssetViews, None]:
        """
        Maps a bucket from the API response to a search log AssetViews instance.
        """
        # Handle the case where the bucket is empty or not a dictionary
        if not bucket or not isinstance(bucket, dict):
            return None

        return AssetViews(
            guid=bucket.get("key", ""),
            total_views=bucket.get("doc_count", 0),
            distinct_users=bucket.get(UNIQUE_USERS, {}).get("value", 0),
        )

    def _call_search_api(self, criteria: SearchLogRequest) -> dict:
        """
        Calls the Atlan search API, facilitating easier mocking for testing purposes.

        :param criteria: An instance of SearchLogRequest detailing the search query, parameters, etc.
        :return: A dictionary representing the raw JSON response from the search API.
        """
        return self._client._call_api(
            SEARCH_LOG,
            request_obj=criteria,
        )

    @validate_arguments
    def search(
        self, criteria: SearchLogRequest
    ) -> Union[SearchLogViewResults, SearchLogResults]:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :returns: the results of the search
        :raises AtlanError: on any API communication issue
        """
        user_views = []
        asset_views = []
        log_entries = []
        raw_json = self._call_search_api(criteria)
        count = raw_json.get("approximateCount", 0)
        if "aggregations" in raw_json and UNIQUE_USERS in raw_json.get(
            "aggregations", {}
        ):
            try:
                user_views_bucket = raw_json["aggregations"][UNIQUE_USERS].get(
                    "buckets", []
                )
                user_views = parse_obj_as(
                    List[UserViews],
                    [
                        self._map_bucket_to_user_view(user_view)
                        for user_view in user_views_bucket
                    ],
                )
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
            return SearchLogViewResults(
                count=count,
                user_views=user_views,
            )
        if "aggregations" in raw_json and UNIQUE_ASSETS in raw_json.get(
            "aggregations", {}
        ):
            try:
                asset_views_bucket = raw_json["aggregations"][UNIQUE_ASSETS].get(
                    "buckets", []
                )
                asset_views = parse_obj_as(
                    List[AssetViews],
                    [
                        self._map_bucket_to_asset_view(asset_view)
                        for asset_view in asset_views_bucket
                    ],
                )
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
            return SearchLogViewResults(
                count=count,
                asset_views=asset_views,
            )
        # for recent search logs
        if "logs" in raw_json and raw_json.get("logs", []):
            try:
                log_entries = parse_obj_as(List[SearchLogEntry], raw_json["logs"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        return SearchLogResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            log_entries=log_entries,
            aggregations={},
        )
