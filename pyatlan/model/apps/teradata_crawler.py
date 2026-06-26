# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class TeradataCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the `teradata-crawler` / `crawler` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "teradata-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata — Only the selected databases and schemas will be extracted. Exclude gets preference over include for common databases and schemas, if present, in the config."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata — Selected databases and schemas won't be extracted."""
    temp_table_regex: str = Field("", alias="temp-table-regex")
    """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string."""
    advanced_config_strategy: str = Field("default", alias="advanced-config-strategy")
    """Advanced Config — Controls custom experimental features for the crawler"""
    use_source_schema_filtering: str = Field(
        "false", alias="use-source-schema-filtering"
    )
    """Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source. Schemas selected in the include filter will be fetched."""


class TeradataCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for the `teradata-crawler` / `crawler` app.

    Example::

        resp = (
            TeradataCrawler(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .include_metadata({"my_db": ["my_schema"]})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "teradata-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "teradata"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-teradata"
    _INPUTS_CLASS = TeradataCrawlerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "TeradataCrawler":
        """Direct extraction with Basic Authentication auth.

        :param username: Username.
        :param password: Password.
        """
        extras: Dict[str, Any] = {}
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-teradata",
                connector_type="teradata",
                auth_type="basic",
                username=username,
                password=password,
                host=host or "host",
                port=port or 1025,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def ldap(
        self,
        *,
        username: str,
        password: str,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "TeradataCrawler":
        """Direct extraction with LDAP Authentication auth.

        :param username: Username.
        :param password: Password.
        """
        extras: Dict[str, Any] = {}
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-teradata",
                connector_type="teradata",
                auth_type="ldap",
                username=username,
                password=password,
                host=host or "host",
                port=port or 1025,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "TeradataCrawler":
        """Include Metadata — Only the selected databases and schemas will be extracted. Exclude gets preference over include for common databases and schemas, if present, in the config."""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "TeradataCrawler":
        """Exclude Metadata — Selected databases and schemas won't be extracted."""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def exclude_regex_for_tables_views(self, value: str) -> "TeradataCrawler":
        """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string."""
        self._metadata["temp-table-regex"] = value
        return self

    def advanced_config(self, value: Literal["default", "custom"]) -> "TeradataCrawler":
        """Advanced Config — Controls custom experimental features for the crawler"""
        self._metadata["advanced-config-strategy"] = value
        return self

    def enable_source_level_filtering(
        self, value: Literal["true", "false"]
    ) -> "TeradataCrawler":
        """Enable Source Level Filtering — Enable or Disable Schema Level Filtering on source. Schemas selected in the include filter will be fetched."""
        self._metadata["use-source-schema-filtering"] = value
        return self


__all__ = ["TeradataCrawler", "TeradataCrawlerInputs"]
