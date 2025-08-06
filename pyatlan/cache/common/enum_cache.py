# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared logic for enum cache operations.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from pyatlan.model.typedef import EnumDef

if TYPE_CHECKING:
    from pyatlan.model.typedef import TypeDefResponse


class EnumCacheCommon:
    """Shared logic for enum cache operations."""

    @staticmethod
    def refresh_cache_data(response: TypeDefResponse) -> Dict[str, EnumDef]:
        """
        Process typedef response to extract enum cache data.

        :param response: TypeDefResponse from API
        :returns: dictionary mapping enum names to EnumDef objects
        """
        cache_by_name: Dict[str, EnumDef] = {}

        if response and response.enum_defs:
            for enum in response.enum_defs:
                type_name = enum.name
                cache_by_name[type_name] = enum

        return cache_by_name
