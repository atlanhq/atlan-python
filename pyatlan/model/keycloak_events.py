# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from typing import Any, Generator, Optional

from pydantic import Field, parse_obj_as

from pyatlan.client.constants import ADMIN_EVENTS, KEYCLOAK_EVENTS
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AdminOperationType, AdminResourceType, KeycloakEventType


class AuthDetails(AtlanObject):
    client_id: Optional[str] = Field(
        description="Unique identifier (GUID) of the client that carried out the operation."
    )
    ip_address: Optional[str] = Field(
        description="IP address from which the operation was carried out."
    )
    realm_id: Optional[str] = Field(
        description="Unique name of the realm from which the operation was carried out."
    )
    user_id: Optional[str] = Field(
        description="Unique identifier (GUID) of the user who carried out the operation.",
    )


class KeycloakEvent(AtlanObject):
    client_id: Optional[str] = Field(
        description="Where the login occurred (usually 'atlan-frontend')."
    )
    details: Any = Field(description="TBC")
    ip_address: Optional[str] = Field(
        description="IP address from which the user logged in."
    )
    realm_id: Optional[str] = Field(description="TBC")
    session_id: Optional[str] = Field(
        description="Unique identifier (GUID) of the session for the login."
    )
    time: Optional[int] = Field(
        description="Time (epoch) when the login occurred, in milliseconds."
    )
    type: Optional[KeycloakEventType] = Field(
        description="Type of login event that occurred (usually 'LOGIN')."
    )
    user_id: Optional[str] = Field(
        description="Unique identifier (GUID) of the user that logged in."
    )


class AdminEvent(AtlanObject):
    operation_type: Optional[AdminOperationType] = Field(
        description="Type of admin operation that occurred."
    )
    realm_id: Optional[str] = Field(
        description="Unique identifier of the realm in which the event occurred (usually 'default')."
    )
    representation: Optional[str] = Field(
        description="Detailed resource that was created or changed as a result of the operation."
    )
    resource_path: Optional[str] = Field(
        description="Location of the resource that was created or changed as a result of the operation."
    )
    resource_type: Optional[AdminResourceType] = Field(
        description="Type of resource for the admin operation that occurred."
    )
    time: Optional[int] = Field(
        description="Time (epoch) when the admin operation occurred, in milliseconds."
    )
    auth_details: Optional[AuthDetails] = Field(
        description="Details of who carried out the operation."
    )


class KeycloakEventRequest(AtlanObject):
    client: Optional[str] = Field(description="Application or OAuth client name.")
    ip_address: Optional[str] = Field(
        description="IP address from which the event was triggered."
    )
    date_from: Optional[str] = Field(
        description="Earliest date from which to include events (format: yyyy-MM-dd)."
    )
    date_to: Optional[str] = Field(
        description="Latest date up to which to include events (format: yyyy-MM-dd)."
    )
    offset: Optional[int] = Field(
        description="Starting point for the events (for paging)."
    )
    size: Optional[int] = Field(
        description="Maximum number of events to retrieve (per page)."
    )
    types: Optional[list[KeycloakEventType]] = Field(
        description="Include events only of the supplied types."
    )
    user_id: Optional[str] = Field(
        description="Unique identifier (GUID) of the user who triggered the event."
    )

    @property
    def query_params(self) -> dict:
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


class KeycloakEventResponse(object):
    def __init__(
        self,
        client: "AtlanClient",
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
        return self._events

    def next_page(self, start=None, size=None) -> bool:
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._events else False

    def _get_next_page(self):
        self._criteria.offset = self._start
        self._criteria.size = self._size
        raw_json = self._client._call_api(
            KEYCLOAK_EVENTS,
            query_params=self._criteria.query_params,
        )
        if not raw_json:
            self._events = []
            return False
        self._events = parse_obj_as(list[KeycloakEvent], raw_json)
        return True

    def __iter__(self) -> Generator[KeycloakEvent, None, None]:
        while True:
            yield from self.current_page()
            if not self.next_page():
                break


class AdminEventRequest(AtlanObject):
    client_id: Optional[str] = Field(
        description="Unique identifier (GUID) of the client that carried out the operation."
    )
    ip_address: Optional[str] = Field(
        description="IP address from which the operation was carried out."
    )
    realm_id: Optional[str] = Field(
        description="Unique name of the realm from which the operation was carried out."
    )
    user_id: Optional[str] = Field(
        description="Unique identifier (GUID) of the user who carried out the operation."
    )
    date_from: Optional[str] = Field(
        description="Earliest date from which to include events (format: yyyy-MM-dd)."
    )
    date_to: Optional[str] = Field(
        description="Latest date up to which to include events (format: yyyy-MM-dd)."
    )
    offset: Optional[int] = Field(
        description="Starting point for the events (for paging)."
    )
    size: Optional[int] = Field(
        description="Maximum number of events to retrieve (per page)."
    )
    operation_types: Optional[list[AdminOperationType]] = Field(
        description="Include events only with the supplied types of operations."
    )
    resource_path: Optional[str] = Field(
        description="Include events only against the supplied resource."
    )
    resource_types: Optional[list[AdminResourceType]] = Field(
        description="Include events only against the supplied types of resources."
    )

    @property
    def query_params(self) -> dict:
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


class AdminEventResponse(object):
    def __init__(
        self,
        client: "AtlanClient",
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
        return self._events

    def next_page(self, start=None, size=None) -> bool:
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self._events else False

    def _get_next_page(self):
        self._criteria.offset = self._start
        self._criteria.size = self._size
        raw_json = self._client._call_api(
            ADMIN_EVENTS,
            query_params=self._criteria.query_params,
        )
        if not raw_json:
            self._events = []
            return False
        self._events = parse_obj_as(list[AdminEvent], raw_json)
        return True

    def __iter__(self) -> Generator[AdminEvent, None, None]:
        while True:
            yield from self.current_page()
            if not self.next_page():
                break


from pyatlan.client.atlan import AtlanClient  # noqa: E402
