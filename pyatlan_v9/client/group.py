# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import List, Optional

import msgspec

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
from pyatlan_v9.model.group import (
    AtlanGroup,
    CreateGroupRequest,
    CreateGroupResponse,
    GroupRequest,
    GroupResponse,
    RemoveFromGroupRequest,
)
from pyatlan_v9.model.user import AtlanUser, UserRequest, UserResponse
from pyatlan_v9.validate import validate_arguments


class V9GroupClient:
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
    def creator(
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
        raw_json = self._client._call_api(CREATE_GROUP, request_obj=payload)
        return msgspec.convert(raw_json, CreateGroupResponse, strict=False)

    @validate_arguments
    def updater(self, group: AtlanGroup) -> None:
        """
        Update a group. Note that the provided 'group' must have its id populated.

        :param group: details to update on the group
        :raises AtlanError: on any API communication issue
        """
        endpoint = UPDATE_GROUP.format_path_with_params(group.id)
        self._client._call_api(endpoint, request_obj=group)

    @validate_arguments
    def purge(self, guid: str) -> None:
        """
        Delete a group.

        :param guid: unique identifier (GUID) of the group to delete
        :raises AtlanError: on any API communication issue
        """
        endpoint = DELETE_GROUP.format_path({"group_guid": guid})
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
        request = GroupRequest(
            post_filter=post_filter,
            limit=limit,
            sort=sort,
            count=count,
            offset=offset,
            columns=columns,
        )
        endpoint = GET_GROUPS.format_path_with_params()
        raw_json = self._client._call_api(
            api=endpoint, query_params=request.query_params
        )
        records: list[AtlanGroup] = []
        if raw_records := raw_json.get("records"):
            records = msgspec.convert(raw_records, list[AtlanGroup], strict=False)
        response = GroupResponse(
            total_record=raw_json.get("totalRecord"),
            filter_record=raw_json.get("filterRecord"),
            records=records,
        )
        response._size = limit or 20
        response._start = offset
        response._endpoint = GET_GROUPS
        response._client = self._client
        response._criteria = request
        return response

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
        return self.get(offset=offset, limit=limit, sort=sort, columns=columns)

    @validate_arguments
    def get_by_name(
        self,
        alias: str,
        limit: int = 20,
        offset: int = 0,
    ) -> Optional[GroupResponse]:
        """
        Retrieves a GroupResponse object containing a list of groups that match the specified string.

        :param alias: name (as it appears in the UI) on which to filter the groups
        :param limit: maximum number of groups to retrieve
        :param offset: starting point for the list of groups when paging
        :returns: a GroupResponse object containing a list of groups whose UI names include the given string; the results are iterable.
        """
        return self.get(
            offset=offset,
            limit=limit,
            post_filter='{"$and":[{"alias":{"$ilike":"%' + alias + '%"}}]}',
        )

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
        endpoint_obj = GET_GROUP_MEMBERS.format_path({"group_guid": guid})
        raw_json = self._client._call_api(
            api=endpoint_obj.format_path_with_params(),
            query_params=request.query_params,
        )
        records = None
        if raw_records := raw_json.get("records"):
            records = msgspec.convert(raw_records, list[AtlanUser], strict=False)
        response = UserResponse(
            total_record=raw_json.get("totalRecord"),
            filter_record=raw_json.get("filterRecord"),
            records=records,
        )
        response._size = request.limit or 20
        response._start = request.offset or 0
        response._endpoint = endpoint_obj
        response._client = self._client
        response._criteria = request
        return response

    @validate_arguments
    def remove_users(self, guid: str, user_ids: Optional[List[str]] = None) -> None:
        """
        Remove one or more users from a group.

        :param guid: unique identifier (GUID) of the group from which to remove users
        :param user_ids: unique identifiers (GUIDs) of the users to remove from the group
        :raises AtlanError: on any API communication issue
        """
        rfgr = RemoveFromGroupRequest(users=user_ids or [])
        endpoint = REMOVE_USERS_FROM_GROUP.format_path({"group_guid": guid})
        self._client._call_api(endpoint, request_obj=rfgr)
