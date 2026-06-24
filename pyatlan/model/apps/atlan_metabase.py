# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class AtlanMetabaseInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-metabase` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-metabase"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_collections: Dict[str, Any] = Field({}, alias="include-collections")
    """Include collections"""
    exclude_collections: Dict[str, Any] = Field({}, alias="exclude-collections")
    """Exclude collections"""


class AtlanMetabase(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-metabase` app.

    Example::

        resp = (
            AtlanMetabase(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_collections(...)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-metabase"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "metabase"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-metabase"
    _INPUTS_CLASS = AtlanMetabaseInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self, *, username: str, password: str, port: Optional[int] = None, **extra: Any
    ) -> "AtlanMetabase":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="basic",
            username=username,
            password=password,
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def include_collections(self, value: Dict[str, Any]) -> "AtlanMetabase":
        """Include collections"""
        self._metadata["include-collections"] = value
        return self

    def exclude_collections(self, value: Dict[str, Any]) -> "AtlanMetabase":
        """Exclude collections"""
        self._metadata["exclude-collections"] = value
        return self


__all__ = ["AtlanMetabase", "AtlanMetabaseInputs"]
