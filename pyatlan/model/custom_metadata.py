from collections import UserDict
from typing import Any, Dict, Optional, Set

from pydantic.v1 import PrivateAttr

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.errors import NotFoundError
from pyatlan.model.constants import DELETED_, DELETED_SENTINEL
from pyatlan.model.core import AtlanObject


class CustomMetadataDict(UserDict):
    """This class allows the manipulation of a set of custom metadata attributes using the human-readable names."""

    _sentinel: Optional["CustomMetadataDict"] = None

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

    def __init__(self, name: str):
        """Inits CustomMetadataDict with a string containing the human-readable name of a set of custom metadata"""
        super().__init__()
        self._name = name
        self._modified = False
        _id = CustomMetadataCache.get_id_for_name(name)
        self._names = {
            value
            for key, value in CustomMetadataCache.get_cache()
            .map_attr_id_to_name[_id]
            .items()
            if not CustomMetadataCache.is_attr_archived(attr_id=key)
        }

    @classmethod
    def get_deleted_sentinel(cls) -> "CustomMetadataDict":
        """Will return an CustomMetadataDict that is a sentinel object to represent deleted custom meta data."""
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
        """Set the value of a property of the custom metadata set using the human-readable name as the key.
        The name will be validated to ensure that it's valid for this custom metadata set
        """
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        self._modified = True
        self.data[key] = value

    def __getitem__(self, key: str):
        """Retrieve the value of a property of the custom metadata set using the human-readable name as the key.
        The name will be validated to ensure that it's valid for this custom metadata set
        """
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        return None if key not in self.data else self.data[key]

    def clear_all(self):
        """This method will set all the properties available explicitly to None"""
        for attribute_name in self._names:
            self.data[attribute_name] = None
        self._modified = True

    def clear_unset(self):
        """This method will set all properties that haven't been set to None"""
        for name in self.attribute_names:
            if name not in self.data:
                self.data[name] = None

    def is_set(self, key: str):
        """Returns a boolean indicating whether the given property has been set in the metadata set. The key
        will be validated to ensure that it's a valid property name for this metadata set
        """
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        return key in self.data

    @property
    def business_attributes(self) -> Dict[str, Any]:
        """Returns a dict containing the metadata set with the human-readable set name and property names resolved
        to their internal values"""
        return {
            CustomMetadataCache.get_attr_id_for_name(self._name, key): value
            for (key, value) in self.data.items()
        }


class CustomMetadataProxy:
    def __init__(self, business_attributes: Optional[Dict[str, Any]]):
        self._metadata: Optional[Dict[str, CustomMetadataDict]] = None
        self._business_attributes = business_attributes
        self._modified = False
        if self._business_attributes is None:
            return
        self._metadata = {}
        for cm_id, cm_attributes in self._business_attributes.items():
            try:
                cm_name = CustomMetadataCache.get_name_for_id(cm_id)
                attribs = CustomMetadataDict(name=cm_name)
                for attr_id, properties in cm_attributes.items():
                    attr_name = CustomMetadataCache.get_attr_name_for_id(cm_id, attr_id)
                    # Only set active custom metadata attributes
                    if not CustomMetadataCache.is_attr_archived(attr_id=attr_id):
                        attribs[attr_name] = properties
                attribs._modified = False
            except NotFoundError:
                cm_name = DELETED_
                attribs = CustomMetadataDict.get_deleted_sentinel()
            self._metadata[cm_name] = attribs

    def get_custom_metadata(self, name: str) -> CustomMetadataDict:
        if self._metadata is None:
            self._metadata = {}
        if name not in self._metadata:
            attribs = CustomMetadataDict(name=name)
            self._metadata[name] = attribs
        return self._metadata[name]

    def set_custom_metadata(self, custom_metadata: CustomMetadataDict):
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

    @property
    def business_attributes(self) -> Optional[Dict[str, Any]]:
        if self.modified and self._metadata is not None:
            return {
                CustomMetadataCache.get_id_for_name(key): value.business_attributes
                for key, value in self._metadata.items()
            }
        return self._business_attributes


class CustomMetadataRequest(AtlanObject):
    __root__: Dict[str, Any]
    _set_id: str = PrivateAttr()

    @classmethod
    def create(cls, custom_metadata_dict: CustomMetadataDict):
        ret_val = cls(__root__=custom_metadata_dict.business_attributes)
        ret_val._set_id = CustomMetadataCache.get_id_for_name(
            custom_metadata_dict._name
        )
        return ret_val

    @property
    def custom_metadata_set_id(self):
        return self._set_id
