# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Optional, Set

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    AsyncApiCaller,
    TokenCreate,
    TokenGet,
    TokenGetByGuid,
    TokenGetById,
    TokenGetByName,
    TokenPurge,
    TokenUpdate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.api_tokens import ApiToken, ApiTokenResponse


class AsyncTokenClient:
    """
    Async client for operating on API tokens.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def get(
        self,
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> ApiTokenResponse:
        """
        Retrieves an ApiTokenResponse which contains a list of API tokens defined in Atlan.

        :param limit: maximum number of results to be returned
        :param post_filter: which API tokens to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: an ApiTokenResponse which contains a list of API tokens that match the provided criteria
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = TokenGet.prepare_request(
            limit, post_filter, sort, count, offset
        )
        raw_json = await self._client._call_api(endpoint, query_params)
        return TokenGet.process_response(raw_json)

    @validate_arguments
    async def get_by_name(self, display_name: str) -> Optional[ApiToken]:
        """
        Retrieves the API token with a name that exactly matches the provided string.

        :param display_name: name (as it appears in the UI) by which to retrieve the API token
        :returns: the API token whose name (in the UI) matches the provided string, or None if there is none
        """
        endpoint, query_params = TokenGetByName.prepare_request(display_name)
        raw_json = await self._client._call_api(endpoint, query_params)
        return TokenGetByName.process_response(raw_json)

    @validate_arguments
    async def get_by_id(self, client_id: str) -> Optional[ApiToken]:
        """
        Retrieves the API token with a client ID that exactly matches the provided string.

        :param client_id: unique client identifier by which to retrieve the API token
        :returns: the API token whose clientId matches the provided string, or None if there is none
        """
        endpoint, query_params = TokenGetById.prepare_request(client_id)
        raw_json = await self._client._call_api(endpoint, query_params)
        return TokenGetById.process_response(raw_json)

    @validate_arguments
    async def get_by_guid(self, guid: str) -> Optional[ApiToken]:
        """
        Retrieves the API token with a unique ID (GUID) that exactly matches the provided string.

        :param guid: unique identifier by which to retrieve the API token
        :returns: the API token whose clientId matches the provided string, or None if there is none
        """
        endpoint, query_params = TokenGetByGuid.prepare_request(guid)
        raw_json = await self._client._call_api(endpoint, query_params)
        return TokenGetByGuid.process_response(raw_json)

    @validate_arguments
    async def create(
        self,
        display_name: str,
        description: str = "",
        personas: Optional[Set[str]] = None,
        validity_seconds: int = -1,
    ) -> ApiToken:
        """
        Create a new API token with the provided settings.

        :param display_name: human-readable name for the API token
        :param description: optional explanation of the API token
        :param personas: qualified_names of personas that should  be linked to the token
        :param validity_seconds: time in seconds after which the token should expire (negative numbers are treated as
                                 infinite)
        :returns: the created API token
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = TokenCreate.prepare_request(
            display_name, description, personas, validity_seconds
        )
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return TokenCreate.process_response(raw_json)

    @validate_arguments
    async def update(
        self,
        guid: str,
        display_name: str,
        description: str = "",
        personas: Optional[Set[str]] = None,
    ) -> ApiToken:
        """
        Update an existing API token with the provided settings.

        :param guid: unique identifier (GUID) of the API token
        :param display_name: human-readable name for the API token
        :param description: optional explanation of the API token
        :param personas: qualified_names of personas that should  be linked to the token, note that you MUST
                         provide the complete list on any update (any not included in the list will be removed,
                         so if you do not specify any personas then ALL personas will be unlinked from the API token)
        :returns: the created API token
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = TokenUpdate.prepare_request(
            guid, display_name, description, personas
        )
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return TokenUpdate.process_response(raw_json)

    @validate_arguments
    async def purge(self, guid: str) -> None:
        """
        Delete (purge) the specified API token.

        :param guid: unique identifier (GUID) of the API token to delete
        :raises AtlanError: on any API communication issue
        """
        endpoint, _ = TokenPurge.prepare_request(guid)
        await self._client._call_api(endpoint)
