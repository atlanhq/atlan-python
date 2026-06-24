# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class AtlanMssqlInputs(AppInput):
    """Typed, UI-facing inputs for the `atlan-mssql` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "atlan-mssql"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    agent_name: str = Field("", alias="agent-name")
    """Agent Name — Name of the offline agent installed on the same network as the database."""
    include_filter: Union[Dict[str, Any], str] = Field("{}", alias="include-filter")
    """Include Metadata"""
    exclude_filter: Union[Dict[str, Any], str] = Field("{}", alias="exclude-filter")
    """Exclude Metadata"""
    temp_table_regex: str = Field("", alias="temp-table-regex")
    """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string."""


class AtlanMssql(AppBuilder):
    """Fluent, UI-equivalent builder for the `atlan-mssql` app.

    Example::

        resp = (
            AtlanMssql(client)
            .basic(username="...", password="...", database="...")
            .connection(name="my-connection", admins=["jdoe"])
            .agent_name("")
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "atlan-mssql"
    _ENTRYPOINT: ClassVar[Optional[str]] = ""
    _CONNECTOR_NAME: ClassVar[str] = "mssql"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-mssql"
    _INPUTS_CLASS = AtlanMssqlInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        database: str,
        enable_ssl: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanMssql":
        """Direct extraction with Basic Authentication auth.

        :param username: Username.
        :param password: Password.
        :param database: Database.
        :param enable_ssl: Encrypt Connection.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["database"] = database
        if enable_ssl is not None:
            extras["__enable_ssl"] = enable_ssl
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="basic",
            username=username,
            password=password,
            host=host or "host",
            port=port or 1433,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def azure_ad_sp(
        self,
        *,
        aad_principal_id: str,
        aad_principal_secret: str,
        tenant_id: str,
        database: str,
        enable_ssl: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanMssql":
        """Direct extraction with Azure AD (Microsoft Entra) auth.

        :param aad_principal_id: Azure AD Principal Application ID.
        :param aad_principal_secret: Azure AD Principal Secret.
        :param tenant_id: Azure AD Tenant ID.
        :param database: Database.
        :param enable_ssl: Encrypt Connection.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["aad_principal_id"] = aad_principal_id
        extras["aad_principal_secret"] = aad_principal_secret
        extras["tenant_id"] = tenant_id
        extras["database"] = database
        if enable_ssl is not None:
            extras["__enable_ssl"] = enable_ssl
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="azure-ad-sp",
            host=host or "host",
            port=port or 1433,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def ntlm(
        self,
        *,
        username: str,
        password: str,
        domain: str,
        database: str,
        enable_ssl: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "AtlanMssql":
        """Direct extraction with Windows (NTLM) auth.

        :param username: Username.
        :param password: Password.
        :param domain: Windows Domain.
        :param database: Database.
        :param enable_ssl: Encrypt Connection.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["domain"] = domain
        extras["database"] = database
        if enable_ssl is not None:
            extras["__enable_ssl"] = enable_ssl
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="ntlm",
            username=username,
            password=password,
            host=host or "host",
            port=port or 1433,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def agent_name(self, value: str) -> "AtlanMssql":
        """Agent Name — Name of the offline agent installed on the same network as the database."""
        self._metadata["agent-name"] = value
        return self

    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanMssql":
        """Include Metadata"""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "AtlanMssql":
        """Exclude Metadata"""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def exclude_regex_for_tables_views(self, value: str) -> "AtlanMssql":
        """Exclude regex for tables & views — Regex of tables & views to ignore. Defaults to empty string."""
        self._metadata["temp-table-regex"] = value
        return self


__all__ = ["AtlanMssql", "AtlanMssqlInputs"]
