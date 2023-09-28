# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Iterable, Optional

from pyatlan.model.role import AtlanRole, RoleProvider


class RoleCache:
    """
    Lazily-loaded cache for translating Atlan-internal roles into their various IDs.
    """

    caches: dict[int, "RoleCache"] = {}

    @classmethod
    def get_cache(cls) -> "RoleCache":
        from pyatlan.client.atlan import AtlanClient

        client = AtlanClient.get_default_client()
        cache_key = client.cache_key
        if cache_key not in cls.caches:
            cls.caches[cache_key] = RoleCache(provider=client)
        return cls.caches[cache_key]

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable role name to its GUID.

        :param name: human-readable name of the role
        :returns: unique identifier (GUID) of the role
        """
        return cls.get_cache()._get_id_for_name(name=name)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided role GUID to the human-readable role name.

        :param idstr: unique identifier (GUID) of the role
        :returns: human-readable name of the role
        """
        return cls.get_cache()._get_name_for_id(idstr=idstr)

    @classmethod
    def validate_idstrs(cls, idstrs: Iterable[str]):
        """
        Validate that the given role GUIDs are valid. A ValueError will be raised in any are not.

        :param idstrs: a collection of unique identifiers (GUID) of the roles to be checked
        """
        return cls.get_cache()._validate_idstrs(idstrs=idstrs)

    def __init__(self, provider: RoleProvider):
        self.provider = provider
        self.cache_by_id: dict[str, AtlanRole] = {}
        self.map_id_to_name: dict[str, str] = {}
        self.map_name_to_id: dict[str, str] = {}

    def _refresh_cache(self) -> None:
        response = self.provider.get_roles(
            limit=100, post_filter='{"name":{"$ilike":"$%"}}'
        )
        if response is not None:
            self.cache_by_id = {}
            self.map_id_to_name = {}
            self.map_name_to_id = {}
            for role in response.records:
                role_id = role.id
                role_name = role.name
                self.cache_by_id[role_id] = role
                self.map_id_to_name[role_id] = role_name
                self.map_name_to_id[role_name] = role_id

    def _get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable role name to its GUID.

        :param name: human-readable name of the role
        :returns: unique identifier (GUID) of the role
        """
        if role_id := self.map_name_to_id.get(name):
            return role_id
        self._refresh_cache()
        return self.map_name_to_id.get(name)

    def _get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided role GUID to the human-readable role name.

        :param idstr: unique identifier (GUID) of the role
        :returns: human-readable name of the role
        """
        if role_name := self.map_id_to_name.get(idstr):
            return role_name
        self._refresh_cache()
        return self.map_id_to_name.get(idstr)

    def _validate_idstrs(self, idstrs: Iterable[str]):
        """
        Validate that the given role GUIDs are valid. A ValueError will be raised in any are not.

        :param idstrs: a collection of unique identifiers (GUID) of the roles to be checked
        """
        for role_id in idstrs:
            if not self.get_name_for_id(role_id):
                raise ValueError(f"Provided role ID {role_id} was not found in Atlan.")
