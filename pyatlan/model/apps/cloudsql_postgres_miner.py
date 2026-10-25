# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from pydantic.v1 import Field

from ._base import AppBuilder, AppInput


class CloudsqlPostgresMinerInputs(AppInput):
    """Typed, UI-facing inputs for the `cloudsql-postgres-miner` / `miner` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "cloudsql-postgres-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    redact_sql_text: bool = Field(False, alias="redact-sql-text")
    """Redact SQL Text — Replaces string and numeric literals in mined query text with placeholders, in memory, before anything is written to disk. Queries that can't be parsed are kept as-is. Query structure and lineage are preserved. Note: Increases mining runtime."""


class CloudsqlPostgresMiner(AppBuilder):
    """Fluent, UI-equivalent builder for the `cloudsql-postgres-miner` / `miner` app.

    Example::

        resp = (
            CloudsqlPostgresMiner(client)
            .connection(qualified_name="default/cloudsql-postgres/1700000000")
            .redact_sql_text(True)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "cloudsql-postgres-miner"
    _ENTRYPOINT: ClassVar[Optional[str]] = "miner"
    _CONNECTOR_NAME: ClassVar[str] = "cloudsql-postgres"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _EXTRACTION_METHOD: ClassVar[str] = "query_history"
    _INPUTS_CLASS = CloudsqlPostgresMinerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 3 · Metadata ──
    def redact_sql_text(self, enabled: bool = True) -> "CloudsqlPostgresMiner":
        """Redact SQL Text — Replaces string and numeric literals in mined query text with placeholders, in memory, before anything is written to disk. Queries that can't be parsed are kept as-is. Query structure and lineage are preserved. Note: Increases mining runtime."""
        self._metadata["redact-sql-text"] = enabled
        return self


__all__ = ["CloudsqlPostgresMiner", "CloudsqlPostgresMinerInputs"]
