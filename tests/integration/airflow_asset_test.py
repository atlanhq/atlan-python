# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AirflowDag, AirflowTask, Connection
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

MODULE_NAME = TestId.make_unique("AIRFLOW")

AIRFLOW_DAG_NAME = f"test_dag_{MODULE_NAME}"
AIRFLOW_TASK_NAME = f"test_task_{MODULE_NAME}"
AIRFLOW_TASK_NAME_OVERLOAD = f"test_task_overload_{MODULE_NAME}"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED

ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


response = block(AtlanClient(), AssetMutationResponse())


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.AIRFLOW
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def airflow_dag(
    client: AtlanClient, connection: Connection
) -> Generator[AirflowDag, None, None]:
    assert connection.qualified_name
    to_create = AirflowDag.creator(
        name=AIRFLOW_DAG_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AirflowDag)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AirflowDag)


def test_airflow_dag(
    client: AtlanClient,
    connection: Connection,
    airflow_dag: AirflowDag,
):
    assert airflow_dag
    assert airflow_dag.guid
    assert airflow_dag.qualified_name
    assert airflow_dag.name == AIRFLOW_DAG_NAME
    assert airflow_dag.connector_name == AtlanConnectorType.AIRFLOW
    assert airflow_dag.connection_qualified_name == connection.qualified_name


@pytest.fixture(scope="module")
def airflow_task(
    client: AtlanClient, airflow_dag: AirflowDag
) -> Generator[AirflowTask, None, None]:
    assert airflow_dag.qualified_name
    to_create = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME, airflow_dag_qualified_name=airflow_dag.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AirflowTask)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AirflowTask)


def test_airflow_task(
    client: AtlanClient,
    airflow_dag: AirflowDag,
    airflow_task: AirflowTask,
):
    assert airflow_task
    assert airflow_task.guid
    assert airflow_task.qualified_name
    assert airflow_task.name == AIRFLOW_TASK_NAME
    assert airflow_task.connector_name == AtlanConnectorType.AIRFLOW
    assert airflow_task.airflow_dag_qualified_name == airflow_dag.qualified_name


@pytest.fixture(scope="module")
def airflow_task_overload(
    client: AtlanClient, airflow_dag: AirflowDag, connection: Connection
) -> Generator[AirflowTask, None, None]:
    assert airflow_dag.qualified_name
    assert connection.qualified_name
    to_create = AirflowTask.creator(
        name=AIRFLOW_TASK_NAME_OVERLOAD,
        airflow_dag_qualified_name=airflow_dag.qualified_name,
        connection_qualified_name=connection.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AirflowTask)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AirflowTask)


def test_overload_airflow_task(
    client: AtlanClient,
    airflow_dag: AirflowDag,
    airflow_task_overload: AirflowTask,
):
    assert airflow_task_overload
    assert airflow_task_overload.guid
    assert airflow_task_overload.qualified_name
    assert airflow_task_overload.name == AIRFLOW_TASK_NAME_OVERLOAD
    assert airflow_task_overload.connector_name == AtlanConnectorType.AIRFLOW
    assert (
        airflow_task_overload.airflow_dag_qualified_name == airflow_dag.qualified_name
    )


def _update_cert_and_annoucement(client, asset, asset_type):
    assert asset.name
    assert asset.qualified_name

    updated = client.asset.update_certificate(
        name=asset.name,
        asset_type=asset_type,
        qualified_name=asset.qualified_name,
        message=CERTIFICATE_MESSAGE,
        certificate_status=CERTIFICATE_STATUS,
    )
    assert updated
    assert updated.certificate_status == CERTIFICATE_STATUS
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE

    updated = client.asset.update_announcement(
        name=asset.name,
        asset_type=asset_type,
        qualified_name=asset.qualified_name,
        announcement=Announcement(
            announcement_type=ANNOUNCEMENT_TYPE,
            announcement_title=ANNOUNCEMENT_TITLE,
            announcement_message=ANNOUNCEMENT_MESSAGE,
        ),
    )
    assert updated
    assert updated.announcement_type == ANNOUNCEMENT_TYPE
    assert updated.announcement_title == ANNOUNCEMENT_TITLE
    assert updated.announcement_message == ANNOUNCEMENT_MESSAGE


def test_update_airflow_assets(
    client: AtlanClient,
    airflow_dag: AirflowDag,
    airflow_task: AirflowTask,
):
    _update_cert_and_annoucement(client, airflow_dag, AirflowDag)
    _update_cert_and_annoucement(client, airflow_task, AirflowTask)


def _retrieve_airflow_assets(client, asset, asset_type):
    retrieved = client.asset.get_by_guid(asset.guid, asset_type=asset_type)
    assert retrieved
    assert not retrieved.is_incomplete
    assert retrieved.guid == asset.guid
    assert retrieved.qualified_name == asset.qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.AIRFLOW
    assert retrieved.certificate_status == CERTIFICATE_STATUS
    assert retrieved.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_update_airflow_assets")
def test_retrieve_airflow_assets(
    client: AtlanClient,
    airflow_dag: AirflowDag,
    airflow_task: AirflowTask,
):
    _retrieve_airflow_assets(client, airflow_dag, AirflowDag)
    _retrieve_airflow_assets(client, airflow_task, AirflowTask)


@pytest.mark.order(after="test_retrieve_airflow_assets")
def test_delete_airflow_task(
    client: AtlanClient,
    airflow_task: AirflowTask,
):
    response = client.asset.delete_by_guid(guid=airflow_task.guid)
    assert response
    assert not response.assets_created(asset_type=AirflowTask)
    assert not response.assets_updated(asset_type=AirflowTask)
    deleted = response.assets_deleted(asset_type=AirflowTask)

    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == airflow_task.guid
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED
    assert deleted[0].qualified_name == airflow_task.qualified_name


@pytest.mark.order(after="test_delete_airflow_task")
def test_read_deleted_airflow_task(
    client: AtlanClient,
    airflow_task: AirflowTask,
):
    deleted = client.asset.get_by_guid(airflow_task.guid, asset_type=AirflowTask)
    assert deleted
    assert deleted.status == EntityStatus.DELETED
    assert deleted.guid == airflow_task.guid
    assert deleted.qualified_name == airflow_task.qualified_name


@pytest.mark.order(after="test_read_deleted_airflow_task")
def test_restore_airflow_task(
    client: AtlanClient,
    airflow_task: AirflowTask,
):
    assert airflow_task.qualified_name
    assert client.asset.restore(
        asset_type=AirflowTask, qualified_name=airflow_task.qualified_name
    )
    assert airflow_task.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=AirflowTask, qualified_name=airflow_task.qualified_name
    )
    assert restored
    assert restored.guid == airflow_task.guid
    assert restored.status == EntityStatus.ACTIVE
    assert restored.qualified_name == airflow_task.qualified_name
