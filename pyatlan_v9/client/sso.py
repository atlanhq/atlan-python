# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from enum import Enum
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
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan.utils import get_epoch_timestamp
from pyatlan_v9.model.group import AtlanGroup
from pyatlan_v9.model.sso import SSOMapper, SSOMapperConfig
from pyatlan_v9.validate import validate_arguments

GROUP_MAPPER_ATTRIBUTE = "memberOf"
GROUP_MAPPER_SYNC_MODE = "FORCE"
IDP_GROUP_MAPPER = "saml-group-idp-mapper"


def _resolve_sso_alias(sso_alias) -> str:
    """Extract the string value from an SSO alias, handling enums properly."""
    if isinstance(sso_alias, Enum):
        return sso_alias.value
    return str(sso_alias)


def _group_name_for_sso(atlan_group: AtlanGroup) -> str:
    """Resolve group name for SSO payload; API list response may omit top-level name."""
    if atlan_group.name:
        return atlan_group.name
    if atlan_group.alias:
        return atlan_group.alias
    if (
        atlan_group.attributes
        and atlan_group.attributes.alias
        and len(atlan_group.attributes.alias) > 0
    ):
        return atlan_group.attributes.alias[0]
    return atlan_group.id or ""


def _generate_group_mapper_name(atlan_group_id) -> str:
    return f"{atlan_group_id}--{int(get_epoch_timestamp() * 1000)}"


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
        sso_alias_str = _resolve_sso_alias(sso_alias)
        self._check_existing_group_mappings(sso_alias_str, atlan_group)
        group_name = _group_name_for_sso(atlan_group)
        mapper = SSOMapper(
            name=_generate_group_mapper_name(atlan_group.id),
            config=SSOMapperConfig(
                attributes="[]",
                sync_mode=GROUP_MAPPER_SYNC_MODE,
                attribute_values_regex="",
                attribute_name=GROUP_MAPPER_ATTRIBUTE,
                attribute_value=sso_group_name,
                group_name=group_name,
            ),
            identity_provider_alias=sso_alias_str,
            identity_provider_mapper=IDP_GROUP_MAPPER,
        )
        endpoint = CREATE_SSO_GROUP_MAPPING.format_path({"sso_alias": sso_alias_str})
        raw_json = self._client._call_api(endpoint, request_obj=mapper)
        return self._parse_sso_mapper(raw_json)

    @validate_arguments
    def update_group_mapping(
        self,
        sso_alias: str,
        atlan_group: AtlanGroup,
        group_map_id: str,
        group_map_name: str,
        sso_group_name: str,
    ) -> SSOMapper:
        """
        Update an existing Atlan SSO group mapping.

        :param sso_alias: name of the SSO provider.
        :param atlan_group: existing Atlan group.
        :param group_map_id: existing SSO group map identifier.
        :param group_map_name: existing SSO group map name.
        :param sso_group_name: new SSO group name.
        :raises AtlanError: on any error during API invocation.
        :returns: updated SSO group mapping instance.
        """
        sso_alias_str = _resolve_sso_alias(sso_alias)
        group_name = _group_name_for_sso(atlan_group)
        mapper = SSOMapper(
            id=group_map_id,
            name=group_map_name,
            config=SSOMapperConfig(
                attributes="[]",
                sync_mode=GROUP_MAPPER_SYNC_MODE,
                group_name=group_name,
                attribute_name=GROUP_MAPPER_ATTRIBUTE,
                attribute_value=sso_group_name,
            ),
            identity_provider_alias=sso_alias_str,
            identity_provider_mapper=IDP_GROUP_MAPPER,
        )
        endpoint = UPDATE_SSO_GROUP_MAPPING.format_path(
            {"sso_alias": sso_alias_str, "group_map_id": group_map_id}
        )
        raw_json = self._client._call_api(endpoint, request_obj=mapper)
        return self._parse_sso_mapper(raw_json)

    @validate_arguments
    def get_all_group_mappings(self, sso_alias: str) -> List[SSOMapper]:
        """
        Retrieves all existing Atlan SSO group mappings.

        :param sso_alias: name of the SSO provider.
        :raises AtlanError: on any error during API invocation (other than 404).
        :returns: list of existing SSO group mapping instances. Returns [] if the
            endpoint returns 404 (e.g. SSO not configured).
        """
        endpoint = GET_ALL_SSO_GROUP_MAPPING.format_path(
            {"sso_alias": _resolve_sso_alias(sso_alias)}
        )
        try:
            raw_json = self._client._call_api(endpoint)
        except AtlanError as e:
            if "404" in str(e):
                return []
            raise
        group_mappings = [
            mapping
            for mapping in raw_json
            if mapping.get("identityProviderMapper") == IDP_GROUP_MAPPER
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
            {"sso_alias": _resolve_sso_alias(sso_alias), "group_map_id": group_map_id}
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
            {"sso_alias": _resolve_sso_alias(sso_alias), "group_map_id": group_map_id}
        )
        raw_json = self._client._call_api(endpoint)
        return raw_json
