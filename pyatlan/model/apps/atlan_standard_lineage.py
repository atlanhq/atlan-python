# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional

from pydantic.v1 import Field

from ._base import AppBuilder, AppInput
from pyatlan.model.apps._overlays.atlan_standard_lineage import (
    AtlanStandardLineageOverlay,
)


class AtlanStandardLineageInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-standard-lineage` / `standard-lineage` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-standard-lineage"
    _ENTRYPOINT: ClassVar[Optional[str]] = "standard-lineage"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    connector: str = "bigquery"
    """Connector"""
    cross_connection_qualified_names: str = Field(
        "", alias="cross-connection-qualified-names"
    )
    """Connections"""


class AtlanStandardLineage(AtlanStandardLineageOverlay, AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-standard-lineage` / `standard-lineage` app.

    Example::

        resp = (
            AtlanStandardLineage(client)
            .credential_guid("...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .connector('bigquery')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-standard-lineage"
    _ENTRYPOINT: ClassVar[Optional[str]] = "standard-lineage"
    _CONNECTOR_NAME: ClassVar[str] = "standard-lineage"
    _CONNECTOR_CONFIG: ClassVar[str] = ""
    _INPUTS_CLASS = AtlanStandardLineageInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {"run_role": "standard-lineage"}

    # ── Step 3 · Metadata ──
    def connector(self, value: Literal["bigquery"]) -> "AtlanStandardLineage":
        """Connector"""
        self._metadata["connector"] = value
        return self


__all__ = ["AtlanStandardLineage", "AtlanStandardLineageInputs"]
