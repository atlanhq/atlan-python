# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

import os
from typing import Any, Dict, NamedTuple, Optional, Tuple

from pyatlan.client.constants import GET_CLIENT_SECRET, GET_KEYCLOAK_USER, GET_TOKEN
from pyatlan.errors import ErrorCode
from pyatlan.model.response import AccessTokenResponse
from pyatlan.utils import API


class ClientInfo(NamedTuple):
    client_id: str
    client_secret: str


class ImpersonateUser:
    """Shared logic for user impersonation operations."""

    @staticmethod
    def get_client_info(
        client_id: Optional[str] = None, client_secret: Optional[str] = None
    ) -> ClientInfo:
        """Get client info from user provided client_id and client_secret or environment variables."""
        final_client_id = client_id or os.getenv("CLIENT_ID")
        final_client_secret = client_secret or os.getenv("CLIENT_SECRET")
        if not final_client_id or not final_client_secret:
            raise ErrorCode.MISSING_CREDENTIALS.exception_with_parameters()
        return ClientInfo(client_id=final_client_id, client_secret=final_client_secret)

    @staticmethod
    def prepare_request(client_info: ClientInfo) -> Tuple[API, Dict[str, str]]:
        """Prepare the escalation token request."""
        credentials = {
            "grant_type": "client_credentials",
            "client_id": client_info.client_id,
            "client_secret": client_info.client_secret,
        }
        return GET_TOKEN, credentials

    @staticmethod
    def prepare_impersonation_request(
        client_info: ClientInfo, argo_token: str, user_id: str
    ) -> Tuple[API, Dict[str, str]]:
        """Prepare the user impersonation request."""
        user_credentials = {
            "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
            "client_id": client_info.client_id,
            "client_secret": client_info.client_secret,
            "subject_token": argo_token,
            "requested_subject": user_id,
        }
        return GET_TOKEN, user_credentials

    @staticmethod
    def process_response(raw_json: Dict[str, Any]) -> str:
        """Process token response to extract access token."""
        return AccessTokenResponse(**raw_json).access_token


class ImpersonateEscalate:
    """Shared logic for escalating privileges."""

    @staticmethod
    def get_client_info() -> ClientInfo:
        """Get client info from environment variables."""
        return ImpersonateUser.get_client_info()

    @staticmethod
    def prepare_request(client_info: ClientInfo) -> Tuple[API, Dict[str, str]]:
        """Prepare the escalation request."""
        credentials = {
            "grant_type": "client_credentials",
            "client_id": client_info.client_id,
            "client_secret": client_info.client_secret,
            "scope": "openid",
        }
        return GET_TOKEN, credentials

    @staticmethod
    def process_response(raw_json: Dict[str, Any]) -> str:
        """Process escalation response to extract access token."""
        return AccessTokenResponse(**raw_json).access_token


class ImpersonateGetClientSecret:
    """Shared logic for retrieving client secrets."""

    @staticmethod
    def prepare_request(client_guid: str) -> str:
        """Prepare the get client secret request."""
        return GET_CLIENT_SECRET.format_path({"client_guid": client_guid})

    @staticmethod
    def process_response(raw_json: Any) -> Optional[str]:
        """Process client secret response."""
        return raw_json and raw_json.get("value")


class ImpersonateGetUserId:
    """Shared logic for retrieving user IDs from Keycloak."""

    @staticmethod
    def prepare_request(username: str) -> Tuple[API, Dict[str, str]]:
        """Prepare the get user ID request."""
        endpoint = GET_KEYCLOAK_USER.format_path_with_params()
        query_params = {"username": username or " "}
        return endpoint, query_params

    @staticmethod
    def process_response(raw_json: Any) -> Optional[str]:
        """Process user ID response."""
        return (
            raw_json
            and isinstance(raw_json, list)
            and len(raw_json) >= 1
            and raw_json[0].get("id")
            or None
        )
