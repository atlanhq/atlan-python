# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
Group-related admin models.

This module contains msgspec.Struct classes for Atlan group management.
"""

from __future__ import annotations

from typing import Any, Union

import msgspec
from msgspec import UNSET, UnsetType


class AtlanGroup(msgspec.Struct, kw_only=True, omit_defaults=True, rename="camel"):
    """
    Represents an Atlan group.

    Contains group information and metadata from the Atlan admin API.
    """

    id: Union[str, None, UnsetType] = UNSET
    """Unique identifier (GUID) for the group."""

    name: Union[str, None, UnsetType] = UNSET
    """Internal name of the group (auto-generated from alias)."""

    alias: Union[str, None, UnsetType] = UNSET
    """Human-readable name of the group (as shown in UI)."""

    path: Union[str, None, UnsetType] = UNSET
    """Path of the group in the hierarchy."""

    description: Union[str, None, UnsetType] = UNSET
    """Description of the group."""

    is_default: Union[bool, UnsetType] = UNSET
    """Whether this is a default group."""

    user_count: Union[int, UnsetType] = UNSET
    """Number of users in the group."""

    attributes: Union[dict[str, Any], None, UnsetType] = UNSET
    """Custom attributes for the group."""

    personas: Union[list[dict[str, Any]], None, UnsetType] = UNSET
    """Personas assigned to the group."""

    purposes: Union[list[dict[str, Any]], None, UnsetType] = UNSET
    """Purposes assigned to the group."""


class GroupResponse(msgspec.Struct, kw_only=True, omit_defaults=True, rename="camel"):
    """
    Response from group list operations.

    Contains paginated group records and count metadata.
    """

    records: list[AtlanGroup] = msgspec.field(default_factory=list)
    """List of groups in this response page."""

    total_record: int = 0
    """Total number of records matching the query."""

    filter_record: int = 0
    """Number of records after filtering."""


class CreateGroupResponse(
    msgspec.Struct, kw_only=True, omit_defaults=True, rename="camel"
):
    """
    Response from creating a group.

    Contains the GUID of the created group and user association results.
    """

    group: Union[str, None, UnsetType] = UNSET
    """GUID of the created group."""

    users: Union[dict[str, str], None, UnsetType] = UNSET
    """Map of user GUIDs to their association status."""
