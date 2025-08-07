# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Shared cache logic for sync and async cache implementations.

This package contains all shared business logic used by both
sync and async cache implementations following the sandwich pattern.

All classes here use static methods for prepare_request() and process_response()
to ensure zero code duplication between sync and async cache implementations.
"""

from __future__ import annotations

# Cache shared logic classes
from .atlan_tag_cache import AtlanTagCacheCommon
from .custom_metadata_cache import CustomMetadataCacheCommon
from .dq_template_config_cache import DQTemplateConfigCacheCommon
from .enum_cache import EnumCacheCommon
from .group_cache import GroupCacheCommon
from .role_cache import RoleCacheCommon
from .user_cache import UserCacheCommon

__all__ = [
    # Cache shared logic classes
    "AtlanTagCacheCommon",
    "CustomMetadataCacheCommon",
    "DQTemplateConfigCacheCommon",
    "EnumCacheCommon",
    "GroupCacheCommon",
    "RoleCacheCommon",
    "UserCacheCommon",
]
