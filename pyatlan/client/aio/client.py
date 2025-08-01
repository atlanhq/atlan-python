"""
Async Atlan Client
==================

Main async client that provides the same API as AtlanClient but with async/await support.
"""

from typing import Optional

import httpx
from pydantic.v1 import PrivateAttr

from pyatlan.client.atlan import AtlanClient

from .asset import AsyncAssetClient


class AsyncAtlanClient(AtlanClient):
    """
    Async Atlan client with the same API as sync AtlanClient.

    This client reuses all existing sync business logic while providing
    async/await support for all operations.

    Usage:
        # Same API as sync, just add await
        async_client = AsyncAtlanClient()
        results = await async_client.asset.search(criteria)  # vs sync: client.asset.search(criteria)

        # Or with context manager
        async with AsyncAtlanClient() as client:
            results = await client.asset.search(criteria)
    """

    _async_session: Optional[httpx.AsyncClient] = PrivateAttr(default=None)
    _async_asset_client: Optional[AsyncAssetClient] = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        # Initialize sync client (handles all validation, env vars, etc.)
        super().__init__(**kwargs)

    @property
    def asset(self) -> AsyncAssetClient:
        """Get async asset client with same API as sync"""
        if self._async_asset_client is None:
            self._async_asset_client = AsyncAssetClient(self)
        return self._async_asset_client

    def _get_async_session(self) -> httpx.AsyncClient:
        """Get or create async HTTP session"""
        if self._async_session is None:
            self._async_session = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                headers={"authorization": f"Bearer {self.api_key}"},
                base_url=str(self.base_url),
            )
        return self._async_session

    async def _call_api(
        self, api, query_params=None, request_obj=None, exclude_unset=True
    ):
        """
        Async version of _call_api that reuses sync client's logic.

        Pattern for reuse:
        1. Use sync client to prepare request (same validation, serialization)
        2. Make async HTTP call
        3. Return JSON for sync client's response processing
        """
        # Step 1: Reuse sync client's request preparation
        path = self._create_path(api)
        params = self._create_params(api, query_params, request_obj, exclude_unset)

        # Step 2: Make async HTTP call
        session = self._get_async_session()
        response = await session.request(
            api.method.value,
            path,
            **{k: v for k, v in params.items() if k != "headers"},
            headers={**session.headers, **params.get("headers", {})},
            timeout=httpx.Timeout(self.read_timeout),
        )
        response.raise_for_status()

        # Step 3: Return JSON for sync client's response processing
        return response.json()

    async def aclose(self):
        """Close async resources"""
        if self._async_session:
            await self._async_session.aclose()
            self._async_session = None
        if self._async_asset_client:
            self._async_asset_client = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
