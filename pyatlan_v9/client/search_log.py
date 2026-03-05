# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import List, Union

import msgspec

from pyatlan.client.common import ApiCaller, SearchLogSearch
from pyatlan.errors import ErrorCode
from pyatlan_v9.model.search_log import (
    AssetViews,
    SearchLogEntry,
    SearchLogRequest,
    SearchLogResults,
    SearchLogViewResults,
    UserViews,
)
from pyatlan_v9.validate import validate_arguments

UNIQUE_USERS = "uniqueUsers"
UNIQUE_ASSETS = "uniqueAssets"


_MS_TIMESTAMP_THRESHOLD = 1e12
_LOG_TS_FIELDS = ("createdAt", "timestamp")


def _normalize_ms_timestamp(val):
    """Convert a millisecond epoch timestamp to seconds for msgspec datetime parsing."""
    if isinstance(val, (int, float)) and val > _MS_TIMESTAMP_THRESHOLD:
        return val / 1000
    return val


def _parse_user_views(raw_json: dict) -> List[UserViews]:
    """Parse user views from aggregation buckets using msgspec."""
    buckets = raw_json.get("aggregations", {}).get(UNIQUE_USERS, {}).get("buckets", [])
    mapped = [
        {
            "username": b.get("key", ""),
            "view_count": b.get("doc_count", 0),
            "most_recent_view": _normalize_ms_timestamp(
                b.get("latest_timestamp", {}).get("value", 0)
            ),
        }
        for b in buckets
        if b and isinstance(b, dict)
    ]
    return msgspec.convert(mapped, list[UserViews], strict=False)


def _parse_asset_views(raw_json: dict) -> List[AssetViews]:
    """Parse asset views from aggregation buckets using msgspec."""
    buckets = raw_json.get("aggregations", {}).get(UNIQUE_ASSETS, {}).get("buckets", [])
    mapped = [
        {
            "guid": b.get("key", ""),
            "total_views": b.get("doc_count", 0),
            "distinct_users": b.get(UNIQUE_USERS, {}).get("value", 0),
        }
        for b in buckets
        if b and isinstance(b, dict)
    ]
    return msgspec.convert(mapped, list[AssetViews], strict=False)


def _normalize_ms_timestamps_copy(record: dict, fields: tuple) -> dict:
    """Return a shallow copy with millisecond epoch timestamps converted to seconds."""
    out = dict(record)
    for field in fields:
        val = out.get(field)
        if isinstance(val, (int, float)) and val > _MS_TIMESTAMP_THRESHOLD:
            out[field] = val / 1000
    return out


def _parse_log_entries(raw_json: dict) -> List[SearchLogEntry]:
    """Parse log entries from raw JSON response using msgspec."""
    logs = raw_json.get("logs", [])
    if logs:
        normalized = [_normalize_ms_timestamps_copy(e, _LOG_TS_FIELDS) for e in logs]
        return msgspec.convert(normalized, list[SearchLogEntry], strict=False)
    return []


class V9SearchLogClient:
    """
    This class can be used to configure and run a search against Atlan's search log.
    This class does not need to be instantiated directly but can be obtained
    through the search_log property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def search(
        self, criteria: SearchLogRequest, bulk=False
    ) -> Union[SearchLogViewResults, SearchLogResults]:
        """
        Search for search logs using the provided criteria.
        `Note:` if the number of results exceeds the predefined threshold
        (10,000 search logs) this will be automatically converted into an search log `bulk` search.

        :param criteria: detailing the search query, parameters, and so on to run
        :param bulk: whether to run the search to retrieve search logs that match the supplied criteria,
        for large numbers of results (> `10,000`), defaults to `False`. Note: this will reorder the results
        (based on creation timestamp) in order to iterate through a large number (more than `10,000`) results.
        :raises InvalidRequestError:

            - if search log bulk search is enabled (`bulk=True`) and any
              user-specified sorting options are found in the search request.
            - if search log bulk search is disabled (`bulk=False`) and the number of results
              exceeds the predefined threshold (i.e: `10,000` assets)
              and any user-specified sorting options are found in the search request.

        :raises AtlanError: on any API communication issue
        :returns: the results of the search
        """
        endpoint, request_obj = SearchLogSearch.prepare_request(criteria, bulk)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)

        count = raw_json.get("approximateCount", 0)
        aggregations = raw_json.get("aggregations", {})

        if aggregations and UNIQUE_USERS in aggregations:
            user_views = _parse_user_views(raw_json)
            return SearchLogViewResults(count=count, user_views=user_views)

        if aggregations and UNIQUE_ASSETS in aggregations:
            asset_views = _parse_asset_views(raw_json)
            return SearchLogViewResults(count=count, asset_views=asset_views)

        log_entries = _parse_log_entries(raw_json)
        results = SearchLogResults(
            client=self._client,
            criteria=criteria,
            start=criteria.dsl.from_,
            size=criteria.dsl.size,
            count=count,
            log_entries=log_entries,
            aggregations=aggregations,
            bulk=bulk,
            processed_log_entries_count=len(log_entries),
        )

        if SearchLogSearch.check_for_bulk_search(
            results.count, criteria, bulk, SearchLogResults
        ):
            return self.search(criteria)

        return results
