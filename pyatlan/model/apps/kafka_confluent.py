# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# Hand-maintained (see _HAND_WRITTEN in the generator): the credential vaults under
# a connector config name (atlan-connectors-kafka-confluent-cloud) that differs from
# the configmap's credentialType, so it can't be derived automatically.
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
    include_cloud_metrics: Optional[str] = Field(None, alias="include-cloud-metrics")
    """Include Cloud Metrics — Collect topic sizes from the Confluent Cloud Metrics API. Unset falls back to the credential's legacy includeCloudMetrics."""
    include_connect_lineage: Optional[str] = Field(
        None, alias="include-connect-lineage"
    )
    """Include Connect Lineage — Build lineage from Confluent Cloud connectors to the tables they read and write."""


class KafkaConfluent(AppBuilder):
    """Fluent, UI-equivalent builder for the `Kafka-confluent` / `confluent` app.

    Example::

        resp = (
            KafkaConfluent(client)
            .basic(username="...", password="...", security_protocol="SASL_SSL", enable_cloud_api=True, cloud_api_key="...", cloud_api_secret="...", cluster_id="...", include_schema_registry="false", host="...")
            .connection(name="my-connection", admin_users=["jdoe"])
            .skip_internal_topics(True)
            .include_cloud_metrics(True)
            .include_connect_lineage(True)
            .run()
        )
    """

    _APP_ID: ClassVar[str] = "Kafka-confluent"
    _ENTRYPOINT: ClassVar[Optional[str]] = "confluent"
    _CONNECTOR_NAME: ClassVar[str] = "confluent-kafka"
    _CONNECTOR_CONFIG: ClassVar[str] = "atlan-connectors-kafka-confluent-cloud"
    _INPUTS_CLASS = KafkaConfluentInputs
    _HIDDEN_DEFAULTS: ClassVar[Dict[str, Any]] = {}

    # ── Step 1 · Credential ──
    def basic(
        self,
        *,
        username: str,
        password: str,
        security_protocol: str,
        enable_cloud_api: Optional[bool] = None,
        include_cloud_metrics: Optional[str] = None,
        cloud_api_key: Optional[str] = None,
        cloud_api_secret: Optional[str] = None,
        cluster_id: Optional[str] = None,
        include_schema_registry: str,
        schema_registry_host: Optional[str] = None,
        schema_registry_username: Optional[str] = None,
        schema_registry_password: Optional[str] = None,
        host: str,
        port: Optional[int] = None,
        **extra: Any,
    ) -> "KafkaConfluent":
        """Direct extraction with basic auth.

        :param username: API Key.
        :param password: API Secret.
        :param security_protocol: Security protocol.
        :param enable_cloud_api: Enable Cloud API, for topic size metrics and Connect lineage.
            Omitted, the app falls back to the legacy ``include_cloud_metrics``.
        :param include_cloud_metrics: Legacy credential toggle, superseded by
            ``enable_cloud_api`` plus the ``include_cloud_metrics()`` workflow setter.
        :param cloud_api_key: Cloud API Key.
        :param cloud_api_secret: Cloud API Secret.
        :param cluster_id: Cluster ID.
        :param include_schema_registry: Include Schema Registry.
        :param schema_registry_host: Schema registry host.
        :param schema_registry_username: API Key.
        :param schema_registry_password: API Secret.
        """
        extras: Dict[str, Any] = {}
        extras["securityProtocol"] = security_protocol
        if enable_cloud_api is not None:
            extras["enableCloudApi"] = "true" if enable_cloud_api else "false"
        if include_cloud_metrics is not None:
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
        return self._stage_credential(
            "credential_guid",
            Credential(
                # The vault registers this connector as kafka-confluent-cloud; the
                # configmap's credentialType (atlan-connectors-confluent-kafka) is a
                # different name the vault can't store ("failed to store credential").
                connector_config_name="atlan-connectors-kafka-confluent-cloud",
                connector_type="confluent-kafka",
                auth_type="basic",
                username=username,
                password=password,
                host=host,
                port=port or 9092,
                extra=extras,
            ),
        )

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

    def include_cloud_metrics(self, value: bool) -> "KafkaConfluent":
        """Include Cloud Metrics — Collect topic sizes from the Confluent Cloud Metrics API. Needs enable_cloud_api on the credential."""
        self._metadata["include-cloud-metrics"] = "true" if value else "false"
        return self

    def include_connect_lineage(self, value: bool) -> "KafkaConfluent":
        """Include Connect Lineage — Build lineage from Confluent Cloud connectors to the tables they read and write. Needs enable_cloud_api on the credential."""
        self._metadata["include-connect-lineage"] = "true" if value else "false"
        return self

    def preflight_check(self, value: str) -> "KafkaConfluent":
        self._metadata["preflight-check"] = value
        return self


__all__ = ["KafkaConfluent", "KafkaConfluentInputs"]
