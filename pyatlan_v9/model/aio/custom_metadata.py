# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from collections import UserDict
from typing import TYPE_CHECKING, Any, Union

from pyatlan.errors import NotFoundError
from pyatlan.model.constants import DELETED_, DELETED_SENTINEL

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient


class AsyncCustomMetadataDict(UserDict):
    """
    Async version of CustomMetadataDict for manipulating custom metadata
    attributes using human-readable names.

    Recommended usage:
        custom_metadata = await AsyncCustomMetadataDict.creator(client=client, name="set_name")
        custom_metadata["attribute_name"] = "value"
    """

    _sentinel: Union[AsyncCustomMetadataDict, None] = None

    def __new__(cls, *args, **kwargs):
        if args and args[0] == DELETED_SENTINEL and cls._sentinel:
            return cls._sentinel
        obj = super().__new__(cls)
        super().__init__(obj)
        if args and args[0] == DELETED_SENTINEL:
            obj._name = DELETED_
            obj._modified = False
            obj._names: set[str] = set()
            cls._sentinel = obj
        return obj

    @property
    def attribute_names(self) -> set[str]:
        """Names of all attributes in this custom metadata set."""
        return self._names

    async def __ainit__(self, client: AsyncAtlanClient, name: str):
        """Async init with human-readable name of custom metadata set."""
        super().__init__()
        self._name = name
        self._modified = False
        self._client = client
        _id = await self._client.custom_metadata_cache.get_id_for_name(name)
        attr_map = await self._client.custom_metadata_cache.get_attr_map_for_id(_id)
        self._names = {
            value
            for key, value in attr_map.items()
            if not await self._client.custom_metadata_cache.is_attr_archived(
                attr_id=key
            )
        }

    @classmethod
    async def creator(
        cls, client: AsyncAtlanClient, name: str
    ) -> AsyncCustomMetadataDict:
        """Create and initialize an AsyncCustomMetadataDict instance."""
        instance = cls()
        await instance.__ainit__(client, name)
        return instance

    @classmethod
    def get_deleted_sentinel(cls) -> AsyncCustomMetadataDict:
        """Return a sentinel representing deleted custom metadata."""
        if cls._sentinel is not None:
            return cls._sentinel
        return cls.__new__(cls, DELETED_SENTINEL)

    @property
    def modified(self) -> bool:
        """Whether the set has been modified from its initial values."""
        return self._modified

    def __setitem__(self, key: str, value):
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        self._modified = True
        self.data[key] = value

    def __getitem__(self, key: str):
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        return None if key not in self.data else self.data[key]

    def clear_all(self):
        """Set all available properties explicitly to None."""
        for attribute_name in self._names:
            self.data[attribute_name] = None
        self._modified = True

    def clear_unset(self):
        """Set all properties that haven't been set to None."""
        for name in self.attribute_names:
            if name not in self.data:
                self.data[name] = None

    def is_set(self, key: str) -> bool:
        """Whether the given property has been set in the metadata set."""
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        return key in self.data

    async def business_attributes(self) -> dict[str, Any]:
        """Return the metadata set with names resolved to their internal values."""
        result = {}
        for key, value in self.data.items():
            attr_id = await self._client.custom_metadata_cache.get_attr_id_for_name(
                self._name, key
            )
            result[attr_id] = value
        return result


class AsyncCustomMetadataProxy:
    """Async proxy for accessing and managing custom metadata on an asset."""

    def __init__(
        self,
        client: AsyncAtlanClient,
        business_attributes: Union[dict[str, Any], None],
    ):
        self._client = client
        self._metadata: Union[dict[str, AsyncCustomMetadataDict], None] = None
        self._business_attributes = business_attributes
        self._modified = False

    async def _initialize_metadata(self):
        """Initialize metadata from business_attributes if needed."""
        if self._business_attributes is None or self._metadata is not None:
            return

        self._metadata = {}
        for cm_id, cm_attributes in self._business_attributes.items():
            try:
                cm_name = await self._client.custom_metadata_cache.get_name_for_id(
                    cm_id
                )
                attribs = AsyncCustomMetadataDict()
                await attribs.__ainit__(name=cm_name, client=self._client)
                for attr_id, properties in cm_attributes.items():
                    attr_name = (
                        await self._client.custom_metadata_cache.get_attr_name_for_id(
                            cm_id, attr_id
                        )
                    )
                    if not await self._client.custom_metadata_cache.is_attr_archived(
                        attr_id=attr_id
                    ):
                        attribs[attr_name] = properties
                attribs._modified = False
            except NotFoundError:
                cm_name = DELETED_
                attribs = AsyncCustomMetadataDict.get_deleted_sentinel()
            self._metadata[cm_name] = attribs

    async def get_custom_metadata(self, name: str) -> AsyncCustomMetadataDict:
        """Get or create a custom metadata set by name."""
        await self._initialize_metadata()
        if self._metadata is None:
            self._metadata = {}
        if name not in self._metadata:
            attribs = AsyncCustomMetadataDict()
            await attribs.__ainit__(name=name, client=self._client)
            self._metadata[name] = attribs
        return self._metadata[name]

    async def set_custom_metadata(self, custom_metadata: AsyncCustomMetadataDict):
        """Set a custom metadata set."""
        await self._initialize_metadata()
        if self._metadata is None:
            self._metadata = {}
        self._metadata[custom_metadata._name] = custom_metadata
        self._modified = True

    @property
    def modified(self) -> bool:
        """Whether any custom metadata has been modified."""
        if self._modified:
            return True
        if self._metadata is None:
            return False
        return any(metadata_dict.modified for metadata_dict in self._metadata.values())

    async def business_attributes(self) -> Union[dict[str, Any], None]:
        """Return the business attributes in internal format."""
        await self._initialize_metadata()
        if self.modified and self._metadata is not None:
            result = {}
            for key, value in self._metadata.items():
                cm_id = await self._client.custom_metadata_cache.get_id_for_name(key)
                result[cm_id] = await value.business_attributes()
            return result
        return self._business_attributes


class AsyncCustomMetadataRequest:
    """Async request to update custom metadata on an asset."""

    def __init__(self, data: dict[str, Any], set_id: str):
        self._data = data
        self._set_id = set_id

    @classmethod
    async def create(
        cls, custom_metadata_dict: AsyncCustomMetadataDict
    ) -> AsyncCustomMetadataRequest:
        """Create a request from an AsyncCustomMetadataDict."""
        business_attrs = await custom_metadata_dict.business_attributes()
        set_id = await (
            custom_metadata_dict._client.custom_metadata_cache.get_id_for_name(
                custom_metadata_dict._name
            )
        )
        return cls(data=business_attrs, set_id=set_id)

    @property
    def custom_metadata_set_id(self) -> str:
        """Unique identifier of the custom metadata set."""
        return self._set_id

    def to_dict(self) -> dict[str, Any]:
        """Return the underlying data dict."""
        return self._data
