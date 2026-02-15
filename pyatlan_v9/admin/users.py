# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
User-related admin models.

This module contains msgspec.Struct classes for Atlan user management.
"""

from __future__ import annotations

from typing import Any, Union

import msgspec
from msgspec import UNSET, UnsetType


class AtlanUser(msgspec.Struct, kw_only=True, omit_defaults=True, rename="camel"):
    """
    Represents an Atlan user.

    Contains user profile information and metadata from the Atlan admin API.
    """

    id: Union[str, UnsetType] = UNSET
    """Unique identifier (GUID) for the user."""

    username: Union[str, UnsetType] = UNSET
    """Username of the user."""

    email: Union[str, None, UnsetType] = UNSET
    """Email address of the user."""

    first_name: Union[str, None, UnsetType] = UNSET
    """First name of the user."""

    last_name: Union[str, None, UnsetType] = UNSET
    """Last name of the user."""

    enabled: Union[bool, UnsetType] = UNSET
    """Whether the user is enabled."""

    email_verified: Union[bool, UnsetType] = UNSET
    """Whether the user's email is verified."""

    workspace_role: Union[str, None, UnsetType] = UNSET
    """Role of the user in the workspace."""

    group_count: Union[int, UnsetType] = UNSET
    """Number of groups the user belongs to."""

    created_timestamp: Union[int, None, UnsetType] = UNSET
    """Timestamp when the user was created (epoch milliseconds)."""

    last_login_time: Union[int, None, UnsetType] = UNSET
    """Timestamp of the user's last login (epoch milliseconds)."""

    attributes: Union[dict[str, Any], None, UnsetType] = UNSET
    """Custom attributes for the user."""

    personas: Union[list[dict[str, Any]], None, UnsetType] = UNSET
    """Personas assigned to the user."""

    roles: Union[list[str], None, UnsetType] = UNSET
    """Roles assigned to the user."""

    default_roles: Union[list[str], None, UnsetType] = UNSET
    """Default roles for the user."""

    is_locked: Union[bool, UnsetType] = UNSET
    """Whether the user account is locked."""

    login_events: Union[list[dict[str, Any]], None, UnsetType] = UNSET
    """Recent login events for the user."""


class UserResponse(msgspec.Struct, kw_only=True, omit_defaults=True, rename="camel"):
    """
    Response from user list operations.

    Contains paginated user records and count metadata.
    """

    records: list[AtlanUser] = msgspec.field(default_factory=list)
    """List of users in this response page."""

    total_record: int = 0
    """Total number of records matching the query."""

    filter_record: int = 0
    """Number of records after filtering."""


class UserMinimalResponse(
    msgspec.Struct, kw_only=True, omit_defaults=True, rename="camel"
):
    """
    Minimal response for user operations like update or get current user.

    Contains only basic user identification.
    """

    id: Union[str, UnsetType] = UNSET
    """Unique identifier (GUID) for the user."""

    username: Union[str, UnsetType] = UNSET
    """Username of the user."""

    email: Union[str, None, UnsetType] = UNSET
    """Email address of the user."""
