# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from typing import AsyncGenerator, List

from pydantic.v1 import parse_obj_as

from pyatlan.client.constants import ADMIN_EVENTS, KEYCLOAK_EVENTS
from pyatlan.model.keycloak_events import (
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
        events: List[KeycloakEvent],
    ):
        self._client = client
        self._criteria = criteria
        self._start = start
        self._size = size
        self._events = events

    def current_page(self) -> List[KeycloakEvent]:
        """
        Retrieve the current page of events.

        :returns: list of events in the current page
        """
        return self._events

    async def next_page(self, start=None, size=None) -> bool:
        """
        Fetch the next page of events.

        :param start: starting point for the next page (for paging)
        :param size: maximum number of events to retrieve (per page)
        :returns: True if there are more results, False otherwise
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._events else False

    async def _get_next_page(self):
        """
        Fetch the next page of events from the API.

        :returns: True if there are more results, False otherwise
        """
        self._criteria.offset = self._start
        self._criteria.size = self._size
        raw_json = await self._client._call_api(
            KEYCLOAK_EVENTS,
            query_params=self._criteria.query_params,
        )
        if not raw_json:
            self._events = []
            return False
        self._events = parse_obj_as(List[KeycloakEvent], raw_json)
        return True

    async def __aiter__(self) -> AsyncGenerator[KeycloakEvent, None]:
        """
        Iterate through all events across all pages.

        :returns: async generator of KeycloakEvent objects
        """
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
        events: List[AdminEvent],
    ):
        self._client = client
        self._criteria = criteria
        self._start = start
        self._size = size
        self._events = events

    def current_page(self) -> List[AdminEvent]:
        """
        Retrieve the current page of events.

        :returns: list of events in the current page
        """
        return self._events

    async def next_page(self, start=None, size=None) -> bool:
        """
        Fetch the next page of events.

        :param start: starting point for the next page (for paging)
        :param size: maximum number of events to retrieve (per page)
        :returns: True if there are more results, False otherwise
        """
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return await self._get_next_page() if self._events else False

    async def _get_next_page(self):
        """
        Fetch the next page of events from the API.

        :returns: True if there are more results, False otherwise
        """
        self._criteria.offset = self._start
        self._criteria.size = self._size
        raw_json = await self._client._call_api(
            ADMIN_EVENTS,
            query_params=self._criteria.query_params,
        )
        if not raw_json:
            self._events = []
            return False
        self._events = parse_obj_as(List[AdminEvent], raw_json)
        return True

    async def __aiter__(self) -> AsyncGenerator[AdminEvent, None]:
        """
        Iterate through all events across all pages.

        :returns: async generator of AdminEvent objects
        """
        while True:
            for event in self.current_page():
                yield event
            if not await self.next_page():
                break
