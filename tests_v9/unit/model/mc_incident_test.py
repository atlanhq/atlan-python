# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for MCIncident model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-monte-carlo-app emits today
(``{connectionQN}/{incidentId}``, transform_incident), so a creator change that
would re-key existing incidents (and alerts, which share the type) fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import MCIncident

CONNECTION_QUALIFIED_NAME = "default/monte-carlo/123456789"
CONNECTOR_NAME = "monte-carlo"
INCIDENT_NAME = "orders freshness breach"
INCIDENT_ID = "9a8b7c6d-incident-id"
INCIDENT_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{INCIDENT_ID}"
MONITOR_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/ui/5f1e2d3c-monitor-id"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-monte-carlo-app's transform_incident inputs and output."""
    sut = MCIncident.creator(
        name="orders freshness breach",
        mc_incident_id="d4e5f6",
        connection_qualified_name="default/monte-carlo/1700000000",
        mc_monitor_qualified_name="default/monte-carlo/1700000000/ui/a1b2c3",
    )

    assert sut.qualified_name == "default/monte-carlo/1700000000/d4e5f6"
    assert sut.mc_monitor.unique_attributes == {
        "qualifiedName": "default/monte-carlo/1700000000/ui/a1b2c3"
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, mc_incident_id, connection_qualified_name, message",
    [
        (None, INCIDENT_ID, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", INCIDENT_ID, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (
            INCIDENT_NAME,
            None,
            CONNECTION_QUALIFIED_NAME,
            "mc_incident_id is required",
        ),
        (
            INCIDENT_NAME,
            " ",
            CONNECTION_QUALIFIED_NAME,
            "mc_incident_id cannot be blank",
        ),
        (INCIDENT_NAME, INCIDENT_ID, None, "connection_qualified_name is required"),
        (
            INCIDENT_NAME,
            INCIDENT_ID,
            " ",
            "connection_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, mc_incident_id: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        MCIncident.creator(
            name=name,
            mc_incident_id=mc_incident_id,
            connection_qualified_name=connection_qualified_name,
        )


@pytest.mark.parametrize(
    "mc_monitor_qualified_name",
    [
        "default/monte-carlo/987654321/ui/5f1e2d3c",  # another connection
        f"{CONNECTION_QUALIFIED_NAME}/5f1e2d3c",  # no namespace segment
        f"{CONNECTION_QUALIFIED_NAME}/ui/5f1e2d3c/extra",
    ],
)
def test_creator_with_invalid_monitor_qualified_name_raises_value_error(
    mc_monitor_qualified_name: str,
):
    """Test creator rejects a monitor qn that is not {conn}/{namespace}/{id}."""
    with pytest.raises(ValueError, match="mc_monitor_qualified_name is invalid"):
        MCIncident.creator(
            name=INCIDENT_NAME,
            mc_incident_id=INCIDENT_ID,
            connection_qualified_name=CONNECTION_QUALIFIED_NAME,
            mc_monitor_qualified_name=mc_monitor_qualified_name,
        )


def test_creator():
    """Test creator sets the incident id, monitor and connection attributes."""
    sut = MCIncident.creator(
        name=INCIDENT_NAME,
        mc_incident_id=INCIDENT_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        mc_monitor_qualified_name=MONITOR_QUALIFIED_NAME,
    )

    assert sut.type_name == "MCIncident"
    assert sut.name == INCIDENT_NAME
    assert sut.mc_incident_id == INCIDENT_ID
    assert sut.qualified_name == INCIDENT_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.mc_monitor.type_name == "MCMonitor"
    assert sut.mc_monitor.unique_attributes == {"qualifiedName": MONITOR_QUALIFIED_NAME}
    assert sut.guid
    sut.validate(for_creation=True)


@pytest.mark.parametrize("mc_monitor_qualified_name", [None, ""])
def test_creator_without_monitor(mc_monitor_qualified_name):
    """The app emits incidents whose monitor it cannot resolve without one."""
    sut = MCIncident.creator(
        name=INCIDENT_NAME,
        mc_incident_id=INCIDENT_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        mc_monitor_qualified_name=mc_monitor_qualified_name,
    )

    assert sut.qualified_name == INCIDENT_QUALIFIED_NAME
    assert sut.mc_monitor is UNSET
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, INCIDENT_NAME, "qualified_name is required"),
        (INCIDENT_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        MCIncident.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an MCIncident for modification."""
    sut = MCIncident.updater(qualified_name=INCIDENT_QUALIFIED_NAME, name=INCIDENT_NAME)

    assert sut.qualified_name == INCIDENT_QUALIFIED_NAME
    assert sut.name == INCIDENT_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = MCIncident.creator(
        name=INCIDENT_NAME,
        mc_incident_id=INCIDENT_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        mc_monitor_qualified_name=MONITOR_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == INCIDENT_QUALIFIED_NAME
    assert sut.name == INCIDENT_NAME
    assert sut.mc_incident_id is UNSET
    assert sut.mc_monitor is UNSET
