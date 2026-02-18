# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import List, Optional

from pyatlan.client.common.validate import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    OAuthClientCreate,
    OAuthClientGet,
    OAuthClientGetById,
    OAuthClientPurge,
    OAuthClientUpdate,
    RoleGet,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.oauth_client import (
    OAuthClientCreateResponse,
    OAuthClientListResponse,
    OAuthClientResponse,
)


class OAuthClient:
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

    @validate_arguments
    def get(
        self,
        limit: int = 20,
        offset: int = 0,
        sort: Optional[str] = None,
    ) -> OAuthClientListResponse:
        """
        Retrieves OAuth clients defined in Atlan with pagination support.

        :param limit: maximum number of results to be returned per page (default: 20)
        :param offset: starting point for results to return, for paging
        :param sort: property by which to sort the results (e.g., 'createdAt' for descending)
        :returns: an OAuthClientListResponse containing records and pagination info
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = OAuthClientGet.prepare_request(limit, offset, sort)
        raw_json = self._client._call_api(endpoint, query_params)
        return OAuthClientListResponse(
            **raw_json,
            endpoint=endpoint,
            client=self._client,
            size=limit,
            start=offset,
            sort=sort,
        )

    @validate_arguments
    def get_by_id(self, client_id: str) -> OAuthClientResponse:
        """
        Retrieves the OAuth client with the specified client ID.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :returns: the OAuthClientResponse with the specified client ID
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
    ) -> OAuthClientResponse:
        """
        Update an existing OAuth client with the provided settings.

        :param client_id: unique client identifier (e.g., 'oauth-client-xxx')
        :param display_name: human-readable name for the OAuth client
        :param description: optional explanation of the OAuth client
        :returns: the updated OAuthClientResponse
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

    def _fetch_available_roles(self):
        """
        Fetch all available roles (workspace and admin-subrole levels).

        :returns: list of AtlanRole objects
        """
        filter_str = OAuthClientCreate.build_roles_filter()
        endpoint, query_params = RoleGet.prepare_request(
            limit=100,
            post_filter=filter_str,
        )
        raw_json = self._client._call_api(endpoint, query_params)
        response = RoleGet.process_response(raw_json)
        return response.records or []

    @validate_arguments
    def create(
        self,
        name: str,
        role: str,
        description: Optional[str] = None,
        persona_qualified_names: Optional[List[str]] = None,
    ) -> OAuthClientCreateResponse:
        """
        Create a new OAuth client with the provided settings.

        :param name: human-readable name for the OAuth client (displayed in UI)
        :param role: role description to assign to the OAuth client (e.g., 'Admin', 'Member').
        :param description: optional explanation of the OAuth client
        :param persona_qualified_names: qualified names of personas to associate with the OAuth client
        :returns: the created OAuthClientCreateResponse (includes client_id and client_secret)
        :raises AtlanError: on any API communication issue
        :raises NotFoundError: if the specified role description is not found
        """
        # Fetch available roles and resolve the user-provided role name
        available_roles = self._fetch_available_roles()
        resolved_role = OAuthClientCreate.resolve_role_name(role, available_roles)

        # Prepare and execute the request
        endpoint, request_obj = OAuthClientCreate.prepare_request(
            display_name=name,
            role=resolved_role,
            description=description,
            persona_qualified_names=persona_qualified_names,
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return OAuthClientCreate.process_response(raw_json)
