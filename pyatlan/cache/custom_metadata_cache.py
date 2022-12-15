
from pyatlan.client.atlan import AtlanClient
from pyatlan.client.typedef import TypeDefClient
from pyatlan.model.typedef import CustomMetadataDef, AttributeDef
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.error import LogicError

from typing import Optional

class CustomMetadataCache:

    cache_by_id: dict[str, CustomMetadataDef] = dict()
    map_id_to_name: dict[str, str] = dict()
    map_name_to_id: dict[str, str] = dict()
    map_attr_id_to_name: dict[str, dict[str, str]] = dict()
    map_attr_name_to_id: dict[str, dict[str, str]] = dict()
    archived_attr_ids: dict[str, str] = dict()

    @classmethod
    def _refresh_cache(cls) -> None:
        response = TypeDefClient(AtlanClient()).get_typedefs(type=AtlanTypeCategory.CUSTOM_METADATA)
        if response is not None:
            cls.cache_by_id = dict()
            cls.map_id_to_name = dict()
            cls.map_name_to_id = dict()
            cls.map_attr_id_to_name = dict()
            cls.map_attr_name_to_id = dict()
            cls.archived_attr_ids = dict()
            for cm in response.custom_metadata_defs:
                type_id = cm.name
                type_name = cm.display_name
                cls.cache_by_id[type_id] = cm
                cls.map_id_to_name[type_id] = type_name
                cls.map_name_to_id[type_name] = type_id
                cls.map_attr_id_to_name[type_id] = dict()
                cls.map_attr_name_to_id[type_id] = dict()
                if cm.attribute_defs:
                    for attr in cm.attribute_defs:
                        attr_id = attr.name
                        attr_name = attr.display_name
                        cls.map_attr_id_to_name[type_id][attr_id] = attr_name
                        if attr.options and attr.options.is_archived:
                            cls.archived_attr_ids[attr_id] = attr_name
                        else:
                            if attr_name in cls.map_attr_name_to_id[type_id]:
                                raise LogicError(
                                    "Multiple custom attributes with exactly the same name (" + attr_name + ") found for: " + type_name,
                                    code="ATLAN-PYTHON-500-100"
                                )
                            cls.map_attr_name_to_id[type_id][attr_name] = attr_id


    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable custom metadata set name to its Atlan-internal ID string.
        """
        cm_id = cls.map_name_to_id.get(name)
        if cm_id:
            return cm_id
        else:
            # If not found, refresh the cache and look again (could be stale)
            cls._refresh_cache()
            return cls.map_name_to_id.get(name)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal custom metadata ID string to the human-readable custom metadata set name.
        """
        cm_name = cls.map_id_to_name.get(idstr)
        if cm_name:
            return cm_name
        else:
            # If not found, refresh the cache and look again (could be stale)
            cls._refresh_cache()
            return cls.map_id_to_name.get(idstr)

    @classmethod
    def get_all_custom_attributes(cls, include_deleted: bool=False, force_refresh: bool=False) -> dict[str, list[AttributeDef]]:
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
            attribute_defs = cm.attribute_defs
            if include_deleted:
                to_include = attribute_defs
            else:
                to_include = []
                if attribute_defs:
                    for attr in attribute_defs:
                        if not attr.options or not attr.options.is_archived:
                            to_include.append(attr)
            m[type_name] = to_include
        return m

    @classmethod
    def get_attr_id_for_name(cls, set_name: str, attr_name: str) -> Optional[str]:
        """
        Translate the provided human-readable custom metadata set and attribute names to the Atlan-internal ID string
        for the attribute.
        """
        attr_id = None
        set_id = cls.get_id_for_name(set_name)
        if set_id:
            sub_map = cls.map_attr_name_to_id.get(set_id)
            if sub_map:
                attr_id = sub_map.get(attr_name)
            if attr_id:
                # If found, return straight away
                return attr_id
            else:
                # Otherwise, refresh the cache and look again (could be stale)
                cls._refresh_cache()
                sub_map = cls.map_attr_name_to_id.get(set_id)
                if sub_map:
                    return sub_map.get(attr_name)
        return None

    @classmethod
    def _get_attributes_for_search_results(cls, set_id: str) -> Optional[list[str]]:
        sub_map = cls.map_attr_name_to_id.get(set_id)
        if sub_map:
            attr_ids = sub_map.values()
            dot_names = []
            for idstr in attr_ids:
                dot_names.append(set_id + "." + idstr)
            return dot_names
        return None

    @classmethod
    def get_attributes_for_search_results(cls, set_name: str) -> Optional[list[str]]:
        """
        Retrieve the full set of custom attributes to include on search results.
        """
        set_id = cls.get_id_for_name(set_name)
        if set_id:
            dot_names = cls._get_attributes_for_search_results(set_id)
            if dot_names:
                return dot_names
            else:
                cls._refresh_cache()
                return cls._get_attributes_for_search_results(set_id)
        return None
