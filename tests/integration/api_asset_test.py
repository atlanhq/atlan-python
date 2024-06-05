from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import APIPath, APISpec, Connection
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

MODULE_NAME = TestId.make_unique("API")

CONNECTOR_TYPE = AtlanConnectorType.API
API_SPEC_NAME = "api-spec"
API_PATH_NAME = "/api/path"
API_PATH_NAME_OVERLOAD = "/api/path/overload"
API_CONNECTION_QUALIFIED_NAME = "default/api/1696792060"
API_QUALIFIED_NAME = f"{API_CONNECTION_QUALIFIED_NAME}/{API_SPEC_NAME}"
API_PATH_RAW_URI = "/api/path"
API_PATH_RAW_URI_OVERLOAD = "/api/path/overload"
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
def api_spec(
    client: AtlanClient, connection: Connection
) -> Generator[APISpec, None, None]:
    assert connection.qualified_name
    to_create = APISpec.create(
        name=API_SPEC_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APISpec)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APISpec)


def test_api_spec(client: AtlanClient, connection: Connection, api_spec: APISpec):
    assert api_spec
    assert api_spec.guid
    assert api_spec.qualified_name
    assert api_spec.name == API_SPEC_NAME
    assert api_spec.connection_qualified_name == connection.qualified_name
    assert api_spec.connector_name == AtlanConnectorType.API.value


@pytest.fixture(scope="module")
def api_path(client: AtlanClient, api_spec: APISpec) -> Generator[APIPath, None, None]:
    assert api_spec.qualified_name
    to_create = APIPath.create(
        path_raw_uri=API_PATH_RAW_URI,
        spec_qualified_name=api_spec.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIPath)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIPath)


def test_api_path(client: AtlanClient, api_spec: APISpec, api_path: APIPath):
    assert api_path
    assert api_path.guid
    assert api_path.qualified_name
    assert api_path.api_spec_qualified_name
    assert api_path.api_path_raw_u_r_i == API_PATH_RAW_URI
    assert api_path.name == API_PATH_NAME
    assert api_path.connection_qualified_name == api_spec.connection_qualified_name
    assert api_path.connector_name == AtlanConnectorType.API.value


@pytest.fixture(scope="module")
def api_path_overload(
    client: AtlanClient, api_spec: APISpec
) -> Generator[APIPath, None, None]:
    assert api_spec.qualified_name
    to_create = APIPath.creator(
        path_raw_uri=API_PATH_RAW_URI_OVERLOAD,
        spec_qualified_name=api_spec.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIPath)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIPath)


def test_overload_api_path(
    client: AtlanClient, api_spec: APISpec, api_path_overload: APIPath
):
    assert api_path_overload
    assert api_path_overload.guid
    assert api_path_overload.qualified_name
    assert api_path_overload.api_spec_qualified_name
    assert api_path_overload.api_path_raw_u_r_i == API_PATH_RAW_URI_OVERLOAD
    assert api_path_overload.name == API_PATH_NAME_OVERLOAD
    assert (
        api_path_overload.connection_qualified_name
        == api_spec.connection_qualified_name
    )
    assert api_path_overload.connector_name == AtlanConnectorType.API.value


def test_update_api_path(
    client: AtlanClient, connection: Connection, api_spec: APISpec, api_path: APIPath
):
    assert api_path.qualified_name
    assert api_path.name
    updated = client.asset.update_certificate(
        asset_type=APIPath,
        qualified_name=api_path.qualified_name,
        name=api_path.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert api_path.qualified_name
    assert api_path.name
    updated = client.asset.update_announcement(
        asset_type=APIPath,
        qualified_name=api_path.qualified_name,
        name=api_path.name,
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


@pytest.mark.order(after="test_update_api_path")
def test_retrieve_api_path(
    client: AtlanClient, connection: Connection, api_spec: APISpec, api_path: APIPath
):
    b = client.asset.get_by_guid(api_path.guid, asset_type=APIPath)
    assert b
    assert not b.is_incomplete
    assert b.guid == api_path.guid
    assert b.qualified_name == api_path.qualified_name
    assert b.name == api_path.name
    assert b.connector_name == api_path.connector_name
    assert b.connection_qualified_name == api_path.connection_qualified_name
    assert b.api_path_raw_u_r_i == api_path.api_path_raw_u_r_i
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_api_path")
def test_update_api_path_again(
    client: AtlanClient, connection: Connection, api_spec: APISpec, api_path: APIPath
):
    assert api_path.qualified_name
    assert api_path.name
    updated = client.asset.remove_certificate(
        asset_type=APIPath,
        qualified_name=api_path.qualified_name,
        name=api_path.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert api_path.qualified_name
    updated = client.asset.remove_announcement(
        asset_type=APIPath,
        qualified_name=api_path.qualified_name,
        name=api_path.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_api_path_again")
def test_delete_api_path(
    client: AtlanClient, connection: Connection, api_spec: APISpec, api_path: APIPath
):
    response = client.asset.delete_by_guid(api_path.guid)
    assert response
    assert not response.assets_created(asset_type=APIPath)
    assert not response.assets_updated(asset_type=APIPath)
    deleted = response.assets_deleted(asset_type=APIPath)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == api_path.guid
    assert deleted[0].qualified_name == api_path.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_api_path")
def test_read_deleted_api_path(
    client: AtlanClient, connection: Connection, api_spec: APISpec, api_path: APIPath
):
    deleted = client.asset.get_by_guid(api_path.guid, asset_type=APIPath)
    assert deleted
    assert deleted.guid == api_path.guid
    assert deleted.qualified_name == api_path.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_api_path")
def test_restore_path(
    client: AtlanClient, connection: Connection, api_spec: APISpec, api_path: APIPath
):
    assert api_path.qualified_name
    assert client.asset.restore(
        asset_type=APIPath, qualified_name=api_path.qualified_name
    )
    assert api_path.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=APIPath, qualified_name=api_path.qualified_name
    )
    assert restored
    assert restored.guid == api_path.guid
    assert restored.qualified_name == api_path.qualified_name
    assert restored.status == EntityStatus.ACTIVE
