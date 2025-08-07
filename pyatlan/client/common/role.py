# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from typing import Any, Dict, Optional

from pyatlan.client.constants import GET_ROLES
from pyatlan.model.role import RoleResponse


class RoleGet:
    """Shared logic for getting roles with query parameters."""

    @staticmethod
    def prepare_request(
        limit: int,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
    ) -> tuple[str, Dict[str, str]]:
        """
        Prepare the request for getting roles with query parameters.

        :param limit: maximum number of results to be returned
        :param post_filter: which roles to retrieve
        :param sort: property by which to sort the results
        :param count: whether to return the total number of records (True) or not (False)
        :param offset: starting point for results to return, for paging
        :returns: tuple of (api_endpoint, query_params)
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

        return GET_ROLES.format_path_with_params(), query_params

    @staticmethod
    def process_response(raw_json: Any) -> RoleResponse:
        """
        Process the raw API response into a RoleResponse.

        :param raw_json: raw API response
        :returns: RoleResponse with role data
        """
        return RoleResponse(**raw_json)


class RoleGetAll:
    """Shared logic for getting all roles."""

    @staticmethod
    def prepare_request() -> str:
        """
        Prepare the request for getting all roles.

        :returns: api_endpoint
        """
        return GET_ROLES.format_path_with_params()

    @staticmethod
    def process_response(raw_json: Any) -> RoleResponse:
        """
        Process the raw API response into a RoleResponse.

        :param raw_json: raw API response
        :returns: RoleResponse with role data
        """
        return RoleResponse(**raw_json)
