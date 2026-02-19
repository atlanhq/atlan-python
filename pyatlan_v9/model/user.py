# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Generator, Protocol, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan.model.api_tokens import ApiToken
from pyatlan.utils import validate_required_fields


class UserAttributes(msgspec.Struct, kw_only=True):
    """Detailed attributes of an Atlan user."""

    designation: Union[list[str], None] = None
    """Designation for the user, such as an honorific or title."""
    skills: Union[list[str], None] = None
    """Skills the user possesses."""
    slack: Union[list[str], None] = None
    """Unique Slack member identifier."""
    jira: Union[list[str], None] = None
    """Unique JIRA user identifier."""
    invited_at: Union[list[str], None] = None
    """Time at which the user was invited (as a formatted string)."""
    invited_by: Union[list[str], None] = None
    """User who invited this user."""
    invited_by_name: Union[list[str], None] = None


class UserPersona(msgspec.Struct, kw_only=True):
    """Persona associated with a user."""

    id: Union[str, None] = None
    """Unique identifier (GUID) of the persona."""
    name: Union[str, None] = None
    """Internal name of the persona."""
    display_name: Union[str, None] = None
    """Human-readable name of the persona."""


class UserLoginEvent(msgspec.Struct, kw_only=True):
    """Login event for a user."""

    client_id: Union[str, None] = None
    """Where the login occurred (usually 'atlan-frontend')."""
    details: Union[Any, None] = None
    ip_address: Union[str, None] = None
    """IP address from which the user logged in."""
    realm_id: Union[str, None] = None
    session_id: Union[str, None] = None
    """Unique identifier (GUID) of the session for the login."""
    time: Union[int, None] = None
    """Time (epoch) when the login occurred, in milliseconds."""
    type: Union[str, None] = None
    """Type of login event that occurred (usually 'LOGIN')."""
    user_id: Union[str, None] = None
    """Unique identifier (GUID) of the user that logged in."""


class UserAuthDetails(msgspec.Struct, kw_only=True):
    """Authentication details for a user."""

    client_id: Union[str, None] = None
    ip_address: Union[str, None] = None
    realm_id: Union[str, None] = None
    user_id: Union[str, None] = None


class UserAdminEvent(msgspec.Struct, kw_only=True):
    """Admin event for a user."""

    operation_type: Union[str, None] = None
    """Type of admin operation that occurred."""
    realm_id: Union[str, None] = None
    representation: Union[str, None] = None
    resource_path: Union[str, None] = None
    resource_type: Union[str, None] = None
    """Type of resource for the admin operation that occurred."""
    time: Union[int, None] = None
    """Time (epoch) when the admin operation occurred, in milliseconds."""
    auth_details: Union[UserAuthDetails, None] = None


class AtlanUser(msgspec.Struct, kw_only=True):
    """Representation of a user in Atlan."""

    username: Union[str, None] = None
    """Username of the user within Atlan."""
    id: Union[str, None] = None
    """Unique identifier (GUID) of the user within Atlan."""
    workspace_role: Union[str, None] = None
    """Name of the role of the user within Atlan."""
    email: Union[str, None] = None
    """Email address of the user."""
    email_verified: Union[bool, None] = None
    """When true, the email address of the user has been verified."""
    enabled: Union[bool, None] = None
    """When true, the user is enabled."""
    first_name: Union[str, None] = None
    """First name of the user."""
    last_name: Union[str, None] = None
    """Last name (surname) of the user."""
    attributes: Union[UserAttributes, None] = None
    """Detailed attributes of the user."""
    created_timestamp: Union[int, None] = None
    """Time (epoch) at which the user was created, in milliseconds."""
    last_login_time: Union[int, None] = None
    """Time (epoch) at which the user last logged into Atlan."""
    group_count: Union[int, None] = None
    """Number of groups to which the user belongs."""
    default_roles: Union[list[str], None] = None
    roles: Union[list[str], None] = None
    decentralized_roles: Union[Any, None] = None
    personas: Union[list[UserPersona], None] = None
    """Personas the user is associated with."""
    purposes: Union[list[Any], None] = None
    """Purposes the user is associated with."""
    admin_events: Union[list[UserAdminEvent], None] = None
    """List of administration-related events for this user."""
    login_events: Union[list[UserLoginEvent], None] = None
    """List of login-related events for this user."""

    @staticmethod
    def creator(email: str, role_name: str) -> AtlanUser:
        """
        Create a new user with the given email and role.

        :param email: email address of the user
        :param role_name: name of the workspace role for the user
        :returns: an AtlanUser configured for creation
        """
        validate_required_fields(["email", "role_name"], [email, role_name])
        return AtlanUser(email=email, workspace_role=role_name)

    @staticmethod
    def updater(guid: str) -> AtlanUser:
        """
        Create a user reference for modification.

        :param guid: unique identifier of the user
        :returns: an AtlanUser configured for update
        """
        validate_required_fields(["guid"], [guid])
        return AtlanUser(id=guid)


class UserMinimalResponse(msgspec.Struct, kw_only=True):
    """Minimal user response with basic fields."""

    username: Union[str, None] = None
    """Username of the user within Atlan."""
    id: Union[str, None] = None
    """Unique identifier (GUID) of the user within Atlan."""
    email: Union[str, None] = None
    """Email address of the user."""
    email_verified: Union[bool, None] = None
    enabled: Union[bool, None] = None
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None
    attributes: Union[UserAttributes, None] = None
    created_timestamp: Union[int, None] = None
    totp: Union[bool, None] = None
    disableable_credential_types: Union[Any, None] = None
    required_actions: Union[Any, None] = None
    access: Union[Any, None] = None


class UserRequest(msgspec.Struct, kw_only=True):
    """Request parameters for listing users."""

    max_login_events: int = 1
    post_filter: Union[str, None] = None
    """Criteria by which to filter the list of users to retrieve."""
    sort: Union[str, None] = "username"
    """Property by which to sort the resulting list of users."""
    count: bool = True
    """Whether to include an overall count of users."""
    offset: Union[int, None] = 0
    """Starting point for the list of users when paging."""
    limit: Union[int, None] = 20
    """Maximum number of users to return per page."""
    columns: Union[list[str], None] = None
    """List of columns to be returned about each user in the response."""

    @property
    def query_params(self) -> dict:
        """Convert to query parameters dict."""
        qp: dict[str, object] = {}
        if self.post_filter:
            qp["filter"] = self.post_filter
        if self.sort:
            qp["sort"] = self.sort
        if self.columns:
            qp["columns"] = self.columns
        qp["count"] = self.count
        qp["offset"] = self.offset
        qp["limit"] = self.limit
        qp["maxLoginEvents"] = self.max_login_events
        return qp


class UserResponse(msgspec.Struct, kw_only=True):
    """Response containing user information with pagination support."""

    total_record: Union[int, None] = None
    """Total number of users."""
    filter_record: Union[int, None] = None
    """Number of users in the filtered response."""
    records: Union[list[AtlanUser], None] = None
    """Details of each user included in the response."""

    # Pagination state (not from JSON — set after construction)
    _size: int = 20
    _start: int = 0
    _endpoint: Any = None
    _client: Any = None
    _criteria: Any = None

    def current_page(self) -> Union[list[AtlanUser], None]:
        """Return the current page of user results."""
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
                raw_json.get("records"), list[AtlanUser], strict=False
            )
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    def __iter__(self) -> Generator[AtlanUser, None, None]:  # type: ignore[override]
        """Iterate through all pages of results."""
        while True:
            yield from self.current_page() or []
            if not self.next_page():
                break


class CreateUser(msgspec.Struct, kw_only=True):
    """Specification for a user to create."""

    email: str
    """Email address of the user."""
    role_name: str
    """Name of the workspace role for the user."""
    role_id: str
    """Unique identifier (GUID) of the workspace role for the user."""


class CreateUserRequest(msgspec.Struct, kw_only=True):
    """Request to create users."""

    users: list[CreateUser]
    """List of users to create."""


class AddToGroupsRequest(msgspec.Struct, kw_only=True):
    """Request to add a user to groups."""

    groups: Union[list[str], None] = None
    """List of groups (their GUIDs) to add the user to."""


class ChangeRoleRequest(msgspec.Struct, kw_only=True):
    """Request to change a user's workspace role."""

    role_id: str
    """Unique identifier (GUID) of the new workspace role for the user."""


class UserProvider(Protocol):
    """Protocol that is implemented by classes that can provide a list of all the users in Atlan."""

    def get_all_users(self, limit: int = 20) -> list[AtlanUser]:
        """Retrieve all users defined in Atlan."""
        ...

    def get_api_token_by_id(self, client_id: str) -> Union[ApiToken, None]:
        """Retrieve an API token by its client ID."""
        ...
