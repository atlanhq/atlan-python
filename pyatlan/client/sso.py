import logging
from typing import List

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
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

logger = logging.getLogger(__name__)


class SSOClient:
    """
    A client for operating on Atlan's single sign-on (SSO).
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    def _check_existing_group_mappings(
        self, sso_alias: str, atlan_group: AtlanGroup
    ) -> None:
        """
        Check if an SSO group mapping already exists within Atlan.
        This is necessary to avoid duplicate group mappings with
        the same configuration due to a unique name generated on upon each creation.

        :raises AtlanError: on any error during API invocation.
        :raises InvalidRequestException: if the provided group mapping already exists.
        """
        existing_group_maps = self.get_all_group_mappings(sso_alias=sso_alias)
        SSOCheckExistingMappings.check_existing_group_mappings(
            sso_alias, atlan_group, existing_group_maps
        )

    @validate_arguments
    def create_group_mapping(
        self, sso_alias: str, atlan_group: AtlanGroup, sso_group_name: str
    ) -> SSOMapper:
        """
        Creates a new Atlan SSO group mapping.

        :param sso_alias: name of the SSO provider.
        :param atlan_group: existing Atlan group.
        :param sso_group_name: name of the SSO group.
        :raises AtlanError: on any error during API invocation.
        :raises InvalidRequestError: if the group doesn't have required fields or mapping already exists.
        :returns: created SSO group mapping instance.
        """
        # Validate the group has required fields
        if not atlan_group.id:
            raise ErrorCode.SSO_MAPPING_VALIDATION_ERROR.exception_with_parameters(
                "Atlan group must have an 'id' field populated",
                sso_alias,
            )
        if not atlan_group.name:
            raise ErrorCode.SSO_MAPPING_VALIDATION_ERROR.exception_with_parameters(
                "Atlan group must have a 'name' field populated",
                sso_alias,
            )

        logger.info(
            f"Creating SSO group mapping: {atlan_group.alias} (ID: {atlan_group.id}) "
            f"<-> {sso_group_name} (SSO: {sso_alias})"
        )

        self._check_existing_group_mappings(sso_alias, atlan_group)
        endpoint, request_obj = SSOCreateGroupMapping.prepare_request(
            sso_alias, atlan_group, sso_group_name
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        result = SSOCreateGroupMapping.process_response(raw_json)

        logger.info(f"Successfully created SSO group mapping with ID: {result.id}")
        return result

    @validate_arguments
    def update_group_mapping(
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
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return SSOUpdateGroupMapping.process_response(raw_json)

    @validate_arguments
    def get_all_group_mappings(self, sso_alias: str) -> List[SSOMapper]:
        """
        Retrieves all existing Atlan SSO group mappings.

        :param sso_alias: name of the SSO provider.
        :raises AtlanError: on any error during API invocation.
        :returns: list of existing SSO group mapping instances.
        """
        endpoint, request_obj = SSOGetAllGroupMappings.prepare_request(sso_alias)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return SSOGetAllGroupMappings.process_response(raw_json)

    @validate_arguments
    def get_group_mapping(self, sso_alias: str, group_map_id: str) -> SSOMapper:
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
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return SSOGetGroupMapping.process_response(raw_json)

    @validate_arguments
    def delete_group_mapping(self, sso_alias: str, group_map_id: str) -> None:
        """
        Deletes an existing Atlan SSO group mapping.

        Note: This only deletes the SSO mapping (identity provider mapper).
        If you're experiencing issues with Okta Push Groups failing with
        stale externalId errors, you may need to run the diagnostic script
        to identify and clean up orphaned mappings.

        :param sso_alias: name of the SSO provider.
        :param group_map_id: existing SSO group map identifier.
        :raises AtlanError: on any error during API invocation.
        :returns: an empty response (`None`).
        """
        logger.info(f"Deleting SSO group mapping: {group_map_id} (SSO: {sso_alias})")

        endpoint, request_obj = SSODeleteGroupMapping.prepare_request(
            sso_alias, group_map_id
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)

        logger.info(f"Successfully deleted SSO group mapping: {group_map_id}")
        logger.debug(
            "If you're experiencing Okta Push Groups issues with stale externalId, "
            "run: python -m pyatlan.samples.sso.diagnose_orphaned_group_mappings "
            f"--mode diagnose --sso-alias {sso_alias}"
        )

        return raw_json
