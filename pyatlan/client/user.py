# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

import json
from typing import List, Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    UserAddToGroups,
    UserChangeRole,
    UserCreate,
    UserGet,
    UserGetByEmail,
    UserGetByEmails,
    UserGetByUsername,
    UserGetByUsernames,
    UserGetCurrent,
    UserGetGroups,
    UserUpdate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.assets import Asset
from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan.model.fluent_search import FluentSearch
from pyatlan.model.group import GroupRequest, GroupResponse
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.user import AtlanUser, UserMinimalResponse, UserRequest, UserResponse


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
        self, users: List[AtlanUser], return_info: bool = False
    ) -> Optional[UserResponse]:
        """
        Create one or more new users.

        :param users: the details of the new users
        :param return_info: whether to return the details of created users, defaults to `False`
        :raises AtlanError: on any API communication issue
        :returns: a UserResponse object which contains the list of details of created users if `return_info` is `True`, otherwise `None`
        """
        endpoint, request_obj = UserCreate.prepare_request(users, self._client)
        self._client._call_api(endpoint, request_obj=request_obj, exclude_unset=True)
        if return_info:
            users_emails = [user.email for user in request_obj.users]
            return self.get_by_emails(emails=users_emails)
        return None

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
        endpoint, request_obj = UserUpdate.prepare_request(guid, user)
        raw_json = self._client._call_api(
            endpoint, request_obj=request_obj, exclude_unset=True
        )
        return UserUpdate.process_response(raw_json)

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
        endpoint, request_obj = UserChangeRole.prepare_request(guid, role_id)
        self._client._call_api(endpoint, request_obj=request_obj, exclude_unset=True)

    def get_current(
        self,
    ) -> UserMinimalResponse:
        """
        Retrieve the current user (representing the API token).

        :returns: basic details about the current user (API token)
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = UserGetCurrent.prepare_request()
        raw_json = self._client._call_api(endpoint, request_obj)
        return UserGetCurrent.process_response(raw_json)

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
        endpoint, query_params = UserGet.prepare_request(
            limit, post_filter, sort, count, offset
        )
        raw_json = self._client._call_api(api=endpoint, query_params=query_params)

        # Build the request object for response processing

        request = UserRequest(
            post_filter=post_filter,
            limit=limit,
            sort=sort,
            count=count,
            offset=offset,
        )

        response_data = UserGet.process_response(
            raw_json, self._client, endpoint, request, offset, limit
        )
        return UserResponse(**response_data)

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
        endpoint, query_params = UserGetByEmail.prepare_request(email, limit, offset)
        raw_json = self._client._call_api(api=endpoint, query_params=query_params)

        # Build the request object for response processing

        request = UserRequest(
            post_filter='{"email":{"$ilike":"%' + email + '%"}}',
            limit=limit,
            offset=offset,
        )

        response_data = UserGet.process_response(
            raw_json, self._client, endpoint, request, offset, limit
        )
        return UserResponse(**response_data)

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
        endpoint, query_params = UserGetByEmails.prepare_request(emails, limit, offset)
        raw_json = self._client._call_api(api=endpoint, query_params=query_params)

        # Build the request object for response processing

        email_filter = '{"email":{"$in":' + json.dumps(emails or [""]) + "}}"
        request = UserRequest(
            post_filter=email_filter,
            limit=limit,
            offset=offset,
        )

        response_data = UserGet.process_response(
            raw_json, self._client, endpoint, request, offset, limit
        )
        return UserResponse(**response_data)

    @validate_arguments
    def get_by_username(self, username: str) -> Optional[AtlanUser]:
        """
        Retrieves a user based on the username. (This attempts an exact match on username
        rather than a contains search.)

        :param username: the username by which to find the user
        :returns: the with that username
        """
        endpoint, query_params = UserGetByUsername.prepare_request(username)
        raw_json = self._client._call_api(api=endpoint, query_params=query_params)

        # Build the request object for response processing

        request = UserRequest(
            post_filter='{"username":"' + username + '"}',
            limit=5,
            offset=0,
        )

        response_data = UserGet.process_response(
            raw_json, self._client, endpoint, request, 0, 5
        )
        response = UserResponse(**response_data)
        return UserGetByUsername.process_response(response)

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
        endpoint, query_params = UserGetByUsernames.prepare_request(
            usernames, limit, offset
        )
        raw_json = self._client._call_api(api=endpoint, query_params=query_params)

        # Build the request object for response processing

        username_filter = '{"username":{"$in":' + json.dumps(usernames or [""]) + "}}"
        request = UserRequest(
            post_filter=username_filter,
            limit=limit,
            offset=offset,
        )

        response_data = UserGet.process_response(
            raw_json, self._client, endpoint, request, offset, limit
        )
        return UserResponse(**response_data)

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
        endpoint, request_obj = UserAddToGroups.prepare_request(guid, group_ids)
        self._client._call_api(endpoint, request_obj=request_obj, exclude_unset=True)

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
        endpoint, query_params = UserGetGroups.prepare_request(guid, request)
        raw_json = self._client._call_api(api=endpoint, query_params=query_params)

        if not request:
            request = GroupRequest()
        response_data = UserGetGroups.process_response(
            raw_json, self._client, endpoint, request
        )
        return GroupResponse(**response_data)

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
        from pyatlan.client.atlan import client_connection

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
