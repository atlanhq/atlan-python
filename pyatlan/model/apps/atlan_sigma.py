# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter  # noqa: F401


class AtlanSigmaInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-sigma` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-sigma"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Dict[str, Any] = Field("{}", alias="include-filter")
    """Include Workbooks — Selected workbooks will be extracted."""
    exclude_filter: Dict[str, Any] = Field("{}", alias="exclude-filter")
    """Exclude Workbooks — Selected workbooks will be excluded from extraction."""


class AtlanSigma(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-sigma` app.

    Example::

        resp = (
            AtlanSigma(client)
            .api_token(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_workbooks(...)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-sigma"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "sigma"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-sigma"
    _INPUTS_CLASS = AtlanSigmaInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {"extraction_method": "direct"}

    # ── Step 1 · Credential ──
    def api_token(
        self,
        *,
        username: str,
        password: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanSigma":
        """Direct extraction with api_token auth.

        :param username: Client ID.
        :param password: API Token.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="api_token",
            username=username,
            password=password,
            host=host or "aws-api.sigmacomputing.com",
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def include_workbooks(self, value: Dict[str, Any]) -> "AtlanSigma":
        """Include Workbooks — Selected workbooks will be extracted."""
        self._metadata["include-filter"] = value
        return self

    def exclude_workbooks(self, value: Dict[str, Any]) -> "AtlanSigma":
        """Exclude Workbooks — Selected workbooks will be excluded from extraction."""
        self._metadata["exclude-filter"] = value
        return self


__all__ = ["AtlanSigma", "AtlanSigmaInputs"]
