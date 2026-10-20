# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    FabricActivity,
    FabricDataflow,
    FabricDataflowEntityColumn,
    FabricDataPipeline,
    FabricPage,
    FabricReport,
    FabricSemanticModel,
    FabricSemanticModelMeasure,
    FabricSemanticModelTable,
    FabricSemanticModelTableColumn,
    FabricVisual,
    FabricWorkspace,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("FABRIC")

WORKSPACE_ID = f"ws-{MODULE_NAME}"
SEMANTIC_MODEL_ID = f"sm-{MODULE_NAME}"
REPORT_ID = f"rp-{MODULE_NAME}"
PAGE_ID = f"pg-{MODULE_NAME}"
DATAFLOW_ID = f"df-{MODULE_NAME}"
DATA_PIPELINE_ID = f"dp-{MODULE_NAME}"
TABLE_NAME = f"table_{MODULE_NAME}"
ENTITY_NAME = f"entity_{MODULE_NAME}"


def _save(client: AtlanClient, to_create, asset_type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.FABRIC
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def workspace(
    client: AtlanClient, connection: Connection
) -> Generator[FabricWorkspace, None, None]:
    # FabricWorkspace has no creator yet, so build it the way atlan-fabric-app does.
    to_create = FabricWorkspace(
        name=f"workspace_{MODULE_NAME}",
        qualified_name=f"{connection.qualified_name}/{WORKSPACE_ID}",
        connection_qualified_name=connection.qualified_name,
        connector_name=AtlanConnectorType.FABRIC.value,
    )
    result = _save(client, to_create, FabricWorkspace)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricWorkspace)


@pytest.fixture(scope="module")
def semantic_model(
    client: AtlanClient, workspace: FabricWorkspace
) -> Generator[FabricSemanticModel, None, None]:
    to_create = FabricSemanticModel.creator(
        name=f"semantic_model_{MODULE_NAME}",
        workspace_qualified_name=workspace.qualified_name,
        semantic_model_id=SEMANTIC_MODEL_ID,
    )
    result = _save(client, to_create, FabricSemanticModel)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricSemanticModel)


@pytest.fixture(scope="module")
def table(
    client: AtlanClient, semantic_model: FabricSemanticModel
) -> Generator[FabricSemanticModelTable, None, None]:
    to_create = FabricSemanticModelTable.creator(
        name=TABLE_NAME, semantic_model_qualified_name=semantic_model.qualified_name
    )
    result = _save(client, to_create, FabricSemanticModelTable)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricSemanticModelTable)


@pytest.fixture(scope="module")
def column(
    client: AtlanClient, table: FabricSemanticModelTable
) -> Generator[FabricSemanticModelTableColumn, None, None]:
    to_create = FabricSemanticModelTableColumn.creator(
        name=f"column_{MODULE_NAME}",
        semantic_model_table_qualified_name=table.qualified_name,
    )
    result = _save(client, to_create, FabricSemanticModelTableColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricSemanticModelTableColumn)


@pytest.fixture(scope="module")
def measure(
    client: AtlanClient, table: FabricSemanticModelTable
) -> Generator[FabricSemanticModelMeasure, None, None]:
    to_create = FabricSemanticModelMeasure.creator(
        name=f"measure_{MODULE_NAME}",
        semantic_model_table_qualified_name=table.qualified_name,
    )
    result = _save(client, to_create, FabricSemanticModelMeasure)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricSemanticModelMeasure)


@pytest.fixture(scope="module")
def report(
    client: AtlanClient, workspace: FabricWorkspace
) -> Generator[FabricReport, None, None]:
    to_create = FabricReport.creator(
        name=f"report_{MODULE_NAME}",
        workspace_qualified_name=workspace.qualified_name,
        report_id=REPORT_ID,
    )
    result = _save(client, to_create, FabricReport)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricReport)


@pytest.fixture(scope="module")
def page(
    client: AtlanClient, report: FabricReport
) -> Generator[FabricPage, None, None]:
    to_create = FabricPage.creator(
        name=f"page_{MODULE_NAME}",
        report_qualified_name=report.qualified_name,
        page_id=PAGE_ID,
    )
    result = _save(client, to_create, FabricPage)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricPage)


@pytest.fixture(scope="module")
def visual(
    client: AtlanClient, page: FabricPage
) -> Generator[FabricVisual, None, None]:
    to_create = FabricVisual.creator(
        name=f"visual_{MODULE_NAME}",
        page_qualified_name=page.qualified_name,
        page_name=page.name,
    )
    result = _save(client, to_create, FabricVisual)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricVisual)


@pytest.fixture(scope="module")
def dataflow(
    client: AtlanClient, workspace: FabricWorkspace
) -> Generator[FabricDataflow, None, None]:
    to_create = FabricDataflow.creator(
        name=f"dataflow_{MODULE_NAME}",
        workspace_qualified_name=workspace.qualified_name,
        dataflow_id=DATAFLOW_ID,
    )
    result = _save(client, to_create, FabricDataflow)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricDataflow)


@pytest.fixture(scope="module")
def dataflow_column(
    client: AtlanClient, dataflow: FabricDataflow
) -> Generator[FabricDataflowEntityColumn, None, None]:
    to_create = FabricDataflowEntityColumn.creator(
        name=f"dataflow_column_{MODULE_NAME}",
        dataflow_qualified_name=dataflow.qualified_name,
        dataflow_name=dataflow.name,
        entity_name=ENTITY_NAME,
    )
    result = _save(client, to_create, FabricDataflowEntityColumn)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricDataflowEntityColumn)


@pytest.fixture(scope="module")
def data_pipeline(
    client: AtlanClient, workspace: FabricWorkspace
) -> Generator[FabricDataPipeline, None, None]:
    to_create = FabricDataPipeline.creator(
        name=f"data_pipeline_{MODULE_NAME}",
        workspace_qualified_name=workspace.qualified_name,
        data_pipeline_id=DATA_PIPELINE_ID,
    )
    result = _save(client, to_create, FabricDataPipeline)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricDataPipeline)


@pytest.fixture(scope="module")
def activity(
    client: AtlanClient, data_pipeline: FabricDataPipeline
) -> Generator[FabricActivity, None, None]:
    to_create = FabricActivity.creator(
        name=f"activity_{MODULE_NAME}",
        data_pipeline_qualified_name=data_pipeline.qualified_name,
    )
    result = _save(client, to_create, FabricActivity)
    yield result
    delete_asset(client, guid=result.guid, asset_type=FabricActivity)


def _assert_retrieved(client, asset, asset_type, connection, expected_suffix):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.qualified_name == f"{connection.qualified_name}/{expected_suffix}"
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.FABRIC
    assert retrieved.connection_qualified_name == connection.qualified_name
    assert (
        retrieved.asset_space_qualified_name
        == f"{connection.qualified_name}/{WORKSPACE_ID}"
    )
    return retrieved


def test_semantic_model(client, connection, workspace, semantic_model):
    retrieved = _assert_retrieved(
        client,
        semantic_model,
        FabricSemanticModel,
        connection,
        f"{WORKSPACE_ID}/{SEMANTIC_MODEL_ID}",
    )
    assert retrieved.fabric_workspace.guid == workspace.guid


def test_semantic_model_table(client, connection, semantic_model, table):
    retrieved = _assert_retrieved(
        client,
        table,
        FabricSemanticModelTable,
        connection,
        f"{WORKSPACE_ID}/{SEMANTIC_MODEL_ID}/{TABLE_NAME}",
    )
    assert retrieved.fabric_semantic_model.guid == semantic_model.guid
    assert (
        retrieved.fabric_semantic_model_qualified_name == semantic_model.qualified_name
    )


def test_semantic_model_table_column(client, connection, table, column):
    retrieved = _assert_retrieved(
        client,
        column,
        FabricSemanticModelTableColumn,
        connection,
        f"{WORKSPACE_ID}/{SEMANTIC_MODEL_ID}/{TABLE_NAME}/{column.name}",
    )
    assert retrieved.fabric_semantic_model_table.guid == table.guid
    assert retrieved.fabric_semantic_model_table_qualified_name == table.qualified_name
    assert retrieved.fabric_semantic_model_table_name == TABLE_NAME


def test_semantic_model_measure(client, connection, semantic_model, table, measure):
    retrieved = _assert_retrieved(
        client,
        measure,
        FabricSemanticModelMeasure,
        connection,
        f"{WORKSPACE_ID}/{SEMANTIC_MODEL_ID}/{TABLE_NAME}/{measure.name}",
    )
    assert retrieved.fabric_semantic_model_table.guid == table.guid
    assert retrieved.fabric_semantic_model_table_qualified_name == table.qualified_name
    assert retrieved.fabric_semantic_model_table_name == TABLE_NAME
    assert (
        retrieved.fabric_semantic_model_qualified_name == semantic_model.qualified_name
    )


def test_report(client, connection, workspace, report):
    retrieved = _assert_retrieved(
        client, report, FabricReport, connection, f"{WORKSPACE_ID}/{REPORT_ID}"
    )
    assert retrieved.fabric_workspace.guid == workspace.guid


def test_page(client, connection, report, page):
    retrieved = _assert_retrieved(
        client, page, FabricPage, connection, f"{WORKSPACE_ID}/{REPORT_ID}/{PAGE_ID}"
    )
    assert retrieved.fabric_report.guid == report.guid
    assert retrieved.fabric_report_qualified_name == report.qualified_name


def test_visual(client, connection, page, visual):
    retrieved = _assert_retrieved(
        client,
        visual,
        FabricVisual,
        connection,
        f"{WORKSPACE_ID}/{REPORT_ID}/{PAGE_ID}/{visual.name}",
    )
    assert retrieved.fabric_page.guid == page.guid
    assert retrieved.fabric_page_qualified_name == page.qualified_name
    assert retrieved.fabric_page_name == page.name


def test_dataflow(client, connection, workspace, dataflow):
    retrieved = _assert_retrieved(
        client, dataflow, FabricDataflow, connection, f"{WORKSPACE_ID}/{DATAFLOW_ID}"
    )
    assert retrieved.fabric_workspace.guid == workspace.guid


def test_dataflow_entity_column(client, connection, dataflow, dataflow_column):
    retrieved = _assert_retrieved(
        client,
        dataflow_column,
        FabricDataflowEntityColumn,
        connection,
        f"{WORKSPACE_ID}/{DATAFLOW_ID}/{ENTITY_NAME}/{dataflow_column.name}",
    )
    assert retrieved.fabric_dataflow.guid == dataflow.guid
    assert retrieved.fabric_dataflow_qualified_name == dataflow.qualified_name
    assert retrieved.fabric_dataflow_name == dataflow.name


def test_data_pipeline(client, connection, workspace, data_pipeline):
    retrieved = _assert_retrieved(
        client,
        data_pipeline,
        FabricDataPipeline,
        connection,
        f"{WORKSPACE_ID}/{DATA_PIPELINE_ID}",
    )
    assert retrieved.fabric_workspace.guid == workspace.guid


def test_activity(client, connection, data_pipeline, activity):
    retrieved = _assert_retrieved(
        client,
        activity,
        FabricActivity,
        connection,
        f"{WORKSPACE_ID}/{DATA_PIPELINE_ID}/{activity.name}",
    )
    assert retrieved.fabric_data_pipeline.guid == data_pipeline.guid
