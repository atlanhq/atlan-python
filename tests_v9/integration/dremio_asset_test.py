# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import Connection, DremioFolder, DremioSource, DremioSpace
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("DREMIO")

SOURCE_NAME = f"source_{MODULE_NAME}"
SPACE_NAME = f"space_{MODULE_NAME}"
FOLDER_NAME = f"folder_{MODULE_NAME}"
SUB_FOLDER_NAME = f"sub_folder_{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.DREMIO
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def source(
    client: AtlanClient, connection: Connection
) -> Generator[DremioSource, None, None]:
    to_create = DremioSource.creator(
        name=SOURCE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=DremioSource)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DremioSource)


@pytest.fixture(scope="module")
def space(
    client: AtlanClient, connection: Connection
) -> Generator[DremioSpace, None, None]:
    to_create = DremioSpace.creator(
        name=SPACE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=DremioSpace)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DremioSpace)


@pytest.fixture(scope="module")
def folder(
    client: AtlanClient, source: DremioSource
) -> Generator[DremioFolder, None, None]:
    to_create = DremioFolder.creator(
        name=FOLDER_NAME,
        parent_qualified_name=source.qualified_name,
        dremio_source_qualified_name=source.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=DremioFolder)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DremioFolder)


@pytest.fixture(scope="module")
def sub_folder(
    client: AtlanClient, source: DremioSource, folder: DremioFolder
) -> Generator[DremioFolder, None, None]:
    to_create = DremioFolder.creator(
        name=SUB_FOLDER_NAME,
        parent_qualified_name=folder.qualified_name,
        dremio_source_qualified_name=source.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=DremioFolder)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DremioFolder)


@pytest.fixture(scope="module")
def space_folder(
    client: AtlanClient, space: DremioSpace
) -> Generator[DremioFolder, None, None]:
    to_create = DremioFolder.creator(
        name=FOLDER_NAME,
        parent_qualified_name=space.qualified_name,
        dremio_space_qualified_name=space.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=DremioFolder)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DremioFolder)


def _assert_retrieved(client, asset, asset_type, connection, qualified_name):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.DREMIO
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_source(client: AtlanClient, connection: Connection, source: DremioSource):
    assert source.guid
    retrieved = _assert_retrieved(
        client,
        source,
        DremioSource,
        connection,
        f"{connection.qualified_name}/{SOURCE_NAME}",
    )
    assert retrieved.dremio_source_qualified_name == retrieved.qualified_name
    assert retrieved.dremio_source_name == SOURCE_NAME


def test_space(client: AtlanClient, connection: Connection, space: DremioSpace):
    assert space.guid
    retrieved = _assert_retrieved(
        client,
        space,
        DremioSpace,
        connection,
        f"{connection.qualified_name}/{SPACE_NAME}",
    )
    assert retrieved.dremio_space_qualified_name == retrieved.qualified_name
    assert retrieved.dremio_space_name == SPACE_NAME


def test_folder(
    client: AtlanClient,
    connection: Connection,
    source: DremioSource,
    folder: DremioFolder,
):
    assert folder.guid
    retrieved = _assert_retrieved(
        client,
        folder,
        DremioFolder,
        connection,
        f"{source.qualified_name}/{FOLDER_NAME}",
    )
    assert retrieved.dremio_source.guid == source.guid
    assert retrieved.dremio_source_qualified_name == source.qualified_name
    assert retrieved.dremio_source_name == SOURCE_NAME


def test_sub_folder(
    client: AtlanClient,
    connection: Connection,
    source: DremioSource,
    folder: DremioFolder,
    sub_folder: DremioFolder,
):
    assert sub_folder.guid
    retrieved = _assert_retrieved(
        client,
        sub_folder,
        DremioFolder,
        connection,
        f"{folder.qualified_name}/{SUB_FOLDER_NAME}",
    )
    assert retrieved.dremio_source.guid == source.guid
    assert retrieved.dremio_parent_folder.guid == folder.guid
    assert retrieved.dremio_parent_folder_qualified_name == folder.qualified_name


def test_space_folder(
    client: AtlanClient,
    connection: Connection,
    space: DremioSpace,
    space_folder: DremioFolder,
):
    assert space_folder.guid
    retrieved = _assert_retrieved(
        client,
        space_folder,
        DremioFolder,
        connection,
        f"{space.qualified_name}/{FOLDER_NAME}",
    )
    assert retrieved.dremio_space.guid == space.guid
    assert retrieved.dremio_space_qualified_name == space.qualified_name
