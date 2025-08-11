# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import TYPE_CHECKING, List

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    AsyncApiCaller,
    SSOCheckExistingMappings,
    SSOCreateGroupMapping,
    SSODeleteGroupMapping,
    SSOGetAllGroupMappings,
    SSOGetGroupMapping,
    SSOUpdateGroupMapping,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.group import AtlanGroup
from pyatlan.model.sso import SSOMapper

if TYPE_CHECKING:
    pass


class AsyncSSOClient:
    """
    Async client for operating on Atlan's single sign-on (SSO).
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    async def _check_existing_group_mappings(
        self, sso_alias: str, atlan_group: AtlanGroup
    ) -> None:
        """
        Check if an SSO group mapping already exists within Atlan.
        This is necessary to avoid duplicate group mappings with
        the same configuration due to a unique name generated on upon each creation.

        :raises AtlanError: on any error during API invocation.
        :raises InvalidRequestException: if the provided group mapping already exists.
        """
        existing_group_maps = await self.get_all_group_mappings(sso_alias=sso_alias)
        SSOCheckExistingMappings.check_existing_group_mappings(
            sso_alias, atlan_group, existing_group_maps
        )

    @validate_arguments
    async def create_group_mapping(
        self, sso_alias: str, atlan_group: AtlanGroup, sso_group_name: str
    ) -> SSOMapper:
        """
        Creates a new Atlan SSO group mapping.

        :param sso_alias: name of the SSO provider.
        :param atlan_group: existing Atlan group.
        :param sso_group_name: name of the SSO group.
        :raises AtlanError: on any error during API invocation.
        :returns: created SSO group mapping instance.
        """
        await self._check_existing_group_mappings(sso_alias, atlan_group)
        endpoint, request_obj = SSOCreateGroupMapping.prepare_request(
            sso_alias, atlan_group, sso_group_name
        )
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return SSOCreateGroupMapping.process_response(raw_json)

    @validate_arguments
    async def update_group_mapping(
        self,
        sso_alias: str,
        atlan_group: AtlanGroup,
        group_map_id: str,
        sso_group_name: str,
    ) -> SSOMapper:
        """
        Update an existing Atlan SSO group mapping.

        :param sso_alias: name of the SSO provider.
        :param atlan_group: existing Atlan group.
        :param group_map_id: existing SSO group map identifier.
        :param sso_group_name: new SSO group name.
        :raises AtlanError: on any error during API invocation.
        :returns: updated SSO group mapping instance.
        """
        endpoint, request_obj = SSOUpdateGroupMapping.prepare_request(
            sso_alias, atlan_group, group_map_id, sso_group_name
        )
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return SSOUpdateGroupMapping.process_response(raw_json)

    @validate_arguments
    async def get_all_group_mappings(self, sso_alias: str) -> List[SSOMapper]:
        """
        Retrieves all existing Atlan SSO group mappings.

        :param sso_alias: name of the SSO provider.
        :raises AtlanError: on any error during API invocation.
        :returns: list of existing SSO group mapping instances.
        """
        endpoint, request_obj = SSOGetAllGroupMappings.prepare_request(sso_alias)
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return SSOGetAllGroupMappings.process_response(raw_json)

    @validate_arguments
    async def get_group_mapping(self, sso_alias: str, group_map_id: str) -> SSOMapper:
        """
        Retrieves an existing Atlan SSO group mapping.

        :param sso_alias: name of the SSO provider.
        :param group_map_id: existing SSO group map identifier.
        :raises AtlanError: on any error during API invocation.
        :returns: existing SSO group mapping instance.
        """
        endpoint, request_obj = SSOGetGroupMapping.prepare_request(
            sso_alias, group_map_id
        )
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return SSOGetGroupMapping.process_response(raw_json)

    @validate_arguments
    async def delete_group_mapping(self, sso_alias: str, group_map_id: str) -> None:
        """
        Deletes an existing Atlan SSO group mapping.

        :param sso_alias: name of the SSO provider.
        :param group_map_id: existing SSO group map identifier.
        :raises AtlanError: on any error during API invocation.
        :returns: an empty response (`None`).
        """
        endpoint, request_obj = SSODeleteGroupMapping.prepare_request(
            sso_alias, group_map_id
        )
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return raw_json
