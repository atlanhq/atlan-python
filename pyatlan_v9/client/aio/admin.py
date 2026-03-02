# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

import msgspec

from pyatlan.client.common import (
    AdminGetAdminEvents,
    AdminGetKeycloakEvents,
    AsyncApiCaller,
)
from pyatlan.errors import ErrorCode
from pyatlan.validate import validate_arguments
from pyatlan_v9.model.aio.keycloak_events import (
    AsyncAdminEventResponse,
    AsyncKeycloakEventResponse,
)
from pyatlan_v9.model.keycloak_events import (
    AdminEvent,
    AdminEventRequest,
    KeycloakEvent,
    KeycloakEventRequest,
)


class V9AsyncAdminClient:
    """
    Async version of AdminClient for retrieving keycloak and admin events. This class does not need to be instantiated
    directly but can be obtained through the admin property of the async Atlan client.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def get_keycloak_events(
        self, keycloak_request: KeycloakEventRequest
    ) -> AsyncKeycloakEventResponse:
        """
        Retrieve all events, based on the supplied filters.

        :param keycloak_request: details of the filters to apply when retrieving events
        :returns: the events that match the supplied filters
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = AdminGetKeycloakEvents.prepare_request(
            keycloak_request
        )
        raw_json = await self._client._call_api(
            endpoint,
            query_params=query_params,
        )
        if raw_json:
            events = msgspec.convert(raw_json, list[KeycloakEvent], strict=False)
        else:
            events = []

        return AsyncKeycloakEventResponse(
            client=self._client,
            criteria=keycloak_request,
            start=keycloak_request.offset or 0,
            size=keycloak_request.size or 100,
            events=events,
        )

    @validate_arguments
    async def get_admin_events(
        self, admin_request: AdminEventRequest
    ) -> AsyncAdminEventResponse:
        """
        Retrieve admin events based on the supplied filters.

        :param admin_request: details of the filters to apply when retrieving admin events
        :returns: the admin events that match the supplied filters
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = AdminGetAdminEvents.prepare_request(admin_request)
        raw_json = await self._client._call_api(
            endpoint, query_params=query_params
        )
        if raw_json:
            events = msgspec.convert(raw_json, list[AdminEvent], strict=False)
        else:
            events = []

        return AsyncAdminEventResponse(
            client=self._client,
            criteria=admin_request,
            start=admin_request.offset or 0,
            size=admin_request.size or 100,
            events=events,
        )
