# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import List

import msgspec

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    CREATE_SSO_GROUP_MAPPING,
    DELETE_SSO_GROUP_MAPPING,
    GET_ALL_SSO_GROUP_MAPPING,
    GET_SSO_GROUP_MAPPING,
    UPDATE_SSO_GROUP_MAPPING,
)
from pyatlan.errors import ErrorCode
from pyatlan.utils import get_epoch_timestamp
from pyatlan.validate import validate_arguments
from pyatlan_v9.model.group import AtlanGroup
from pyatlan_v9.model.sso import SSOMapper, SSOMapperConfig

GROUP_MAPPER_ATTRIBUTE = "memberOf"
GROUP_MAPPER_SYNC_MODE = "FORCE"
IDP_GROUP_MAPPER = "saml-group-idp-mapper"


class V9SSOClient:
    """
    A client for operating on Atlan's single sign-on (SSO).
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @staticmethod
    def _generate_group_mapper_name(atlan_group_id) -> str:
        return f"{atlan_group_id}--{int(get_epoch_timestamp() * 1000)}"

    @staticmethod
    def _parse_sso_mapper(raw_json):
        try:
            if isinstance(raw_json, list):
                return msgspec.convert(raw_json, List[SSOMapper], strict=False)
            return msgspec.convert(raw_json, SSOMapper, strict=False)
        except msgspec.ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

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
        for group_map in existing_group_maps:
            if group_map.name and str(atlan_group.id) in group_map.name:
                raise ErrorCode.SSO_GROUP_MAPPING_ALREADY_EXISTS.exception_with_parameters(
                    atlan_group.alias, group_map.config.attribute_value
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
        :returns: created SSO group mapping instance.
        """
        self._check_existing_group_mappings(sso_alias, atlan_group)

        group_mapper_config = SSOMapperConfig(
            attributes="[]",
            sync_mode=GROUP_MAPPER_SYNC_MODE,
            attribute_values_regex="",
            attribute_name=GROUP_MAPPER_ATTRIBUTE,
            attribute_value=sso_group_name,
            group_name=atlan_group.name,
        )
        group_mapper_name = self._generate_group_mapper_name(atlan_group.id)
        group_mapper = SSOMapper(
            name=group_mapper_name,
            config=group_mapper_config,
            identity_provider_alias=sso_alias,
            identity_provider_mapper=IDP_GROUP_MAPPER,
        )

        endpoint = CREATE_SSO_GROUP_MAPPING.format_path({"sso_alias": sso_alias})
        raw_json = self._client._call_api(endpoint, request_obj=group_mapper)
        return self._parse_sso_mapper(raw_json)


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
        group_mapper_config = SSOMapperConfig(
            attributes="[]",
            sync_mode=GROUP_MAPPER_SYNC_MODE,
            group_name=atlan_group.name,
            attribute_name=GROUP_MAPPER_ATTRIBUTE,
            attribute_value=sso_group_name,
        )
        group_mapper = SSOMapper(
            id=group_map_id,
            config=group_mapper_config,
            identity_provider_alias=sso_alias,
            identity_provider_mapper=IDP_GROUP_MAPPER,
        )

        endpoint = UPDATE_SSO_GROUP_MAPPING.format_path(
            {"sso_alias": sso_alias, "group_map_id": group_map_id}
        )
        raw_json = self._client._call_api(endpoint, request_obj=group_mapper)
        return self._parse_sso_mapper(raw_json)


    @validate_arguments
    def get_all_group_mappings(self, sso_alias: str) -> List[SSOMapper]:
        """
        Retrieves all existing Atlan SSO group mappings.

        :param sso_alias: name of the SSO provider.
        :raises AtlanError: on any error during API invocation.
        :returns: list of existing SSO group mapping instances.
        """
        endpoint = GET_ALL_SSO_GROUP_MAPPING.format_path({"sso_alias": sso_alias})
        raw_json = self._client._call_api(endpoint)
        group_mappings = [
            mapping
            for mapping in raw_json
            if mapping["identityProviderMapper"] == IDP_GROUP_MAPPER
        ]
        return self._parse_sso_mapper(group_mappings)

    @validate_arguments
    def get_group_mapping(self, sso_alias: str, group_map_id: str) -> SSOMapper:
        """
        Retrieves an existing Atlan SSO group mapping.

        :param sso_alias: name of the SSO provider.
        :param group_map_id: existing SSO group map identifier.
        :raises AtlanError: on any error during API invocation.
        :returns: existing SSO group mapping instance.
        """
        endpoint = GET_SSO_GROUP_MAPPING.format_path(
            {"sso_alias": sso_alias, "group_map_id": group_map_id}
        )
        raw_json = self._client._call_api(endpoint)
        return self._parse_sso_mapper(raw_json)

    @validate_arguments
    def delete_group_mapping(self, sso_alias: str, group_map_id: str) -> None:
        """
        Deletes an existing Atlan SSO group mapping.

        :param sso_alias: name of the SSO provider.
        :param group_map_id: existing SSO group map identifier.
        :raises AtlanError: on any error during API invocation.
        :returns: an empty response (`None`).
        """
        endpoint = DELETE_SSO_GROUP_MAPPING.format_path(
            {"sso_alias": sso_alias, "group_map_id": group_map_id}
        )
        raw_json = self._client._call_api(endpoint)
        return raw_json
