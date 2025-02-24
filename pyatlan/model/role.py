# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import List, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject


class AtlanRole(AtlanObject):
    id: str = Field(description="Unique identifier for the role (GUID).\n")
    """Unique identifier for the role (GUID)."""
    name: str = Field(description="Unique name for the role.\n")
    description: Optional[str] = Field(
        default=None, description="Description of the role.\n"
    )
    client_role: Optional[bool] = Field(default=None, description="TBC\n")
    level: Optional[str] = Field(default=None, description="TBC\n")
    member_count: Optional[str] = Field(
        default=None, description="Number of users with this role.\n"
    )
    user_count: Optional[str] = Field(default=None, description="TBC\n")


class RoleResponse(AtlanObject):
    total_record: Optional[int] = Field(
        default=None, description="Total number of roles.\n"
    )
    filter_record: Optional[int] = Field(
        None,
        description="Number of roles in the filtered response.\n",
    )
    records: List["AtlanRole"] = Field(
        description="Details of each role included in the response.\n"
    )
