# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class DatabricksCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the `databricks-crawler` / `crawler` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "databricks-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    extract_strategy: Union[Dict[str, Any], str] = Field(
        "system-tables", alias="extract-strategy"
    )
    """Extraction Strategy — `System Tables` issues SQL against Unity Catalog's `system.information_schema` (fast, efficient). `REST API` uses the Databricks SDK (works on workspaces where system tables are not enabled). `JDBC` is deprecated and only available for tenants on PAT auth (legacy `hive_metastore` workloads)."""
    enable_cross_workspace_discovery: Union[Dict[str, Any], str] = Field(
        "false", alias="enable-cross-workspace-discovery"
    )
    """Enable Cross-Workspace Discovery — Discover catalogs and assets from all workspaces sharing the same Unity Catalog metastore. Uses `system.access.workspaces_latest` to enumerate peer workspaces."""
    temp_table_regex: Union[Dict[str, Any], str] = Field("", alias="temp-table-regex")
    """Exclude regex for tables and views — Regex matching temp table names to exclude from extraction (e.g. `.*_TMP|.*_TEMP|TMP.*|TEMP.*`)."""
    enable_tags: Union[Dict[str, Any], str] = Field("false", alias="enable-tags")
    """Import tags — Sync Unity Catalog tags from Databricks to Atlan."""
    enable_models: Union[Dict[str, Any], str] = Field("false", alias="enable-models")
    """Import AI Models — Import Databricks ML model and model-version metadata."""
    enable_model_lineage: Union[Dict[str, Any], str] = Field(
        "false", alias="enable-model-lineage"
    )
    """Import AI Model Lineage — Emit lineage edges from ML model assets."""
    enable_complex_types: str = Field("true", alias="enable-complex-types")
    """Nested Columns — Parse STRUCT/ARRAY/MAP columns into nested child columns."""
    advanced_config_strategy: Union[Dict[str, Any], str] = Field(
        "default", alias="advanced-config-strategy"
    )
    """Advanced Config — `Default` ships a sensible JDBC default. `Custom` reveals JDBC-only tuning knobs."""
    enable_view_lineage: Union[Dict[str, Any], str] = Field(
        "true", alias="enable-view-lineage"
    )
    """Enable View Lineage — Build column-level lineage edges for views from their definitions."""
    use_source_schema_filtering: Union[Dict[str, Any], str] = Field(
        "false", alias="use-source-schema-filtering"
    )
    """Use Source Schema Filtering — Apply include/exclude schema filters at the source query layer (JDBC only)."""
    incremental_extraction: Union[Dict[str, Any], str] = Field(
        "false", alias="incremental-extraction"
    )
    """Incremental Extraction — Only extract assets changed since the last successful run (uses a timestamp watermark)."""
    sql_warehouse: Union[Dict[str, Any], str] = Field({}, alias="sql-warehouse")
    """SQL warehouse — SQL warehouse used for tag extraction and REST preflight checks."""
    asset_selection: Union[Dict[str, Any], str] = Field("{}", alias="asset-selection")
    """Asset selection — Select the assets you want to crawl, or filter out the ones you don't."""


class DatabricksCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for the `databricks-crawler` / `crawler` app.

    Example::

        resp = (
            DatabricksCrawler(client)
            .basic(password="...", http_path="...", host="...")
            .connection(name="my-connection", admins=["jdoe"])
            .extraction_strategy('system-tables')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "databricks-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "databricks"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-databricks"
    _INPUTS_CLASS = DatabricksCrawlerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {
        "workspace_credential_overrides": "{}",
        "include_filter": "{}",
        "exclude_filter": "{}",
        "use_parallelize_table_enrichment": "true",
        "enable_tag_sync": "false",
    }

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        password: str,
        http_path: str,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "DatabricksCrawler":
        """Direct extraction with basic auth.

        :param password: Personal Access Token.
        :param http_path: HTTP Path.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["__http_path"] = http_path
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="basic",
            password=password,
            host=host,
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def aws_service(
        self,
        *,
        client_id: str,
        client_secret: str,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "DatabricksCrawler":
        """Direct extraction with aws_service auth.

        :param client_id: Client ID.
        :param client_secret: Client Secret.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["clientID"] = client_id
        extras["clientSecret"] = client_secret
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="aws_service",
            host=host,
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def azure_service(
        self,
        *,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "DatabricksCrawler":
        """Direct extraction with azure_service auth.

        :param client_id: Client ID.
        :param client_secret: Client Secret.
        :param tenant_id: Tenant ID.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["clientID"] = client_id
        extras["clientSecret"] = client_secret
        extras["tenantID"] = tenant_id
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="azure_service",
            host=host,
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def extraction_strategy(
        self, value: Literal["system-tables", "rest-api"]
    ) -> "DatabricksCrawler":
        """Extraction Strategy — `System Tables` issues SQL against Unity Catalog's `system.information_schema` (fast, efficient). `REST API` uses the Databricks SDK (works on workspaces where system tables are not enabled). `JDBC` is deprecated and only available for tenants on PAT auth (legacy `hive_metastore` workloads)."""
        self._metadata["extract-strategy"] = value
        return self

    def enable_cross_workspace_discovery(
        self, value: Literal["false", "true"]
    ) -> "DatabricksCrawler":
        """Enable Cross-Workspace Discovery — Discover catalogs and assets from all workspaces sharing the same Unity Catalog metastore. Uses `system.access.workspaces_latest` to enumerate peer workspaces."""
        self._metadata["enable-cross-workspace-discovery"] = value
        return self

    def exclude_regex_for_tables_and_views(
        self, value: Union[Dict[str, Any], str]
    ) -> "DatabricksCrawler":
        """Exclude regex for tables and views — Regex matching temp table names to exclude from extraction (e.g. `.*_TMP|.*_TEMP|TMP.*|TEMP.*`)."""
        self._metadata["temp-table-regex"] = value
        return self

    def import_tags(self, value: Literal["false", "true"]) -> "DatabricksCrawler":
        """Import tags — Sync Unity Catalog tags from Databricks to Atlan."""
        self._metadata["enable-tags"] = value
        return self

    def import_ai_models(self, value: Literal["false", "true"]) -> "DatabricksCrawler":
        """Import AI Models — Import Databricks ML model and model-version metadata."""
        self._metadata["enable-models"] = value
        return self

    def import_ai_model_lineage(
        self, value: Literal["false", "true"]
    ) -> "DatabricksCrawler":
        """Import AI Model Lineage — Emit lineage edges from ML model assets."""
        self._metadata["enable-model-lineage"] = value
        return self

    def nested_columns(self, value: Literal["false", "true"]) -> "DatabricksCrawler":
        """Nested Columns — Parse STRUCT/ARRAY/MAP columns into nested child columns."""
        self._metadata["enable-complex-types"] = value
        return self

    def advanced_config(
        self, value: Literal["default", "custom"]
    ) -> "DatabricksCrawler":
        """Advanced Config — `Default` ships a sensible JDBC default. `Custom` reveals JDBC-only tuning knobs."""
        self._metadata["advanced-config-strategy"] = value
        return self

    def enable_view_lineage(
        self, value: Literal["false", "true"]
    ) -> "DatabricksCrawler":
        """Enable View Lineage — Build column-level lineage edges for views from their definitions."""
        self._metadata["enable-view-lineage"] = value
        return self

    def use_source_schema_filtering(
        self, value: Literal["false", "true"]
    ) -> "DatabricksCrawler":
        """Use Source Schema Filtering — Apply include/exclude schema filters at the source query layer (JDBC only)."""
        self._metadata["use-source-schema-filtering"] = value
        return self

    def incremental_extraction(
        self, value: Literal["false", "true"]
    ) -> "DatabricksCrawler":
        """Incremental Extraction — Only extract assets changed since the last successful run (uses a timestamp watermark)."""
        self._metadata["incremental-extraction"] = value
        return self

    def sql_warehouse(self, value: Union[Dict[str, Any], str]) -> "DatabricksCrawler":
        """SQL warehouse — SQL warehouse used for tag extraction and REST preflight checks."""
        self._metadata["sql-warehouse"] = value
        return self

    def asset_selection(self, value: Union[Dict[str, Any], str]) -> "DatabricksCrawler":
        """Asset selection — Select the assets you want to crawl, or filter out the ones you don't."""
        self._metadata["asset-selection"] = value
        return self


__all__ = ["DatabricksCrawler", "DatabricksCrawlerInputs"]
