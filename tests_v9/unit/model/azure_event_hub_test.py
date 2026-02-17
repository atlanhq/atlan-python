# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for AzureEventHub model in pyatlan_v9."""

import pytest

from pyatlan_v9.model import AzureEventHub
from tests_v9.unit.model.constants import (
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
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AzureEventHub.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator initializes expected derived fields."""
    event_hub = AzureEventHub.creator(
        name=EVENT_HUB_NAME,
        connection_qualified_name=EVENT_HUB_CONNECTION_QUALIFIED_NAME,
    )

    assert event_hub.name == EVENT_HUB_NAME
    assert event_hub.qualified_name == EVENT_HUB_QUALIFIED_NAME
    assert event_hub.connector_name == "azure-event-hub"
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
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AzureEventHub.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates AzureEventHub for modification."""
    event_hub = AzureEventHub.updater(
        name=EVENT_HUB_NAME, qualified_name=EVENT_HUB_QUALIFIED_NAME
    )
    assert event_hub.name == EVENT_HUB_NAME
    assert event_hub.qualified_name == EVENT_HUB_QUALIFIED_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    event_hub = AzureEventHub.updater(
        name=EVENT_HUB_NAME,
        qualified_name=EVENT_HUB_CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert event_hub.name == EVENT_HUB_NAME
    assert event_hub.qualified_name == EVENT_HUB_CONNECTION_QUALIFIED_NAME
