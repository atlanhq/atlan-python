# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class AnaplanInputs(AppInput):
    """Typed, UI-facing inputs for the `anaplan-anaplan` / `anaplan` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "anaplan-anaplan"
    _ENTRYPOINT: ClassVar[Optional[str]] = "anaplan"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_metadata: Dict[str, Any] = Field({}, alias="include-metadata")
    """Include Metadata"""
    exclude_metadata: Dict[str, Any] = Field({}, alias="exclude-metadata")
    """Exclude Metadata"""
    exclude_empty_modules: bool = Field(False, alias="exclude-empty-modules")
    """Exclude Empty Modules — Exclude modules that have no line items."""
    ingest_system_dimension: str = Field("individual", alias="ingest-system-dimension")
    """Ingest System Dimensions? — Ingest System Dimensions (Time and Versions) as a proxy, individually, or not at all."""


class Anaplan(AppBuilder):
    """Fluent, UI-equivalent builder for the `anaplan-anaplan` / `anaplan` app.

    Example::

        resp = (
            Anaplan(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_metadata({})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "anaplan-anaplan"
    _ENTRYPOINT: ClassVar[Optional[str]] = "anaplan"
    _CONNECTOR_NAME: ClassVar[str] = "anaplan"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-anaplan"
    _INPUTS_CLASS = AnaplanInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self, *, username: str, password: str, host: Optional[str] = None, **extra: Any
    ) -> "Anaplan":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        """
        extras: Dict[str, Any] = {}
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-anaplan",
                connector_type="anaplan",
                auth_type="basic",
                username=username,
                password=password,
                host=host or "",
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def ca_cert(
        self,
        *,
        username: str,
        password: str,
        ca_certificate: str,
        host: Optional[str] = None,
        **extra: Any,
    ) -> "Anaplan":
        """Direct extraction with CA Certificate Authentication auth.

        :param username: Encoded Data.
        :param password: Encoded Signed Data.
        :param ca_certificate: CA Certificate File.
        """
        extras: Dict[str, Any] = {}
        extras["CaCertificate"] = ca_certificate
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-anaplan",
                connector_type="anaplan",
                auth_type="ca_cert",
                username=username,
                password=password,
                host=host or "",
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def include_metadata(self, value: Dict[str, Any]) -> "Anaplan":
        """Include Metadata"""
        self._metadata["include-metadata"] = value
        return self

    def exclude_metadata(self, value: Dict[str, Any]) -> "Anaplan":
        """Exclude Metadata"""
        self._metadata["exclude-metadata"] = value
        return self

    def exclude_empty_modules(self, enabled: bool = True) -> "Anaplan":
        """Exclude Empty Modules — Exclude modules that have no line items."""
        self._metadata["exclude-empty-modules"] = enabled
        return self

    def ingest_system_dimensions(
        self, value: Literal["proxy", "individual", "no"]
    ) -> "Anaplan":
        """Ingest System Dimensions? — Ingest System Dimensions (Time and Versions) as a proxy, individually, or not at all."""
        self._metadata["ingest-system-dimension"] = value
        return self


__all__ = ["Anaplan", "AnaplanInputs"]
