# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import threading
import time
from typing import Optional

import httpx
from authlib.oauth2.rfc6749 import OAuth2Token


class OAuthTokenManager:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        http_client: Optional[httpx.Client] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f"{self.base_url}/api/service/oauth-clients/token"
        self._lock = threading.Lock()
        self._http_client = http_client or httpx.Client(timeout=30.0)
        self._token: Optional[OAuth2Token] = None
        self._owns_client = http_client is None

    def get_token(self) -> str:
        with self._lock:
            if self._token and not self._token.is_expired():
                return self._token["access_token"]

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
        with self._lock:
            self._token = None

    def close(self):
        if self._owns_client:
            self._http_client.close()
