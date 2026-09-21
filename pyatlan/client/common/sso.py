# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

import base64
import binascii
from typing import List

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import (
    CREATE_SSO_GROUP_MAPPING,
    DELETE_SSO_GROUP_MAPPING,
    GET_ALL_IDPS,
    GET_ALL_SSO_GROUP_MAPPING,
    GET_SSO_GROUP_MAPPING,
    UPDATE_IDP,
    UPDATE_SSO_GROUP_MAPPING,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.group import AtlanGroup
from pyatlan.model.sso import SSOMapper, SSOMapperConfig, SSOProvider
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
        group_map_name: str,
        sso_group_name: str,
    ) -> tuple:
        """
        Prepare the request for updating an SSO group mapping.

        :param sso_alias: name of the SSO provider
        :param atlan_group: existing Atlan group
        :param group_map_id: existing SSO group map identifier
        :param group_map_name: existing SSO group map name
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

        group_mapper = SSOMapper(
            id=group_map_id,
            name=group_map_name,
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


class SSOGetAllIdentityProviders:
    """Shared logic for retrieving all SSO identity providers."""

    @staticmethod
    def prepare_request() -> tuple:
        """
        Prepare the request for retrieving all identity providers.

        :returns: tuple of (endpoint, request_obj)
        """
        return GET_ALL_IDPS, None

    @staticmethod
    def process_response(raw_json) -> List[SSOProvider]:
        """
        Process the raw API response into a list of identity providers.

        :param raw_json: raw API response
        :returns: list of the tenant's SSO identity providers
        """
        if not raw_json:
            return []
        try:
            return parse_obj_as(List[SSOProvider], raw_json)
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err


class SSOUpdateIdentityProvider:
    """Shared logic for updating an SSO identity provider."""

    @staticmethod
    def prepare_request(provider: SSOProvider) -> tuple:
        """
        Prepare the request for updating an identity provider.

        The backend treats this update as a full replacement of the
        provider's configuration, so `provider` must be the complete
        object (retrieve it first, modify it, then pass it here) -
        never a partial one, or omitted fields may be reset.

        :param provider: the complete identity provider configuration to store
        :returns: tuple of (endpoint, request_obj)
        """
        if not provider.alias:
            raise ErrorCode.MISSING_REQUIRED_QUERY_PARAM.exception_with_parameters(
                "the identity provider", "alias"
            )
        endpoint = UPDATE_IDP.format_path({"sso_alias": provider.alias})
        return endpoint, provider


def normalize_signing_certificate(certificate: str) -> str:
    """
    Convert an X.509 certificate to the form the SSO configuration stores:
    a single line of base64, with no BEGIN/END lines and no whitespace.

    Accepts PEM or already-normalized input. Exactly one certificate must
    be provided.

    :param certificate: certificate as PEM or single-line base64
    :raises InvalidRequestError: if the input contains more than one
        certificate, no certificate, or is not base64
    :returns: single-line base64 certificate value
    """
    cert_count = certificate.count("BEGIN CERTIFICATE")
    if cert_count > 1:
        raise ErrorCode.INVALID_CERTIFICATE.exception_with_parameters(
            f"found {cert_count} certificates, expected 1 (IdP metadata files "
            "often include both the old and new certificate - pass only the new one)"
        )
    lines = [
        line.strip()
        for line in certificate.strip().splitlines()
        if line.strip() and "CERTIFICATE" not in line
    ]
    normalized = "".join("".join(line.split()) for line in lines)
    if not normalized:
        raise ErrorCode.INVALID_CERTIFICATE.exception_with_parameters(
            "no certificate content between the BEGIN/END lines"
        )
    try:
        base64.b64decode(normalized, validate=True)
    except binascii.Error as err:
        raise ErrorCode.INVALID_CERTIFICATE.exception_with_parameters(
            f"not base64 ({err}) - check for truncation or non-certificate text"
        ) from err
    return normalized
