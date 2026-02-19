# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from collections import UserDict
from typing import TYPE_CHECKING, Any, Union

from pyatlan.errors import NotFoundError
from pyatlan.model.constants import DELETED_, DELETED_SENTINEL

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient


class CustomMetadataDict(UserDict):
    """
    Allows the manipulation of a set of custom metadata attributes
    using the human-readable names.
    """

    _sentinel: Union[CustomMetadataDict, None] = None

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

    def __init__(self, client: AtlanClient, name: str):
        """Init CustomMetadataDict with the human-readable name of a custom metadata set."""
        super().__init__()
        self._name = name
        self._modified = False
        self._client = client
        _id = self._client.custom_metadata_cache.get_id_for_name(name)
        self._names = {
            value
            for key, value in self._client.custom_metadata_cache.map_attr_id_to_name[
                _id
            ].items()
            if not self._client.custom_metadata_cache.is_attr_archived(attr_id=key)
        }

    @classmethod
    def get_deleted_sentinel(cls) -> CustomMetadataDict:
        """Return a sentinel CustomMetadataDict representing deleted custom metadata."""
        if cls._sentinel is not None:
            return cls._sentinel
        return cls.__new__(cls, DELETED_SENTINEL)

    @property
    def modified(self) -> bool:
        """Whether the set has been modified from its initial values."""
        return self._modified

    def __setitem__(self, key: str, value):
        """Set a property value using the human-readable name as the key."""
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        self._modified = True
        self.data[key] = value

    def __getitem__(self, key: str):
        """Retrieve a property value using the human-readable name as the key."""
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        return None if key not in self.data else self.data[key]

    def clear_all(self):
        """Set all properties to None."""
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

    @property
    def business_attributes(self) -> dict[str, Any]:
        """Return the metadata set with names resolved to their internal values."""
        return {
            self._client.custom_metadata_cache.get_attr_id_for_name(
                self._name, key
            ): value
            for (key, value) in self.data.items()
        }


class CustomMetadataProxy:
    """Proxy for accessing and managing custom metadata on an asset."""

    def __init__(
        self,
        client: AtlanClient,
        business_attributes: Union[dict[str, Any], None],
    ):
        self._client = client
        self._metadata: Union[dict[str, CustomMetadataDict], None] = None
        self._business_attributes = business_attributes
        self._modified = False
        if self._business_attributes is None:
            return
        self._metadata = {}
        for cm_id, cm_attributes in self._business_attributes.items():
            try:
                cm_name = self._client.custom_metadata_cache.get_name_for_id(cm_id)
                attribs = CustomMetadataDict(name=cm_name, client=self._client)
                for attr_id, properties in cm_attributes.items():
                    attr_name = self._client.custom_metadata_cache.get_attr_name_for_id(
                        cm_id, attr_id
                    )
                    if not self._client.custom_metadata_cache.is_attr_archived(
                        attr_id=attr_id
                    ):
                        attribs[attr_name] = properties
                attribs._modified = False
            except NotFoundError:
                cm_name = DELETED_
                attribs = CustomMetadataDict.get_deleted_sentinel()
            self._metadata[cm_name] = attribs

    def get_custom_metadata(self, name: str) -> CustomMetadataDict:
        """Get or create a custom metadata set by name."""
        if self._metadata is None:
            self._metadata = {}
        if name not in self._metadata:
            attribs = CustomMetadataDict(name=name, client=self._client)
            self._metadata[name] = attribs
        return self._metadata[name]

    def set_custom_metadata(self, custom_metadata: CustomMetadataDict):
        """Set a custom metadata set."""
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

    @property
    def business_attributes(self) -> Union[dict[str, Any], None]:
        """Return the business attributes in internal format."""
        if self.modified and self._metadata is not None:
            return {
                self._client.custom_metadata_cache.get_id_for_name(
                    key
                ): value.business_attributes
                for key, value in self._metadata.items()
            }
        return self._business_attributes


class CustomMetadataRequest:
    """
    Request to update custom metadata on an asset.

    Replaces the Pydantic __root__ pattern with a simple dict wrapper.
    """

    def __init__(self, data: dict[str, Any], set_id: str):
        self._data = data
        self._set_id = set_id

    @classmethod
    def create(cls, custom_metadata_dict: CustomMetadataDict) -> CustomMetadataRequest:
        """Create a request from a CustomMetadataDict."""
        set_id = custom_metadata_dict._client.custom_metadata_cache.get_id_for_name(
            custom_metadata_dict._name
        )
        return cls(data=custom_metadata_dict.business_attributes, set_id=set_id)

    @property
    def custom_metadata_set_id(self) -> str:
        """Unique identifier of the custom metadata set."""
        return self._set_id

    def to_dict(self) -> dict[str, Any]:
        """Return the underlying data dict."""
        return self._data
