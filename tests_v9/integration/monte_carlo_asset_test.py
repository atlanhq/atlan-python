# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest
from msgspec import UNSET

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, MCIncident, MCMonitor
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("MC")

MONITOR_ID = f"monitor-{MODULE_NAME}"
MONITOR_NAMESPACE = "ui"
INCIDENT_ID = f"incident-{MODULE_NAME}"
ALERT_ID = f"alert-{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.MONTE_CARLO
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def mc_monitor(
    client: AtlanClient, connection: Connection
) -> Generator[MCMonitor, None, None]:
    to_create = MCMonitor.creator(
        name=f"monitor_{MODULE_NAME}",
        mc_monitor_id=MONITOR_ID,
        mc_monitor_namespace=MONITOR_NAMESPACE,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=MCMonitor)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MCMonitor)


@pytest.fixture(scope="module")
def mc_incident(
    client: AtlanClient, connection: Connection, mc_monitor: MCMonitor
) -> Generator[MCIncident, None, None]:
    to_create = MCIncident.creator(
        name=f"incident_{MODULE_NAME}",
        mc_incident_id=INCIDENT_ID,
        connection_qualified_name=connection.qualified_name,
        mc_monitor_qualified_name=mc_monitor.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=MCIncident)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MCIncident)


@pytest.fixture(scope="module")
def mc_alert(
    client: AtlanClient, connection: Connection
) -> Generator[MCIncident, None, None]:
    to_create = MCIncident.creator(
        name=f"alert_{MODULE_NAME}",
        mc_incident_id=ALERT_ID,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=MCIncident)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MCIncident)


def test_mc_monitor(client: AtlanClient, connection: Connection, mc_monitor: MCMonitor):
    assert mc_monitor.guid
    retrieved = client.asset.get_by_qualified_name(
        f"{connection.qualified_name}/{MONITOR_NAMESPACE}/{MONITOR_ID}",
        asset_type=MCMonitor,
    )
    assert retrieved.guid == mc_monitor.guid
    assert retrieved.name == mc_monitor.name
    assert retrieved.mc_monitor_id == MONITOR_ID
    assert retrieved.mc_monitor_namespace == MONITOR_NAMESPACE
    assert retrieved.connector_name == AtlanConnectorType.MONTE_CARLO
    assert retrieved.connection_qualified_name == connection.qualified_name
    retrieved.validate(for_creation=True)


def test_mc_incident(
    client: AtlanClient,
    connection: Connection,
    mc_monitor: MCMonitor,
    mc_incident: MCIncident,
):
    assert mc_incident.guid
    retrieved = client.asset.get_by_qualified_name(
        f"{connection.qualified_name}/{INCIDENT_ID}", asset_type=MCIncident
    )
    assert retrieved.guid == mc_incident.guid
    assert retrieved.name == mc_incident.name
    assert retrieved.mc_incident_id == INCIDENT_ID
    assert retrieved.connector_name == AtlanConnectorType.MONTE_CARLO
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert retrieved.mc_monitor
    assert retrieved.mc_monitor.guid == mc_monitor.guid
    retrieved.validate(for_creation=True)


def test_mc_incident_without_monitor(
    client: AtlanClient, connection: Connection, mc_alert: MCIncident
):
    assert mc_alert.guid
    retrieved = client.asset.get_by_qualified_name(
        f"{connection.qualified_name}/{ALERT_ID}", asset_type=MCIncident
    )
    assert retrieved.guid == mc_alert.guid
    assert retrieved.mc_incident_id == ALERT_ID
    assert retrieved.mc_monitor in (None, UNSET)
    retrieved.validate(for_creation=True)
