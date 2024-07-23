from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Connection,
    SupersetChart,
    SupersetDashboard,
    SupersetDataset,
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

MODULE_NAME = TestId.make_unique("SUPERSET")

CONNECTOR_TYPE = AtlanConnectorType.SUPERSET
SUPERSET_DASHBOARD_NAME = MODULE_NAME + "-dash"
SUPERSET_DATASET_NAME = MODULE_NAME + "-ds"
SUPERSET_CHART_NAME = MODULE_NAME + "-cht"
SUPERSET_DATASET_NAME_OVERLOAD = MODULE_NAME + "-overload-ds"
SUPERSET_CHART_NAME_OVERLOAD = MODULE_NAME + "-overload-cht"
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
def superset_dashboard(
    client: AtlanClient, connection: Connection
) -> Generator[SupersetDashboard, None, None]:
    assert connection.qualified_name
    to_create = SupersetDashboard.create(
        name=SUPERSET_DASHBOARD_NAME,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SupersetDashboard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SupersetDashboard)


def test_superset_dashboard(
    client: AtlanClient,
    superset_dashboard: SupersetDashboard,
    connection: Connection,
):
    assert superset_dashboard
    assert superset_dashboard.guid
    assert superset_dashboard.qualified_name
    assert superset_dashboard.connection_qualified_name == connection.qualified_name
    assert superset_dashboard.name == SUPERSET_DASHBOARD_NAME
    assert superset_dashboard.connector_name == AtlanConnectorType.SUPERSET.value


@pytest.fixture(scope="module")
def superset_chart(
    client: AtlanClient, superset_dashboard: SupersetDashboard
) -> Generator[SupersetChart, None, None]:
    assert superset_dashboard.qualified_name
    to_create = SupersetChart.create(
        name=SUPERSET_CHART_NAME,
        superset_dashboard_qualified_name=superset_dashboard.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SupersetChart)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SupersetChart)


def test_superset_chart(
    client: AtlanClient,
    superset_chart: SupersetChart,
    superset_dashboard: SupersetDashboard,
):
    assert superset_chart
    assert superset_chart.guid
    assert superset_chart.qualified_name
    assert (
        superset_chart.superset_dashboard_qualified_name
        == superset_dashboard.qualified_name
    )
    assert superset_chart.name == SUPERSET_CHART_NAME
    assert superset_chart.connector_name == AtlanConnectorType.SUPERSET.value


@pytest.fixture(scope="module")
def superset_chart_overload(
    client: AtlanClient,
    superset_dashboard: SupersetDashboard,
    connection: Connection,
) -> Generator[SupersetChart, None, None]:
    assert superset_dashboard.qualified_name
    assert connection.qualified_name
    to_create = SupersetChart.creator(
        name=SUPERSET_CHART_NAME_OVERLOAD,
        superset_dashboard_qualified_name=superset_dashboard.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SupersetChart)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SupersetChart)


def test_overload_superset_chart(
    client: AtlanClient,
    superset_chart_overload: SupersetChart,
    superset_dashboard: SupersetDashboard,
):
    assert superset_chart_overload
    assert superset_chart_overload.guid
    assert superset_chart_overload.qualified_name
    assert (
        superset_chart_overload.superset_dashboard_qualified_name
        == superset_dashboard.qualified_name
    )
    assert superset_chart_overload.name == SUPERSET_CHART_NAME_OVERLOAD
    assert superset_chart_overload.connector_name == AtlanConnectorType.SUPERSET.value


@pytest.fixture(scope="module")
def superset_dataset(
    client: AtlanClient, connection: Connection, superset_dashboard: SupersetDashboard
) -> Generator[SupersetDataset, None, None]:
    assert superset_dashboard.qualified_name
    to_create = SupersetDataset.create(
        name=SUPERSET_DATASET_NAME,
        superset_dashboard_qualified_name=superset_dashboard.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SupersetDataset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SupersetDataset)


def test_superset_dataset(
    client: AtlanClient,
    superset_dataset: SupersetDataset,
    connection: Connection,
):
    assert superset_dataset
    assert superset_dataset.guid
    assert superset_dataset.qualified_name
    assert superset_dataset.connection_qualified_name == connection.qualified_name
    assert superset_dataset.name == SUPERSET_DATASET_NAME
    assert superset_dataset.connector_name == AtlanConnectorType.SUPERSET.value


@pytest.fixture(scope="module")
def superset_dataset_overload(
    client: AtlanClient,
    connection: Connection,
    superset_dashboard: SupersetDashboard,
) -> Generator[SupersetDataset, None, None]:
    assert superset_dashboard.qualified_name
    assert connection.qualified_name
    to_create = SupersetDataset.creator(
        name=SUPERSET_DATASET_NAME_OVERLOAD,
        superset_dashboard_qualified_name=superset_dashboard.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SupersetDataset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SupersetDataset)


def test_overload_superset_dataset(
    client: AtlanClient,
    superset_dataset_overload: SupersetDataset,
    connection: Connection,
):
    assert superset_dataset_overload
    assert superset_dataset_overload.guid
    assert superset_dataset_overload.qualified_name
    assert (
        superset_dataset_overload.connection_qualified_name == connection.qualified_name
    )
    assert superset_dataset_overload.name == SUPERSET_DATASET_NAME_OVERLOAD
    assert superset_dataset_overload.connector_name == AtlanConnectorType.SUPERSET.value


def test_update_superset_dashboard(
    client: AtlanClient,
    superset_dashboard: SupersetDashboard,
):
    assert superset_dashboard.qualified_name
    assert superset_dashboard.name
    updated = client.asset.update_certificate(
        asset_type=SupersetDashboard,
        qualified_name=superset_dashboard.qualified_name,
        name=SUPERSET_DASHBOARD_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert superset_dashboard.qualified_name
    assert superset_dashboard.name
    updated = client.asset.update_announcement(
        asset_type=SupersetDashboard,
        qualified_name=superset_dashboard.qualified_name,
        name=SUPERSET_DASHBOARD_NAME,
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


def test_update_superset_chart(
    client: AtlanClient,
    superset_chart: SupersetChart,
):
    assert superset_chart.qualified_name
    assert superset_chart.name
    updated = client.asset.update_certificate(
        asset_type=SupersetChart,
        qualified_name=superset_chart.qualified_name,
        name=SUPERSET_CHART_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert superset_chart.qualified_name
    assert superset_chart.name
    updated = client.asset.update_announcement(
        asset_type=SupersetChart,
        qualified_name=superset_chart.qualified_name,
        name=SUPERSET_CHART_NAME,
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


@pytest.mark.order(after="test_update_superset_dashboard")
def test_retrieve_superset_dashboard(
    client: AtlanClient,
    superset_dashboard: SupersetDashboard,
):
    b = client.asset.get_by_guid(superset_dashboard.guid, asset_type=SupersetDashboard)
    assert b
    assert not b.is_incomplete
    assert b.guid == superset_dashboard.guid
    assert b.qualified_name == superset_dashboard.qualified_name
    assert b.name == SUPERSET_DASHBOARD_NAME
    assert b.connector_name == AtlanConnectorType.SUPERSET.value
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_superset_dashboard")
def test_update_superset_dashboard_again(
    client: AtlanClient,
    superset_dashboard: SupersetDashboard,
):
    assert superset_dashboard.qualified_name
    assert superset_dashboard.name
    updated = client.asset.remove_certificate(
        asset_type=SupersetDashboard,
        qualified_name=superset_dashboard.qualified_name,
        name=superset_dashboard.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert superset_dashboard.qualified_name
    updated = client.asset.remove_announcement(
        qualified_name=superset_dashboard.qualified_name,
        asset_type=SupersetDashboard,
        name=superset_dashboard.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_superset_dashboard_again")
def test_delete_superset_dashboard(
    client: AtlanClient, superset_dashboard: SupersetDashboard
):
    response = client.asset.delete_by_guid(superset_dashboard.guid)
    assert response
    assert not response.assets_created(asset_type=SupersetDashboard)
    assert not response.assets_updated(asset_type=SupersetDashboard)
    deleted = response.assets_deleted(asset_type=SupersetDashboard)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == superset_dashboard.guid
    assert deleted[0].qualified_name == superset_dashboard.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_superset_dashboard")
def test_restore_dashboard(
    client: AtlanClient,
    superset_dashboard: SupersetDashboard,
):
    assert superset_dashboard.qualified_name
    assert client.asset.restore(
        asset_type=SupersetDashboard, qualified_name=superset_dashboard.qualified_name
    )
    assert superset_dashboard.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=SupersetDashboard, qualified_name=superset_dashboard.qualified_name
    )
    assert restored
    assert restored.guid == superset_dashboard.guid
    assert restored.qualified_name == superset_dashboard.qualified_name
    assert restored.status == EntityStatus.ACTIVE
