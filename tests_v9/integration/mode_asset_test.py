# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    ModeChart,
    ModeCollection,
    ModeQuery,
    ModeReport,
    ModeWorkspace,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("MODE")

WORKSPACE_NAME = f"workspace_{MODULE_NAME}"
REPORT_NAME = f"report_{MODULE_NAME}"


def _mode_token(slug: str) -> str:
    return f"t{slug}{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.MODE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def workspace(
    client: AtlanClient, connection: Connection
) -> Generator[ModeWorkspace, None, None]:
    to_create = ModeWorkspace.creator(
        name=WORKSPACE_NAME,
        mode_token=_mode_token("workspace"),
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=ModeWorkspace)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ModeWorkspace)


@pytest.fixture(scope="module")
def collection(
    client: AtlanClient, workspace: ModeWorkspace
) -> Generator[ModeCollection, None, None]:
    to_create = ModeCollection.creator(
        name=f"collection_{MODULE_NAME}",
        mode_token=_mode_token("collection"),
        mode_workspace_qualified_name=workspace.qualified_name,
        mode_workspace_name=WORKSPACE_NAME,
    )
    result = client.asset.save(to_create).assets_created(asset_type=ModeCollection)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ModeCollection)


@pytest.fixture(scope="module")
def report(
    client: AtlanClient, workspace: ModeWorkspace, collection: ModeCollection
) -> Generator[ModeReport, None, None]:
    to_create = ModeReport.creator(
        name=REPORT_NAME,
        mode_token=_mode_token("report"),
        mode_workspace_qualified_name=workspace.qualified_name,
        mode_workspace_name=WORKSPACE_NAME,
        mode_collection_qualified_names=[collection.qualified_name],
    )
    result = client.asset.save(to_create).assets_created(asset_type=ModeReport)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ModeReport)


@pytest.fixture(scope="module")
def query(client: AtlanClient, report: ModeReport) -> Generator[ModeQuery, None, None]:
    to_create = ModeQuery.creator(
        name=f"query_{MODULE_NAME}",
        mode_token=_mode_token("query"),
        mode_report_qualified_name=report.qualified_name,
        mode_report_name=REPORT_NAME,
        mode_workspace_name=WORKSPACE_NAME,
    )
    result = client.asset.save(to_create).assets_created(asset_type=ModeQuery)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ModeQuery)


@pytest.fixture(scope="module")
def chart(
    client: AtlanClient, report: ModeReport, query: ModeQuery
) -> Generator[ModeChart, None, None]:
    to_create = ModeChart.creator(
        name=f"chart_{MODULE_NAME}",
        mode_token=_mode_token("chart"),
        mode_report_qualified_name=report.qualified_name,
        mode_workspace_name=WORKSPACE_NAME,
        mode_query_qualified_name=query.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=ModeChart)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=ModeChart)


def _assert_retrieved(client, asset, asset_type, connection, qualified_name, slug):
    assert asset.guid
    assert asset.qualified_name == qualified_name
    retrieved = client.asset.get_by_qualified_name(
        qualified_name, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.guid == asset.guid
    assert retrieved.name == asset.name
    assert retrieved.mode_token == _mode_token(slug)
    assert retrieved.connector_name == AtlanConnectorType.MODE
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_workspace(
    client: AtlanClient, connection: Connection, workspace: ModeWorkspace
):
    _assert_retrieved(
        client,
        workspace,
        ModeWorkspace,
        connection,
        f"{connection.qualified_name}/workspaces/{_mode_token('workspace')}",
        "workspace",
    )


def test_collection(
    client: AtlanClient,
    connection: Connection,
    workspace: ModeWorkspace,
    collection: ModeCollection,
):
    retrieved = _assert_retrieved(
        client,
        collection,
        ModeCollection,
        connection,
        f"{workspace.qualified_name}/collections/{_mode_token('collection')}",
        "collection",
    )
    assert retrieved.mode_workspace_qualified_name == workspace.qualified_name
    assert retrieved.mode_workspace_name == WORKSPACE_NAME
    assert retrieved.mode_workspace.guid == workspace.guid


def test_report(
    client: AtlanClient,
    connection: Connection,
    workspace: ModeWorkspace,
    collection: ModeCollection,
    report: ModeReport,
):
    retrieved = _assert_retrieved(
        client,
        report,
        ModeReport,
        connection,
        f"{workspace.qualified_name}/reports/{_mode_token('report')}",
        "report",
    )
    assert retrieved.mode_workspace_qualified_name == workspace.qualified_name
    assert retrieved.mode_workspace_name == WORKSPACE_NAME
    assert [c.guid for c in retrieved.mode_collections] == [collection.guid]


def test_query(
    client: AtlanClient,
    connection: Connection,
    workspace: ModeWorkspace,
    report: ModeReport,
    query: ModeQuery,
):
    retrieved = _assert_retrieved(
        client,
        query,
        ModeQuery,
        connection,
        f"{report.qualified_name}/queries/{_mode_token('query')}",
        "query",
    )
    assert retrieved.mode_workspace_qualified_name == workspace.qualified_name
    assert retrieved.mode_report_qualified_name == report.qualified_name
    assert retrieved.mode_report_name == REPORT_NAME
    assert retrieved.mode_report.guid == report.guid


def test_chart(
    client: AtlanClient,
    connection: Connection,
    workspace: ModeWorkspace,
    report: ModeReport,
    query: ModeQuery,
    chart: ModeChart,
):
    retrieved = _assert_retrieved(
        client,
        chart,
        ModeChart,
        connection,
        f"{report.qualified_name}/charts/{_mode_token('chart')}",
        "chart",
    )
    assert retrieved.mode_workspace_qualified_name == workspace.qualified_name
    assert retrieved.mode_report_qualified_name == report.qualified_name
    assert retrieved.mode_query_qualified_name == query.qualified_name
    assert retrieved.mode_query.guid == query.guid
