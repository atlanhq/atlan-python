from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, DataStudioAsset
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
    GoogleDatastudioAssetType,
)
from pyatlan.model.response import AssetMutationResponse
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection
from tests.integration.utils import block

MODULE_NAME = TestId.make_unique("datastudio")

CONNECTOR_TYPE = AtlanConnectorType.DATASTUDIO
REPORT_NAME = f"{MODULE_NAME}-report"
SOURCE_NAME = f"{MODULE_NAME}-source"
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
def data_studio_asset_report(
    client: AtlanClient, connection: Connection
) -> Generator[DataStudioAsset, None, None]:
    assert connection.qualified_name
    to_create = DataStudioAsset.create(
        name=REPORT_NAME,
        connection_qualified_name=connection.qualified_name,
        data_studio_asset_type=GoogleDatastudioAssetType.REPORT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataStudioAsset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataStudioAsset)


def test_data_studio_asset_report(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_report: DataStudioAsset,
):
    assert data_studio_asset_report
    assert data_studio_asset_report.guid
    assert data_studio_asset_report.qualified_name
    assert (
        data_studio_asset_report.connection_qualified_name == connection.qualified_name
    )
    assert data_studio_asset_report.name == REPORT_NAME
    assert (
        data_studio_asset_report.connector_name == AtlanConnectorType.DATASTUDIO.value
    )
    assert (
        data_studio_asset_report.data_studio_asset_type
        == GoogleDatastudioAssetType.REPORT
    )


def test_update_data_studio_asset_report(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_report: DataStudioAsset,
):
    assert data_studio_asset_report.qualified_name
    assert data_studio_asset_report.name
    updated = client.asset.update_certificate(
        asset_type=DataStudioAsset,
        qualified_name=data_studio_asset_report.qualified_name,
        name=SOURCE_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert data_studio_asset_report.qualified_name
    assert data_studio_asset_report
    updated = client.asset.update_announcement(
        asset_type=DataStudioAsset,
        qualified_name=data_studio_asset_report.qualified_name,
        name=SOURCE_NAME,
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


@pytest.fixture(scope="module")
def data_studio_asset_data_source(
    client: AtlanClient, connection: Connection
) -> Generator[DataStudioAsset, None, None]:
    assert connection.qualified_name
    to_create = DataStudioAsset.create(
        name=SOURCE_NAME,
        connection_qualified_name=connection.qualified_name,
        data_studio_asset_type=GoogleDatastudioAssetType.DATA_SOURCE,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=DataStudioAsset)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=DataStudioAsset)


def test_data_studio_asset_data_source(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_data_source: DataStudioAsset,
):
    assert data_studio_asset_data_source
    assert data_studio_asset_data_source.guid
    assert data_studio_asset_data_source.qualified_name
    assert (
        data_studio_asset_data_source.connection_qualified_name
        == connection.qualified_name
    )
    assert data_studio_asset_data_source.name == SOURCE_NAME
    assert (
        data_studio_asset_data_source.connector_name
        == AtlanConnectorType.DATASTUDIO.value
    )
    assert (
        data_studio_asset_data_source.data_studio_asset_type
        == GoogleDatastudioAssetType.DATA_SOURCE
    )


def test_update_data_studio_asset_data_source(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_data_source: DataStudioAsset,
):
    assert data_studio_asset_data_source.connection_qualified_name
    assert data_studio_asset_data_source.qualified_name
    assert data_studio_asset_data_source.name
    updated = client.asset.update_certificate(
        asset_type=DataStudioAsset,
        qualified_name=data_studio_asset_data_source.qualified_name,
        name=SOURCE_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert data_studio_asset_data_source.qualified_name
    assert data_studio_asset_data_source
    updated = client.asset.update_announcement(
        asset_type=DataStudioAsset,
        qualified_name=data_studio_asset_data_source.qualified_name,
        name=SOURCE_NAME,
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


@pytest.mark.order(after="test_update_data_studio_asset_data_source")
def test_retrieve_data_studio_asset_data_source(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_data_source: DataStudioAsset,
):
    b = client.asset.get_by_guid(
        data_studio_asset_data_source.guid, asset_type=DataStudioAsset
    )
    assert b
    assert not b.is_incomplete
    assert b.guid == data_studio_asset_data_source.guid
    assert b.qualified_name == data_studio_asset_data_source.qualified_name
    assert b.name == SOURCE_NAME
    assert b.connector_name == AtlanConnectorType.DATASTUDIO.value
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_data_studio_asset_data_source")
def test_update_data_studio_asset_data_source_again(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_data_source: DataStudioAsset,
):
    assert data_studio_asset_data_source.qualified_name
    assert data_studio_asset_data_source.name
    updated = client.asset.remove_certificate(
        asset_type=DataStudioAsset,
        qualified_name=data_studio_asset_data_source.qualified_name,
        name=SOURCE_NAME,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert data_studio_asset_data_source.qualified_name
    updated = client.asset.remove_announcement(
        asset_type=DataStudioAsset,
        qualified_name=data_studio_asset_data_source.qualified_name,
        name=SOURCE_NAME,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_data_studio_asset_data_source_again")
def test_delete_data_studio_asset_data_source(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_data_source: DataStudioAsset,
):
    response = client.asset.delete_by_guid(data_studio_asset_data_source.guid)
    assert response
    assert not response.assets_created(asset_type=DataStudioAsset)
    assert not response.assets_updated(asset_type=DataStudioAsset)
    deleted = response.assets_deleted(asset_type=DataStudioAsset)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == data_studio_asset_data_source.guid
    assert deleted[0].qualified_name == data_studio_asset_data_source.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_data_studio_asset_data_source")
def test_read_deleted_data_studio_asset_data_source(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_data_source: DataStudioAsset,
):
    deleted = client.asset.get_by_guid(
        data_studio_asset_data_source.guid, asset_type=DataStudioAsset
    )
    assert deleted
    assert deleted.guid == data_studio_asset_data_source.guid
    assert deleted.qualified_name == data_studio_asset_data_source.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_data_studio_asset_data_source")
def test_restore_data_studio_asset_data_source(
    client: AtlanClient,
    connection: Connection,
    data_studio_asset_data_source: DataStudioAsset,
):
    assert data_studio_asset_data_source.qualified_name
    assert client.asset.restore(
        asset_type=DataStudioAsset,
        qualified_name=data_studio_asset_data_source.qualified_name,
    )
    assert data_studio_asset_data_source.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=DataStudioAsset,
        qualified_name=data_studio_asset_data_source.qualified_name,
    )
    assert restored
    assert restored.guid == data_studio_asset_data_source.guid
    assert restored.qualified_name == data_studio_asset_data_source.qualified_name
    assert restored.status == EntityStatus.ACTIVE
