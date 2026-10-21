# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for MCMonitor model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-monte-carlo-app emits today
(``{connectionQN}/{namespace}/{monitorId}``, transform_monitor), so a creator
change that would re-key existing monitors fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import MCMonitor

CONNECTION_QUALIFIED_NAME = "default/monte-carlo/123456789"
CONNECTOR_NAME = "monte-carlo"
MONITOR_NAME = "orders freshness"
MONITOR_ID = "5f1e2d3c-monitor-id"
MONITOR_NAMESPACE = "dbt"
MONITOR_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{MONITOR_NAMESPACE}/{MONITOR_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-monte-carlo-app's transform_monitor inputs and output."""
    sut = MCMonitor.creator(
        name="orders freshness",
        mc_monitor_id="a1b2c3",
        mc_monitor_namespace="ui",
        connection_qualified_name="default/monte-carlo/1700000000",
    )

    assert sut.qualified_name == "default/monte-carlo/1700000000/ui/a1b2c3"
    sut.validate(for_creation=True)


@pytest.mark.parametrize("namespace", [None, ""])
def test_creator_defaults_blank_namespace_to_ui(namespace):
    """A blank namespace matches the app's incident-side `ui` fallback."""
    sut = MCMonitor.creator(
        name=MONITOR_NAME,
        mc_monitor_id=MONITOR_ID,
        mc_monitor_namespace=namespace,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.mc_monitor_namespace == "ui"
    assert sut.qualified_name == f"{CONNECTION_QUALIFIED_NAME}/ui/{MONITOR_ID}"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, mc_monitor_id, connection_qualified_name, message",
    [
        (None, MONITOR_ID, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", MONITOR_ID, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (MONITOR_NAME, None, CONNECTION_QUALIFIED_NAME, "mc_monitor_id is required"),
        (
            MONITOR_NAME,
            " ",
            CONNECTION_QUALIFIED_NAME,
            "mc_monitor_id cannot be blank",
        ),
        (MONITOR_NAME, MONITOR_ID, None, "connection_qualified_name is required"),
        (MONITOR_NAME, MONITOR_ID, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, mc_monitor_id: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        MCMonitor.creator(
            name=name,
            mc_monitor_id=mc_monitor_id,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the monitor id, namespace and connection attributes."""
    sut = MCMonitor.creator(
        name=MONITOR_NAME,
        mc_monitor_id=MONITOR_ID,
        mc_monitor_namespace=MONITOR_NAMESPACE,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.type_name == "MCMonitor"
    assert sut.name == MONITOR_NAME
    assert sut.mc_monitor_id == MONITOR_ID
    assert sut.mc_monitor_namespace == MONITOR_NAMESPACE
    assert sut.qualified_name == MONITOR_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.guid
    sut.validate(for_creation=True)


def test_validate_rejects_qualified_name_without_namespace():
    """The app's `{conn}//{id}` (no namespace) is not a valid creator qn."""
    sut = MCMonitor(
        name=MONITOR_NAME,
        qualified_name=f"{CONNECTION_QUALIFIED_NAME}//{MONITOR_ID}",
    )

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, MONITOR_NAME, "qualified_name is required"),
        (MONITOR_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        MCMonitor.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an MCMonitor for modification."""
    sut = MCMonitor.updater(qualified_name=MONITOR_QUALIFIED_NAME, name=MONITOR_NAME)

    assert sut.qualified_name == MONITOR_QUALIFIED_NAME
    assert sut.name == MONITOR_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = MCMonitor.creator(
        name=MONITOR_NAME,
        mc_monitor_id=MONITOR_ID,
        mc_monitor_namespace=MONITOR_NAMESPACE,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == MONITOR_QUALIFIED_NAME
    assert sut.name == MONITOR_NAME
    assert sut.mc_monitor_id is UNSET
