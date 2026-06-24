# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Literal, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class AtlanRedashInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-redash` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-redash"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_queries_tags: Dict[str, Any] = Field({}, alias="include-queries-tags")
    """Include queries with tags — Queries having selected tags will be crawled. Exclude gets preference over include."""
    exclude_queries_tags: Dict[str, Any] = Field({}, alias="exclude-queries-tags")
    """Exclude queries with tags — Queries having selected tags will not be crawled."""
    include_dashboards_tags: Dict[str, Any] = Field({}, alias="include-dashboards-tags")
    """Include dashboards with tags — Dashboards having selected tags will be crawled. Exclude gets preference over include."""
    exclude_dashboards_tags: Dict[str, Any] = Field({}, alias="exclude-dashboards-tags")
    """Exclude dashboards with tags — Dashboards having selected tags will not be crawled."""
    advanced_config_strategy: str = Field("default", alias="advanced-config-strategy")
    """Advanced Config — Controls advanced asset inclusion features."""
    include_unpublished_queries: str = Field(
        "true", alias="include-unpublished-queries"
    )
    """Include unpublished queries — Select whether unpublished queries should be fetched."""
    queries_without_tags: str = Field("true", alias="queries-without-tags")
    """Include queries without tags — Include queries that do not have any tags associated to them."""
    dashboards_without_tags: str = Field("true", alias="dashboards-without-tags")
    """Include dashboards without tags — Include dashboards that do not have any tags associated to them."""
    redash_alternate_host: str = Field("", alias="redash-alternate-host")
    """Alternate Host URL — Protocol and host used in the 'View in Redash' link."""


class AtlanRedash(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-redash` app.

    Example::

        resp = (
            AtlanRedash(client)
            .api_key(password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_queries_with_tags(...)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-redash"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "redash"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-redash"
    _INPUTS_CLASS = AtlanRedashInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {"extraction_method": "direct"}

    # ── Step 1 · Credential ──
    def api_key(
        self, *, password: str, port: Optional[int] = None, **extra: Any
    ) -> "AtlanRedash":
        """Direct extraction with api_key auth.

        :param password: API Key.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="api_key",
            password=password,
            port=port or 443,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def include_queries_with_tags(self, value: Dict[str, Any]) -> "AtlanRedash":
        """Include queries with tags — Queries having selected tags will be crawled. Exclude gets preference over include."""
        self._metadata["include-queries-tags"] = value
        return self

    def exclude_queries_with_tags(self, value: Dict[str, Any]) -> "AtlanRedash":
        """Exclude queries with tags — Queries having selected tags will not be crawled."""
        self._metadata["exclude-queries-tags"] = value
        return self

    def include_dashboards_with_tags(self, value: Dict[str, Any]) -> "AtlanRedash":
        """Include dashboards with tags — Dashboards having selected tags will be crawled. Exclude gets preference over include."""
        self._metadata["include-dashboards-tags"] = value
        return self

    def exclude_dashboards_with_tags(self, value: Dict[str, Any]) -> "AtlanRedash":
        """Exclude dashboards with tags — Dashboards having selected tags will not be crawled."""
        self._metadata["exclude-dashboards-tags"] = value
        return self

    def advanced_config(self, value: Literal["default", "custom"]) -> "AtlanRedash":
        """Advanced Config — Controls advanced asset inclusion features."""
        self._metadata["advanced-config-strategy"] = value
        return self

    def include_unpublished_queries(
        self, value: Literal["true", "false"]
    ) -> "AtlanRedash":
        """Include unpublished queries — Select whether unpublished queries should be fetched."""
        self._metadata["include-unpublished-queries"] = value
        return self

    def include_queries_without_tags(
        self, value: Literal["true", "false"]
    ) -> "AtlanRedash":
        """Include queries without tags — Include queries that do not have any tags associated to them."""
        self._metadata["queries-without-tags"] = value
        return self

    def include_dashboards_without_tags(
        self, value: Literal["true", "false"]
    ) -> "AtlanRedash":
        """Include dashboards without tags — Include dashboards that do not have any tags associated to them."""
        self._metadata["dashboards-without-tags"] = value
        return self

    def alternate_host_url(self, value: str) -> "AtlanRedash":
        """Alternate Host URL — Protocol and host used in the 'View in Redash' link."""
        self._metadata["redash-alternate-host"] = value
        return self


__all__ = ["AtlanRedash", "AtlanRedashInputs"]
