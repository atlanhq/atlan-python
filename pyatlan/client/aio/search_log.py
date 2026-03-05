# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Union, cast

from pydantic.v1 import validate_arguments

from pyatlan.client.common import AsyncApiCaller, SearchLogSearch
from pyatlan.errors import ErrorCode
from pyatlan.model.aio.search_log import AsyncSearchLogResults
from pyatlan.model.search_log import SearchLogRequest, SearchLogViewResults


class AsyncSearchLogClient:
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
        # Prepare request using shared logic
        endpoint, request_obj = SearchLogSearch.prepare_request(criteria, bulk)

        # Execute async API call
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)

        # Process response using shared logic (which returns the final results)
        results = SearchLogSearch.process_response(
            raw_json, criteria, bulk, self._client
        )
        # Cast to the expected union type since we know it's an async client
        results = cast(Union[SearchLogViewResults, AsyncSearchLogResults], results)

        # If it's AsyncSearchLogResults (not SearchLogViewResults), check for bulk search conversion
        if isinstance(results, AsyncSearchLogResults):
            if SearchLogSearch.check_for_bulk_search(
                results.count, criteria, bulk, AsyncSearchLogResults
            ):
                # Recursive async call with updated criteria
                return await self.search(criteria)

        return results
