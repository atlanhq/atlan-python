# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Optional

from pydantic.v1 import Field

from ._base import AppBuilder, AppInput


class SnowflakeMinerInputs(AppInput):
    """Typed, UI-facing inputs for the `snowflake-miner` / `miner` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "snowflake-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    snowflake_database: str = Field("default", alias="snowflake-database")
    """Snowflake Database — Optionally provide details of the cloned version of the snowflake database"""
    database_name: str = Field("SNOWFLAKE", alias="database-name")
    """Database Name — Snowflake database name to be used"""
    schema_name: str = Field("ACCOUNT_USAGE", alias="schema-name")
    """Schema Name — Account Usage schema name in the Snowflake database"""
    miner_start_time_epoch: float = Field(0, alias="miner-start-time-epoch")
    """Start date"""
    control_config_strategy: str = Field("default", alias="control-config-strategy")
    """Advanced Config — Controls custom experimental feature flags for the miner"""
    control_config: str = Field("", alias="control-config")
    """Custom Config — Custom JSON config controlling experimental feature flags for the miner"""
    preflight_check: str = Field("", alias="preflight-check")
    calculate_popularity: bool = Field(True, alias="calculate-popularity")
    """Calculate popularity — Enable popularity metrics generated using mined data."""
    popularity_window_days: float = Field(30, alias="popularity-window-days")
    """Popularity Window (days) — Number of days to consider for calculating popularity."""
    popularity_exclude_user_config: List[Any] = Field(
        [], alias="popularity-exclude-user-config"
    )
    """Excluded Users — List of users who should be excluded while calculating usage metrics for assets"""


class SnowflakeMiner(AppBuilder):
    """Fluent, UI-equivalent builder for the `snowflake-miner` / `miner` app.

    Example::

        resp = (
            SnowflakeMiner(client)
            .connection(qualified_name="default/snowflake/1700000000")
            .snowflake_database('default')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "snowflake-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"
    _CONNECTOR_NAME: ClassVar[str] = "snowflake"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _INPUTS_CLASS = SnowflakeMinerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {
        "extract_strategy": "miner",
        "native_lineage_active": False,
        "indirect_lineage": "false",
        "ignore_orphans": "false",
        "enable_sharded": "false",
        "enable_parent_job_scoping": "false",
        "enable_fallback_match": "true",
        "include_indirect_column_relations": "false",
        "process_routines": "true",
    }

    # ── Step 3 · Metadata ──
    def snowflake_database(
        self, value: Literal["default", "cloned"]
    ) -> "SnowflakeMiner":
        """Snowflake Database — Optionally provide details of the cloned version of the snowflake database"""
        self._metadata["snowflake-database"] = value
        return self

    def database_name(self, value: str) -> "SnowflakeMiner":
        """Database Name — Snowflake database name to be used"""
        self._metadata["database-name"] = value
        return self

    def schema_name(self, value: str) -> "SnowflakeMiner":
        """Schema Name — Account Usage schema name in the Snowflake database"""
        self._metadata["schema-name"] = value
        return self

    def start_date(self, value: float) -> "SnowflakeMiner":
        """Start date"""
        self._metadata["miner-start-time-epoch"] = value
        return self

    def advanced_config(self, value: Literal["default", "custom"]) -> "SnowflakeMiner":
        """Advanced Config — Controls custom experimental feature flags for the miner"""
        self._metadata["control-config-strategy"] = value
        return self

    def custom_config(self, value: str) -> "SnowflakeMiner":
        """Custom Config — Custom JSON config controlling experimental feature flags for the miner"""
        self._metadata["control-config"] = value
        return self

    def preflight_check(self, value: str) -> "SnowflakeMiner":
        self._metadata["preflight-check"] = value
        return self

    def calculate_popularity(self, value: bool) -> "SnowflakeMiner":
        """Calculate popularity — Enable popularity metrics generated using mined data."""
        self._metadata["calculate-popularity"] = value
        return self

    def popularity_window_days(self, value: float) -> "SnowflakeMiner":
        """Popularity Window (days) — Number of days to consider for calculating popularity."""
        self._metadata["popularity-window-days"] = value
        return self

    def excluded_users(self, value: List[Any]) -> "SnowflakeMiner":
        """Excluded Users — List of users who should be excluded while calculating usage metrics for assets"""
        self._metadata["popularity-exclude-user-config"] = value
        return self


__all__ = ["SnowflakeMiner", "SnowflakeMinerInputs"]
