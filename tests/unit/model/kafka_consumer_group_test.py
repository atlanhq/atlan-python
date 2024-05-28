import pytest

from pyatlan.model.assets import KafkaConsumerGroup
from pyatlan.model.enums import AtlanConnectorType
from tests.unit.model.constants import (
    KAFKA_CONNECTION_QUALIFIED_NAME,
    KAFKA_CONSUMER_GROUP_NAME,
    KAFKA_CONSUMER_GROUP_QUALIFIED_NAME,
    KAFKA_TOPIC_QUALIFIED_NAMES,
)


@pytest.mark.parametrize(
    "name, kafka_topic_qualified_names, message",
    [
        (None, "kafka/topic", "name is required"),
        (KAFKA_TOPIC_QUALIFIED_NAMES, None, "kafka_topic_qualified_names is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, kafka_topic_qualified_names: str, message: str
):
    with pytest.raises(ValueError, match=message):
        KafkaConsumerGroup.creator(
            name=name, kafka_topic_qualified_names=kafka_topic_qualified_names
        )


def test_creator():
    group = KafkaConsumerGroup.creator(
        name=KAFKA_CONSUMER_GROUP_NAME,
        kafka_topic_qualified_names=KAFKA_TOPIC_QUALIFIED_NAMES,
    )

    assert group.name == KAFKA_CONSUMER_GROUP_NAME
    assert group.connector_name == AtlanConnectorType.KAFKA
    assert group.kafka_topic_qualified_names == set(KAFKA_TOPIC_QUALIFIED_NAMES)
    assert group.connection_qualified_name == KAFKA_CONNECTION_QUALIFIED_NAME
    assert group.qualified_name == KAFKA_CONSUMER_GROUP_QUALIFIED_NAME


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
    with pytest.raises(ValueError, match=message):
        KafkaConsumerGroup.updater(qualified_name=qualified_name, name=name)


def test_updater():
    group = KafkaConsumerGroup.updater(
        name=KAFKA_CONSUMER_GROUP_NAME,
        qualified_name=KAFKA_CONSUMER_GROUP_QUALIFIED_NAME,
    )

    assert group.name == KAFKA_CONSUMER_GROUP_NAME
    assert group.qualified_name == KAFKA_CONSUMER_GROUP_QUALIFIED_NAME


def test_trim_to_required():
    group = KafkaConsumerGroup.updater(
        name=KAFKA_CONSUMER_GROUP_NAME,
        qualified_name=KAFKA_CONSUMER_GROUP_QUALIFIED_NAME,
    ).trim_to_required()

    assert group.name == KAFKA_CONSUMER_GROUP_NAME
    assert group.qualified_name == KAFKA_CONSUMER_GROUP_QUALIFIED_NAME
