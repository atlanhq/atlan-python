# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    DomoCard,
    DomoDashboard,
    DomoDataset,
    DomoDatasetColumn,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("DOMO")


def _domo_id(slug: str) -> str:
    return f"i{slug}{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.DOMO
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def dataset(
    client: AtlanClient, connection: Connection
) -> Generator[DomoDataset, None, None]:
    to_create = DomoDataset.creator(
        name=f"dataset_{MODULE_NAME}",
        domo_id=_domo_id("dataset"),
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=DomoDataset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DomoDataset)


@pytest.fixture(scope="module")
def dataset_column(
    client: AtlanClient, dataset: DomoDataset
) -> Generator[DomoDatasetColumn, None, None]:
    to_create = DomoDatasetColumn.creator(
        name=f"column_{MODULE_NAME}",
        domo_dataset_qualified_name=dataset.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=DomoDatasetColumn)[
        0
    ]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DomoDatasetColumn)


@pytest.fixture(scope="module")
def dashboard(
    client: AtlanClient, connection: Connection
) -> Generator[DomoDashboard, None, None]:
    to_create = DomoDashboard.creator(
        name=f"dashboard_{MODULE_NAME}",
        domo_id=_domo_id("dashboard"),
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=DomoDashboard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DomoDashboard)


@pytest.fixture(scope="module")
def card(
    client: AtlanClient,
    connection: Connection,
    dataset: DomoDataset,
    dashboard: DomoDashboard,
) -> Generator[DomoCard, None, None]:
    to_create = DomoCard.creator(
        name=f"card_{MODULE_NAME}",
        domo_id=_domo_id("card"),
        connection_qualified_name=connection.qualified_name,
    )
    to_create.domo_dataset = dataset.relate()
    to_create.domo_dashboards = [dashboard.relate()]
    result = client.asset.save(to_create).assets_created(asset_type=DomoCard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DomoCard)


@pytest.fixture(scope="module")
def doc_card(
    client: AtlanClient, connection: Connection
) -> Generator[DomoCard, None, None]:
    # Doc and notebook cards have no dataset; atlan-domo-app omits domoDataset.
    to_create = DomoCard.creator(
        name=f"doc_card_{MODULE_NAME}",
        domo_id=_domo_id("doccard"),
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=DomoCard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DomoCard)


def _assert_retrieved(client, asset, asset_type, connection, qualified_name):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.DOMO
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_dataset(client: AtlanClient, connection: Connection, dataset: DomoDataset):
    retrieved = _assert_retrieved(
        client,
        dataset,
        DomoDataset,
        connection,
        f"{connection.qualified_name}/dataset/{_domo_id('dataset')}",
    )
    assert retrieved.domo_id == _domo_id("dataset")


def test_dataset_column(
    client: AtlanClient,
    connection: Connection,
    dataset: DomoDataset,
    dataset_column: DomoDatasetColumn,
):
    retrieved = _assert_retrieved(
        client,
        dataset_column,
        DomoDatasetColumn,
        connection,
        f"{dataset.qualified_name}/column/column_{MODULE_NAME}",
    )
    assert retrieved.domo_dataset_qualified_name == dataset.qualified_name
    assert retrieved.domo_dataset.guid == dataset.guid


def test_dashboard(
    client: AtlanClient, connection: Connection, dashboard: DomoDashboard
):
    retrieved = _assert_retrieved(
        client,
        dashboard,
        DomoDashboard,
        connection,
        f"{connection.qualified_name}/dashboard/{_domo_id('dashboard')}",
    )
    assert retrieved.domo_id == _domo_id("dashboard")


def test_card(
    client: AtlanClient,
    connection: Connection,
    dataset: DomoDataset,
    dashboard: DomoDashboard,
    card: DomoCard,
):
    retrieved = _assert_retrieved(
        client,
        card,
        DomoCard,
        connection,
        f"{connection.qualified_name}/card/{_domo_id('card')}",
    )
    assert retrieved.domo_id == _domo_id("card")
    assert retrieved.domo_dataset.guid == dataset.guid
    assert [d.guid for d in retrieved.domo_dashboards] == [dashboard.guid]


def test_card_without_dataset(
    client: AtlanClient, connection: Connection, doc_card: DomoCard
):
    retrieved = _assert_retrieved(
        client,
        doc_card,
        DomoCard,
        connection,
        f"{connection.qualified_name}/card/{_domo_id('doccard')}",
    )
    assert not retrieved.domo_dataset
