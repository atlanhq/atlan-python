# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from collections import UserDict
from typing import TYPE_CHECKING, Any, Dict, Optional, Set

from pydantic.v1 import PrivateAttr, StrictStr

from pyatlan.errors import NotFoundError
from pyatlan.model.constants import DELETED_, DELETED_SENTINEL
from pyatlan.model.core import AtlanObject
from pyatlan.model.search import Exists, SearchFieldType, Term

if TYPE_CHECKING:
    from pyatlan.client.aio.client import AsyncAtlanClient


class AsyncCustomMetadataDict(UserDict):
    """Async version of CustomMetadataDict for manipulating custom metadata attributes using human-readable names.

    Recommended usage:
        # Use the factory method for consistency with sync CustomMetadataDict
        custom_metadata = await AsyncCustomMetadataDict.creator(client=client, name="metadata_set_name")
        custom_metadata["attribute_name"] = "value"
    """

    _sentinel: Optional["AsyncCustomMetadataDict"] = None

    def __new__(cls, *args, **kwargs):
        if args and args[0] == DELETED_SENTINEL and cls._sentinel:
            return cls._sentinel
        obj = super().__new__(cls)
        super().__init__(obj)
        if args and args[0] == DELETED_SENTINEL:
            obj._name = DELETED_
            obj._modified = False
            obj._names = set()
            cls._sentinel = obj
        return obj

    @property
    def attribute_names(self) -> Set[str]:
        return self._names

    async def __ainit__(self, client: AsyncAtlanClient, name: str):
        """Async init for AsyncCustomMetadataDict with human-readable name of custom metadata set"""
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
        """Create and initialize an AsyncCustomMetadataDict instance.

        This is the recommended way to create an AsyncCustomMetadataDict as it mirrors
        the sync CustomMetadataDict(client, name) constructor pattern.

        :param client: async Atlan client to use for the request
        :param name: human-readable name of the custom metadata set
        :returns: initialized AsyncCustomMetadataDict instance
        """
        instance = cls()
        await instance.__ainit__(client, name)
        return instance

    @classmethod
    def get_deleted_sentinel(cls) -> "AsyncCustomMetadataDict":
        """Returns an AsyncCustomMetadataDict sentinel object to represent deleted custom metadata."""
        if cls._sentinel is not None:
            return cls._sentinel
        return cls.__new__(
            cls, DELETED_SENTINEL
        )  # Because __new__ is being invoked directly __init__ won't be invoked

    @property
    def modified(self):
        """Returns a boolean indicating whether the set has been modified from its initial values"""
        return self._modified

    def __setitem__(self, key: str, value):
        """Set the value of a property using the human-readable name as the key."""
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        self._modified = True
        self.data[key] = value

    def __getitem__(self, key: str):
        """Retrieve the value of a property using the human-readable name as the key."""
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        return None if key not in self.data else self.data[key]

    def clear_all(self):
        """Set all available properties explicitly to None"""
        for attribute_name in self._names:
            self.data[attribute_name] = None
        self._modified = True

    def clear_unset(self):
        """Set all properties that haven't been set to None"""
        for name in self.attribute_names:
            if name not in self.data:
                self.data[name] = None

    def is_set(self, key: str):
        """Returns whether the given property has been set in the metadata set."""
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        return key in self.data

    async def business_attributes(self) -> Dict[str, Any]:
        """Returns a dict with human-readable names resolved to their internal values"""
        result = {}
        for key, value in self.data.items():
            attr_id = await self._client.custom_metadata_cache.get_attr_id_for_name(
                self._name, key
            )
            result[attr_id] = value
        return result


class AsyncCustomMetadataProxy:
    def __init__(
        self,
        client: AsyncAtlanClient,
        business_attributes: Optional[Dict[str, Any]],
    ):
        self._client = client
        self._metadata: Optional[Dict[str, AsyncCustomMetadataDict]] = None
        self._business_attributes = business_attributes
        self._modified = False

    async def _initialize_metadata(self):
        """Initialize metadata from business_attributes if needed"""
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
                    # Only set active custom metadata attributes
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
        await self._initialize_metadata()
        if self._metadata is None:
            self._metadata = {}
        if name not in self._metadata:
            attribs = AsyncCustomMetadataDict()
            await attribs.__ainit__(name=name, client=self._client)
            self._metadata[name] = attribs
        return self._metadata[name]

    async def set_custom_metadata(self, custom_metadata: AsyncCustomMetadataDict):
        await self._initialize_metadata()
        if self._metadata is None:
            self._metadata = {}
        self._metadata[custom_metadata._name] = custom_metadata
        self._modified = True

    @property
    def modified(self) -> bool:
        if self._modified:
            return True
        if self._metadata is None:
            return False
        return any(metadata_dict.modified for metadata_dict in self._metadata.values())

    async def business_attributes(self) -> Optional[Dict[str, Any]]:
        await self._initialize_metadata()
        if self.modified and self._metadata is not None:
            result = {}
            for key, value in self._metadata.items():
                cm_id = await self._client.custom_metadata_cache.get_id_for_name(key)
                result[cm_id] = await value.business_attributes()
            return result
        return self._business_attributes


class AsyncCustomMetadataRequest(AtlanObject):
    __root__: Dict[str, Any]
    _set_id: str = PrivateAttr()

    @classmethod
    async def create(cls, custom_metadata_dict: AsyncCustomMetadataDict):
        business_attrs = await custom_metadata_dict.business_attributes()
        ret_val = cls(__root__=business_attrs)
        ret_val._set_id = await (
            custom_metadata_dict._client.custom_metadata_cache.get_id_for_name(
                custom_metadata_dict._name
            )
        )
        return ret_val

    @property
    def custom_metadata_set_id(self):
        return self._set_id


class AsyncCustomMetadataField:
    """
    Async utility class to simplify searching for values on custom metadata attributes.
    """

    def __init__(self, client, set_name: str, attribute_name: str):
        self.client = client
        self.set_name = set_name
        self.attribute_name = attribute_name
        self._initialized = False
        self.field_name = None
        self.elastic_field_name = None
        self.attribute_def = None

    async def _ensure_initialized(self):
        """Lazy initialization of field properties."""
        if not self._initialized:
            self.field_name = StrictStr(
                await self.client.custom_metadata_cache.get_attribute_for_search_results(
                    self.set_name, self.attribute_name
                )
            )
            self.elastic_field_name = StrictStr(
                await self.client.custom_metadata_cache.get_attr_id_for_name(
                    set_name=self.set_name, attr_name=self.attribute_name
                )
            )
            self.attribute_def = (
                await self.client.custom_metadata_cache.get_attribute_def(
                    self.elastic_field_name
                )
            )
            self._initialized = True

    async def eq(self, value: SearchFieldType, case_insensitive: bool = False):
        """
        Returns a query that will match all assets whose field has a value that exactly equals
        the provided value.
        """
        await self._ensure_initialized()
        # After initialization, elastic_field_name is guaranteed to be a StrictStr
        return Term(
            field=self.elastic_field_name,  # type: ignore[arg-type]
            value=value,
            case_insensitive=case_insensitive,
        )

    async def has_any_value(self):
        """
        Returns a query that will match all assets that have some (non-null) value for the field.
        """
        await self._ensure_initialized()
        # After initialization, elastic_field_name is guaranteed to be a StrictStr
        return Exists(field=self.elastic_field_name)  # type: ignore[arg-type]
