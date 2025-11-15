# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
import asyncio
import time
from typing import Optional

import httpx
from authlib.oauth2.rfc6749 import OAuth2Token

from pyatlan.client.constants import GET_OAUTH_CLIENT
from pyatlan.utils import API


class AsyncOAuthTokenManager:
    def __init__(
        self,
        base_url: str,
        client_id: str,
        client_secret: str,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token_url = self._create_path(GET_OAUTH_CLIENT)
        self._lock = asyncio.Lock()
        self._http_client = http_client or httpx.AsyncClient(timeout=30.0)
        self._token: Optional[OAuth2Token] = None
        self._owns_client = http_client is None

    async def get_token(self) -> str:
        async with self._lock:
            if self._token and not self._token.is_expired():
                return str(self._token["access_token"])

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

    def _create_path(self, api: API):
        from urllib.parse import urljoin

        if self.base_url == "INTERNAL":
            base_with_prefix = urljoin(api.endpoint.service, api.endpoint.prefix)
            return urljoin(base_with_prefix, api.path)
        else:
            base_with_prefix = urljoin(self.base_url, api.endpoint.prefix)
            return urljoin(base_with_prefix, api.path)

    async def aclose(self):
        if self._owns_client:
            await self._http_client.aclose()
