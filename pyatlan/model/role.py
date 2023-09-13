# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import List, Optional, Protocol

from pydantic import Field

from pyatlan.model.core import AtlanObject


class AtlanRole(AtlanObject):
    id: str = Field(description="Unique identifier for the role (GUID).\n")
    """Unique identifier for the role (GUID)."""
    name: str = Field(description="Unique name for the role.\n")
    description: Optional[str] = Field(None, description="Description of the role.\n")
    client_role: Optional[bool] = Field(None, description="TBC\n")
    level: Optional[str] = Field(None, description="TBC\n")
    member_count: Optional[str] = Field(
        None, description="Number of users with this role.\n"
    )
    user_count: Optional[str] = Field(None, description="TBC\n")


class RoleResponse(AtlanObject):
    total_record: Optional[int] = Field(None, description="Total number of roles.\n")
    filter_record: Optional[int] = Field(
        None,
        description="Number of roles in the filtered response.\n",
    )
    records: List["AtlanRole"] = Field(
        description="Details of each role included in the response.\n"
    )


class RoleProvider(Protocol):
    """Protocal that is implemented by classes that can provide of list of the roles defined in Atlan."""

    def get_roles(
        self,
        limit: int,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> RoleResponse:
        """
        Retrieves a list of the roles defined in Atlan.

        :param limit: maximum number of results to be returned
        :param post_filter: which roles to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: a list of roles that match the provided criteria
        :raise AtlanError: on any API communication issue
        """
