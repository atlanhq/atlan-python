# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Dict, Optional

from pyatlan.cache.common.dq_template_config_cache import DQTemplateConfigCacheCommon

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient


class AsyncDQTemplateConfigCache:
    """
    Lazily-loaded async cache for DQ rule template configurations to avoid multiple API calls.
    """

    def __init__(self, client: AsyncAtlanClient):
        self.client: AsyncAtlanClient = client
        self._cache: Dict[str, Dict] = {}
        self._lock: asyncio.Lock = asyncio.Lock()
        self._initialized: bool = False

    async def refresh_cache(self) -> None:
        """
        Refreshes the cache of DQ template configurations by requesting the full set from Atlan.
        """
        await self._refresh_cache()

    async def get_template_config(self, rule_type: str) -> Optional[Dict]:
        """
        Get template configuration for a specific rule type.

        :param rule_type: The display name of the rule type
        :returns: Template configuration dict or None if not found
        """
        if not self._initialized:
            await self._refresh_cache()

        return self._cache.get(rule_type)

    async def _refresh_cache(self) -> None:
        """Refresh the cache by fetching all template configurations."""
        async with self._lock:
            if self._initialized:
                return

            try:
                search_request = DQTemplateConfigCacheCommon.prepare_search_request()
                request = search_request.to_request()
                results = await self.client.asset.search(request)

                success, error = DQTemplateConfigCacheCommon.process_search_results(
                    results, self._cache
                )

                if success:
                    self._initialized = True
                else:
                    # If cache refresh fails, mark as initialized to prevent infinite retries
                    self._initialized = True
                    if error:
                        raise error
            except Exception:
                # If cache refresh fails, mark as initialized to prevent infinite retries
                self._initialized = True
                raise
