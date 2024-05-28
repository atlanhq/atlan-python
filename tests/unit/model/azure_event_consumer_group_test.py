import pytest

from pyatlan.model.assets import AzureEventHubConsumerGroup
from pyatlan.model.enums import AtlanConnectorType
from tests.unit.model.constants import (
    EVENT_HUB_CONNECTION_QUALIFIED_NAME,
    EVENT_HUB_CONSUMER_GROUP_NAME,
    EVENT_HUB_CONSUMER_GROUP_QUALIFIED_NAME,
    EVENT_HUB_QUALIFIED_NAMES,
)


@pytest.mark.parametrize(
    "name, event_hub_qualified_names, message",
    [
        (None, "event/hub", "name is required"),
        (EVENT_HUB_QUALIFIED_NAMES, None, "event_hub_qualified_names is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, event_hub_qualified_names: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AzureEventHubConsumerGroup.creator(
            name=name, event_hub_qualified_names=event_hub_qualified_names
        )


def test_creator():
    group = AzureEventHubConsumerGroup.creator(
        name=EVENT_HUB_CONSUMER_GROUP_NAME,
        event_hub_qualified_names=EVENT_HUB_QUALIFIED_NAMES,
    )

    assert group.name == EVENT_HUB_CONSUMER_GROUP_NAME
    assert group.connector_name == AtlanConnectorType.AZURE_EVENT_HUB
    assert group.kafka_topic_qualified_names == set(EVENT_HUB_QUALIFIED_NAMES)
    assert group.connection_qualified_name == EVENT_HUB_CONNECTION_QUALIFIED_NAME
    assert group.qualified_name == EVENT_HUB_CONSUMER_GROUP_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, EVENT_HUB_CONSUMER_GROUP_NAME, "qualified_name is required"),
        (EVENT_HUB_CONSUMER_GROUP_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AzureEventHubConsumerGroup.updater(qualified_name=qualified_name, name=name)


def test_updater():
    group = AzureEventHubConsumerGroup.updater(
        name=EVENT_HUB_CONSUMER_GROUP_NAME,
        qualified_name=EVENT_HUB_CONSUMER_GROUP_QUALIFIED_NAME,
    )

    assert group.name == EVENT_HUB_CONSUMER_GROUP_NAME
    assert group.qualified_name == EVENT_HUB_CONSUMER_GROUP_QUALIFIED_NAME


def test_trim_to_required():
    group = AzureEventHubConsumerGroup.updater(
        name=EVENT_HUB_CONSUMER_GROUP_NAME,
        qualified_name=EVENT_HUB_CONSUMER_GROUP_QUALIFIED_NAME,
    ).trim_to_required()

    assert group.name == EVENT_HUB_CONSUMER_GROUP_NAME
    assert group.qualified_name == EVENT_HUB_CONSUMER_GROUP_QUALIFIED_NAME
