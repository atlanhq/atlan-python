from typing import Optional

from pydantic import ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import SEARCH_LOG
from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregations
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

    def _map_bucket_to_user_view(self, bucket) -> UserViews:
        """
        Maps a bucket from the API response to a search log UniqueUsers instance.
        """
        # Handle the case where the bucket is empty or not a dictionary
        if not bucket or not isinstance(bucket, dict):
            return None

        return UserViews(
            username=bucket.get("key", ""),
            view_count=bucket.get("doc_count", 0),
            most_recent_view=bucket.get("latest_timestamp", {}).get("value", 0),
        )

    def _map_bucket_to_asset_view(self, bucket) -> AssetViews:
        """
        Maps a bucket from the API response to a search log UniqueUsers instance.
        """
        # Handle the case where the bucket is empty or not a dictionary
        if not bucket or not isinstance(bucket, dict):
            return None

        return AssetViews(
            guid=bucket.get("key", ""),
            total_views=bucket.get("doc_count", 0),
            distinct_users=bucket.get(UNIQUE_USERS, {}).get("value", 0),
        )

    def search(self, criteria: SearchLogRequest) -> dict:
        """
        Search for assets using the provided criteria.

        :param criteria: detailing the search query, parameters, and so on to run
        :returns: the results of the search
        :raises AtlanError: on any API communication issue
        """
        user_views = []
        asset_views = []
        raw_json = self._client._call_api(
            SEARCH_LOG,
            request_obj=criteria,
        )
        if "aggregations" in raw_json and UNIQUE_USERS in raw_json.get(
            "aggregations", {}
        ):
            try:
                user_views_bucket = raw_json["aggregations"][UNIQUE_USERS].get(
                    "buckets", []
                )
                user_views = parse_obj_as(
                    list[UserViews],
                    [
                        self._map_bucket_to_user_view(user_view)
                        for user_view in user_views_bucket
                    ],
                )
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
            self._get_aggregations(raw_json)
            count = (
                raw_json["approximateCount"] if "approximateCount" in raw_json else 0
            )
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
                    list[AssetViews],
                    [
                        self._map_bucket_to_asset_view(asset_view)
                        for asset_view in asset_views_bucket
                    ],
                )
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
            self._get_aggregations(raw_json)
            count = (
                raw_json["approximateCount"] if "approximateCount" in raw_json else 0
            )
            return SearchLogViewResults(
                count=count,
                asset_views=asset_views,
            )
        # for recent search logs
        if "logs" in raw_json:
            try:
                log_enties = parse_obj_as(list[SearchLogEntry], raw_json["logs"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
            count = (
                raw_json["approximateCount"] if "approximateCount" in raw_json else 0
            )
            return SearchLogResults(
                client=self._client,
                criteria=criteria,
                start=criteria.dsl.from_,
                size=criteria.dsl.size,
                count=count,
                log_enties=log_enties,
                aggregations=None,
            )
