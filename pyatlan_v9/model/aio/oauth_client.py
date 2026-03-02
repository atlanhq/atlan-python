# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, AsyncGenerator, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan_v9.model.oauth_client import OAuthClientResponse


class AsyncOAuthClientListResponse(msgspec.Struct, kw_only=True, rename="camel"):
    """Async version of OAuthClientListResponse with async pagination support."""

    total_record: Union[int, None] = None
    """Total number of OAuth clients."""
    filter_record: Union[int, None] = None
    """Number of OAuth clients that matched the specified filters."""
    records: Union[list[OAuthClientResponse], None] = None
    """List of OAuth clients."""

    _size: int = 20
    _start: int = 0
    _endpoint: Any = None
    _client: Any = None
    _sort: Any = None

    def current_page(self) -> list[OAuthClientResponse]:
        """Get the current page of OAuth clients."""
        return self.records or []

    async def next_page(
        self, start: Union[int, None] = None, size: Union[int, None] = None
    ) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self.records else False

    async def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        query_params: dict[str, str] = {
            "count": "true",
            "offset": str(self._start),
            "limit": str(self._size),
        }
        if self._sort is not None:
            query_params["sort"] = self._sort
        raw_json = await self._client._call_api(
            api=self._endpoint,
            query_params=query_params,
        )
        if not raw_json.get("records"):
            self.records = []
            return False
        try:
            self.records = msgspec.convert(
                raw_json.get("records"), list[OAuthClientResponse], strict=False
            )
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    async def __aiter__(self) -> AsyncGenerator[OAuthClientResponse, None]:
        """Async iterate over all OAuth clients across all pages."""
        while self.records:
            for record in self.records:
                yield record
            if not await self.next_page():
                break
