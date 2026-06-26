# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class AtlanPrestoInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-presto` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-presto"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata — Select the catalogs and schemas to include in extraction."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata — Select the catalogs and schemas to exclude from extraction."""


class AtlanPresto(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-presto` app.

    Example::

        resp = (
            AtlanPresto(client)
            .basic(username="...", password="...", host="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .include_metadata({"my_db": ["my_schema"]})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-presto"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "presto"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-presto"
    _INPUTS_CLASS = AtlanPrestoInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {"extraction_method": "direct"}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanPresto":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        """
        extras: Dict[str, Any] = {}
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-presto",
                connector_type="presto",
                auth_type="basic",
                username=username,
                password=password,
                host=host,
                port=port or 8080,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanPresto":
        """Include Metadata — Select the catalogs and schemas to include in extraction."""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanPresto":
        """Exclude Metadata — Select the catalogs and schemas to exclude from extraction."""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self


__all__ = ["AtlanPresto", "AtlanPrestoInputs"]
