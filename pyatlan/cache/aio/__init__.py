# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Async cache modules for Atlan.

This module provides async versions of all cache functionality
with the same API as the sync versions, just requiring await.

Pattern: All async cache methods reuse shared business logic from pyatlan.cache.common
to ensure identical behavior with sync cache implementations.
"""

from .atlan_tag_cache import AsyncAtlanTagCache
from .connection_cache import AsyncConnectionCache
from .custom_metadata_cache import AsyncCustomMetadataCache
from .dq_template_config_cache import AsyncDQTemplateConfigCache
from .enum_cache import AsyncEnumCache
from .group_cache import AsyncGroupCache
from .role_cache import AsyncRoleCache
from .source_tag_cache import AsyncSourceTagCache
from .user_cache import AsyncUserCache

__all__ = [
    "AsyncAtlanTagCache",
    "AsyncConnectionCache",
    "AsyncCustomMetadataCache",
    "AsyncDQTemplateConfigCache",
    "AsyncEnumCache",
    "AsyncGroupCache",
    "AsyncRoleCache",
    "AsyncSourceTagCache",
    "AsyncUserCache",
]
