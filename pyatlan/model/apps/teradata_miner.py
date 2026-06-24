# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional

from pydantic.v1 import Field

from ._base import AppBuilder, AppInput


class TeradataMinerInputs(AppInput):
    """Typed, UI-facing inputs for the `teradata-miner` / `miner` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "teradata-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    miner_start_time_epoch: str = Field(0, alias="miner-start-time-epoch")
    """Start date — Earliest date (epoch seconds) from which to mine query history. The miner extracts up to two weeks of history. Set 0 to use the full window."""
    advanced_config: str = Field("default", alias="advanced-config")
    """Advanced Config — Set advanced configuration of the miner"""
    cross_connection: str = Field("false", alias="cross-connection")
    """Cross Connection — Enable searching for lineage across all available connections on Atlan instead of the selected connection. Defaults to false."""
    control_config_strategy: str = Field("default", alias="control-config-strategy")
    """Advanced Config — Controls custom experimental feature flags for the miner"""
    control_config: str = Field("", alias="control-config")
    """Custom Config — Custom JSON config controlling experimental feature flags."""


class TeradataMiner(AppBuilder):
    """Fluent, UI-equivalent builder for the `teradata-miner` / `miner` app.

    Example::

        resp = (
            TeradataMiner(client)
            .connection(qualified_name="default/teradata/1700000000")
            .start_date("")
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "teradata-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"
    _CONNECTOR_NAME: ClassVar[str] = "teradata"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _INPUTS_CLASS = TeradataMinerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 3 · Metadata ──
    def start_date(self, value: str) -> "TeradataMiner":
        """Start date — Earliest date (epoch seconds) from which to mine query history. The miner extracts up to two weeks of history. Set 0 to use the full window."""
        self._metadata["miner-start-time-epoch"] = value
        return self

    def advanced_config(self, value: Literal["default", "custom"]) -> "TeradataMiner":
        """Advanced Config — Set advanced configuration of the miner"""
        self._metadata["advanced-config"] = value
        return self

    def cross_connection(self, value: Literal["true", "false"]) -> "TeradataMiner":
        """Cross Connection — Enable searching for lineage across all available connections on Atlan instead of the selected connection. Defaults to false."""
        self._metadata["cross-connection"] = value
        return self

    def set_control_config_strategy(
        self, value: Literal["default", "custom"]
    ) -> "TeradataMiner":
        """Advanced Config — Controls custom experimental feature flags for the miner"""
        self._metadata["control-config-strategy"] = value
        return self

    def custom_config(self, value: str) -> "TeradataMiner":
        """Custom Config — Custom JSON config controlling experimental feature flags."""
        self._metadata["control-config"] = value
        return self


__all__ = ["TeradataMiner", "TeradataMinerInputs"]
