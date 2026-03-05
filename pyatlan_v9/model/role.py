# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Union

import msgspec


class AtlanRole(msgspec.Struct, kw_only=True):
    """Representation of a role in Atlan."""

    id: str
    """Unique identifier for the role (GUID)."""

    name: str
    """Unique name for the role."""

    description: Union[str, None] = None
    """Description of the role."""

    client_role: Union[bool, None] = None
    """Whether this is a client-level role."""

    level: Union[str, None] = None
    """Level of the role."""

    member_count: Union[str, None] = None
    """Number of users with this role."""

    user_count: Union[str, None] = None
    """Count of users assigned to this role."""


class RoleResponse(msgspec.Struct, kw_only=True):
    """Response containing role information."""

    total_record: Union[int, None] = None
    """Total number of roles."""

    filter_record: Union[int, None] = None
    """Number of roles in the filtered response."""

    records: list[AtlanRole] = msgspec.field(default_factory=list)
    """Details of each role included in the response."""
