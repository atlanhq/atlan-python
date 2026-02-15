# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for KafkaConsumerGroup model in pyatlan_v9."""

import json

import pytest
from msgspec import UNSET

from pyatlan_v9.models import KafkaConsumerGroup
from tests_v9.unit.model.constants import (
    KAFKA_CONNECTION_QUALIFIED_NAME,
    KAFKA_CONSUMER_GROUP_NAME,
    KAFKA_CONSUMER_GROUP_QUALIFIED_NAME,
    KAFKA_TOPIC_QUALIFIED_NAMES,
)


@pytest.mark.parametrize(
    "name, kafka_topic_qualified_names, message",
    [
        (None, "kafka/topic", "name is required"),
        (KAFKA_CONSUMER_GROUP_NAME, None, "kafka_topic_qualified_names is required"),
    ],
)
def test_creator_with_missing_parameters_raises_value_error(
    name: str, kafka_topic_qualified_names: str, message: str
):
    """Test that creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        KafkaConsumerGroup.creator(
            name=name, kafka_topic_qualified_names=kafka_topic_qualified_names
        )


def test_creator():
    """Test that creator properly initializes a KafkaConsumerGroup with all derived fields."""
    sut = KafkaConsumerGroup.creator(
        name=KAFKA_CONSUMER_GROUP_NAME,
        kafka_topic_qualified_names=KAFKA_TOPIC_QUALIFIED_NAMES,
    )

    assert sut.name == KAFKA_CONSUMER_GROUP_NAME
    assert sut.connector_name == "kafka"
    assert sut.kafka_topic_qualified_names == set(KAFKA_TOPIC_QUALIFIED_NAMES)
    assert sut.connection_qualified_name == KAFKA_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == KAFKA_CONSUMER_GROUP_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, KAFKA_CONSUMER_GROUP_NAME, "qualified_name is required"),
        (KAFKA_CONSUMER_GROUP_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test that updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        KafkaConsumerGroup.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test that updater creates a KafkaConsumerGroup instance for modification."""
    sut = KafkaConsumerGroup.updater(
        name=KAFKA_CONSUMER_GROUP_NAME,
        qualified_name=KAFKA_CONSUMER_GROUP_QUALIFIED_NAME,
    )

    assert sut.name == KAFKA_CONSUMER_GROUP_NAME
    assert sut.qualified_name == KAFKA_CONSUMER_GROUP_QUALIFIED_NAME


def test_trim_to_required():
    """Test that trim_to_required returns a KafkaConsumerGroup with only required fields."""
    sut = KafkaConsumerGroup.updater(
        name=KAFKA_CONSUMER_GROUP_NAME,
        qualified_name=KAFKA_CONSUMER_GROUP_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.name == KAFKA_CONSUMER_GROUP_NAME
    assert sut.qualified_name == KAFKA_CONSUMER_GROUP_QUALIFIED_NAME


def test_basic_construction():
    """Test basic KafkaConsumerGroup construction with minimal parameters."""
    group = KafkaConsumerGroup(
        name=KAFKA_CONSUMER_GROUP_NAME,
        qualified_name=KAFKA_CONSUMER_GROUP_QUALIFIED_NAME,
    )

    assert group.name == KAFKA_CONSUMER_GROUP_NAME
    assert group.qualified_name == KAFKA_CONSUMER_GROUP_QUALIFIED_NAME
    assert group.type_name == "KafkaConsumerGroup"


def test_serialization_to_json_nested(serde):
    """Test serialization to nested JSON format (API format)."""
    group = KafkaConsumerGroup.creator(
        name=KAFKA_CONSUMER_GROUP_NAME,
        kafka_topic_qualified_names=KAFKA_TOPIC_QUALIFIED_NAMES,
    )

    json_str = group.to_json(nested=True, serde=serde)
    data = json.loads(json_str)

    assert data["typeName"] == "KafkaConsumerGroup"
    assert "attributes" in data
    assert data["attributes"]["name"] == KAFKA_CONSUMER_GROUP_NAME


def test_round_trip_serialization(serde):
    """Test that serialization and deserialization preserve all data."""
    original = KafkaConsumerGroup.creator(
        name=KAFKA_CONSUMER_GROUP_NAME,
        kafka_topic_qualified_names=KAFKA_TOPIC_QUALIFIED_NAMES,
    )

    json_str = original.to_json(nested=True, serde=serde)
    restored = KafkaConsumerGroup.from_json(json_str, serde=serde)

    assert restored.name == original.name
    assert restored.qualified_name == original.qualified_name


def test_creator_with_guid():
    """Test that creator initializes a temporary GUID for new assets."""
    group = KafkaConsumerGroup.creator(
        name=KAFKA_CONSUMER_GROUP_NAME,
        kafka_topic_qualified_names=KAFKA_TOPIC_QUALIFIED_NAMES,
    )

    assert group.guid is not UNSET
    assert group.guid is not None
    assert isinstance(group.guid, str)
    assert group.guid.startswith("-")
