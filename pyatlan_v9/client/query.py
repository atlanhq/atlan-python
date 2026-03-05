# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from pyatlan.client.common import ApiCaller, QueryStream
from pyatlan.errors import ErrorCode
from pyatlan_v9.model.query import QueryRequest, QueryResponse
from pyatlan_v9.validate import validate_arguments


class V9QueryClient:
    """
    A client for running SQL queries.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def stream(self, request: QueryRequest) -> QueryResponse:
        """
        Runs the provided query and returns its results.

        :param: request query to run.
        :returns: results of the query.
        :raises : AtlanError on any issues with API communication.
        """
        endpoint, request_obj = QueryStream.prepare_request(request)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return QueryResponse(events=raw_json)
