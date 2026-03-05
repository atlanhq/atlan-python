# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from pydantic.v1 import validate_arguments

from pyatlan.client.common import AdminGetAdminEvents, AdminGetKeycloakEvents, ApiCaller
from pyatlan.errors import ErrorCode
from pyatlan.model.keycloak_events import (
    AdminEventRequest,
    AdminEventResponse,
    KeycloakEventRequest,
    KeycloakEventResponse,
)


class AdminClient:
    """
    This class can be used to retrieve keycloak and admin events. This class does not need to be instantiated
    directly but can be obtained through the admin property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def get_keycloak_events(
        self, keycloak_request: KeycloakEventRequest
    ) -> KeycloakEventResponse:
        """
        Retrieve all events, based on the supplied filters.

        :param keycloak_request: details of the filters to apply when retrieving events
        :returns: the events that match the supplied filters
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = AdminGetKeycloakEvents.prepare_request(
            keycloak_request
        )
        raw_json = self._client._call_api(
            endpoint,
            query_params=query_params,
            exclude_unset=True,
        )
        response_data = AdminGetKeycloakEvents.process_response(
            raw_json, keycloak_request
        )

        return KeycloakEventResponse(client=self._client, **response_data)

    @validate_arguments
    def get_admin_events(self, admin_request: AdminEventRequest) -> AdminEventResponse:
        """
        Retrieve admin events based on the supplied filters.

        :param admin_request: details of the filters to apply when retrieving admin events
        :returns: the admin events that match the supplied filters
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = AdminGetAdminEvents.prepare_request(admin_request)
        raw_json = self._client._call_api(
            endpoint, query_params=query_params, exclude_unset=True
        )
        response_data = AdminGetAdminEvents.process_response(raw_json, admin_request)

        return AdminEventResponse(client=self._client, **response_data)
