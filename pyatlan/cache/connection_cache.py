# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import logging
import threading
from typing import Dict, Optional

from pyatlan.cache.abstract_asset_cache import AbstractAssetCache
from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Asset, Connection
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fluent_search import FluentSearch

logger = logging.getLogger(__name__)

lock = threading.Lock()


class ConnectionCache(AbstractAssetCache):

    _CONNECTION_ATTRIBUTES = [
        Connection.NAME,
        Connection.STATUS,
        Connection.CONNECTOR_NAME,
    ]
    caches: Dict[int, ConnectionCache] = dict()

    def __init__(self, client: AtlanClient):
        super().__init__(client)

    @classmethod
    def get_cache(cls) -> ConnectionCache:
        from pyatlan.client.atlan import AtlanClient

        with lock:
            default_client = AtlanClient.get_default_client()
            cache_key = default_client.cache_key
            if cache_key not in cls.caches:
                cls.caches[cache_key] = ConnectionCache(client=default_client)
            return cls.caches[cache_key]

    @classmethod
    def get_by_guid(cls, guid: str, allow_refresh: bool = True) -> Connection:
        return cls.get_cache()._get_by_guid(guid=guid, allow_refresh=allow_refresh)

    @classmethod
    def get_by_qualified_name(
        cls, qualified_name: str, allow_refresh: bool = True
    ) -> Connection:
        return cls.get_cache()._get_by_qualified_name(
            qualified_name=qualified_name, allow_refresh=allow_refresh
        )

    @classmethod
    def get_by_name(cls, name: str, allow_refresh: bool = True) -> Connection:
        return cls.get_cache()._get_by_name(name=name, allow_refresh=allow_refresh)

    def lookup_by_guid(self, guid: Optional[str]) -> None:
        if not guid:
            return
        with self.lock:
            response = (
                FluentSearch(_includes_on_results=self._CONNECTION_ATTRIBUTES)
                .select()
                .where(Connection.GUID.eq(guid))
                .execute(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            if candidate and isinstance(candidate, Connection):
                self.cache(candidate)

    def lookup_by_qualified_name(self, connection_qn: Optional[str]) -> None:
        if not connection_qn:
            return
        with self.lock:
            response = (
                FluentSearch(_includes_on_results=self._CONNECTION_ATTRIBUTES)
                .select()
                .where(Connection.QUALIFIED_NAME.eq(connection_qn))
                .execute(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            if candidate and isinstance(candidate, Connection):
                self.cache(candidate)

    def lookup_by_name(self, name) -> None:
        if isinstance(name, ConnectionName):
            results = self.client.asset.find_connections_by_name(
                name=name.name,
                connector_type=name.type,
                attributes=self._CONNECTION_ATTRIBUTES,
            )
            if results:
                if len(results) > 1:
                    logger.warning(
                        "Found multiple connections of the same type with the same name, caching only the first: %s",
                        name,
                    )
                self.cache(results[0])

    def get_name(self, asset: Asset):
        if isinstance(asset, Connection):
            return ConnectionName(asset)


class ConnectionName(object):

    def __init__(
        self, connection: Optional[Connection] = None, identity: Optional[str] = None
    ):
        self.name = None
        self.type = None

        if connection:
            self.name = connection.name
            self.type = connection.connection_name

        elif identity:
            tokens = identity.split("/")
            if len(tokens) > 1:
                self.type = AtlanConnectorType(tokens[0])
                self.name = identity[len(tokens[0]) + 1 :]  # noqa

    def __eq__(self, other):
        if isinstance(other, ConnectionName):
            return self.name == other.name and self.type == other.type
        return False

    def __hash__(self):
        return hash((self.name, self.type))

    def __str__(self):
        return f"{self.type}/{self.name}"
