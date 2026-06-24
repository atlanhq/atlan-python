# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class DatabricksCrawlerInputs(AppInput):
    """Typed inputs for the `databricks-crawler` / `crawler` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "databricks-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    connection: Optional[Any] = None
    credential_guid: str = ""
    """Credential Guid"""
    credential_ref: Any = None
    extraction_method: str = ""
    """Extraction Method"""
    agent_json: Any = None
    exclude_filter: Optional[Dict[str, Any]] = None
    """Exclude Filter"""
    include_filter: Optional[Dict[str, Any]] = None
    """Include Filter"""
    temp_table_regex: str = ""
    """Temp Table Regex"""
    source_tag_prefix: str = ""
    """Source Tag Prefix"""
    extract_strategy: str = "system-tables"
    """Extract Strategy"""
    enable_cross_workspace_discovery: str = "false"
    """Enable Cross Workspace Discovery"""
    workspace_credential_overrides: str = "{}"
    """Workspace Credential Overrides"""
    catalog_include_regex: str = ""
    """Catalog Include Regex"""
    catalog_exclude_regex: str = ""
    """Catalog Exclude Regex"""
    schema_include_regex: str = ""
    """Schema Include Regex"""
    schema_exclude_regex: str = ""
    """Schema Exclude Regex"""
    table_include_regex: str = ""
    """Table Include Regex"""
    table_exclude_regex: str = ""
    """Table Exclude Regex"""
    enable_tags: str = "false"
    """Enable Tags"""
    enable_models: str = "false"
    """Enable Models"""
    enable_model_lineage: str = "false"
    """Enable Model Lineage"""
    include_filter_system_tables: Optional[Dict[str, Any]] = None
    """Include Filter System Tables"""
    exclude_filter_system_tables: Optional[Dict[str, Any]] = None
    """Exclude Filter System Tables"""
    temp_table_regex_system_tables: str = ""
    """Temp Table Regex System Tables"""
    include_filter_rest: Optional[Dict[str, Any]] = None
    """Include Filter Rest"""
    exclude_filter_rest: Optional[Dict[str, Any]] = None
    """Exclude Filter Rest"""
    enable_complex_types: str = "true"
    """Enable Complex Types"""
    advanced_config_strategy: str = "default"
    """Advanced Config Strategy"""
    use_parallelize_table_enrichment: str = "true"
    """Use Parallelize Table Enrichment"""
    enable_view_lineage: str = "true"
    """Enable View Lineage"""
    use_source_schema_filtering: str = "false"
    """Use Source Schema Filtering"""
    incremental_extraction: str = "false"
    """Incremental Extraction"""
    sql_warehouse: Optional[Dict[str, Any]] = None
    """Sql Warehouse"""
    enable_tag_sync: str = "false"
    """Enable Tag Sync"""
    preflight_check: str = ""
    """Preflight Check"""
    databricks_crawler_credential: Any = None


__all__ = ["DatabricksCrawlerInputs"]
