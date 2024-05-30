# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from threading import Lock
from typing import Dict, Optional, Set

from pyatlan.client.typedef import TypeDefClient
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import AtlanTagDef

lock: Lock = Lock()


class AtlanTagCache:
    """
    Lazily-loaded cache for translating between Atlan-internal ID strings and human-readable names
    for Atlan tags.
    """

    caches: Dict[int, "AtlanTagCache"] = {}

    @classmethod
    def get_cache(cls) -> "AtlanTagCache":
        from pyatlan.client.atlan import AtlanClient

        with lock:
            client = AtlanClient.get_default_client()
            cache_key = client.cache_key
            if cache_key not in cls.caches:
                cls.caches[cache_key] = AtlanTagCache(typedef_client=client.typedef)
            return cls.caches[cache_key]

    @classmethod
    def refresh_cache(cls) -> None:
        """
        Refreshes the cache of Atlan tags by requesting the full set of Atlan tags from Atlan.
        """
        cls.get_cache()._refresh_cache()

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable Atlan tag name to its Atlan-internal ID string.

        :param name: human-readable name of the Atlan tag
        :returns: Atlan-internal ID string of the Atlan tag
        """
        return cls.get_cache()._get_id_for_name(name=name)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal classification ID string to the human-readable Atlan tag name.

        :param idstr: Atlan-internal ID string of the Atlan tag
        :returns: human-readable name of the Atlan tag
        """
        return cls.get_cache()._get_name_for_id(idstr=idstr)

    @classmethod
    def get_source_tags_attr_id(cls, id: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal Atlan tag ID string to the Atlan-internal name of the attribute that
        captures tag attachment details (for source-synced tags).

        :param id: Atlan-internal ID string of the Atlan tag
        :returns: Atlan-internal ID string of the attribute containing source-synced tag attachment details
        """
        return cls.get_cache()._get_source_tags_attr_id(id)

    def __init__(self, typedef_client: TypeDefClient):
        self.typdef_client: TypeDefClient = typedef_client
        self.cache_by_id: Dict[str, AtlanTagDef] = {}
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.deleted_ids: Set[str] = set()
        self.deleted_names: Set[str] = set()
        self.map_id_to_source_tags_attr_id: Dict[str, str] = {}
        self.lock: Lock = Lock()

    def _refresh_cache(self) -> None:
        """
        Refreshes the cache of Atlan tags by requesting the full set of Atlan tags from Atlan.
        """
        with self.lock:
            response = self.typdef_client.get(
                type_category=[
                    AtlanTypeCategory.CLASSIFICATION,
                    AtlanTypeCategory.STRUCT,
                ]
            )
            if not response or not response.struct_defs:
                raise ErrorCode.EXPIRED_API_TOKEN.exception_with_parameters()
            if response is not None:
                self.cache_by_id = {}
                self.map_id_to_name = {}
                self.map_name_to_id = {}
                for atlan_tag in response.atlan_tag_defs:
                    atlan_tag_id = atlan_tag.name
                    atlan_tag_name = atlan_tag.display_name
                    self.cache_by_id[atlan_tag_id] = atlan_tag
                    self.map_id_to_name[atlan_tag_id] = atlan_tag_name
                    self.map_name_to_id[atlan_tag_name] = atlan_tag_id
                    sourceTagsId = ""
                    for attr_def in atlan_tag.attribute_defs or []:
                        if attr_def.display_name == "sourceTagAttachment":
                            sourceTagsId = attr_def.name or ""
                    self.map_id_to_source_tags_attr_id[atlan_tag_id] = sourceTagsId

    def _get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable Atlan tag name to its Atlan-internal ID string.

        :param name: human-readable name of the Atlan tag
        :returns: Atlan-internal ID string of the Atlan tag
        """
        cls_id = self.map_name_to_id.get(name)
        if not cls_id and name not in self.deleted_names:
            # If not found, refresh the cache and look again (could be stale)
            self._refresh_cache()
            cls_id = self.map_name_to_id.get(name)
            if not cls_id:
                # If still not found after refresh, mark it as deleted (could be
                # an entry in an audit log that refers to a classification that
                # no longer exists)
                self.deleted_names.add(name)
        return cls_id

    def _get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal classification ID string to the human-readable Atlan tag name.

        :param idstr: Atlan-internal ID string of the Atlan tag
        :returns: human-readable name of the Atlan tag
        """
        cls_name = self.map_id_to_name.get(idstr)
        if not cls_name and idstr not in self.deleted_ids:
            # If not found, refresh the cache and look again (could be stale)
            self._refresh_cache()
            cls_name = self.map_id_to_name.get(idstr)
            if not cls_name:
                # If still not found after refresh, mark it as deleted (could be
                # an entry in an audit log that refers to a classification that
                # no longer exists)
                self.deleted_ids.add(idstr)
        return cls_name

    def _get_source_tags_attr_id(self, id: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal Atlan tag ID string to the Atlan-internal name of the attribute that
        captures tag attachment details (for source-synced tags).

        :param id: Atlan-internal ID string of the Atlan tag
        :returns: Atlan-internal ID string of the attribute containing source-synced tag attachment details
        """
        if id and id.strip():
            attr_id = self.map_id_to_source_tags_attr_id.get(id)
            if attr_id is not None or id in self.deleted_ids:
                return attr_id
            self.refresh_cache()
            if attr_id := self.map_id_to_source_tags_attr_id.get(id):
                return attr_id
            self.deleted_ids.add(id)
            raise ErrorCode.ATLAN_TAG_NOT_FOUND_BY_ID.exception_with_parameters(id)
        raise ErrorCode.MISSING_ATLAN_TAG_ID.exception_with_parameters()
