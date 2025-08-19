# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from typing import Any

from pyatlan.client.constants import API, RUN_QUERY
from pyatlan.model.query import QueryRequest, QueryResponse


class QueryStream:
    """Shared logic for streaming query operations."""

    @staticmethod
    def prepare_request(request: QueryRequest) -> tuple[API, QueryRequest]:
        """
        Prepare the request for streaming query execution.

        :param request: the query request to execute
        :returns: tuple of (api_endpoint, request_object)
        """
        return RUN_QUERY, request

    @staticmethod
    def process_response(raw_json: Any) -> QueryResponse:
        """
        Process the raw API response into a QueryResponse.

        :param raw_json: raw API response
        :returns: QueryResponse with query results
        """
        return QueryResponse(events=raw_json)
