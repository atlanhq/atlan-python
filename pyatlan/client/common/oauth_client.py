# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Dict, Optional

from pyatlan.client.constants import (
    DELETE_OAUTH_CLIENT,
    GET_OAUTH_CLIENT_BY_ID,
    GET_OAUTH_CLIENTS,
    UPDATE_OAUTH_CLIENT,
)
from pyatlan.model.oauth_clients import OAuthClient, OAuthClientResponse


class OAuthClientGetAll:
    """Shared logic for getting all OAuth clients without pagination."""

    @staticmethod
    def prepare_request() -> tuple:
        """
        Prepare the request for getting all OAuth clients.

        :returns: tuple of (endpoint, query_params)
        """
        return GET_OAUTH_CLIENTS.format_path_with_params(), None

    @staticmethod
    def process_response(raw_json: Dict) -> OAuthClientResponse:
        """
        Process the API response into an OAuthClientResponse object.

        :param raw_json: raw response from the API
        :returns: OAuthClientResponse with pagination info and records
        """
        return OAuthClientResponse(**raw_json)


class OAuthClientGet:
    """Shared logic for getting OAuth clients with pagination."""

    @staticmethod
    def prepare_request(
        limit: Optional[int] = None,
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
        }
        if limit is not None:
            query_params["limit"] = str(limit)
        if sort is not None:
            query_params["sort"] = sort

        return GET_OAUTH_CLIENTS.format_path_with_params(), query_params

    @staticmethod
    def process_response(raw_json: Dict) -> OAuthClientResponse:
        """
        Process the API response into an OAuthClientResponse object.

        :param raw_json: raw response from the API
        :returns: OAuthClientResponse with pagination info and records
        """
        return OAuthClientResponse(**raw_json)


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
    def process_response(raw_json: Dict) -> OAuthClient:
        """
        Process the API response into an OAuthClient object.

        :param raw_json: raw response from the API
        :returns: OAuthClient object
        """
        return OAuthClient(**raw_json)


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
    def process_response(raw_json: Dict) -> OAuthClient:
        """
        Process the API response into an OAuthClient.

        :param raw_json: raw response from the API
        :returns: the updated OAuthClient
        """
        return OAuthClient(**raw_json)


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
