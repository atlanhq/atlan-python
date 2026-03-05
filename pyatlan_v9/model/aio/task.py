# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, AsyncGenerator, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan_v9.model.task import AtlanTask, TaskSearchRequest


class AsyncTaskSearchResponse:
    """Async version of TaskSearchResponse for paginated task results."""

    def __init__(
        self,
        client: Any,
        endpoint: Any,
        criteria: TaskSearchRequest,
        start: int,
        size: int,
        count: int,
        tasks: list[AtlanTask],
        aggregations: Any,
    ):
        self._client = client
        self._endpoint = endpoint
        self._criteria = criteria
        self._start = start
        self._size = size
        self._count = count
        self._tasks = tasks
        self._aggregations = aggregations

    @property
    def count(self) -> int:
        """Total count of matching tasks."""
        return self._count

    def current_page(self) -> list[AtlanTask]:
        """Retrieve the current page of results."""
        return self._tasks

    async def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._tasks else False

    async def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := await self._get_next_page_json():
            self._count = raw_json.get("approximateCount", 0)
            return True
        return False

    async def _get_next_page_json(self) -> Union[dict, None]:
        """Fetch the next page of results and return raw JSON."""
        raw_json = await self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "tasks" not in raw_json or not raw_json["tasks"]:
            self._tasks = []
            return None
        try:
            self._tasks = msgspec.convert(
                raw_json["tasks"], list[AtlanTask], strict=False
            )
            return raw_json
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    async def __aiter__(self) -> AsyncGenerator[AtlanTask, None]:
        """Iterate through all pages of results."""
        while True:
            for task in self.current_page():
                yield task
            if not await self.next_page():
                break
