from collections import UserDict
from typing import Any, Optional

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache


class CustomMetadataDict(UserDict):
    @property
    def attribute_names(self) -> set[str]:
        return self._names

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        self._modified = False
        id = CustomMetadataCache.get_id_for_name(name)
        self._names = set(CustomMetadataCache.map_attr_id_to_name[id].values())
        pass

    @property
    def modified(self):
        return self._modified

    def __setitem__(self, key, value):
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        self._modified = True
        self.data[key] = value

    def __getitem__(self, key):
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")
        if key not in self.data:
            raise KeyError(f"'{key}' must be set before trying to retrieve the value")
        return self.data[key]

    def clear(self):
        for attribute_name in self._names:
            self.data[attribute_name] = None


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
        def convert(cm_name: str, properties: CustomMetadataDict):
            return {
                CustomMetadataCache.get_attr_id_for_name(cm_name, key): value
                for (key, value) in properties.items()
            }

        if self.modified and self._metadata is not None:
            new_metadata = {
                CustomMetadataCache.get_id_for_name(cm_name): convert(cm_name, attribs)
                for (cm_name, attribs) in self._metadata.items()
            }
            self._business_attributes = new_metadata
        return self._business_attributes
