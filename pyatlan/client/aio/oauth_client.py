# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    AsyncApiCaller,
    OAuthClientGet,
    OAuthClientGetAll,
    OAuthClientGetById,
    OAuthClientPurge,
    OAuthClientUpdate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.oauth_clients import OAuthClient, OAuthClientResponse


class AsyncOAuthClientClient:
    """
    Async client for managing OAuth client credentials.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    async def get_all(self) -> OAuthClientResponse:
        """
        Retrieves all OAuth clients defined in Atlan.

        :returns: an OAuthClientResponse containing all OAuth clients
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = OAuthClientGetAll.prepare_request()
        raw_json = await self._client._call_api(endpoint, query_params)
        return OAuthClientGetAll.process_response(raw_json)

    @validate_arguments
    async def get(
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
        raw_json = await self._client._call_api(endpoint, query_params)
        return OAuthClientGet.process_response(raw_json)

    @validate_arguments
    async def get_by_id(self, client_id: str) -> OAuthClient:
        """
        Retrieves the OAuth client with the specified client ID.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :returns: the OAuthClient with the specified client ID
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = OAuthClientGetById.prepare_request(client_id)
        raw_json = await self._client._call_api(endpoint, query_params)
        return OAuthClientGetById.process_response(raw_json)

    @validate_arguments
    async def update(
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
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return OAuthClientUpdate.process_response(raw_json)

    @validate_arguments
    async def purge(self, client_id: str) -> None:
        """
        Delete (purge) the specified OAuth client.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :raises AtlanError: on any API communication issue
        """
        endpoint, _ = OAuthClientPurge.prepare_request(client_id)
        await self._client._call_api(endpoint)
