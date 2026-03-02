# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, AsyncGenerator, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan_v9.model.group import AtlanGroup


class AsyncGroupResponse(msgspec.Struct, kw_only=True, rename="camel"):
    """Async version of GroupResponse with async pagination support."""

    total_record: Union[int, None] = None
    """Total number of groups."""
    filter_record: Union[int, None] = None
    """Number of groups in the filtered response."""
    records: Union[list[AtlanGroup], None] = msgspec.field(default_factory=list)
    """Details of each group included in the response."""

    _size: int = 20
    _start: int = 0
    _endpoint: Any = None
    _client: Any = None
    _criteria: Any = None

    def current_page(self) -> list[AtlanGroup]:
        """Return the current page of group results."""
        return self.records or []

    async def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self.records else False

    async def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
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
            self.records = msgspec.convert(
                raw_json.get("records"), list[AtlanGroup], strict=False
            )
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    async def __aiter__(self) -> AsyncGenerator[AtlanGroup, None]:
        """Async iterator for groups across all pages."""
        while self.records:
            for group in self.records:
                yield group
            if not await self.next_page():
                break
