# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, List, Optional

from pydantic import Field

from pyatlan.model.core import AtlanObject


class AtlanUser(AtlanObject):
    class Attributes(AtlanObject):
        designation: Optional[List[str]] = Field(
            description="Designation for the user, such as an honorific or title."
        )
        skills: Optional[List[str]] = Field(description="Skills the user possesses.")
        slack: Optional[List[str]] = Field(
            description="Unique Slack member identifier."
        )
        jira: Optional[List[str]] = Field(description="Unique JIRA user identifier.")
        invited_at: Optional[List[str]] = Field(
            description="Time at which the user was invited (as a formatted string)."
        )
        invited_by: Optional[List[str]] = Field(
            description="User who invited this user."
        )
        invited_by_name: Optional[List[str]] = Field(description="TBC")

    class Persona(AtlanObject):
        id: Optional[str] = Field(
            description="Unique identifier (GUID) of the persona."
        )
        name: Optional[str] = Field(description="Internal name of the persona.")
        display_name: Optional[str] = Field(
            description="Human-readable name of the persona."
        )

    class LoginEvent(AtlanObject):
        client_id: Optional[str] = Field(
            description="Where the login occurred (usually `atlan-frontend`)."
        )
        details: Optional[Any] = Field(description="TBC")
        ip_address: Optional[str] = Field(
            description="IP address from which the user logged in."
        )
        realm_id: Optional[str] = Field(description="TBC")
        session_id: Optional[str] = Field(
            description="Unique identifier (GUID) of the session for the login."
        )
        time: Optional[int] = Field(
            description="Time (epoch) when the login occurred, in milliseconds."
        )
        type: Optional[str] = Field(
            description="Type of login event that occurred (usually `LOGIN`)."
        )
        user_id: Optional[str] = Field(
            description="Unique identifier (GUID) of the user that logged in."
        )

    class AuthDetails(AtlanObject):
        client_id: Optional[str] = Field(description="TBC")
        ip_address: Optional[str] = Field(description="TBC")
        realm_id: Optional[str] = Field(description="TBC")
        user_id: Optional[str] = Field(description="TBC")

    class AdminEvent(AtlanObject):
        operation_type: Optional[str] = Field(
            description="Type of admin operation that occurred."
        )
        realm_id: Optional[str] = Field(description="TBC")
        representation: Optional[str] = Field(description="TBC")
        resource_path: Optional[str] = Field(description="TBC")
        resource_type: Optional[str] = Field(
            description="Type of resource for the admin operation that occurred."
        )
        time: Optional[int] = Field(
            description="Time (epoch) when the admin operation occurred, in milliseconds."
        )
        auth_details: Optional[AtlanUser.AuthDetails] = Field(description="TBC")

    username: Optional[str] = Field(description="Username of the user within Atlan.")
    id: Optional[str] = Field(
        description="Unique identifier (GUID) of the user within Atlan."
    )
    workspace_role: Optional[str] = Field(
        description="Name of the role of the user within Atlan."
    )
    email: Optional[str] = Field(description="Email address of the user.")
    email_verified: Optional[bool] = Field(
        description="When true, the email address of the user has been verified."
    )
    enabled: Optional[bool] = Field(
        description="When true, the user is enabled. When false, the user has been deactivated."
    )
    first_name: Optional[str] = Field(description="First name of the user.")
    last_name: Optional[str] = Field(description="Last name (surname) of the user.")
    attributes: Optional[AtlanUser.Attributes] = Field(
        description="Detailed attributes of the user."
    )
    created_timestamp: Optional[int] = Field(
        description="Time (epoch) at which the user was created, in milliseconds."
    )
    last_login_time: Optional[int] = Field(
        description="Time (epoch) at which the user last logged into Atlan."
    )
    group_count: Optional[int] = Field(
        description="Number of groups to which the user belongs."
    )
    default_roles: Optional[List[str]] = Field(description="TBC")
    roles: Optional[List[str]] = Field(description="TBC")
    decentralized_roles: Optional[Any] = Field(description="TBC")
    personas: Optional[List[AtlanUser.Persona]] = Field(
        description="Personas the user is associated with."
    )
    purposes: Optional[List[Any]] = Field(
        description="Purposes the user is associated with."
    )
    admin_events: Optional[List[AtlanUser.AdminEvent]] = Field(
        description="List of administration-related events for this user."
    )
    login_events: Optional[List[AtlanUser.LoginEvent]] = Field(
        description="List of login-related events for this user."
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
    username: Optional[str] = Field(description="Username of the user within Atlan.")
    id: Optional[str] = Field(
        description="Unique identifier (GUID) of the user within Atlan."
    )
    email: Optional[str] = Field(description="Email address of the user.")
    email_verified: Optional[bool] = Field(
        description="When true, the email address of the user has been verified."
    )
    enabled: Optional[bool] = Field(
        description="When true, the user is enabled. When false, the user has been deactivated."
    )
    first_name: Optional[str] = Field(description="First name of the user.")
    last_name: Optional[str] = Field(description="Last name (surname) of the user.")
    attributes: Optional[AtlanUser.Attributes] = Field(
        description="Detailed attributes of the user."
    )
    created_timestamp: Optional[int] = Field(
        description="Time (epoch) at which the use was created, in milliseconds."
    )
    totp: Optional[bool] = Field(description="TBC")
    disableable_credential_types: Optional[Any] = Field(description="TBC")
    required_actions: Optional[Any] = Field(description="TBC")
    access: Optional[Any] = Field(description="TBC")


class UserResponse(AtlanObject):
    total_record: Optional[int] = Field(description="Total number of users.")
    filter_record: Optional[int] = Field(
        description="Number of users in the filtered response.",
    )
    records: Optional[List[AtlanUser]] = Field(
        description="Details of each user included in the response."
    )


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
