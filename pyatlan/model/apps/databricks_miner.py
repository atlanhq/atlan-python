# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401


from ._base import AppBuilder, AppInput, _anchor_filter  # noqa: F401


class DatabricksMinerInputs(AppInput):
    """Typed, UI-facing inputs for the `databricks-miner` / `miner` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "databricks-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    extract_strategy: str = Field("system-table", alias="extract-strategy")
    """Lineage Extraction Method — Determines the method used to fetch the lineage. `System Table` reads lineage from `system.access.*`. `Offline` skips extraction (used when lineage is pre-computed upstream)."""
    extraction_catalog_type_lineage: str = Field(
        "system-table", alias="extraction-catalog-type-lineage"
    )
    """Extraction Catalog Type — Select the catalog to use for extraction. By default uses 'system' catalog and 'access' schema. To use cloned catalog, select 'Cloned Catalog'."""
    cloned_catalog_name_lineage: str = Field(
        "system", alias="cloned-catalog-name-lineage"
    )
    """Cloned Catalog Name — Name of the catalog that contains the cloned schema for lineage"""
    cloned_schema_name_lineage: str = Field(
        "access", alias="cloned-schema-name-lineage"
    )
    """Cloned Schema Name — Name of the schema that contains the cloned tables for lineage"""
    sql_warehouse: str = Field("", alias="sql-warehouse")
    """SQL Warehouse ID — Warehouse ID used by Statement Execution API for lineage extraction."""
    path_level_lineage: str = Field("false", alias="path-level-lineage")
    """Enable File Path Lineage — Control lineage tracking at the file-path level for volumes and external locations."""
    calculate_popularity: str = Field("false", alias="calculate-popularity")
    """Fetch Query History and Calculate Popularity — Aggregate query-history counts into popularity scores. Requires `system.access.query_history`."""
    extraction_catalog_type_popularity: str = Field(
        "system-table", alias="extraction-catalog-type-popularity"
    )
    """Extraction Catalog for Popularity — Select the catalog to use for popularity extraction. By default uses 'system' catalog and 'query' schema. To use cloned catalog, select 'Cloned Catalog'."""
    cloned_catalog_name_popularity: str = Field(
        "system", alias="cloned-catalog-name-popularity"
    )
    """Cloned Catalog Name for Popularity — Name of the catalog that contains the cloned schema for popularity"""
    cloned_schema_name_popularity: str = Field(
        "query", alias="cloned-schema-name-popularity"
    )
    """Cloned Schema Name for Popularity — Name of the schema that contains the cloned tables for popularity"""
    popularity_window_days: float = Field(30, alias="popularity-window-days")
    """Popularity Window (days) — Lookback window in days for popularity computation. 30 = last month."""
    popularity_exclude_user_config: List[Any] = Field(
        [], alias="popularity-exclude-user-config"
    )
    """Excluded Users — List of users whose queries should be excluded while calculating usage metrics for assets."""
    miner_start_time_epoch: float = Field(0, alias="miner-start-time-epoch")
    """Start Date — Queries from this date onwards are fetched for Query History mining and popularity calculation. This does not change lineage extraction."""
    sql_warehouse_popularity: str = Field("", alias="sql-warehouse-popularity")
    """SQL Warehouse ID — Warehouse ID used by Statement Execution API for popularity extraction."""


class DatabricksMiner(AppBuilder):
    """Fluent, UI-equivalent builder for the `databricks-miner` / `miner` app.

    Example::

        resp = (
            DatabricksMiner(client)
            .connection(qualified_name="default/databricks/1700000000")
            .lineage_extraction_method('system-table')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "databricks-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"
    _CONNECTOR_NAME: ClassVar[str] = "databricks"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _INPUTS_CLASS = DatabricksMinerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {
        "miner_lookback_days": 30,
        "miner_chunk_interval_hours": 0,
        "miner_max_concurrent_activities": 20,
        "miner_wave_size": 50,
        "miner_wave_concurrency": 10,
        "preflight_context": "miner",
    }

    # ── Step 3 · Metadata ──
    def lineage_extraction_method(
        self, value: Literal["system-table", "offline"]
    ) -> "DatabricksMiner":
        """Lineage Extraction Method — Determines the method used to fetch the lineage. `System Table` reads lineage from `system.access.*`. `Offline` skips extraction (used when lineage is pre-computed upstream)."""
        self._metadata["extract-strategy"] = value
        return self

    def extraction_catalog_type(
        self, value: Literal["system-table", "cloned-schema"]
    ) -> "DatabricksMiner":
        """Extraction Catalog Type — Select the catalog to use for extraction. By default uses 'system' catalog and 'access' schema. To use cloned catalog, select 'Cloned Catalog'."""
        self._metadata["extraction-catalog-type-lineage"] = value
        return self

    def cloned_catalog_name(self, value: str) -> "DatabricksMiner":
        """Cloned Catalog Name — Name of the catalog that contains the cloned schema for lineage"""
        self._metadata["cloned-catalog-name-lineage"] = value
        return self

    def cloned_schema_name(self, value: str) -> "DatabricksMiner":
        """Cloned Schema Name — Name of the schema that contains the cloned tables for lineage"""
        self._metadata["cloned-schema-name-lineage"] = value
        return self

    def sql_warehouse_id(self, value: str) -> "DatabricksMiner":
        """SQL Warehouse ID — Warehouse ID used by Statement Execution API for lineage extraction."""
        self._metadata["sql-warehouse"] = value
        return self

    def enable_file_path_lineage(
        self, value: Literal["false", "true"]
    ) -> "DatabricksMiner":
        """Enable File Path Lineage — Control lineage tracking at the file-path level for volumes and external locations."""
        self._metadata["path-level-lineage"] = value
        return self

    def fetch_query_history_and_calculate_popularity(
        self, value: Literal["false", "true"]
    ) -> "DatabricksMiner":
        """Fetch Query History and Calculate Popularity — Aggregate query-history counts into popularity scores. Requires `system.access.query_history`."""
        self._metadata["calculate-popularity"] = value
        return self

    def extraction_catalog_for_popularity(
        self, value: Literal["system-table", "cloned-schema"]
    ) -> "DatabricksMiner":
        """Extraction Catalog for Popularity — Select the catalog to use for popularity extraction. By default uses 'system' catalog and 'query' schema. To use cloned catalog, select 'Cloned Catalog'."""
        self._metadata["extraction-catalog-type-popularity"] = value
        return self

    def cloned_catalog_name_for_popularity(self, value: str) -> "DatabricksMiner":
        """Cloned Catalog Name for Popularity — Name of the catalog that contains the cloned schema for popularity"""
        self._metadata["cloned-catalog-name-popularity"] = value
        return self

    def cloned_schema_name_for_popularity(self, value: str) -> "DatabricksMiner":
        """Cloned Schema Name for Popularity — Name of the schema that contains the cloned tables for popularity"""
        self._metadata["cloned-schema-name-popularity"] = value
        return self

    def popularity_window_days(self, value: float) -> "DatabricksMiner":
        """Popularity Window (days) — Lookback window in days for popularity computation. 30 = last month."""
        self._metadata["popularity-window-days"] = value
        return self

    def excluded_users(self, value: List[Any]) -> "DatabricksMiner":
        """Excluded Users — List of users whose queries should be excluded while calculating usage metrics for assets."""
        self._metadata["popularity-exclude-user-config"] = value
        return self

    def start_date(self, value: float) -> "DatabricksMiner":
        """Start Date — Queries from this date onwards are fetched for Query History mining and popularity calculation. This does not change lineage extraction."""
        self._metadata["miner-start-time-epoch"] = value
        return self

    def set_sql_warehouse_popularity(self, value: str) -> "DatabricksMiner":
        """SQL Warehouse ID — Warehouse ID used by Statement Execution API for popularity extraction."""
        self._metadata["sql-warehouse-popularity"] = value
        return self


__all__ = ["DatabricksMiner", "DatabricksMinerInputs"]
