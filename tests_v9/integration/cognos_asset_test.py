# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    CognosColumn,
    CognosDashboard,
    CognosDataset,
    CognosDatasource,
    CognosExploration,
    CognosFile,
    CognosFolder,
    CognosModule,
    CognosPackage,
    CognosReport,
    Connection,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("COGNOS")

FOLDER_CHILDREN = [
    (CognosReport, "report"),
    (CognosDashboard, "dashboard"),
    (CognosExploration, "exploration"),
    (CognosFile, "file"),
    (CognosModule, "module"),
    (CognosPackage, "package"),
    (CognosDataset, "dataSet2"),
]


def _cognos_id(slug: str) -> str:
    return f"i{slug}{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.COGNOS
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def folder(
    client: AtlanClient, connection: Connection
) -> Generator[CognosFolder, None, None]:
    to_create = CognosFolder.creator(
        name=f"folder_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        cognos_id=_cognos_id("folder"),
    )
    result = client.asset.save(to_create).assets_created(asset_type=CognosFolder)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=CognosFolder)


@pytest.fixture(scope="module")
def folder_children(
    client: AtlanClient, connection: Connection, folder: CognosFolder
) -> Generator[dict, None, None]:
    created = {}
    for asset_type, slug in FOLDER_CHILDREN:
        to_create = asset_type.creator(
            name=f"{slug}_{MODULE_NAME}",
            connection_qualified_name=connection.qualified_name,
            cognos_id=_cognos_id(slug),
        )
        to_create.cognos_folder = folder.relate()
        created[asset_type] = client.asset.save(to_create).assets_created(
            asset_type=asset_type
        )[0]
    yield created
    for asset_type, asset in created.items():
        delete_asset(client, guid=asset.guid, asset_type=asset_type)


@pytest.fixture(scope="module")
def datasource(
    client: AtlanClient, connection: Connection
) -> Generator[CognosDatasource, None, None]:
    to_create = CognosDatasource.creator(
        name=f"datasource_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        cognos_id=_cognos_id("datasource"),
    )
    result = client.asset.save(to_create).assets_created(asset_type=CognosDatasource)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=CognosDatasource)


@pytest.fixture(scope="module")
def column(
    client: AtlanClient, connection: Connection, folder_children: dict
) -> Generator[CognosColumn, None, None]:
    to_create = CognosColumn.creator(
        name=f"column_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        cognos_id=_cognos_id("column"),
    )
    to_create.cognos_dataset = folder_children[CognosDataset].relate()
    result = client.asset.save(to_create).assets_created(asset_type=CognosColumn)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=CognosColumn)


def _assert_retrieved(client, asset, asset_type, connection, slug):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == (
        f"{connection.qualified_name}/{slug}/{_cognos_id(slug)}"
    )
    assert retrieved.name == asset.name
    assert retrieved.cognos_id == _cognos_id(slug)
    assert retrieved.connector_name == AtlanConnectorType.COGNOS
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_folder(client: AtlanClient, connection: Connection, folder: CognosFolder):
    _assert_retrieved(client, folder, CognosFolder, connection, "folder")


def test_folder_children(
    client: AtlanClient,
    connection: Connection,
    folder: CognosFolder,
    folder_children: dict,
):
    for asset_type, slug in FOLDER_CHILDREN:
        retrieved = _assert_retrieved(
            client, folder_children[asset_type], asset_type, connection, slug
        )
        assert retrieved.cognos_folder.guid == folder.guid


def test_datasource(
    client: AtlanClient, connection: Connection, datasource: CognosDatasource
):
    _assert_retrieved(client, datasource, CognosDatasource, connection, "datasource")


def test_column(
    client: AtlanClient,
    connection: Connection,
    folder_children: dict,
    column: CognosColumn,
):
    retrieved = _assert_retrieved(client, column, CognosColumn, connection, "column")
    assert retrieved.cognos_dataset.guid == folder_children[CognosDataset].guid
