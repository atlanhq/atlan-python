# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's /v1/apps/{app}/inputs contract — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_app_inputs
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.app_inputs._base import AppInput


class DatabricksMinerInputs(AppInput):
    """Typed inputs for the `databricks-miner` / `miner` app (generated from its input contract)."""

    _APP_ID: ClassVar[str] = "databricks-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

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
    extract_strategy: str = "system-table"
    """Extract Strategy"""
    extraction_catalog_type_lineage: str = "system-table"
    """Extraction Catalog Type Lineage"""
    cloned_catalog_name_lineage: str = "system"
    """Cloned Catalog Name Lineage"""
    cloned_schema_name_lineage: str = "access"
    """Cloned Schema Name Lineage"""
    sql_warehouse: str = ""
    """Sql Warehouse"""
    path_level_lineage: str = "false"
    """Path Level Lineage"""
    miner_lookback_days: int = 30
    """Miner Lookback Days"""
    miner_chunk_interval_hours: int = 0
    """Miner Chunk Interval Hours"""
    miner_max_concurrent_activities: int = 20
    """Miner Max Concurrent Activities"""
    miner_wave_size: int = 50
    """Miner Wave Size"""
    miner_wave_concurrency: int = 10
    """Miner Wave Concurrency"""
    preflight_context: str = "miner"
    """Preflight Context"""
    calculate_popularity: str = "false"
    """Calculate Popularity"""
    extraction_catalog_type_popularity: str = "system-table"
    """Extraction Catalog Type Popularity"""
    cloned_catalog_name_popularity: str = "system"
    """Cloned Catalog Name Popularity"""
    cloned_schema_name_popularity: str = "query"
    """Cloned Schema Name Popularity"""
    popularity_window_days: int = 30
    """Popularity Window Days"""
    popularity_exclude_user_config: Optional[List[Any]] = None
    """Popularity Exclude User Config"""
    miner_start_time_epoch: int = 0
    """Miner Start Time Epoch"""
    sql_warehouse_popularity: str = ""
    """Sql Warehouse Popularity"""
    preflight_check: str = ""
    """Preflight Check"""
    databricks_miner_credential: Any = None


__all__ = ["DatabricksMinerInputs"]
