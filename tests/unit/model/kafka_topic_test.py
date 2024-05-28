import pytest

from pyatlan.model.assets import KafkaTopic
from pyatlan.model.enums import AtlanConnectorType
from tests.unit.model.constants import (
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
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        KafkaTopic.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    topic = KafkaTopic.creator(
        name=KAFKA_TOPIC_NAME,
        connection_qualified_name=KAFKA_CONNECTION_QUALIFIED_NAME,
    )

    assert topic.name == KAFKA_TOPIC_NAME
    assert topic.qualified_name == KAFKA_TOPIC_QUALIFIED_NAME
    assert topic.connector_name == AtlanConnectorType.KAFKA
    assert topic.connection_qualified_name == KAFKA_CONNECTION_QUALIFIED_NAME


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
    with pytest.raises(ValueError, match=message):
        KafkaTopic.updater(qualified_name=qualified_name, name=name)


def test_updater():
    topic = KafkaTopic.updater(
        name=KAFKA_TOPIC_NAME, qualified_name=KAFKA_TOPIC_QUALIFIED_NAME
    )
    assert topic.name == KAFKA_TOPIC_NAME
    assert topic.qualified_name == KAFKA_TOPIC_QUALIFIED_NAME


def test_trim_to_required():
    topic = KafkaTopic.updater(
        name=KAFKA_TOPIC_NAME,
        qualified_name=KAFKA_CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert topic.name == KAFKA_TOPIC_NAME
    assert topic.qualified_name == KAFKA_CONNECTION_QUALIFIED_NAME
