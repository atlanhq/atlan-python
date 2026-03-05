# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import AsyncGenerator

import msgspec

from pyatlan.client.constants import ADMIN_EVENTS, KEYCLOAK_EVENTS
from pyatlan_v9.model.keycloak_events import (
    AdminEvent,
    AdminEventRequest,
    KeycloakEvent,
    KeycloakEventRequest,
)


class AsyncKeycloakEventResponse:
    """Async paginated response for Keycloak events."""

    def __init__(
        self,
        client,
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

    async def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._events else False

    async def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        self._criteria.offset = self._start
        self._criteria.size = self._size
        raw_json = await self._client._call_api(
            KEYCLOAK_EVENTS,
            query_params=self._criteria.query_params,
        )
        if not raw_json:
            self._events = []
            return False
        self._events = msgspec.convert(raw_json, list[KeycloakEvent], strict=False)
        return True

    async def __aiter__(self) -> AsyncGenerator[KeycloakEvent, None]:
        """Iterate through all pages of results."""
        while True:
            for event in self.current_page():
                yield event
            if not await self.next_page():
                break


class AsyncAdminEventResponse:
    """Async paginated response for admin events."""

    def __init__(
        self,
        client,
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

    async def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._events else False

    async def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        self._criteria.offset = self._start
        self._criteria.size = self._size
        raw_json = await self._client._call_api(
            ADMIN_EVENTS,
            query_params=self._criteria.query_params,
        )
        if not raw_json:
            self._events = []
            return False
        self._events = msgspec.convert(raw_json, list[AdminEvent], strict=False)
        return True

    async def __aiter__(self) -> AsyncGenerator[AdminEvent, None]:
        """Iterate through all pages of results."""
        while True:
            for event in self.current_page():
                yield event
            if not await self.next_page():
                break
