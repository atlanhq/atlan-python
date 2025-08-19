# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, Dict, Iterable, Optional

from pyatlan.cache.common import UserCacheCommon
from pyatlan.errors import ErrorCode
from pyatlan.model.constants import SERVICE_ACCOUNT_

if TYPE_CHECKING:
    from pyatlan.client.aio import AsyncAtlanClient


class AsyncUserCache:
    """
    Async lazily-loaded cache for translating Atlan-internal users into their various IDs.
    """

    def __init__(self, client: AsyncAtlanClient):
        self.client: AsyncAtlanClient = client
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.map_email_to_id: Dict[str, str] = {}
        self.lock: asyncio.Lock = asyncio.Lock()

    async def get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable username to its GUID.

        :param name: human-readable name of the user
        :returns: unique identifier (GUID) of the user
        """
        return await self._get_id_for_name(name=name)

    async def get_id_for_email(self, email: str) -> Optional[str]:
        """
        Translate the provided email to its GUID.

        :param email: email address of the user
        :returns: unique identifier (GUID) of the user
        """
        return await self._get_id_for_email(email=email)

    async def get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided user GUID to the human-readable username.

        :param idstr: unique identifier (GUID) of the user
        :returns: username of the user
        """
        return await self._get_name_for_id(idstr=idstr)

    async def validate_names(self, names: Iterable[str]):
        """
        Validate that the given human-readable usernames are valid. A ValueError will be raised in any are not.

        :param names: a collection of usernames to be checked
        """
        for username in names:
            if not await self.get_id_for_name(
                username
            ) and not await self.client.token.get_by_id(username):
                raise ValueError(
                    f"Provided username {username} was not found in Atlan."
                )

    async def refresh_cache(self) -> None:
        """
        Refreshes the cache of users by requesting the full set of users from Atlan.
        """
        await self._refresh_cache()

    async def _refresh_cache(self) -> None:
        async with self.lock:
            users = await self.client.user.get_all()
            if not users:
                return
            # Process response using shared logic - extract records from response
            user_list = users.records or []
            (self.map_id_to_name, self.map_name_to_id, self.map_email_to_id) = (
                UserCacheCommon.refresh_cache_data(user_list)
            )

    async def _get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable username to its GUID.

        :param name: human-readable name of the user
        :returns: unique identifier (GUID) of the user
        """
        if user_id := self.map_name_to_id.get(name):
            return user_id
        # If we are translating an API token,
        # short-circuit any further cache refresh
        if name.startswith(SERVICE_ACCOUNT_):
            token = await self.client.token.get_by_id(client_id=name)
            if token and token.guid:
                self.map_name_to_id[name] = token.guid
                return token.guid
            else:
                raise ErrorCode.API_TOKEN_NOT_FOUND_BY_NAME.exception_with_parameters(
                    name
                )
        await self._refresh_cache()
        return self.map_name_to_id.get(name)

    async def _get_id_for_email(self, email: str) -> Optional[str]:
        """
        Translate the provided email to its GUID.

        :param email: email address of the user
        :returns: unique identifier (GUID) of the user
        """
        if user_id := self.map_email_to_id.get(email):
            return user_id
        await self._refresh_cache()
        return self.map_email_to_id.get(email)

    async def _get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided user GUID to the human-readable username.

        :param idstr: unique identifier (GUID) of the user
        :returns: username of the user
        """
        if username := self.map_id_to_name.get(idstr):
            return username
        # If the username isn't found, check if it is an API token
        token = await self.client.token.get_by_guid(guid=idstr)
        if token and token.client_id:
            return token.username
        else:
            await self._refresh_cache()
            return self.map_id_to_name.get(idstr)
