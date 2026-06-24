# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import KafkaApache, KafkaApacheInputs


def test_kafka_apache_inputs_defaults():
    i = KafkaApacheInputs()
    assert KafkaApacheInputs._APP_ID == "Kafka-apache"
    assert KafkaApacheInputs._ENTRYPOINT == "apache"
    assert i.skip_internal_topics is True
    assert i.exclude_filter == ""
    assert i.include_filter == ""
    assert i.preflight_check == ""


def test_kafka_apache_builder_payload():
    out = (
        KafkaApache(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "apache-kafka"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_kafka_apache_credential_noauth():
    b = KafkaApache(Mock()).noauth(
        security_protocol="x", include_schema_registry="x", host="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_kafka_apache_credential_basic():
    b = KafkaApache(Mock()).basic(
        username="x",
        password="x",
        security_protocol="x",
        include_schema_registry="x",
        host="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_kafka_apache_credential_scram():
    b = KafkaApache(Mock()).scram(
        username="x",
        password="x",
        security_protocol="x",
        sasl_mechanism="x",
        include_schema_registry="x",
        host="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_kafka_apache_credential_mtls():
    b = KafkaApache(Mock()).mtls(mtls_cert="x", include_schema_registry="x", host="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
