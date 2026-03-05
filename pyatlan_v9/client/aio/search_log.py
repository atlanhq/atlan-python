# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Union

from pyatlan.client.common import AsyncApiCaller, SearchLogSearch
from pyatlan.errors import ErrorCode
from pyatlan_v9.client.search_log import (
    UNIQUE_ASSETS,
    UNIQUE_USERS,
    _parse_asset_views,
    _parse_log_entries,
    _parse_user_views,
)
from pyatlan_v9.model.aio.search_log import AsyncSearchLogResults
from pyatlan_v9.model.search_log import SearchLogRequest, SearchLogViewResults
from pyatlan_v9.validate import validate_arguments


class V9AsyncSearchLogClient:
    """
    Async client for configuring and running searches against Atlan's search log.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def search(
        self, criteria: SearchLogRequest, bulk=False
    ) -> Union[SearchLogViewResults, AsyncSearchLogResults]:
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
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)

        count = raw_json.get("approximateCount", 0)
        aggregations = raw_json.get("aggregations", {})

        if aggregations and UNIQUE_USERS in aggregations:
            user_views = _parse_user_views(raw_json)
            return SearchLogViewResults(count=count, user_views=user_views)

        if aggregations and UNIQUE_ASSETS in aggregations:
            asset_views = _parse_asset_views(raw_json)
            return SearchLogViewResults(count=count, asset_views=asset_views)

        log_entries = _parse_log_entries(raw_json)
        results = AsyncSearchLogResults(
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
            results.count, criteria, bulk, AsyncSearchLogResults
        ):
            return await self.search(criteria)

        return results
