# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Union

from pyatlan.cache.abstract_asset_cache import (
    AbstractAssetName,  # Import base class for AsyncSourceTagName
)
from pyatlan.cache.aio.abstract_asset_cache import AsyncAbstractAssetCache
from pyatlan.cache.connection_cache import ConnectionName  # Reuse sync ConnectionName
from pyatlan.errors import AtlanError
from pyatlan.model.assets import Asset, Tag
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.search import Term

if TYPE_CHECKING:
    from pyatlan.client.aio import AsyncAtlanClient

LOGGER = logging.getLogger(__name__)


class AsyncSourceTagCache(AsyncAbstractAssetCache):
    """
    Async lazily-loaded cache for translating between
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

    def __init__(self, client: AsyncAtlanClient):
        super().__init__(client)

    async def get_by_guid(self, guid: str, allow_refresh: bool = True) -> Tag:
        """
        Retrieve a source tag from the cache by its UUID.
        If the asset is not found, it will be looked up and added to the cache.

        :param guid: UUID of the source tag in Atlan
        :returns: source tag (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the source tag cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no UUID was provided for the source tag to retrieve
        """
        return await self._get_by_guid(guid, allow_refresh)

    async def get_by_qualified_name(
        self, source_tag_qn: str, allow_refresh: bool = True
    ) -> Tag:
        """
        Retrieve a source tag from the cache by its qualifiedName.
        If the asset is not found, it will be looked up and added to the cache.

        :param source_tag_qn: qualifiedName of the source tag in Atlan
        :param allow_refresh: whether to allow a refresh of the cache (True) or not (False)
        :returns: source tag (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the source tag cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no qualified name was provided for the source tag to retrieve
        """
        return await self._get_by_qualified_name(source_tag_qn, allow_refresh)

    async def get_by_name(
        self,
        name: Union[str, AsyncSourceTagName],
        allow_refresh: bool = True,
    ) -> Tag:
        """
        Retrieve a source tag from the cache by its name.
        If the asset is not found, it will be looked up and added to the cache.

        :param name: name of the source tag
        :param allow_refresh: whether to allow a refresh of the cache (True) or not (False)
        :returns: source tag (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the source tag cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no name was provided for the source tag to retrieve
        """
        if isinstance(name, str):
            name = await AsyncSourceTagName.creator(self.client, name)
        return await self._get_by_name(name, allow_refresh)

    async def lookup_by_guid(self, guid: str) -> None:
        if not guid:
            return
        async with self.lock:
            response = await (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Asset.SUPER_TYPE_NAMES.eq(Tag.__name__))
                .where(Asset.GUID.eq(guid))
                .execute_async(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            # NOTE: Checking if the first result is an "Asset" since in pyatlan,
            # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
            # preventing Dbt tags from being excluded from caching:
            if candidate and isinstance(candidate, Asset):
                await self.cache(candidate)

    async def lookup_by_qualified_name(self, source_tag_qn: str) -> None:
        if not source_tag_qn:
            return
        async with self.lock:
            response = await (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Asset.SUPER_TYPE_NAMES.eq(Tag.__name__))
                .where(Asset.QUALIFIED_NAME.eq(source_tag_qn))
                .execute_async(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            # NOTE: Checking if the first result is an "Asset" since in pyatlan,
            # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
            # preventing Dbt tags from being excluded from caching:
            if candidate and isinstance(candidate, Asset):
                await self.cache(candidate)

    async def lookup_by_name(self, stn: AsyncSourceTagName) -> None:
        if not isinstance(stn, AsyncSourceTagName):
            return
        connection_name = stn.connection
        connection = await self.client.connection_cache.get_by_name(
            connection_name  # type: ignore[arg-type]
        )
        connection_qn = connection.qualified_name
        source_tag_qn = f"{connection_qn}/{stn.partial_tag_name}"

        async with self.lock:
            response = await (
                FluentSearch(_includes_on_results=self.SEARCH_ATTRIBUTES)
                .where(Term.with_state("ACTIVE"))
                .where(Asset.SUPER_TYPE_NAMES.eq(Tag.__name__))
                .where(Asset.QUALIFIED_NAME.eq(source_tag_qn))
                .execute_async(self.client)
            )
            candidate = (response.current_page() and response.current_page()[0]) or None
            # NOTE: Checking if the first result is an "Asset" since in pyatlan,
            # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
            # preventing Dbt tags from being excluded from caching:
            if candidate and isinstance(candidate, Asset):
                await self.cache(candidate)

    async def get_name(self, asset: Asset):
        # NOTE: Checking if the first result is an "Asset" since in pyatlan,
        # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
        # preventing Dbt tags from being excluded from caching:
        if not isinstance(asset, Asset):
            return
        try:
            source_tag_name = str(
                await AsyncSourceTagName.creator(client=self.client, tag=asset)
            )
        except AtlanError as e:
            LOGGER.error(
                "Unable to construct a source tag name for: %s", asset.qualified_name
            )
            LOGGER.debug("Details: %s", e)
            return None
        return source_tag_name


class AsyncSourceTagName(AbstractAssetName):
    """
    Async unique identity for a source tag,
    in the form: {{connectorType}}/{{connectorName}}@@DB/SCHEMA/TAG_NAME

    - For eg: snowflake/development@@DB/SCHEMA/TAG_NAME
    """

    _TYPE_NAME = "SourceTagAttachment"
    _CONNECTION_DELIMITER = "@@"

    def __init__(self):
        """
        Private constructor - use creator() class method for proper initialization.
        """
        self.connection = None
        self.partial_tag_name = None

    @classmethod
    async def creator(
        cls, client: AsyncAtlanClient, tag: Union[str, Asset]
    ) -> "AsyncSourceTagName":
        """
        Async creator method for AsyncSourceTagName.
        This is the exact async equivalent of the sync SourceTagName.__init__() logic.

        :param client: async Atlan client
        :param tag: either a string name or Asset object
        :returns: properly initialized AsyncSourceTagName instance
        """
        instance = cls()

        # NOTE: Checking if the first result is an "Asset" since in pyatlan,
        # "DbtTag" extends "Dbt" (unlike other tags like "SnowflakeTag" that extend the "Tag" model),
        # preventing Dbt tags from being excluded from caching:
        if isinstance(tag, Asset):
            source_tag_qn = tag.qualified_name or ""
            tokens = source_tag_qn.split("/")
            connection_qn = "/".join(tokens[:3]) if len(tokens) >= 3 else ""
            conn = await client.connection_cache.get_by_qualified_name(connection_qn)
            instance.connection = ConnectionName(conn)
            instance.partial_tag_name = source_tag_qn[len(connection_qn) + 1 :]  # noqa

        elif isinstance(tag, str):
            tokens = tag.split(cls._CONNECTION_DELIMITER)
            if len(tokens) == 2:
                instance.connection = ConnectionName(tokens[0])
                instance.partial_tag_name = tokens[1]

        return instance

    def __str__(self):
        return f"{self.connection}{self._CONNECTION_DELIMITER}{self.partial_tag_name}"
