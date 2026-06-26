# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional

from pydantic.v1 import Field

from ._base import AppBuilder, AppInput


class PowerbiMinerInputs(AppInput):
    """Typed, UI-facing inputs for the `powerbi-miner` / `miner` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "powerbi-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    advanced_config: str = Field("default", alias="advanced-config")
    """Advanced Config — Set advanced configuration of the miner"""
    miner_start_timestamp: float = Field(0, alias="miner-start-timestamp")
    """Start date — Earliest date from which to mine activity events. The Power BI API only retains the last 14 days; the default uses that full window."""
    popularity_exclude_user_config: str = Field(
        "", alias="popularity-exclude-user-config"
    )
    """Excluded Users — Comma-separated list of user IDs (typically service accounts) whose activity should not count toward popularity."""


class PowerbiMiner(AppBuilder):
    """Fluent, UI-equivalent builder for the `powerbi-miner` / `miner` app.

    Example::

        resp = (
            PowerbiMiner(client)
            .connection(qualified_name="default/powerbi/1700000000")
            .advanced_config('default')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "powerbi-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"
    _CONNECTOR_NAME: ClassVar[str] = "powerbi"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _INPUTS_CLASS = PowerbiMinerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 3 · Metadata ──
    def advanced_config(self, value: Literal["default", "advanced"]) -> "PowerbiMiner":
        """Advanced Config — Set advanced configuration of the miner"""
        self._metadata["advanced-config"] = value
        return self

    def start_date(self, value: float) -> "PowerbiMiner":
        """Start date — Earliest date from which to mine activity events. The Power BI API only retains the last 14 days; the default uses that full window."""
        self._metadata["miner-start-timestamp"] = value
        return self

    def excluded_users(self, value: str) -> "PowerbiMiner":
        """Excluded Users — Comma-separated list of user IDs (typically service accounts) whose activity should not count toward popularity."""
        self._metadata["popularity-exclude-user-config"] = value
        return self


__all__ = ["PowerbiMiner", "PowerbiMinerInputs"]
