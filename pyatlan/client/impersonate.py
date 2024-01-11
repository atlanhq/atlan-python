# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

import os

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import GET_TOKEN
from pyatlan.errors import ErrorCode
from pyatlan.model.response import AccessTokenResponse


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
        client_id = os.getenv("CLIENT_ID")
        client_secret = os.getenv("CLIENT_SECRET")
        if not client_id or not client_secret:
            raise ErrorCode.MISSING_CREDENTIALS.exception_with_parameters()
        credentials = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

        raw_json = self._client._call_api(GET_TOKEN, request_obj=credentials)

        return AccessTokenResponse(**raw_json)
