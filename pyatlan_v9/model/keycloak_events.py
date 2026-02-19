# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Generator, Union

import msgspec

from pyatlan.client.constants import ADMIN_EVENTS, KEYCLOAK_EVENTS
from pyatlan.model.enums import AdminOperationType, AdminResourceType, KeycloakEventType


class AuthDetails(msgspec.Struct, kw_only=True):
    """Authentication details for an admin event."""

    client_id: Union[str, None] = None
    """Unique identifier (GUID) of the client that carried out the operation."""
    ip_address: Union[str, None] = None
    """IP address from which the operation was carried out."""
    realm_id: Union[str, None] = None
    """Unique name of the realm from which the operation was carried out."""
    user_id: Union[str, None] = None
    """Unique identifier (GUID) of the user who carried out the operation."""


class KeycloakEvent(msgspec.Struct, kw_only=True):
    """Keycloak login event."""

    client_id: Union[str, None] = None
    """Where the login occurred (usually 'atlan-frontend')."""
    details: Union[Any, None] = None
    ip_address: Union[str, None] = None
    """IP address from which the user logged in."""
    realm_id: Union[str, None] = None
    session_id: Union[str, None] = None
    """Unique identifier (GUID) of the session for the login."""
    time: Union[int, None] = None
    """Time (epoch) when the login occurred, in milliseconds."""
    type: Union[KeycloakEventType, None] = None
    """Type of login event that occurred (usually 'LOGIN')."""
    user_id: Union[str, None] = None
    """Unique identifier (GUID) of the user that logged in."""


class AdminEvent(msgspec.Struct, kw_only=True):
    """Admin operation event."""

    operation_type: Union[AdminOperationType, None] = None
    """Type of admin operation that occurred."""
    realm_id: Union[str, None] = None
    """Unique identifier of the realm in which the event occurred."""
    representation: Union[str, None] = None
    """Detailed resource that was created or changed."""
    resource_path: Union[str, None] = None
    """Location of the resource that was created or changed."""
    resource_type: Union[AdminResourceType, None] = None
    """Type of resource for the admin operation."""
    time: Union[int, None] = None
    """Time (epoch) when the admin operation occurred, in milliseconds."""
    auth_details: Union[AuthDetails, None] = None
    """Details of who carried out the operation."""


class KeycloakEventRequest(msgspec.Struct, kw_only=True):
    """Request parameters for listing Keycloak events."""

    client: Union[str, None] = None
    """Application or OAuth client name."""
    ip_address: Union[str, None] = None
    """IP address from which the event was triggered."""
    date_from: Union[str, None] = None
    """Earliest date from which to include events (format: yyyy-MM-dd)."""
    date_to: Union[str, None] = None
    """Latest date up to which to include events (format: yyyy-MM-dd)."""
    offset: Union[int, None] = None
    """Starting point for the events (for paging)."""
    size: Union[int, None] = None
    """Maximum number of events to retrieve (per page)."""
    types: Union[list[KeycloakEventType], None] = None
    """Include events only of the supplied types."""
    user_id: Union[str, None] = None
    """Unique identifier (GUID) of the user who triggered the event."""

    @property
    def query_params(self) -> dict:
        """Convert to query parameters dict."""
        d: dict[str, object] = {}
        if self.client:
            d["client"] = self.client
        if self.ip_address:
            d["ipAddress"] = self.ip_address
        if self.date_from:
            d["dateFrom"] = self.date_from
        if self.date_to:
            d["dateTo"] = self.date_to
        d["first"] = self.offset or 0
        d["max"] = self.size or 100
        if self.types:
            d["type"] = self.types
        if self.user_id:
            d["user"] = self.user_id
        return d


class KeycloakEventResponse:
    """Response with pagination for Keycloak events."""

    def __init__(
        self,
        client: Any,
        criteria: KeycloakEventRequest,
        start: int,
        size: int,
        events: list[KeycloakEvent],
    ):
        self._client = client
        self._criteria = criteria
        self._start = start
        self._size = size
        self._events = events

    def current_page(self) -> list[KeycloakEvent]:
        """Return the current page of events."""
        return self._events

    def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._events else False

    def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        self._criteria.offset = self._start
        self._criteria.size = self._size
        raw_json = self._client._call_api(
            KEYCLOAK_EVENTS,
            query_params=self._criteria.query_params,
        )
        if not raw_json:
            self._events = []
            return False
        self._events = msgspec.convert(raw_json, list[KeycloakEvent], strict=False)
        return True

    def __iter__(self) -> Generator[KeycloakEvent, None, None]:
        """Iterate through all pages of results."""
        while True:
            yield from self.current_page()
            if not self.next_page():
                break


class AdminEventRequest(msgspec.Struct, kw_only=True):
    """Request parameters for listing admin events."""

    client_id: Union[str, None] = None
    """Unique identifier (GUID) of the client."""
    ip_address: Union[str, None] = None
    """IP address from which the operation was carried out."""
    realm_id: Union[str, None] = None
    """Unique name of the realm."""
    user_id: Union[str, None] = None
    """Unique identifier (GUID) of the user."""
    date_from: Union[str, None] = None
    """Earliest date from which to include events (format: yyyy-MM-dd)."""
    date_to: Union[str, None] = None
    """Latest date up to which to include events (format: yyyy-MM-dd)."""
    offset: Union[int, None] = None
    """Starting point for the events (for paging)."""
    size: Union[int, None] = None
    """Maximum number of events to retrieve (per page)."""
    operation_types: Union[list[AdminOperationType], None] = None
    """Include events only with the supplied types of operations."""
    resource_path: Union[str, None] = None
    """Include events only against the supplied resource."""
    resource_types: Union[list[AdminResourceType], None] = None
    """Include events only against the supplied types of resources."""

    @property
    def query_params(self) -> dict:
        """Convert to query parameters dict."""
        d: dict[str, object] = {}
        if self.client_id:
            d["authClient"] = self.client_id
        if self.ip_address:
            d["authIpAddress"] = self.ip_address
        if self.realm_id:
            d["authRealm"] = self.realm_id
        if self.user_id:
            d["authUser"] = self.user_id
        if self.date_from:
            d["dateFrom"] = self.date_from
        if self.date_to:
            d["dateTo"] = self.date_to
        d["first"] = self.offset or 0
        d["max"] = self.size or 100
        if self.operation_types:
            d["operationTypes"] = self.operation_types
        if self.resource_path:
            d["resourcePath"] = self.resource_path
        if self.resource_types:
            d["resourceTypes"] = self.resource_types
        return d


class AdminEventResponse:
    """Response with pagination for admin events."""

    def __init__(
        self,
        client: Any,
        criteria: AdminEventRequest,
        start: int,
        size: int,
        events: list[AdminEvent],
    ):
        self._client = client
        self._criteria = criteria
        self._start = start
        self._size = size
        self._events = events

    def current_page(self) -> list[AdminEvent]:
        """Return the current page of events."""
        return self._events

    def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._events else False

    def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        self._criteria.offset = self._start
        self._criteria.size = self._size
        raw_json = self._client._call_api(
            ADMIN_EVENTS,
            query_params=self._criteria.query_params,
        )
        if not raw_json:
            self._events = []
            return False
        self._events = msgspec.convert(raw_json, list[AdminEvent], strict=False)
        return True

    def __iter__(self) -> Generator[AdminEvent, None, None]:
        """Iterate through all pages of results."""
        while True:
            yield from self.current_page()
            if not self.next_page():
                break
