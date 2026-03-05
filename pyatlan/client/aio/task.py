# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from pydantic.v1 import validate_arguments

from pyatlan.client.common import AsyncApiCaller, TaskSearch
from pyatlan.errors import ErrorCode
from pyatlan.model.aio.task import AsyncTaskSearchResponse
from pyatlan.model.task import TaskSearchRequest


class AsyncTaskClient:
    """
    Async client for operating on tasks.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def search(self, request: TaskSearchRequest) -> AsyncTaskSearchResponse:
        """
        Search for tasks using the provided criteria.

        :param request: search request for tasks
        :returns: search results for tasks
        """
        endpoint, request_obj = TaskSearch.prepare_request(request)
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        response_data = TaskSearch.process_response(raw_json)

        return AsyncTaskSearchResponse(
            client=self._client,
            endpoint=endpoint,
            criteria=request,
            start=request.dsl.from_,
            size=request.dsl.size,
            count=response_data["count"],
            tasks=response_data["tasks"],
            aggregations=response_data["aggregations"],
        )
