# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for KafkaTopic model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import KafkaTopic
from tests_v9.unit.model.constants import (
    KAFKA_CONNECTION_QUALIFIED_NAME,
    KAFKA_TOPIC_NAME,
    KAFKA_TOPIC_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (KAFKA_TOPIC_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        KafkaTopic.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test that creator properly initializes a KafkaTopic with all derived fields."""
    sut = KafkaTopic.creator(
        name=KAFKA_TOPIC_NAME,
        connection_qualified_name=KAFKA_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == KAFKA_TOPIC_NAME
    assert sut.qualified_name == KAFKA_TOPIC_QUALIFIED_NAME
    assert sut.connector_name == "kafka"
    assert sut.connection_qualified_name == KAFKA_CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, KAFKA_TOPIC_QUALIFIED_NAME, "qualified_name is required"),
        (KAFKA_TOPIC_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        KafkaTopic.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a KafkaTopic instance for modification."""
    sut = KafkaTopic.updater(
        name=KAFKA_TOPIC_NAME, qualified_name=KAFKA_TOPIC_QUALIFIED_NAME
    )

    assert sut.name == KAFKA_TOPIC_NAME
    assert sut.qualified_name == KAFKA_TOPIC_QUALIFIED_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a KafkaTopic with only required fields."""
    sut = KafkaTopic.updater(
        name=KAFKA_TOPIC_NAME,
        qualified_name=KAFKA_CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.name == KAFKA_TOPIC_NAME
    assert sut.qualified_name == KAFKA_CONNECTION_QUALIFIED_NAME


def test_basic_construction():
    """Test basic KafkaTopic construction with minimal parameters."""
    topic = KafkaTopic(name=KAFKA_TOPIC_NAME, qualified_name=KAFKA_TOPIC_QUALIFIED_NAME)

    assert topic.name == KAFKA_TOPIC_NAME
    assert topic.qualified_name == KAFKA_TOPIC_QUALIFIED_NAME
    assert topic.type_name == "KafkaTopic"


def test_unset_fields():
    """Test that optional fields default to UNSET."""
    topic = KafkaTopic(name=KAFKA_TOPIC_NAME, qualified_name=KAFKA_TOPIC_QUALIFIED_NAME)

    assert topic.kafka_topic_compression_type is UNSET
    assert topic.kafka_topic_replication_factor is UNSET


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    topic = KafkaTopic.creator(
        name=KAFKA_TOPIC_NAME,
        connection_qualified_name=KAFKA_CONNECTION_QUALIFIED_NAME,
    )

    json_str = topic.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "KafkaTopic"
    assert "attributes" in data
    assert data["attributes"]["name"] == KAFKA_TOPIC_NAME


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = KafkaTopic.creator(
        name=KAFKA_TOPIC_NAME,
        connection_qualified_name=KAFKA_CONNECTION_QUALIFIED_NAME,
    )

    json_str = original.to_json(nested=True, serde=serde)
    restored = KafkaTopic.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    topic = KafkaTopic.creator(
        name=KAFKA_TOPIC_NAME,
        connection_qualified_name=KAFKA_CONNECTION_QUALIFIED_NAME,
    )

    assert topic.guid is not UNSET
    assert topic.guid is not None
    assert isinstance(topic.guid, str)
    assert topic.guid.startswith("-")
