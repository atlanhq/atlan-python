# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, AsyncGenerator, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan_v9.model.workflow import (
    WorkflowSearchHits,
    WorkflowSearchRequest,
    WorkflowSearchResult,
)


class AsyncWorkflowSearchResponse(msgspec.Struct, kw_only=True, rename="camel"):
    """Async version of WorkflowSearchResponse with async pagination support."""

    took: Union[int, None] = None
    hits: Union[WorkflowSearchHits, None] = None
    shards: Union[dict[str, Any], None] = msgspec.field(default=None, name="_shards")

    _size: int = 10
    _start: int = 0
    _endpoint: Any = None
    _client: Any = None
    _criteria: Any = None

    @property
    def count(self) -> int:
        """Total count of workflow search results."""
        return self.hits.total.get("value", 0) if self.hits and self.hits.total else 0

    def current_page(self) -> Union[list[WorkflowSearchResult], None]:
        """Return the current page of results."""
        return self.hits.hits if self.hits else None

    async def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        if self.hits and self.hits.hits:
            return await self._get_next_page()
        return False

    async def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        request = WorkflowSearchRequest(
            query=self._criteria, from_=self._start, size=self._size
        )
        raw_json = await self._client._call_api(
            api=self._endpoint,
            request_obj=request,
        )
        if not raw_json.get("hits", {}).get("hits"):
            if self.hits:
                self.hits.hits = []
            return False
        try:
            if self.hits:
                self.hits.hits = msgspec.convert(
                    raw_json["hits"]["hits"],
                    list[WorkflowSearchResult],
                    strict=False,
                )
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    async def __aiter__(self) -> AsyncGenerator[WorkflowSearchResult, None]:
        """Iterate through all pages of results."""
        while True:
            for item in self.current_page() or []:
                yield item
            if not await self.next_page():
                break
