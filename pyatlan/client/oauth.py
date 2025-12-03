# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import threading
import time
from typing import Optional
from urllib.parse import urljoin

import httpx
from authlib.oauth2.rfc6749 import OAuth2Token

from pyatlan.client.constants import GET_OAUTH_CLIENT
from pyatlan.utils import API


class OAuthTokenManager:
    """
    Manages OAuth tokens for HTTP clients.
    :param base_url: Base URL of the Atlan tenant.
    :param client_id: OAuth client ID.
    :param client_secret: OAuth client secret.
    :param http_client: Optional HTTP client to use.
    :param connect_timeout: Timeout for establishing connections.
    :param read_timeout: Timeout for reading data.
    :param write_timeout: Timeout for writing data.
    :param pool_timeout: Timeout for acquiring a connection from the pool.
    """

    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        http_client: Optional[httpx.Client] = None,
        connect_timeout: float = 30.0,
        read_timeout: float = 900.0,
        write_timeout: float = 30.0,
        pool_timeout: float = 30.0,
    ):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = self._create_path(GET_OAUTH_CLIENT)
        self._lock = threading.Lock()
        self._http_client = http_client or httpx.Client(
            timeout=httpx.Timeout(
                connect=connect_timeout,
                read=read_timeout,
                write=write_timeout,
                pool=pool_timeout,
            )
        )
        self._token: Optional[OAuth2Token] = None
        self._owns_client = http_client is None

    def get_token(self) -> str:
        """
        Retrieves a valid OAuth token, refreshing it if necessary.
        """
        with self._lock:
            if self._token and not self._token.is_expired():
                return str(self._token["access_token"])

            response = self._http_client.post(
                self.token_url,
                json={
                    "clientId": self.client_id,
                    "clientSecret": self.client_secret,
                },
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()

            data = response.json()
            access_token = data.get("accessToken") or data.get("access_token")

            if not access_token:
                raise ValueError(
                    f"OAuth token response missing 'accessToken' field. "
                    f"Response keys: {list(data.keys())}"
                )

            expires_in = data.get("expiresIn") or data.get("expires_in", 600)

            self._token = OAuth2Token(
                {
                    "access_token": access_token,
                    "token_type": data.get("tokenType")
                    or data.get("token_type", "Bearer"),
                    "expires_in": expires_in,
                    "expires_at": int(time.time()) + expires_in,
                }
            )

            return access_token

    def invalidate_token(self):
        """
        Invalidates the current OAuth token.
        """
        with self._lock:
            self._token = None

    def _create_path(self, api: API):
        """
        Creates the full URL for the given API endpoint.
        """
        if self.base_url == "INTERNAL":
            return urljoin(api.endpoint.service, api.path)
        else:
            base_with_prefix = urljoin(self.base_url, api.endpoint.prefix)
            return urljoin(base_with_prefix, api.path)

    def close(self):
        """
        Closes the underlying HTTP client if owned by this manager.
        """
        if self._owns_client:
            self._http_client.close()
