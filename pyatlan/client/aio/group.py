# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from __future__ import annotations

from typing import List, Optional

from pydantic.v1 import parse_obj_as, validate_arguments

from pyatlan.client.common import (
    AsyncApiCaller,
    GroupCreate,
    GroupGet,
    GroupGetMembers,
    GroupPurge,
    GroupRemoveUsers,
    GroupUpdate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.aio.group import AsyncGroupResponse
from pyatlan.model.aio.user import AsyncUserResponse
from pyatlan.model.group import AtlanGroup, CreateGroupResponse
from pyatlan.model.user import UserRequest


class AsyncGroupClient:
    """
    Async version of GroupClient for retrieving information about groups.
    This class does not need to be instantiated directly but can be obtained through the group property of AsyncAtlanClient.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def create(
        self,
        group: AtlanGroup,
        user_ids: Optional[List[str]] = None,
    ) -> CreateGroupResponse:
        """
        Create a new group (async version).

        :param group: details of the new group
        :param user_ids: list of unique identifiers (GUIDs) of users to associate with the group
        :returns: details of the created group and user association
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint, request_obj = GroupCreate.prepare_request(group, user_ids)

        # Make async API call
        raw_json = await self._client._call_api(
            endpoint, request_obj=request_obj, exclude_unset=True
        )

        # Process response using shared logic
        return GroupCreate.process_response(raw_json)

    @validate_arguments
    async def update(
        self,
        group: AtlanGroup,
    ) -> None:
        """
        Update a group (async version). Note that the provided 'group' must have its id populated.

        :param group: details to update on the group
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint = GroupUpdate.prepare_request(group)

        # Make async API call
        await self._client._call_api(
            endpoint,
            request_obj=group,
            exclude_unset=True,
        )

    @validate_arguments
    async def purge(
        self,
        guid: str,
    ) -> None:
        """
        Delete a group (async version).

        :param guid: unique identifier (GUID) of the group to delete
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint = GroupPurge.prepare_request(guid)

        # Make async API call
        await self._client._call_api(endpoint)

    @validate_arguments
    async def get(
        self,
        limit: Optional[int] = 20,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        columns: Optional[List[str]] = None,
    ) -> AsyncGroupResponse:
        """
        Retrieves a GroupResponse object which contains a list of the groups defined in Atlan (async version).

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

        # Make async API call
        raw_json = await self._client._call_api(
            api=endpoint, query_params=request.query_params
        )

        # Process response using shared logic
        response_data = GroupGet.process_response(
            raw_json, self._client, endpoint, request
        )

        # Parse records into AtlanGroup objects if they exist
        if response_data.get("records"):
            response_data["records"] = parse_obj_as(
                List[AtlanGroup], response_data["records"]
            )

        return AsyncGroupResponse(**response_data)

    @validate_arguments
    async def get_all(
        self,
        limit: int = 20,
        offset: int = 0,
        sort: Optional[str] = "name",
        columns: Optional[List[str]] = None,
    ) -> AsyncGroupResponse:
        """
        Retrieve a GroupResponse object containing a list of all groups defined in Atlan (async version).

        :param limit: maximum number of results to be returned
        :param offset: starting point for the list of groups when paging
        :param sort: property by which to sort the results, by default : name
        :param columns: provides columns projection support for groups endpoint
        :returns: a GroupResponse object with all groups based on the parameters; results are iterable.
        """
        response: AsyncGroupResponse = await self.get(
            offset=offset, limit=limit, sort=sort, columns=columns
        )
        return response

    @validate_arguments
    async def get_by_name(
        self,
        alias: str,
        limit: int = 20,
        offset: int = 0,
    ) -> Optional[AsyncGroupResponse]:
        """
        Retrieves a GroupResponse object containing a list of groups that match the specified string (async version).
        (This could include a complete group name, in which case there should be at most
        a single item in the returned list, or could be a partial group name to retrieve
        all groups with that naming convention.)

        :param alias: name (as it appears in the UI) on which to filter the groups
        :param limit: maximum number of groups to retrieve
        :param offset: starting point for the list of groups when paging
        :returns: a GroupResponse object containing a list of groups whose UI names include the given string; the results are iterable.
        """
        response: AsyncGroupResponse = await self.get(
            offset=offset,
            limit=limit,
            post_filter='{"$and":[{"alias":{"$ilike":"%' + alias + '%"}}]}',
        )
        return response

    @validate_arguments
    async def get_members(
        self, guid: str, request: Optional[UserRequest] = None
    ) -> AsyncUserResponse:
        """
        Retrieves a UserResponse object which contains a list of the members (users) of a group (async version).

        :param guid: unique identifier (GUID) of the group from which to retrieve members
        :param request: request containing details about which members to retrieve
        :returns: a UserResponse object which contains a list of users that are members of the group
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint, user_request = GroupGetMembers.prepare_request(guid, request)

        # Make async API call
        raw_json = await self._client._call_api(
            api=endpoint,
            query_params=user_request.query_params,
        )

        # Process response using shared logic
        response_data = GroupGetMembers.process_response(
            raw_json, self._client, endpoint, user_request
        )
        return AsyncUserResponse(**response_data)

    @validate_arguments
    async def remove_users(
        self, guid: str, user_ids: Optional[List[str]] = None
    ) -> None:
        """
        Remove one or more users from a group (async version).

        :param guid: unique identifier (GUID) of the group from which to remove users
        :param user_ids: unique identifiers (GUIDs) of the users to remove from the group
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint, request_obj = GroupRemoveUsers.prepare_request(guid, user_ids)

        # Make async API call
        await self._client._call_api(
            endpoint,
            request_obj=request_obj,
            exclude_unset=True,
        )
