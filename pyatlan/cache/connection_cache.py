# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Optional, Union

from pyatlan.cache.abstract_asset_cache import AbstractAssetCache, AbstractAssetName
from pyatlan.model.assets import Asset, Connection
from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.search import Term

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

lock = threading.Lock()
LOGGER = logging.getLogger(__name__)


class ConnectionCache(AbstractAssetCache):
    """
    Lazily-loaded cache for translating between
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

    def __init__(self, client: AtlanClient):
        super().__init__(client)

    def get_by_guid(self, guid: str, allow_refresh: bool = True) -> Connection:
        """
        Retrieve a connection from the cache by its UUID.
        If the asset is not found, it will be looked up and added to the cache.

        :param guid: UUID of the connection in Atlan
            for eg: 9c677e77-e01d-40e0-85b7-8ba4cd7d0ea9
        :returns: connection (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the connection cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no UUID was provided for the connection to retrieve
        """
        return self._get_by_guid(guid=guid, allow_refresh=allow_refresh)

    def get_by_qualified_name(
        self, qualified_name: str, allow_refresh: bool = True
    ) -> Connection:
        """
        Retrieve a connection from the cache by its unique Atlan-internal name.

        :param qualified_name: unique Atlan-internal name of the connection
            for eg: default/snowflake/1234567890
        :param allow_refresh: whether to allow a refresh of the cache (`True`) or not (`False`)
        :param qualified_name: unique Atlan-internal name of the connection
        :returns: connection (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the connection cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no qualified_name was provided for the connection to retrieve
        """
        return self._get_by_qualified_name(
            qualified_name=qualified_name, allow_refresh=allow_refresh
        )

    def get_by_name(
        self, name: ConnectionName, allow_refresh: bool = True
    ) -> Connection:
        """
        Retrieve an connection from the cache by its uniquely identifiable name.

        :param name: uniquely identifiable name of the connection in Atlan
            In the form of {{connectorType}}/{{connectorName}}
            for eg: snowflake/development
        :param allow_refresh: whether to allow a refresh of the cache (`True`) or not (`False`)
        :returns: connection (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the connection cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no name was provided for the connection to retrieve
        """
        return self._get_by_name(name=name, allow_refresh=allow_refresh)

    def lookup_by_guid(self, guid: str) -> None:
        if not guid:
            return
        with self.lock:
            response = (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Term.with_super_type_names("Asset"))
                .where(Connection.GUID.eq(guid))
                .execute(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            if candidate and isinstance(candidate, Connection):
                self.cache(candidate)

    def lookup_by_qualified_name(self, connection_qn: str) -> None:
        if not connection_qn:
            return
        with self.lock:
            response = (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Term.with_super_type_names("Asset"))
                .where(Connection.QUALIFIED_NAME.eq(connection_qn))
                .execute(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            if candidate and isinstance(candidate, Connection):
                self.cache(candidate)

    def lookup_by_name(self, name: ConnectionName) -> None:
        if not isinstance(name, ConnectionName):
            return
        with self.lock:
            results = self.client.asset.find_connections_by_name(
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
            self.cache(results[0])

    def get_name(self, asset: Asset):
        if not isinstance(asset, Connection):
            return
        return str(ConnectionName(asset))


class ConnectionName(AbstractAssetName):
    """
    Unique identity for a connection,
    in the form: {{type}}/{{name}}

    - For eg: snowflake/development
    """

    _TYPE_NAME = "Connection"

    def __init__(
        self,
        connection: Union[
            str,
            Optional[Connection],
        ] = None,
    ):
        self.name = None
        self.type = None

        if isinstance(connection, Connection):
            self.name = connection.name
            self.type = connection.connector_name

        elif isinstance(connection, str):
            tokens = connection.split("/")
            if len(tokens) > 1:
                # Try enum conversion; fallback to custom connector if it fails
                try:
                    self.type = AtlanConnectorType(tokens[0]).value  # type: ignore[call-arg]
                    self.name = connection[len(tokens[0]) + 1 :]  # noqa
                except ValueError:
                    custom_connector = AtlanConnectorType.CREATE_CUSTOM(
                        # Ensure the enum name is converted to UPPER_SNAKE_CASE from kebab-case
                        name=tokens[0].replace("-", "_").upper(),
                        value=tokens[0],
                    )
                    self.type = custom_connector.value
                    self.name = connection[len(tokens[0]) + 1 :]

    def __hash__(self):
        return hash((self.name, self.type))

    def __str__(self):
        return f"{self.type}/{self.name}"

    def __eq__(self, other):
        if isinstance(other, ConnectionName):
            return self.name == other.name and self.type == other.type
        return False
