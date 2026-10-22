# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    SSRSDataSet,
    SSRSField,
    SSRSFolder,
    SSRSReport,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SSRS")

# Names carry a space: the app (and so the creators) strip it from the qn segment.
FOLDER_NAME = f"folder {MODULE_NAME}"
SUB_FOLDER_NAME = f"sub folder {MODULE_NAME}"
REPORT_NAME = f"report {MODULE_NAME}"
ROOT_REPORT_NAME = f"root report {MODULE_NAME}"
DATA_SET_NAME = f"data set {MODULE_NAME}"
FIELD_NAME = f"field {MODULE_NAME}"


def _segment(name: str) -> str:
    return name.replace(" ", "")


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SSRS
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def folder(
    client: AtlanClient, connection: Connection
) -> Generator[SSRSFolder, None, None]:
    to_create = SSRSFolder.creator(
        name=FOLDER_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=SSRSFolder)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SSRSFolder)


@pytest.fixture(scope="module")
def sub_folder(
    client: AtlanClient, connection: Connection, folder: SSRSFolder
) -> Generator[SSRSFolder, None, None]:
    to_create = SSRSFolder.creator(
        name=SUB_FOLDER_NAME,
        connection_qualified_name=connection.qualified_name,
        parent_folder_qualified_name=folder.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SSRSFolder)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SSRSFolder)


@pytest.fixture(scope="module")
def report(
    client: AtlanClient, connection: Connection, sub_folder: SSRSFolder
) -> Generator[SSRSReport, None, None]:
    to_create = SSRSReport.creator(
        name=REPORT_NAME,
        connection_qualified_name=connection.qualified_name,
        folder_qualified_name=sub_folder.qualified_name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=SSRSReport)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SSRSReport)


@pytest.fixture(scope="module")
def root_report(
    client: AtlanClient, connection: Connection
) -> Generator[SSRSReport, None, None]:
    to_create = SSRSReport.creator(
        name=ROOT_REPORT_NAME, connection_qualified_name=connection.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=SSRSReport)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SSRSReport)


@pytest.fixture(scope="module")
def data_set(
    client: AtlanClient, report: SSRSReport
) -> Generator[SSRSDataSet, None, None]:
    to_create = SSRSDataSet.creator(
        name=DATA_SET_NAME, ssrs_report_qualified_name=report.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=SSRSDataSet)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SSRSDataSet)


@pytest.fixture(scope="module")
def field(
    client: AtlanClient, data_set: SSRSDataSet
) -> Generator[SSRSField, None, None]:
    to_create = SSRSField.creator(
        name=FIELD_NAME, ssrs_data_set_qualified_name=data_set.qualified_name
    )
    result = client.asset.save(to_create).assets_created(asset_type=SSRSField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SSRSField)


def _retrieve(client: AtlanClient, asset, asset_type, connection: Connection):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == asset.qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.SSRS
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_folder(client: AtlanClient, connection: Connection, folder: SSRSFolder):
    assert folder.guid
    assert folder.qualified_name == (
        f"{connection.qualified_name}/{_segment(FOLDER_NAME)}"
    )
    _retrieve(client, folder, SSRSFolder, connection)


def test_sub_folder(
    client: AtlanClient,
    connection: Connection,
    folder: SSRSFolder,
    sub_folder: SSRSFolder,
):
    assert sub_folder.qualified_name == (
        f"{folder.qualified_name}/{_segment(SUB_FOLDER_NAME)}"
    )
    retrieved = _retrieve(client, sub_folder, SSRSFolder, connection)
    assert retrieved.ssrs_parent_folder.guid == folder.guid


def test_report(
    client: AtlanClient,
    connection: Connection,
    sub_folder: SSRSFolder,
    report: SSRSReport,
):
    assert report.qualified_name == (
        f"{sub_folder.qualified_name}/{_segment(REPORT_NAME)}"
    )
    retrieved = _retrieve(client, report, SSRSReport, connection)
    assert retrieved.ssrs_folder.guid == sub_folder.guid


def test_root_report(
    client: AtlanClient, connection: Connection, root_report: SSRSReport
):
    assert root_report.qualified_name == (
        f"{connection.qualified_name}/{_segment(ROOT_REPORT_NAME)}"
    )
    _retrieve(client, root_report, SSRSReport, connection)


def test_data_set(
    client: AtlanClient,
    connection: Connection,
    report: SSRSReport,
    data_set: SSRSDataSet,
):
    assert data_set.qualified_name == (
        f"{report.qualified_name}/{_segment(DATA_SET_NAME)}"
    )
    retrieved = _retrieve(client, data_set, SSRSDataSet, connection)
    assert retrieved.ssrs_report.guid == report.guid


def test_field(
    client: AtlanClient,
    connection: Connection,
    data_set: SSRSDataSet,
    field: SSRSField,
):
    assert field.qualified_name == (f"{data_set.qualified_name}/{_segment(FIELD_NAME)}")
    retrieved = _retrieve(client, field, SSRSField, connection)
    assert retrieved.ssrs_data_set.guid == data_set.guid
