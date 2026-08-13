# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, List, Optional

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.errors import ErrorCode
from pyatlan.model.atlan_request import AtlanRequest, AtlanRequestsCriteria
from pyatlan.model.core import AtlanObject
from pyatlan.utils import API

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient


class AsyncAtlanRequestResponse(AtlanObject):
    """Async version of AtlanRequestResponse with async pagination support."""

    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: AsyncAtlanClient = PrivateAttr()
    _criteria: AtlanRequestsCriteria = PrivateAttr()
    total_record: Optional[int] = Field(
        default=None, description="Total number of requests."
    )
    filter_record: Optional[int] = Field(
        default=None, description="Number of requests matching the filter."
    )
    records: Optional[List[AtlanRequest]] = Field(
        default=None, description="Requests in this page of results."
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._endpoint = data.get("endpoint")  # type: ignore[assignment]
        self._client = data.get("client")  # type: ignore[assignment]
        self._criteria = data.get("criteria")  # type: ignore[assignment]
        self._start = data.get("start") or 0
        self._size = data.get("size") or 20

    def current_page(self) -> Optional[List[AtlanRequest]]:
        return self.records

    async def next_page(self, start=None, size=None) -> bool:
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self.records else False

    async def _get_next_page(self) -> bool:
        self._criteria.offset = self._start
        self._criteria.limit = self._size
        raw_json = await self._client._call_api(
            api=self._endpoint.format_path_with_params(),
            query_params=self._criteria.query_params,
        )
        if not raw_json.get("records"):
            self.records = []
            return False
        try:
            self.records = parse_obj_as(List[AtlanRequest], raw_json.get("records"))
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    async def __aiter__(self) -> AsyncGenerator[AtlanRequest, None]:  # type: ignore[misc]
        while self.records:
            for record in self.records:
                yield record
            if not await self.next_page():
                break
