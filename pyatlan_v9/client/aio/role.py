from __future__ import annotations

from typing import Optional

import msgspec

from pyatlan.client.common import AsyncApiCaller, RoleGet, RoleGetAll
from pyatlan.errors import ErrorCode
from pyatlan_v9.model.role import RoleResponse
from pyatlan_v9.validate import validate_arguments


class V9AsyncRoleClient:
    """
    Async client for retrieving information about roles.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def get(
        self,
        limit: int,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> RoleResponse:
        """
        Retrieves a RoleResponse which contains a list of the roles defined in Atlan.

        :param limit: maximum number of results to be returned
        :param post_filter: which roles to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: None or a RoleResponse object which contains list of roles that match the provided criteria
        :raises AtlanError: on any API communication issue
        """
        endpoint, query_params = RoleGet.prepare_request(
            limit=limit,
            post_filter=post_filter,
            sort=sort,
            count=count,
            offset=offset,
        )
        raw_json = await self._client._call_api(endpoint, query_params)
        return msgspec.convert(raw_json, RoleResponse, strict=False)

    async def get_all(self) -> RoleResponse:
        """
        Retrieves a RoleResponse which contains a list of all the roles defined in Atlan.

        :returns:  a RoleResponse which contains a list of all the roles defined in Atlan
        :raises AtlanError: on any API communication issue
        """
        endpoint = RoleGetAll.prepare_request()
        raw_json = await self._client._call_api(endpoint)
        return msgspec.convert(raw_json, RoleResponse, strict=False)
