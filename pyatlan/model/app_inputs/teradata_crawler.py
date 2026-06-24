# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class TeradataCrawlerInputs(AppInput):
    """Typed inputs for the `teradata-crawler` / `crawler` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "teradata-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

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
    advanced_config_strategy: str = "default"
    """Advanced Config Strategy"""
    use_source_schema_filtering: str = "false"
    """Use Source Schema Filtering"""
    preflight_check: str = ""
    """Preflight Check"""
    teradata_crawler_credential: Any = None


__all__ = ["TeradataCrawlerInputs"]
