# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import Any, Dict, List, Optional

from pyatlan.client.constants import (
    CREATE_GROUP,
    DELETE_GROUP,
    GET_GROUP_MEMBERS,
    GET_GROUPS,
    REMOVE_USERS_FROM_GROUP,
    UPDATE_GROUP,
)
from pyatlan.model.group import (
    AtlanGroup,
    CreateGroupRequest,
    CreateGroupResponse,
    GroupRequest,
    RemoveFromGroupRequest,
)
from pyatlan.model.user import UserRequest


class GroupCreate:
    """
    Shared business logic for group creation operations.
    """

    @staticmethod
    def prepare_request(
        group: AtlanGroup, user_ids: Optional[List[str]] = None
    ) -> tuple[Any, CreateGroupRequest]:
        """
        Prepare the API request for creating a group.

        :param group: details of the new group
        :param user_ids: list of user GUIDs to associate with the group
        :returns: tuple of (endpoint, request_obj)
        """
        payload = CreateGroupRequest(group=group)
        if user_ids:
            payload.users = user_ids
        return CREATE_GROUP, payload

    @staticmethod
    def process_response(raw_json: Dict[str, Any]) -> CreateGroupResponse:
        """
        Process the response from group creation.

        :param raw_json: raw API response
        :returns: CreateGroupResponse object
        """
        return CreateGroupResponse(**raw_json)


class GroupUpdate:
    """
    Shared business logic for group update operations.
    """

    @staticmethod
    def prepare_request(group: AtlanGroup) -> Any:
        """
        Prepare the API request for updating a group.

        :param group: group details to update (must have id populated)
        :returns: formatted API endpoint
        """
        return UPDATE_GROUP.format_path_with_params(group.id)


class GroupPurge:
    """
    Shared business logic for group deletion operations.
    """

    @staticmethod
    def prepare_request(guid: str) -> Any:
        """
        Prepare the API request for deleting a group.

        :param guid: unique identifier of the group to delete
        :returns: formatted API endpoint
        """
        return DELETE_GROUP.format_path({"group_guid": guid})


class GroupGet:
    """
    Shared business logic for group retrieval operations.
    """

    @staticmethod
    def prepare_request(
        limit: Optional[int] = 20,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        columns: Optional[List[str]] = None,
    ) -> tuple[Any, GroupRequest]:
        """
        Prepare the API request for getting groups.

        :param limit: maximum number of results
        :param post_filter: filter for groups to retrieve
        :param sort: property to sort results by
        :param count: whether to return total count
        :param offset: starting point for paging
        :param columns: columns projection support
        :returns: tuple of (endpoint, request_obj)
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
        return endpoint, request

    @staticmethod
    def process_response(
        raw_json: Dict[str, Any], client, endpoint, request: GroupRequest
    ) -> Dict[str, Any]:
        """
        Process the response from group retrieval.

        :param raw_json: raw API response
        :param client: the API client for pagination
        :param endpoint: the API endpoint used
        :param request: the original request for pagination
        :returns: Dictionary with response data for GroupResponse or AsyncGroupResponse
        """
        return {
            "client": client,
            "endpoint": GET_GROUPS,
            "criteria": request,
            "start": request.offset,
            "size": request.limit,
            "records": raw_json.get("records"),
            "filter_record": raw_json.get("filterRecord"),
            "total_record": raw_json.get("totalRecord"),
        }


class GroupGetMembers:
    """
    Shared business logic for retrieving group members.
    """

    @staticmethod
    def prepare_request(
        guid: str, request: Optional[UserRequest] = None
    ) -> tuple[Any, UserRequest]:
        """
        Prepare the API request for getting group members.

        :param guid: unique identifier of the group
        :param request: request details for member retrieval
        :returns: tuple of (endpoint, request_obj)
        """
        if not request:
            request = UserRequest()
        endpoint = GET_GROUP_MEMBERS.format_path(
            {"group_guid": guid}
        ).format_path_with_params()
        return endpoint, request

    @staticmethod
    def process_response(
        raw_json: Dict[str, Any], client, endpoint, request: UserRequest
    ) -> Dict[str, Any]:
        """
        Process the response from group member retrieval.

        :param raw_json: raw API response
        :param client: the API client for pagination
        :param endpoint: the API endpoint used
        :param request: the original request for pagination
        :returns: Dictionary with response data for UserResponse or AsyncUserResponse
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


class GroupRemoveUsers:
    """
    Shared business logic for removing users from groups.
    """

    @staticmethod
    def prepare_request(
        guid: str, user_ids: Optional[List[str]] = None
    ) -> tuple[Any, RemoveFromGroupRequest]:
        """
        Prepare the API request for removing users from a group.

        :param guid: unique identifier of the group
        :param user_ids: unique identifiers of users to remove
        :returns: tuple of (endpoint, request_obj)
        """
        rfgr = RemoveFromGroupRequest(users=user_ids or [])
        endpoint = REMOVE_USERS_FROM_GROUP.format_path({"group_guid": guid})
        return endpoint, rfgr
