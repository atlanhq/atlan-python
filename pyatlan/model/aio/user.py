# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, AsyncGenerator, List, Optional

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject
from pyatlan.model.user import AtlanUser, UserRequest

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient
    from pyatlan.client.constants import API


class AsyncUserResponse(AtlanObject):
    """Async version of UserResponse with async pagination support."""

    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: AsyncAtlanClient = PrivateAttr()
    _criteria: UserRequest = PrivateAttr()
    total_record: Optional[int] = Field(
        default=None, description="Total number of users."
    )
    filter_record: Optional[int] = Field(
        default=None,
        description="Number of users in the filtered response.",
    )
    records: Optional[List[AtlanUser]] = Field(
        default=None, description="Details of each user included in the response."
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._endpoint = data.get("endpoint")  # type: ignore[assignment]
        self._client = data.get("client")  # type: ignore[assignment]
        self._criteria = data.get("criteria")  # type: ignore[assignment]
        self._size = data.get("size")  # type: ignore[assignment]
        self._start = data.get("start")  # type: ignore[assignment]

    def current_page(self) -> Optional[List[AtlanUser]]:
        """Get the current page of users."""
        return self.records

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
            self.records = parse_obj_as(List[AtlanUser], raw_json.get("records"))
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    async def __aiter__(self) -> AsyncGenerator[AtlanUser, None]:
        """Async iterator for users across all pages."""
        while self.records:
            for user in self.records:
                yield user
            if not await self.next_page():
                break
