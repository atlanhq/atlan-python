# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    RedashDashboard,
    RedashQuery,
    RedashVisualization,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("REDASH")

QUERY_ID = 42
VISUALIZATION_ID = 7
DASHBOARD_SLUG = f"dash-{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.REDASH
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def query(
    client: AtlanClient, connection: Connection
) -> Generator[RedashQuery, None, None]:
    to_create = RedashQuery.creator(
        name=f"query_{MODULE_NAME}",
        query_id=QUERY_ID,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=RedashQuery)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=RedashQuery)


@pytest.fixture(scope="module")
def visualization(
    client: AtlanClient, query: RedashQuery
) -> Generator[RedashVisualization, None, None]:
    to_create = RedashVisualization.creator(
        name=f"viz_{MODULE_NAME}",
        visualization_id=VISUALIZATION_ID,
        redash_query_qualified_name=query.qualified_name,
        redash_query_name=query.name,
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=RedashVisualization
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=RedashVisualization)


@pytest.fixture(scope="module")
def dashboard(
    client: AtlanClient, connection: Connection
) -> Generator[RedashDashboard, None, None]:
    to_create = RedashDashboard.creator(
        name=f"dashboard_{MODULE_NAME}",
        slug=DASHBOARD_SLUG,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=RedashDashboard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=RedashDashboard)


def _assert_retrieved(client, asset, asset_type, connection, expected_qn):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == expected_qn
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.REDASH
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_query(client: AtlanClient, connection: Connection, query: RedashQuery):
    assert query.guid
    _assert_retrieved(
        client,
        query,
        RedashQuery,
        connection,
        f"{connection.qualified_name}/queries/{QUERY_ID}",
    )


def test_visualization(
    client: AtlanClient,
    connection: Connection,
    query: RedashQuery,
    visualization: RedashVisualization,
):
    assert visualization.guid
    retrieved = _assert_retrieved(
        client,
        visualization,
        RedashVisualization,
        connection,
        f"{connection.qualified_name}/visualizations/{VISUALIZATION_ID}",
    )
    assert retrieved.redash_query_qualified_name == query.qualified_name
    assert retrieved.redash_query_name == query.name
    assert retrieved.redash_query.guid == query.guid


def test_dashboard(
    client: AtlanClient, connection: Connection, dashboard: RedashDashboard
):
    assert dashboard.guid
    _assert_retrieved(
        client,
        dashboard,
        RedashDashboard,
        connection,
        f"{connection.qualified_name}/dashboards/{DASHBOARD_SLUG}",
    )
