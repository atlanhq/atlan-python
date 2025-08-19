# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Dict, Iterable, Optional

from pyatlan.cache.common import GroupCacheCommon

if TYPE_CHECKING:
    from pyatlan.client.aio import AsyncAtlanClient


class AsyncGroupCache:
    """
    Async lazily-loaded cache for translating Atlan-internal groups into their various IDs.
    """

    def __init__(self, client: AsyncAtlanClient):
        self.client: AsyncAtlanClient = client
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.map_alias_to_id: Dict[str, str] = {}
        self.lock: asyncio.Lock = asyncio.Lock()

    async def get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided internal group name to its GUID.

        :param name: human-readable name of the group
        :returns: unique identifier (GUID) of the group
        """
        return await self._get_id_for_name(name=name)

    async def get_id_for_alias(self, alias: str) -> Optional[str]:
        """
        Translate the provided human-readable group name to its GUID.

        :param alias: name of the group as it appears in the UI
        :returns: unique identifier (GUID) of the group
        """
        return await self._get_id_for_alias(alias=alias)

    async def get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided group GUID to the internal group name.

        :param idstr: unique identifier (GUID) of the group
        :returns: internal name of the group
        """
        return await self._get_name_for_id(idstr=idstr)

    async def validate_names(self, names: Iterable[str]):
        """
        Validate that the given internal group names are valid. A ValueError will be raised in any are not.

        :param names: a collection of internal group names to be checked
        """
        for group_name in names:
            if not await self.get_id_for_name(group_name):
                raise ValueError(
                    f"Provided group name {group_name} was not found in Atlan."
                )

    async def validate_aliases(self, aliases: Iterable[str]):
        """
        Validate that the given human-readable group names are valid. A ValueError will be raised in any are not.

        :param aliases: a collection of group names (as they appear in the UI) to be checked
        """
        for group_alias in aliases:
            if not await self.get_id_for_alias(group_alias):
                raise ValueError(
                    f"Provided group alias {group_alias} was not found in Atlan."
                )

    async def refresh_cache(self) -> None:
        """
        Refreshes the cache of groups by requesting the full set of groups from Atlan.
        """
        await self._refresh_cache()

    async def _refresh_cache(self) -> None:
        async with self.lock:
            groups = await self.client.group.get_all()
            if not groups:
                return
            # Process response using shared logic - extract records from response
            group_list = groups.records or []
            (self.map_id_to_name, self.map_name_to_id, self.map_alias_to_id) = (
                GroupCacheCommon.refresh_cache_data(group_list)
            )

    async def _get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided internal group name to its GUID.

        :param name: internal name of the group
        :returns: unique identifier (GUID) of the group
        """
        if group_id := self.map_name_to_id.get(name):
            return group_id
        await self._refresh_cache()
        return self.map_name_to_id.get(name)

    async def _get_id_for_alias(self, alias: str) -> Optional[str]:
        """
        Translate the provided human-readable group name to its GUID.

        :param alias: name of the group as it appears in the UI
        :returns: unique identifier (GUID) of the group
        """
        if group_id := self.map_alias_to_id.get(alias):
            return group_id
        await self._refresh_cache()
        return self.map_alias_to_id.get(alias)

    async def _get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided group GUID to the internal group name.

        :param idstr: unique identifier (GUID) of the group
        :returns: internal name of the group
        """
        if group_name := self.map_id_to_name.get(idstr):
            return group_name
        await self._refresh_cache()
        return self.map_id_to_name.get(idstr)
