# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.client.atlan import AtlanClient


class GroupCache:
    """
    Lazily-loaded cache for translating Atlan-internal groups into their various IDs.
    """

    map_id_to_name: dict[str, str] = dict()
    map_name_to_id: dict[str, str] = dict()
    map_alias_to_id: dict[str, str] = dict()

    @classmethod
    def _refresh_cache(cls) -> None:
        client = AtlanClient.get_default_client()
        if client is None:
            client = AtlanClient()
        groups = client.get_all_groups()
        if groups is not None:
            cls.map_id_to_name = {}
            cls.map_name_to_id = {}
            cls.map_alias_to_id = {}
            for group in groups:
                group_id = str(group.id)
                group_name = str(group.name)
                group_alias = str(group.alias)
                cls.map_id_to_name[group_id] = group_name
                cls.map_name_to_id[group_name] = group_id
                cls.map_alias_to_id[group_alias] = group_id

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable group name to its GUID.

        :param name: human-readable name of the group
        :returns: unique identifier (GUID) of the group
        """
        if group_id := cls.map_name_to_id.get(name):
            return group_id
        cls._refresh_cache()
        return cls.map_name_to_id.get(name)

    @classmethod
    def get_id_for_alias(cls, alias: str) -> Optional[str]:
        """
        Translate the provided alias to its GUID.

        :param alias: name of the group as it appears in the UI
        :returns: unique identifier (GUID) of the group
        """
        if group_id := cls.map_alias_to_id.get(alias):
            return group_id
        cls._refresh_cache()
        return cls.map_alias_to_id.get(alias)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided group GUID to the human-readable group name.

        :param idstr: unique identifier (GUID) of the group
        :returns: human-readable name of the group
        """
        if group_name := cls.map_id_to_name.get(idstr):
            return group_name
        cls._refresh_cache()
        return cls.map_id_to_name.get(idstr)
