# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import List, Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    GroupCreate,
    GroupGet,
    GroupGetMembers,
    GroupPurge,
    GroupRemoveUsers,
    GroupUpdate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.group import AtlanGroup, CreateGroupResponse, GroupResponse
from pyatlan.model.user import UserRequest, UserResponse


class GroupClient:
    """
    This class can be used to retrieve information about groups. This class does not need to be instantiated
    directly but can be obtained through the group property of AtlanClient.
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
        group: AtlanGroup,
        user_ids: Optional[List[str]] = None,
    ) -> CreateGroupResponse:
        """
        Create a new group.

        :param group: details of the new group
        :param user_ids: list of unique identifiers (GUIDs) of users to associate with the group
        :returns: details of the created group and user association
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint, request_obj = GroupCreate.prepare_request(group, user_ids)

        # Make API call
        raw_json = self._client._call_api(
            endpoint, request_obj=request_obj, exclude_unset=True
        )

        # Process response using shared logic
        return GroupCreate.process_response(raw_json)

    @validate_arguments
    def update(
        self,
        group: AtlanGroup,
    ) -> None:
        """
        Update a group. Note that the provided 'group' must have its id populated.

        :param group: details to update on the group
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint = GroupUpdate.prepare_request(group)

        # Make API call
        self._client._call_api(
            endpoint,
            request_obj=group,
            exclude_unset=True,
        )

    @validate_arguments
    def purge(
        self,
        guid: str,
    ) -> None:
        """
        Delete a group.

        :param guid: unique identifier (GUID) of the group to delete
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint = GroupPurge.prepare_request(guid)

        # Make API call
        self._client._call_api(endpoint)

    @validate_arguments
    def get(
        self,
        limit: Optional[int] = 20,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        columns: Optional[List[str]] = None,
    ) -> GroupResponse:
        """
        Retrieves a GroupResponse object which contains a list of the groups defined in Atlan.

        :param limit: maximum number of results to be returned
        :param post_filter: which groups to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :param columns: provides columns projection support for groups endpoint
        :returns: a GroupResponse object which contains a list of groups that match the provided criteria
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint, request = GroupGet.prepare_request(
            limit, post_filter, sort, count, offset, columns
        )

        # Make API call
        raw_json = self._client._call_api(
            api=endpoint, query_params=request.query_params
        )

        # Process response using shared logic
        response_data = GroupGet.process_response(
            raw_json, self._client, endpoint, request
        )
        return GroupResponse(**response_data)

    @validate_arguments
    def get_all(
        self,
        limit: int = 20,
        offset: int = 0,
        sort: Optional[str] = "name",
        columns: Optional[List[str]] = None,
    ) -> GroupResponse:
        """
        Retrieve a GroupResponse object containing a list of all groups defined in Atlan.

        :param limit: maximum number of results to be returned
        :param offset: starting point for the list of groups when paging
        :param sort: property by which to sort the results, by default : name
        :param columns: provides columns projection support for groups endpoint
        :returns: a GroupResponse object with all groups based on the parameters; results are iterable.
        """
        response: GroupResponse = self.get(
            offset=offset, limit=limit, sort=sort, columns=columns
        )
        return response

    @validate_arguments
    def get_by_name(
        self,
        alias: str,
        limit: int = 20,
        offset: int = 0,
    ) -> Optional[GroupResponse]:
        """
        Retrieves a GroupResponse object containing a list of groups that match the specified string.
        (This could include a complete group name, in which case there should be at most
        a single item in the returned list, or could be a partial group name to retrieve
        all groups with that naming convention.)

        :param alias: name (as it appears in the UI) on which to filter the groups
        :param limit: maximum number of groups to retrieve
        :param offset: starting point for the list of groups when paging
        :returns: a GroupResponse object containing a list of groups whose UI names include the given string; the results are iterable.
        """
        response: GroupResponse = self.get(
            offset=offset,
            limit=limit,
            post_filter='{"$and":[{"alias":{"$ilike":"%' + alias + '%"}}]}',
        )
        return response

    @validate_arguments
    def get_members(
        self, guid: str, request: Optional[UserRequest] = None
    ) -> UserResponse:
        """
        Retrieves a UserResponse object which contains a list of the members (users) of a group.

        :param guid: unique identifier (GUID) of the group from which to retrieve members
        :param request: request containing details about which members to retrieve
        :returns: a UserResponse object which contains a list of users that are members of the group
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint, user_request = GroupGetMembers.prepare_request(guid, request)

        # Make API call
        raw_json = self._client._call_api(
            api=endpoint,
            query_params=user_request.query_params,
        )

        # Process response using shared logic
        response_data = GroupGetMembers.process_response(
            raw_json, self._client, endpoint, user_request
        )
        return UserResponse(**response_data)

    @validate_arguments
    def remove_users(self, guid: str, user_ids: Optional[List[str]] = None) -> None:
        """
        Remove one or more users from a group.

        :param guid: unique identifier (GUID) of the group from which to remove users
        :param user_ids: unique identifiers (GUIDs) of the users to remove from the group
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint, request_obj = GroupRemoveUsers.prepare_request(guid, user_ids)

        # Make API call
        self._client._call_api(
            endpoint,
            request_obj=request_obj,
            exclude_unset=True,
        )
