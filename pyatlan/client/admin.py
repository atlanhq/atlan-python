# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

from typing import List

from pydantic.v1 import ValidationError, parse_obj_as, validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import ADMIN_EVENTS, KEYCLOAK_EVENTS
from pyatlan.errors import ErrorCode
from pyatlan.model.keycloak_events import (
    AdminEvent,
    AdminEventRequest,
    AdminEventResponse,
    KeycloakEvent,
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
        if raw_json := self._client._call_api(
            KEYCLOAK_EVENTS,
            query_params=keycloak_request.query_params,
            exclude_unset=True,
        ):
            try:
                events = parse_obj_as(List[KeycloakEvent], raw_json)
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            events = []
        return KeycloakEventResponse(
            client=self._client,
            criteria=keycloak_request,
            start=keycloak_request.offset or 0,
            size=keycloak_request.size or 100,
            events=events,
        )

    @validate_arguments
    def get_admin_events(self, admin_request: AdminEventRequest) -> AdminEventResponse:
        """
        Retrieve admin events based on the supplied filters.

        :param admin_request: details of the filters to apply when retrieving admin events
        :returns: the admin events that match the supplied filters
        :raises AtlanError: on any API communication issue
        """
        if raw_json := self._client._call_api(
            ADMIN_EVENTS, query_params=admin_request.query_params, exclude_unset=True
        ):
            try:
                events = parse_obj_as(List[AdminEvent], raw_json)
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            events = []
        return AdminEventResponse(
            client=self._client,
            criteria=admin_request,
            start=admin_request.offset or 0,
            size=admin_request.size or 100,
            events=events,
        )
