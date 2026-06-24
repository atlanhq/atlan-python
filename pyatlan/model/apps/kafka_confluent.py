# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from __future__ import annotations

from typing import Any, ClassVar, Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.credential import Credential

from ._base import AppBuilder, AppInput


class KafkaConfluentInputs(AppInput):
    """Typed, UI-facing inputs for the `Kafka-confluent` / `confluent` app (generated from its configmap)."""

    _APP_ID: ClassVar[str] = "Kafka-confluent"
    _ENTRYPOINT: ClassVar[Optional[str]] = "confluent"

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


class KafkaConfluent(AppBuilder):
    """Fluent, UI-equivalent builder for the `Kafka-confluent` / `confluent` app.

    Example::

        resp = (
            KafkaConfluent(client)
            .basic(username="...", password="...", security_protocol="...", include_cloud_metrics="...", include_schema_registry="...", host="...")
            .connection(name="my-connection", admins=["jdoe"])
            .skip_internal_topics(True)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "Kafka-confluent"
    _ENTRYPOINT: ClassVar[Optional[str]] = "confluent"
    _CONNECTOR_NAME: ClassVar[str] = "confluent-kafka"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-confluent-kafka"
    _INPUTS_CLASS = KafkaConfluentInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        security_protocol: str,
        include_cloud_metrics: str,
        cloud_api_key: Optional[str] = None,
        cloud_api_secret: Optional[str] = None,
        cluster_id: Optional[str] = None,
        include_schema_registry: str,
        schema_registry_host: Optional[str] = None,
        schema_registry_username: Optional[str] = None,
        schema_registry_password: Optional[str] = None,
        host: str,
        **extra: Any,
    ) -> "KafkaConfluent":
        """Direct extraction with basic auth.

        :param username: API Key.
        :param password: API Secret.
        :param security_protocol: Security protocol.
        :param include_cloud_metrics: Include Cloud Metrics.
        :param cloud_api_key: Cloud API Key.
        :param cloud_api_secret: Cloud API Secret.
        :param cluster_id: Cluster ID.
        :param include_schema_registry: Include Schema Registry.
        :param schema_registry_host: Schema registry host.
        :param schema_registry_username: API Key.
        :param schema_registry_password: API Secret.
        """
        self._extraction_method = "direct"
        extras: Dict[str, Any] = {}
        extras["securityProtocol"] = security_protocol
        extras["includeCloudMetrics"] = include_cloud_metrics
        if cloud_api_key is not None:
            extras["cloudApiKey"] = cloud_api_key
        if cloud_api_secret is not None:
            extras["cloudApiSecret"] = cloud_api_secret
        if cluster_id is not None:
            extras["clusterId"] = cluster_id
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
            host=host,
            extra=extras,
        )
        return self

    # ── Step 3 · Metadata ──
    def skip_internal_topics(self, value: bool) -> "KafkaConfluent":
        """Skip internal topics — Skip Kafka's internal topics (e.g. __consumer_offsets, _schemas etc). This takes priority over other filters."""
        self._metadata["skip-internal-topics"] = value
        return self

    def exclude_topic_regex(self, value: str) -> "KafkaConfluent":
        """Exclude topic regex — Regex of kafka topics to ignore. By default, nothing will be excluded. This takes priority over include regex."""
        self._metadata["exclude-filter"] = value
        return self

    def include_topic_regex(self, value: str) -> "KafkaConfluent":
        """Include topic regex — Regex of kafka topics to include.  By default, everything will be included."""
        self._metadata["include-filter"] = value
        return self

    def preflight_check(self, value: str) -> "KafkaConfluent":
        self._metadata["preflight-check"] = value
        return self


__all__ = ["KafkaConfluent", "KafkaConfluentInputs"]
