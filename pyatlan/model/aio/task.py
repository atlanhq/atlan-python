# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, AsyncGenerator, Dict, List

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.errors import ErrorCode
from pyatlan.model.aggregation import Aggregation
from pyatlan.model.task import AtlanTask, TaskSearchRequest
from pyatlan.utils import API

if TYPE_CHECKING:
    from pyatlan.client.constants import API
    from pyatlan.client.protocol import AsyncApiCaller


class AsyncTaskSearchResponse:
    """Async version of TaskSearchResponse with async pagination support."""

    def __init__(
        self,
        client: AsyncApiCaller,
        endpoint: API,
        criteria: TaskSearchRequest,
        start: int,
        size: int,
        count: int,
        tasks: List[AtlanTask],
        aggregations: Dict[str, Aggregation],
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
        """Get the total count of tasks."""
        return self._count

    def current_page(self) -> List[AtlanTask]:
        """Get the current page of tasks."""
        return self._tasks

    async def next_page(self, start=None, size=None) -> bool:
        """
        Retrieve the next page of results.

        :param start: starting point for the next page
        :param size: page size for the next page
        :returns: True if there was a next page, False otherwise
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._tasks else False

    async def _get_next_page(self) -> bool:
        """
        Fetches the next page of results.

        :returns: True if the next page of results was fetched, False if there was no next page
        """
        self._criteria.dsl.from_ = self._start
        self._criteria.dsl.size = self._size
        if raw_json := await self._get_next_page_json():
            self._count = raw_json.get("approximateCount", 0)
            return True
        return False

    async def _get_next_page_json(self):
        """
        Fetches the next page of results and returns the raw JSON of the retrieval.

        :returns: JSON for the next page of results, as-is
        """
        raw_json = await self._client._call_api(
            self._endpoint,
            request_obj=self._criteria,
        )
        if "tasks" not in raw_json or not raw_json["tasks"]:
            self._tasks = []
            return None
        try:
            self._tasks = parse_obj_as(List[AtlanTask], raw_json["tasks"])
            return raw_json
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    async def __aiter__(self) -> AsyncGenerator[AtlanTask, None]:
        """Async iterator for tasks across all pages."""
        while self._tasks:
            for task in self._tasks:
                yield task
            if not await self.next_page():
                break
