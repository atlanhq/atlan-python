from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    AnaplanApp,
    AnaplanDimension,
    AnaplanLineItem,
    AnaplanList,
    AnaplanModel,
    AnaplanModule,
    AnaplanPage,
    AnaplanSystemDimension,
    AnaplanView,
    AnaplanWorkspace,
    Connection,
)
from pyatlan.model.core import Announcement
from pyatlan.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
)
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("ANAPLAN")

CONNECTOR_TYPE = AtlanConnectorType.ANAPLAN
ANAPLAN_WORKSPACE_NAME = f"{MODULE_NAME}-anaplan-workspace"
ANAPLAN_APP_NAME = f"{MODULE_NAME}-anaplan-app"
ANAPLAN_PAGE_NAME = f"{MODULE_NAME}-anaplan-page"
ANAPLAN_PAGE_NAME_OVERLOAD = f"{MODULE_NAME}-anaplan-page-overload"
ANAPLAN_MODEL_NAME = f"{MODULE_NAME}-anaplan-model"
ANAPLAN_MODEL_NAME_OVERLOAD = f"{MODULE_NAME}-anaplan-model-overload"
ANAPLAN_MODULE_NAME = f"{MODULE_NAME}-anaplan-module"
ANAPLAN_MODULE_NAME_OVERLOAD = f"{MODULE_NAME}-anaplan-module-overload"
ANAPLAN_LIST_NAME = f"{MODULE_NAME}-anaplan-list"
ANAPLAN_LIST_NAME_OVERLOAD = f"{MODULE_NAME}-anaplan-list-overload"
ANAPLAN_SYSTEM_DIMENSION_NAME = f"{MODULE_NAME}-anaplan-system-dimension"
ANAPLAN_DIMENSION_NAME = f"{MODULE_NAME}-anaplan-dimension"
ANAPLAN_DIMENSION_NAME_OVERLOAD = f"{MODULE_NAME}-anaplan-dimension-overload"
ANAPLAN_LINEITEM_NAME = f"{MODULE_NAME}-anaplan-lineitem"
ANAPLAN_LINEITEM_NAME_OVERLOAD = f"{MODULE_NAME}-anaplan-lineitem-overload"
ANAPLAN_VIEW_NAME = f"{MODULE_NAME}-anaplan-view"
ANAPLAN_VIEW_NAME_OVERLOAD = f"{MODULE_NAME}-anaplan-view-overload"

CERTIFICATE_STATUS = CertificateStatus.VERIFIED
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def anaplan_workspace(
    client: AtlanClient, connection: Connection
) -> Generator[AnaplanWorkspace, None, None]:
    assert connection.qualified_name
    to_create = AnaplanWorkspace.creator(
        name=ANAPLAN_WORKSPACE_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanWorkspace)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanWorkspace)


def test_anaplan_workspace(
    client: AtlanClient, connection: Connection, anaplan_workspace: AnaplanWorkspace
):
    assert anaplan_workspace
    assert anaplan_workspace.guid
    assert anaplan_workspace.qualified_name
    assert anaplan_workspace.name == ANAPLAN_WORKSPACE_NAME
    assert anaplan_workspace.connection_qualified_name == connection.qualified_name
    assert anaplan_workspace.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_system_dimension(
    client: AtlanClient, connection: Connection
) -> Generator[AnaplanSystemDimension, None, None]:
    assert connection.qualified_name
    to_create = AnaplanSystemDimension.creator(
        name=ANAPLAN_SYSTEM_DIMENSION_NAME,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanSystemDimension)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanSystemDimension)


def test_anaplan_system_dimension(
    client: AtlanClient,
    connection: Connection,
    anaplan_system_dimension: AnaplanSystemDimension,
):
    assert anaplan_system_dimension
    assert anaplan_system_dimension.guid
    assert anaplan_system_dimension.qualified_name
    assert anaplan_system_dimension.name == ANAPLAN_SYSTEM_DIMENSION_NAME
    assert (
        anaplan_system_dimension.connection_qualified_name == connection.qualified_name
    )
    assert anaplan_system_dimension.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_app(
    client: AtlanClient, connection: Connection
) -> Generator[AnaplanApp, None, None]:
    assert connection.qualified_name
    to_create = AnaplanApp.creator(
        name=ANAPLAN_APP_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanApp)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanApp)


def test_anaplan_app(
    client: AtlanClient, connection: Connection, anaplan_app: AnaplanApp
):
    assert anaplan_app
    assert anaplan_app.guid
    assert anaplan_app.qualified_name
    assert anaplan_app.name == ANAPLAN_APP_NAME
    assert anaplan_app.connection_qualified_name == connection.qualified_name
    assert anaplan_app.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_page(
    client: AtlanClient, anaplan_app: AnaplanApp
) -> Generator[AnaplanPage, None, None]:
    assert anaplan_app.qualified_name
    to_create = AnaplanPage.creator(
        name=ANAPLAN_PAGE_NAME, app_qualified_name=anaplan_app.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanPage)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanPage)


def test_anaplan_page(
    client: AtlanClient, anaplan_app: AnaplanApp, anaplan_page: AnaplanPage
):
    assert anaplan_page
    assert anaplan_page.guid
    assert anaplan_page.qualified_name
    assert anaplan_page.name == ANAPLAN_PAGE_NAME
    assert (
        anaplan_page.connection_qualified_name == anaplan_app.connection_qualified_name
    )
    assert anaplan_page.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_page_overload(
    client: AtlanClient, connection: Connection, anaplan_app: AnaplanApp
) -> Generator[AnaplanPage, None, None]:
    assert connection.qualified_name
    assert anaplan_app.qualified_name
    to_create = AnaplanPage.creator(
        name=ANAPLAN_PAGE_NAME_OVERLOAD,
        app_qualified_name=anaplan_app.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanPage)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanPage)


def test_overload_anaplan_page(
    client: AtlanClient, anaplan_app: AnaplanApp, anaplan_page_overload: AnaplanPage
):
    assert anaplan_page_overload
    assert anaplan_page_overload.guid
    assert anaplan_page_overload.qualified_name
    assert anaplan_page_overload.name == ANAPLAN_PAGE_NAME_OVERLOAD
    assert (
        anaplan_page_overload.connection_qualified_name
        == anaplan_app.connection_qualified_name
    )
    assert anaplan_page_overload.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_model(
    client: AtlanClient, anaplan_workspace: AnaplanWorkspace
) -> Generator[AnaplanModel, None, None]:
    assert anaplan_workspace.qualified_name
    to_create = AnaplanModel.creator(
        name=ANAPLAN_MODEL_NAME,
        workspace_qualified_name=anaplan_workspace.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanModel)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanModel)


def test_anaplan_model(
    client: AtlanClient,
    anaplan_workspace: AnaplanWorkspace,
    anaplan_model: AnaplanModel,
):
    assert anaplan_model
    assert anaplan_model.guid
    assert anaplan_model.qualified_name
    assert anaplan_model.name == ANAPLAN_MODEL_NAME
    assert (
        anaplan_model.connection_qualified_name
        == anaplan_workspace.connection_qualified_name
    )
    assert anaplan_model.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_model_overload(
    client: AtlanClient, connection: Connection, anaplan_workspace: AnaplanWorkspace
) -> Generator[AnaplanModel, None, None]:
    assert connection.qualified_name
    assert anaplan_workspace.qualified_name
    to_create = AnaplanModel.creator(
        name=ANAPLAN_MODEL_NAME_OVERLOAD,
        workspace_qualified_name=anaplan_workspace.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanModel)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanModel)


def test_overload_anaplan_model(
    client: AtlanClient,
    anaplan_workspace: AnaplanWorkspace,
    anaplan_model_overload: AnaplanModel,
):
    assert anaplan_model_overload
    assert anaplan_model_overload.guid
    assert anaplan_model_overload.qualified_name
    assert anaplan_model_overload.name == ANAPLAN_MODEL_NAME_OVERLOAD
    assert (
        anaplan_model_overload.connection_qualified_name
        == anaplan_workspace.connection_qualified_name
    )
    assert anaplan_model_overload.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_module(
    client: AtlanClient, anaplan_model: AnaplanModel
) -> Generator[AnaplanModule, None, None]:
    assert anaplan_model.qualified_name
    to_create = AnaplanModule.creator(
        name=ANAPLAN_MODULE_NAME, model_qualified_name=anaplan_model.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanModule)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanModule)


def test_anaplan_module(
    client: AtlanClient, anaplan_model: AnaplanModel, anaplan_module: AnaplanModule
):
    assert anaplan_module
    assert anaplan_module.guid
    assert anaplan_module.qualified_name
    assert anaplan_module.name == ANAPLAN_MODULE_NAME
    assert (
        anaplan_module.connection_qualified_name
        == anaplan_model.connection_qualified_name
    )
    assert anaplan_module.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_module_overload(
    client: AtlanClient, connection: Connection, anaplan_model: AnaplanModel
) -> Generator[AnaplanModule, None, None]:
    assert connection.qualified_name
    assert anaplan_model.qualified_name
    to_create = AnaplanModule.creator(
        name=ANAPLAN_MODULE_NAME_OVERLOAD,
        model_qualified_name=anaplan_model.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanModule)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanModule)


def test_overload_anaplan_module(
    client: AtlanClient,
    anaplan_model: AnaplanModel,
    anaplan_module_overload: AnaplanModule,
):
    assert anaplan_module_overload
    assert anaplan_module_overload.guid
    assert anaplan_module_overload.qualified_name
    assert anaplan_module_overload.name == ANAPLAN_MODULE_NAME_OVERLOAD
    assert (
        anaplan_module_overload.connection_qualified_name
        == anaplan_model.connection_qualified_name
    )
    assert anaplan_module_overload.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_list(
    client: AtlanClient, anaplan_model: AnaplanModel
) -> Generator[AnaplanList, None, None]:
    assert anaplan_model.qualified_name
    to_create = AnaplanList.creator(
        name=ANAPLAN_LIST_NAME, model_qualified_name=anaplan_model.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanList)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanList)


def test_anaplan_list(
    client: AtlanClient, anaplan_model: AnaplanModel, anaplan_list: AnaplanList
):
    assert anaplan_list
    assert anaplan_list.guid
    assert anaplan_list.qualified_name
    assert anaplan_list.name == ANAPLAN_LIST_NAME
    assert (
        anaplan_list.connection_qualified_name
        == anaplan_model.connection_qualified_name
    )
    assert anaplan_list.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_list_overload(
    client: AtlanClient, connection: Connection, anaplan_model: AnaplanModel
) -> Generator[AnaplanList, None, None]:
    assert connection.qualified_name
    assert anaplan_model.qualified_name
    to_create = AnaplanList.creator(
        name=ANAPLAN_LIST_NAME_OVERLOAD,
        model_qualified_name=anaplan_model.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanList)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanList)


def test_overload_anaplan_list(
    client: AtlanClient, anaplan_model: AnaplanModel, anaplan_list_overload: AnaplanList
):
    assert anaplan_list_overload
    assert anaplan_list_overload.guid
    assert anaplan_list_overload.qualified_name
    assert anaplan_list_overload.name == ANAPLAN_LIST_NAME_OVERLOAD
    assert (
        anaplan_list_overload.connection_qualified_name
        == anaplan_model.connection_qualified_name
    )
    assert anaplan_list_overload.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_dimension(
    client: AtlanClient, anaplan_model: AnaplanModel
) -> Generator[AnaplanDimension, None, None]:
    assert anaplan_model.qualified_name
    to_create = AnaplanDimension.creator(
        name=ANAPLAN_DIMENSION_NAME, model_qualified_name=anaplan_model.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanDimension)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanDimension)


def test_anaplan_dimension(
    client: AtlanClient,
    anaplan_model: AnaplanModel,
    anaplan_dimension: AnaplanDimension,
):
    assert anaplan_dimension
    assert anaplan_dimension.guid
    assert anaplan_dimension.qualified_name
    assert anaplan_dimension.name == ANAPLAN_DIMENSION_NAME
    assert (
        anaplan_dimension.connection_qualified_name
        == anaplan_model.connection_qualified_name
    )
    assert anaplan_dimension.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_dimension_overload(
    client: AtlanClient, connection: Connection, anaplan_model: AnaplanModel
) -> Generator[AnaplanDimension, None, None]:
    assert connection.qualified_name
    assert anaplan_model.qualified_name
    to_create = AnaplanDimension.creator(
        name=ANAPLAN_DIMENSION_NAME_OVERLOAD,
        model_qualified_name=anaplan_model.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanDimension)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanDimension)


def test_overload_anaplan_dimension(
    client: AtlanClient,
    anaplan_model: AnaplanModel,
    anaplan_dimension_overload: AnaplanDimension,
):
    assert anaplan_dimension_overload
    assert anaplan_dimension_overload.guid
    assert anaplan_dimension_overload.qualified_name
    assert anaplan_dimension_overload.name == ANAPLAN_DIMENSION_NAME_OVERLOAD
    assert (
        anaplan_dimension_overload.connection_qualified_name
        == anaplan_model.connection_qualified_name
    )
    assert anaplan_dimension_overload.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_lineitem(
    client: AtlanClient, anaplan_module: AnaplanModule
) -> Generator[AnaplanLineItem, None, None]:
    assert anaplan_module.qualified_name
    to_create = AnaplanLineItem.creator(
        name=ANAPLAN_LINEITEM_NAME, module_qualified_name=anaplan_module.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanLineItem)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanLineItem)


def test_anaplan_lineitem(
    client: AtlanClient,
    anaplan_module: AnaplanModule,
    anaplan_lineitem: AnaplanLineItem,
):
    assert anaplan_lineitem
    assert anaplan_lineitem.guid
    assert anaplan_lineitem.qualified_name
    assert anaplan_lineitem.name == ANAPLAN_LINEITEM_NAME
    assert (
        anaplan_lineitem.connection_qualified_name
        == anaplan_module.connection_qualified_name
    )
    assert anaplan_lineitem.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_lineitem_overload(
    client: AtlanClient, connection: Connection, anaplan_module: AnaplanModule
) -> Generator[AnaplanLineItem, None, None]:
    assert connection.qualified_name
    assert anaplan_module.qualified_name
    to_create = AnaplanLineItem.creator(
        name=ANAPLAN_LINEITEM_NAME_OVERLOAD,
        module_qualified_name=anaplan_module.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanLineItem)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanLineItem)


def test_overload_anaplan_lineitem(
    client: AtlanClient,
    anaplan_module: AnaplanModule,
    anaplan_lineitem_overload: AnaplanLineItem,
):
    assert anaplan_lineitem_overload
    assert anaplan_lineitem_overload.guid
    assert anaplan_lineitem_overload.qualified_name
    assert anaplan_lineitem_overload.name == ANAPLAN_LINEITEM_NAME_OVERLOAD
    assert (
        anaplan_lineitem_overload.connection_qualified_name
        == anaplan_module.connection_qualified_name
    )
    assert anaplan_lineitem_overload.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_view(
    client: AtlanClient, anaplan_module: AnaplanModule
) -> Generator[AnaplanView, None, None]:
    assert anaplan_module.qualified_name
    to_create = AnaplanView.creator(
        name=ANAPLAN_VIEW_NAME, module_qualified_name=anaplan_module.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanView)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanView)


def test_anaplan_view(
    client: AtlanClient, anaplan_module: AnaplanModule, anaplan_view: AnaplanView
):
    assert anaplan_view
    assert anaplan_view.guid
    assert anaplan_view.qualified_name
    assert anaplan_view.name == ANAPLAN_VIEW_NAME
    assert (
        anaplan_view.connection_qualified_name
        == anaplan_module.connection_qualified_name
    )
    assert anaplan_view.connector_name == AtlanConnectorType.ANAPLAN.value


@pytest.fixture(scope="module")
def anaplan_view_overload(
    client: AtlanClient, connection: Connection, anaplan_module: AnaplanModule
) -> Generator[AnaplanView, None, None]:
    assert connection.qualified_name
    assert anaplan_module.qualified_name
    to_create = AnaplanView.creator(
        name=ANAPLAN_VIEW_NAME_OVERLOAD,
        module_qualified_name=anaplan_module.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AnaplanView)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AnaplanView)


def test_overload_anaplan_view(
    client: AtlanClient,
    anaplan_module: AnaplanModule,
    anaplan_view_overload: AnaplanView,
):
    assert anaplan_view_overload
    assert anaplan_view_overload.guid
    assert anaplan_view_overload.qualified_name
    assert anaplan_view_overload.name == ANAPLAN_VIEW_NAME_OVERLOAD
    assert (
        anaplan_view_overload.connection_qualified_name
        == anaplan_module.connection_qualified_name
    )
    assert anaplan_view_overload.connector_name == AtlanConnectorType.ANAPLAN.value


# here
def test_update_anaplan_view(
    client: AtlanClient,
    connection: Connection,
    anaplan_module: AnaplanModule,
    anaplan_view: AnaplanView,
):
    assert anaplan_view.qualified_name
    assert anaplan_view.name
    updated = client.asset.update_certificate(
        asset_type=AnaplanView,
        qualified_name=anaplan_view.qualified_name,
        name=anaplan_view.name,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    assert anaplan_view.qualified_name
    assert anaplan_view.name
    updated = client.asset.update_announcement(
        asset_type=AnaplanView,
        qualified_name=anaplan_view.qualified_name,
        name=anaplan_view.name,
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


@pytest.mark.order(after="test_update_anaplan_view")
def test_retrieve_anaplan_view(
    client: AtlanClient,
    connection: Connection,
    anaplan_module: AnaplanModule,
    anaplan_view: AnaplanView,
):
    b = client.asset.get_by_guid(anaplan_view.guid, asset_type=AnaplanView)
    assert b
    assert not b.is_incomplete
    assert b.guid == anaplan_view.guid
    assert b.qualified_name == anaplan_view.qualified_name
    assert b.name == anaplan_view.name
    assert b.connector_name == anaplan_view.connector_name
    assert b.connection_qualified_name == anaplan_view.connection_qualified_name
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_anaplan_view")
def test_update_anaplan_view_again(
    client: AtlanClient,
    connection: Connection,
    anaplan_module: AnaplanModule,
    anaplan_view: AnaplanView,
):
    assert anaplan_view.qualified_name
    assert anaplan_view.name
    updated = client.asset.remove_certificate(
        asset_type=AnaplanView,
        qualified_name=anaplan_view.qualified_name,
        name=anaplan_view.name,
    )
    assert updated
    assert not updated.certificate_status
    assert not updated.certificate_status_message
    assert updated.announcement_type == ANNOUNCEMENT_TYPE.value
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE
    assert anaplan_view.qualified_name
    updated = client.asset.remove_announcement(
        asset_type=AnaplanView,
        qualified_name=anaplan_view.qualified_name,
        name=anaplan_view.name,
    )
    assert updated
    assert not updated.announcement_type
    assert not updated.announcement_title
    assert not updated.announcement_message


@pytest.mark.order(after="test_update_anaplan_view_again")
def test_delete_anaplan_view(
    client: AtlanClient,
    connection: Connection,
    anaplan_module: AnaplanModule,
    anaplan_view: AnaplanView,
):
    response = client.asset.delete_by_guid(anaplan_view.guid)
    assert response
    assert not response.assets_created(asset_type=AnaplanView)
    assert not response.assets_updated(asset_type=AnaplanView)
    deleted = response.assets_deleted(asset_type=AnaplanView)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == anaplan_view.guid
    assert deleted[0].qualified_name == anaplan_view.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_anaplan_view")
def test_read_deleted_anaplan_view(
    client: AtlanClient,
    connection: Connection,
    anaplan_module: AnaplanModule,
    anaplan_view: AnaplanView,
):
    deleted = client.asset.get_by_guid(anaplan_view.guid, asset_type=AnaplanView)
    assert deleted
    assert deleted.guid == anaplan_view.guid
    assert deleted.qualified_name == anaplan_view.qualified_name
    assert deleted.status == EntityStatus.DELETED


@pytest.mark.order(after="test_read_deleted_anaplan_view")
def test_restore_anaplan_view(
    client: AtlanClient,
    connection: Connection,
    anaplan_module: AnaplanModule,
    anaplan_view: AnaplanView,
):
    assert anaplan_view.qualified_name
    assert client.asset.restore(
        asset_type=AnaplanView, qualified_name=anaplan_view.qualified_name
    )
    assert anaplan_view.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=AnaplanView, qualified_name=anaplan_view.qualified_name
    )
    assert restored
    assert restored.guid == anaplan_view.guid
    assert restored.qualified_name == anaplan_view.qualified_name
    assert restored.status == EntityStatus.ACTIVE
