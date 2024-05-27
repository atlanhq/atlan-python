# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AzureEventHub, AzureEventHubConsumerGroup, Connection
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

MODULE_NAME = TestId.make_unique("AZURE_EVENT_HUB")

EVENT_HUB_NAME = f"test_eh_{MODULE_NAME}"
EVENT_HUB_CONSUMER_GROUP_NAME = f"test_eh_consumer_group_{MODULE_NAME}"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED

ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


response = block(AtlanClient(), AssetMutationResponse())


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client,
        name=MODULE_NAME,
        connector_type=AtlanConnectorType.AZURE_EVENT_HUB,
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def event_hub(
    client: AtlanClient, connection: Connection
) -> Generator[AzureEventHub, None, None]:
    assert connection.qualified_name
    to_create = AzureEventHub.creator(
        name=EVENT_HUB_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AzureEventHub)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AzureEventHub)


def test_event_hub(
    client: AtlanClient,
    connection: Connection,
    event_hub: AzureEventHub,
):
    assert event_hub
    assert event_hub.guid
    assert event_hub.qualified_name
    assert event_hub.name == EVENT_HUB_NAME
    assert event_hub.connector_name == AtlanConnectorType.AZURE_EVENT_HUB
    assert event_hub.connection_qualified_name == connection.qualified_name


@pytest.fixture(scope="module")
def consumer_group(
    client: AtlanClient, event_hub: AzureEventHub
) -> Generator[AzureEventHubConsumerGroup, None, None]:
    assert event_hub.qualified_name
    to_create = AzureEventHubConsumerGroup.creator(
        name=EVENT_HUB_CONSUMER_GROUP_NAME,
        event_hub_qualified_names=[event_hub.qualified_name],
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=AzureEventHubConsumerGroup)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=AzureEventHubConsumerGroup)


def test_event_hub_consumer_group(
    client: AtlanClient,
    event_hub: AzureEventHub,
    consumer_group: AzureEventHubConsumerGroup,
):
    assert consumer_group
    assert consumer_group.guid
    assert consumer_group.qualified_name
    assert consumer_group.name == EVENT_HUB_CONSUMER_GROUP_NAME
    assert consumer_group.connector_name == AtlanConnectorType.AZURE_EVENT_HUB
    assert (
        event_hub.qualified_name
        and consumer_group.kafka_topic_qualified_names
        and event_hub.qualified_name in consumer_group.kafka_topic_qualified_names
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


def test_update_event_hub_assets(
    client: AtlanClient,
    event_hub: AzureEventHub,
    consumer_group: AzureEventHubConsumerGroup,
):
    _update_cert_and_annoucement(client, event_hub, AzureEventHub)
    _update_cert_and_annoucement(client, consumer_group, AzureEventHubConsumerGroup)


def _retrieve_event_hub_assets(client, asset, asset_type):
    retrieved = client.asset.get_by_guid(asset.guid, asset_type=asset_type)
    assert retrieved
    assert not retrieved.is_incomplete
    assert retrieved.guid == asset.guid
    assert retrieved.qualified_name == asset.qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.AZURE_EVENT_HUB
    assert retrieved.certificate_status == CERTIFICATE_STATUS
    assert retrieved.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_update_event_hub_assets")
def test_retrieve_event_hub_assets(
    client: AtlanClient,
    event_hub: AzureEventHub,
    consumer_group: AzureEventHubConsumerGroup,
):
    _retrieve_event_hub_assets(client, event_hub, AzureEventHub)
    _retrieve_event_hub_assets(client, consumer_group, AzureEventHubConsumerGroup)


@pytest.mark.order(after="test_retrieve_event_hub_assets")
def test_delete_event_hub_consumer_group(
    client: AtlanClient,
    consumer_group: AzureEventHubConsumerGroup,
):
    response = client.asset.delete_by_guid(guid=consumer_group.guid)
    assert response
    assert not response.assets_created(asset_type=AzureEventHubConsumerGroup)
    assert not response.assets_updated(asset_type=AzureEventHubConsumerGroup)
    deleted = response.assets_deleted(asset_type=AzureEventHubConsumerGroup)

    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == consumer_group.guid
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED
    assert deleted[0].qualified_name == consumer_group.qualified_name


@pytest.mark.order(after="test_delete_event_hub_consumer_group")
def test_read_deleted_event_hub_consumer_group(
    client: AtlanClient,
    consumer_group: AzureEventHubConsumerGroup,
):
    deleted = client.asset.get_by_guid(
        consumer_group.guid, asset_type=AzureEventHubConsumerGroup
    )
    assert deleted
    assert deleted.status == EntityStatus.DELETED
    assert deleted.guid == consumer_group.guid
    assert deleted.qualified_name == consumer_group.qualified_name


@pytest.mark.order(after="test_read_deleted_event_hub_consumer_group")
def test_restore_event_hub_consumer_group(
    client: AtlanClient,
    consumer_group: AzureEventHubConsumerGroup,
):
    assert consumer_group.qualified_name
    assert client.asset.restore(
        asset_type=AzureEventHubConsumerGroup,
        qualified_name=consumer_group.qualified_name,
    )
    assert consumer_group.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=AzureEventHubConsumerGroup,
        qualified_name=consumer_group.qualified_name,
    )
    assert restored
    assert restored.guid == consumer_group.guid
    assert restored.status == EntityStatus.ACTIVE
    assert restored.qualified_name == consumer_group.qualified_name
