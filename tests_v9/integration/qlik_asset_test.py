# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Integration tests for the Qlik Sense creators in pyatlan_v9 (FND-3857).

Creates a Qlik Sense connection, then every Qlik type through its creator, parents
before children, the way atlan-qlik-sense-app links them: a space and a stream, an
app in each, a sheet and a chart under the space's app, a dataset in the space, and
a column under each of the sheet, chart and dataset. Each asset is retrieved by guid
and checked for its exact qualifiedName and parent relationship, then purged.
"""

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    QlikApp,
    QlikChart,
    QlikColumn,
    QlikDataset,
    QlikSheet,
    QlikSpace,
    QlikStream,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("QLIK")

SPACE_ID = f"sp-{MODULE_NAME}"
STREAM_ID = f"st-{MODULE_NAME}"
APP_ID = f"ap-{MODULE_NAME}"
STREAM_APP_ID = f"sa-{MODULE_NAME}"
SHEET_ID = f"sh-{MODULE_NAME}"
CHART_ID = f"ch-{MODULE_NAME}"
DATASET_ID = f"ds-{MODULE_NAME}"
FIELD = f"field_{MODULE_NAME}"


def _save(client: AtlanClient, to_create, asset_type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.QLIKSENSE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def space(
    client: AtlanClient, connection: Connection
) -> Generator[QlikSpace, None, None]:
    to_create = QlikSpace.creator(
        name=f"space_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        qlik_id=SPACE_ID,
    )
    result = _save(client, to_create, QlikSpace)
    yield result
    delete_asset(client, guid=result.guid, asset_type=QlikSpace)


@pytest.fixture(scope="module")
def stream(
    client: AtlanClient, connection: Connection
) -> Generator[QlikStream, None, None]:
    to_create = QlikStream.creator(
        name=f"stream_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        qlik_id=STREAM_ID,
    )
    result = _save(client, to_create, QlikStream)
    yield result
    delete_asset(client, guid=result.guid, asset_type=QlikStream)


@pytest.fixture(scope="module")
def app(client: AtlanClient, space: QlikSpace) -> Generator[QlikApp, None, None]:
    to_create = QlikApp.creator(
        name=f"app_{MODULE_NAME}",
        qlik_id=APP_ID,
        space_qualified_name=space.qualified_name,
    )
    result = _save(client, to_create, QlikApp)
    yield result
    delete_asset(client, guid=result.guid, asset_type=QlikApp)


@pytest.fixture(scope="module")
def stream_app(
    client: AtlanClient, stream: QlikStream
) -> Generator[QlikApp, None, None]:
    to_create = QlikApp.creator(
        name=f"stream_app_{MODULE_NAME}",
        qlik_id=STREAM_APP_ID,
        space_qualified_name=stream.qualified_name,
    )
    result = _save(client, to_create, QlikApp)
    yield result
    delete_asset(client, guid=result.guid, asset_type=QlikApp)


@pytest.fixture(scope="module")
def sheet(
    client: AtlanClient, app: QlikApp, space: QlikSpace
) -> Generator[QlikSheet, None, None]:
    to_create = QlikSheet.creator(
        name=f"sheet_{MODULE_NAME}",
        qlik_id=SHEET_ID,
        app_qualified_name=app.qualified_name,
        space_qualified_name=space.qualified_name,
    )
    result = _save(client, to_create, QlikSheet)
    yield result
    delete_asset(client, guid=result.guid, asset_type=QlikSheet)


@pytest.fixture(scope="module")
def chart(
    client: AtlanClient, sheet: QlikSheet, space: QlikSpace
) -> Generator[QlikChart, None, None]:
    to_create = QlikChart.creator(
        name=f"chart_{MODULE_NAME}",
        qlik_id=CHART_ID,
        sheet_qualified_name=sheet.qualified_name,
        space_qualified_name=space.qualified_name,
    )
    result = _save(client, to_create, QlikChart)
    yield result
    delete_asset(client, guid=result.guid, asset_type=QlikChart)


@pytest.fixture(scope="module")
def dataset(
    client: AtlanClient, space: QlikSpace
) -> Generator[QlikDataset, None, None]:
    to_create = QlikDataset.creator(
        name=f"dataset_{MODULE_NAME}",
        qlik_id=DATASET_ID,
        space_qualified_name=space.qualified_name,
    )
    result = _save(client, to_create, QlikDataset)
    yield result
    delete_asset(client, guid=result.guid, asset_type=QlikDataset)


def _column(client: AtlanClient, parent_qualified_name: str, space_qualified_name):
    to_create = QlikColumn.creator(
        name=FIELD,
        parent_qualified_name=parent_qualified_name,
        space_qualified_name=space_qualified_name,
    )
    return to_create, _save(client, to_create, QlikColumn)


@pytest.fixture(scope="module")
def sheet_column(client: AtlanClient, sheet: QlikSheet, space: QlikSpace):
    to_create, result = _column(client, sheet.qualified_name, space.qualified_name)
    yield to_create, result
    delete_asset(client, guid=result.guid, asset_type=QlikColumn)


@pytest.fixture(scope="module")
def chart_column(client: AtlanClient, chart: QlikChart, space: QlikSpace):
    to_create, result = _column(client, chart.qualified_name, space.qualified_name)
    yield to_create, result
    delete_asset(client, guid=result.guid, asset_type=QlikColumn)


@pytest.fixture(scope="module")
def dataset_column(client: AtlanClient, dataset: QlikDataset, space: QlikSpace):
    to_create, result = _column(client, dataset.qualified_name, space.qualified_name)
    yield to_create, result
    delete_asset(client, guid=result.guid, asset_type=QlikColumn)


def _assert_retrieved(client, asset, asset_type, connection, expected_suffix):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == f"{connection.qualified_name}/{expected_suffix}"
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.QLIKSENSE
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_space(client, connection, space):
    retrieved = _assert_retrieved(
        client, space, QlikSpace, connection, f"space/{SPACE_ID}"
    )
    assert retrieved.qlik_id == SPACE_ID


def test_stream(client, connection, stream):
    retrieved = _assert_retrieved(
        client, stream, QlikStream, connection, f"stream/{STREAM_ID}"
    )
    assert retrieved.qlik_id == STREAM_ID


def test_app(client, connection, space, app):
    retrieved = _assert_retrieved(client, app, QlikApp, connection, f"app/{APP_ID}")
    assert retrieved.qlik_space.guid == space.guid
    assert retrieved.qlik_space_id == SPACE_ID
    assert retrieved.qlik_space_qualified_name == space.qualified_name


def test_app_in_stream(client, connection, stream, stream_app):
    retrieved = _assert_retrieved(
        client, stream_app, QlikApp, connection, f"app/{STREAM_APP_ID}"
    )
    # The app links to the stream itself, not a space with the stream's name.
    assert retrieved.qlik_space.guid == stream.guid
    assert retrieved.qlik_space_qualified_name == stream.qualified_name
    retrieved_stream = client.asset.get_by_guid(
        stream.guid, asset_type=QlikStream, ignore_relationships=False
    )
    assert stream_app.guid in {app.guid for app in retrieved_stream.qlik_apps}


def test_sheet(client, connection, space, app, sheet):
    retrieved = _assert_retrieved(
        client, sheet, QlikSheet, connection, f"app/{APP_ID}/sheet/{SHEET_ID}"
    )
    assert retrieved.qlik_app.guid == app.guid
    assert retrieved.qlik_app_qualified_name == app.qualified_name
    assert retrieved.qlik_space_qualified_name == space.qualified_name


def test_chart(client, connection, app, sheet, chart):
    # A chart's qualifiedName hangs off its app, not its sheet.
    retrieved = _assert_retrieved(
        client, chart, QlikChart, connection, f"app/{APP_ID}/chart/{CHART_ID}"
    )
    assert retrieved.qlik_sheet.guid == sheet.guid
    assert retrieved.qlik_app_qualified_name == app.qualified_name


def test_dataset(client, connection, space, dataset):
    retrieved = _assert_retrieved(
        client, dataset, QlikDataset, connection, f"dataset/{DATASET_ID}"
    )
    assert retrieved.qlik_space.guid == space.guid


@pytest.mark.parametrize(
    "column_fixture, parent_fixture, relationship, parent_suffix",
    [
        ("sheet_column", "sheet", "qlik_sheet", f"app/{APP_ID}/sheet/{SHEET_ID}"),
        ("chart_column", "chart", "qlik_chart", f"app/{APP_ID}/chart/{CHART_ID}"),
        ("dataset_column", "dataset", "qlik_dataset", f"dataset/{DATASET_ID}"),
    ],
    ids=["sheet", "chart", "dataset"],
)
def test_column(
    request,
    client,
    connection,
    column_fixture,
    parent_fixture,
    relationship,
    parent_suffix,
):
    to_create, column = request.getfixturevalue(column_fixture)
    parent = request.getfixturevalue(parent_fixture)

    retrieved = _assert_retrieved(
        client,
        column,
        QlikColumn,
        connection,
        to_create.qualified_name[len(connection.qualified_name) + 1 :],
    )
    assert retrieved.qualified_name.startswith(
        f"{connection.qualified_name}/{parent_suffix}/column/"
    )
    assert getattr(retrieved, relationship).guid == parent.guid
    assert retrieved.qlik_column_name == FIELD
    assert retrieved.qlik_parent_qualified_name == parent.qualified_name
