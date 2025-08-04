# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic.v1 import validate_arguments

from pyatlan.client.common import QueryStream
from pyatlan.model.query import QueryRequest, QueryResponse

if TYPE_CHECKING:
    from .client import AsyncAtlanClient


class AsyncQueryClient:
    """
    Async client for running SQL queries.
    """

    def __init__(self, client: AsyncAtlanClient):
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
