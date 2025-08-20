# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from pydantic.v1 import validate_arguments

from pyatlan.client.common import AsyncApiCaller, QueryStream
from pyatlan.errors import ErrorCode
from pyatlan.model.query import QueryRequest, QueryResponse


class AsyncQueryClient:
    """
    Async client for running SQL queries.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def stream(self, request: QueryRequest) -> QueryResponse:
        """
        Runs the provided query and returns its results.

        :param: request query to run.
        :returns: results of the query.
        :raises : AtlanError on any issues with API communication.
        """
        # Prepare request using shared logic
        endpoint, request_obj = QueryStream.prepare_request(request)

        # Execute async API call
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)

        # Process response using shared logic
        return QueryStream.process_response(raw_json)
