# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING, Dict, Iterable, Optional

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

lock: Lock = Lock()


class GroupCache:
    """
    Lazily-loaded cache for translating Atlan-internal groups into their various IDs.
    """

    caches: Dict[int, "GroupCache"] = {}

    def __init__(self, client: AtlanClient):
        self.client: AtlanClient = client
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.map_alias_to_id: Dict[str, str] = {}
        self.lock: Lock = Lock()

    def get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided internal group name to its GUID.

        :param name: human-readable name of the group
        :returns: unique identifier (GUID) of the group
        """
        return self._get_id_for_name(name=name)

    def get_id_for_alias(self, alias: str) -> Optional[str]:
        """
        Translate the provided human-readable group name to its GUID.

        :param alias: name of the group as it appears in the UI
        :returns: unique identifier (GUID) of the group
        """
        return self._get_id_for_alias(alias=alias)

    def get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided group GUID to the internal group name.

        :param idstr: unique identifier (GUID) of the group
        :returns: human-readable name of the group
        """
        return self._get_name_for_id(idstr=idstr)

    def validate_aliases(self, aliases: Iterable[str]):
        """
        Validate that the given (internal) group names are valid. A ValueError will be raised in any are not.

        :param aliases: a collection of (internal) group names to be checked
        """
        return self._validate_aliases(aliases)

    def _refresh_cache(self) -> None:
        with self.lock:
            groups = self.client.group.get_all()
            if not groups:
                return
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
        Translate the provided internal group name to its GUID.

        :param name: internal name of the group
        :returns: unique identifier (GUID) of the group
        """
        if group_id := self.map_name_to_id.get(name):
            return group_id
        self._refresh_cache()
        return self.map_name_to_id.get(name)

    def _get_id_for_alias(self, alias: str) -> Optional[str]:
        """
        Translate the provided human-readable group name to its GUID.

        :param alias: name of the group as it appears in the UI
        :returns: unique identifier (GUID) of the group
        """
        if group_id := self.map_alias_to_id.get(alias):
            return group_id
        self._refresh_cache()
        return self.map_alias_to_id.get(alias)

    def _get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided group GUID to the internal group name.

        :param idstr: unique identifier (GUID) of the group
        :returns: internal name of the group
        """
        if group_name := self.map_id_to_name.get(idstr):
            return group_name
        self._refresh_cache()
        return self.map_id_to_name.get(idstr)

    def _validate_aliases(self, aliases: Iterable[str]):
        """
        Validate that the given (internal) group names are valid. A ValueError will be raised in any are not.

        :param aliases: a collection of (internal) group names to be checked
        """
        for group_alias in aliases:
            if not self.get_id_for_name(group_alias):
                raise ValueError(
                    f"Provided group name {group_alias} was not found in Atlan."
                )
