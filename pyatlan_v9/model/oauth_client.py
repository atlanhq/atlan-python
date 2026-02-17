# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Generator, Union

import msgspec

from pyatlan.errors import ErrorCode


class OAuthClientRequest(msgspec.Struct, kw_only=True):
    """Request object for creating an OAuth client."""

    display_name: str
    """Human-readable name for the OAuth client."""
    description: Union[str, None] = None
    """Explanation of the OAuth client."""
    role: str
    """Role assigned to the OAuth client (e.g., '$admin', '$member')."""
    persona_qualified_names: Union[list[str], None] = msgspec.field(
        default=None, name="personaQNs"
    )
    """Qualified names of personas to associate with the OAuth client."""


class OAuthClientCreateResponse(msgspec.Struct, kw_only=True):
    """Response object returned when creating an OAuth client (includes client secret)."""

    id: Union[str, None] = None
    """Unique identifier (GUID) of the OAuth client."""
    client_id: Union[str, None] = None
    """Unique client identifier of the OAuth client."""
    client_secret: Union[str, None] = None
    """Client secret for the OAuth client (only returned on creation)."""
    display_name: Union[str, None] = None
    """Human-readable name provided when creating the OAuth client."""
    description: Union[str, None] = None
    """Explanation of the OAuth client."""
    token_expiry_seconds: Union[int, None] = None
    """Time in seconds after which the token will expire."""
    created_at: Union[str, None] = None
    """Epoch time, in milliseconds, at which the OAuth client was created."""
    created_by: Union[str, None] = None
    """User who created the OAuth client."""


class OAuthClientResponse(msgspec.Struct, kw_only=True):
    """Represents an OAuth client credential in Atlan."""

    id: Union[str, None] = None
    """Unique identifier (GUID) of the OAuth client."""
    client_id: Union[str, None] = None
    """Unique client identifier of the OAuth client."""
    display_name: Union[str, None] = None
    """Human-readable name provided when creating the OAuth client."""
    description: Union[str, None] = None
    """Explanation of the OAuth client."""
    role: Union[str, None] = None
    """Role assigned to the OAuth client (e.g., '$admin')."""
    persona_qualified_names: Union[list[str], None] = msgspec.field(
        default=None, name="personaQNs"
    )
    """Qualified names of personas associated with the OAuth client."""
    token_expiry_seconds: Union[int, None] = None
    """Time in seconds after which the token will expire."""
    created_at: Union[str, None] = None
    """Epoch time, in milliseconds, at which the OAuth client was created."""
    created_by: Union[str, None] = None
    """User who created the OAuth client."""
    updated_at: Union[str, None] = None
    """Epoch time, in milliseconds, at which the OAuth client was last updated."""
    updated_by: Union[str, None] = None
    """User who last updated the OAuth client."""


class OAuthClientListResponse(msgspec.Struct, kw_only=True):
    """Response object containing a list of OAuth clients with pagination info."""

    total_record: Union[int, None] = None
    """Total number of OAuth clients."""
    filter_record: Union[int, None] = None
    """Number of OAuth clients that matched the specified filters."""
    records: Union[list[OAuthClientResponse], None] = None
    """List of OAuth clients."""

    # Pagination state (not from JSON — set after construction)
    _size: int = 20
    _start: int = 0
    _endpoint: Any = None
    _client: Any = None
    _sort: Any = None

    def current_page(self) -> Union[list[OAuthClientResponse], None]:
        """Get the current page of OAuth clients."""
        return self.records

    def next_page(
        self, start: Union[int, None] = None, size: Union[int, None] = None
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
        return self._get_next_page() if self.records else False

    def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        query_params: dict[str, str] = {
            "count": "true",
            "offset": str(self._start),
            "limit": str(self._size),
        }
        if self._sort is not None:
            query_params["sort"] = self._sort
        raw_json = self._client._call_api(
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

    def __iter__(self) -> Generator[OAuthClientResponse, None, None]:  # type: ignore[override]
        """Iterate over all OAuth clients across all pages."""
        while True:
            yield from self.current_page() or []
            if not self.next_page():
                break
