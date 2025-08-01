"""
Async Atlan Client (AIO)
========================

This module provides async versions of all Atlan client functionality
with the same API as the sync versions, just requiring await.

Pattern: All async methods reuse shared business logic from pyatlan.client.shared
to ensure identical behavior with sync clients.

Usage:
    from pyatlan.client.aio import AsyncAtlanClient

    async with AsyncAtlanClient() as client:
        results = await client.asset.search(criteria)

        # Async iteration through paginated results
        async for asset in results:
            print(asset.name)
"""

from .asset import AsyncAssetClient
from .client import AsyncAtlanClient
from .results import (
    AsyncIndexSearchResults,
    AsyncLineageListResults,
    AsyncSearchResults,
    SimpleConcurrentAsyncIndexSearchResults,
)

__all__ = [
    "AsyncAtlanClient",
    "AsyncAssetClient",
    "AsyncIndexSearchResults",
    "AsyncLineageListResults",
    "AsyncSearchResults",
    "SimpleConcurrentAsyncIndexSearchResults",
]
