# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from __future__ import annotations

import threading
from abc import ABC, abstractmethod
from typing import Any

from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.enums import AtlanConnectorType


class AbstractAssetCache(ABC):

    def __init__(self, client):
        self.client = client
        self.lock = threading.Lock()
        self.name_to_guid = dict()
        self.guid_to_asset = dict()
        self.qualified_name_to_guid = dict()

    @classmethod
    @abstractmethod
    def get_cache(cls):
        """Abstract method to retreive cache."""

    @abstractmethod
    def lookup_by_guid(self, guid: str):
        """Abstract method to lookup asset by guid."""

    @abstractmethod
    def lookup_by_qualified_name(self, qualified_name: str):
        """Abstract method to lookup asset by qualified name."""

    @abstractmethod
    def lookup_by_name(self, name: Any):
        """Abstract method to lookup asset by name."""

    @abstractmethod
    def get_name(self, asset: Asset):
        """Abstract method to get name from asset."""

    def is_guid_known(self, guid: str):
        return guid in self.guid_to_asset

    def is_qualified_name_known(self, qualified_name: str):
        return qualified_name in self.qualified_name_to_guid

    def is_name_known(self, name: str):
        return name in self.name_to_guid

    def cache(self, asset: Asset):
        name = asset and self.get_name(asset)
        if not all([name, asset.guid, asset.qualified_name]):
            return
        self.name_to_guid[name] = asset.guid
        self.guid_to_asset[asset.guid] = asset
        self.qualified_name_to_guid[asset.qualified_name] = asset.guid

    def _get_by_guid(self, guid: str, allow_refresh: bool = True):
        if not guid:
            raise ErrorCode.MISSING_ID.exception_with_parameters()
        asset = self.guid_to_asset.get(guid)
        if not asset and allow_refresh:
            self.lookup_by_guid(guid)
            asset = self.guid_to_asset.get(guid)
        if not asset:
            raise ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters(guid)
        return asset

    def _get_by_qualified_name(self, qualified_name: str, allow_refresh: bool = True):
        if not qualified_name:
            raise ErrorCode.MISSING_ID.exception_with_parameters()
        guid = self.qualified_name_to_guid.get(qualified_name)
        if not guid and allow_refresh:
            self.lookup_by_qualified_name(qualified_name)
            guid = self.qualified_name_to_guid.get(qualified_name)
        if not guid:
            raise ErrorCode.ASSET_NOT_FOUND_BY_QN.exception_with_parameters(
                qualified_name,
                AtlanConnectorType._get_connector_type_from_qualified_name(
                    qualified_name
                ),
            )
        return self._get_by_guid(guid=guid, allow_refresh=False)

    def _get_by_name(self, name: AbstractAssetName, allow_refresh: bool = True):
        if not isinstance(name, AbstractAssetName):
            raise ErrorCode.MISSING_NAME.exception_with_parameters()
        guid = self.name_to_guid.get(str(name))
        if not guid and allow_refresh:
            self.lookup_by_name(name)
            guid = self.name_to_guid.get(str(name))
        if not guid:
            raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(
                name._TYPE_NAME, name
            )
        return self._get_by_guid(guid=guid, allow_refresh=False)


class AbstractAssetName(ABC):
    _TYPE_NAME = ""

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __str__(self):
        pass
