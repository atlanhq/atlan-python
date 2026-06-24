# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from ._base import AppBuilder, AppInput


class PostgresMinerInputs(AppInput):
    """Typed, UI-facing inputs for the `postgres-miner` / `miner` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "postgres-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)


class PostgresMiner(AppBuilder):
    """Fluent, UI-equivalent builder for the `postgres-miner` / `miner` app.

    Example::

        resp = (
            PostgresMiner(client)
            .connection(qualified_name="default/postgres/1700000000")
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "postgres-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"
    _CONNECTOR_NAME: ClassVar[str] = "postgres"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _INPUTS_CLASS = PostgresMinerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}


__all__ = ["PostgresMiner", "PostgresMinerInputs"]
