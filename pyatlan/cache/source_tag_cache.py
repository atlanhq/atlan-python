# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import logging
import threading
from typing import TYPE_CHECKING, Union

from pyatlan.cache.abstract_asset_cache import AbstractAssetCache, AbstractAssetName
from pyatlan.cache.connection_cache import ConnectionName
from pyatlan.errors import AtlanError
from pyatlan.model.assets import Asset, Tag
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.search import Term

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

lock = threading.Lock()
LOGGER = logging.getLogger(__name__)


class SourceTagCache(AbstractAssetCache):
    """
    Lazily-loaded cache for translating between
    source-synced tags and the qualifiedName of such.

    - guid = UUID of the source tag
        for eg: 9c677e77-e01d-40e0-85b7-8ba4cd7d0ea9
    - qualified_name = of the source tag (with epoch)
        for eg: default/snowflake/1234567890/DB/SCHEMA/TAG_NAME
    - name = simple name of the form {{connectorType}}/{{connectorName}}@@DB/SCHEMA/TAG_NAME
        for eg: snowflake/development@@DB/SCHEMA/TAG_NAME
    """

    _SEARCH_FIELDS = [Asset.NAME]
    SEARCH_ATTRIBUTES = [field.atlan_field_name for field in _SEARCH_FIELDS]

    def __init__(self, client: AtlanClient):
        super().__init__(client)

    def get_by_guid(self, guid: str, allow_refresh: bool = True) -> Tag:
        """
        Retrieve a source tag from the cache by its UUID.
        If the asset is not found, it will be looked up and added to the cache.

        :param guid: UUID of the source tag in Atlan
            for eg: 9c677e77-e01d-40e0-85b7-8ba4cd7d0ea9
        :returns: source tag (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the source tag cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no UUID was provided for the source tag to retrieve
        """
        return self._get_by_guid(guid=guid, allow_refresh=allow_refresh)

    def get_by_qualified_name(
        self, qualified_name: str, allow_refresh: bool = True
    ) -> Tag:
        """
        Retrieve a source tag from the cache by its unique Atlan-internal name.

        :param qualified_name: unique Atlan-internal name of the source tag
            for eg: default/snowflake/1234567890/DB/SCHEMA/TAG_NAME
        :param allow_refresh: whether to allow a refresh of the cache (`True`) or not (`False`)
        :param qualified_name: unique Atlan-internal name of the source tag
        :returns: source tag (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the source tag cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no qualified_name was provided for the source tag to retrieve
        """
        return self._get_by_qualified_name(
            qualified_name=qualified_name, allow_refresh=allow_refresh
        )

    def get_by_name(self, name: SourceTagName, allow_refresh: bool = True) -> Tag:
        """
        Retrieve an connection from the cache by its uniquely identifiable name.

        :param name: uniquely identifiable name of the connection in Atlan.
            In the form of {{connectorType}}/{{connectorName}}@@DB/SCHEMA/TAG_NAME
            for eg: snowflake/development@@DB/SCHEMA/TAG_NAME
        :param allow_refresh: whether to allow a refresh of the cache (`True`) or not (`False`)
        :returns: the connection (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the object cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no name was provided for the object to retrieve
        """
        return self._get_by_name(name=name, allow_refresh=allow_refresh)

    def lookup_by_guid(self, guid: str) -> None:
        if not guid:
            return
        with self.lock:
            response = (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Asset.SUPER_TYPE_NAMES.eq(Tag.__name__))
                .where(Asset.GUID.eq(guid))
                .execute(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            # NOTE: Checking if the first result is an "Asset" since in pyatlan,
            # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
            # preventing Dbt tags from being excluded from caching:
            if candidate and isinstance(candidate, Asset):
                self.cache(candidate)

    def lookup_by_qualified_name(self, source_tag_qn: str) -> None:
        if not source_tag_qn:
            return
        with self.lock:
            response = (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Asset.SUPER_TYPE_NAMES.eq(Tag.__name__))
                .where(Asset.QUALIFIED_NAME.eq(source_tag_qn))
                .execute(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            # NOTE: Checking if the first result is an "Asset" since in pyatlan,
            # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
            # preventing Dbt tags from being excluded from caching:
            if candidate and isinstance(candidate, Asset):
                self.cache(candidate)

    def lookup_by_name(self, stn: SourceTagName) -> None:
        if not isinstance(stn, SourceTagName):
            return
        connection_name = stn.connection
        connection_qn = self.client.connection_cache.get_by_name(
            connection_name  # type: ignore[arg-type]
        ).qualified_name
        source_tag_qn = f"{connection_qn}/{stn.partial_tag_name}"

        with self.lock:
            response = (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Asset.SUPER_TYPE_NAMES.eq(Tag.__name__))
                .where(Asset.QUALIFIED_NAME.eq(source_tag_qn))
                .execute(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            # NOTE: Checking if the first result is an "Asset" since in pyatlan,
            # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
            # preventing Dbt tags from being excluded from caching:
            if candidate and isinstance(candidate, Asset):
                self.cache(candidate)

    def get_name(self, asset: Asset):
        # NOTE: Checking if the first result is an "Asset" since in pyatlan,
        # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
        # preventing Dbt tags from being excluded from caching:
        if not isinstance(asset, Asset):
            return
        try:
            source_tag_name = str(SourceTagName(client=self.client, tag=asset))
        except AtlanError as e:
            LOGGER.error(
                "Unable to construct a source tag name for: %s", asset.qualified_name
            )
            LOGGER.debug("Details: %s", e)
        return source_tag_name


class SourceTagName(AbstractAssetName):
    """
    Unique identity for a source tag,
    in the form: {{connectorType}}/{{connectorName}}@@DB/SCHEMA/TAG_NAME

    - For eg: snowflake/development
    """

    _TYPE_NAME = "SourceTagAttachment"
    _CONNECTION_DELIMITER = "@@"

    def __init__(self, client: AtlanClient, tag: Union[str, Asset]):
        self.connection = None
        self.partial_tag_name = None

        # NOTE: Checking if the first result is an "Asset" since in pyatlan,
        # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
        # preventing Dbt tags from being excluded from caching:
        if isinstance(tag, Asset):
            source_tag_qn = tag.qualified_name or ""
            tokens = source_tag_qn.split("/")
            connection_qn = "/".join(tokens[:3]) if len(tokens) >= 3 else ""
            conn = client.connection_cache.get_by_qualified_name(connection_qn)
            self.connection = ConnectionName(conn)
            self.partial_tag_name = source_tag_qn[len(connection_qn) + 1 :]  # noqa

        elif isinstance(tag, str):
            tokens = tag.split(self._CONNECTION_DELIMITER)
            if len(tokens) == 2:
                self.connection = ConnectionName(tokens[0])
                self.partial_tag_name = tokens[1]

    def __str__(self):
        return f"{self.connection}{self._CONNECTION_DELIMITER}{self.partial_tag_name}"
