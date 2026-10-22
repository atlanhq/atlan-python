from typing import List, cast

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    SSOCheckExistingMappings,
    SSOCreateGroupMapping,
    SSODeleteGroupMapping,
    SSOGetAllGroupMappings,
    SSOGetAllIdentityProviders,
    SSOGetGroupMapping,
    SSOUpdateGroupMapping,
    SSOUpdateIdentityProvider,
    normalize_signing_certificate,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.group import AtlanGroup
from pyatlan.model.sso import SSOMapper, SSOProvider


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
        :returns: created SSO group mapping instance.
        """
        self._check_existing_group_mappings(sso_alias, atlan_group)
        endpoint, request_obj = SSOCreateGroupMapping.prepare_request(
            sso_alias, atlan_group, sso_group_name
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return SSOCreateGroupMapping.process_response(raw_json)

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
        endpoint, request_obj = SSOUpdateGroupMapping.prepare_request(
            sso_alias, atlan_group, group_map_id, group_map_name, sso_group_name
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

        :param sso_alias: name of the SSO provider.
        :param group_map_id: existing SSO group map identifier.
        :raises AtlanError: on any error during API invocation.
        :returns: an empty response (`None`).
        """
        endpoint, request_obj = SSODeleteGroupMapping.prepare_request(
            sso_alias, group_map_id
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return raw_json

    def get_all_identity_providers(self) -> List[SSOProvider]:
        """
        Retrieves all SSO identity providers configured on the tenant.

        Requires an API token with the admin role or workspace-admin
        subrole (READ_TENANT_IDP); other tokens receive a 403.

        :raises AtlanError: on any error during API invocation.
        :returns: list of the tenant's SSO identity providers
        """
        endpoint, request_obj = SSOGetAllIdentityProviders.prepare_request()
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return SSOGetAllIdentityProviders.process_response(raw_json)

    @validate_arguments
    def get_identity_provider(self, sso_alias: str) -> SSOProvider:
        """
        Retrieves the SSO identity provider with the given alias.

        :param sso_alias: alias of the SSO provider (e.g. `azure`, `okta`)
        :raises AtlanError: on any error during API invocation.
        :raises NotFoundError: if no identity provider exists with the given alias.
        :returns: the identity provider configuration
        """
        for provider in self.get_all_identity_providers():
            if provider.alias == sso_alias:
                return provider
        raise ErrorCode.IDP_NOT_FOUND_BY_ALIAS.exception_with_parameters(sso_alias)

    @validate_arguments
    def update_identity_provider(self, provider: SSOProvider) -> SSOProvider:
        """
        Updates an SSO identity provider's configuration.

        The backend treats this as a full replacement: always retrieve the
        current configuration first (`get_identity_provider()`), modify it,
        and pass the complete object here. Sending a partial object may
        silently reset fields that were omitted.

        Requires an API token with the admin role or workspace-admin
        subrole (UPDATE_TENANT_IDP); other tokens receive a 403.

        :param provider: the complete identity provider configuration to store
        :raises AtlanError: on any error during API invocation.
        :returns: the identity provider configuration, re-read after the update
        """
        endpoint, request_obj = SSOUpdateIdentityProvider.prepare_request(provider)
        alias = cast(str, provider.alias)  # validated non-empty by prepare_request
        self._client._call_api(endpoint, request_obj=request_obj)
        return self.get_identity_provider(sso_alias=alias)

    @validate_arguments
    def update_signing_certificate(
        self, sso_alias: str, certificate: str
    ) -> SSOProvider:
        """
        Replaces the signing certificate on the given SSO identity
        provider, leaving the rest of the configuration untouched.

        API tokens authenticate independently of SSO, so this works even
        while SSO logins are failing (for example, after the certificate
        expired) - as long as the token already exists.

        :param sso_alias: alias of the SSO provider (e.g. `azure`, `okta`)
        :param certificate: new X.509 certificate, as PEM or a single line
            of base64; stored as one line with no BEGIN/END lines and no
            line breaks
        :raises AtlanError: on any error during API invocation.
        :raises NotFoundError: if no identity provider exists with the given alias.
        :returns: the identity provider configuration, re-read after the update
        """
        provider = self.get_identity_provider(sso_alias=sso_alias)
        provider.config = provider.config or {}
        provider.config["signingCertificate"] = normalize_signing_certificate(
            certificate
        )
        return self.update_identity_provider(provider=provider)
