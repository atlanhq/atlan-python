# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared logic for user cache operations.
"""

from __future__ import annotations

from typing import Dict

from pyatlan.model.user import AtlanUser


class UserCacheCommon:
    """Shared logic for user cache operations."""

    @staticmethod
    def refresh_cache_data(users: list[AtlanUser]) -> tuple:
        """
        Process user list to extract user cache data.

        :param users: list of AtlanUser objects from API
        :returns: tuple of (map_id_to_name, map_name_to_id, map_email_to_id)
        """
        map_id_to_name: Dict[str, str] = {}
        map_name_to_id: Dict[str, str] = {}
        map_email_to_id: Dict[str, str] = {}

        for user in users:
            user_id = str(user.id)
            username = str(user.username)
            user_email = str(user.email)
            map_id_to_name[user_id] = username
            map_name_to_id[username] = user_id
            map_email_to_id[user_email] = user_id

        return map_id_to_name, map_name_to_id, map_email_to_id
