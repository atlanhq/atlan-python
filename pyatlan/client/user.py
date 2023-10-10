# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/apache/atlas (under Apache-2.0 license)
from __future__ import annotations

from typing import Any, Optional

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    CHANGE_USER_ROLE,
    CREATE_USERS,
    GET_CURRENT_USER,
    GET_USERS,
    UPDATE_USER,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.user import (
    AtlanUser,
    ChangeRoleRequest,
    CreateUserRequest,
    UserMinimalResponse,
    UserResponse,
)


class UserClient:
    """
    This class can be used to retrieve information pertaining to users. This class does not need to be instantiated
    directly but can be obtained through the user property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def create_users(
        self,
        users: list[AtlanUser],
    ) -> None:
        """
        Create one or more new users.

        :param users: the details of the new users
        :raises AtlanError: on any API communication issue
        """
        from pyatlan.cache.role_cache import RoleCache

        cur = CreateUserRequest(users=[])
        for user in users:
            role_name = str(user.workspace_role)
            if role_id := RoleCache.get_id_for_name(role_name):
                to_create = CreateUserRequest.CreateUser(
                    email=user.email,
                    role_name=role_name,
                    role_id=role_id,
                )
                cur.users.append(to_create)
        self._client._call_api(CREATE_USERS, request_obj=cur, exclude_unset=True)

    def update_user(
        self,
        guid: str,
        user: AtlanUser,
    ) -> UserMinimalResponse:
        """
        Update a user.
        Note: you can only update users that have already signed up to Atlan. Users that are
        only invited (but have not yet logged in) cannot be updated.

        :param guid: unique identifier (GUID) of the user to update
        :param user: details to update on the user
        :returns: basic details about the updated user
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(
            UPDATE_USER.format_path_with_params(guid),
            request_obj=user,
            exclude_unset=True,
        )
        return UserMinimalResponse(**raw_json)

    def change_user_role(
        self,
        guid: str,
        role_id: str,
    ) -> None:
        """
        Change the role of a user.

        :param guid: unique identifier (GUID) of the user whose role should be changed
        :param role_id: unique identifier (GUID) of the role to move the user into
        :raises AtlanError: on any API communication issue
        """
        crr = ChangeRoleRequest(role_id=role_id)
        self._client._call_api(
            CHANGE_USER_ROLE.format_path({"user_guid": guid}),
            request_obj=crr,
            exclude_unset=True,
        )

    def get_current_user(
        self,
    ) -> UserMinimalResponse:
        """
        Retrieve the current user (representing the API token).

        :returns: basic details about the current user (API token)
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(GET_CURRENT_USER)
        return UserMinimalResponse(**raw_json)

    def get_users(
        self,
        limit: Optional[int] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> UserResponse:
        """
        Retrieves a list of users defined in Atlan.

        :param limit: maximum number of results to be returned
        :param post_filter: which users to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: a list of users that match the provided criteria
        :raises AtlanError: on any API communication issue
        """
        query_params: dict[str, Any] = {
            "count": str(count),
            "offset": str(offset),
        }
        if limit is not None:
            query_params["limit"] = str(limit)
        if post_filter is not None:
            query_params["filter"] = post_filter
        if sort is not None:
            query_params["sort"] = sort
        query_params["maxLoginEvents"] = 1
        query_params["columns"] = [
            "firstName",
            "lastName",
            "username",
            "id",
            "email",
            "emailVerified",
            "enabled",
            "roles",
            "defaultRoles",
            "groupCount",
            "attributes",
            "personas",
            "createdTimestamp",
            "lastLoginTime",
            "loginEvents",
            "isLocked",
        ]
        raw_json = self._client._call_api(
            GET_USERS.format_path_with_params(), query_params
        )
        return UserResponse(**raw_json)

    def get_all_users(
        self,
        limit: int = 20,
    ) -> list[AtlanUser]:
        """
        Retrieve all users defined in Atlan.

        :returns: a list of all the users in Atlan
        """
        users: list[AtlanUser] = []
        offset = 0
        response: Optional[UserResponse] = self.get_users(
            offset=offset, limit=limit, sort="username"
        )
        while response:
            if page := response.records:
                users.extend(page)
                offset += limit
                response = self.get_users(offset=offset, limit=limit, sort="username")
            else:
                response = None
        return users

    def get_users_by_email(
        self,
        email: str,
        limit: int = 20,
    ) -> Optional[list[AtlanUser]]:
        """
        Retrieves all users with email addresses that contain the provided email.
        (This could include a complete email address, in which case there should be at
        most a single item in the returned list, or could be a partial email address
        such as "@example.com" to retrieve all users with that domain in their email
        address.)

        :param email: on which to filter the users
        :param limit: maximum number of users to retrieve
        :returns: all users whose email addresses contain the provided string
        """
        if response := self.get_users(
            offset=0,
            limit=limit,
            post_filter='{"email":{"$ilike":"%' + email + '%"}}',
        ):
            return response.records
        return None

    def get_user_by_username(self, username: str) -> Optional[AtlanUser]:
        """
        Retrieves a user based on the username. (This attempts an exact match on username
        rather than a contains search.)

        :param username: the username by which to find the user
        :returns: the user with that username
        """
        if response := self.get_users(
            offset=0,
            limit=5,
            post_filter='{"username":"' + username + '"}',
        ):
            if response.records and len(response.records) >= 1:
                return response.records[0]
        return None
