# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
from unittest.mock import Mock

from pyatlan.model.apps import KafkaConfluent, KafkaConfluentInputs


def test_kafka_confluent_inputs_defaults():
    i = KafkaConfluentInputs()
    assert KafkaConfluentInputs._APP_ID == "Kafka-confluent"
    assert KafkaConfluentInputs._ENTRYPOINT == "confluent"
    assert i.skip_internal_topics is True
    assert i.exclude_filter == ""
    assert i.include_filter == ""
    assert i.preflight_check == ""
    assert i.include_cloud_metrics is None
    assert i.include_connect_lineage is None


def test_kafka_confluent_builder_payload():
    out = (
        KafkaConfluent(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "confluent-kafka"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert "include_cloud_metrics" not in out
    assert "include_connect_lineage" not in out


def test_kafka_confluent_cloud_toggles():
    out = (
        KafkaConfluent(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .include_cloud_metrics(False)
        .include_connect_lineage(True)
        .preview()
    )
    assert out["include_cloud_metrics"] == "false"
    assert out["include_connect_lineage"] == "true"


def test_kafka_confluent_credential_basic():
    b = KafkaConfluent(Mock()).basic(
        username="x",
        password="x",
        security_protocol="x",
        include_schema_registry="x",
        host="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
    assert "enableCloudApi" not in cred.extras
    assert "includeCloudMetrics" not in cred.extras


def test_kafka_confluent_credential_cloud_api():
    b = KafkaConfluent(Mock()).basic(
        username="x",
        password="x",
        security_protocol="x",
        enable_cloud_api=True,
        include_cloud_metrics="true",
        include_schema_registry="x",
        host="x",
    )
    cred = next(iter(b._raw_creds.values()))
    assert cred.extras["enableCloudApi"] == "true"
    assert cred.extras["includeCloudMetrics"] == "true"


def test_kafka_confluent_credential_cloud_api_off():
    b = KafkaConfluent(Mock()).basic(
        username="x",
        password="x",
        security_protocol="x",
        enable_cloud_api=False,
        include_schema_registry="x",
        host="x",
    )
    cred = next(iter(b._raw_creds.values()))
    assert cred.extras["enableCloudApi"] == "false"
