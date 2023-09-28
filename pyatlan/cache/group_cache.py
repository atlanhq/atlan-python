# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Iterable, Optional

from pyatlan.model.group import GroupProvider


class GroupCache:
    """
    Lazily-loaded cache for translating Atlan-internal groups into their various IDs.
    """

    caches: dict[int, "GroupCache"] = {}

    @classmethod
    def get_cache(cls) -> "GroupCache":
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient.get_default_client()
        cache_key = client.cache_key
        if cache_key not in cls.caches:
            cls.caches[cache_key] = GroupCache(provider=client)
        return cls.caches[cache_key]

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable group name to its GUID.

        :param name: human-readable name of the group
        :returns: unique identifier (GUID) of the group
        """
        return cls.get_cache()._get_id_for_name(name=name)

    @classmethod
    def get_id_for_alias(cls, alias: str) -> Optional[str]:
        """
        Translate the provided alias to its GUID.

        :param alias: name of the group as it appears in the UI
        :returns: unique identifier (GUID) of the group
        """
        return cls.get_cache()._get_id_for_alias(alias=alias)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided group GUID to the human-readable group name.

        :param idstr: unique identifier (GUID) of the group
        :returns: human-readable name of the group
        """
        return cls.get_cache()._get_name_for_id(idstr=idstr)

    @classmethod
    def validate_aliases(cls, aliases: Iterable[str]):
        """
        Validate that the given human-readable group aliases are valid. A ValueError will be raised in any are not.

        :param aliases: a collection of group aliases to be checked
        """
        return cls.get_cache()._validate_aliases(aliases)

    def __init__(self, provider: GroupProvider):
        self.provider = provider
        self.map_id_to_name: dict[str, str] = {}
        self.map_name_to_id: dict[str, str] = {}
        self.map_alias_to_id: dict[str, str] = {}

    def _refresh_cache(self) -> None:
        groups = self.provider.get_all_groups()
        if groups is not None:
            self.map_id_to_name = {}
            self.map_name_to_id = {}
            self.map_alias_to_id = {}
            for group in groups:
                group_id = str(group.id)
                group_name = str(group.name)
                group_alias = str(group.alias)
                self.map_id_to_name[group_id] = group_name
                self.map_name_to_id[group_name] = group_id
                self.map_alias_to_id[group_alias] = group_id

    def _get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable group name to its GUID.

        :param name: human-readable name of the group
        :returns: unique identifier (GUID) of the group
        """
        if group_id := self.map_name_to_id.get(name):
            return group_id
        self._refresh_cache()
        return self.map_name_to_id.get(name)

    def _get_id_for_alias(self, alias: str) -> Optional[str]:
        """
        Translate the provided alias to its GUID.

        :param alias: name of the group as it appears in the UI
        :returns: unique identifier (GUID) of the group
        """
        if group_id := self.map_alias_to_id.get(alias):
            return group_id
        self._refresh_cache()
        return self.map_alias_to_id.get(alias)

    def _get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided group GUID to the human-readable group name.

        :param idstr: unique identifier (GUID) of the group
        :returns: human-readable name of the group
        """
        if group_name := self.map_id_to_name.get(idstr):
            return group_name
        self._refresh_cache()
        return self.map_id_to_name.get(idstr)

    def _validate_aliases(self, aliases: Iterable[str]):
        """
        Validate that the given human-readable group aliases are valid. A ValueError will be raised in any are not.

        :param aliases: a collection of group aliases to be checked
        """
        for group_alias in aliases:
            if not self.get_id_for_alias(group_alias):
                raise ValueError(
                    f"Provided group name {group_alias} was not found in Atlan."
                )
