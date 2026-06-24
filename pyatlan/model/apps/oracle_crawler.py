# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class OracleCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the `oracle-crawler` / `crawler` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "oracle-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata — Only the selected databases and schemas will be extracted. Exclude takes precedence over include for shared databases/schemas."""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata — Selected databases and schemas won't be extracted."""
    temp_table_regex: str = Field("", alias="temp-table-regex")
    """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string."""
    advanced_config_strategy: str = Field("default", alias="advanced-config-strategy")
    """Advanced Config — Controls custom experimental features for the crawler."""


class OracleCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for the `oracle-crawler` / `crawler` app.

    Example::

        resp = (
            OracleCrawler(client)
            .basic(username="...", password="...", sid="...", database_name="...", host="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_metadata({"my_db": ["my_schema"]})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "oracle-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "oracle"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-oracle"
    _INPUTS_CLASS = OracleCrawlerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {
        "workflow_type": "crawler",
        "incremental_extraction": "false",
        "system_schema_name": "SYS",
    }

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        sid: str,
        database_name: str,
        protocol: Optional[str] = None,
        oracle_wallet: Optional[str] = None,
        wallet_password: Optional[str] = None,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "OracleCrawler":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        :param sid: SID / Service Name.
        :param database_name: Default Database Name.
        :param protocol: Protocol.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["sid"] = sid
        extras["databaseName"] = database_name
        if protocol is not None:
            extras["protocol"] = protocol
        if oracle_wallet is not None:
            extras["oracleWallet"] = oracle_wallet
        if wallet_password is not None:
            extras["walletPassword"] = wallet_password
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="basic",
            username=username,
            password=password,
            host=host,
            port=port or 1521,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "OracleCrawler":
        """Include Metadata — Only the selected databases and schemas will be extracted. Exclude takes precedence over include for shared databases/schemas."""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "OracleCrawler":
        """Exclude Metadata — Selected databases and schemas won't be extracted."""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def exclude_regex_for_tables_views(self, value: str) -> "OracleCrawler":
        """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string."""
        self._metadata["temp-table-regex"] = value
        return self

    def advanced_config(self, value: Literal["default", "custom"]) -> "OracleCrawler":
        """Advanced Config — Controls custom experimental features for the crawler."""
        self._metadata["advanced-config-strategy"] = value
        return self


__all__ = ["OracleCrawler", "OracleCrawlerInputs"]
