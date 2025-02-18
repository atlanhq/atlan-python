from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Connection,
    QuickSightAnalysis,
    QuickSightAnalysisVisual,
    QuickSightDashboard,
    QuickSightDashboardVisual,
    QuickSightDataset,
    QuickSightDatasetField,
    QuickSightFolder,
)
from pyatlan.model.enums import (
    AtlanConnectorType,
    QuickSightDatasetFieldType,
    QuickSightDatasetImportMode,
    QuickSightFolderType,
)
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("QUICKSIGHT")

CONNECTOR_TYPE = AtlanConnectorType.QUICKSIGHT
QUICKSIGHT_FOLDER_NAME = f"{MODULE_NAME}-QUICKSIGHT-FOLDER"
QUICKSIGHT_FOLDER_ID = f"{MODULE_NAME}-FOLDER-ID"
QUICKSIGHT_DATASET_NAME = f"{MODULE_NAME}-QUICKSIGHT-DATASET"
QUICKSIGHT_DATASET_ID = f"{MODULE_NAME}-DATASET-ID"
QUICKSIGHT_DASHBOARD_NAME = f"{MODULE_NAME}-QUICKSIGHT-DASHBOARD"
QUICKSIGHT_DASHBOARD_ID = f"{MODULE_NAME}-DASHBOARD-ID"
QUICKSIGHT_ANALYSIS_NAME = f"{MODULE_NAME}-QUICKSIGHT-ANALYSIS"
QUICKSIGHT_ANALYSIS_ID = f"{MODULE_NAME}-ANALYSIS-ID"
QUICKSIGHT_DATASET_FIELD_NAME = f"{MODULE_NAME}-QUICKSIGHT-DATASET-FIELD"
QUICKSIGHT_DATASET_FIELD_ID = f"{MODULE_NAME}-DATASET-FIELD-ID"
QUICKSIGHT_DASHBOARD_VISUAL_NAME = f"{MODULE_NAME}-QUICKSIGHT-DASHBOARD-VISUAL"
QUICKSIGHT_DASHBOARD_VISUAL_ID = f"{MODULE_NAME}-DASHBOARD-VISUAL-ID"
QUICKSIGHT_ANALYSIS_VISUAL_NAME = f"{MODULE_NAME}-QUICKSIGHT-ANALYSIS-VISUAL"
QUICKSIGHT_ANALYSIS_VISUAL_ID = f"{MODULE_NAME}-ANALYSIS-VISUAL-ID"
QUICKSIGHT_SHEET_NAME = f"{MODULE_NAME}-QUICKSIGHT-SHEET-NAME"
QUICKSIGHT_SHEET_ID = f"{MODULE_NAME}-SHEET-ID"
QUICK_SIGHT_DESCRIPTION = "Automated testing of the Python SDK."


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def quick_sight_folder(
    client: AtlanClient, connection: Connection
) -> Generator[QuickSightFolder, None, None]:
    assert connection.qualified_name
    to_create = QuickSightFolder.creator(
        name=QUICKSIGHT_FOLDER_NAME,
        connection_qualified_name=connection.qualified_name,
        quick_sight_id=QUICKSIGHT_FOLDER_ID,
        quick_sight_folder_type=QuickSightFolderType.SHARED,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=QuickSightFolder)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=QuickSightFolder)


@pytest.fixture(scope="module")
def quick_sight_dataset(
    client: AtlanClient, connection: Connection, quick_sight_folder: QuickSightFolder
) -> Generator[QuickSightDataset, None, None]:
    assert connection.qualified_name
    assert quick_sight_folder.qualified_name
    to_create = QuickSightDataset.creator(
        name=QUICKSIGHT_DATASET_NAME,
        connection_qualified_name=connection.qualified_name,
        quick_sight_id=QUICKSIGHT_DATASET_ID,
        quick_sight_dataset_import_mode=QuickSightDatasetImportMode.SPICE,
        quick_sight_dataset_folders=[str(quick_sight_folder.qualified_name)],
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=QuickSightDataset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=QuickSightDataset)


@pytest.fixture(scope="module")
def quick_sight_dashboard(
    client: AtlanClient, connection: Connection, quick_sight_folder: QuickSightFolder
) -> Generator[QuickSightDashboard, None, None]:
    assert connection.qualified_name
    assert quick_sight_folder.qualified_name
    to_create = QuickSightDashboard.creator(
        name=QUICKSIGHT_DASHBOARD_NAME,
        connection_qualified_name=connection.qualified_name,
        quick_sight_id=QUICKSIGHT_DASHBOARD_ID,
        quick_sight_dashboard_folders=[str(quick_sight_folder.qualified_name)],
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=QuickSightDashboard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=QuickSightDashboard)


@pytest.fixture(scope="module")
def quick_sight_analysis(
    client: AtlanClient, connection: Connection, quick_sight_folder: QuickSightFolder
) -> Generator[QuickSightAnalysis, None, None]:
    assert connection.qualified_name
    assert quick_sight_folder.qualified_name
    to_create = QuickSightAnalysis.creator(
        name=QUICKSIGHT_ANALYSIS_NAME,
        connection_qualified_name=connection.qualified_name,
        quick_sight_id=QUICKSIGHT_ANALYSIS_ID,
        quick_sight_analysis_folders=[str(quick_sight_folder.qualified_name)],
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=QuickSightAnalysis)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=QuickSightAnalysis)


@pytest.fixture(scope="module")
def quick_sight_dataset_field(
    client: AtlanClient,
    connection: Connection,
    quick_sight_dataset: QuickSightDataset,
) -> Generator[QuickSightDatasetField, None, None]:
    assert connection.qualified_name
    to_create = QuickSightDatasetField.creator(
        name=QUICKSIGHT_DATASET_FIELD_NAME,
        quick_sight_dataset_qualified_name=str(quick_sight_dataset.qualified_name),
        connection_qualified_name=connection.qualified_name,
        quick_sight_id=QUICKSIGHT_DATASET_FIELD_ID,
        quick_sight_dataset_field_type=QuickSightDatasetFieldType.STRING,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=QuickSightDatasetField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=QuickSightDatasetField)


@pytest.fixture(scope="module")
def quick_sight_analysis_visual(
    client: AtlanClient,
    connection: Connection,
    quick_sight_analysis: QuickSightAnalysis,
) -> Generator[QuickSightAnalysisVisual, None, None]:
    assert connection.qualified_name
    to_create = QuickSightAnalysisVisual.creator(
        name=QUICKSIGHT_ANALYSIS_VISUAL_NAME,
        quick_sight_sheet_id=QUICKSIGHT_SHEET_ID,
        quick_sight_sheet_name=QUICKSIGHT_SHEET_NAME,
        quick_sight_analysis_qualified_name=str(quick_sight_analysis.qualified_name),
        connection_qualified_name=connection.qualified_name,
        quick_sight_id=QUICKSIGHT_ANALYSIS_VISUAL_ID,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=QuickSightAnalysisVisual)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=QuickSightAnalysisVisual)


@pytest.fixture(scope="module")
def quick_sight_dashboard_visual(
    client: AtlanClient,
    connection: Connection,
    quick_sight_dashboard: QuickSightDashboard,
) -> Generator[QuickSightDashboardVisual, None, None]:
    assert connection.qualified_name
    to_create = QuickSightDashboardVisual.creator(
        name=QUICKSIGHT_DASHBOARD_VISUAL_NAME,
        quick_sight_sheet_id=QUICKSIGHT_SHEET_ID,
        quick_sight_sheet_name=QUICKSIGHT_SHEET_NAME,
        quick_sight_dashboard_qualified_name=str(quick_sight_dashboard.qualified_name),
        connection_qualified_name=connection.qualified_name,
        quick_sight_id=QUICKSIGHT_DASHBOARD_VISUAL_ID,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=QuickSightDashboardVisual)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=QuickSightDashboardVisual)


def test_sight_folder(
    client: AtlanClient, connection: Connection, quick_sight_folder: QuickSightFolder
):
    assert quick_sight_folder
    assert quick_sight_folder.guid
    assert quick_sight_folder.qualified_name
    assert quick_sight_folder.name == QUICKSIGHT_FOLDER_NAME
    assert quick_sight_folder.quick_sight_id == QUICKSIGHT_FOLDER_ID
    assert quick_sight_folder.connection_qualified_name == connection.qualified_name
    assert quick_sight_folder.connector_name == AtlanConnectorType.QUICKSIGHT.value
    assert quick_sight_folder.quick_sight_folder_type == QuickSightFolderType.SHARED

    to_update = quick_sight_folder.updater(
        name=quick_sight_folder.name, qualified_name=quick_sight_folder.qualified_name
    )
    to_update.description = QUICK_SIGHT_DESCRIPTION
    response = client.asset.save(to_update)
    assert response and response.mutated_entities

    asset = client.asset.get_by_qualified_name(
        qualified_name=quick_sight_folder.qualified_name, asset_type=QuickSightFolder
    )
    assert asset
    assert asset.name == QUICKSIGHT_FOLDER_NAME
    assert asset.description == QUICK_SIGHT_DESCRIPTION
    assert asset.qualified_name == quick_sight_folder.qualified_name


def test_sight_dataset(
    client: AtlanClient, connection: Connection, quick_sight_dataset: QuickSightDataset
):
    assert quick_sight_dataset
    assert quick_sight_dataset.guid
    assert quick_sight_dataset.qualified_name
    assert quick_sight_dataset.name == QUICKSIGHT_DATASET_NAME
    assert quick_sight_dataset.quick_sight_id == QUICKSIGHT_DATASET_ID
    assert quick_sight_dataset.connection_qualified_name == connection.qualified_name
    assert quick_sight_dataset.connector_name == AtlanConnectorType.QUICKSIGHT.value
    assert (
        quick_sight_dataset.quick_sight_dataset_import_mode
        == QuickSightDatasetImportMode.SPICE
    )

    to_update = quick_sight_dataset.updater(
        name=quick_sight_dataset.name, qualified_name=quick_sight_dataset.qualified_name
    )
    to_update.description = QUICK_SIGHT_DESCRIPTION
    response = client.asset.save(to_update)
    assert response and response.mutated_entities

    asset = client.asset.get_by_qualified_name(
        qualified_name=quick_sight_dataset.qualified_name, asset_type=QuickSightDataset
    )
    assert asset
    assert asset.name == QUICKSIGHT_DATASET_NAME
    assert asset.description == QUICK_SIGHT_DESCRIPTION
    assert asset.qualified_name == quick_sight_dataset.qualified_name


def test_sight_dashboard(
    client: AtlanClient,
    connection: Connection,
    quick_sight_dashboard: QuickSightDashboard,
):
    assert quick_sight_dashboard
    assert quick_sight_dashboard.guid
    assert quick_sight_dashboard.qualified_name
    assert quick_sight_dashboard.name == QUICKSIGHT_DASHBOARD_NAME
    assert quick_sight_dashboard.quick_sight_id == QUICKSIGHT_DASHBOARD_ID
    assert quick_sight_dashboard.connection_qualified_name == connection.qualified_name
    assert quick_sight_dashboard.connector_name == AtlanConnectorType.QUICKSIGHT.value

    to_update = quick_sight_dashboard.updater(
        name=quick_sight_dashboard.name,
        qualified_name=quick_sight_dashboard.qualified_name,
    )
    to_update.description = QUICK_SIGHT_DESCRIPTION
    response = client.asset.save(to_update)
    assert response and response.mutated_entities

    asset = client.asset.get_by_qualified_name(
        qualified_name=quick_sight_dashboard.qualified_name,
        asset_type=QuickSightDashboard,
    )
    assert asset
    assert asset.name == QUICKSIGHT_DASHBOARD_NAME
    assert asset.description == QUICK_SIGHT_DESCRIPTION
    assert asset.qualified_name == quick_sight_dashboard.qualified_name


def test_sight_analysis(
    client: AtlanClient,
    connection: Connection,
    quick_sight_analysis: QuickSightAnalysis,
):
    assert quick_sight_analysis
    assert quick_sight_analysis.guid
    assert quick_sight_analysis.qualified_name
    assert quick_sight_analysis.name == QUICKSIGHT_ANALYSIS_NAME
    assert quick_sight_analysis.quick_sight_id == QUICKSIGHT_ANALYSIS_ID
    assert quick_sight_analysis.connection_qualified_name == connection.qualified_name
    assert quick_sight_analysis.connector_name == AtlanConnectorType.QUICKSIGHT.value

    to_update = quick_sight_analysis.updater(
        name=quick_sight_analysis.name,
        qualified_name=quick_sight_analysis.qualified_name,
    )
    to_update.description = QUICK_SIGHT_DESCRIPTION
    response = client.asset.save(to_update)
    assert response and response.mutated_entities

    asset = client.asset.get_by_qualified_name(
        qualified_name=quick_sight_analysis.qualified_name,
        asset_type=QuickSightAnalysis,
    )
    assert asset
    assert asset.name == QUICKSIGHT_ANALYSIS_NAME
    assert asset.description == QUICK_SIGHT_DESCRIPTION
    assert asset.qualified_name == quick_sight_analysis.qualified_name


def test_sight_dataset_field(
    client: AtlanClient,
    connection: Connection,
    quick_sight_dataset_field: QuickSightDatasetField,
    quick_sight_dataset: QuickSightDataset,
):
    assert quick_sight_dataset_field
    assert quick_sight_dataset_field.guid
    assert quick_sight_dataset_field.qualified_name
    assert quick_sight_dataset_field.name == QUICKSIGHT_DATASET_FIELD_NAME
    assert quick_sight_dataset_field.quick_sight_id == QUICKSIGHT_DATASET_FIELD_ID
    assert (
        quick_sight_dataset_field.connection_qualified_name == connection.qualified_name
    )
    assert (
        quick_sight_dataset_field.connector_name == AtlanConnectorType.QUICKSIGHT.value
    )
    assert (
        quick_sight_dataset_field.quick_sight_dataset_qualified_name
        == quick_sight_dataset.qualified_name
    )
    assert (
        quick_sight_dataset_field.quick_sight_dataset_field_type
        == QuickSightDatasetFieldType.STRING
    )

    to_update = quick_sight_dataset_field.updater(
        name=quick_sight_dataset_field.name,
        qualified_name=quick_sight_dataset_field.qualified_name,
    )
    to_update.description = QUICK_SIGHT_DESCRIPTION
    response = client.asset.save(to_update)
    assert response and response.mutated_entities

    asset = client.asset.get_by_qualified_name(
        qualified_name=quick_sight_dataset_field.qualified_name,
        asset_type=QuickSightDatasetField,
    )
    assert asset
    assert asset.name == QUICKSIGHT_DATASET_FIELD_NAME
    assert asset.description == QUICK_SIGHT_DESCRIPTION
    assert asset.qualified_name == quick_sight_dataset_field.qualified_name


def test_sight_analysis_visual(
    client: AtlanClient,
    connection: Connection,
    quick_sight_analysis_visual: QuickSightAnalysisVisual,
    quick_sight_analysis: QuickSightAnalysis,
):
    assert quick_sight_analysis_visual
    assert quick_sight_analysis_visual.guid
    assert quick_sight_analysis_visual.qualified_name
    assert quick_sight_analysis_visual.name == QUICKSIGHT_ANALYSIS_VISUAL_NAME
    assert quick_sight_analysis_visual.quick_sight_id == QUICKSIGHT_ANALYSIS_VISUAL_ID
    assert (
        quick_sight_analysis_visual.connection_qualified_name
        == connection.qualified_name
    )
    assert (
        quick_sight_analysis_visual.connector_name
        == AtlanConnectorType.QUICKSIGHT.value
    )
    assert (
        quick_sight_analysis_visual.quick_sight_analysis_qualified_name
        == quick_sight_analysis.qualified_name
    )
    assert quick_sight_analysis_visual.quick_sight_sheet_id == QUICKSIGHT_SHEET_ID
    assert quick_sight_analysis_visual.quick_sight_sheet_name == QUICKSIGHT_SHEET_NAME

    to_update = quick_sight_analysis_visual.updater(
        name=quick_sight_analysis_visual.name,
        qualified_name=quick_sight_analysis_visual.qualified_name,
    )
    to_update.description = QUICK_SIGHT_DESCRIPTION
    response = client.asset.save(to_update)
    assert response and response.mutated_entities

    asset = client.asset.get_by_qualified_name(
        qualified_name=quick_sight_analysis_visual.qualified_name,
        asset_type=QuickSightAnalysisVisual,
    )
    assert asset
    assert asset.name == QUICKSIGHT_ANALYSIS_VISUAL_NAME
    assert asset.description == QUICK_SIGHT_DESCRIPTION
    assert asset.qualified_name == quick_sight_analysis_visual.qualified_name


def test_sight_dashboard_visual(
    client: AtlanClient,
    connection: Connection,
    quick_sight_dashboard_visual: QuickSightDashboardVisual,
    quick_sight_dashboard: QuickSightDashboard,
):
    assert quick_sight_dashboard_visual
    assert quick_sight_dashboard_visual.guid
    assert quick_sight_dashboard_visual.qualified_name
    assert quick_sight_dashboard_visual.name == QUICKSIGHT_DASHBOARD_VISUAL_NAME
    assert quick_sight_dashboard_visual.quick_sight_id == QUICKSIGHT_DASHBOARD_VISUAL_ID
    assert (
        quick_sight_dashboard_visual.connection_qualified_name
        == connection.qualified_name
    )
    assert (
        quick_sight_dashboard_visual.connector_name
        == AtlanConnectorType.QUICKSIGHT.value
    )
    assert (
        quick_sight_dashboard_visual.quick_sight_dashboard_qualified_name
        == quick_sight_dashboard.qualified_name
    )
    assert quick_sight_dashboard_visual.quick_sight_sheet_id == QUICKSIGHT_SHEET_ID
    assert quick_sight_dashboard_visual.quick_sight_sheet_name == QUICKSIGHT_SHEET_NAME

    to_update = quick_sight_dashboard_visual.updater(
        name=quick_sight_dashboard_visual.name,
        qualified_name=quick_sight_dashboard_visual.qualified_name,
    )
    to_update.description = QUICK_SIGHT_DESCRIPTION
    response = client.asset.save(to_update)
    assert response and response.mutated_entities

    asset = client.asset.get_by_qualified_name(
        qualified_name=quick_sight_dashboard_visual.qualified_name,
        asset_type=QuickSightDashboardVisual,
    )
    assert asset
    assert asset.name == QUICKSIGHT_DASHBOARD_VISUAL_NAME
    assert asset.description == QUICK_SIGHT_DESCRIPTION
    assert asset.qualified_name == quick_sight_dashboard_visual.qualified_name
