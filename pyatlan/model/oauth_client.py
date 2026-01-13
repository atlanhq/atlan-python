# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, Generator, List, Optional

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject

if TYPE_CHECKING:
    from pyatlan.client.protocol import ApiCaller
    from pyatlan.utils import API


class OAuthClientRequest(AtlanObject):
    """Request object for creating an OAuth client."""

    display_name: str = Field(
        description="Human-readable name for the OAuth client.",
    )
    description: Optional[str] = Field(
        default=None,
        description="Explanation of the OAuth client.",
    )
    role: str = Field(
        description="Role assigned to the OAuth client (e.g., '$admin', '$member').",
    )
    persona_qualified_names: Optional[List[str]] = Field(
        default=None,
        description="Qualified names of personas to associate with the OAuth client.",
        alias="personaQNs",
    )


class OAuthClientCreateResponse(AtlanObject):
    """Response object returned when creating an OAuth client (includes client secret)."""

    id: Optional[str] = Field(
        default=None,
        description="Unique identifier (GUID) of the OAuth client.",
    )
    client_id: Optional[str] = Field(
        default=None,
        description="Unique client identifier of the OAuth client.",
    )
    client_secret: Optional[str] = Field(
        default=None,
        description="Client secret for the OAuth client (only returned on creation).",
    )
    display_name: Optional[str] = Field(
        default=None,
        description="Human-readable name provided when creating the OAuth client.",
    )
    description: Optional[str] = Field(
        default=None,
        description="Explanation of the OAuth client.",
    )
    token_expiry_seconds: Optional[int] = Field(
        default=None,
        description="Time in seconds after which the token will expire.",
    )
    created_at: Optional[str] = Field(
        default=None,
        description="Epoch time, in milliseconds, at which the OAuth client was created.",
    )
    created_by: Optional[str] = Field(
        default=None,
        description="User who created the OAuth client.",
    )


class OAuthClientResponse(AtlanObject):
    """Represents an OAuth client credential in Atlan."""

    id: Optional[str] = Field(
        default=None,
        description="Unique identifier (GUID) of the OAuth client.",
    )
    client_id: Optional[str] = Field(
        default=None,
        description="Unique client identifier of the OAuth client.",
    )
    display_name: Optional[str] = Field(
        default=None,
        description="Human-readable name provided when creating the OAuth client.",
    )
    description: Optional[str] = Field(
        default=None,
        description="Explanation of the OAuth client.",
    )
    role: Optional[str] = Field(
        default=None,
        description="Role assigned to the OAuth client (e.g., '$admin').",
    )
    persona_qualified_names: Optional[List[str]] = Field(
        default=None,
        description="Qualified names of personas associated with the OAuth client.",
        alias="personaQNs",
    )
    token_expiry_seconds: Optional[int] = Field(
        default=None,
        description="Time in seconds after which the token will expire.",
    )
    created_at: Optional[str] = Field(
        default=None,
        description="Epoch time, in milliseconds, at which the OAuth client was created.",
    )
    created_by: Optional[str] = Field(
        default=None,
        description="User who created the OAuth client.",
    )
    updated_at: Optional[str] = Field(
        default=None,
        description="Epoch time, in milliseconds, at which the OAuth client was last updated.",
    )
    updated_by: Optional[str] = Field(
        default=None,
        description="User who last updated the OAuth client.",
    )


class OAuthClientListResponse(AtlanObject):
    """Response object containing a list of OAuth clients with pagination info."""

    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: ApiCaller = PrivateAttr()
    _sort: Optional[str] = PrivateAttr()

    total_record: Optional[int] = Field(
        default=None,
        description="Total number of OAuth clients.",
    )
    filter_record: Optional[int] = Field(
        default=None,
        description="Number of OAuth clients that matched the specified filters.",
    )
    records: Optional[List[OAuthClientResponse]] = Field(
        default=None,
        description="List of OAuth clients.",
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

    def next_page(
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
        return self._get_next_page() if self.records else False

    def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        query_params: Dict[str, str] = {
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
            self.records = parse_obj_as(
                List[OAuthClientResponse], raw_json.get("records")
            )
        except ValidationError as err:
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
