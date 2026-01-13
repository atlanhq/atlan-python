# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, Dict, List, Optional

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject
from pyatlan.model.oauth_client import OAuthClientResponse

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient
    from pyatlan.client.constants import API


class AsyncOAuthClientListResponse(AtlanObject):
    """Async version of OAuthClientListResponse with async pagination support."""

    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: AsyncAtlanClient = PrivateAttr()
    _sort: Optional[str] = PrivateAttr()

    total_record: Optional[int] = Field(
        default=None, description="Total number of OAuth clients."
    )
    filter_record: Optional[int] = Field(
        default=None,
        description="Number of OAuth clients that matched the specified filters.",
    )
    records: Optional[List[OAuthClientResponse]] = Field(
        default=None, description="List of OAuth clients."
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._endpoint = data.get("endpoint")  # type: ignore[assignment]
        self._client = data.get("client")  # type: ignore[assignment]
        self._size = data.get("size") or 20  # type: ignore[assignment]
        self._start = data.get("start") or 0  # type: ignore[assignment]
        self._sort = data.get("sort")  # type: ignore[assignment]

    def current_page(self) -> Optional[List[OAuthClientResponse]]:
        """Get the current page of OAuth clients."""
        return self.records

    async def next_page(
        self, start: Optional[int] = None, size: Optional[int] = None
    ) -> bool:
        """
        Retrieve the next page of results.

        :param start: starting point for the next page
        :param size: page size for the next page
        :returns: True if there was a next page, False otherwise
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self.records else False

    async def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        query_params: Dict[str, str] = {
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
            self.records = parse_obj_as(
                List[OAuthClientResponse], raw_json.get("records")
            )
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    async def __aiter__(self) -> AsyncGenerator[OAuthClientResponse, None]:
        """Async iterator for OAuth clients across all pages."""
        while self.records:
            for oauth_client in self.records:
                yield oauth_client
            if not await self.next_page():
                break
