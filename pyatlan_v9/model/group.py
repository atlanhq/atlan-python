# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Generator, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan.utils import validate_required_fields


class GroupAttributes(msgspec.Struct, kw_only=True):
    """Detailed attributes of an Atlan group."""

    alias: Union[list[str], None] = None
    """Name of the group as it appears in the UI."""

    created_at: Union[list[str], None] = None
    """Time (epoch) at which the group was created, in milliseconds."""

    created_by: Union[list[str], None] = None
    """User who created the group."""

    updated_at: Union[list[str], None] = None
    """Time (epoch) at which the group was last updated, in milliseconds."""

    updated_by: Union[list[str], None] = None
    """User who last updated the group."""

    description: Union[list[str], None] = None
    """Description of the group."""

    is_default: Union[list[str], None] = None
    """Whether this group should be auto-assigned to all new users or not."""

    channels: Union[list[str], None] = None
    """Slack channels for this group."""


class AtlanGroup(msgspec.Struct, kw_only=True):
    """Representation of a group in Atlan."""

    alias: Union[str, None] = None
    """Name of the group as it appears in the UI."""

    attributes: Union[GroupAttributes, None] = None
    """Detailed attributes of the group."""

    roles: Union[list[str], None] = None

    decentralized_roles: Union[list[Any], None] = None

    id: Union[str, None] = None
    """Unique identifier for the group (GUID)."""

    name: Union[str, None] = None
    """Unique (internal) name for the group."""

    path: Union[str, None] = None

    personas: Union[list[Any], None] = None
    """Personas the group is associated with."""

    purposes: Union[list[Any], None] = None
    """Purposes the group is associated with."""

    user_count: Union[int, None] = None
    """Number of users in the group."""

    def is_default(self) -> bool:
        """Whether this group is auto-assigned to all new users."""
        return (
            self.attributes is not None
            and self.attributes.is_default is not None
            and self.attributes.is_default == ["true"]
        )

    @staticmethod
    def creator(alias: str) -> AtlanGroup:
        """
        Create a new group with the given alias.

        :param alias: human-readable name for the group
        :returns: a new AtlanGroup configured for creation
        """
        validate_required_fields(["alias"], [alias])
        return AtlanGroup(
            name=AtlanGroup.generate_name(alias),
            attributes=GroupAttributes(alias=[alias]),
        )

    @staticmethod
    def updater(guid: str, path: str) -> AtlanGroup:
        """
        Create a group reference for modification.

        :param guid: unique identifier of the group
        :param path: path of the group
        :returns: an AtlanGroup configured for update
        """
        validate_required_fields(["guid", "path"], [guid, path])
        return AtlanGroup(id=guid, path=path)

    @staticmethod
    def generate_name(alias: str) -> str:
        """
        Generate internal name from alias.

        :param alias: human-readable name for the group
        :returns: internal name for the group
        """
        validate_required_fields(["alias"], [alias])
        internal = alias.lower()
        return internal.replace(" ", "_")


class GroupRequest(msgspec.Struct, kw_only=True):
    """Request parameters for listing groups."""

    post_filter: Union[str, None] = None
    """Criteria by which to filter the list of groups to retrieve."""

    sort: Union[str, None] = "name"
    """Property by which to sort the resulting list of groups."""

    count: bool = True
    """Whether to include an overall count of groups (True) or not (False)."""

    offset: int = 0
    """Starting point for the list of groups when paging."""

    limit: Union[int, None] = 20
    """Maximum number of groups to return per page."""

    columns: Union[list[str], None] = None
    """List of specific fields to include in the response."""

    @property
    def query_params(self) -> dict:
        """Convert to query parameters dict."""
        qp: dict[str, object] = {}
        if self.post_filter:
            qp["filter"] = self.post_filter
        if self.sort:
            qp["sort"] = self.sort
        qp["count"] = self.count
        qp["offset"] = self.offset
        qp["limit"] = self.limit
        if self.columns:
            qp["columns"] = self.columns
        return qp


class GroupResponse(msgspec.Struct, kw_only=True):
    """Response containing group information with pagination support."""

    total_record: Union[int, None] = None
    """Total number of groups."""

    filter_record: Union[int, None] = None
    """Number of groups in the filtered response."""

    records: Union[list[AtlanGroup], None] = None
    """Details of each group included in the response."""

    # Pagination state (not from JSON — set after construction)
    _size: int = 20
    _start: int = 0
    _endpoint: Any = None
    _client: Any = None
    _criteria: Any = None

    def current_page(self) -> Union[list[AtlanGroup], None]:
        """Return the current page of group results."""
        return self.records

    def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self.records else False

    def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        self._criteria.offset = self._start
        self._criteria.limit = self._size
        raw_json = self._client._call_api(
            api=self._endpoint.format_path_with_params(),
            query_params=self._criteria.query_params,
        )
        if not raw_json.get("records"):
            self.records = []
            return False
        try:
            self.records = msgspec.convert(
                raw_json.get("records"), list[AtlanGroup], strict=False
            )
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    def __iter__(self) -> Generator[AtlanGroup, None, None]:  # type: ignore[override]
        """Iterate through all pages of results."""
        while True:
            yield from self.current_page() or []
            if not self.next_page():
                break


class CreateGroupRequest(msgspec.Struct, kw_only=True):
    """Request to create a group."""

    group: AtlanGroup
    """Group to be created."""

    users: Union[list[str], None] = None
    """List of users (their GUIDs) to be included in the group."""


class RemoveFromGroupRequest(msgspec.Struct, kw_only=True):
    """Request to remove users from a group."""

    users: Union[list[str], None] = None
    """List of users (their GUIDs) to remove from the group."""


class UserStatus(msgspec.Struct, kw_only=True):
    """Status of a user association with a group."""

    status: Union[int, None] = None
    """Response code for the association (200 is success)."""

    status_message: Union[str, None] = None
    """Status message for the association."""

    def was_successful(self) -> bool:
        """Whether the association was successful."""
        return (self.status is not None and self.status == 200) or (
            self.status_message is not None and self.status_message == "success"
        )


class CreateGroupResponse(msgspec.Struct, kw_only=True):
    """Response from creating a group."""

    group: str
    """Unique identifier (GUID) of the group that was created."""

    users: Union[dict[str, UserStatus], None] = None
    """Map of user association statuses, keyed by GUID of the user."""
