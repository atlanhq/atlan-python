# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

import logging
import os

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import GET_TOKEN
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.model.response import AccessTokenResponse

LOGGER = logging.getLogger(__name__)


class ImpersonationClient:
    """
    This class can be used for impersonating users as part of Atlan automations (if desired).
    Note: this will only work when run as part of Atlan's packaged workflow ecosystem (running in the cluster back-end).
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def user(self, user_id: str) -> str:
        """
        Retrieves a bearer token that impersonates the provided user.

        :param user_id: unique identifier of the user to impersonate
        :returns: a bearer token that impersonates the provided user
        :raises AtlanError: on any API communication issue
        """
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        if not client_id or not client_secret:
            raise ErrorCode.MISSING_CREDENTIALS.exception_with_parameters()
        credentials = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

        LOGGER.debug("Getting token with client id and secret")
        try:
            raw_json = self._client._call_api(GET_TOKEN, request_obj=credentials)
            argo_token = AccessTokenResponse(**raw_json).access_token
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_ESCALATE.exception_with_parameters() from atlan_err
        LOGGER.debug("Getting token with subject token")
        try:
            user_credentials = {
                "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
                "client_id": client_id,
                "client_secret": client_secret,
                "subject_token": argo_token,
                "requested_subject": user_id,
            }
            raw_json = self._client._call_api(GET_TOKEN, request_obj=user_credentials)
            return AccessTokenResponse(**raw_json).access_token
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_IMPERSONATE.exception_with_parameters() from atlan_err
