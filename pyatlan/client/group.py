# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import List, Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    CREATE_GROUP,
    DELETE_GROUP,
    GET_GROUP_MEMBERS,
    GET_GROUPS,
    REMOVE_USERS_FROM_GROUP,
    UPDATE_GROUP,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.group import (
    AtlanGroup,
    CreateGroupRequest,
    CreateGroupResponse,
    GroupRequest,
    GroupResponse,
    RemoveFromGroupRequest,
)
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
        payload = CreateGroupRequest(group=group)
        if user_ids:
            payload.users = user_ids
        raw_json = self._client._call_api(
            CREATE_GROUP, request_obj=payload, exclude_unset=True
        )
        return CreateGroupResponse(**raw_json)

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
        self._client._call_api(
            UPDATE_GROUP.format_path_with_params(group.id),
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
        self._client._call_api(DELETE_GROUP.format_path({"group_guid": guid}))

    @validate_arguments
    def get(
        self,
        limit: Optional[int] = 20,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> GroupResponse:
        """
        Retrieves a GroupResponse object which contains a list of the groups defined in Atlan.

        :param limit: maximum number of results to be returned
        :param post_filter: which groups to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: a GroupResponse object which contains a list of groups that match the provided criteria
        :raises AtlanError: on any API communication issue
        """
        request = GroupRequest(
            post_filter=post_filter, limit=limit, sort=sort, count=count, offset=offset
        )
        endpoint = GET_GROUPS.format_path_with_params()
        raw_json = self._client._call_api(
            api=endpoint, query_params=request.query_params
        )
        return GroupResponse(
            client=self._client,
            endpoint=GET_GROUPS,
            criteria=request,
            start=request.offset,
            size=request.limit,
            records=raw_json.get("records"),
            filter_record=raw_json.get("filterRecord"),
            total_record=raw_json.get("totalRecord"),
        )

    @validate_arguments
    def get_all(
        self,
        limit: int = 20,
        offset: int = 0,
        sort: Optional[str] = "name",
    ) -> List[AtlanGroup]:
        """
        Retrieve all groups defined in Atlan.

        :param limit: maximum number of results to be returned
        :param offset: starting point for the list of groups when paging
        :param sort: property by which to sort the results, by default : `name`
        :returns: a list of all the groups in Atlan
        """
        response: GroupResponse = self.get(offset=offset, limit=limit, sort=sort)
        return [group for group in response]

    @validate_arguments
    def get_by_name(
        self,
        alias: str,
        limit: int = 20,
        offset: int = 0,
    ) -> Optional[List[AtlanGroup]]:
        """
        Retrieve all groups with a name that contains the provided string.
        (This could include a complete group name, in which case there should be at most
        a single item in the returned list, or could be a partial group name to retrieve
        all groups with that naming convention.)

        :param alias: name (as it appears in the UI) on which to filter the groups
        :param limit: maximum number of groups to retrieve
        :param offset: starting point for the list of groups when paging
        :returns: all groups whose name (in the UI) contains the provided string
        """
        if response := self.get(
            offset=offset,
            limit=limit,
            post_filter='{"$and":[{"alias":{"$ilike":"%' + alias + '%"}}]}',
        ):
            return response.records
        return None

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
        if not request:
            request = UserRequest()
        endpoint = GET_GROUP_MEMBERS.format_path(
            {"group_guid": guid}
        ).format_path_with_params()
        raw_json = self._client._call_api(
            api=endpoint,
            query_params=request.query_params,
        )
        return UserResponse(
            client=self._client,
            endpoint=endpoint,
            criteria=request,
            start=request.offset,
            size=request.limit,
            records=raw_json.get("records"),
            filter_record=raw_json.get("filterRecord"),
            total_record=raw_json.get("totalRecord"),
        )

    @validate_arguments
    def remove_users(self, guid: str, user_ids: Optional[List[str]] = None) -> None:
        """
        Remove one or more users from a group.

        :param guid: unique identifier (GUID) of the group from which to remove users
        :param user_ids: unique identifiers (GUIDs) of the users to remove from the group
        :raises AtlanError: on any API communication issue
        """
        rfgr = RemoveFromGroupRequest(users=user_ids or [])
        self._client._call_api(
            REMOVE_USERS_FROM_GROUP.format_path({"group_guid": guid}),
            request_obj=rfgr,
            exclude_unset=True,
        )
