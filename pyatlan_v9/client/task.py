# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import List

import msgspec

from pyatlan.client.common import ApiCaller, TaskSearch
from pyatlan.errors import ErrorCode
from pyatlan.validate import validate_arguments
from pyatlan_v9.model.task import AtlanTask, TaskSearchRequest, TaskSearchResponse


def _parse_tasks(raw_json: dict) -> List[AtlanTask]:
    """Parse tasks from the raw API response using msgspec."""
    tasks = raw_json.get("tasks", [])
    if tasks:
        return msgspec.convert(tasks, list[AtlanTask], strict=False)
    return []


class V9TaskClient:
    """
    A client for operating on tasks.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def search(self, request: TaskSearchRequest) -> TaskSearchResponse:
        """
        Search for tasks using the provided criteria.

        :param request: search request for tasks
        :returns: search results for tasks
        """
        endpoint, request_obj = TaskSearch.prepare_request(request)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        count = raw_json.get("approximateCount", 0)
        aggregations = raw_json.get("aggregations")
        tasks = _parse_tasks(raw_json)

        return TaskSearchResponse(
            client=self._client,
            endpoint=endpoint,
            criteria=request,
            start=request.dsl.from_,
            size=request.dsl.size,
            count=count,
            tasks=tasks,
            aggregations=aggregations,
        )
