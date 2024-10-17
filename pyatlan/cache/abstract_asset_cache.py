# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

import threading
from abc import ABC, abstractmethod
from typing import Any, Dict

from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.enums import AtlanConnectorType


class AbstractAssetCache(ABC):

    def __init__(self, client):
        self.client = client
        self.qualified_name_to_guid: Dict[str, str] = {}
        self.name_to_guid: Dict[str, str] = {}
        self.guid_to_asset: Dict[str, Any] = {}
        self.lock = threading.Lock()

    @classmethod
    @abstractmethod
    def get_cache(cls):
        """Abstract method to retreive cache."""

    @abstractmethod
    def lookup_by_guid(self, guid):
        """Abstract method to lookup asset by guid."""

    @abstractmethod
    def lookup_by_qualified_name(self, qualified_name):
        """Abstract method to lookup asset by qualified name."""

    @abstractmethod
    def lookup_by_name(self, name):
        """Abstract method to lookup asset by name."""

    @abstractmethod
    def get_name(self, asset):
        """Abstract method to get name from asset."""

    def cache(self, asset: Asset):
        name = asset and self.get_name(asset)
        if name:
            guid = asset.guid
            qn = asset.qualified_name
            self.name_to_guid[name] = guid
            self.guid_to_asset[guid] = asset
            self.qualified_name_to_guid[qn] = guid

    def _get_by_guid(self, guid, allow_refresh=True):
        if not guid:
            raise ErrorCode.MISSING_ID.exception_with_parameters()
        asset = self.guid_to_asset.get(guid)
        if asset is None and allow_refresh:
            self.lookup_by_guid(guid)
            asset = self.guid_to_asset.get(guid)
        if asset is None:
            raise ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters(guid)
        return asset

    def _get_by_qualified_name(self, qualified_name, allow_refresh=True):
        if qualified_name:
            guid = self.qualified_name_to_guid.get(qualified_name)
            if guid is None and allow_refresh:
                self.lookup_by_qualified_name(qualified_name)
                guid = self.qualified_name_to_guid.get(qualified_name)
            if guid is None:
                raise ErrorCode.ASSET_NOT_FOUND_BY_QN.exception_with_parameters(
                    qualified_name,
                    AtlanConnectorType.get_connector_name(qualified_name),
                )
            return self._get_by_guid(guid, False)
        else:
            raise ErrorCode.MISSING_ID.exception_with_parameters()

    def _get_by_name(self, name, allow_refresh=True):
        if name:
            guid = self.name_to_guid.get(name)
            if guid is None and allow_refresh:
                self.lookup_by_name(name)
                guid = self.name_to_guid.get(name)
            if guid is None:
                raise ErrorCode.ASSET_NOT_FOUND_BY_NAME.exception_with_parameters(name)
            return self._get_by_guid(guid, False)
        else:
            raise ErrorCode.MISSING_NAME.exception_with_parameters()

    def is_guid_known(self, guid):
        return guid in self.guid_to_asset

    def is_qualified_name_known(self, qualified_name):
        return qualified_name in self.qualified_name_to_guid

    def is_name_known(self, name):
        return name in self.name_to_guid
