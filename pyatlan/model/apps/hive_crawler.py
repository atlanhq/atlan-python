# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter


class HiveCrawlerInputs(AppInput):
    """Typed, UI-facing inputs for the `hive-crawler` / `crawler` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "hive-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"

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
    advanced_config_strategy: str = Field("default", alias="advanced-config-strategy")
    """Advanced Config — Advanced configuration for the workflow. Do not edit if unsure."""
    allow_partial_success: bool = Field(False, alias="allow-partial-success")
    """Allow partial success — Enable this if you are aware of permission limitations and still want Atlan to ingest remaining assets. If unsure, don't enable this."""


class HiveCrawler(AppBuilder):
    """Fluent, UI-equivalent builder for the `hive-crawler` / `crawler` app.

    Example::

        resp = (
            HiveCrawler(client)
            .basic(username="...", password="...")
            .connection(name="my-connection", admins=["jdoe"])
            .include_metadata({"my_db": ["my_schema"]})
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "hive-crawler"
    _ENTRYPOINT: ClassVar[Optional[str]] = "crawler"
    _CONNECTOR_NAME: ClassVar[str] = "hive"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-hive"
    _INPUTS_CLASS = HiveCrawlerInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        default_schema: Optional[str] = None,
        database_name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "HiveCrawler":
        """Direct extraction with Basic Authentication auth.

        :param username: Username.
        :param password: Password.
        """
        extras: Dict[str, Any] = {}
        if default_schema is not None:
            extras["default_schema"] = default_schema
        if database_name is not None:
            extras["databaseName"] = database_name
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-hive",
                connector_type="hive",
                auth_type="basic",
                username=username,
                password=password,
                host=host or "",
                port=port or 10000,
                extra=extras,
            ),
        )

    # ── Step 1 · Credential ──
    def kerberos(
        self,
        *,
        principal: str,
        service_name: str,
        keytab_file: str,
        krb5_conf_file: str,
        kerberos_type: str,
        ca_cert_file: Optional[str] = None,
        client_cert_file: Optional[str] = None,
        client_key_file: Optional[str] = None,
        client_key_passphrase: Optional[str] = None,
        default_schema: Optional[str] = None,
        database_name: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "HiveCrawler":
        """Direct extraction with Kerberos Authentication auth.

        :param principal: Principal.
        :param service_name: Service Name.
        :param keytab_file: Keytab File.
        :param krb5_conf_file: Kerberos Config File (krb5.conf).
        :param kerberos_type: Kerberos Connection Type.
        """
        extras: Dict[str, Any] = {}
        extras["principal"] = principal
        extras["service-name"] = service_name
        extras["keytab-file"] = keytab_file
        extras["krb5-conf-file"] = krb5_conf_file
        extras["kerberos-type"] = kerberos_type
        if ca_cert_file is not None:
            extras["ca_cert-file"] = ca_cert_file
        if client_cert_file is not None:
            extras["client_cert-file"] = client_cert_file
        if client_key_file is not None:
            extras["client_key-file"] = client_key_file
        if client_key_passphrase is not None:
            extras["client_key_passphrase"] = client_key_passphrase
        if default_schema is not None:
            extras["default_schema"] = default_schema
        if database_name is not None:
            extras["databaseName"] = database_name
        extras.update(extra)
        return self._stage_credential(
            "credential_guid",
            Credential(
                connector_config_name="atlan-connectors-hive",
                connector_type="hive",
                auth_type="kerberos",
                host=host or "",
                port=port or 10000,
                extra=extras,
            ),
        )

    # ── Step 3 · Metadata ──
    def include_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "HiveCrawler":
        """Include Metadata"""
        self._metadata["include-filter"] = _anchor_filter(assets)
        return self

    def exclude_metadata(
        self, assets: Union[str, Mapping[str, List[str]]]
    ) -> "HiveCrawler":
        """Exclude Metadata"""
        self._metadata["exclude-filter"] = _anchor_filter(assets)
        return self

    def advanced_config(self, value: Literal["default", "custom"]) -> "HiveCrawler":
        """Advanced Config — Advanced configuration for the workflow. Do not edit if unsure."""
        self._metadata["advanced-config-strategy"] = value
        return self

    def allow_partial_success(self, enabled: bool = True) -> "HiveCrawler":
        """Allow partial success — Enable this if you are aware of permission limitations and still want Atlan to ingest remaining assets. If unsure, don't enable this."""
        self._metadata["allow-partial-success"] = enabled
        return self


__all__ = ["HiveCrawler", "HiveCrawlerInputs"]
