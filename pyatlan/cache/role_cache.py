# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Optional

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.role import AtlanRole


class RoleCache:

    cache_by_id: dict[str, AtlanRole] = dict()
    map_id_to_name: dict[str, str] = dict()
    map_name_to_id: dict[str, str] = dict()

    @classmethod
    def _refresh_cache(cls) -> None:
        client = AtlanClient.get_default_client()
        if client is None:
            client = AtlanClient()
        response = client.get_all_roles()
        if response is not None:
            cls.cache_by_id = {}
            cls.map_id_to_name = {}
            cls.map_name_to_id = {}
            for role in response.records:
                role_id = role.id
                role_name = role.name
                cls.cache_by_id[role_id] = role
                cls.map_id_to_name[role_id] = role_name
                cls.map_name_to_id[role_name] = role_id

    @classmethod
    def get_id_for_name(cls, name: str) -> Optional[str]:
        """
        Translate the provided human-readable role name to its GUID.
        """
        if role_id := cls.map_name_to_id.get(name):
            return role_id
        cls._refresh_cache()
        return cls.map_name_to_id.get(name)

    @classmethod
    def get_name_for_id(cls, idstr: str) -> Optional[str]:
        """
        Translate the provided role GUID to the human-readable role name.
        """
        if role_name := cls.map_id_to_name.get(idstr):
            return role_name
        cls._refresh_cache()
        return cls.map_id_to_name.get(idstr)
