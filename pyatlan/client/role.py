# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Dict, Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import GET_ROLES
from pyatlan.errors import ErrorCode
from pyatlan.model.role import RoleResponse


class RoleClient:
    """
    This class can be used to retrieve information about roles. This class does not need to be instantiated
    directly but can be obtained through the role property of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def get(
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
        query_params: Dict[str, str] = {
            "count": str(count),
            "offset": str(offset),
            "limit": str(limit),
        }
        if post_filter:
            query_params["filter"] = post_filter
        if sort:
            query_params["sort"] = sort
        raw_json = self._client._call_api(
            GET_ROLES.format_path_with_params(), query_params
        )
        return RoleResponse(**raw_json)

    def get_all(self) -> RoleResponse:
        """
        Retrieves a RoleResponse which contains a list of all the roles defined in Atlan.

        :returns:  a RoleResponse which contains a list of all the roles defined in Atlan
        :raises AtlanError: on any API communication issue
        """
        raw_json = self._client._call_api(GET_ROLES.format_path_with_params())
        return RoleResponse(**raw_json)
