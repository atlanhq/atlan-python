import pytest

from pyatlan.model.assets import AzureEventHub
from pyatlan.model.enums import AtlanConnectorType
from tests.unit.model.constants import (
    EVENT_HUB_CONNECTION_QUALIFIED_NAME,
    EVENT_HUB_NAME,
    EVENT_HUB_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (EVENT_HUB_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AzureEventHub.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    event_hub = AzureEventHub.creator(
        name=EVENT_HUB_NAME,
        connection_qualified_name=EVENT_HUB_CONNECTION_QUALIFIED_NAME,
    )

    assert event_hub.name == EVENT_HUB_NAME
    assert event_hub.qualified_name == EVENT_HUB_QUALIFIED_NAME
    assert event_hub.connector_name == AtlanConnectorType.AZURE_EVENT_HUB
    assert event_hub.connection_qualified_name == EVENT_HUB_CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, EVENT_HUB_QUALIFIED_NAME, "qualified_name is required"),
        (EVENT_HUB_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        AzureEventHub.updater(qualified_name=qualified_name, name=name)


def test_updater():
    event_hub = AzureEventHub.updater(
        name=EVENT_HUB_NAME, qualified_name=EVENT_HUB_QUALIFIED_NAME
    )
    assert event_hub.name == EVENT_HUB_NAME
    assert event_hub.qualified_name == EVENT_HUB_QUALIFIED_NAME


def test_trim_to_required():
    event_hub = AzureEventHub.updater(
        name=EVENT_HUB_NAME,
        qualified_name=EVENT_HUB_CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert event_hub.name == EVENT_HUB_NAME
    assert event_hub.qualified_name == EVENT_HUB_CONNECTION_QUALIFIED_NAME
