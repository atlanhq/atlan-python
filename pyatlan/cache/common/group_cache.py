# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared logic for group cache operations.
"""

from __future__ import annotations

from typing import Dict

from pyatlan.model.group import AtlanGroup


class GroupCacheCommon:
    """Shared logic for group cache operations."""

    @staticmethod
    def refresh_cache_data(groups: list[AtlanGroup]) -> tuple:
        """
        Process group list to extract group cache data.

        :param groups: list of AtlanGroup objects from API
        :returns: tuple of (map_id_to_name, map_name_to_id, map_alias_to_id)
        """
        map_id_to_name: Dict[str, str] = {}
        map_name_to_id: Dict[str, str] = {}
        map_alias_to_id: Dict[str, str] = {}

        for group in groups:
            group_id = str(group.id)
            group_name = str(group.name)
            group_alias = str(group.alias)
            map_id_to_name[group_id] = group_name
            map_name_to_id[group_name] = group_id
            map_alias_to_id[group_alias] = group_id

        return map_id_to_name, map_name_to_id, map_alias_to_id
