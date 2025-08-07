# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from json import dumps
from typing import Dict, List, Optional

from pyatlan.client.constants import (
    ADD_USER_TO_GROUPS,
    CHANGE_USER_ROLE,
    CREATE_USERS,
    GET_CURRENT_USER,
    GET_USER_GROUPS,
    GET_USERS,
    UPDATE_USER,
)
from pyatlan.model.group import GroupRequest
from pyatlan.model.user import (
    AddToGroupsRequest,
    AtlanUser,
    ChangeRoleRequest,
    CreateUserRequest,
    UserMinimalResponse,
    UserRequest,
)


class UserCreate:
    """Shared logic for creating users."""

    @staticmethod
    def prepare_request(users: List[AtlanUser], client) -> tuple:
        """
        Prepare the request for creating users.

        :param users: the details of the new users
        :param client: client instance to access role cache
        :returns: tuple of (endpoint, request_obj)
        """
        cur = CreateUserRequest(users=[])
        for user in users:
            role_name = str(user.workspace_role)
            if (role_id := client.role_cache.get_id_for_name(role_name)) and user.email:
                to_create = CreateUserRequest.CreateUser(
                    email=user.email,
                    role_name=role_name,
                    role_id=role_id,
                )
                cur.users.append(to_create)
        return CREATE_USERS, cur


class UserUpdate:
    """Shared logic for updating users."""

    @staticmethod
    def prepare_request(guid: str, user: AtlanUser) -> tuple:
        """
        Prepare the request for updating a user.

        :param guid: unique identifier (GUID) of the user to update
        :param user: details to update on the user
        :returns: tuple of (endpoint, request_obj)
        """
        endpoint = UPDATE_USER.format_path_with_params(guid)
        return endpoint, user

    @staticmethod
    def process_response(raw_json: Dict) -> UserMinimalResponse:
        """
        Process the API response into a UserMinimalResponse.

        :param raw_json: raw response from the API
        :returns: UserMinimalResponse object
        """
        return UserMinimalResponse(**raw_json)


class UserChangeRole:
    """Shared logic for changing user roles."""

    @staticmethod
    def prepare_request(guid: str, role_id: str) -> tuple:
        """
        Prepare the request for changing a user's role.

        :param guid: unique identifier (GUID) of the user whose role should be changed
        :param role_id: unique identifier (GUID) of the role to move the user into
        :returns: tuple of (endpoint, request_obj)
        """
        crr = ChangeRoleRequest(role_id=role_id)
        endpoint = CHANGE_USER_ROLE.format_path({"user_guid": guid})
        return endpoint, crr


class UserGetCurrent:
    """Shared logic for getting the current user."""

    @staticmethod
    def prepare_request() -> tuple:
        """
        Prepare the request for getting the current user.

        :returns: tuple of (endpoint, request_obj)
        """
        return GET_CURRENT_USER, None

    @staticmethod
    def process_response(raw_json: Dict) -> UserMinimalResponse:
        """
        Process the API response into a UserMinimalResponse.

        :param raw_json: raw response from the API
        :returns: UserMinimalResponse object
        """
        return UserMinimalResponse(**raw_json)


class UserGet:
    """Shared logic for getting users with various filters."""

    @staticmethod
    def prepare_request(
        limit: Optional[int] = 20,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> tuple:
        """
        Prepare the request for getting users.

        :param limit: maximum number of results to be returned
        :param post_filter: which users to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: tuple of (endpoint, query_params)
        """
        request = UserRequest(
            post_filter=post_filter,
            limit=limit,
            sort=sort,
            count=count,
            offset=offset,
            columns=[
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
                "workspaceRole",
            ],
        )
        endpoint = GET_USERS.format_path_with_params()
        return endpoint, request.query_params

    @staticmethod
    def process_response(
        raw_json: Dict, client, endpoint, request, offset, limit
    ) -> Dict:
        """
        Process the API response into UserResponse data.

        :param raw_json: raw response from the API
        :param client: client instance
        :param endpoint: API endpoint
        :param request: original request
        :param offset: starting point for results
        :param limit: maximum number of results
        :returns: dictionary with response data
        """
        return {
            "client": client,
            "endpoint": endpoint,
            "criteria": request,
            "start": offset,
            "size": limit,
            "records": raw_json["records"],
            "filter_record": raw_json["filterRecord"],
            "total_record": raw_json["totalRecord"],
        }


class UserGetByEmail:
    """Shared logic for getting users by email."""

    @staticmethod
    def prepare_request(email: str, limit: int = 20, offset: int = 0) -> tuple:
        """
        Prepare the request for getting users by email.

        :param email: on which to filter the users
        :param limit: maximum number of users to retrieve
        :param offset: starting point for the list of users when paging
        :returns: tuple of (endpoint, query_params)
        """
        post_filter = '{"email":{"$ilike":"%' + email + '%"}}'
        return UserGet.prepare_request(
            offset=offset, limit=limit, post_filter=post_filter
        )


class UserGetByEmails:
    """Shared logic for getting users by list of emails."""

    @staticmethod
    def prepare_request(emails: List[str], limit: int = 20, offset: int = 0) -> tuple:
        """
        Prepare the request for getting users by list of emails.

        :param emails: list of email addresses to filter the users
        :param limit: maximum number of users to retrieve
        :param offset: starting point for the list of users when paginating
        :returns: tuple of (endpoint, query_params)
        """
        email_filter = '{"email":{"$in":' + dumps(emails or [""]) + "}}"
        return UserGet.prepare_request(
            offset=offset, limit=limit, post_filter=email_filter
        )


class UserGetByUsername:
    """Shared logic for getting user by username."""

    @staticmethod
    def prepare_request(username: str) -> tuple:
        """
        Prepare the request for getting user by username.

        :param username: the username by which to find the user
        :returns: tuple of (endpoint, query_params)
        """
        post_filter = '{"username":"' + username + '"}'
        return UserGet.prepare_request(offset=0, limit=5, post_filter=post_filter)

    @staticmethod
    def process_response(response) -> Optional[AtlanUser]:
        """
        Process the UserResponse and extract the first user.

        :param response: UserResponse object
        :returns: the first user found, or None
        """
        if response and response.records and len(response.records) >= 1:
            return response.records[0]
        return None


class UserGetByUsernames:
    """Shared logic for getting users by list of usernames."""

    @staticmethod
    def prepare_request(usernames: List[str], limit: int = 5, offset: int = 0) -> tuple:
        """
        Prepare the request for getting users by list of usernames.

        :param usernames: the list of usernames by which to find the users
        :param limit: maximum number of users to retrieve
        :param offset: starting point for the list of users when paginating
        :returns: tuple of (endpoint, query_params)
        """
        username_filter = '{"username":{"$in":' + dumps(usernames or [""]) + "}}"
        return UserGet.prepare_request(
            offset=offset, limit=limit, post_filter=username_filter
        )


class UserAddToGroups:
    """Shared logic for adding users to groups."""

    @staticmethod
    def prepare_request(guid: str, group_ids: List[str]) -> tuple:
        """
        Prepare the request for adding a user to groups.

        :param guid: unique identifier (GUID) of the user to add into groups
        :param group_ids: unique identifiers (GUIDs) of the groups to add the user into
        :returns: tuple of (endpoint, request_obj)
        """
        atgr = AddToGroupsRequest(groups=group_ids)
        endpoint = ADD_USER_TO_GROUPS.format_path({"user_guid": guid})
        return endpoint, atgr


class UserGetGroups:
    """Shared logic for getting user groups."""

    @staticmethod
    def prepare_request(guid: str, request: Optional[GroupRequest] = None) -> tuple:
        """
        Prepare the request for getting user groups.

        :param guid: unique identifier (GUID) of the user
        :param request: request containing details about which groups to retrieve
        :returns: tuple of (endpoint, query_params)
        """
        if not request:
            request = GroupRequest()
        endpoint = GET_USER_GROUPS.format_path(
            {"user_guid": guid}
        ).format_path_with_params()
        return endpoint, request.query_params

    @staticmethod
    def process_response(raw_json: Dict, client, endpoint, request) -> Dict:
        """
        Process the API response into GroupResponse data.

        :param raw_json: raw response from the API
        :param client: client instance
        :param endpoint: API endpoint
        :param request: original request
        :returns: dictionary with response data
        """
        return {
            "client": client,
            "endpoint": endpoint,
            "criteria": request,
            "start": request.offset,
            "size": request.limit,
            "records": raw_json.get("records"),
            "filter_record": raw_json.get("filterRecord"),
            "total_record": raw_json.get("totalRecord"),
        }
