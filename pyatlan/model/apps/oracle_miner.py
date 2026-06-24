# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from pydantic.v1 import Field

from ._base import AppBuilder, AppInput


class OracleMinerInputs(AppInput):
    """Typed, UI-facing inputs for the `oracle-miner` / `miner` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "oracle-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    miner_start_time_epoch: float = Field(0, alias="miner-start-time-epoch")
    """Start date — Pick how far back to mine query history. The widget returns a negative-day offset (e.g. -3 = three days ago) which the miner converts to an AWR cutoff timestamp. Mirrors MSSQL v3 miner's date widget."""


class OracleMiner(AppBuilder):
    """Fluent, UI-equivalent builder for the `oracle-miner` / `miner` app.

    Example::

        resp = (
            OracleMiner(client)
            .connection(qualified_name="default/oracle/1700000000")
            .start_date(...)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "oracle-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"
    _CONNECTOR_NAME: ClassVar[str] = "oracle"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _INPUTS_CLASS = OracleMinerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {"workflow_type": "miner"}

    # ── Step 3 · Metadata ──
    def start_date(self, value: float) -> "OracleMiner":
        """Start date — Pick how far back to mine query history. The widget returns a negative-day offset (e.g. -3 = three days ago) which the miner converts to an AWR cutoff timestamp. Mirrors MSSQL v3 miner's date widget."""
        self._metadata["miner-start-time-epoch"] = value
        return self


__all__ = ["OracleMiner", "OracleMinerInputs"]
