# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class PowerbiCrawlerInputs(AppInput):
    """Typed inputs for the `powerbi-crawler` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "powerbi-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    connection: Optional[Any] = None
    credential_guid: str = ""
    """Credential Guid"""
    credential_ref: Any = None
    extraction_method: str = ""
    """Extraction Method"""
    agent_json: Any = None
    exclude_filter: Union[Dict[str, Any], str] = ""
    """Exclude Filter"""
    include_filter: Union[Dict[str, Any], str] = ""
    """Include Filter"""
    temp_table_regex: str = ""
    """Temp Table Regex"""
    source_tag_prefix: str = ""
    """Source Tag Prefix"""
    dashboard_report_include_regex: str = ""
    """Dashboard Report Include Regex"""
    dashboard_report_exclude_regex: str = ""
    """Dashboard Report Exclude Regex"""
    fetch_report_definition_extracts: bool = True
    """Fetch Report Definition Extracts"""
    endorsement_attach_mode: str = "metastore"
    """Endorsement Attach Mode"""
    incremental_extraction: bool = False
    """Incremental Extraction"""
    sql_connection_qualified_names: str = ""
    """Sql Connection Qualified Names"""
    enable_odbc_connectivity_mapping: str = "false"
    """Enable Odbc Connectivity Mapping"""
    odbc_dsn_config_mapping: Optional[Dict[str, Any]] = None
    """Odbc Dsn Config Mapping"""
    preflight_check: str = ""
    """Preflight Check"""
    powerbi_credential: Any = None


__all__ = ["PowerbiCrawlerInputs"]
