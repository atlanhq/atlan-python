# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import json
from typing import Any, Optional

from pyatlan.client.atlan import AtlanClient
from pyatlan.error import LogicError, NotFoundError
from pyatlan.model.core import CustomMetadata
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef


class Synonym:
    def __init__(self, storage_name):
        self.storage_name = storage_name

    def __set__(self, instance, value):
        instance[self.storage_name] = value

    def __get__(self, instance, owner):
        if self.storage_name in instance:
            return instance[self.storage_name]
        return None


class CustomMetadataCache:

    cache_by_id: dict[str, CustomMetadataDef] = dict()
    map_id_to_name: dict[str, str] = dict()
    map_id_to_type: dict[str, type] = dict()
    map_name_to_id: dict[str, str] = dict()
    map_attr_id_to_name: dict[str, dict[str, str]] = dict()
    map_attr_name_to_id: dict[str, dict[str, str]] = dict()
    archived_attr_ids: dict[str, str] = dict()
    types_by_asset: dict[str, set[type]] = dict()

    @classmethod
    def _refresh_cache(cls) -> None:
        from pyatlan.model.core import CustomMetadata, to_snake_case

        client = AtlanClient.get_default_client()
        if client is None:
            client = AtlanClient()
        response = client.get_typedefs(type_category=AtlanTypeCategory.CUSTOM_METADATA)
        if response is not None:
            cls.map_id_to_name = {}
            cls.map_name_to_id = {}
            cls.map_attr_id_to_name = {}
            cls.map_attr_name_to_id = {}
            cls.archived_attr_ids = {}
            cls.cache_by_id = {}
            for cm in response.custom_metadata_defs:
                type_id = cm.name
                type_name = cm.display_name
                cls.cache_by_id[type_id] = cm
                cls.map_id_to_name[type_id] = type_name
                cls.map_name_to_id[type_name] = type_id
                cls.map_attr_id_to_name[type_id] = {}
                cls.map_attr_name_to_id[type_id] = {}
                meta_name = cm.display_name.replace(" ", "")
                attribute_class_name = f"Attributes_{meta_name}"
                attrib_type = type(attribute_class_name, (CustomMetadata,), {})
                attrib_type._meta_data_type_id = type_id  # type: ignore
                attrib_type._meta_data_type_name = type_name  # type: ignore
                cls.map_id_to_type[type_id] = attrib_type
                applicable_types: set[str] = set()
                if cm.attribute_defs:
                    for attr in cm.attribute_defs:
                        if attr.options.custom_applicable_entity_types:
                            applicable_types.update(
                                json.loads(attr.options.custom_applicable_entity_types)
                            )
                        attr_id = attr.name
                        attr_name = attr.display_name
                        cls.map_attr_id_to_name[type_id][attr_id] = attr_name
                        if attr.options and attr.options.is_archived:
                            cls.archived_attr_ids[attr_id] = attr_name
                        elif attr_name in cls.map_attr_name_to_id[type_id]:
                            raise LogicError(
                                f"Multiple custom attributes with exactly the same name ({attr_name}) "
                                f"found for: {type_name}",
                                code="ATLAN-PYTHON-500-100",
                            )
                        else:
                            attr_name = to_snake_case(attr_name.replace(" ", ""))
                            setattr(attrib_type, attr_name, Synonym(attr_id))
                            cls.map_attr_name_to_id[type_id][attr_name] = attr_id
                    for asset_type in applicable_types:
                        if asset_type not in cls.types_by_asset:
                            cls.types_by_asset[asset_type] = set()
                        cls.types_by_asset[asset_type].add(attrib_type)

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable custom metadata set name to its Atlan-internal ID string.
        """
        if cm_id := cls.map_name_to_id.get(name):
            return cm_id
        # If not found, refresh the cache and look again (could be stale)
        cls._refresh_cache()
        return cls.map_name_to_id.get(name)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal custom metadata ID string to the human-readable custom metadata set name.
        """
        if cm_name := cls.map_id_to_name.get(idstr):
            return cm_name
        # If not found, refresh the cache and look again (could be stale)
        cls._refresh_cache()
        return cls.map_id_to_name.get(idstr)

    @classmethod
    def get_type_for_id(cls, idstr: str) -> Optional[type]:
        if cm_type := cls.map_id_to_type.get(idstr):
            return cm_type
        cls._refresh_cache()
        return cls.map_id_to_type.get(idstr)

    @classmethod
    def get_all_custom_attributes(
        cls, include_deleted: bool = False, force_refresh: bool = False
    ) -> dict[str, list[AttributeDef]]:
        """
        Retrieve all the custom metadata attributes. The map will be keyed by custom metadata set
        name, and the value will be a listing of all the attributes within that set (with all the details
        of each of those attributes).
        """
        if len(cls.cache_by_id) == 0 or force_refresh:
            cls._refresh_cache()
        m = {}
        for type_id, cm in cls.cache_by_id.items():
            type_name = cls.get_name_for_id(type_id)
            if not type_name:
                raise NotFoundError(
                    f"The type_name for {type_id} could not be found.", code="fixme"
                )
            attribute_defs = cm.attribute_defs
            if include_deleted:
                to_include = attribute_defs
            else:
                to_include = []
                if attribute_defs:
                    to_include.extend(
                        attr
                        for attr in attribute_defs
                        if not attr.options or not attr.options.is_archived
                    )
            m[type_name] = to_include
        return m

    @classmethod
    def get_attr_id_for_name(cls, set_name: str, attr_name: str) -> Optional[str]:
        """
        Translate the provided human-readable custom metadata set and attribute names to the Atlan-internal ID string
        for the attribute.
        """
        attr_id = None
        if set_id := cls.get_id_for_name(set_name):
            if sub_map := cls.map_attr_name_to_id.get(set_id):
                attr_id = sub_map.get(attr_name)
            if attr_id:
                # If found, return straight away
                return attr_id
            # Otherwise, refresh the cache and look again (could be stale)
            cls._refresh_cache()
            if sub_map := cls.map_attr_name_to_id.get(set_id):
                return sub_map.get(attr_name)
        return None

    @classmethod
    def get_attr_name_for_id(cls, set_id: str, attr_id: str) -> Optional[str]:
        """
        Translate the provided human-readable custom metadata set and attribute names to the Atlan-internal ID string
        for the attribute.
        """
        if sub_map := cls.map_attr_id_to_name.get(set_id):
            attr_name = sub_map.get(attr_id)
            if attr_name:
                return attr_name
            cls._refresh_cache()
            if sub_map := cls.map_attr_id_to_name.get(set_id):
                return sub_map.get(attr_id)
        return None

    @classmethod
    def _get_attributes_for_search_results(cls, set_id: str) -> Optional[list[str]]:
        if sub_map := cls.map_attr_name_to_id.get(set_id):
            attr_ids = sub_map.values()
            return [f"{set_id}.{idstr}" for idstr in attr_ids]
        return None

    @classmethod
    def get_attributes_for_search_results(cls, set_name: str) -> Optional[list[str]]:
        """
        Retrieve the full set of custom attributes to include on search results.
        """
        if set_id := cls.get_id_for_name(set_name):
            if dot_names := cls._get_attributes_for_search_results(set_id):
                return dot_names
            cls._refresh_cache()
            return cls._get_attributes_for_search_results(set_id)
        return None

    @classmethod
    def get_custom_metadata(
        cls,
        name: str,
        asset_type: type,
        business_attributes: Optional[dict[str, Any]] = None,
    ) -> CustomMetadata:
        type_name = asset_type.__name__
        ba_id = cls.get_id_for_name(name)
        if ba_id is None:
            raise ValueError(f"No custom metadata with the name: {name} exist")
        for a_type in CustomMetadataCache.types_by_asset[type_name]:
            if (
                hasattr(a_type, "_meta_data_type_name")
                and a_type._meta_data_type_name == name
            ):
                break
        else:
            raise ValueError(f"Custom metadata {name} is not applicable to {type_name}")
        if ba_type := CustomMetadataCache.get_type_for_id(ba_id):
            return (
                ba_type(business_attributes[ba_id])
                if business_attributes and ba_id in business_attributes
                else ba_type()
            )
        raise ValueError(f"Custom metadata {name} is not applicable to {type_name}")
