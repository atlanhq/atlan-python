# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter  # noqa: F401


class AtlanAzureEventHubInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-azure-event-hub` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-azure-event-hub"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    metadata_type: str = Field("kafkaandeventhub", alias="metadata-type")
    """Select which metadata to fetch — Select the type of metadata you want to fetch"""
    skip_internal_topics: str = Field("true", alias="skip-internal-topics")
    """Skip internal event hubs — Skip Kafka's internal event hubs (e.g. __consumer_offsets, _schemas etc). This takes priority over other filters."""
    exclude_filter: str = Field("", alias="exclude-filter")
    """Exclude event hubs regex — Regex of Azure event hubs to ignore. By default, nothing will be excluded. This takes priority over include regex."""
    include_filter: str = Field("", alias="include-filter")
    """Include event hubs regex — Regex of Azure event hubs to include.  By default, everything will be included."""


class AtlanAzureEventHub(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-azure-event-hub` app.

    Example::

        resp = (
            AtlanAzureEventHub(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .select_which_metadata_to_fetch('eventhub')
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-azure-event-hub"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "azure-event-hub"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-azure-event-hub"
    _INPUTS_CLASS = AtlanAzureEventHubInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self, *, username: str, password: str, port: Optional[int] = None, **extra: Any
    ) -> "AtlanAzureEventHub":
        """Direct extraction with basic auth.

        :param username: username.
        :param password: Connection string-primary key.
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
            port=port or 9093,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def service_principal(
        self,
        *,
        username: str,
        password: str,
        client_id: str,
        client_secret: str,
        tenant_id: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanAzureEventHub":
        """Direct extraction with IAM Role Authentication auth.

        :param username: username.
        :param client_id: Client ID.
        :param client_secret: Client Secret.
        :param tenant_id: Tenant ID.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["clientID"] = client_id
        extras["clientSecret"] = client_secret
        extras["tenantID"] = tenant_id
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="servicePrincipal",
            username=username,
            password=password,
            port=port or 9093,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def select_which_metadata_to_fetch(
        self, value: Literal["eventhub", "kafkaandeventhub"]
    ) -> "AtlanAzureEventHub":
        """Select which metadata to fetch — Select the type of metadata you want to fetch"""
        self._metadata["metadata-type"] = value
        return self

    def skip_internal_event_hubs(
        self, value: Literal["true", "false"]
    ) -> "AtlanAzureEventHub":
        """Skip internal event hubs — Skip Kafka's internal event hubs (e.g. __consumer_offsets, _schemas etc). This takes priority over other filters."""
        self._metadata["skip-internal-topics"] = value
        return self

    def exclude_event_hubs_regex(self, value: str) -> "AtlanAzureEventHub":
        """Exclude event hubs regex — Regex of Azure event hubs to ignore. By default, nothing will be excluded. This takes priority over include regex."""
        self._metadata["exclude-filter"] = value
        return self

    def include_event_hubs_regex(self, value: str) -> "AtlanAzureEventHub":
        """Include event hubs regex — Regex of Azure event hubs to include.  By default, everything will be included."""
        self._metadata["include-filter"] = value
        return self


__all__ = ["AtlanAzureEventHub", "AtlanAzureEventHubInputs"]
