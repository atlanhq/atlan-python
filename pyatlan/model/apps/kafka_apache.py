# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, List, Literal, Mapping, Optional, Union  # noqa: F401

from pydantic.v1 import Field  # noqa: F401

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput, _anchor_filter  # noqa: F401


class KafkaApacheInputs(AppInput):
    """Typed, UI-facing inputs for the `Kafka-apache` / `apache` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "Kafka-apache"
    _ENTRYPOINT: ClassVar[Optional[str]] = "apache"

    # Step 1 · Credential / Connection plumbing
    connection: Optional[Any] = None
    extraction_method: str = "direct"
    credential_guid: Optional[str] = None
    agent_json: Optional[Any] = None

    # Step 3 · Metadata (only fields the UI surfaces)
    skip_internal_topics: bool = Field(True, alias="skip-internal-topics")
    """Skip internal topics — Skip Kafka's internal topics (e.g. __consumer_offsets, _schemas etc). This takes priority over other filters."""
    exclude_filter: str = Field("", alias="exclude-filter")
    """Exclude topic regex — Regex of kafka topics to ignore. By default, nothing will be excluded. This takes priority over include regex."""
    include_filter: str = Field("", alias="include-filter")
    """Include topic regex — Regex of kafka topics to include.  By default, everything will be included."""
    preflight_check: str = Field("", alias="preflight-check")


class KafkaApache(AppBuilder):
    """Fluent, UI-equivalent builder for the `Kafka-apache` / `apache` app.

    Example::

        resp = (
            KafkaApache(client)
            .noauth(security_protocol="...", include_schema_registry="...")
            .connection(name="my-connection", admins=["jdoe"])
            .skip_internal_topics(True)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "Kafka-apache"
    _ENTRYPOINT: ClassVar[Optional[str]] = "apache"
    _CONNECTOR_NAME: ClassVar[str] = "apache-kafka"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-apache-kafka"
    _INPUTS_CLASS = KafkaApacheInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def noauth(
        self,
        *,
        security_protocol: str,
        include_schema_registry: str,
        schema_registry_host: Optional[str] = None,
        schema_registry_username: Optional[str] = None,
        schema_registry_password: Optional[str] = None,
        **extra: Any,
    ) -> "KafkaApache":
        """Direct extraction with noauth auth.

        :param security_protocol: Security protocol.
        :param include_schema_registry: Include Schema Registry.
        :param schema_registry_host: Schema registry host.
        :param schema_registry_username: API Key.
        :param schema_registry_password: API Secret.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["securityProtocol"] = security_protocol
        extras["includeSchemaRegistry"] = include_schema_registry
        if schema_registry_host is not None:
            extras["schemaRegistryHost"] = schema_registry_host
        if schema_registry_username is not None:
            extras["schemaRegistryUsername"] = schema_registry_username
        if schema_registry_password is not None:
            extras["schemaRegistryPassword"] = schema_registry_password
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="noauth",
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        security_protocol: str,
        include_schema_registry: str,
        schema_registry_host: Optional[str] = None,
        schema_registry_username: Optional[str] = None,
        schema_registry_password: Optional[str] = None,
        **extra: Any,
    ) -> "KafkaApache":
        """Direct extraction with basic auth.

        :param username: Username.
        :param password: Password.
        :param security_protocol: Security protocol.
        :param include_schema_registry: Include Schema Registry.
        :param schema_registry_host: Schema registry host.
        :param schema_registry_username: API Key.
        :param schema_registry_password: API Secret.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["securityProtocol"] = security_protocol
        extras["includeSchemaRegistry"] = include_schema_registry
        if schema_registry_host is not None:
            extras["schemaRegistryHost"] = schema_registry_host
        if schema_registry_username is not None:
            extras["schemaRegistryUsername"] = schema_registry_username
        if schema_registry_password is not None:
            extras["schemaRegistryPassword"] = schema_registry_password
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="basic",
            username=username,
            password=password,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def scram(
        self,
        *,
        username: str,
        password: str,
        security_protocol: str,
        sasl_mechanism: str,
        include_schema_registry: str,
        schema_registry_host: Optional[str] = None,
        schema_registry_username: Optional[str] = None,
        schema_registry_password: Optional[str] = None,
        **extra: Any,
    ) -> "KafkaApache":
        """Direct extraction with scram auth.

        :param username: Username.
        :param password: Password.
        :param security_protocol: Security protocol.
        :param sasl_mechanism: SASL Mechanism.
        :param include_schema_registry: Include Schema Registry.
        :param schema_registry_host: Schema registry host.
        :param schema_registry_username: API Key.
        :param schema_registry_password: API Secret.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["securityProtocol"] = security_protocol
        extras["saslMechanism"] = sasl_mechanism
        extras["includeSchemaRegistry"] = include_schema_registry
        if schema_registry_host is not None:
            extras["schemaRegistryHost"] = schema_registry_host
        if schema_registry_username is not None:
            extras["schemaRegistryUsername"] = schema_registry_username
        if schema_registry_password is not None:
            extras["schemaRegistryPassword"] = schema_registry_password
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="scram",
            username=username,
            password=password,
            extra=extras,
        )
        return self

    # ── Step 1 · Credential ──
    def mtls(
        self,
        *,
        key_password: Optional[str] = None,
        mtls_cert: str,
        include_schema_registry: str,
        schema_registry_host: Optional[str] = None,
        schema_registry_username: Optional[str] = None,
        schema_registry_password: Optional[str] = None,
        **extra: Any,
    ) -> "KafkaApache":
        """Direct extraction with mtls auth.

        :param key_password: Key Password.
        :param mtls_cert: Certificates.
        :param include_schema_registry: Include Schema Registry.
        :param schema_registry_host: Schema registry host.
        :param schema_registry_username: API Key.
        :param schema_registry_password: API Secret.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        if key_password is not None:
            extras["key_password"] = key_password
        extras["mtls_cert"] = mtls_cert
        extras["includeSchemaRegistry"] = include_schema_registry
        if schema_registry_host is not None:
            extras["schemaRegistryHost"] = schema_registry_host
        if schema_registry_username is not None:
            extras["schemaRegistryUsername"] = schema_registry_username
        if schema_registry_password is not None:
            extras["schemaRegistryPassword"] = schema_registry_password
        extras.update(extra)
        self._credential = Credential(
            connector_config_name=self._CONNECTOR_CONFIG,
            connector_type=self._CONNECTOR_NAME,
            auth_type="mtls",
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def skip_internal_topics(self, value: bool) -> "KafkaApache":
        """Skip internal topics — Skip Kafka's internal topics (e.g. __consumer_offsets, _schemas etc). This takes priority over other filters."""
        self._metadata["skip-internal-topics"] = value
        return self

    def exclude_topic_regex(self, value: str) -> "KafkaApache":
        """Exclude topic regex — Regex of kafka topics to ignore. By default, nothing will be excluded. This takes priority over include regex."""
        self._metadata["exclude-filter"] = value
        return self

    def include_topic_regex(self, value: str) -> "KafkaApache":
        """Include topic regex — Regex of kafka topics to include.  By default, everything will be included."""
        self._metadata["include-filter"] = value
        return self

    def preflight_check(self, value: str) -> "KafkaApache":
        self._metadata["preflight-check"] = value
        return self


__all__ = ["KafkaApache", "KafkaApacheInputs"]
