# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared logic for role cache operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from pyatlan.model.role import AtlanRole

if TYPE_CHECKING:
    pass


class RoleCacheCommon:
    """Shared logic for role cache operations."""

    @staticmethod
    def refresh_cache_data(roles: list[AtlanRole]) -> tuple:
        """
        Process role list to extract role cache data.

        :param roles: list of AtlanRole objects from API
        :returns: tuple of (cache_by_id, map_id_to_name, map_name_to_id)
        """
        cache_by_id: Dict[str, AtlanRole] = {}
        map_id_to_name: Dict[str, str] = {}
        map_name_to_id: Dict[str, str] = {}

        for role in roles:
            role_id = role.id
            role_name = role.name
            if role_id and role_name:
                cache_by_id[role_id] = role
                map_id_to_name[role_id] = role_name
                map_name_to_id[role_name] = role_id

        return cache_by_id, map_id_to_name, map_name_to_id
