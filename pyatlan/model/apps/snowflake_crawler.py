# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class SnowflakeCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the `snowflake-crawler` / `crawler` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "snowflake-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    extract_strategy: str = Field("information-schema", alias="extract-strategy")
    """Extraction method — Determines the method the package will use to extract metadata from Snowflake. Please refer to the docs [here](https://docs.atlan.com/apps/connectors/data-warehouses/snowflake/how-tos/set-up-snowflake#choose-metadata-fetching-method)."""
    account_usage_database_name: str = Field(
        "SNOWFLAKE", alias="account-usage-database-name"
    )
    """Database Name — Database name to extract account usage data from. Defaults to SNOWFLAKE"""
    account_usage_schema_name: str = Field(
        "ACCOUNT_USAGE", alias="account-usage-schema-name"
    )
    """Schema Name — Schema name to extract account usage data from. Defaults to ACCOUNT_USAGE"""
    temp_table_regex: str = Field("", alias="temp-table-regex")
    """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string"""
    exclude_empty_tables: bool = Field(False, alias="exclude-empty-tables")
    """Exclude tables with empty data — Excludes tables and their corresponding columns when the table contains no data."""
    exclude_views: bool = Field(False, alias="exclude-views")
    """Exclude views — Excludes all views"""
    enable_lineage: bool = Field(True, alias="enable-lineage")
    """View Definition Lineage — Enable view definition lineage while crawling"""
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata — Only the selected databases will be extracted. Exclude gets preference over include for common databases, if present, in the config."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata — Selected databases and schemas wont be extracted."""
    asset_selection: Union[Dict[str, Any], str] = Field("{}", alias="asset-selection")
    """Asset selection — Select the assets you want to crawl, or filter out the ones you don't."""
    preflight_check: str = Field("", alias="preflight-check")
    enable_snowflake_tags: bool = Field(False, alias="enable-snowflake-tags")
    """Import Tags — Syncing tags from snowflake to atlan"""
    enable_stages: bool = Field(False, alias="enable-stages")
    """Import Stages — Import internal and external named stages from snowflake to atlan"""
    incremental_extraction: bool = Field(True, alias="incremental-extraction")
    """Enable Incremental Extraction — Enable or Disable Schema Incremental Extraction on source."""
    control_config_strategy: str = Field("default", alias="control-config-strategy")
    """Control Config — Controls custom experimental feature flags for the crawler"""
    control_config: str = Field("", alias="control-config")
    """Custom Config — Custom JSON config controlling experimental feature flags for the crawler"""
    enable_semantic_views: bool = Field(False, alias="enable-semantic-views")
    """Import Semantic Views — Import semantic views, logical tables, dimensions, metrics and facts from snowflake to atlan"""


class SnowflakeCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for the `snowflake-crawler` / `crawler` app.

    Example::

        resp = (
            SnowflakeCrawler(client)
            .keypair(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .extraction_method('information-schema')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "snowflake-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "snowflake"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-snowflake"
    _INPUTS_CLASS = SnowflakeCrawlerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def keypair(
        self,
        *,
        username: str,
        password: str,
        private_key_password: Optional[str] = None,
        role: Optional[str] = None,
        warehouse: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "SnowflakeCrawler":
        """Direct extraction with Keypair Authentication auth.

        :param username: Username.
        :param password: Encrypted Private Key.
        :param private_key_password: Private Key Password.
        :param role: Role.
        :param warehouse: Warehouse.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        if private_key_password is not None:
            extras["private_key_password"] = private_key_password
        if role is not None:
            extras["role"] = role
        if warehouse is not None:
            extras["warehouse"] = warehouse
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="keypair",
            username=username,
            password=password,
            host=host or "",
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def okta(
        self,
        *,
        username: str,
        password: str,
        authenticator: str,
        role: Optional[str] = None,
        warehouse: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "SnowflakeCrawler":
        """Direct extraction with Okta SSO Authentication auth.

        :param username: Username.
        :param password: Password.
        :param authenticator: Authenticator.
        :param role: Role.
        :param warehouse: Warehouse.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["authenticator"] = authenticator
        if role is not None:
            extras["role"] = role
        if warehouse is not None:
            extras["warehouse"] = warehouse
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="okta",
            username=username,
            password=password,
            host=host or "",
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def entra_id(
        self,
        *,
        username: str,
        password: str,
        tenant_id: str,
        oauth_scope: str,
        role: Optional[str] = None,
        warehouse: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "SnowflakeCrawler":
        """Direct extraction with Microsoft Entra ID auth.

        :param username: Client ID.
        :param password: Client Secret.
        :param tenant_id: Tenant ID.
        :param oauth_scope: OAuth Scope.
        :param role: Role.
        :param warehouse: Warehouse.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["tenantId"] = tenant_id
        extras["oauthScope"] = oauth_scope
        if role is not None:
            extras["role"] = role
        if warehouse is not None:
            extras["warehouse"] = warehouse
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="entra_id",
            username=username,
            password=password,
            host=host or "",
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        role: Optional[str] = None,
        warehouse: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "SnowflakeCrawler":
        """Direct extraction with Basic Authentication auth.

        :param username: Username.
        :param password: Password.
        :param role: Role.
        :param warehouse: Warehouse.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        if role is not None:
            extras["role"] = role
        if warehouse is not None:
            extras["warehouse"] = warehouse
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="basic",
            username=username,
            password=password,
            host=host or "",
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def extraction_method(
        self, value: Literal["information-schema", "account-usage"]
    ) -> "SnowflakeCrawler":
        """Extraction method — Determines the method the package will use to extract metadata from Snowflake. Please refer to the docs [here](https://docs.atlan.com/apps/connectors/data-warehouses/snowflake/how-tos/set-up-snowflake#choose-metadata-fetching-method)."""
        self._metadata["extract-strategy"] = value
        return self

    def database_name(self, value: str) -> "SnowflakeCrawler":
        """Database Name — Database name to extract account usage data from. Defaults to SNOWFLAKE"""
        self._metadata["account-usage-database-name"] = value
        return self

    def schema_name(self, value: str) -> "SnowflakeCrawler":
        """Schema Name — Schema name to extract account usage data from. Defaults to ACCOUNT_USAGE"""
        self._metadata["account-usage-schema-name"] = value
        return self

    def exclude_regex_for_tables_views(self, value: str) -> "SnowflakeCrawler":
        """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string"""
        self._metadata["temp-table-regex"] = value
        return self

    def exclude_tables_with_empty_data(self, value: bool) -> "SnowflakeCrawler":
        """Exclude tables with empty data — Excludes tables and their corresponding columns when the table contains no data."""
        self._metadata["exclude-empty-tables"] = value
        return self

    def exclude_views(self, value: bool) -> "SnowflakeCrawler":
        """Exclude views — Excludes all views"""
        self._metadata["exclude-views"] = value
        return self

    def view_definition_lineage(self, value: bool) -> "SnowflakeCrawler":
        """View Definition Lineage — Enable view definition lineage while crawling"""
        self._metadata["enable-lineage"] = value
        return self

    def include_metadata(self, value: Union[Dict[str, Any], str]) -> "SnowflakeCrawler":
        """Include Metadata — Only the selected databases will be extracted. Exclude gets preference over include for common databases, if present, in the config."""
        self._metadata["include-filter"] = value
        return self

    def exclude_metadata(self, value: Union[Dict[str, Any], str]) -> "SnowflakeCrawler":
        """Exclude Metadata — Selected databases and schemas wont be extracted."""
        self._metadata["exclude-filter"] = value
        return self

    def asset_selection(self, value: Union[Dict[str, Any], str]) -> "SnowflakeCrawler":
        """Asset selection — Select the assets you want to crawl, or filter out the ones you don't."""
        self._metadata["asset-selection"] = value
        return self

    def preflight_check(self, value: str) -> "SnowflakeCrawler":
        self._metadata["preflight-check"] = value
        return self

    def import_tags(self, value: bool) -> "SnowflakeCrawler":
        """Import Tags — Syncing tags from snowflake to atlan"""
        self._metadata["enable-snowflake-tags"] = value
        return self

    def import_stages(self, value: bool) -> "SnowflakeCrawler":
        """Import Stages — Import internal and external named stages from snowflake to atlan"""
        self._metadata["enable-stages"] = value
        return self

    def enable_incremental_extraction(self, value: bool) -> "SnowflakeCrawler":
        """Enable Incremental Extraction — Enable or Disable Schema Incremental Extraction on source."""
        self._metadata["incremental-extraction"] = value
        return self

    def control_config(self, value: Literal["default", "custom"]) -> "SnowflakeCrawler":
        """Control Config — Controls custom experimental feature flags for the crawler"""
        self._metadata["control-config-strategy"] = value
        return self

    def custom_config(self, value: str) -> "SnowflakeCrawler":
        """Custom Config — Custom JSON config controlling experimental feature flags for the crawler"""
        self._metadata["control-config"] = value
        return self

    def import_semantic_views(self, value: bool) -> "SnowflakeCrawler":
        """Import Semantic Views — Import semantic views, logical tables, dimensions, metrics and facts from snowflake to atlan"""
        self._metadata["enable-semantic-views"] = value
        return self


__all__ = ["SnowflakeCrawler", "SnowflakeCrawlerInputs"]
