# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
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


def test_kafka_confluent_builder_payload():
    out = (
        KafkaConfluent(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "confluent-kafka"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_kafka_confluent_credential_basic():
    b = KafkaConfluent(Mock()).basic(
        username="x",
        password="x",
        security_protocol="x",
        include_cloud_metrics="x",
        include_schema_registry="x",
        host="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
