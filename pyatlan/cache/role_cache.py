# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from threading import Lock
from typing import TYPE_CHECKING, Dict, Iterable, Optional

from pyatlan.cache.common import RoleCacheCommon
from pyatlan.client.constants import GET_KEYCLOAK_USER_ROLE_MAPPING
from pyatlan.model.role import AtlanRole

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient

lock: Lock = Lock()


class RoleCache:
    """
    Lazily-loaded cache for translating Atlan-internal roles into their various IDs.
    """

    def __init__(self, client: AtlanClient):
        self.client: AtlanClient = client
        self.cache_by_id: Dict[str, AtlanRole] = {}
        self.map_id_to_name: Dict[str, str] = {}
        self.map_name_to_id: Dict[str, str] = {}
        self.lock: Lock = Lock()
        self._is_api_token_user: Optional[bool] = None

    def get_id_for_name(self, name: str) -> Optional[str]:
        """
        Translate the provided human-readable role name to its GUID.

        :param name: human-readable name of the role
        :returns: unique identifier (GUID) of the role
        """
        return self._get_id_for_name(name=name)

    def get_name_for_id(self, idstr: str) -> Optional[str]:
        """
        Translate the provided role GUID to the human-readable role name.

        :param idstr: unique identifier (GUID) of the role
        :returns: human-readable name of the role
        """
        return self._get_name_for_id(idstr=idstr)

    def validate_idstrs(self, idstrs: Iterable[str]):
        """
        Validate that the given role GUIDs are valid. A ValueError will be raised in any are not.

        :param idstrs: a collection of unique identifiers (GUID) of the roles to be checked
        """
        return self._validate_idstrs(idstrs=idstrs)

    def _refresh_cache(self) -> None:
        with self.lock:
            response = self.client.role.get(
                limit=100, post_filter='{"name":{"$ilike":"$%"}}'
            )
            if not response:
                return

            # Process response using shared logic
            (self.cache_by_id, self.map_id_to_name, self.map_name_to_id) = (
                RoleCacheCommon.refresh_cache_data(response.records)
            )

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

    def is_api_token_user(self) -> bool:
        """
        Check if the current user is authenticated via an API token or OAuth client.
        This method checks for the presence of $api-token-default-access or $admin roles.

        :returns: True if the user is an API token user, False otherwise
        """
        if self._is_api_token_user is not None:
            return self._is_api_token_user

        # Get current user to retrieve their UUID
        current_user = self.client.user.get_current()

        # Fetch role mappings for the current user
        raw_json = self.client._call_api(
            api=GET_KEYCLOAK_USER_ROLE_MAPPING.format_path(
                {"user_uuid": current_user.id}
            )
        )

        # Check if the user has $api-token-default-access or $admin roles
        for role_mapping in raw_json["realmMappings"]:
            role_name = role_mapping.get("name")
            if role_name in ["$api-token-default-access", "$admin"]:
                self._is_api_token_user = True
                return self._is_api_token_user

        self._is_api_token_user = False
        return self._is_api_token_user
