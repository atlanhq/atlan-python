# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

import logging
from typing import Optional

from pyatlan.client.common import (
    AsyncApiCaller,
    ImpersonateEscalate,
    ImpersonateGetClientSecret,
    ImpersonateGetUserId,
    ImpersonateUser,
)
from pyatlan.errors import AtlanError, ErrorCode

LOGGER = logging.getLogger(__name__)


class AsyncImpersonationClient:
    """
    Async version of ImpersonationClient for impersonating users as part of Atlan automations.
    Note: this will only work when run as part of Atlan's packaged workflow ecosystem (running in the cluster back-end).
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    async def user(self, user_id: str) -> str:
        """
        Retrieves a bearer token that impersonates the provided user.

        :param user_id: unique identifier of the user to impersonate
        :returns: a bearer token that impersonates the provided user
        :raises AtlanError: on any API communication issue
        """
        # Get client info using shared logic
        client_info = ImpersonateUser.get_client_info()

        # Prepare escalation request using shared logic
        endpoint, credentials = ImpersonateUser.prepare_request(client_info)

        LOGGER.debug("Getting token with client id and secret")
        try:
            raw_json = await self._client._call_api(endpoint, request_obj=credentials)
            argo_token = ImpersonateUser.process_response(raw_json)
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_ESCALATE.exception_with_parameters() from atlan_err

        LOGGER.debug("Getting token with subject token")
        try:
            # Prepare impersonation request using shared logic
            endpoint, user_credentials = ImpersonateUser.prepare_impersonation_request(
                client_info, argo_token, user_id
            )
            raw_json = await self._client._call_api(
                endpoint, request_obj=user_credentials
            )
            return ImpersonateUser.process_response(raw_json)
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_IMPERSONATE.exception_with_parameters() from atlan_err

    async def escalate(self) -> str:
        """
        Escalate to a privileged user on a short-term basis.
        Note: this is only possible from within the Atlan tenant, and only when given the appropriate credentials.

        :returns: a short-lived bearer token with escalated privileges
        :raises AtlanError: on any API communication issue
        """
        # Get client info using shared logic
        client_info = ImpersonateEscalate.get_client_info()

        # Prepare escalation request using shared logic
        endpoint, credentials = ImpersonateEscalate.prepare_request(client_info)

        try:
            raw_json = await self._client._call_api(endpoint, request_obj=credentials)
            return ImpersonateEscalate.process_response(raw_json)
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_ESCALATE.exception_with_parameters() from atlan_err

    async def get_client_secret(self, client_guid: str) -> Optional[str]:
        """
        Retrieves the client secret associated with the given client GUID

        :param client_guid: GUID of the client whose secret is to be retrieved
        :returns: client secret if available, otherwise `None`
        :raises:
            - AtlanError: If an API error occurs.
            - InvalidRequestError: If the provided GUID is invalid or retrieval fails.
        """
        try:
            # Prepare request using shared logic
            endpoint = ImpersonateGetClientSecret.prepare_request(client_guid)

            # Make async API call
            raw_json = await self._client._call_api(endpoint)

            # Process response using shared logic
            return ImpersonateGetClientSecret.process_response(raw_json)
        except AtlanError as e:
            raise ErrorCode.UNABLE_TO_RETRIEVE_CLIENT_SECRET.exception_with_parameters(
                client_guid
            ) from e

    async def get_user_id(self, username: str) -> Optional[str]:
        """
        Retrieves the user ID from Keycloak for the specified username.
        This method is particularly useful for impersonating API tokens.

        :param username: username of the user whose ID needs to be retrieved.
        :returns: Keycloak user ID
        :raises:
            - AtlanError: If an API error occurs.
            - InvalidRequestError: If an error occurs while fetching the user ID from Keycloak.
        """
        try:
            # Prepare request using shared logic
            endpoint, query_params = ImpersonateGetUserId.prepare_request(username)

            # Make async API call
            raw_json = await self._client._call_api(endpoint, query_params=query_params)

            # Process response using shared logic
            return ImpersonateGetUserId.process_response(raw_json)
        except AtlanError as e:
            raise ErrorCode.UNABLE_TO_RETRIEVE_USER_GUID.exception_with_parameters(
                username
            ) from e
