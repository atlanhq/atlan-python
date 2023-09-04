from collections import UserDict
from typing import Any, Optional

from pydantic import PrivateAttr

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache
from pyatlan.model.core import AtlanObject


class CustomMetadataDict(UserDict):
    """This class allows the manipulation of a set of custom metadata attributes using the human readable names."""

    @property
    def attribute_names(self) -> set[str]:
        return self._names

    def __init__(self, name: str):
        """Inits CustomMetadataDict with a string containing the human readable name of a set of custom metadata"""
        super().__init__()
        self._name = name
        self._modified = False
        id = CustomMetadataCache.get_id_for_name(name)
        self._names = set(CustomMetadataCache.map_attr_id_to_name[id].values())

    @property
    def modified(self):
        """Returns a boolean indicating whether the set has been modified from its initial values"""
        return self._modified

    def __setitem__(self, key: str, value):
        """Set the value of a property of the custom metadata set using the human readable name as the key.
        The name will be validated to ensure that it's valid for this custom metadata set
        """
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        self._modified = True
        self.data[key] = value

    def __getitem__(self, key: str):
        """Retrieve the value of a property of the custom metadata set using the human readable name as the key.
        The name will be validated to ensure that it's valid for this custom metadata set
        """
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        if key not in self.data:
            return None
        return self.data[key]

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
    def business_attributes(self) -> dict[str, Any]:
        """Returns a dict containing the metadat set with the human readable set name and property names resolved
        to their internal values"""
        return {
            CustomMetadataCache.get_attr_id_for_name(self._name, key): value
            for (key, value) in self.data.items()
        }


class CustomMetadataProxy:
    def __init__(self, business_attributes: Optional[dict[str, Any]]):
        self._metadata: Optional[dict[str, CustomMetadataDict]] = None
        self._business_attributes = business_attributes
        self._modified = False
        if self._business_attributes is None:
            return
        self._metadata = {}
        for cm_id, cm_attributes in self._business_attributes.items():
            cm_name = CustomMetadataCache.get_name_for_id(cm_id)
            attribs = CustomMetadataDict(name=cm_name)
            for attr_id, properties in cm_attributes.items():
                attr_name = CustomMetadataCache.get_attr_name_for_id(cm_id, attr_id)
                attribs[attr_name] = properties
            attribs._modified = False
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
        for metadata_dict in self._metadata.values():
            if metadata_dict.modified:
                return True
        return False

    @property
    def business_attributes(self) -> Optional[dict[str, Any]]:
        if self.modified and self._metadata is not None:
            return {
                CustomMetadataCache.get_id_for_name(key): value.business_attributes
                for key, value in self._metadata.items()
            }
        return self._business_attributes


class CustomMetadataRequest(AtlanObject):
    __root__: dict[str, Any]
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
