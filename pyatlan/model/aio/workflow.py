# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, Dict, List, Optional

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject
from pyatlan.model.workflow import (
    WorkflowSearchHits,
    WorkflowSearchRequest,
    WorkflowSearchResult,
)
from pyatlan.utils import API

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient
    from pyatlan.client.constants import API


class AsyncWorkflowSearchResponse(AtlanObject):
    """Async version of WorkflowSearchResponse with async pagination support."""

    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: AsyncAtlanClient = PrivateAttr()
    _criteria: WorkflowSearchRequest = PrivateAttr()
    took: Optional[int] = Field(default=None)
    hits: Optional[WorkflowSearchHits] = Field(default=None)
    shards: Optional[Dict[str, Any]] = Field(alias="_shards", default=None)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._endpoint = data.get("endpoint")  # type: ignore[assignment]
        self._client = data.get("client")  # type: ignore[assignment]
        self._criteria = data.get("criteria")  # type: ignore[assignment]
        self._size = data.get("size")  # type: ignore[assignment]
        self._start = data.get("start")  # type: ignore[assignment]

    @property
    def count(self):
        """Get the total count of workflow results."""
        return self.hits.total.get("value", 0) if self.hits and self.hits.total else 0

    def current_page(self) -> Optional[List[WorkflowSearchResult]]:
        """Get the current page of workflow results."""
        return self.hits.hits if self.hits else None

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
        return await self._get_next_page() if self.hits and self.hits.hits else False

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
            if self.hits is not None:
                self.hits.hits = []
            return False
        try:
            if self.hits is not None:
                self.hits.hits = parse_obj_as(
                    List[WorkflowSearchResult], raw_json["hits"]["hits"]
                )
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    async def __aiter__(self) -> AsyncGenerator[WorkflowSearchResult, None]:
        """Async iterator for workflow results across all pages."""
        while self.hits and self.hits.hits:
            for result in self.hits.hits:
                yield result
            if not await self.next_page():
                break
