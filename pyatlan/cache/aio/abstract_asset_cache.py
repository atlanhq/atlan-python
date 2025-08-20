# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, Dict

from pyatlan.cache.abstract_asset_cache import AbstractAssetName
from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.enums import AtlanConnectorType

if TYPE_CHECKING:
    from pyatlan.client.aio import AsyncAtlanClient


class AsyncAbstractAssetCache(ABC):
    """
    Async base class for reusable components that are common
    to all caches, where a cache is populated entry-by-entry.
    """

    def __init__(self, client: AsyncAtlanClient):
        self.client = client
        self.lock = asyncio.Lock()
        self.name_to_guid: Dict[str, str] = dict()
        self.guid_to_asset: Dict[str, Asset] = dict()
        self.qualified_name_to_guid: Dict[str, str] = dict()

    @abstractmethod
    async def lookup_by_guid(self, guid: str):
        """Abstract method to lookup asset by guid."""

    @abstractmethod
    async def lookup_by_qualified_name(self, qualified_name: str):
        """Abstract method to lookup asset by qualified name."""

    @abstractmethod
    async def lookup_by_name(self, name: Any):
        """Abstract method to lookup asset by name."""

    @abstractmethod
    def get_name(self, asset: Asset):
        """Abstract method to get name from asset."""

    def is_guid_known(self, guid: str) -> bool:
        """
        Checks whether the provided Atlan-internal UUID is known.
        NOTE: will not refresh the cache itself to determine this.

        :param guid: Atlan-internal UUID of the object
        :returns: `True` if the object is known, `False` otherwise
        """
        return guid in self.guid_to_asset

    def is_qualified_name_known(self, qualified_name: str) -> bool:
        """
        Checks whether the provided Atlan-internal ID string is known.
        NOTE: will not refresh the cache itself to determine this.

        :param qualified_name: Atlan-internal ID string of the object
        :returns: `True` if the object is known, `False` otherwise
        """
        return qualified_name in self.qualified_name_to_guid

    def is_name_known(self, name: str) -> bool:
        """
        Checks whether the provided Atlan-internal ID string is known.
        NOTE: will not refresh the cache itself to determine this.

        :param name: human-constructable name of the object
        :returns: `True` if the object is known, `False` otherwise
        """
        return name in self.name_to_guid

    async def cache(self, asset: Asset):
        """
        Add an entry to the cache.

        :param asset: to be cached
        """
        name_result = asset and self.get_name(asset)
        if asyncio.iscoroutine(name_result):
            name = await name_result
        else:
            name = name_result
        if not all([name, asset.guid, asset.qualified_name]):
            return
        self.name_to_guid[name] = asset.guid  # type: ignore[index]
        self.guid_to_asset[asset.guid] = asset  # type: ignore[index]
        self.qualified_name_to_guid[asset.qualified_name] = asset.guid  # type: ignore[index]

    async def _get_by_guid(self, guid: str, allow_refresh: bool = True):
        """
        Retrieve an asset from the cache by its UUID.

        :param guid: UUID of the asset in Atlan
        :param allow_refresh: whether to allow a refresh of the cache (`True`) or not (`False`)
        :returns: the asset (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the object cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no UUID was provided for the object to retrieve
        """
        if not guid:
            raise ErrorCode.MISSING_ID.exception_with_parameters()
        asset = self.guid_to_asset.get(guid)
        if not asset and allow_refresh:
            await self.lookup_by_guid(guid)
            asset = self.guid_to_asset.get(guid)
        if not asset:
            raise ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters(guid)
        return asset

    async def _get_by_qualified_name(
        self, qualified_name: str, allow_refresh: bool = True
    ):
        """
        Retrieve an asset from the cache by its qualifiedName.

        :param qualified_name: qualifiedName of the asset in Atlan
        :param allow_refresh: whether to allow a refresh of the cache (`True`) or not (`False`)
        :returns: the asset (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the object cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no qualified name was provided for the object to retrieve
        """
        if not qualified_name:
            raise ErrorCode.MISSING_ID.exception_with_parameters()
        guid = self.qualified_name_to_guid.get(qualified_name)
        if not guid and allow_refresh:
            await self.lookup_by_qualified_name(qualified_name)
            guid = self.qualified_name_to_guid.get(qualified_name)
        if not guid:
            raise ErrorCode.ASSET_NOT_FOUND_BY_QN.exception_with_parameters(
                qualified_name,
                AtlanConnectorType._get_connector_type_from_qualified_name(
                    qualified_name
                ).value,
            )

        return await self._get_by_guid(guid=guid, allow_refresh=False)

    async def _get_by_name(self, name, allow_refresh: bool = True):
        """
        Retrieve an asset from the cache by its uniquely identifiable name.

        :param name: uniquely identifiable name of the asset in Atlan
        :param allow_refresh: whether to allow a refresh of the cache (`True`) or not (`False`)
        :returns: the asset (if found)
        :raises AtlanError: on any API communication problem if the cache needs to be refreshed
        :raises NotFoundError: if the object cannot be found (does not exist) in Atlan
        :raises InvalidRequestError: if no name was provided for the object to retrieve
        """
        if not isinstance(name, AbstractAssetName):
            raise ErrorCode.MISSING_NAME.exception_with_parameters()
        guid = self.name_to_guid.get(str(name))
        if not guid and allow_refresh:
            await self.lookup_by_name(name)
            guid = self.name_to_guid.get(str(name))
        if not guid:
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                name._TYPE_NAME, name
            )

        return await self._get_by_guid(guid=guid, allow_refresh=False)
