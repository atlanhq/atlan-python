# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Admin models for Atlan user and group management.

This module provides msgspec.Struct classes for the Atlan admin API,
covering users, groups, and related response types.
"""

from .groups import AtlanGroup, CreateGroupResponse, GroupResponse
from .users import AtlanUser, UserMinimalResponse, UserResponse

__all__ = [
    # Users
    "AtlanUser",
    "UserResponse",
    "UserMinimalResponse",
    # Groups
    "AtlanGroup",
    "GroupResponse",
    "CreateGroupResponse",
]
