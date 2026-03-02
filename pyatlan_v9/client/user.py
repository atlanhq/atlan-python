# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

import json
from typing import List, Optional

import msgspec

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    ADD_USER_TO_GROUPS,
    CHANGE_USER_ROLE,
    CREATE_USERS,
    GET_CURRENT_USER,
    GET_USER_GROUPS,
    GET_USERS,
    UPDATE_USER,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan_v9.model.assets import Asset
from pyatlan_v9.model.fluent_search import FluentSearch
from pyatlan_v9.model.response import AssetMutationResponse
from pyatlan.validate import validate_arguments
from pyatlan_v9.model.group import AtlanGroup, GroupRequest, GroupResponse
from pyatlan_v9.model.user import (
    AddToGroupsRequest,
    AtlanUser,
    ChangeRoleRequest,
    CreateUser,
    CreateUserRequest,
    UserMinimalResponse,
    UserRequest,
    UserResponse,
)

_USER_COLUMNS = [
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
]


class V9UserClient:
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

    def _build_user_response(
        self,
        raw_json: dict,
        request: UserRequest,
        offset: int,
        limit: Optional[int],
    ) -> UserResponse:
        records: list[AtlanUser] = []
        if raw_records := raw_json.get("records"):
            records = msgspec.convert(raw_records, list[AtlanUser], strict=False)
        response = UserResponse(
            total_record=raw_json.get("totalRecord"),
            filter_record=raw_json.get("filterRecord"),
            records=records,
        )
        response._size = limit or 20
        response._start = offset
        response._endpoint = GET_USERS
        response._client = self._client
        response._criteria = request
        return response

    @validate_arguments
    def creator(
        self, users: List[AtlanUser], return_info: bool = False
    ) -> Optional[UserResponse]:
        """
        Create one or more new users.

        :param users: the details of the new users
        :param return_info: whether to return the details of created users, defaults to `False`
        :raises AtlanError: on any API communication issue
        :returns: a UserResponse object which contains the list of details of created users if `return_info` is `True`, otherwise `None`
        """
        to_create: list[CreateUser] = []
        for user in users:
            role_name = str(user.workspace_role)
            if (
                role_id := self._client.role_cache.get_id_for_name(role_name)
            ) and user.email:
                to_create.append(
                    CreateUser(
                        email=user.email, role_name=role_name, role_id=role_id
                    )
                )
        payload = CreateUserRequest(users=to_create)
        self._client._call_api(CREATE_USERS, request_obj=payload)
        if return_info:
            emails = [cu.email for cu in to_create]
            return self.get_by_emails(emails=emails)
        return None


    @validate_arguments
    def updater(
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
        endpoint = UPDATE_USER.format_path_with_params(guid)
        raw_json = self._client._call_api(
            endpoint, request_obj=user        )
        return msgspec.convert(raw_json, UserMinimalResponse, strict=False)


    @validate_arguments
    def change_role(
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
        payload = ChangeRoleRequest(role_id=role_id)
        endpoint = CHANGE_USER_ROLE.format_path({"user_guid": guid})
        self._client._call_api(endpoint, request_obj=payload)

    def get_current(
        self,
    ) -> UserMinimalResponse:
        """
        Retrieve the current user (representing the API token).

        :returns: basic details about the current user (API token)
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(GET_CURRENT_USER, None)
        return msgspec.convert(raw_json, UserMinimalResponse, strict=False)

    @validate_arguments
    def get(
        self,
        limit: Optional[int] = 20,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> UserResponse:
        """
        Retrieves a UserResponse which contains a list of users defined in Atlan.

        :param limit: maximum number of results to be returned
        :param post_filter: which users to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: a UserResponse which contains a list of users that match the provided criteria
        :raises AtlanError: on any API communication issue
        """
        request = UserRequest(
            post_filter=post_filter,
            limit=limit,
            sort=sort,
            count=count,
            offset=offset,
            columns=_USER_COLUMNS,
        )
        endpoint = GET_USERS.format_path_with_params()
        raw_json = self._client._call_api(
            api=endpoint, query_params=request.query_params
        )
        return self._build_user_response(raw_json, request, offset, limit)

    @validate_arguments
    def get_all(
        self,
        limit: int = 20,
        offset: int = 0,
        sort: Optional[str] = "username",
    ) -> UserResponse:
        """
        Retrieve a UserResponse object containing a list of all users defined in Atlan.

        :param limit: maximum number of users to retrieve
        :param offset: starting point for the list of users when paging
        :param sort: property by which to sort the results, by default : `username`
        :returns: a UserResponse object with all users based on the parameters; results are iterable.
        """
        response: UserResponse = self.get(offset=offset, limit=limit, sort=sort)
        return response

    @validate_arguments
    def get_by_email(
        self,
        email: str,
        limit: int = 20,
        offset: int = 0,
    ) -> Optional[UserResponse]:
        """
        Retrieves a UserResponse object containing a list of users with email addresses that contain the provided email.
        (This could include a complete email address, in which case there should be at
        most a single item in the returned list, or could be a partial email address
        such as "@example.com" to retrieve all users with that domain in their email
        address.)

        :param email: on which to filter the users
        :param limit: maximum number of users to retrieve
        :param offset: starting point for the list of users when pagin
        :returns: a UserResponse object containing a list of users whose email addresses contain the provided string
        """
        post_filter = '{"email":{"$ilike":"%' + email + '%"}}'
        return self.get(offset=offset, limit=limit, post_filter=post_filter)

    @validate_arguments
    def get_by_emails(
        self,
        emails: List[str],
        limit: int = 20,
        offset: int = 0,
    ) -> Optional[UserResponse]:
        """
        Retrieves a UserResponse object containing a list of users with email addresses that match the provided list of emails.

        :param emails: list of email addresses to filter the users
        :param limit: maximum number of users to retrieve
        :param offset: starting point for the list of users when paginating
        :returns: a UserResponse object containing a list of users whose email addresses match the provided list
        """
        email_filter = '{"email":{"$in":' + json.dumps(emails or [""]) + "}}"
        return self.get(offset=offset, limit=limit, post_filter=email_filter)

    @validate_arguments
    def get_by_username(self, username: str) -> Optional[AtlanUser]:
        """
        Retrieves a user based on the username. (This attempts an exact match on username
        rather than a contains search.)

        :param username: the username by which to find the user
        :returns: the with that username
        """
        post_filter = '{"username":"' + username + '"}'
        response = self.get(offset=0, limit=5, post_filter=post_filter)
        if response and response.records and len(response.records) >= 1:
            return response.records[0]
        return None

    @validate_arguments
    def get_by_usernames(
        self, usernames: List[str], limit: int = 5, offset: int = 0
    ) -> Optional[UserResponse]:
        """
        Retrieves a UserResponse object containing a list of users based on their usernames.

        :param usernames: the list of usernames by which to find the users
        :param limit: maximum number of users to retrieve
        :param offset: starting point for the list of users when paginating
        :returns: a UserResponse object containing list of users with the specified usernames
        """
        username_filter = '{"username":{"$in":' + json.dumps(usernames or [""]) + "}}"
        return self.get(offset=offset, limit=limit, post_filter=username_filter)

    @validate_arguments
    def add_to_groups(
        self,
        guid: str,
        group_ids: List[str],
    ) -> None:
        """
        Add a user to one or more groups.

        :param guid: unique identifier (GUID) of the user to add into groups
        :param group_ids: unique identifiers (GUIDs) of the groups to add the user into
        :raises AtlanError: on any API communication issue
        """
        payload = AddToGroupsRequest(groups=group_ids)
        endpoint = ADD_USER_TO_GROUPS.format_path({"user_guid": guid})
        self._client._call_api(endpoint, request_obj=payload)

    @validate_arguments
    def get_groups(
        self, guid: str, request: Optional[GroupRequest] = None
    ) -> GroupResponse:
        """
        Retrieve the groups this user belongs to.

        :param guid: unique identifier (GUID) of the user
        :param request: request containing details about which groups to retrieve
        :returns: a GroupResponse which contains the groups this user belongs to
        :raises AtlanError: on any API communication issue
        """
        if not request:
            request = GroupRequest()
        endpoint_obj = GET_USER_GROUPS.format_path({"user_guid": guid})
        raw_json = self._client._call_api(
            api=endpoint_obj.format_path_with_params(),
            query_params=request.query_params,
        )
        records = None
        if raw_records := raw_json.get("records"):
            records = msgspec.convert(raw_records, list[AtlanGroup], strict=False)
        response = GroupResponse(
            total_record=raw_json.get("totalRecord"),
            filter_record=raw_json.get("filterRecord"),
            records=records,
        )
        response._size = request.limit or 20
        response._start = request.offset
        response._endpoint = endpoint_obj
        response._client = self._client
        response._criteria = request
        return response

    @validate_arguments
    def add_as_admin(
        self, asset_guid: str, impersonation_token: str
    ) -> Optional[AssetMutationResponse]:
        """
        Add the API token configured for the default client as an admin to the asset with the provided GUID.
        This is primarily useful for connections, to allow the API token to manage policies for the connection, and
        for query collections, to allow the API token to manage the queries in a collection or the collection itself.

        :param asset_guid: unique identifier (GUID) of the asset to which we should add this API token as an admin
        :param impersonation_token: a bearer token for an actual user who is already an admin for the asset,
                                    NOT an API token
        :returns: a AssetMutationResponse which contains the results of the operation
        :raises NotFoundError: if the asset to which to add the API token as an admin cannot be found
        """
        return self._add_as(
            asset_guid=asset_guid,
            impersonation_token=impersonation_token,
            keyword_field=Asset.ADMIN_USERS,
        )

    @validate_arguments
    def add_as_viewer(
        self, asset_guid: str, impersonation_token: str
    ) -> Optional[AssetMutationResponse]:
        """
        Add the API token configured for the default client as a viewer to the asset with the provided GUID.
        This is primarily useful for query collections, to allow the API token to view or run queries within the
        collection, but not make any changes to them.

        :param asset_guid: unique identifier (GUID) of the asset to which we should add this API token as an admin
        :param impersonation_token: a bearer token for an actual user who is already an admin for the asset,
                                    NOT an API token
        :returns: a AssetMutationResponse which contains the results of the operation
        :raises NotFoundError: if the asset to which to add the API token as a viewer cannot be found
        """
        return self._add_as(
            asset_guid=asset_guid,
            impersonation_token=impersonation_token,
            keyword_field=Asset.VIEWER_USERS,
        )

    def _add_as(
        self, asset_guid: str, impersonation_token: str, keyword_field: KeywordField
    ) -> Optional[AssetMutationResponse]:
        """
        Add the API token configured for the default client as a viewer or admin to the asset with the provided GUID.

        :param asset_guid: unique identifier (GUID) of the asset to which we should add this API token as an admin
        :param impersonation_token: a bearer token for an actual user who is already an admin for the asset,
                                    NOT an API token
        :param keyword_field: must be either Asset.ADMIN_USERS or Asset.VIEWER_USERS
        :returns: a AssetMutationResponse which contains the results of the operation
        :raises NotFoundError: if the asset to which to add the API token as a viewer cannot be found
        """
        from pyatlan_v9.client.atlan import client_connection

        if keyword_field not in [Asset.ADMIN_USERS, Asset.VIEWER_USERS]:
            raise ValueError(
                f"keyword_field should be {Asset.VIEWER_USERS} or {Asset.ADMIN_USERS}"
            )

        token_user = self.get_current().username or ""
        with client_connection(client=self._client, api_key=impersonation_token) as tmp:  # type: ignore[arg-type]
            request = (
                FluentSearch()
                .where(Asset.GUID.eq(asset_guid))
                .include_on_results(keyword_field)
                .page_size(1)
            ).to_request()
            results = tmp.asset.search(request)
            if not results.current_page():
                raise ErrorCode.ASSET_NOT_FOUND_BY_GUID.exception_with_parameters(
                    asset_guid
                )
            asset = results.current_page()[0]
            if keyword_field == Asset.VIEWER_USERS:
                existing_viewers = asset.viewer_users or set()
                existing_viewers.add(token_user)
            else:
                existing_admins = asset.admin_users or set()
                existing_admins.add(token_user)
            to_update = asset.trim_to_required()
            if keyword_field == Asset.VIEWER_USERS:
                to_update.viewer_users = existing_viewers
            else:
                to_update.admin_users = existing_admins
            return tmp.asset.save(to_update)
