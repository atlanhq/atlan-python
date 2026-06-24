# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter  # noqa: F401


class AtlanTrinoInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-trino` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-trino"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata"""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata"""


class AtlanTrino(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-trino` app.

    Example::

        resp = (
            AtlanTrino(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_metadata({"my_db": ["my_schema"]})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-trino"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "trino"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-trino"
    _INPUTS_CLASS = AtlanTrinoInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self, *, username: str, password: str, port: Optional[int] = None, **extra: Any
    ) -> "AtlanTrino":
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
            port=port or 8080,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def jwt(
        self, *, jwt_token: str, port: Optional[int] = None, **extra: Any
    ) -> "AtlanTrino":
        """Direct extraction with jwt auth.

        :param jwt_token: JWT Token.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["__jwt_token"] = jwt_token
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="jwt",
            port=port or 8080,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanTrino":
        """Include Metadata"""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanTrino":
        """Exclude Metadata"""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self


__all__ = ["AtlanTrino", "AtlanTrinoInputs"]
