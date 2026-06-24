# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class AtlanTableauInputs(AppInput):
    """Typed inputs for the `atlan-tableau` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "atlan-tableau"
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
    exclude_projects_regex: str = ""
    """Exclude Projects Regex"""
    preflight_check: str = ""
    """Preflight Check"""
    tableau_alternate_host: str = ""
    """Tableau Alternate Host"""
    crawl_unpublished_worksheets_dashboards: bool = True
    """Crawl Unpublished Worksheets Dashboards"""
    crawl_hidden_datasource_fields: bool = True
    """Crawl Hidden Datasource Fields"""
    crawl_embedded_dashboards: bool = False
    """Crawl Embedded Dashboards"""
    incremental_enabled: bool = False
    """Incremental Enabled"""
    force_full_extraction: bool = False
    """Force Full Extraction"""
    tableau_credential: Any = None


__all__ = ["AtlanTableauInputs"]
