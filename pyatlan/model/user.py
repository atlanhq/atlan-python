# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Dict, Generator, List, Optional, Protocol

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.errors import ErrorCode
from pyatlan.model.api_tokens import ApiToken
from pyatlan.model.core import AtlanObject
from pyatlan.utils import API


class AtlanUser(AtlanObject):
    class Attributes(AtlanObject):
        designation: Optional[List[str]] = Field(
            default=None,
            description="Designation for the user, such as an honorific or title.",
        )
        skills: Optional[List[str]] = Field(
            default=None, description="Skills the user possesses."
        )
        slack: Optional[List[str]] = Field(
            default=None, description="Unique Slack member identifier."
        )
        jira: Optional[List[str]] = Field(
            default=None, description="Unique JIRA user identifier."
        )
        invited_at: Optional[List[str]] = Field(
            default=None,
            description="Time at which the user was invited (as a formatted string).",
        )
        invited_by: Optional[List[str]] = Field(
            default=None, description="User who invited this user."
        )
        invited_by_name: Optional[List[str]] = Field(default=None, description="TBC")

    class Persona(AtlanObject):
        id: Optional[str] = Field(
            default=None, description="Unique identifier (GUID) of the persona."
        )
        name: Optional[str] = Field(
            default=None, description="Internal name of the persona."
        )
        display_name: Optional[str] = Field(
            default=None, description="Human-readable name of the persona."
        )

    class LoginEvent(AtlanObject):
        client_id: Optional[str] = Field(
            default=None,
            description="Where the login occurred (usually `atlan-frontend`).",
        )
        details: Optional[Any] = Field(default=None, description="TBC")
        ip_address: Optional[str] = Field(
            default=None, description="IP address from which the user logged in."
        )
        realm_id: Optional[str] = Field(default=None, description="TBC")
        session_id: Optional[str] = Field(
            default=None,
            description="Unique identifier (GUID) of the session for the login.",
        )
        time: Optional[int] = Field(
            description="Time (epoch) when the login occurred, in milliseconds."
        )
        type: Optional[str] = Field(
            default=None,
            description="Type of login event that occurred (usually `LOGIN`).",
        )
        user_id: Optional[str] = Field(
            default=None,
            description="Unique identifier (GUID) of the user that logged in.",
        )

    class AuthDetails(AtlanObject):
        client_id: Optional[str] = Field(default=None, description="TBC")
        ip_address: Optional[str] = Field(default=None, description="TBC")
        realm_id: Optional[str] = Field(default=None, description="TBC")
        user_id: Optional[str] = Field(default=None, description="TBC")

    class AdminEvent(AtlanObject):
        operation_type: Optional[str] = Field(
            default=None, description="Type of admin operation that occurred."
        )
        realm_id: Optional[str] = Field(default=None, description="TBC")
        representation: Optional[str] = Field(default=None, description="TBC")
        resource_path: Optional[str] = Field(default=None, description="TBC")
        resource_type: Optional[str] = Field(
            default=None,
            description="Type of resource for the admin operation that occurred.",
        )
        time: Optional[int] = Field(
            default=None,
            description="Time (epoch) when the admin operation occurred, in milliseconds.",
        )
        auth_details: Optional[AtlanUser.AuthDetails] = Field(
            default=None, description="TBC"
        )

    username: Optional[str] = Field(
        default=None, description="Username of the user within Atlan."
    )
    id: Optional[str] = Field(
        default=None, description="Unique identifier (GUID) of the user within Atlan."
    )
    workspace_role: Optional[str] = Field(
        default=None, description="Name of the role of the user within Atlan."
    )
    email: Optional[str] = Field(default=None, description="Email address of the user.")
    email_verified: Optional[bool] = Field(
        default=None,
        description="When true, the email address of the user has been verified.",
    )
    enabled: Optional[bool] = Field(
        default=None,
        description="When true, the user is enabled. When false, the user has been deactivated.",
    )
    first_name: Optional[str] = Field(
        default=None, description="First name of the user."
    )
    last_name: Optional[str] = Field(
        default=None, description="Last name (surname) of the user."
    )
    attributes: Optional[AtlanUser.Attributes] = Field(
        default=None, description="Detailed attributes of the user."
    )
    created_timestamp: Optional[int] = Field(
        default=None,
        description="Time (epoch) at which the user was created, in milliseconds.",
    )
    last_login_time: Optional[int] = Field(
        default=None,
        description="Time (epoch) at which the user last logged into Atlan.",
    )
    group_count: Optional[int] = Field(
        default=None, description="Number of groups to which the user belongs."
    )
    default_roles: Optional[List[str]] = Field(default=None, description="TBC")
    roles: Optional[List[str]] = Field(default=None, description="TBC")
    decentralized_roles: Optional[Any] = Field(default=None, description="TBC")
    personas: Optional[List[AtlanUser.Persona]] = Field(
        default=None, description="Personas the user is associated with."
    )
    purposes: Optional[List[Any]] = Field(
        default=None, description="Purposes the user is associated with."
    )
    admin_events: Optional[List[AtlanUser.AdminEvent]] = Field(
        default=None, description="List of administration-related events for this user."
    )
    login_events: Optional[List[AtlanUser.LoginEvent]] = Field(
        default=None, description="List of login-related events for this user."
    )

    @staticmethod
    def create(
        email: str,
        role_name: str,
    ) -> AtlanUser:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["email", "role_name"],
            [email, role_name],
        )
        return AtlanUser(email=email, workspace_role=role_name)

    @staticmethod
    def create_for_modification(
        guid: str,
    ) -> AtlanUser:
        from pyatlan.utils import validate_required_fields

        validate_required_fields(
            ["guid"],
            [guid],
        )
        return AtlanUser(id=guid)


AtlanUser.AdminEvent.update_forward_refs()


class UserMinimalResponse(AtlanObject):
    username: Optional[str] = Field(
        default=None, description="Username of the user within Atlan."
    )
    id: Optional[str] = Field(
        default=None, description="Unique identifier (GUID) of the user within Atlan."
    )
    email: Optional[str] = Field(default=None, description="Email address of the user.")
    email_verified: Optional[bool] = Field(
        default=None,
        description="When true, the email address of the user has been verified.",
    )
    enabled: Optional[bool] = Field(
        default=None,
        description="When true, the user is enabled. When false, the user has been deactivated.",
    )
    first_name: Optional[str] = Field(
        default=None, description="First name of the user."
    )
    last_name: Optional[str] = Field(
        default=None, description="Last name (surname) of the user."
    )
    attributes: Optional[AtlanUser.Attributes] = Field(
        default=None, description="Detailed attributes of the user."
    )
    created_timestamp: Optional[int] = Field(
        default=None,
        description="Time (epoch) at which the use was created, in milliseconds.",
    )
    totp: Optional[bool] = Field(default=None, description="TBC")
    disableable_credential_types: Optional[Any] = Field(default=None, description="TBC")
    required_actions: Optional[Any] = Field(default=None, description="TBC")
    access: Optional[Any] = Field(default=None, description="TBC")


class UserResponse(AtlanObject):
    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: ApiCaller = PrivateAttr()
    _criteria: UserRequest = PrivateAttr()
    total_record: Optional[int] = Field(
        default=None, description="Total number of users."
    )
    filter_record: Optional[int] = Field(
        default=None,
        description="Number of users in the filtered response.",
    )
    records: Optional[List[AtlanUser]] = Field(
        default=None, description="Details of each user included in the response."
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._endpoint = data.get("endpoint")  # type: ignore[assignment]
        self._client = data.get("client")  # type: ignore[assignment]
        self._criteria = data.get("criteria")  # type: ignore[assignment]
        self._size = data.get("size")  # type: ignore[assignment]
        self._start = data.get("start")  # type: ignore[assignment]

    def current_page(self) -> Optional[List[AtlanUser]]:
        return self.records

    def next_page(self, start=None, size=None) -> bool:
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self.records else False

    def _get_next_page(self):
        self._criteria.offset = self._start
        self._criteria.limit = self._size
        raw_json = self._client._call_api(
            api=self._endpoint,
            query_params=self._criteria.query_params,
        )
        if not raw_json.get("records"):
            self.records = []
            return False
        try:
            self.records = parse_obj_as(List[AtlanUser], raw_json.get("records"))
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    def __iter__(self) -> Generator[AtlanUser, None, None]:  # type: ignore[override]
        while True:
            yield from self.current_page() or []
            if not self.next_page():
                break


class UserRequest(AtlanObject):
    max_login_events: int = Field(
        default=1,
        description="TBC",
    )
    post_filter: Optional[str] = Field(
        default=None,
        description="Criteria by which to filter the list of users to retrieve.",
    )
    sort: Optional[str] = Field(
        default="username",
        description="Property by which to sort the resulting list of user.",
    )
    count: bool = Field(
        default=True,
        description="Whether to include an overall count of users (True) or not (False).",
    )
    offset: Optional[int] = Field(
        default=0,
        description="Starting point for the list of users when paging.",
    )
    limit: Optional[int] = Field(
        default=20,
        description="Maximum number of users to return per page.",
    )
    columns: Optional[List[str]] = Field(
        default=None,
        description="List of columns to be returned about each user in the response.",
    )

    @property
    def query_params(self) -> dict:
        qp: Dict[str, object] = {}
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


class CreateUserRequest(AtlanObject):
    class CreateUser(AtlanObject):
        email: str = Field(description="Email address of the user.")
        role_name: str = Field(description="Name of the workspace role for the user.")
        role_id: str = Field(
            description="Unique identifier (GUID) of the workspace role for the user."
        )

    users: List[CreateUserRequest.CreateUser] = Field(
        description="List of users to create."
    )


class AddToGroupsRequest(AtlanObject):
    groups: Optional[List[str]] = Field(
        description="List of groups (their GUIDs) to add the user to."
    )


class ChangeRoleRequest(AtlanObject):
    role_id: str = Field(
        description="Unique identifier (GUID) of the new workspace role for the user."
    )


class UserProvider(Protocol):
    """Protocol that is implemented by classes that can provide a list of all the users in Atlan"""

    def get_all_users(
        self,
        limit: int = 20,
    ) -> List[AtlanUser]:
        """
        Retrieve all users defined in Atlan.

        :returns: a list of all the users in Atlan
        """

    def get_api_token_by_id(self, client_id: str) -> Optional[ApiToken]:
        """
        Retrieves the API token with a name that exactly matches the provided string.

        :param display_name: name (as it appears in the UI) by which to retrieve the API token
        :returns: the API token whose name (in the UI) matches the provided string, or None if there is none
        """
