# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Optional

from pydantic.v1 import Field

from ._base import AppBuilder, AppInput


class BigqueryMinerInputs(AppInput):
    """Typed, UI-facing inputs for the `bigquery-miner` / `miner` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "bigquery-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    miner_start_time_epoch: float = Field(0, alias="miner-start-time-epoch")
    """Start date"""
    region_strategy: str = Field("default", alias="region-strategy")
    """Region — Set the default region used by the BigQuery Miner. Defaults to `region-us` if unspecified."""
    region: str = "region-us"
    """Custom BigQuery Region — The miner works in a single region by default. Defaults to `region-us` if unspecified."""
    fetch_all_projects_query_history: bool = Field(
        False, alias="fetch-all-projects-query-history"
    )
    """Fetch excluded project's QUERY_HISTORY — Enable this if you want to bring-in queries from excluded database/project. If unsure, don't enable this."""
    calculate_popularity: str = Field("true", alias="calculate-popularity")
    """Calculate popularity — Enable popularity metrics generated using mined data."""
    pricing_model: str = Field("on-demand", alias="pricing-model")
    """Pricing Model — Pricing Model configured on BigQuery for running queries"""
    popularity_window_days: float = Field(30, alias="popularity-window-days")
    """Popularity Window (days) — Number of days to consider for calculating popularity. Maximum allowed value is 30."""
    popularity_exclude_user_config: List[Any] = Field(
        [], alias="popularity-exclude-user-config"
    )
    """Excluded Users — List of users who should be excluded while calculating usage metrics for assets"""
    control_config_strategy: str = Field("default", alias="control-config-strategy")
    """Control Config — Controls custom experimental feature flags for the miner"""
    control_config: str = Field("{}", alias="control-config")
    """Custom Config — Custom JSON config controlling experimental feature flags for the miner"""


class BigqueryMiner(AppBuilder):
    """Fluent, UI-equivalent builder for the `bigquery-miner` / `miner` app.

    Example::

        resp = (
            BigqueryMiner(client)
            .connection(qualified_name="default/bigquery/1700000000")
            .start_date(0.0)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "bigquery-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"
    _CONNECTOR_NAME: ClassVar[str] = "bigquery"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _EXTRACTION_METHOD: ClassVar[str] = "query_history"
    _INPUTS_CLASS = BigqueryMinerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {
        "chunk_interval_hours": 0,
        "enable_continue_as_new": False,
        "max_concurrent_activities": 50,
        "max_activities_per_execution": 300,
        "schedule_to_start_timeout_secs": 10800,
        "sql_pandas_batch_size": 6000,
    }

    # ── Step 3 · Metadata ──
    def start_date(self, value: float) -> "BigqueryMiner":
        """Start date"""
        self._metadata["miner-start-time-epoch"] = value
        return self

    def region(self, value: Literal["default", "custom"]) -> "BigqueryMiner":
        """Region — Set the default region used by the BigQuery Miner. Defaults to `region-us` if unspecified."""
        self._metadata["region-strategy"] = value
        return self

    def custom_big_query_region(self, value: str) -> "BigqueryMiner":
        """Custom BigQuery Region — The miner works in a single region by default. Defaults to `region-us` if unspecified."""
        self._metadata["region"] = value
        return self

    def fetch_excluded_projects_query_history(
        self, enabled: bool = True
    ) -> "BigqueryMiner":
        """Fetch excluded project's QUERY_HISTORY — Enable this if you want to bring-in queries from excluded database/project. If unsure, don't enable this."""
        self._metadata["fetch-all-projects-query-history"] = enabled
        return self

    def calculate_popularity(self, value: Literal["true", "false"]) -> "BigqueryMiner":
        """Calculate popularity — Enable popularity metrics generated using mined data."""
        self._metadata["calculate-popularity"] = value
        return self

    def pricing_model(
        self, value: Literal["on-demand", "flat-rate"]
    ) -> "BigqueryMiner":
        """Pricing Model — Pricing Model configured on BigQuery for running queries"""
        self._metadata["pricing-model"] = value
        return self

    def popularity_window_days(self, value: float) -> "BigqueryMiner":
        """Popularity Window (days) — Number of days to consider for calculating popularity. Maximum allowed value is 30."""
        self._metadata["popularity-window-days"] = value
        return self

    def excluded_users(self, value: List[Any]) -> "BigqueryMiner":
        """Excluded Users — List of users who should be excluded while calculating usage metrics for assets"""
        self._metadata["popularity-exclude-user-config"] = value
        return self

    def control_config(self, value: Literal["default", "custom"]) -> "BigqueryMiner":
        """Control Config — Controls custom experimental feature flags for the miner"""
        self._metadata["control-config-strategy"] = value
        return self

    def custom_config(self, value: str) -> "BigqueryMiner":
        """Custom Config — Custom JSON config controlling experimental feature flags for the miner"""
        self._metadata["control-config"] = value
        return self


__all__ = ["BigqueryMiner", "BigqueryMinerInputs"]
