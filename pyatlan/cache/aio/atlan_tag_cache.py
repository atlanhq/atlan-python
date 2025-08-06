# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Dict, Optional, Set

from pyatlan.cache.common import AtlanTagCacheCommon
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import AtlanTagDef

if TYPE_CHECKING:
    from pyatlan.client.aio import AsyncAtlanClient


class AsyncAtlanTagCache:
    """
    Async lazily-loaded cache for translating between Atlan-internal ID strings and human-readable names
    for Atlan tags.
    """

    def __init__(self, client: AsyncAtlanClient):
        self.client: AsyncAtlanClient = client
        self.cache_by_id: Dict[str, AtlanTagDef] = {}
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.deleted_ids: Set[str] = set()
        self.deleted_names: Set[str] = set()
        self.map_id_to_source_tags_attr_id: Dict[str, str] = {}
        self.lock: asyncio.Lock = asyncio.Lock()

    async def refresh_cache(self) -> None:
        """
        Refreshes the cache of Atlan tags by requesting the full set of Atlan tags from Atlan.
        """
        await self._refresh_cache()

    async def get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable Atlan tag name to its Atlan-internal ID string.

        :param name: human-readable name of the Atlan tag
        :returns: Atlan-internal ID string of the Atlan tag
        """
        return await self._get_id_for_name(name=name)

    async def get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal classification ID string to the human-readable Atlan tag name.

        :param idstr: Atlan-internal ID string of the Atlan tag
        :returns: human-readable name of the Atlan tag
        """
        return await self._get_name_for_id(idstr=idstr)

    async def get_source_tags_attr_id(self, id: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal Atlan tag ID string to the Atlan-internal name of the attribute that
        captures tag attachment details (for source-synced tags).

        :param id: Atlan-internal ID string of the Atlan tag
        :returns: Atlan-internal ID string of the attribute containing source-synced tag attachment details
        """
        return await self._get_source_tags_attr_id(id)

    async def _refresh_cache(self) -> None:
        """
        Refreshes the cache of Atlan tags by requesting the full set of Atlan tags from Atlan.
        """
        async with self.lock:
            # Make async API call directly
            response = await self.client.typedef.get(
                type_category=[
                    AtlanTypeCategory.CLASSIFICATION,
                    AtlanTypeCategory.STRUCT,
                ]
            )

            if not response or not response.struct_defs:
                raise ErrorCode.EXPIRED_API_TOKEN.exception_with_parameters()

            # Process response using shared logic
            (
                self.cache_by_id,
                self.map_id_to_name,
                self.map_name_to_id,
                self.map_id_to_source_tags_attr_id,
            ) = AtlanTagCacheCommon.refresh_cache_data(response)

    async def _get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable Atlan tag name to its Atlan-internal ID string.

        :param name: human-readable name of the Atlan tag
        :returns: Atlan-internal ID string of the Atlan tag
        """
        if not self.cache_by_id:
            await self._refresh_cache()
        result, should_refresh = AtlanTagCacheCommon.get_id_for_name(
            name, self.map_name_to_id, self.deleted_names
        )
        if should_refresh:
            await self._refresh_cache()
            return AtlanTagCacheCommon.get_id_for_name_after_refresh(
                name, self.map_name_to_id, self.deleted_names
            )
        return result

    async def _get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal classification ID string to the human-readable Atlan tag name.

        :param idstr: Atlan-internal ID string of the Atlan tag
        :returns: human-readable name of the Atlan tag
        """
        if not self.cache_by_id:
            await self._refresh_cache()
        result, should_refresh = AtlanTagCacheCommon.get_name_for_id(
            idstr, self.map_id_to_name, self.deleted_ids
        )
        if should_refresh:
            await self._refresh_cache()
            return AtlanTagCacheCommon.get_name_for_id_after_refresh(
                idstr, self.map_id_to_name, self.deleted_ids
            )
        return result

    async def _get_source_tags_attr_id(self, id: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal Atlan tag ID string to the Atlan-internal name of the attribute that
        captures tag attachment details (for source-synced tags).

        :param id: Atlan-internal ID string of the Atlan tag
        :returns: Atlan-internal ID string of the attribute containing source-synced tag attachment details
        """
        if not self.cache_by_id:
            await self._refresh_cache()
        result, should_refresh = AtlanTagCacheCommon.get_source_tags_attr_id(
            id, self.map_id_to_source_tags_attr_id, self.deleted_ids
        )
        if should_refresh:
            await self._refresh_cache()
            return AtlanTagCacheCommon.get_source_tags_attr_id_after_refresh(
                id, self.map_id_to_source_tags_attr_id, self.deleted_ids
            )
        return result
