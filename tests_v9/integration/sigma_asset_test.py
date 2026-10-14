# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    SigmaDataElement,
    SigmaDataElementField,
    SigmaDataModel,
    SigmaDataModelColumn,
    SigmaDataset,
    SigmaPage,
    SigmaWorkbook,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("SIGMA")

WORKBOOK_ID = f"wb-{MODULE_NAME}"
PAGE_ID = f"pg-{MODULE_NAME}"
DATA_ELEMENT_ID = f"el-{MODULE_NAME}"
FIELD_ID = f"fld-{MODULE_NAME}"
DATASET_ID = f"ds-{MODULE_NAME}"
DATA_MODEL_ID = f"dm-{MODULE_NAME}"
ELEMENT_ID = f"dmel-{MODULE_NAME}"
COLUMN_ID = f"col-{MODULE_NAME}"


def _save(client: AtlanClient, to_create, asset_type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.SIGMA
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def workbook(
    client: AtlanClient, connection: Connection
) -> Generator[SigmaWorkbook, None, None]:
    to_create = SigmaWorkbook.creator(
        name=f"workbook_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        workbook_id=WORKBOOK_ID,
    )
    result = _save(client, to_create, SigmaWorkbook)
    yield result
    delete_asset(client, guid=result.guid, asset_type=SigmaWorkbook)


@pytest.fixture(scope="module")
def page(
    client: AtlanClient, workbook: SigmaWorkbook
) -> Generator[SigmaPage, None, None]:
    to_create = SigmaPage.creator(
        name=f"page_{MODULE_NAME}",
        workbook_qualified_name=workbook.qualified_name,
        workbook_name=workbook.name,
        page_id=PAGE_ID,
    )
    result = _save(client, to_create, SigmaPage)
    yield result
    delete_asset(client, guid=result.guid, asset_type=SigmaPage)


@pytest.fixture(scope="module")
def data_element(
    client: AtlanClient, workbook: SigmaWorkbook, page: SigmaPage
) -> Generator[SigmaDataElement, None, None]:
    to_create = SigmaDataElement.creator(
        name=f"data_element_{MODULE_NAME}",
        page_qualified_name=page.qualified_name,
        page_name=page.name,
        workbook_name=workbook.name,
        data_element_id=DATA_ELEMENT_ID,
    )
    result = _save(client, to_create, SigmaDataElement)
    yield result
    delete_asset(client, guid=result.guid, asset_type=SigmaDataElement)


@pytest.fixture(scope="module")
def data_element_field(
    client: AtlanClient,
    workbook: SigmaWorkbook,
    page: SigmaPage,
    data_element: SigmaDataElement,
) -> Generator[SigmaDataElementField, None, None]:
    to_create = SigmaDataElementField.creator(
        name=f"field_{MODULE_NAME}",
        data_element_qualified_name=data_element.qualified_name,
        data_element_name=data_element.name,
        page_name=page.name,
        workbook_name=workbook.name,
        field_id=FIELD_ID,
    )
    result = _save(client, to_create, SigmaDataElementField)
    yield result
    delete_asset(client, guid=result.guid, asset_type=SigmaDataElementField)


@pytest.fixture(scope="module")
def dataset(
    client: AtlanClient, connection: Connection
) -> Generator[SigmaDataset, None, None]:
    to_create = SigmaDataset.creator(
        name=f"dataset_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        dataset_id=DATASET_ID,
    )
    result = _save(client, to_create, SigmaDataset)
    yield result
    delete_asset(client, guid=result.guid, asset_type=SigmaDataset)


@pytest.fixture(scope="module")
def data_model(
    client: AtlanClient, connection: Connection
) -> Generator[SigmaDataModel, None, None]:
    to_create = SigmaDataModel.creator(
        name=f"data_model_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        data_model_id=DATA_MODEL_ID,
    )
    result = _save(client, to_create, SigmaDataModel)
    yield result
    delete_asset(client, guid=result.guid, asset_type=SigmaDataModel)


@pytest.fixture(scope="module")
def data_model_column(
    client: AtlanClient, data_model: SigmaDataModel
) -> Generator[SigmaDataModelColumn, None, None]:
    to_create = SigmaDataModelColumn.creator(
        name=f"column_{MODULE_NAME}",
        data_model_qualified_name=data_model.qualified_name,
        data_model_name=data_model.name,
        element_id=ELEMENT_ID,
        column_id=COLUMN_ID,
    )
    result = _save(client, to_create, SigmaDataModelColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=SigmaDataModelColumn)


def _assert_retrieved(client, asset, asset_type, connection, expected_suffix):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == f"{connection.qualified_name}/{expected_suffix}"
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.SIGMA
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_workbook(client: AtlanClient, connection: Connection, workbook):
    _assert_retrieved(client, workbook, SigmaWorkbook, connection, WORKBOOK_ID)


def test_page(client: AtlanClient, connection: Connection, workbook, page):
    retrieved = _assert_retrieved(
        client, page, SigmaPage, connection, f"{WORKBOOK_ID}/{PAGE_ID}"
    )
    assert retrieved.sigma_workbook.guid == workbook.guid
    assert retrieved.sigma_workbook_qualified_name == workbook.qualified_name
    assert retrieved.sigma_workbook_name == workbook.name


def test_data_element(
    client: AtlanClient, connection: Connection, workbook, page, data_element
):
    retrieved = _assert_retrieved(
        client,
        data_element,
        SigmaDataElement,
        connection,
        f"{WORKBOOK_ID}/{PAGE_ID}/{DATA_ELEMENT_ID}",
    )
    assert retrieved.sigma_page.guid == page.guid
    assert retrieved.sigma_page_qualified_name == page.qualified_name
    assert retrieved.sigma_workbook_qualified_name == workbook.qualified_name


def test_data_element_field(
    client: AtlanClient,
    connection: Connection,
    workbook,
    page,
    data_element,
    data_element_field,
):
    retrieved = _assert_retrieved(
        client,
        data_element_field,
        SigmaDataElementField,
        connection,
        f"{WORKBOOK_ID}/{PAGE_ID}/{DATA_ELEMENT_ID}/{FIELD_ID}",
    )
    assert retrieved.sigma_data_element.guid == data_element.guid
    assert retrieved.sigma_data_element_qualified_name == data_element.qualified_name
    assert retrieved.sigma_page_qualified_name == page.qualified_name
    assert retrieved.sigma_workbook_qualified_name == workbook.qualified_name


def test_dataset(client: AtlanClient, connection: Connection, dataset):
    _assert_retrieved(client, dataset, SigmaDataset, connection, DATASET_ID)


def test_data_model(client: AtlanClient, connection: Connection, data_model):
    retrieved = _assert_retrieved(
        client, data_model, SigmaDataModel, connection, f"dataModels/{DATA_MODEL_ID}"
    )
    assert retrieved.asset_source_id == DATA_MODEL_ID


def test_data_model_column(
    client: AtlanClient, connection: Connection, data_model, data_model_column
):
    retrieved = _assert_retrieved(
        client,
        data_model_column,
        SigmaDataModelColumn,
        connection,
        f"dataModels/{DATA_MODEL_ID}/{ELEMENT_ID}/{COLUMN_ID}",
    )
    assert retrieved.sigma_data_model.guid == data_model.guid
    assert retrieved.sigma_data_model_qualified_name == data_model.qualified_name
    assert retrieved.asset_source_id == COLUMN_ID
