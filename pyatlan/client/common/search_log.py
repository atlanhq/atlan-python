# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

import logging
from typing import Any, List, Union

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import SEARCH_LOG
from pyatlan.errors import ErrorCode
from pyatlan.model.search import SortItem
from pyatlan.model.search_log import (
    AssetViews,
    SearchLogEntry,
    SearchLogRequest,
    SearchLogResults,
    SearchLogViewResults,
    UserViews,
)
from pyatlan.utils import API

UNIQUE_USERS = "uniqueUsers"
UNIQUE_ASSETS = "uniqueAssets"
LOGGER = logging.getLogger(__name__)


class SearchLogSearch:
    """Shared logic for search log operations."""

    @staticmethod
    def prepare_request(
        criteria: SearchLogRequest, bulk: bool = False
    ) -> tuple[API, SearchLogRequest]:
        """
        Prepare the request for search log search.

        :param criteria: detailing the search query, parameters, and so on to run
        :param bulk: whether to run the search as bulk search
        :returns: tuple of (api_endpoint, prepared_criteria)
        """
        if bulk:
            if criteria.dsl.sort and len(criteria.dsl.sort) > 2:
                raise ErrorCode.UNABLE_TO_RUN_SEARCH_LOG_BULK_WITH_SORTS.exception_with_parameters()
            criteria.dsl.sort = SearchLogSearch.prepare_sorts_for_bulk_search(
                criteria.dsl.sort
            )
            LOGGER.debug(SearchLogSearch.get_bulk_search_log_message(bulk))

        return SEARCH_LOG, criteria

    @staticmethod
    def process_response(
        raw_json: Any,
        criteria: SearchLogRequest,
        bulk: bool = False,
        client: Any = None,
    ) -> Union[SearchLogViewResults, SearchLogResults, Any]:
        """
        Process the raw API response into search log results.

        :param raw_json: raw API response
        :param criteria: original search criteria
        :param bulk: whether this was a bulk search
        :param client: client instance for SearchLogResults
        :returns: SearchLogViewResults or SearchLogResults
        """
        count = SearchLogSearch.get_total_count(raw_json)
        aggregations = raw_json.get("aggregations", {})

        # Check for user views aggregation
        if aggregations and UNIQUE_USERS in aggregations:
            user_views = SearchLogSearch.parse_user_views(raw_json)
            return SearchLogViewResults(
                count=count,
                user_views=user_views,
            )

        # Check for asset views aggregation
        if aggregations and UNIQUE_ASSETS in aggregations:
            asset_views = SearchLogSearch.parse_asset_views(raw_json)
            return SearchLogViewResults(
                count=count,
                asset_views=asset_views,
            )

        # Process log entries
        log_entries = SearchLogSearch.parse_log_entries(raw_json)

        # Check if we need async results
        if hasattr(client, "_async_session"):
            # This is an async client, return async results
            from pyatlan.model.aio.search_log import AsyncSearchLogResults

            return AsyncSearchLogResults(
                client=client,
                criteria=criteria,
                start=criteria.dsl.from_,
                size=criteria.dsl.size,
                log_entries=log_entries,
                count=count,
                aggregations=aggregations,
                bulk=bulk,
                processed_log_entries_count=len(log_entries),
            )
        else:
            # This is a sync client, return sync results
            from pyatlan.model.search_log import SearchLogResults

            return SearchLogResults(
                client=client,
                criteria=criteria,
                start=criteria.dsl.from_,
                size=criteria.dsl.size,
                count=count,
                log_entries=log_entries,
                aggregations=aggregations,
                bulk=bulk,
                processed_log_entries_count=len(log_entries),
            )

    @staticmethod
    def check_for_bulk_search(
        count: int,
        criteria: SearchLogRequest,
        bulk: bool = False,
        search_results_class=None,
    ) -> bool:
        """
        Check if the search should be converted to bulk search based on result count.

        :param count: total number of results
        :param criteria: the search log criteria
        :param bulk: whether bulk search is already enabled
        :param search_results_class: the search results class to use for thresholds
        :returns: True if conversion to bulk search is needed
        """
        # Use provided search results class or default to sync version
        if search_results_class is None:
            # Import here to avoid circular import
            from pyatlan.model.search_log import SearchLogResults

            search_results_class = SearchLogResults

        if bulk:
            return False

        if (
            count > search_results_class._MASS_EXTRACT_THRESHOLD
            and not search_results_class.presorted_by_timestamp(criteria.dsl.sort)
        ):
            if criteria.dsl.sort and len(criteria.dsl.sort) > 2:
                raise ErrorCode.UNABLE_TO_RUN_SEARCH_LOG_BULK_WITH_SORTS.exception_with_parameters()
            # Update criteria for bulk search
            criteria.dsl.sort = SearchLogSearch.prepare_sorts_for_bulk_search(
                criteria.dsl.sort, search_results_class
            )
            LOGGER.debug(
                SearchLogSearch.get_bulk_search_log_message(False),
                count,
                search_results_class._MASS_EXTRACT_THRESHOLD,
            )
            return True
        return False

    @staticmethod
    def parse_user_views(raw_json: dict) -> List[UserViews]:
        """Parse user views from API response."""
        try:
            user_views_bucket = raw_json["aggregations"][UNIQUE_USERS].get(
                "buckets", []
            )
            return parse_obj_as(
                List[UserViews],
                [
                    SearchLogSearch.map_bucket_to_user_view(user_view)
                    for user_view in user_views_bucket
                ],
            )
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    @staticmethod
    def parse_asset_views(raw_json: dict) -> List[AssetViews]:
        """Parse asset views from API response."""
        try:
            asset_views_bucket = raw_json["aggregations"][UNIQUE_ASSETS].get(
                "buckets", []
            )
            return parse_obj_as(
                List[AssetViews],
                [
                    SearchLogSearch.map_bucket_to_asset_view(asset_view)
                    for asset_view in asset_views_bucket
                ],
            )
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    @staticmethod
    def parse_log_entries(raw_json: dict) -> List[SearchLogEntry]:
        """Parse log entries from API response."""
        if "logs" in raw_json and raw_json.get("logs", []):
            try:
                return parse_obj_as(List[SearchLogEntry], raw_json["logs"])
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        return []

    @staticmethod
    def map_bucket_to_user_view(bucket) -> Union[UserViews, None]:
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

    @staticmethod
    def map_bucket_to_asset_view(bucket) -> Union[AssetViews, None]:
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

    @staticmethod
    def prepare_sorts_for_bulk_search(
        sorts: List[SortItem], search_results_class=None
    ) -> List[SortItem]:
        """
        Ensures that sorting by creation timestamp is prioritized for search log bulk searches.

        :param sorts: list of existing sorting options.
        :param search_results_class: the search results class to use for sorting logic
        :returns: a modified list of sorting options with creation timestamp as the top priority.
        """
        # Use provided search results class or default to sync version
        if search_results_class is None:
            # Import here to avoid circular import
            from pyatlan.model.search_log import SearchLogResults

            search_results_class = SearchLogResults

        if not search_results_class.presorted_by_timestamp(sorts):
            return search_results_class.sort_by_timestamp_first(sorts)
        return sorts

    @staticmethod
    def get_total_count(raw_json: dict) -> int:
        """
        Extract total count from search log response.

        :param raw_json: the raw JSON response from search log API
        :returns: total count of search log entries
        """
        return raw_json.get("approximateCount", 0)

    @staticmethod
    def get_bulk_search_log_message(bulk: bool) -> str:
        """Get the bulk search log message."""
        return (
            (
                "Search log bulk search option is enabled. "
                if bulk
                else "Result size (%s) exceeds threshold (%s). "
            )
            + "Ignoring requests for offset-based paging and using timestamp-based paging instead."
        )
