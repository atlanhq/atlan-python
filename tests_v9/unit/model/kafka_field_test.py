# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for KafkaField model in pyatlan_v9.

The parity tests use the exact qualifiedNames atlan-kafka-app emits today
(``{connectionQN}/topic/{topicName}/field/{field_path}``, ``kafka_fields.yaml``),
where nested fields use the full dotted ``field_path``, so a creator change
that would re-key existing fields fails here.
"""

import pytest

from pyatlan_v9.model import KafkaField

CONNECTION_QUALIFIED_NAME = "default/apache-kafka/1770801720"
TOPIC_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/topic/orders"
FIELD_NAME = "address.city"
FIELD_QUALIFIED_NAME = f"{TOPIC_QUALIFIED_NAME}/field/{FIELD_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-kafka-app's kafka_fields transform for a top-level field."""
    sut = KafkaField.creator(
        name="order_id",
        kafka_topic_qualified_name="default/apache-kafka/1770801720/topic/orders",
    )

    assert (
        sut.qualified_name
        == "default/apache-kafka/1770801720/topic/orders/field/order_id"
    )
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_for_nested_field():
    """Mirror atlan-kafka-app's kafka_fields transform for a nested field."""
    sut = KafkaField.creator(
        name="customer.address.city",
        kafka_topic_qualified_name="default/apache-kafka/1770801720/topic/orders",
        parent_field_path="customer.address",
    )

    assert (
        sut.qualified_name
        == "default/apache-kafka/1770801720/topic/orders/field/customer.address.city"
    )
    assert (
        sut.kafka_parent_field_qualified_name
        == "default/apache-kafka/1770801720/topic/orders/field/customer.address"
    )
    assert sut.kafka_parent_field_name == "customer.address"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, topic_qualified_name, parent_field_path, message",
    [
        (None, TOPIC_QUALIFIED_NAME, None, "name is required"),
        (" ", TOPIC_QUALIFIED_NAME, None, "name cannot be blank"),
        (FIELD_NAME, None, None, "kafka_topic_qualified_name is required"),
        (FIELD_NAME, " ", None, "kafka_topic_qualified_name cannot be blank"),
        (
            FIELD_NAME,
            CONNECTION_QUALIFIED_NAME,
            None,
            "kafka_topic_qualified_name is invalid",
        ),
        (
            FIELD_NAME,
            f"{CONNECTION_QUALIFIED_NAME}/cluster/orders",
            None,
            "kafka_topic_qualified_name is invalid",
        ),
        (FIELD_NAME, TOPIC_QUALIFIED_NAME, "customer", "parent_field_path is invalid"),
        (FIELD_NAME, TOPIC_QUALIFIED_NAME, FIELD_NAME, "parent_field_path is invalid"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, topic_qualified_name: str, parent_field_path: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        KafkaField.creator(
            name=name,
            kafka_topic_qualified_name=topic_qualified_name,
            parent_field_path=parent_field_path,
        )


def test_creator():
    """Test creator derives the connection from the topic."""
    sut = KafkaField.creator(
        name=FIELD_NAME, kafka_topic_qualified_name=TOPIC_QUALIFIED_NAME
    )

    assert sut.name == FIELD_NAME
    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.kafka_topic_qualified_name == TOPIC_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "apache-kafka"
    assert sut.kafka_topic.unique_attributes == {"qualifiedName": TOPIC_QUALIFIED_NAME}
    assert not sut.kafka_parent_field_qualified_name
    assert not sut.kafka_parent_field_name
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit connection qualified name."""
    sut = KafkaField.creator(
        name=FIELD_NAME,
        kafka_topic_qualified_name=TOPIC_QUALIFIED_NAME,
        parent_field_path="address",
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "apache-kafka"
    assert (
        sut.kafka_parent_field_qualified_name == f"{TOPIC_QUALIFIED_NAME}/field/address"
    )
    assert sut.kafka_parent_field_name == "address"


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, FIELD_NAME, "qualified_name is required"),
        (FIELD_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        KafkaField.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a KafkaField for modification."""
    sut = KafkaField.updater(qualified_name=FIELD_QUALIFIED_NAME, name=FIELD_NAME)

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.name == FIELD_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = KafkaField.updater(
        qualified_name=FIELD_QUALIFIED_NAME, name=FIELD_NAME
    ).trim_to_required()

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.name == FIELD_NAME
