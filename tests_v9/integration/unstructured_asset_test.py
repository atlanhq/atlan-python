# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    SourceTag,
    UnstructuredContainer,
    UnstructuredFolder,
    UnstructuredObject,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("UNSTRUCTURED")

CONTAINER_NAME = f"container_{MODULE_NAME}"
FOLDER_NAME = f"folder_{MODULE_NAME}"
SUB_FOLDER_NAME = f"subfolder_{MODULE_NAME}"
ROOT_OBJECT_NAME = f"root_{MODULE_NAME}.pdf"
NESTED_OBJECT_NAME = f"nested_{MODULE_NAME}.csv"
TAG_NAME = f"tag_{MODULE_NAME}"
TAG_ID = f"i{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.BIGID
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def container(
    client: AtlanClient, connection: Connection
) -> Generator[UnstructuredContainer, None, None]:
    to_create = UnstructuredContainer.creator(
        name=CONTAINER_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=UnstructuredContainer
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=UnstructuredContainer)


@pytest.fixture(scope="module")
def folder(
    client: AtlanClient, container: UnstructuredContainer
) -> Generator[UnstructuredFolder, None, None]:
    to_create = UnstructuredFolder.creator(
        name=FOLDER_NAME,
        unstructured_container_qualified_name=container.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=UnstructuredFolder)[
        0
    ]
    yield result
    delete_asset(client, guid=result.guid, asset_type=UnstructuredFolder)


@pytest.fixture(scope="module")
def sub_folder(
    client: AtlanClient,
    container: UnstructuredContainer,
    folder: UnstructuredFolder,
) -> Generator[UnstructuredFolder, None, None]:
    to_create = UnstructuredFolder.creator(
        name=SUB_FOLDER_NAME,
        unstructured_container_qualified_name=container.qualified_name,
        unstructured_parent_folder_qualified_name=folder.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=UnstructuredFolder)[
        0
    ]
    yield result
    delete_asset(client, guid=result.guid, asset_type=UnstructuredFolder)


@pytest.fixture(scope="module")
def root_object(
    client: AtlanClient, container: UnstructuredContainer
) -> Generator[UnstructuredObject, None, None]:
    to_create = UnstructuredObject.creator(
        name=ROOT_OBJECT_NAME,
        unstructured_container_qualified_name=container.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=UnstructuredObject)[
        0
    ]
    yield result
    delete_asset(client, guid=result.guid, asset_type=UnstructuredObject)


@pytest.fixture(scope="module")
def nested_object(
    client: AtlanClient,
    container: UnstructuredContainer,
    sub_folder: UnstructuredFolder,
) -> Generator[UnstructuredObject, None, None]:
    to_create = UnstructuredObject.creator(
        name=NESTED_OBJECT_NAME,
        unstructured_container_qualified_name=container.qualified_name,
        unstructured_parent_folder_qualified_name=sub_folder.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=UnstructuredObject)[
        0
    ]
    yield result
    delete_asset(client, guid=result.guid, asset_type=UnstructuredObject)


@pytest.fixture(scope="module")
def source_tag(
    client: AtlanClient, connection: Connection
) -> Generator[SourceTag, None, None]:
    to_create = SourceTag.creator(
        name=TAG_NAME,
        tag_id=TAG_ID,
        connection_qualified_name=connection.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SourceTag)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SourceTag)


def _retrieve(client: AtlanClient, asset, asset_type, connection: Connection):
    assert asset.guid
    retrieved = client.asset.get_by_qualified_name(
        asset.qualified_name, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.guid == asset.guid
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.BIGID
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_container(
    client: AtlanClient, connection: Connection, container: UnstructuredContainer
):
    assert container.qualified_name == f"{connection.qualified_name}/{CONTAINER_NAME}"
    _retrieve(client, container, UnstructuredContainer, connection)


def test_folder(
    client: AtlanClient,
    connection: Connection,
    container: UnstructuredContainer,
    folder: UnstructuredFolder,
):
    assert folder.qualified_name == f"{container.qualified_name}/{FOLDER_NAME}"
    retrieved = _retrieve(client, folder, UnstructuredFolder, connection)
    assert retrieved.unstructured_container_name == CONTAINER_NAME
    assert retrieved.unstructured_container_qualified_name == container.qualified_name
    assert retrieved.unstructured_container.guid == container.guid


def test_sub_folder(
    client: AtlanClient,
    connection: Connection,
    container: UnstructuredContainer,
    folder: UnstructuredFolder,
    sub_folder: UnstructuredFolder,
):
    assert sub_folder.qualified_name == (
        f"{container.qualified_name}/{FOLDER_NAME}/{SUB_FOLDER_NAME}"
    )
    retrieved = _retrieve(client, sub_folder, UnstructuredFolder, connection)
    assert retrieved.unstructured_container_qualified_name == container.qualified_name
    assert retrieved.unstructured_parent_folder_qualified_name == folder.qualified_name
    assert retrieved.unstructured_parent_folder.guid == folder.guid


def test_root_object(
    client: AtlanClient,
    connection: Connection,
    container: UnstructuredContainer,
    root_object: UnstructuredObject,
):
    assert root_object.qualified_name == (
        f"{container.qualified_name}/{ROOT_OBJECT_NAME}"
    )
    retrieved = _retrieve(client, root_object, UnstructuredObject, connection)
    assert retrieved.unstructured_object_key == ROOT_OBJECT_NAME
    assert retrieved.unstructured_container.guid == container.guid


def test_nested_object(
    client: AtlanClient,
    connection: Connection,
    container: UnstructuredContainer,
    sub_folder: UnstructuredFolder,
    nested_object: UnstructuredObject,
):
    object_key = f"{FOLDER_NAME}/{SUB_FOLDER_NAME}/{NESTED_OBJECT_NAME}"
    assert nested_object.qualified_name == f"{container.qualified_name}/{object_key}"
    retrieved = _retrieve(client, nested_object, UnstructuredObject, connection)
    assert retrieved.unstructured_object_key == object_key
    assert retrieved.unstructured_container_qualified_name == container.qualified_name
    assert retrieved.unstructured_parent_folder.guid == sub_folder.guid


def test_source_tag(client: AtlanClient, connection: Connection, source_tag: SourceTag):
    assert source_tag.qualified_name == (
        f"{connection.qualified_name}/source-tag/{TAG_ID}"
    )
    retrieved = _retrieve(client, source_tag, SourceTag, connection)
    assert retrieved.tag_id == TAG_ID
