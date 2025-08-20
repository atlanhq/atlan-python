# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Union

from pyatlan.cache.aio.abstract_asset_cache import AsyncAbstractAssetCache
from pyatlan.cache.connection_cache import (
    ConnectionName,  # Reuse the sync ConnectionName class
)
from pyatlan.model.assets import Asset, Connection
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.search import Term

if TYPE_CHECKING:
    from pyatlan.client.aio import AsyncAtlanClient

LOGGER = logging.getLogger(__name__)


class AsyncConnectionCache(AsyncAbstractAssetCache):
    """
    Async lazily-loaded cache for translating between
    a connection's simplified name its details.

    - guid = UUID of the connection
        for eg: 9c677e77-e01d-40e0-85b7-8ba4cd7d0ea9
    - qualified_name = Atlan-internal name of the connection (with epoch)
        for eg: default/snowflake/1234567890
    - name = simple name of the form {{connectorType}}/{{connectorName}},
        for eg: snowflake/development
    """

    _SEARCH_FIELDS = [
        Connection.NAME,
        Connection.STATUS,
        Connection.CONNECTOR_NAME,
    ]
    SEARCH_ATTRIBUTES = [field.atlan_field_name for field in _SEARCH_FIELDS]

    def __init__(self, client: AsyncAtlanClient):
        super().__init__(client)

    async def get_by_guid(self, guid: str, allow_refresh: bool = True) -> Connection:
        """
        Retrieve a connection from the cache by its UUID.
        If the asset is not found, it will be looked up and added to the cache.

        :param guid: UUID of the connection in Atlan
        :param allow_refresh: whether to allow a refresh of the cache (True) or not (False)
        :returns: connection (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the connection cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no UUID was provided for the connection to retrieve
        """
        return await self._get_by_guid(guid, allow_refresh)

    async def get_by_qualified_name(
        self, connection_qn: str, allow_refresh: bool = True
    ) -> Connection:
        """
        Retrieve a connection from the cache by its qualifiedName.
        If the asset is not found, it will be looked up and added to the cache.

        :param connection_qn: qualifiedName of the connection in Atlan
        :param allow_refresh: whether to allow a refresh of the cache (True) or not (False)
        :returns: connection (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the connection cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no qualified name was provided for the connection to retrieve
        """
        return await self._get_by_qualified_name(connection_qn, allow_refresh)

    async def get_by_name(
        self,
        name: Union[str, ConnectionName],
        allow_refresh: bool = True,
    ) -> Connection:
        """
        Retrieve a connection from the cache by its name.
        If the asset is not found, it will be looked up and added to the cache.

        :param name: name of the connection
        :param allow_refresh: whether to allow a refresh of the cache (True) or not (False)
        :returns: connection (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the connection cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no name was provided for the connection to retrieve
        """
        return await self._get_by_name(name, allow_refresh)

    async def lookup_by_guid(self, guid: str) -> None:
        if not guid:
            return
        async with self.lock:
            response = await (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Term.with_super_type_names("Asset"))
                .where(Connection.GUID.eq(guid))
                .execute_async(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            if candidate and isinstance(candidate, Connection):
                await self.cache(candidate)

    async def lookup_by_qualified_name(self, connection_qn: str) -> None:
        if not connection_qn:
            return
        async with self.lock:
            response = await (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Term.with_super_type_names("Asset"))
                .where(Connection.QUALIFIED_NAME.eq(connection_qn))
                .execute_async(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            if candidate and isinstance(candidate, Connection):
                await self.cache(candidate)

    async def lookup_by_name(self, name: ConnectionName) -> None:
        if not isinstance(name, ConnectionName):
            return
        async with self.lock:
            results = await self.client.asset.find_connections_by_name(
                name=name.name,  # type: ignore[arg-type]
                connector_type=name.type,  # type: ignore[arg-type]
                attributes=self.SEARCH_ATTRIBUTES,
            )
            if not results:
                return
            if len(results) > 1:
                LOGGER.warning(
                    (
                        "Found multiple connections of the same type with the same name, caching only the first: %s"
                    ),
                    name,
                )
            await self.cache(results[0])

    def get_name(self, asset: Asset):
        if not isinstance(asset, Connection):
            return
        return str(ConnectionName(asset))
