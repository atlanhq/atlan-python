# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _selective_filter


class AtlanTableauInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-tableau` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-tableau"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Projects — Selected projects will be processed (empty = all projects)."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Projects — Selected projects will not be processed."""
    exclude_projects_regex: str = Field("", alias="exclude-projects-regex")
    """Exclude Projects Regex — Projects whose names match the regex will not be processed. Defaults to empty string."""
    tableau_alternate_host: str = Field(
        "https://alternate.tableau.com", alias="tableau-alternate-host"
    )
    """Alternate Host URL — Protocol and host name to use in the link for the 'View in Tableau' button."""
    crawl_unpublished_worksheets_dashboards: bool = Field(
        True, alias="crawl-unpublished-worksheets-dashboards"
    )
    """Crawl Unpublished Worksheets and Dashboards — Default behaviour is to crawl all worksheets and dashboards, including hidden ones. Selecting 'No' will exclude assets marked hidden in Tableau Desktop."""
    crawl_hidden_datasource_fields: bool = Field(
        True, alias="crawl-hidden-datasource-fields"
    )
    """Crawl Hidden Datasource Fields — Default behaviour is to crawl all datasource fields, including hidden ones. Selecting 'No' will exclude fields marked hidden in Tableau Desktop."""
    crawl_embedded_dashboards: bool = Field(False, alias="crawl-embedded-dashboards")
    """Crawl Embedded Dashboards — Default behaviour does not create relationships between embedded dashboards. Selecting 'Yes' will create them; this can increase workflow runtime."""
    incremental_enabled: bool = Field(False, alias="incremental-enabled")
    """Incremental Mode — v3-only. When enabled, only fetches metadata changed since the last successful run."""
    force_full_extraction: bool = Field(False, alias="force-full-extraction")
    """Force Full Field Extraction — v3-only. When enabled, ignores the incremental marker and performs a full field extraction even if Incremental Mode is on. Use this to re-seed the incremental field cache. Has no effect when Incremental Mode is off."""


class AtlanTableau(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-tableau` app.

    Example::

        resp = (
            AtlanTableau(client)
            .basic(username="...", password="...", protocol="...", host="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .include_projects({})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-tableau"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "tableau"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-tableau"
    _INPUTS_CLASS = AtlanTableauInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        default_site: Optional[str] = None,
        protocol: str,
        self_signed_ssl_certificate: Optional[str] = None,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanTableau":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        :param default_site: Site.
        :param protocol: SSL.
        :param self_signed_ssl_certificate: SSL Certificate.
        """
        extras: Dict[str, Any] = {}
        if default_site is not None:
            extras["defaultSite"] = default_site
        extras["protocol"] = protocol
        if self_signed_ssl_certificate is not None:
            extras["selfSignedSSLCertificate"] = self_signed_ssl_certificate
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-tableau",
                connector_type="tableau",
                auth_type="basic",
                username=username,
                password=password,
                host=host,
                port=port or 443,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def personal_access_token(
        self,
        *,
        username: str,
        password: str,
        default_site: Optional[str] = None,
        protocol: str,
        self_signed_ssl_certificate: Optional[str] = None,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanTableau":
        """Direct extraction with personal_access_token auth.

        :param username: PAT Name.
        :param password: PAT Secret.
        :param default_site: Site.
        :param protocol: SSL.
        :param self_signed_ssl_certificate: SSL Certificate.
        """
        extras: Dict[str, Any] = {}
        if default_site is not None:
            extras["defaultSite"] = default_site
        extras["protocol"] = protocol
        if self_signed_ssl_certificate is not None:
            extras["selfSignedSSLCertificate"] = self_signed_ssl_certificate
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-tableau",
                connector_type="tableau",
                auth_type="personal_access_token",
                username=username,
                password=password,
                host=host,
                port=port or 443,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def jwt(
        self,
        *,
        username: str,
        client_id: str,
        private_id: str,
        private_key: str,
        default_site: Optional[str] = None,
        protocol: str,
        self_signed_ssl_certificate: Optional[str] = None,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanTableau":
        """Direct extraction with jwt auth.

        :param username: Username (sub claim).
        :param client_id: Client ID (iss claim).
        :param private_id: Secret ID (kid claim).
        :param private_key: Secret.
        :param default_site: Site.
        :param protocol: SSL.
        :param self_signed_ssl_certificate: SSL Certificate.
        """
        extras: Dict[str, Any] = {}
        extras["client_id"] = client_id
        extras["private_id"] = private_id
        extras["private_key"] = private_key
        if default_site is not None:
            extras["defaultSite"] = default_site
        extras["protocol"] = protocol
        if self_signed_ssl_certificate is not None:
            extras["selfSignedSSLCertificate"] = self_signed_ssl_certificate
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-tableau",
                connector_type="tableau",
                auth_type="jwt",
                username=username,
                host=host,
                port=port or 443,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def include_projects(self, value: Union[Dict[str, Any], str]) -> "AtlanTableau":
        """Include Projects — Selected projects will be processed (empty = all projects).

        Pass a ``{project_id: {}}`` map — it is serialized to the JSON-string form the
        contract expects. A string passes through as-is.
        """
        self._metadata["include-filter"] = _selective_filter(value)
        return self

    def exclude_projects(self, value: Union[Dict[str, Any], str]) -> "AtlanTableau":
        """Exclude Projects — Selected projects will not be processed.

        Pass a ``{project_id: {}}`` map — it is serialized to the JSON-string form the
        contract expects. A string passes through as-is.
        """
        self._metadata["exclude-filter"] = _selective_filter(value)
        return self

    def exclude_projects_regex(self, value: str) -> "AtlanTableau":
        """Exclude Projects Regex — Projects whose names match the regex will not be processed. Defaults to empty string."""
        self._metadata["exclude-projects-regex"] = value
        return self

    def alternate_host_url(self, value: str) -> "AtlanTableau":
        """Alternate Host URL — Protocol and host name to use in the link for the 'View in Tableau' button."""
        self._metadata["tableau-alternate-host"] = value
        return self

    def crawl_unpublished_worksheets_and_dashboards(
        self, enabled: bool = True
    ) -> "AtlanTableau":
        """Crawl Unpublished Worksheets and Dashboards — Default behaviour is to crawl all worksheets and dashboards, including hidden ones. Selecting 'No' will exclude assets marked hidden in Tableau Desktop."""
        self._metadata["crawl-unpublished-worksheets-dashboards"] = enabled
        return self

    def crawl_hidden_datasource_fields(self, enabled: bool = True) -> "AtlanTableau":
        """Crawl Hidden Datasource Fields — Default behaviour is to crawl all datasource fields, including hidden ones. Selecting 'No' will exclude fields marked hidden in Tableau Desktop."""
        self._metadata["crawl-hidden-datasource-fields"] = enabled
        return self

    def crawl_embedded_dashboards(self, enabled: bool = True) -> "AtlanTableau":
        """Crawl Embedded Dashboards — Default behaviour does not create relationships between embedded dashboards. Selecting 'Yes' will create them; this can increase workflow runtime."""
        self._metadata["crawl-embedded-dashboards"] = enabled
        return self

    def incremental_mode(self, enabled: bool = True) -> "AtlanTableau":
        """Incremental Mode — v3-only. When enabled, only fetches metadata changed since the last successful run."""
        self._metadata["incremental-enabled"] = enabled
        return self

    def force_full_field_extraction(self, enabled: bool = True) -> "AtlanTableau":
        """Force Full Field Extraction — v3-only. When enabled, ignores the incremental marker and performs a full field extraction even if Incremental Mode is on. Use this to re-seed the incremental field cache. Has no effect when Incremental Mode is off."""
        self._metadata["force-full-extraction"] = enabled
        return self


__all__ = ["AtlanTableau", "AtlanTableauInputs"]
