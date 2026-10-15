# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import List

import msgspec

from pyatlan.client.common import AsyncApiCaller
from pyatlan.client.common.sso import normalize_signing_certificate
from pyatlan.client.constants import (
    CREATE_SSO_GROUP_MAPPING,
    DELETE_SSO_GROUP_MAPPING,
    GET_ALL_IDPS,
    GET_ALL_SSO_GROUP_MAPPING,
    GET_SSO_GROUP_MAPPING,
    UPDATE_IDP,
    UPDATE_SSO_GROUP_MAPPING,
)
from pyatlan.errors import AtlanError, ErrorCode
from pyatlan_v9.client.sso import (
    GROUP_MAPPER_ATTRIBUTE,
    GROUP_MAPPER_SYNC_MODE,
    IDP_GROUP_MAPPER,
    _generate_group_mapper_name,
    _group_name_for_sso,
    _resolve_sso_alias,
)
from pyatlan_v9.model.group import AtlanGroup
from pyatlan_v9.model.sso import SSOMapper, SSOMapperConfig, SSOProvider
from pyatlan_v9.validate import validate_arguments


class V9AsyncSSOClient:
    """
    Async client for operating on Atlan's single sign-on (SSO).
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
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

    async def _check_existing_group_mappings(
        self, sso_alias: str, atlan_group: AtlanGroup
    ) -> None:
        """
        Check if an SSO group mapping already exists within Atlan.

        :raises AtlanError: on any error during API invocation.
        :raises InvalidRequestException: if the provided group mapping already exists.
        """
        existing_group_maps = await self.get_all_group_mappings(sso_alias=sso_alias)
        for group_map in existing_group_maps:
            if group_map.name and str(atlan_group.id) in group_map.name:
                raise ErrorCode.SSO_GROUP_MAPPING_ALREADY_EXISTS.exception_with_parameters(
                    atlan_group.alias, group_map.config.attribute_value
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
        sso_alias_str = _resolve_sso_alias(sso_alias)
        await self._check_existing_group_mappings(sso_alias_str, atlan_group)
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
        raw_json = await self._client._call_api(endpoint, request_obj=mapper)
        return self._parse_sso_mapper(raw_json)

    @validate_arguments
    async def update_group_mapping(
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
        raw_json = await self._client._call_api(endpoint, request_obj=mapper)
        return self._parse_sso_mapper(raw_json)

    @validate_arguments
    async def get_all_group_mappings(self, sso_alias: str) -> List[SSOMapper]:
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
            raw_json = await self._client._call_api(endpoint)
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
    async def get_group_mapping(self, sso_alias: str, group_map_id: str) -> SSOMapper:
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
        raw_json = await self._client._call_api(endpoint)
        return self._parse_sso_mapper(raw_json)

    @validate_arguments
    async def delete_group_mapping(self, sso_alias: str, group_map_id: str) -> None:
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
        raw_json = await self._client._call_api(endpoint)
        return raw_json

    @staticmethod
    def _parse_sso_providers(raw_json) -> List[SSOProvider]:
        if not raw_json:
            return []
        try:
            return msgspec.convert(raw_json, List[SSOProvider], strict=False)
        except msgspec.ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    async def get_all_identity_providers(self) -> List[SSOProvider]:
        """
        Retrieves all SSO identity providers configured on the tenant.

        Requires an API token with the admin role or workspace-admin
        subrole (READ_TENANT_IDP); other tokens receive a 403.

        :raises AtlanError: on any error during API invocation.
        :returns: list of the tenant's SSO identity providers.
        """
        raw_json = await self._client._call_api(GET_ALL_IDPS)
        return self._parse_sso_providers(raw_json)

    @validate_arguments
    async def get_identity_provider(self, sso_alias: str) -> SSOProvider:
        """
        Retrieves the SSO identity provider with the given alias.

        :param sso_alias: alias of the SSO provider (e.g. `azure`, `okta`).
        :raises AtlanError: on any error during API invocation.
        :raises NotFoundError: if no identity provider exists with the given alias.
        :returns: the identity provider configuration.
        """
        for provider in await self.get_all_identity_providers():
            if provider.alias == sso_alias:
                return provider
        raise ErrorCode.IDP_NOT_FOUND_BY_ALIAS.exception_with_parameters(sso_alias)

    @validate_arguments
    async def update_identity_provider(self, provider: SSOProvider) -> SSOProvider:
        """
        Updates an SSO identity provider's configuration.

        The backend treats this as a full replacement: always retrieve the
        current configuration first (`get_identity_provider()`), modify it,
        and pass the complete object here. Sending a partial object may
        silently reset fields that were omitted.

        Requires an API token with the admin role or workspace-admin
        subrole (UPDATE_TENANT_IDP); other tokens receive a 403.

        :param provider: the complete identity provider configuration to store.
        :raises AtlanError: on any error during API invocation.
        :returns: the identity provider configuration, re-read after the update.
        """
        if not provider.alias:
            raise ErrorCode.MISSING_REQUIRED_QUERY_PARAM.exception_with_parameters(
                "the identity provider", "alias"
            )
        alias: str = provider.alias
        endpoint = UPDATE_IDP.format_path({"sso_alias": alias})
        await self._client._call_api(endpoint, request_obj=provider)
        return await self.get_identity_provider(sso_alias=alias)

    @validate_arguments
    async def update_signing_certificate(
        self, sso_alias: str, certificate: str
    ) -> SSOProvider:
        """
        Replaces the signing certificate on the given SSO identity
        provider, leaving the rest of the configuration untouched.

        API tokens authenticate independently of SSO, so this works even
        while SSO logins are failing (for example, after the certificate
        expired) - as long as the token already exists.

        :param sso_alias: alias of the SSO provider (e.g. `azure`, `okta`).
        :param certificate: new X.509 certificate, as PEM or a single line
            of base64; stored as one line with no BEGIN/END lines and no
            line breaks.
        :raises AtlanError: on any error during API invocation.
        :raises NotFoundError: if no identity provider exists with the given alias.
        :returns: the identity provider configuration, re-read after the update.
        """
        provider = await self.get_identity_provider(sso_alias=sso_alias)
        provider.config = provider.config or {}
        provider.config["signingCertificate"] = normalize_signing_certificate(
            certificate
        )
        return await self.update_identity_provider(provider=provider)
