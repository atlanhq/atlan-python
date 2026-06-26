# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class PowerbiCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the `powerbi-crawler` / `crawler` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "powerbi-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Workspaces — Selected workspaces will be processed."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Workspaces — Selected workspaces will not be processed."""
    dashboard_report_include_regex: str = Field(
        "", alias="dashboard-report-include-regex"
    )
    """Include Dashboard and Reports Regex — Dashboards and Reports that match the regex will be included. Defaults to empty string."""
    dashboard_report_exclude_regex: str = Field(
        "", alias="dashboard-report-exclude-regex"
    )
    """Exclude Dashboard and Reports Regex — Dashboards and Reports that match the regex will be excluded. Defaults to empty string."""
    fetch_report_definition_extracts: bool = Field(
        True, alias="fetch-report-definition-extracts"
    )
    """Fetch Report Definition Extracts — Whether to fetch Power BI report definition extracts"""
    endorsement_attach_mode: str = Field("metastore", alias="endorsement-attach-mode")
    """Attach Endorsements from Power BI — The workflow automatically certifies the assets endorsed in Power BI"""
    incremental_extraction: bool = Field(False, alias="incremental-extraction")
    """Enable Incremental Extraction — Enable or Disable Incremental Extraction on Source."""
    sql_connection_info_note: str = Field("", alias="sql-connection-info-note")
    enable_odbc_connectivity_mapping: str = Field(
        "false", alias="enable-odbc-connectivity-mapping"
    )
    """Enable ODBC DSN Connectivity Mapping"""
    odbc_dsn_config_mapping: Union[Dict[str, Any], str] = Field(
        "{}", alias="odbc-dsn-config-mapping"
    )


class PowerbiCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for the `powerbi-crawler` / `crawler` app.

    Example::

        resp = (
            PowerbiCrawler(client)
            .connection(qualified_name="default/powerbi/1700000000")
            .include_workspaces({})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "powerbi-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "powerbi"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-powerbi"
    _INPUTS_CLASS = PowerbiCrawlerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def service_principal(
        self,
        *,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        admin_api: str,
        admin_api_summary: Optional[str]=None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "PowerbiCrawler":
        """Direct extraction with service_principal auth.

        :param tenant_id: Tenant ID.
        :param client_id: Client ID.
        :param client_secret: Client Secret.
        :param admin_api: Enable Scanner API Access.
        """
        extras: Dict[str, Any] = {}
        extras["tenantId"] = tenant_id
        extras["clientId"] = client_id
        extras["clientSecret"] = client_secret
        extras["adminAPI"] = admin_api
        if admin_api_summary:
            extras["adminAPISummary"] = admin_api_summary
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-powerbi",
                connector_type="powerbi",
                auth_type="service_principal",
                host=host or "api.powerbi.com",
                port=port or 443,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        tenant_id: str,
        client_id: str,
        client_secret: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "PowerbiCrawler":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        :param tenant_id: Tenant ID.
        :param client_id: Client ID.
        :param client_secret: Client Secret.
        """
        extras: Dict[str, Any] = {}
        extras["tenantId"] = tenant_id
        extras["clientId"] = client_id
        extras["clientSecret"] = client_secret
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-powerbi",
                connector_type="powerbi",
                auth_type="basic",
                username=username,
                password=password,
                host=host or "api.powerbi.com",
                port=port or 443,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def include_workspaces(self, value: Union[Dict[str, Any], str]) -> "PowerbiCrawler":
        """Include Workspaces — Selected workspaces will be processed."""
        self._metadata["include-filter"] = value
        return self

    def exclude_workspaces(self, value: Union[Dict[str, Any], str]) -> "PowerbiCrawler":
        """Exclude Workspaces — Selected workspaces will not be processed."""
        self._metadata["exclude-filter"] = value
        return self

    def include_dashboard_and_reports_regex(self, value: str) -> "PowerbiCrawler":
        """Include Dashboard and Reports Regex — Dashboards and Reports that match the regex will be included. Defaults to empty string."""
        self._metadata["dashboard-report-include-regex"] = value
        return self

    def exclude_dashboard_and_reports_regex(self, value: str) -> "PowerbiCrawler":
        """Exclude Dashboard and Reports Regex — Dashboards and Reports that match the regex will be excluded. Defaults to empty string."""
        self._metadata["dashboard-report-exclude-regex"] = value
        return self

    def fetch_report_definition_extracts(
        self, enabled: bool = True
    ) -> "PowerbiCrawler":
        """Fetch Report Definition Extracts — Whether to fetch Power BI report definition extracts"""
        self._metadata["fetch-report-definition-extracts"] = enabled
        return self

    def attach_endorsements_from_power_bi(
        self, value: Literal["metastore", "requests"]
    ) -> "PowerbiCrawler":
        """Attach Endorsements from Power BI — The workflow automatically certifies the assets endorsed in Power BI"""
        self._metadata["endorsement-attach-mode"] = value
        return self

    def enable_incremental_extraction(self, value: bool) -> "PowerbiCrawler":
        """Enable Incremental Extraction — Enable or Disable Incremental Extraction on Source."""
        self._metadata["incremental-extraction"] = value
        return self

    def sql_connection_info_note(self, value: str) -> "PowerbiCrawler":
        self._metadata["sql-connection-info-note"] = value
        return self

    def enable_odbc_dsn_connectivity_mapping(
        self, value: Literal["true", "false"]
    ) -> "PowerbiCrawler":
        """Enable ODBC DSN Connectivity Mapping"""
        self._metadata["enable-odbc-connectivity-mapping"] = value
        return self

    def odbc_dsn_config_mapping(
        self, value: Union[Dict[str, Any], str]
    ) -> "PowerbiCrawler":
        self._metadata["odbc-dsn-config-mapping"] = value
        return self


__all__ = ["PowerbiCrawler", "PowerbiCrawlerInputs"]
