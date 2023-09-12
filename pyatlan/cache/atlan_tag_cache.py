# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.typedef import AtlanTagDef, TypeDefResponseProvider


class AtlanTagCache:
    """
    Lazily-loaded cache for translating between Atlan-internal ID strings and human-readable names
    for Atlan tags.
    """

    caches: dict[int, "AtlanTagCache"] = {}

    @classmethod
    def get_cache(cls) -> "AtlanTagCache":
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient.get_default_client()
        cache_key = client.cache_key
        if cache_key not in cls.caches:
            cls.caches[cache_key] = AtlanTagCache(provider=client)
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

    def __init__(self, provider: TypeDefResponseProvider):
        self.provider = provider
        self.cache_by_id: dict[str, AtlanTagDef] = dict()
        self.map_id_to_name: dict[str, str] = dict()
        self.map_name_to_id: dict[str, str] = dict()
        self.deleted_ids: set[str] = set()
        self.deleted_names: set[str] = set()

    def _refresh_cache(self) -> None:
        """
        Refreshes the cache of Atlan tags by requesting the full set of Atlan tags from Atlan.
        """
        response = self.provider.get_typedefs(
            type_category=AtlanTypeCategory.CLASSIFICATION
        )
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

    def _get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable Atlan tag name to its Atlan-internal ID string.

        :param name: human-readable name of the Atlan tag
        :returns: Atlan-internal ID string of the Atlan tag
        """
        cls_id = self.map_name_to_id.get(name)
        if not cls_id and name not in self.deleted_names:
            # If not found, refresh the cache and look again (could be stale)
            self.refresh_cache()
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
            self.refresh_cache()
            cls_name = self.map_id_to_name.get(idstr)
            if not cls_name:
                # If still not found after refresh, mark it as deleted (could be
                # an entry in an audit log that refers to a classification that
                # no longer exists)
                self.deleted_ids.add(idstr)
        return cls_name
