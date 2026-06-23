# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class BigqueryCrawlerInputs(AppInput):
    """Typed inputs for the `bigquery-crawler` / `crawler` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "bigquery-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    connection: Optional[Any] = None
    credential_guid: str = ""
    """Credential Guid"""
    credential_ref: Any = None
    extraction_method: str = ""
    """Extraction Method"""
    agent_json: Any = None
    output_prefix: str = ""
    """Output Prefix"""
    output_path: str = ""
    """Output Path"""
    exclude_filter: Union[Dict[str, Any], str] = ""
    """Exclude Filter"""
    include_filter: Union[Dict[str, Any], str] = ""
    """Include Filter"""
    temp_table_regex: str = ""
    """Temp Table Regex"""
    source_tag_prefix: str = ""
    """Source Tag Prefix"""
    atlas_auth_type: str = "internal"
    """Atlas Auth Type"""
    enable_nested_columns: bool = True
    """Enable Nested Columns"""
    enable_bigquery_tag_sync: bool = False
    """Enable Bigquery Tag Sync"""
    filter_sharded_tables: bool = True
    """Filter Sharded Tables"""
    hidden_datasets: bool = False
    """Hidden Datasets"""
    control_config_strategy: str = "default"
    """Control Config Strategy"""
    control_config: str = "{}"
    """Control Config"""
    list_datasets_per_chunk: int = 50
    """List Datasets Per Chunk"""
    mapping_chunk_size: int = 1000
    """Mapping Chunk Size"""
    extract_output_chuck_size: int = 50000
    """Extract Output Chuck Size"""
    max_concurrent_activities: int = 15
    """Max Concurrent Activities"""
    max_activities_per_execution: int = 300
    """Max Activities Per Execution"""
    preflight_check: str = ""
    """Preflight Check"""
    bigquery_crawler_credential: Any = None
    output_dir: str = ""
    """Output Dir"""
    checkpoint_dir: str = ""
    """Checkpoint Dir"""
    load_to_atlan: bool = True
    """Load To Atlan"""
    publish_dry_run: bool = False
    """Publish Dry Run"""


__all__ = ["BigqueryCrawlerInputs"]
