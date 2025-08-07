# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from typing import List

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import (
    CREATE_SSO_GROUP_MAPPING,
    DELETE_SSO_GROUP_MAPPING,
    GET_ALL_SSO_GROUP_MAPPING,
    GET_SSO_GROUP_MAPPING,
    UPDATE_SSO_GROUP_MAPPING,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.group import AtlanGroup
from pyatlan.model.sso import SSOMapper, SSOMapperConfig
from pyatlan.utils import get_epoch_timestamp

GROUP_MAPPER_ATTRIBUTE = "memberOf"
GROUP_MAPPER_SYNC_MODE = "FORCE"
IDP_GROUP_MAPPER = "saml-group-idp-mapper"


class SSOCreateGroupMapping:
    """Shared logic for creating SSO group mappings."""

    @classmethod
    def prepare_request(
        cls, sso_alias: str, atlan_group: AtlanGroup, sso_group_name: str
    ) -> tuple:
        """
        Prepare the request for creating an SSO group mapping.

        :param sso_alias: name of the SSO provider
        :param atlan_group: existing Atlan group
        :param sso_group_name: name of the SSO group
        :returns: tuple of (endpoint, request_obj)
        """
        group_mapper_config = SSOMapperConfig(
            attributes="[]",
            sync_mode=GROUP_MAPPER_SYNC_MODE,
            attribute_values_regex="",
            attribute_name=GROUP_MAPPER_ATTRIBUTE,
            attribute_value=sso_group_name,
            group_name=atlan_group.name,
        )  # type: ignore[call-arg]

        group_mapper_name = cls._generate_group_mapper_name(atlan_group.id)
        group_mapper = SSOMapper(
            name=group_mapper_name,
            config=group_mapper_config,
            identity_provider_alias=sso_alias,
            identity_provider_mapper=IDP_GROUP_MAPPER,
        )  # type: ignore[call-arg]

        endpoint = CREATE_SSO_GROUP_MAPPING.format_path({"sso_alias": sso_alias})
        return endpoint, group_mapper

    @staticmethod
    def process_response(raw_json) -> SSOMapper:
        """
        Process the raw API response into an SSO mapper.

        :param raw_json: raw API response
        :returns: created SSO group mapping instance
        """
        return SSOCreateGroupMapping._parse_sso_mapper(raw_json)

    @staticmethod
    def _generate_group_mapper_name(atlan_group_id) -> str:
        return f"{atlan_group_id}--{int(get_epoch_timestamp() * 1000)}"

    @staticmethod
    def _parse_sso_mapper(raw_json):
        try:
            if isinstance(raw_json, List):
                return parse_obj_as(List[SSOMapper], raw_json)
            return parse_obj_as(SSOMapper, raw_json)
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err


class SSOUpdateGroupMapping:
    """Shared logic for updating SSO group mappings."""

    @classmethod
    def prepare_request(
        cls,
        sso_alias: str,
        atlan_group: AtlanGroup,
        group_map_id: str,
        sso_group_name: str,
    ) -> tuple:
        """
        Prepare the request for updating an SSO group mapping.

        :param sso_alias: name of the SSO provider
        :param atlan_group: existing Atlan group
        :param group_map_id: existing SSO group map identifier
        :param sso_group_name: new SSO group name
        :returns: tuple of (endpoint, request_obj)
        """
        group_mapper_config = SSOMapperConfig(
            attributes="[]",
            sync_mode=GROUP_MAPPER_SYNC_MODE,
            group_name=atlan_group.name,
            attribute_name=GROUP_MAPPER_ATTRIBUTE,
            attribute_value=sso_group_name,
        )  # type: ignore[call-arg]

        # NOTE: Updates don't require a group map name; group map ID works fine
        group_mapper = SSOMapper(
            id=group_map_id,
            config=group_mapper_config,
            identity_provider_alias=sso_alias,
            identity_provider_mapper=IDP_GROUP_MAPPER,
        )  # type: ignore[call-arg]

        endpoint = UPDATE_SSO_GROUP_MAPPING.format_path(
            {"sso_alias": sso_alias, "group_map_id": group_map_id}
        )
        return endpoint, group_mapper

    @staticmethod
    def process_response(raw_json) -> SSOMapper:
        """
        Process the raw API response into an SSO mapper.

        :param raw_json: raw API response
        :returns: updated SSO group mapping instance
        """
        return SSOUpdateGroupMapping._parse_sso_mapper(raw_json)

    @staticmethod
    def _parse_sso_mapper(raw_json):
        try:
            if isinstance(raw_json, List):
                return parse_obj_as(List[SSOMapper], raw_json)
            return parse_obj_as(SSOMapper, raw_json)
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err


class SSOGetAllGroupMappings:
    """Shared logic for getting all SSO group mappings."""

    @staticmethod
    def prepare_request(sso_alias: str) -> tuple:
        """
        Prepare the request for getting all SSO group mappings.

        :param sso_alias: name of the SSO provider
        :returns: tuple of (endpoint, request_obj)
        """
        endpoint = GET_ALL_SSO_GROUP_MAPPING.format_path({"sso_alias": sso_alias})
        return endpoint, None

    @classmethod
    def process_response(cls, raw_json) -> List[SSOMapper]:
        """
        Process the raw API response into a list of SSO mappers.

        :param raw_json: raw API response
        :returns: list of existing SSO group mapping instances
        """
        # Since `raw_json` includes both user and group mappings
        group_mappings = [
            mapping
            for mapping in raw_json
            if mapping["identityProviderMapper"] == IDP_GROUP_MAPPER
        ]
        return cls._parse_sso_mapper(group_mappings)

    @staticmethod
    def _parse_sso_mapper(raw_json):
        try:
            if isinstance(raw_json, List):
                return parse_obj_as(List[SSOMapper], raw_json)
            return parse_obj_as(SSOMapper, raw_json)
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err


class SSOGetGroupMapping:
    """Shared logic for getting a specific SSO group mapping."""

    @staticmethod
    def prepare_request(sso_alias: str, group_map_id: str) -> tuple:
        """
        Prepare the request for getting a specific SSO group mapping.

        :param sso_alias: name of the SSO provider
        :param group_map_id: existing SSO group map identifier
        :returns: tuple of (endpoint, request_obj)
        """
        endpoint = GET_SSO_GROUP_MAPPING.format_path(
            {"sso_alias": sso_alias, "group_map_id": group_map_id}
        )
        return endpoint, None

    @staticmethod
    def process_response(raw_json) -> SSOMapper:
        """
        Process the raw API response into an SSO mapper.

        :param raw_json: raw API response
        :returns: existing SSO group mapping instance
        """
        return SSOGetGroupMapping._parse_sso_mapper(raw_json)

    @staticmethod
    def _parse_sso_mapper(raw_json):
        try:
            if isinstance(raw_json, List):
                return parse_obj_as(List[SSOMapper], raw_json)
            return parse_obj_as(SSOMapper, raw_json)
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err


class SSODeleteGroupMapping:
    """Shared logic for deleting SSO group mappings."""

    @staticmethod
    def prepare_request(sso_alias: str, group_map_id: str) -> tuple:
        """
        Prepare the request for deleting an SSO group mapping.

        :param sso_alias: name of the SSO provider
        :param group_map_id: existing SSO group map identifier
        :returns: tuple of (endpoint, request_obj)
        """
        endpoint = DELETE_SSO_GROUP_MAPPING.format_path(
            {"sso_alias": sso_alias, "group_map_id": group_map_id}
        )
        return endpoint, None

    # Note: No process_response method since delete operations return None/raw response


class SSOCheckExistingMappings:
    """Shared logic for checking existing SSO group mappings."""

    @staticmethod
    def check_existing_group_mappings(
        sso_alias: str, atlan_group: AtlanGroup, existing_mappings: List[SSOMapper]
    ) -> None:
        """
        Check if an SSO group mapping already exists within Atlan.
        This is necessary to avoid duplicate group mappings with
        the same configuration due to a unique name generated on upon each creation.

        :param sso_alias: name of the SSO provider
        :param atlan_group: existing Atlan group
        :param existing_mappings: list of existing group mappings
        :raises AtlanError: on any error during API invocation
        :raises InvalidRequestException: if the provided group mapping already exists
        """
        for group_map in existing_mappings:
            if group_map.name and str(atlan_group.id) in group_map.name:
                raise ErrorCode.SSO_GROUP_MAPPING_ALREADY_EXISTS.exception_with_parameters(
                    atlan_group.alias, group_map.config.attribute_value
                )
