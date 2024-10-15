from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    APIField,
    APIObject,
    APIPath,
    APIQuery,
    APISpec,
    Connection,
)
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    APIQueryParamTypeEnum,
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
API_SPEC_NAME = f"{MODULE_NAME}-api-spec"
API_PATH_NAME = "/api/path"
API_PATH_NAME_OVERLOAD = "/api/path/overload"
API_PATH_RAW_URI = "/api/path"
API_PATH_RAW_URI_OVERLOAD = "/api/path/overload"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."
API_OBJECT_NAME = f"{MODULE_NAME}-api-object"
API_OBJECT_OVERLOAD_NAME = f"{MODULE_NAME}-api-object-overload"
API_OBJECT_FIELD_COUNT = 2
API_QUERY_NAME = "api-query"
API_QUERY_OVERLOAD_1_NAME = f"{MODULE_NAME}-api-query-overload-1"
API_QUERY_OVERLOAD_2_NAME = f"{MODULE_NAME}-api-query-overload-2"
API_QUERY_OVERLOAD_3_NAME = f"{MODULE_NAME}-api-query-overload-3"
API_QUERY_INPUT_FIELD_COUNT = 1
API_QUERY_OUTPUT_TYPE = "String"
API_QUERY_OUTPUT_TYPE_SECONDARY = "String"
API_QUERY_IS_OBJECT_REFERENCE = True
API_FIELD_NAME = f"{MODULE_NAME}-api-field"
API_FIELD_PARENT_QUERY_NAME = f"{MODULE_NAME}-api-field-pq"
API_FIELD_OVERLOAD_1_NAME = f"{MODULE_NAME}-api-field-overload-1"
API_FIELD_OVERLOAD_2_NAME = f"{MODULE_NAME}-api-field-overload-2"
API_FIELD_OVERLOAD_3_NAME = f"{MODULE_NAME}-api-field-overload-3"
API_FIELD_OVERLOAD_4_NAME = f"{MODULE_NAME}-api-field-overload-4"
API_FIELD_TYPE = "Int"
API_FIELD_TYPE_SECONDARY = "Int"
API_FIELD_IS_OBJECT_REFERENCE = True
API_FIELD_REFERENCE_OBJECT_NAME = f"{MODULE_NAME}-api-object-reference"


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


# here
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


@pytest.fixture(scope="module")
def api_object(
    client: AtlanClient, connection: Connection
) -> Generator[APIObject, None, None]:
    assert connection.qualified_name
    to_create = APIObject.creator(
        name=API_OBJECT_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIObject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIObject)


def test_api_object(client: AtlanClient, connection: Connection, api_object: APIObject):
    assert api_object
    assert api_object.guid
    assert api_object.name == API_OBJECT_NAME
    assert api_object.connection_qualified_name == connection.qualified_name
    assert api_object.connector_name == AtlanConnectorType.API.value
    assert api_object.qualified_name == f"{connection.qualified_name}/{API_OBJECT_NAME}"


@pytest.fixture(scope="module")
def api_object_overload(
    client: AtlanClient, connection: Connection
) -> Generator[APIObject, None, None]:
    assert connection.qualified_name
    to_create = APIObject.creator(
        name=API_OBJECT_OVERLOAD_NAME,
        connection_qualified_name=connection.qualified_name,
        api_field_count=API_OBJECT_FIELD_COUNT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIObject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIObject)


def test_api_object_overload(
    client: AtlanClient, connection: Connection, api_object_overload: APIObject
):
    assert api_object_overload
    assert api_object_overload.guid
    assert (
        api_object_overload.qualified_name
        == f"{connection.qualified_name}/{API_OBJECT_OVERLOAD_NAME}"
    )
    assert api_object_overload.name == API_OBJECT_OVERLOAD_NAME
    assert api_object_overload.connection_qualified_name == connection.qualified_name
    assert api_object_overload.api_field_count == API_OBJECT_FIELD_COUNT
    assert api_object_overload.connector_name == AtlanConnectorType.API.value


def test_update_api_object(
    client: AtlanClient, connection: Connection, api_object_overload: APIObject
):
    assert api_object_overload.qualified_name
    assert api_object_overload.name
    updated = client.asset.update_certificate(
        asset_type=APIObject,
        qualified_name=api_object_overload.qualified_name,
        name=api_object_overload.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert api_object_overload.qualified_name
    assert api_object_overload.name
    updated = client.asset.update_announcement(
        asset_type=APIObject,
        qualified_name=api_object_overload.qualified_name,
        name=api_object_overload.name,
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


@pytest.mark.order(after="test_update_api_object")
def test_retrieve_api_object(
    client: AtlanClient, connection: Connection, api_object_overload: APIObject
):
    b = client.asset.get_by_guid(api_object_overload.guid, asset_type=APIObject)
    assert b
    assert not b.is_incomplete
    assert b.guid == api_object_overload.guid
    assert b.qualified_name == api_object_overload.qualified_name
    assert b.name == api_object_overload.name
    assert b.connector_name == api_object_overload.connector_name
    assert b.connection_qualified_name == api_object_overload.connection_qualified_name
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_api_object")
def test_delete_api_object(
    client: AtlanClient, connection: Connection, api_object_overload: APIObject
):
    response = client.asset.delete_by_guid(api_object_overload.guid)
    assert response
    assert not response.assets_created(asset_type=APIObject)
    assert not response.assets_updated(asset_type=APIObject)
    deleted = response.assets_deleted(asset_type=APIObject)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == api_object_overload.guid
    assert deleted[0].qualified_name == api_object_overload.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_api_object")
def test_read_deleted_api_object(
    client: AtlanClient, connection: Connection, api_object_overload: APIObject
):
    deleted = client.asset.get_by_guid(api_object_overload.guid, asset_type=APIObject)
    assert deleted
    assert deleted.guid == api_object_overload.guid
    assert deleted.qualified_name == api_object_overload.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_api_object")
def test_restore_object(
    client: AtlanClient, connection: Connection, api_object_overload: APIObject
):
    assert api_object_overload.qualified_name
    assert client.asset.restore(
        asset_type=APIObject, qualified_name=api_object_overload.qualified_name
    )
    assert api_object_overload.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=APIObject, qualified_name=api_object_overload.qualified_name
    )
    assert restored
    assert restored.guid == api_object_overload.guid
    assert restored.qualified_name == api_object_overload.qualified_name
    assert restored.status == EntityStatus.ACTIVE


@pytest.fixture(scope="module")
def api_query(
    client: AtlanClient, connection: Connection
) -> Generator[APIQuery, None, None]:
    assert connection.qualified_name
    to_create = APIQuery.creator(
        name=API_QUERY_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIQuery)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIQuery)


def test_api_query(client: AtlanClient, connection: Connection, api_query: APIQuery):
    assert api_query
    assert api_query.guid
    assert api_query.qualified_name == f"{connection.qualified_name}/{API_QUERY_NAME}"
    assert api_query.name == API_QUERY_NAME
    assert api_query.connection_qualified_name == connection.qualified_name
    assert api_query.connector_name == AtlanConnectorType.API.value


@pytest.fixture(scope="module")
def api_query_overload_1(
    client: AtlanClient, connection: Connection
) -> Generator[APIQuery, None, None]:
    assert connection.qualified_name
    to_create = APIQuery.creator(
        name=API_QUERY_OVERLOAD_1_NAME,
        connection_qualified_name=connection.qualified_name,
        api_input_field_count=API_QUERY_INPUT_FIELD_COUNT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIQuery)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIQuery)


def test_api_query_overload_1(
    client: AtlanClient, connection: Connection, api_query_overload_1: APIQuery
):
    assert api_query_overload_1
    assert api_query_overload_1.guid
    assert (
        api_query_overload_1.qualified_name
        == f"{connection.qualified_name}/{API_QUERY_OVERLOAD_1_NAME}"
    )
    assert api_query_overload_1.name == API_QUERY_OVERLOAD_1_NAME
    assert api_query_overload_1.connection_qualified_name == connection.qualified_name
    assert api_query_overload_1.api_input_field_count == API_QUERY_INPUT_FIELD_COUNT
    assert api_query_overload_1.connector_name == AtlanConnectorType.API.value


@pytest.fixture(scope="module")
def api_query_overload_2(
    client: AtlanClient, connection: Connection
) -> Generator[APIQuery, None, None]:
    assert connection.qualified_name
    to_create = APIQuery.creator(
        name=API_QUERY_OVERLOAD_2_NAME,
        connection_qualified_name=connection.qualified_name,
        api_input_field_count=API_QUERY_INPUT_FIELD_COUNT,
        api_query_output_type=API_QUERY_OUTPUT_TYPE,
        api_query_output_type_secondary=API_QUERY_OUTPUT_TYPE_SECONDARY,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIQuery)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIQuery)


def test_api_query_overload_2(
    client: AtlanClient, connection: Connection, api_query_overload_2: APIQuery
):
    assert api_query_overload_2
    assert api_query_overload_2.guid
    assert (
        api_query_overload_2.qualified_name
        == f"{connection.qualified_name}/{API_QUERY_OVERLOAD_2_NAME}"
    )
    assert api_query_overload_2.name == API_QUERY_OVERLOAD_2_NAME
    assert api_query_overload_2.connection_qualified_name == connection.qualified_name
    assert api_query_overload_2.api_input_field_count == API_QUERY_INPUT_FIELD_COUNT
    assert api_query_overload_2.api_query_output_type == API_QUERY_OUTPUT_TYPE
    assert (
        api_query_overload_2.api_query_output_type_secondary
        == API_QUERY_OUTPUT_TYPE_SECONDARY
    )
    assert api_query_overload_2.connector_name == AtlanConnectorType.API.value


@pytest.fixture(scope="module")
def api_query_overload_3(
    client: AtlanClient, connection: Connection, api_object: APIObject
) -> Generator[APIQuery, None, None]:
    assert connection.qualified_name
    assert api_object.qualified_name
    to_create = APIQuery.creator(
        name=API_QUERY_OVERLOAD_3_NAME,
        connection_qualified_name=connection.qualified_name,
        api_input_field_count=API_QUERY_INPUT_FIELD_COUNT,
        api_query_output_type=API_QUERY_OUTPUT_TYPE,
        api_query_output_type_secondary=API_QUERY_OUTPUT_TYPE_SECONDARY,
        is_object_reference=API_QUERY_IS_OBJECT_REFERENCE,
        reference_api_object_qualified_name=api_object.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIQuery)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIQuery)


def test_api_query_overload_3(
    client: AtlanClient,
    connection: Connection,
    api_query_overload_3: APIQuery,
    api_object: APIObject,
):
    assert api_query_overload_3
    assert api_query_overload_3.guid
    assert (
        api_query_overload_3.qualified_name
        == f"{connection.qualified_name}/{API_QUERY_OVERLOAD_3_NAME}"
    )
    assert api_query_overload_3.name == API_QUERY_OVERLOAD_3_NAME
    assert api_query_overload_3.connection_qualified_name == connection.qualified_name
    assert api_query_overload_3.api_input_field_count == API_QUERY_INPUT_FIELD_COUNT
    assert api_query_overload_3.api_query_output_type == API_QUERY_OUTPUT_TYPE
    assert (
        api_query_overload_3.api_query_output_type_secondary
        == API_QUERY_OUTPUT_TYPE_SECONDARY
    )
    assert api_query_overload_3.api_is_object_reference == API_QUERY_IS_OBJECT_REFERENCE
    assert api_query_overload_3.api_object_qualified_name == api_object.qualified_name
    assert api_query_overload_3.connector_name == AtlanConnectorType.API.value


def test_update_api_query(
    client: AtlanClient, connection: Connection, api_query_overload_3: APIQuery
):
    assert api_query_overload_3.qualified_name
    assert api_query_overload_3.name
    updated = client.asset.update_certificate(
        asset_type=APIQuery,
        qualified_name=api_query_overload_3.qualified_name,
        name=api_query_overload_3.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert api_query_overload_3.qualified_name
    assert api_query_overload_3.name
    updated = client.asset.update_announcement(
        asset_type=APIQuery,
        qualified_name=api_query_overload_3.qualified_name,
        name=api_query_overload_3.name,
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


@pytest.mark.order(after="test_update_api_query")
def test_retrieve_api_query(
    client: AtlanClient, connection: Connection, api_query_overload_3: APIQuery
):
    b = client.asset.get_by_guid(api_query_overload_3.guid, asset_type=APIQuery)
    assert b
    assert not b.is_incomplete
    assert b.guid == api_query_overload_3.guid
    assert b.qualified_name == api_query_overload_3.qualified_name
    assert b.name == api_query_overload_3.name
    assert b.connector_name == api_query_overload_3.connector_name
    assert b.connection_qualified_name == api_query_overload_3.connection_qualified_name
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_api_query")
def test_delete_api_query(
    client: AtlanClient, connection: Connection, api_query_overload_3: APIQuery
):
    response = client.asset.delete_by_guid(api_query_overload_3.guid)
    assert response
    assert not response.assets_created(asset_type=APIQuery)
    assert not response.assets_updated(asset_type=APIQuery)
    deleted = response.assets_deleted(asset_type=APIQuery)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == api_query_overload_3.guid
    assert deleted[0].qualified_name == api_query_overload_3.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_api_query")
def test_read_deleted_api_query(
    client: AtlanClient, connection: Connection, api_query_overload_3: APIQuery
):
    deleted = client.asset.get_by_guid(api_query_overload_3.guid, asset_type=APIQuery)
    assert deleted
    assert deleted.guid == api_query_overload_3.guid
    assert deleted.qualified_name == api_query_overload_3.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_api_query")
def test_restore_query(
    client: AtlanClient, connection: Connection, api_query_overload_3: APIQuery
):
    assert api_query_overload_3.qualified_name
    assert client.asset.restore(
        asset_type=APIQuery, qualified_name=api_query_overload_3.qualified_name
    )
    assert api_query_overload_3.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=APIQuery, qualified_name=api_query_overload_3.qualified_name
    )
    assert restored
    assert restored.guid == api_query_overload_3.guid
    assert restored.qualified_name == api_query_overload_3.qualified_name
    assert restored.status == EntityStatus.ACTIVE


@pytest.fixture(scope="module")
def api_field_parent_object(
    client: AtlanClient, connection: Connection, api_object: APIObject
) -> Generator[APIField, None, None]:
    assert connection.qualified_name
    to_create = APIField.creator(
        name=API_FIELD_NAME,
        parent_api_object_qualified_name=api_object.qualified_name,
        parent_api_query_qualified_name=None,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIField)


def test_api_field_parent_object(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_object: APIField,
    api_object: APIObject,
):
    assert api_field_parent_object
    assert api_field_parent_object.guid
    assert (
        api_field_parent_object.qualified_name
        == f"{api_object.qualified_name}/{API_FIELD_NAME}"
    )
    assert api_field_parent_object.name == API_FIELD_NAME
    assert (
        api_field_parent_object.connection_qualified_name == connection.qualified_name
    )
    assert api_field_parent_object.connector_name == AtlanConnectorType.API.value


@pytest.fixture(scope="module")
def api_field_parent_object_overload_1(
    client: AtlanClient, connection: Connection, api_object: APIObject
) -> Generator[APIField, None, None]:
    assert connection.qualified_name
    to_create = APIField.creator(
        name=API_FIELD_OVERLOAD_1_NAME,
        parent_api_object_qualified_name=api_object.qualified_name,
        parent_api_query_qualified_name=None,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIField)


def test_api_field_parent_object_overload_1(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_object_overload_1: APIField,
    api_object: APIObject,
):
    assert api_field_parent_object_overload_1
    assert api_field_parent_object_overload_1.guid
    assert (
        api_field_parent_object_overload_1.qualified_name
        == f"{api_object.qualified_name}/{API_FIELD_OVERLOAD_1_NAME}"
    )
    assert api_field_parent_object_overload_1.name == API_FIELD_OVERLOAD_1_NAME
    assert (
        api_field_parent_object_overload_1.connection_qualified_name
        == connection.qualified_name
    )
    assert (
        api_field_parent_object_overload_1.connector_name
        == AtlanConnectorType.API.value
    )


@pytest.fixture(scope="module")
def api_field_parent_object_overload_2(
    client: AtlanClient, connection: Connection, api_object: APIObject
) -> Generator[APIField, None, None]:
    assert connection.qualified_name
    to_create = APIField.creator(
        name=API_FIELD_OVERLOAD_2_NAME,
        parent_api_object_qualified_name=api_object.qualified_name,
        parent_api_query_qualified_name=None,
        api_query_param_type=APIQueryParamTypeEnum.INPUT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIField)


def test_api_field_parent_object_overload_2(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_object_overload_2: APIField,
    api_object: APIObject,
):
    assert api_field_parent_object_overload_2
    assert api_field_parent_object_overload_2.guid
    assert (
        api_field_parent_object_overload_2.qualified_name
        == f"{api_object.qualified_name}/{API_FIELD_OVERLOAD_2_NAME}"
    )
    assert api_field_parent_object_overload_2.name == API_FIELD_OVERLOAD_2_NAME
    assert (
        api_field_parent_object_overload_2.connection_qualified_name
        == connection.qualified_name
    )
    assert (
        api_field_parent_object_overload_2.api_query_param_type
        == APIQueryParamTypeEnum.INPUT.value
    )
    assert (
        api_field_parent_object_overload_2.connector_name
        == AtlanConnectorType.API.value
    )


@pytest.fixture(scope="module")
def api_field_parent_object_overload_3(
    client: AtlanClient, connection: Connection, api_object: APIObject
) -> Generator[APIField, None, None]:
    assert connection.qualified_name
    to_create = APIField.creator(
        name=API_FIELD_OVERLOAD_3_NAME,
        parent_api_object_qualified_name=api_object.qualified_name,
        parent_api_query_qualified_name=None,
        api_field_type=API_FIELD_TYPE,
        api_field_type_secondary=API_FIELD_TYPE_SECONDARY,
        api_query_param_type=APIQueryParamTypeEnum.INPUT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIField)


def test_api_field_parent_object_overload_3(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_object_overload_3: APIField,
    api_object: APIObject,
):
    assert api_field_parent_object_overload_3
    assert api_field_parent_object_overload_3.guid
    assert (
        api_field_parent_object_overload_3.qualified_name
        == f"{api_object.qualified_name}/{API_FIELD_OVERLOAD_3_NAME}"
    )
    assert api_field_parent_object_overload_3.name == API_FIELD_OVERLOAD_3_NAME
    assert (
        api_field_parent_object_overload_3.connection_qualified_name
        == connection.qualified_name
    )
    assert api_field_parent_object_overload_3.api_field_type == API_FIELD_TYPE
    assert (
        api_field_parent_object_overload_3.api_field_type_secondary
        == API_FIELD_TYPE_SECONDARY
    )
    assert (
        api_field_parent_object_overload_3.api_query_param_type
        == APIQueryParamTypeEnum.INPUT.value
    )
    assert (
        api_field_parent_object_overload_3.connector_name
        == AtlanConnectorType.API.value
    )


@pytest.fixture(scope="module")
def api_field_parent_object_overload_4(
    client: AtlanClient, connection: Connection, api_object: APIObject
) -> Generator[APIField, None, None]:
    assert connection.qualified_name
    to_create = APIField.creator(
        name=API_FIELD_OVERLOAD_4_NAME,
        parent_api_object_qualified_name=api_object.qualified_name,
        parent_api_query_qualified_name=None,
        connection_qualified_name=connection.qualified_name,
        api_field_type=API_FIELD_TYPE,
        api_field_type_secondary=API_FIELD_TYPE_SECONDARY,
        is_api_object_reference=API_FIELD_IS_OBJECT_REFERENCE,
        reference_api_object_qualified_name=f"{connection.qualified_name}/{API_FIELD_REFERENCE_OBJECT_NAME}",
        api_query_param_type=APIQueryParamTypeEnum.INPUT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIField)


def test_api_field_parent_object_overload_4(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_object_overload_4: APIField,
    api_object: APIObject,
):
    assert api_field_parent_object_overload_4
    assert api_field_parent_object_overload_4.guid
    assert (
        api_field_parent_object_overload_4.qualified_name
        == f"{api_object.qualified_name}/{API_FIELD_OVERLOAD_4_NAME}"
    )
    assert api_field_parent_object_overload_4.name == API_FIELD_OVERLOAD_4_NAME
    assert (
        api_field_parent_object_overload_4.connection_qualified_name
        == connection.qualified_name
    )
    assert api_field_parent_object_overload_4.api_field_type == API_FIELD_TYPE
    assert (
        api_field_parent_object_overload_4.api_field_type_secondary
        == API_FIELD_TYPE_SECONDARY
    )
    assert (
        api_field_parent_object_overload_4.api_is_object_reference
        == API_FIELD_IS_OBJECT_REFERENCE
    )
    assert (
        api_field_parent_object_overload_4.api_object_qualified_name
        == f"{connection.qualified_name}/{API_FIELD_REFERENCE_OBJECT_NAME}"
    )
    assert (
        api_field_parent_object_overload_4.api_query_param_type
        == APIQueryParamTypeEnum.INPUT.value
    )
    assert (
        api_field_parent_object_overload_4.connector_name
        == AtlanConnectorType.API.value
    )


@pytest.fixture(scope="module")
def api_field_parent_query_overload(
    client: AtlanClient, connection: Connection, api_query: APIQuery
) -> Generator[APIField, None, None]:
    assert connection.qualified_name
    to_create = APIField.creator(
        name=API_FIELD_PARENT_QUERY_NAME,
        parent_api_object_qualified_name=None,
        parent_api_query_qualified_name=api_query.qualified_name,
        connection_qualified_name=connection.qualified_name,
        api_field_type=API_FIELD_TYPE,
        api_field_type_secondary=API_FIELD_TYPE_SECONDARY,
        is_api_object_reference=API_FIELD_IS_OBJECT_REFERENCE,
        reference_api_object_qualified_name=f"{connection.qualified_name}/{API_FIELD_REFERENCE_OBJECT_NAME}",
        api_query_param_type=APIQueryParamTypeEnum.INPUT,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=APIField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=APIField)


def test_api_field_parent_query_overload(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_query_overload: APIField,
    api_query: APIQuery,
):
    assert api_field_parent_query_overload
    assert api_field_parent_query_overload.guid
    assert (
        api_field_parent_query_overload.qualified_name
        == f"{api_query.qualified_name}/{API_FIELD_PARENT_QUERY_NAME}"
    )
    assert api_field_parent_query_overload.name == API_FIELD_PARENT_QUERY_NAME
    assert (
        api_field_parent_query_overload.connection_qualified_name
        == connection.qualified_name
    )
    assert api_field_parent_query_overload.api_field_type == API_FIELD_TYPE
    assert (
        api_field_parent_query_overload.api_field_type_secondary
        == API_FIELD_TYPE_SECONDARY
    )
    assert (
        api_field_parent_query_overload.api_is_object_reference
        == API_FIELD_IS_OBJECT_REFERENCE
    )
    assert (
        api_field_parent_query_overload.api_object_qualified_name
        == f"{connection.qualified_name}/{API_FIELD_REFERENCE_OBJECT_NAME}"
    )
    assert (
        api_field_parent_query_overload.api_query_param_type
        == APIQueryParamTypeEnum.INPUT.value
    )
    assert (
        api_field_parent_query_overload.connector_name == AtlanConnectorType.API.value
    )


def test_update_api_field(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_query_overload: APIField,
):
    assert api_field_parent_query_overload.qualified_name
    assert api_field_parent_query_overload.name
    updated = client.asset.update_certificate(
        asset_type=APIField,
        qualified_name=api_field_parent_query_overload.qualified_name,
        name=api_field_parent_query_overload.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert api_field_parent_query_overload.qualified_name
    assert api_field_parent_query_overload.name
    updated = client.asset.update_announcement(
        asset_type=APIField,
        qualified_name=api_field_parent_query_overload.qualified_name,
        name=api_field_parent_query_overload.name,
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


@pytest.mark.order(after="test_update_api_field")
def test_retrieve_api_field(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_query_overload: APIField,
):
    b = client.asset.get_by_guid(
        api_field_parent_query_overload.guid, asset_type=APIField
    )
    assert b
    assert not b.is_incomplete
    assert b.guid == api_field_parent_query_overload.guid
    assert b.qualified_name == api_field_parent_query_overload.qualified_name
    assert b.name == api_field_parent_query_overload.name
    assert b.connector_name == api_field_parent_query_overload.connector_name
    assert (
        b.connection_qualified_name
        == api_field_parent_query_overload.connection_qualified_name
    )
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_api_field")
def test_delete_api_field(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_query_overload: APIField,
):
    response = client.asset.delete_by_guid(api_field_parent_query_overload.guid)
    assert response
    assert not response.assets_created(asset_type=APIField)
    assert not response.assets_updated(asset_type=APIField)
    deleted = response.assets_deleted(asset_type=APIField)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == api_field_parent_query_overload.guid
    assert deleted[0].qualified_name == api_field_parent_query_overload.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_api_field")
def test_read_deleted_api_field(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_query_overload: APIField,
):
    deleted = client.asset.get_by_guid(
        api_field_parent_query_overload.guid, asset_type=APIField
    )
    assert deleted
    assert deleted.guid == api_field_parent_query_overload.guid
    assert deleted.qualified_name == api_field_parent_query_overload.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_api_field")
def test_restore_field(
    client: AtlanClient,
    connection: Connection,
    api_field_parent_query_overload: APIField,
):
    assert api_field_parent_query_overload.qualified_name
    assert client.asset.restore(
        asset_type=APIField,
        qualified_name=api_field_parent_query_overload.qualified_name,
    )
    assert api_field_parent_query_overload.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=APIField,
        qualified_name=api_field_parent_query_overload.qualified_name,
    )
    assert restored
    assert restored.guid == api_field_parent_query_overload.guid
    assert restored.qualified_name == api_field_parent_query_overload.qualified_name
    assert restored.status == EntityStatus.ACTIVE
