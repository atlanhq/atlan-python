# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

import json
from typing import Dict, List, Optional

from pyatlan.client.constants import (
    CREATE_OAUTH_CLIENT,
    DELETE_OAUTH_CLIENT,
    GET_OAUTH_CLIENT_BY_ID,
    GET_OAUTH_CLIENTS,
    UPDATE_OAUTH_CLIENT,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.oauth_client import (
    OAuthClientCreateResponse,
    OAuthClientRequest,
    OAuthClientResponse,
)
from pyatlan.model.role import AtlanRole


class OAuthClientGet:
    """Shared logic for getting OAuth clients with pagination."""

    @staticmethod
    def prepare_request(
        limit: int = 20,
        offset: int = 0,
        sort: Optional[str] = None,
    ) -> tuple:
        """
        Prepare the request for getting OAuth clients with pagination.

        :param limit: maximum number of results to be returned
        :param offset: starting point for results to return, for paging
        :param sort: property by which to sort the results (e.g., 'createdAt' for descending)
        :returns: tuple of (endpoint, query_params)
        """
        query_params: Dict[str, str] = {
            "count": "true",
            "offset": str(offset),
            "limit": str(limit),
        }
        if sort is not None:
            query_params["sort"] = sort

        return GET_OAUTH_CLIENTS, query_params


class OAuthClientGetById:
    """Shared logic for getting an OAuth client by its client ID."""

    @staticmethod
    def prepare_request(client_id: str) -> tuple:
        """
        Prepare the request for getting an OAuth client by its client ID.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :returns: tuple of (endpoint, query_params)
        """
        endpoint = GET_OAUTH_CLIENT_BY_ID.format_path(
            {"client_id": client_id}
        ).format_path_with_params()
        return endpoint, None

    @staticmethod
    def process_response(raw_json: Dict) -> OAuthClientResponse:
        """
        Process the API response into an OAuthClientResponse object.

        :param raw_json: raw response from the API
        :returns: OAuthClientResponse object
        """
        return OAuthClientResponse(**raw_json)


class OAuthClientUpdate:
    """Shared logic for updating OAuth clients."""

    @staticmethod
    def prepare_request(
        client_id: str,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> tuple:
        """
        Prepare the request for updating an OAuth client.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :param display_name: human-readable name for the OAuth client
        :param description: optional explanation of the OAuth client
        :returns: tuple of (endpoint, request_dict)
        """
        # Build request dict with only non-None values to avoid sending null fields
        request_dict: Dict[str, str] = {}
        if display_name is not None:
            request_dict["displayName"] = display_name
        if description is not None:
            request_dict["description"] = description

        endpoint = UPDATE_OAUTH_CLIENT.format_path(
            {"client_id": client_id}
        ).format_path_with_params()
        return endpoint, request_dict

    @staticmethod
    def process_response(raw_json: Dict) -> OAuthClientResponse:
        """
        Process the API response into an OAuthClientResponse.

        :param raw_json: raw response from the API
        :returns: the updated OAuthClientResponse
        """
        return OAuthClientResponse(**raw_json)


class OAuthClientPurge:
    """Shared logic for deleting OAuth clients."""

    @staticmethod
    def prepare_request(client_id: str) -> tuple:
        """
        Prepare the request for deleting an OAuth client.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :returns: tuple of (endpoint, None)
        """
        endpoint = DELETE_OAUTH_CLIENT.format_path(
            {"client_id": client_id}
        ).format_path_with_params()
        return endpoint, None


class OAuthClientCreate:
    """Shared logic for creating OAuth clients."""

    @staticmethod
    def resolve_role_name(role: str, available_roles: List[AtlanRole]) -> str:
        """
        Resolve the user-provided role to the actual API role name.

        The user provides a role description (e.g., 'Admin', 'Member', 'Admins (Connections)')
        and we find the corresponding role name (e.g., '$admin', '$member', '$admin_connections')
        to send in the API payload.

        :param role: user-provided role description
        :param available_roles: list of available roles from the API
        :returns: the actual API role name (e.g., '$admin')
        :raises NotFoundError: if the role description is not found
        """
        role_lower = role.lower().strip()

        # Build lookup: lowercased description -> role name
        desc_to_name: Dict[str, str] = {}
        available_descriptions: List[str] = []

        for r in available_roles:
            if r.description and r.name:
                desc_to_name[r.description.lower()] = r.name
                available_descriptions.append(r.description)

        # Match against description
        if role_lower in desc_to_name:
            return desc_to_name[role_lower]

        # No match found - raise error with available descriptions
        raise ErrorCode.ROLE_NOT_FOUND_BY_DESCRIPTION.exception_with_parameters(
            role, ", ".join(sorted(available_descriptions))
        )

    @staticmethod
    def build_roles_filter() -> str:
        """
        Build the filter string to fetch workspace and admin-subrole level roles.

        :returns: JSON filter string
        """

        return json.dumps({"$or": [{"level": "workspace"}, {"level": "admin-subrole"}]})

    @staticmethod
    def prepare_request(
        display_name: str,
        role: str,
        description: Optional[str] = None,
        persona_qualified_names: Optional[List[str]] = None,
    ) -> tuple:
        """
        Prepare the request for creating an OAuth client.

        Note: The role should already be resolved to the actual API value
        (e.g., '$admin') before calling this method.

        :param display_name: human-readable name for the OAuth client
        :param role: role assigned to the OAuth client (must be the actual API value like '$admin')
        :param description: optional explanation of the OAuth client
        :param persona_qualified_names: qualified names of personas to associate with the OAuth client
        :returns: tuple of (endpoint, request_dict)
        """
        request = OAuthClientRequest(
            display_name=display_name,
            description=description or "",
            role=role,
            persona_qualified_names=persona_qualified_names or [],
        )  # type: ignore[call-arg]
        return CREATE_OAUTH_CLIENT.format_path_with_params(), request

    @staticmethod
    def process_response(raw_json: Dict) -> OAuthClientCreateResponse:
        """
        Process the API response into an OAuthClientCreateResponse.

        :param raw_json: raw response from the API
        :returns: the created OAuthClientCreateResponse (includes client_secret)
        """
        return OAuthClientCreateResponse(**raw_json)
