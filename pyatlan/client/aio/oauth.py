# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import asyncio
import time
from typing import Optional

import httpx
from authlib.oauth2.rfc6749 import OAuth2Token


class AsyncOAuthTokenManager:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = f"{self.base_url}/api/service/oauth-clients/token"
        self._lock = asyncio.Lock()
        self._http_client = http_client or httpx.AsyncClient(timeout=30.0)
        self._token: Optional[OAuth2Token] = None
        self._owns_client = http_client is None

    async def get_token(self) -> str:
        async with self._lock:
            if self._token and not self._token.is_expired():
                return self._token["access_token"]

            response = await self._http_client.post(
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

    async def invalidate_token(self):
        async with self._lock:
            self._token = None

    async def aclose(self):
        if self._owns_client:
            await self._http_client.aclose()
