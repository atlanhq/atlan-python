# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from typing import Any, Optional

from pydantic import validate_arguments

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
from pyatlan.model.group import GroupResponse
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.user import (
    AddToGroupsRequest,
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

    @validate_arguments
    def create(
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

    @validate_arguments
    def update(
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
        crr = ChangeRoleRequest(role_id=role_id)
        self._client._call_api(
            CHANGE_USER_ROLE.format_path({"user_guid": guid}),
            request_obj=crr,
            exclude_unset=True,
        )

    def get_current(
        self,
    ) -> UserMinimalResponse:
        """
        Retrieve the current user (representing the API token).

        :returns: basic details about the current user (API token)
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(GET_CURRENT_USER)
        return UserMinimalResponse(**raw_json)

    @validate_arguments
    def get(
        self,
        limit: Optional[int] = None,
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

    @validate_arguments
    def get_all(
        self,
        limit: int = 20,
    ) -> list[AtlanUser]:
        """
        Retrieve all users defined in Atlan.

        :param limit: maximum number of users to retrieve
        :returns: a list of all the users in Atlan
        """
        users: list[AtlanUser] = []
        offset = 0
        response: Optional[UserResponse] = self.get(
            offset=offset, limit=limit, sort="username"
        )
        while response:
            if page := response.records:
                users.extend(page)
                offset += limit
                response = self.get(offset=offset, limit=limit, sort="username")
            else:
                response = None
        return users

    @validate_arguments
    def get_by_email(
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
        if response := self.get(
            offset=0,
            limit=limit,
            post_filter='{"email":{"$ilike":"%' + email + '%"}}',
        ):
            return response.records
        return None

    @validate_arguments
    def get_by_username(self, username: str) -> Optional[AtlanUser]:
        """
        Retrieves a user based on the username. (This attempts an exact match on username
        rather than a contains search.)

        :param username: the username by which to find the user
        :returns: the with that username
        """
        if response := self.get(
            offset=0,
            limit=5,
            post_filter='{"username":"' + username + '"}',
        ):
            if response.records and len(response.records) >= 1:
                return response.records[0]
        return None

    @validate_arguments
    def add_to_groups(
        self,
        guid: str,
        group_ids: list[str],
    ) -> None:
        """
        Add a user to one or more groups.

        :param guid: unique identifier (GUID) of the user to add into groups
        :param group_ids: unique identifiers (GUIDs) of the groups to add the user into
        :raises AtlanError: on any API communication issue
        """
        atgr = AddToGroupsRequest(groups=group_ids)
        self._client._call_api(
            ADD_USER_TO_GROUPS.format_path({"user_guid": guid}),
            request_obj=atgr,
            exclude_unset=True,
        )

    @validate_arguments
    def get_groups(
        self,
        guid: str,
    ) -> GroupResponse:
        """
        Retrieve the groups this user belongs to.

        :param guid: unique identifier (GUID) of the user
        :returns: a GroupResponse which contains the groups this user belongs to
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(
            GET_USER_GROUPS.format_path({"user_guid": guid})
        )
        return GroupResponse(**raw_json)

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
        from pyatlan.model.assets import Asset

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
        from pyatlan.model.assets import Asset

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
        from pyatlan.client.atlan import client_connection
        from pyatlan.model.assets.asset00 import Asset
        from pyatlan.model.fluent_search import FluentSearch

        if keyword_field not in [Asset.ADMIN_USERS, Asset.VIEWER_USERS]:
            raise ValueError(
                f"keyword_field should be {Asset.VIEWER_USERS} or {Asset.ADMIN_USERS}"
            )

        token_user = self.get_current().username or ""
        with client_connection(api_key=impersonation_token) as tmp:
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
