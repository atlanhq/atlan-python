# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class MongodbatlasAtlasInputs(AppInput):
    """Typed, UI-facing inputs for the `mongodbatlas-atlas` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "mongodbatlas-atlas"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: str = Field("", alias="include-filter")
    """Include Databases — Comma-separated database name patterns (regex)."""
    exclude_filter: str = Field("", alias="exclude-filter")
    """Exclude Databases — Comma-separated database name patterns (regex). Wins over include."""


class MongodbatlasAtlas(AppBuilder):
    """Fluent, UI-equivalent builder for the `mongodbatlas-atlas` app.

    Example::

        resp = (
            MongodbatlasAtlas(client)
            .basic(username="...", password="...", native_host="...", default_database="...", authsource="...", ssl="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_databases("")
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "mongodbatlas-atlas"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "mongodb"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-mongodb"
    _INPUTS_CLASS = MongodbatlasAtlasInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        native_host: str,
        default_database: str,
        authsource: str,
        ssl: str,
        connection_string: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "MongodbatlasAtlas":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        :param native_host: MongoDB native host.
        :param default_database: Default database.
        :param authsource: Authentication database.
        :param ssl: SSL.
        :param connection_string: Connection string (advanced — overrides above fields).
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["native-host"] = native_host
        extras["default-database"] = default_database
        extras["authsource"] = authsource
        extras["ssl"] = ssl
        if connection_string is not None:
            extras["connection_string"] = connection_string
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="basic",
            username=username,
            password=password,
            port=port or 27017,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def include_databases(self, value: str) -> "MongodbatlasAtlas":
        """Include Databases — Comma-separated database name patterns (regex)."""
        self._metadata["include-filter"] = value
        return self

    def exclude_databases(self, value: str) -> "MongodbatlasAtlas":
        """Exclude Databases — Comma-separated database name patterns (regex). Wins over include."""
        self._metadata["exclude-filter"] = value
        return self


__all__ = ["MongodbatlasAtlas", "MongodbatlasAtlasInputs"]
