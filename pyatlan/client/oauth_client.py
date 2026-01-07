# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    OAuthClientGet,
    OAuthClientGetAll,
    OAuthClientGetById,
    OAuthClientPurge,
    OAuthClientUpdate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.oauth_clients import OAuthClient, OAuthClientResponse


class OAuthClientClient:
    """
    This class can be used to manage OAuth client credentials.
    This class does not need to be instantiated directly but can be
    obtained through the oauth_client property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def get_all(self) -> OAuthClientResponse:
        """
        Retrieves all OAuth clients defined in Atlan.

        :returns: an OAuthClientResponse containing all OAuth clients
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = OAuthClientGetAll.prepare_request()
        raw_json = self._client._call_api(endpoint, query_params)
        return OAuthClientGetAll.process_response(raw_json)

    @validate_arguments
    def get(
        self,
        limit: Optional[int] = None,
        offset: int = 0,
        sort: Optional[str] = None,
    ) -> OAuthClientResponse:
        """
        Retrieves OAuth clients defined in Atlan with pagination support.

        :param limit: maximum number of results to be returned
        :param offset: starting point for results to return, for paging
        :param sort: property by which to sort the results (e.g., 'createdAt' for descending)
        :returns: an OAuthClientResponse containing records and pagination info
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = OAuthClientGet.prepare_request(limit, offset, sort)
        raw_json = self._client._call_api(endpoint, query_params)
        return OAuthClientGet.process_response(raw_json)

    @validate_arguments
    def get_by_id(self, client_id: str) -> OAuthClient:
        """
        Retrieves the OAuth client with the specified client ID.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :returns: the OAuthClient with the specified client ID
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = OAuthClientGetById.prepare_request(client_id)
        raw_json = self._client._call_api(endpoint, query_params)
        return OAuthClientGetById.process_response(raw_json)

    @validate_arguments
    def update(
        self,
        client_id: str,
        display_name: Optional[str] = None,
        description: Optional[str] = None,
    ) -> OAuthClient:
        """
        Update an existing OAuth client with the provided settings.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :param display_name: human-readable name for the OAuth client
        :param description: optional explanation of the OAuth client
        :returns: the updated OAuthClient
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = OAuthClientUpdate.prepare_request(
            client_id, display_name, description
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return OAuthClientUpdate.process_response(raw_json)

    @validate_arguments
    def purge(self, client_id: str) -> None:
        """
        Delete (purge) the specified OAuth client.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :raises AtlanError: on any API communication issue
        """
        endpoint, _ = OAuthClientPurge.prepare_request(client_id)
        self._client._call_api(endpoint)
