# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    PowerBIApp,
    PowerBIColumn,
    PowerBIDashboard,
    PowerBIDataflow,
    PowerBIDataflowEntityColumn,
    PowerBIDataset,
    PowerBIDatasource,
    PowerBIMeasure,
    PowerBIPage,
    PowerBIReport,
    PowerBITable,
    PowerBIWorkspace,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("POWERBI")


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.POWERBI
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def assets(client: AtlanClient, connection: Connection) -> Generator[dict, None, None]:
    """Create every Power BI type through its creator, parents first, as the app does."""
    created: dict = {}

    def save(to_create):
        asset_type = type(to_create)
        created[asset_type] = client.asset.save(to_create).assets_created(
            asset_type=asset_type
        )[0]
        return created[asset_type]

    conn_qn = connection.qualified_name
    workspace = save(
        PowerBIWorkspace.creator(
            name=f"ws_{MODULE_NAME}",
            connection_qualified_name=conn_qn,
            workspace_id=f"ws-{MODULE_NAME}",
        )
    )
    dataset = save(
        PowerBIDataset.creator(
            name=f"ds_{MODULE_NAME}",
            workspace_qualified_name=workspace.qualified_name,
            dataset_id="ds-1",
        )
    )
    table = save(
        PowerBITable.creator(
            name=f"table_{MODULE_NAME}",
            dataset_qualified_name=dataset.qualified_name,
        )
    )
    save(
        PowerBIColumn.creator(
            name="column", power_bi_table_qualified_name=table.qualified_name
        )
    )
    save(
        PowerBIMeasure.creator(
            name="measure", power_bi_table_qualified_name=table.qualified_name
        )
    )
    report = save(
        PowerBIReport.creator(
            name=f"report_{MODULE_NAME}",
            workspace_qualified_name=workspace.qualified_name,
            report_id="rp-1",
        )
    )
    save(
        PowerBIPage.creator(
            name="Overview",
            report_qualified_name=report.qualified_name,
            page_id="ReportSection1",
        )
    )
    save(
        PowerBIDashboard.creator(
            name=f"dashboard_{MODULE_NAME}",
            workspace_qualified_name=workspace.qualified_name,
            dashboard_id="db-1",
        )
    )
    dataflow = save(
        PowerBIDataflow.creator(
            name=f"dataflow_{MODULE_NAME}",
            workspace_qualified_name=workspace.qualified_name,
            dataflow_id="df-1",
        )
    )
    save(
        PowerBIDataflowEntityColumn.creator(
            power_bi_dataflow_qualified_name=dataflow.qualified_name,
            entity_name="Customers",
            column_name="Region",
        )
    )
    save(
        PowerBIDatasource.creator(
            name=f"datasource_{MODULE_NAME}",
            connection_qualified_name=conn_qn,
            datasource_id=f"dsrc-{MODULE_NAME}",
        )
    )
    save(
        PowerBIApp.creator(
            name=f"app_{MODULE_NAME}",
            connection_qualified_name=conn_qn,
            app_id=f"app-{MODULE_NAME}",
        )
    )
    yield created
    for asset_type, asset in reversed(list(created.items())):
        delete_asset(client, guid=asset.guid, asset_type=asset_type)


def _retrieve(client: AtlanClient, assets: dict, asset_type, connection, expected_qn):
    retrieved = client.asset.get_by_guid(
        assets[asset_type].guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == expected_qn
    assert retrieved.connector_name == AtlanConnectorType.POWERBI
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_connection_children(client: AtlanClient, connection: Connection, assets: dict):
    conn_qn = connection.qualified_name
    _retrieve(
        client, assets, PowerBIWorkspace, connection, f"{conn_qn}/ws-{MODULE_NAME}"
    )
    _retrieve(
        client, assets, PowerBIDatasource, connection, f"{conn_qn}/dsrc-{MODULE_NAME}"
    )
    app = _retrieve(
        client, assets, PowerBIApp, connection, f"{conn_qn}/app/app-{MODULE_NAME}"
    )
    assert app.power_bi_app_id == f"app-{MODULE_NAME}"


@pytest.mark.parametrize(
    "asset_type, item_id",
    [
        (PowerBIDataset, "ds-1"),
        (PowerBIReport, "rp-1"),
        (PowerBIDashboard, "db-1"),
        (PowerBIDataflow, "df-1"),
    ],
)
def test_workspace_children(
    client: AtlanClient, connection: Connection, assets: dict, asset_type, item_id
):
    ws = assets[PowerBIWorkspace]
    retrieved = _retrieve(
        client, assets, asset_type, connection, f"{ws.qualified_name}/{item_id}"
    )
    assert retrieved.workspace_qualified_name == ws.qualified_name
    assert retrieved.workspace.guid == ws.guid


def test_table_column_and_measure(
    client: AtlanClient, connection: Connection, assets: dict
):
    dataset = assets[PowerBIDataset]
    table = _retrieve(
        client,
        assets,
        PowerBITable,
        connection,
        f"{dataset.qualified_name}/table_{MODULE_NAME}",
    )
    assert table.dataset.guid == dataset.guid
    for asset_type, name in ((PowerBIColumn, "column"), (PowerBIMeasure, "measure")):
        retrieved = _retrieve(
            client, assets, asset_type, connection, f"{table.qualified_name}/{name}"
        )
        assert retrieved.power_bi_table_qualified_name == table.qualified_name
        assert retrieved.dataset_qualified_name == dataset.qualified_name
        assert retrieved.table.guid == table.guid


def test_page(client: AtlanClient, connection: Connection, assets: dict):
    report = assets[PowerBIReport]
    retrieved = _retrieve(
        client,
        assets,
        PowerBIPage,
        connection,
        f"{report.qualified_name}/ReportSection1",
    )
    assert retrieved.report_qualified_name == report.qualified_name
    assert retrieved.report.guid == report.guid


def test_dataflow_entity_column(
    client: AtlanClient, connection: Connection, assets: dict
):
    dataflow = assets[PowerBIDataflow]
    retrieved = _retrieve(
        client,
        assets,
        PowerBIDataflowEntityColumn,
        connection,
        f"{dataflow.qualified_name}/Customers/Region",
    )
    assert retrieved.name == "Customers -> Region"
    assert retrieved.power_bi_dataflow_entity_name == "Customers"
    assert retrieved.power_bi_dataflow.guid == dataflow.guid
