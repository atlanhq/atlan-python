# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from typing import Dict, List

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import ADMIN_EVENTS, KEYCLOAK_EVENTS
from pyatlan.errors import ErrorCode
from pyatlan.model.keycloak_events import (
    AdminEvent,
    AdminEventRequest,
    KeycloakEvent,
    KeycloakEventRequest,
)


class AdminGetKeycloakEvents:
    """Shared logic for retrieving Keycloak events."""

    @staticmethod
    def prepare_request(keycloak_request: KeycloakEventRequest) -> tuple:
        """
        Prepare the request for retrieving Keycloak events.

        :param keycloak_request: details of the filters to apply when retrieving events
        :returns: tuple of (endpoint, query_params)
        """
        return KEYCLOAK_EVENTS, keycloak_request.query_params

    @staticmethod
    def process_response(
        raw_json: Dict, keycloak_request: KeycloakEventRequest
    ) -> Dict:
        """
        Process the API response and return the data for client-side model creation.

        :param raw_json: raw response from the API
        :param keycloak_request: original request object
        :returns: dictionary containing response data
        """
        if raw_json:
            try:
                events = parse_obj_as(List[KeycloakEvent], raw_json)
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            events = []

        return {
            "criteria": keycloak_request,
            "start": keycloak_request.offset or 0,
            "size": keycloak_request.size or 100,
            "events": events,
        }


class AdminGetAdminEvents:
    """Shared logic for retrieving admin events."""

    @staticmethod
    def prepare_request(admin_request: AdminEventRequest) -> tuple:
        """
        Prepare the request for retrieving admin events.

        :param admin_request: details of the filters to apply when retrieving admin events
        :returns: tuple of (endpoint, query_params)
        """
        return ADMIN_EVENTS, admin_request.query_params

    @staticmethod
    def process_response(raw_json: Dict, admin_request: AdminEventRequest) -> Dict:
        """
        Process the API response and return the data for client-side model creation.

        :param raw_json: raw response from the API
        :param admin_request: original request object
        :returns: dictionary containing response data
        """
        if raw_json:
            try:
                events = parse_obj_as(List[AdminEvent], raw_json)
            except ValidationError as err:
                raise ErrorCode.JSON_ERROR.exception_with_parameters(
                    raw_json, 200, str(err)
                ) from err
        else:
            events = []

        return {
            "criteria": admin_request,
            "start": admin_request.offset or 0,
            "size": admin_request.size or 100,
            "events": events,
        }
