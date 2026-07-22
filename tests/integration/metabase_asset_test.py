# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import (
    Connection,
    MetabaseCollection,
    MetabaseDashboard,
    MetabaseQuestion,
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

MODULE_NAME = TestId.make_unique("METABASE")

CONNECTOR_TYPE = AtlanConnectorType.METABASE
METABASE_COLLECTION_NAME = MODULE_NAME + "-coll"
METABASE_DASHBOARD_NAME = MODULE_NAME + "-dash"
METABASE_QUESTION_NAME = MODULE_NAME + "-qstn"
METABASE_COLLECTION_ID = "1001"
METABASE_DASHBOARD_ID = "2002"
METABASE_QUESTION_ID = "3003"
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
def metabase_collection(
    client: AtlanClient, connection: Connection
) -> Generator[MetabaseCollection, None, None]:
    assert connection.qualified_name
    to_create = MetabaseCollection.creator(
        name=METABASE_COLLECTION_NAME,
        connection_qualified_name=connection.qualified_name,
        metabase_id=METABASE_COLLECTION_ID,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=MetabaseCollection)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MetabaseCollection)


def test_metabase_collection(
    client: AtlanClient,
    metabase_collection: MetabaseCollection,
    connection: Connection,
):
    assert metabase_collection
    assert metabase_collection.guid
    assert metabase_collection.qualified_name
    assert metabase_collection.connection_qualified_name == connection.qualified_name
    assert metabase_collection.qualified_name == (
        f"{connection.qualified_name}/collections/{METABASE_COLLECTION_ID}"
    )
    assert metabase_collection.name == METABASE_COLLECTION_NAME
    assert metabase_collection.connector_name == AtlanConnectorType.METABASE.value


@pytest.fixture(scope="module")
def metabase_dashboard(
    client: AtlanClient, connection: Connection
) -> Generator[MetabaseDashboard, None, None]:
    assert connection.qualified_name
    to_create = MetabaseDashboard.creator(
        name=METABASE_DASHBOARD_NAME,
        connection_qualified_name=connection.qualified_name,
        metabase_id=METABASE_DASHBOARD_ID,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=MetabaseDashboard)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MetabaseDashboard)


def test_metabase_dashboard(
    client: AtlanClient,
    metabase_dashboard: MetabaseDashboard,
    connection: Connection,
):
    assert metabase_dashboard
    assert metabase_dashboard.guid
    assert metabase_dashboard.qualified_name
    assert metabase_dashboard.connection_qualified_name == connection.qualified_name
    assert metabase_dashboard.qualified_name == (
        f"{connection.qualified_name}/dashboards/{METABASE_DASHBOARD_ID}"
    )
    assert metabase_dashboard.name == METABASE_DASHBOARD_NAME
    assert metabase_dashboard.connector_name == AtlanConnectorType.METABASE.value


@pytest.fixture(scope="module")
def metabase_question(
    client: AtlanClient, connection: Connection
) -> Generator[MetabaseQuestion, None, None]:
    assert connection.qualified_name
    to_create = MetabaseQuestion.creator(
        name=METABASE_QUESTION_NAME,
        connection_qualified_name=connection.qualified_name,
        metabase_id=METABASE_QUESTION_ID,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=MetabaseQuestion)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MetabaseQuestion)


def test_metabase_question(
    client: AtlanClient,
    metabase_question: MetabaseQuestion,
    connection: Connection,
):
    assert metabase_question
    assert metabase_question.guid
    assert metabase_question.qualified_name
    assert metabase_question.connection_qualified_name == connection.qualified_name
    assert metabase_question.qualified_name == (
        f"{connection.qualified_name}/questions/{METABASE_QUESTION_ID}"
    )
    assert metabase_question.name == METABASE_QUESTION_NAME
    assert metabase_question.connector_name == AtlanConnectorType.METABASE.value


def test_update_metabase_collection(
    client: AtlanClient,
    metabase_collection: MetabaseCollection,
):
    assert metabase_collection.qualified_name
    assert metabase_collection.name
    updated = client.asset.update_certificate(
        asset_type=MetabaseCollection,
        qualified_name=metabase_collection.qualified_name,
        name=METABASE_COLLECTION_NAME,
        certificate_status=CERTIFICATE_STATUS,
        message=CERTIFICATE_MESSAGE,
    )
    assert updated
    assert updated.certificate_status_message == CERTIFICATE_MESSAGE
    updated = client.asset.update_announcement(
        asset_type=MetabaseCollection,
        qualified_name=metabase_collection.qualified_name,
        name=METABASE_COLLECTION_NAME,
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


@pytest.mark.order(after="test_update_metabase_collection")
def test_retrieve_metabase_collection(
    client: AtlanClient,
    metabase_collection: MetabaseCollection,
):
    b = client.asset.get_by_guid(
        metabase_collection.guid,
        asset_type=MetabaseCollection,
        ignore_relationships=False,
    )
    assert b
    assert not b.is_incomplete
    assert b.guid == metabase_collection.guid
    assert b.qualified_name == metabase_collection.qualified_name
    assert b.name == METABASE_COLLECTION_NAME
    assert b.connector_name == AtlanConnectorType.METABASE.value
    assert b.certificate_status == CERTIFICATE_STATUS
    assert b.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_retrieve_metabase_collection")
def test_delete_metabase_question(
    client: AtlanClient, metabase_question: MetabaseQuestion
):
    response = client.asset.delete_by_guid(metabase_question.guid)
    assert response
    assert not response.assets_created(asset_type=MetabaseQuestion)
    assert not response.assets_updated(asset_type=MetabaseQuestion)
    deleted = response.assets_deleted(asset_type=MetabaseQuestion)
    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == metabase_question.guid
    assert deleted[0].qualified_name == metabase_question.qualified_name
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED


@pytest.mark.order(after="test_delete_metabase_question")
def test_restore_metabase_question(
    client: AtlanClient,
    metabase_question: MetabaseQuestion,
):
    assert metabase_question.qualified_name
    assert client.asset.restore(
        asset_type=MetabaseQuestion, qualified_name=metabase_question.qualified_name
    )
    restored = client.asset.get_by_qualified_name(
        asset_type=MetabaseQuestion,
        qualified_name=metabase_question.qualified_name,
        ignore_relationships=False,
    )
    assert restored
    assert restored.guid == metabase_question.guid
    assert restored.qualified_name == metabase_question.qualified_name
    assert restored.status == EntityStatus.ACTIVE
