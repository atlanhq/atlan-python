# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import AtlanTagDef


class AtlanTagCache:
    """
    Lazily-loaded cache for translating between Atlan-internal ID strings and human-readable names
    for Atlan tags.
    """

    cache_by_id: dict[str, AtlanTagDef] = dict()
    map_id_to_name: dict[str, str] = dict()
    map_name_to_id: dict[str, str] = dict()
    deleted_ids: set[str] = set()
    deleted_names: set[str] = set()

    @classmethod
    def refresh_cache(cls) -> None:
        """
        Refreshes the cache of Atlan tags by requesting the full set of Atlan tags from Atlan.
        """
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient.get_default_client()
        if client is None:
            client = AtlanClient()
        response = client.get_typedefs(type_category=AtlanTypeCategory.CLASSIFICATION)
        if response is not None:
            cls.cache_by_id = {}
            cls.map_id_to_name = {}
            cls.map_name_to_id = {}
            for atlan_tag in response.atlan_tag_defs:
                atlan_tag_id = atlan_tag.name
                atlan_tag_name = atlan_tag.display_name
                cls.cache_by_id[atlan_tag_id] = atlan_tag
                cls.map_id_to_name[atlan_tag_id] = atlan_tag_name
                cls.map_name_to_id[atlan_tag_name] = atlan_tag_id

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable Atlan tag name to its Atlan-internal ID string.

        :param name: human-readable name of the Atlan tag
        :returns: Atlan-internal ID string of the Atlan tag
        """
        cls_id = cls.map_name_to_id.get(name)
        if not cls_id and name not in cls.deleted_names:
            # If not found, refresh the cache and look again (could be stale)
            cls.refresh_cache()
            cls_id = cls.map_name_to_id.get(name)
            if not cls_id:
                # If still not found after refresh, mark it as deleted (could be
                # an entry in an audit log that refers to a classification that
                # no longer exists)
                cls.deleted_names.add(name)
        return cls_id

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided Atlan-internal classification ID string to the human-readable Atlan tag name.

        :param idstr: Atlan-internal ID string of the Atlan tag
        :returns: human-readable name of the Atlan tag
        """
        cls_name = cls.map_id_to_name.get(idstr)
        if not cls_name and idstr not in cls.deleted_ids:
            # If not found, refresh the cache and look again (could be stale)
            cls.refresh_cache()
            cls_name = cls.map_id_to_name.get(idstr)
            if not cls_name:
                # If still not found after refresh, mark it as deleted (could be
                # an entry in an audit log that refers to a classification that
                # no longer exists)
                cls.deleted_ids.add(idstr)
        return cls_name
