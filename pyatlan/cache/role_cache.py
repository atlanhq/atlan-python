
from pyatlan.client.atlan import AtlanClient
from pyatlan.client.role import RoleClient
from pyatlan.model.role import AtlanRole

from typing import Optional

class RoleCache():

    cache_by_id: dict[str, AtlanRole] = dict()
    map_id_to_name: dict[str, str] = dict()
    map_name_to_id: dict[str, str] = dict()

    @classmethod
    def _refresh_cache(cls) -> None:
        print("Refreshing role cache...")
        response = RoleClient(AtlanClient()).get_all_roles()
        if response is not None:
            cls.cache_by_id = dict()
            cls.map_id_to_name = dict()
            cls.map_name_to_id = dict()
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
        role_id = cls.map_name_to_id.get(name)
        if role_id:
            return role_id
        else:
            cls._refresh_cache()
            return cls.map_name_to_id.get(name)

    @classmethod
    def get_name_for_id(cls, id: str) -> Optional[str]:
        """
        Translate the provided role GUID to the human-readable role name.
        """
        role_name = cls.map_id_to_name.get(id)
        if role_name:
            return role_name
        else:
            cls._refresh_cache()
            return cls.map_id_to_name.get(id)
