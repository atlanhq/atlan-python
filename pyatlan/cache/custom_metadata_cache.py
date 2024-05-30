# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from threading import Lock
from typing import Dict, List, Optional, Set

from pyatlan.client.typedef import TypeDefClient
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import AttributeDef, CustomMetadataDef

lock = Lock()


class CustomMetadataCache:
    """
    Lazily-loaded cache for translating between Atlan-internal ID strings and human-readable names
    for custom metadata (including attributes).
    """

    caches: Dict[int, "CustomMetadataCache"] = dict()

    @classmethod
    def get_cache(cls) -> "CustomMetadataCache":
        from pyatlan.client.atlan import AtlanClient

        with lock:
            client = AtlanClient.get_default_client()
            cache_key = client.cache_key
            if cache_key not in cls.caches:
                cls.caches[cache_key] = CustomMetadataCache(
                    typedef_client=client.typedef
                )
            cache = cls.caches[cache_key]
        return cache

    @classmethod
    def refresh_cache(cls) -> None:
        """
        Refreshes the cache of custom metadata structures by requesting the full set of custom metadata
        structures from Atlan.
        :raises LogicError: if duplicate custom attributes are detected
        """
        cls.get_cache()._refresh_cache()

    @classmethod
    def get_id_for_name(cls, name: str) -> str:
        """
        Translate the provided human-readable custom metadata set name to its Atlan-internal ID string.

        :param name: human-readable name of the custom metadata set
        :returns: Atlan-internal ID string of the custom metadata set
        :raises InvalidRequestError: if no name was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        return cls.get_cache()._get_id_for_name(name=name)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> str:
        """
        Translate the provided Atlan-internal custom metadata ID string to the human-readable custom metadata set name.

        :param idstr: Atlan-internal ID string of the custom metadata set
        :returns: human-readable name of the custom metadata set
        :raises InvalidRequestError: if no ID was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        return cls.get_cache()._get_name_for_id(idstr=idstr)

    @classmethod
    def get_all_custom_attributes(
        cls, include_deleted: bool = False, force_refresh: bool = False
    ) -> Dict[str, List[AttributeDef]]:
        """
        Retrieve all the custom metadata attributes. The dict will be keyed by custom metadata set
        name, and the value will be a listing of all the attributes within that set (with all the details
        of each of those attributes).

        :param include_deleted: if True, include the archived (deleted) custom attributes; otherwise only
                                include active custom attributes
        :param force_refresh: if True, will refresh the custom metadata cache; if False, will only refresh the
                              cache if it is empty
        :returns: a dict from custom metadata set name to all details about its attributes
        :raises NotFoundError: if the custom metadata cannot be found
        """
        return cls.get_cache()._get_all_custom_attributes(
            include_deleted=include_deleted, force_refresh=force_refresh
        )

    @classmethod
    def get_attr_id_for_name(cls, set_name: str, attr_name: str) -> str:
        """
        Translate the provided human-readable custom metadata set and attribute names to the Atlan-internal ID string
        for the attribute.

        :param set_name: human-readable name of the custom metadata set
        :param attr_name: human-readable name of the attribute
        :returns: Atlan-internal ID string for the attribute
        :raises NotFoundError: if the custom metadata attribute cannot be found
        """
        return cls.get_cache()._get_attr_id_for_name(
            set_name=set_name, attr_name=attr_name
        )

    @classmethod
    def get_attr_name_for_id(cls, set_id: str, attr_id: str) -> str:
        """
        Given the Atlan-internal ID string for the set and the Atlan-internal ID for the attribute return the
        human-readable custom metadata name for the attribute.

        :param set_id: Atlan-internal ID string for the custom metadata set
        :param attr_id: Atlan-internal ID string for the attribute
        :returns: human-readable name of the attribute
        :raises NotFoundError: if the custom metadata attribute cannot be found
        """
        return cls.get_cache()._get_attr_name_for_id(set_id=set_id, attr_id=attr_id)

    @classmethod
    def is_attr_archived(cls, attr_id: str) -> bool:
        """
        Determine if an attribute is archived
        :param attr_id: Atlan-internal ID string for the attribute
        :returns: True if the attribute has been archived
        """
        return cls.get_cache()._is_attr_archived(attr_id=attr_id)

    @classmethod
    def get_attributes_for_search_results(cls, set_name: str) -> Optional[List[str]]:
        """
        Retrieve the full set of custom attributes to include on search results.

        :param set_name: human-readable name of the custom metadata set for which to retrieve attribute names
        :returns: a list of the attribute names, strictly useful for inclusion in search results
        """
        return cls.get_cache()._get_attributes_for_search_results(set_name=set_name)

    @classmethod
    def get_attribute_for_search_results(
        cls, set_name: str, attr_name: str
    ) -> Optional[str]:
        """
        Retrieve a single custom attribute name to include on search results.

        :param set_name: human-readable name of the custom metadata set for which to retrieve the custom metadata
                         attribute name
        :param attr_name: human-readable name of the attribute
        :returns: the attribute name, strictly useful for inclusion in search results
        """
        return cls.get_cache()._get_attribute_for_search_results(
            set_name=set_name, attr_name=attr_name
        )

    @classmethod
    def get_custom_metadata_def(cls, name: str) -> CustomMetadataDef:
        """
        Retrieve the full custom metadata structure definition.

        :param name: human-readable name of the custom metadata set
        :returns: the full custom metadata structure definition for that set
        :raises InvalidRequestError: if no name was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        return cls.get_cache()._get_custom_metadata_def(name=name)

    @classmethod
    def get_attribute_def(cls, attr_id: str) -> AttributeDef:
        """
        Retrieve a specific custom metadata attribute definition by its unique Atlan-internal ID string.

        :param attr_id: Atlan-internal ID string for the custom metadata attribute
        :returns: attribute definition for the custom metadata attribute
        :raises InvalidRequestError: if no attribute ID was provided
        :raises NotFoundError: if the custom metadata attribute cannot be found
        """
        return cls.get_cache()._get_attribute_def(attr_id=attr_id)

    def __init__(self, typedef_client: TypeDefClient):
        self.typedef_client: TypeDefClient = typedef_client
        self.cache_by_id: Dict[str, CustomMetadataDef] = {}
        self.attr_cache_by_id: Dict[str, AttributeDef] = {}
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.map_attr_id_to_name: Dict[str, Dict[str, str]] = {}
        self.map_attr_name_to_id: Dict[str, Dict[str, str]] = {}
        self.archived_attr_ids: Dict[str, str] = {}
        self.types_by_asset: Dict[str, Set[type]] = {}
        self.lock: Lock = Lock()

    def _refresh_cache(self) -> None:
        """
        Refreshes the cache of custom metadata structures by requesting the full set of custom metadata
        structures from Atlan.
        :raises LogicError: if duplicate custom attributes are detected
        """
        with self.lock:
            response = self.typedef_client.get(
                type_category=[
                    AtlanTypeCategory.CUSTOM_METADATA,
                    AtlanTypeCategory.STRUCT,
                ]
            )
            if not response or not response.struct_defs:
                raise ErrorCode.EXPIRED_API_TOKEN.exception_with_parameters()
            if response is not None:
                self.map_id_to_name = {}
                self.map_name_to_id = {}
                self.map_attr_id_to_name = {}
                self.map_attr_name_to_id = {}
                self.archived_attr_ids = {}
                self.cache_by_id = {}
                self.attr_cache_by_id = {}
                for cm in response.custom_metadata_defs:
                    type_id = cm.name
                    type_name = cm.display_name
                    self.cache_by_id[type_id] = cm
                    self.map_id_to_name[type_id] = type_name
                    self.map_name_to_id[type_name] = type_id
                    self.map_attr_id_to_name[type_id] = {}
                    self.map_attr_name_to_id[type_id] = {}
                    if cm.attribute_defs:
                        for attr in cm.attribute_defs:
                            attr_id = str(attr.name)
                            attr_name = str(attr.display_name)
                            self.map_attr_id_to_name[type_id][attr_id] = attr_name
                            self.attr_cache_by_id[attr_id] = attr
                            if attr.options and attr.options.is_archived:
                                self.archived_attr_ids[attr_id] = attr_name
                            elif attr_name in self.map_attr_name_to_id[type_id]:
                                raise ErrorCode.DUPLICATE_CUSTOM_ATTRIBUTES.exception_with_parameters(
                                    attr_name, type_name
                                )
                            else:
                                self.map_attr_name_to_id[type_id][attr_name] = attr_id

    def _get_id_for_name(self, name: str) -> str:
        """
        Translate the provided human-readable custom metadata set name to its Atlan-internal ID string.

        :param name: human-readable name of the custom metadata set
        :returns: Atlan-internal ID string of the custom metadata set
        :raises InvalidRequestError: if no name was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        if name is None or not name.strip():
            raise ErrorCode.MISSING_CM_NAME.exception_with_parameters()
        if cm_id := self.map_name_to_id.get(name):
            return cm_id
        # If not found, refresh the cache and look again (could be stale)
        self._refresh_cache()
        if cm_id := self.map_name_to_id.get(name):
            return cm_id
        raise ErrorCode.CM_NOT_FOUND_BY_NAME.exception_with_parameters(name)

    def _get_name_for_id(self, idstr: str) -> str:
        """
        Translate the provided Atlan-internal custom metadata ID string to the human-readable custom metadata set name.

        :param idstr: Atlan-internal ID string of the custom metadata set
        :returns: human-readable name of the custom metadata set
        :raises InvalidRequestError: if no ID was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        if idstr is None or not idstr.strip():
            raise ErrorCode.MISSING_CM_ID.exception_with_parameters()
        if cm_name := self.map_id_to_name.get(idstr):
            return cm_name
        # If not found, refresh the cache and look again (could be stale)
        self._refresh_cache()
        if cm_name := self.map_id_to_name.get(idstr):
            return cm_name
        raise ErrorCode.CM_NOT_FOUND_BY_ID.exception_with_parameters(idstr)

    def _get_all_custom_attributes(
        self, include_deleted: bool = False, force_refresh: bool = False
    ) -> Dict[str, List[AttributeDef]]:
        """
        Retrieve all the custom metadata attributes. The dict will be keyed by custom metadata set
        name, and the value will be a listing of all the attributes within that set (with all the details
        of each of those attributes).

        :param include_deleted: if True, include the archived (deleted) custom attributes; otherwise only
                                include active custom attributes
        :param force_refresh: if True, will refresh the custom metadata cache; if False, will only refresh the
                              cache if it is empty
        :returns: a dict from custom metadata set name to all details about its attributes
        :raises NotFoundError: if the custom metadata cannot be found
        """
        if len(self.cache_by_id) == 0 or force_refresh:
            self._refresh_cache()
        m = {}
        for type_id, cm in self.cache_by_id.items():
            type_name = self._get_name_for_id(type_id)
            if not type_name:
                raise ErrorCode.CM_NOT_FOUND_BY_ID.exception_with_parameters(type_id)
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

    def _get_attr_id_for_name(self, set_name: str, attr_name: str) -> str:
        """
        Translate the provided human-readable custom metadata set and attribute names to the Atlan-internal ID string
        for the attribute.

        :param set_name: human-readable name of the custom metadata set
        :param attr_name: human-readable name of the attribute
        :returns: Atlan-internal ID string for the attribute
        :raises NotFoundError: if the custom metadata attribute cannot be found
        """
        set_id = self._get_id_for_name(set_name)
        if sub_map := self.map_attr_name_to_id.get(set_id):
            if attr_id := sub_map.get(attr_name):
                # If found, return straight away
                return attr_id
        # Otherwise, refresh the cache and look again (could be stale)
        self._refresh_cache()
        if sub_map := self.map_attr_name_to_id.get(set_id):
            if attr_id := sub_map.get(attr_name):
                # If found, return straight away
                return attr_id
            raise ErrorCode.CM_ATTR_NOT_FOUND_BY_NAME.exception_with_parameters(
                set_name
            )
        raise ErrorCode.CM_ATTR_NOT_FOUND_BY_ID.exception_with_parameters(set_id)

    def _get_attr_name_for_id(self, set_id: str, attr_id: str) -> str:
        """
        Given the Atlan-internal ID string for the set and the Atlan-internal ID for the attribute return the
        human-readable custom metadata name for the attribute.

        :param set_id: Atlan-internal ID string for the custom metadata set
        :param attr_id: Atlan-internal ID string for the attribute
        :returns: human-readable name of the attribute
        :raises NotFoundError: if the custom metadata attribute cannot be found
        """
        if sub_map := self.map_attr_id_to_name.get(set_id):
            if attr_name := sub_map.get(attr_id):
                return attr_name
            self._refresh_cache()
            if sub_map := self.map_attr_id_to_name.get(set_id):
                if attr_name := sub_map.get(attr_id):
                    return attr_name
        raise ErrorCode.CM_ATTR_NOT_FOUND_BY_ID.exception_with_parameters(
            attr_id, set_id
        )

    def _is_attr_archived(self, attr_id: str) -> bool:
        """
        Determine if an attribute id is archived
        :param attr_id: Atlan-internal ID string for the attribute
        :returns: True if the attribute has been archived
        """

        return attr_id in self.archived_attr_ids

    def _get_attributes_for_search_results_(self, set_id: str) -> Optional[List[str]]:
        if sub_map := self.map_attr_name_to_id.get(set_id):
            attr_ids = sub_map.values()
            return [f"{set_id}.{idstr}" for idstr in attr_ids]
        return None

    def _get_attribute_for_search_results_(
        self, set_id: str, attr_name: str
    ) -> Optional[str]:
        if sub_map := self.map_attr_name_to_id.get(set_id):
            return sub_map.get(attr_name, None)
        return None

    def _get_attributes_for_search_results(self, set_name: str) -> Optional[List[str]]:
        """
        Retrieve the full set of custom attributes to include on search results.

        :param set_name: human-readable name of the custom metadata set for which to retrieve attribute names
        :returns: a list of the attribute names, strictly useful for inclusion in search results
        """
        if set_id := self._get_id_for_name(set_name):
            if dot_names := self._get_attributes_for_search_results_(set_id):
                return dot_names
            self._refresh_cache()
            return self._get_attributes_for_search_results_(set_id)
        return None

    def _get_attribute_for_search_results(
        self, set_name: str, attr_name: str
    ) -> Optional[str]:
        """
        Retrieve a single custom attribute name to include on search results.

        :param set_name: human-readable name of the custom metadata set for which to retrieve the custom metadata
                         attribute name
        :param attr_name: human-readable name of the attribute
        :returns: the attribute name, strictly useful for inclusion in search results
        """
        if set_id := self._get_id_for_name(set_name):
            if attr_id := self._get_attribute_for_search_results_(set_id, attr_name):
                return attr_id
            self._refresh_cache()
            return self._get_attribute_for_search_results_(set_id, attr_name)
        return None

    def _get_custom_metadata_def(self, name: str) -> CustomMetadataDef:
        """
        Retrieve the full custom metadata structure definition.

        :param name: human-readable name of the custom metadata set
        :returns: the full custom metadata structure definition for that set
        :raises InvalidRequestError: if no name was provided
        :raises NotFoundError: if the custom metadata cannot be found
        """
        ba_id = self._get_id_for_name(name)
        if typedef := self.cache_by_id.get(ba_id):
            return typedef
        else:
            raise ErrorCode.CM_NOT_FOUND_BY_NAME.exception_with_parameters(name)

    def _get_attribute_def(self, attr_id: str) -> AttributeDef:
        """
        Retrieve a specific custom metadata attribute definition by its unique Atlan-internal ID string.

        :param attr_id: Atlan-internal ID string for the custom metadata attribute
        :returns: attribute definition for the custom metadata attribute
        :raises InvalidRequestError: if no attribute ID was provided
        :raises NotFoundError: if the custom metadata attribute cannot be found
        """
        if not attr_id:
            raise ErrorCode.MISSING_CM_ATTR_ID.exception_with_parameters()
        if self.attr_cache_by_id is None:
            self._refresh_cache()
        if attr_def := self.attr_cache_by_id.get(attr_id):
            return attr_def
        raise ErrorCode.CM_ATTR_NOT_FOUND_BY_ID.exception_with_parameters(
            attr_id, "(unknown)"
        )
