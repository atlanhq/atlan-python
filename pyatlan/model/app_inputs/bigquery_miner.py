# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class BigqueryMinerInputs(AppInput):
    """Typed inputs for the `bigquery-miner` / `miner` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "bigquery-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

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
    miner_start_time_epoch: int = 0
    """Miner Start Time Epoch"""
    region_strategy: str = "default"
    """Region Strategy"""
    region: str = "region-us"
    """Region"""
    fetch_all_projects_query_history: bool = False
    """Fetch All Projects Query History"""
    chunk_interval_hours: int = 0
    """Chunk Interval Hours"""
    enable_continue_as_new: bool = False
    """Enable Continue As New"""
    max_concurrent_activities: int = 50
    """Max Concurrent Activities"""
    max_activities_per_execution: int = 300
    """Max Activities Per Execution"""
    schedule_to_start_timeout_secs: int = 10800
    """Schedule To Start Timeout Secs"""
    sql_pandas_batch_size: int = 6000
    """Sql Pandas Batch Size"""
    test_miner_table: str = ""
    """Test Miner Table"""
    preflight_check: str = ""
    """Preflight Check"""
    calculate_popularity: str = "true"
    """Calculate Popularity"""
    pricing_model: str = "on-demand"
    """Pricing Model"""
    popularity_window_days: int = 30
    """Popularity Window Days"""
    popularity_exclude_user_config: Optional[List[Any]] = None
    """Popularity Exclude User Config"""
    control_config_strategy: str = "default"
    """Control Config Strategy"""
    control_config: str = "{}"
    """Control Config"""
    bigquery_miner_credential: Any = None


__all__ = ["BigqueryMinerInputs"]
