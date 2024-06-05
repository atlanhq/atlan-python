from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Connection,
    PresetChart,
    PresetDashboard,
    PresetDataset,
    PresetWorkspace,
)
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
)
from pyatlan.model.response import AssetMutationResponse
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection
from tests.integration.utils import block

MODULE_NAME = TestId.make_unique("PRESET")

CONNECTOR_TYPE = AtlanConnectorType.PRESET
PRESET_WORKSPACE_NAME = MODULE_NAME + "-ws"
PRESET_DASHBOARD_NAME = MODULE_NAME + "-coll"
PRESET_DATASET_NAME = MODULE_NAME + "-ds"
PRESET_CHART_NAME = MODULE_NAME + "-cht"
PRESET_DASHBOARD_NAME_OVERLOAD = MODULE_NAME + "-overload-coll"
PRESET_DATASET_NAME_OVERLOAD = MODULE_NAME + "-overload-ds"
PRESET_CHART_NAME_OVERLOAD = MODULE_NAME + "-overload-cht"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."

response = block(AtlanClient(), AssetMutationResponse())


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def preset_workspace(
    client: AtlanClient, connection: Connection
) -> Generator[PresetWorkspace, None, None]:
    assert connection.qualified_name
    to_create = PresetWorkspace.create(
        name=PRESET_WORKSPACE_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=PresetWorkspace)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=PresetWorkspace)


def test_preset_workspace(
    client: AtlanClient,
    preset_workspace: PresetWorkspace,
    connection: Connection,
):
    assert preset_workspace
    assert preset_workspace.guid
    assert preset_workspace.qualified_name
    assert preset_workspace.connection_qualified_name == connection.qualified_name
    assert preset_workspace.name == PRESET_WORKSPACE_NAME
    assert preset_workspace.connector_name == AtlanConnectorType.PRESET.value


@pytest.fixture(scope="module")
def preset_dashboard(
    client: AtlanClient, connection: Connection, preset_workspace: PresetWorkspace
) -> Generator[PresetDashboard, None, None]:
    assert preset_workspace.qualified_name
    to_create = PresetDashboard.create(
        name=PRESET_DASHBOARD_NAME,
        preset_workspace_qualified_name=preset_workspace.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=PresetDashboard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=PresetDashboard)


def test_preset_dashboard(
    client: AtlanClient,
    preset_dashboard: PresetDashboard,
    connection: Connection,
):
    assert preset_dashboard
    assert preset_dashboard.guid
    assert preset_dashboard.qualified_name
    assert preset_dashboard.connection_qualified_name == connection.qualified_name
    assert preset_dashboard.name == PRESET_DASHBOARD_NAME
    assert preset_dashboard.connector_name == AtlanConnectorType.PRESET.value


@pytest.fixture(scope="module")
def preset_dashboard_overload(
    client: AtlanClient, connection: Connection, preset_workspace: PresetWorkspace
) -> Generator[PresetDashboard, None, None]:
    assert preset_workspace.qualified_name
    assert connection.qualified_name
    to_create = PresetDashboard.creator(
        name=PRESET_DASHBOARD_NAME_OVERLOAD,
        preset_workspace_qualified_name=preset_workspace.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=PresetDashboard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=PresetDashboard)


def test_overload_preset_dashboard(
    client: AtlanClient,
    preset_dashboard_overload: PresetDashboard,
    connection: Connection,
):
    assert preset_dashboard_overload
    assert preset_dashboard_overload.guid
    assert preset_dashboard_overload.qualified_name
    assert (
        preset_dashboard_overload.connection_qualified_name == connection.qualified_name
    )
    assert preset_dashboard_overload.name == PRESET_DASHBOARD_NAME_OVERLOAD
    assert preset_dashboard_overload.connector_name == AtlanConnectorType.PRESET.value


@pytest.fixture(scope="module")
def preset_chart(
    client: AtlanClient, preset_dashboard: PresetDashboard
) -> Generator[PresetChart, None, None]:
    assert preset_dashboard.qualified_name
    to_create = PresetChart.create(
        name=PRESET_CHART_NAME,
        preset_dashboard_qualified_name=preset_dashboard.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=PresetChart)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=PresetChart)


def test_preset_chart(
    client: AtlanClient,
    preset_chart: PresetChart,
    preset_dashboard: PresetDashboard,
):
    assert preset_chart
    assert preset_chart.guid
    assert preset_chart.qualified_name
    assert (
        preset_chart.preset_dashboard_qualified_name == preset_dashboard.qualified_name
    )
    assert preset_chart.name == PRESET_CHART_NAME
    assert preset_chart.connector_name == AtlanConnectorType.PRESET.value


@pytest.fixture(scope="module")
def preset_chart_overload(
    client: AtlanClient,
    preset_dashboard_overload: PresetDashboard,
    connection: Connection,
) -> Generator[PresetChart, None, None]:
    assert preset_dashboard_overload.qualified_name
    assert connection.qualified_name
    to_create = PresetChart.creator(
        name=PRESET_CHART_NAME_OVERLOAD,
        preset_dashboard_qualified_name=preset_dashboard_overload.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=PresetChart)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=PresetChart)


def test_overload_preset_chart(
    client: AtlanClient,
    preset_chart_overload: PresetChart,
    preset_dashboard_overload: PresetDashboard,
):
    assert preset_chart_overload
    assert preset_chart_overload.guid
    assert preset_chart_overload.qualified_name
    assert (
        preset_chart_overload.preset_dashboard_qualified_name
        == preset_dashboard_overload.qualified_name
    )
    assert preset_chart_overload.name == PRESET_CHART_NAME_OVERLOAD
    assert preset_chart_overload.connector_name == AtlanConnectorType.PRESET.value


@pytest.fixture(scope="module")
def preset_dataset(
    client: AtlanClient, connection: Connection, preset_dashboard: PresetDashboard
) -> Generator[PresetDataset, None, None]:
    assert preset_dashboard.qualified_name
    to_create = PresetDataset.create(
        name=PRESET_DATASET_NAME,
        preset_dashboard_qualified_name=preset_dashboard.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=PresetDataset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=PresetDataset)


def test_preset_dataset(
    client: AtlanClient,
    preset_dataset: PresetDataset,
    connection: Connection,
):
    assert preset_dataset
    assert preset_dataset.guid
    assert preset_dataset.qualified_name
    assert preset_dataset.connection_qualified_name == connection.qualified_name
    assert preset_dataset.name == PRESET_DATASET_NAME
    assert preset_dataset.connector_name == AtlanConnectorType.PRESET.value


@pytest.fixture(scope="module")
def preset_dataset_overload(
    client: AtlanClient,
    connection: Connection,
    preset_dashboard_overload: PresetDashboard,
) -> Generator[PresetDataset, None, None]:
    assert preset_dashboard_overload.qualified_name
    assert connection.qualified_name
    to_create = PresetDataset.creator(
        name=PRESET_DATASET_NAME_OVERLOAD,
        preset_dashboard_qualified_name=preset_dashboard_overload.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=PresetDataset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=PresetDataset)


def test_overload_preset_dataset(
    client: AtlanClient,
    preset_dataset_overload: PresetDataset,
    connection: Connection,
):
    assert preset_dataset_overload
    assert preset_dataset_overload.guid
    assert preset_dataset_overload.qualified_name
    assert (
        preset_dataset_overload.connection_qualified_name == connection.qualified_name
    )
    assert preset_dataset_overload.name == PRESET_DATASET_NAME_OVERLOAD
    assert preset_dataset_overload.connector_name == AtlanConnectorType.PRESET.value


def test_update_preset_dashboard(
    client: AtlanClient,
    preset_dashboard: PresetDashboard,
):
    assert preset_dashboard.qualified_name
    assert preset_dashboard.name
    updated = client.asset.update_certificate(
        asset_type=PresetDashboard,
        qualified_name=preset_dashboard.qualified_name,
        name=PRESET_DASHBOARD_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert preset_dashboard.qualified_name
    assert preset_dashboard.name
    updated = client.asset.update_announcement(
        asset_type=PresetDashboard,
        qualified_name=preset_dashboard.qualified_name,
        name=PRESET_DASHBOARD_NAME,
        announcement=Announcement(
            announcement_type=ANNOUNCEMENT_TYPE,
            announcement_title=ANNOUNCEMENT_TITLE,
            announcement_message=ANNOUNCEMENT_MESSAGE,
        ),
    )
    assert updated
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE


def test_update_preset_chart(
    client: AtlanClient,
    preset_chart: PresetChart,
):
    assert preset_chart.qualified_name
    assert preset_chart.name
    updated = client.asset.update_certificate(
        asset_type=PresetChart,
        qualified_name=preset_chart.qualified_name,
        name=PRESET_CHART_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert preset_chart.qualified_name
    assert preset_chart.name
    updated = client.asset.update_announcement(
        asset_type=PresetChart,
        qualified_name=preset_chart.qualified_name,
        name=PRESET_CHART_NAME,
        announcement=Announcement(
            announcement_type=ANNOUNCEMENT_TYPE,
            announcement_title=ANNOUNCEMENT_TITLE,
            announcement_message=ANNOUNCEMENT_MESSAGE,
        ),
    )
    assert updated
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE


@pytest.mark.order(after="test_update_preset_dashboard")
def test_retrieve_preset_dashboard(
    client: AtlanClient,
    preset_dashboard: PresetDashboard,
):
    b = client.asset.get_by_guid(preset_dashboard.guid, asset_type=PresetDashboard)
    assert b
    assert not b.is_incomplete
    assert b.guid == preset_dashboard.guid
    assert b.qualified_name == preset_dashboard.qualified_name
    assert b.name == PRESET_DASHBOARD_NAME
    assert b.connector_name == AtlanConnectorType.PRESET.value
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_preset_dashboard")
def test_update_preset_dashboard_again(
    client: AtlanClient,
    preset_dashboard: PresetDashboard,
):
    assert preset_dashboard.qualified_name
    assert preset_dashboard.name
    updated = client.asset.remove_certificate(
        asset_type=PresetDashboard,
        qualified_name=preset_dashboard.qualified_name,
        name=preset_dashboard.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert preset_dashboard.qualified_name
    updated = client.asset.remove_announcement(
        qualified_name=preset_dashboard.qualified_name,
        asset_type=PresetDashboard,
        name=preset_dashboard.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_preset_dashboard_again")
def test_delete_preset_dashboard(
    client: AtlanClient, preset_dashboard: PresetDashboard
):
    response = client.asset.delete_by_guid(preset_dashboard.guid)
    assert response
    assert not response.assets_created(asset_type=PresetDashboard)
    assert not response.assets_updated(asset_type=PresetDashboard)
    deleted = response.assets_deleted(asset_type=PresetDashboard)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == preset_dashboard.guid
    assert deleted[0].qualified_name == preset_dashboard.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_preset_dashboard")
def test_restore_dashboard(
    client: AtlanClient,
    preset_dashboard: PresetDashboard,
):
    assert preset_dashboard.qualified_name
    assert client.asset.restore(
        asset_type=PresetDashboard, qualified_name=preset_dashboard.qualified_name
    )
    assert preset_dashboard.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=PresetDashboard, qualified_name=preset_dashboard.qualified_name
    )
    assert restored
    assert restored.guid == preset_dashboard.guid
    assert restored.qualified_name == preset_dashboard.qualified_name
    assert restored.status == EntityStatus.ACTIVE
