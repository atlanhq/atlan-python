from collections import UserDict
from typing import Any, Optional

from pydantic import BaseModel, PrivateAttr

from pyatlan.cache.custom_metadata_cache import CustomMetadataCache


class CustomMetadataDict(UserDict):
    @property
    def attribute_names(self) -> set[str]:
        return self._names

    def __init__(self, name: str):
        super().__init__()
        self._name = name
        id = CustomMetadataCache.get_id_for_name(name)
        self._names = set(CustomMetadataCache.map_attr_id_to_name[id].values())
        pass

    def __setitem__(self, key, value):
        if key not in self._names:
            raise KeyError(f"'{key}' is not a valid property name for {self._name}")

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


class Container(BaseModel):
    _metadata: Optional[dict[str, CustomMetadataDict]] = PrivateAttr()
    custom_metadata: Optional[dict[str, dict[str, str]]]

    def __init__(self, **data):
        super().__init__(**data)
        if self.custom_metadata:
            self._metadata = {}
            for cm_id, cm_attributes in self.custom_metadata.items():
                cm_name = CustomMetadataCache.get_name_for_id(cm_id)
                attribs = CustomMetadataDict(name=cm_name)
                for attr_id, properties in cm_attributes.items():
                    attr_name = CustomMetadataCache.get_attr_name_for_id(cm_id, attr_id)
                    attribs[attr_name] = properties
                self._metadata[cm_name] = attribs

    def _update_custom_metadata(self):
        def convert(cm_name: str, properties: dict[str, Any]):
            return {
                CustomMetadataCache.get_attr_id_for_name(cm_name, key): value
                for (key, value) in properties.items()
            }

        new_metadata = {
            CustomMetadataCache.get_id_for_name(cm_name): convert(cm_name, attribs)
            for (cm_name, attribs) in self._metadata.items()
        }
        self.custom_metadata = new_metadata

    def json(self, *args, **kwargs) -> str:
        self._update_custom_metadata()
        return super().json(**kwargs)

    def get_metadata(self, name: str) -> CustomMetadataDict:
        if self._metadata is None:
            self._metadata = {}
        if name not in self._metadata:
            attribs = CustomMetadataDict(name=name)
            self._metadata[name] = attribs
        return self._metadata[name]
