# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import Connection, KafkaConsumerGroup, KafkaTopic
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

MODULE_NAME = TestId.make_unique("KAFKA")

KAKFA_TOPIC_NAME = f"test_topic_{MODULE_NAME}"
KAKFA_CONSUMER_GROUP_NAME = f"test_consumer_group_{MODULE_NAME}"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED

ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


response = block(AtlanClient(), AssetMutationResponse())


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.KAFKA
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def kafka_topic(
    client: AtlanClient, connection: Connection
) -> Generator[KafkaTopic, None, None]:
    assert connection.qualified_name
    to_create = KafkaTopic.creator(
        name=KAKFA_TOPIC_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=KafkaTopic)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=KafkaTopic)


def test_kafka_topic(
    client: AtlanClient,
    connection: Connection,
    kafka_topic: KafkaTopic,
):
    assert kafka_topic
    assert kafka_topic.guid
    assert kafka_topic.qualified_name
    assert kafka_topic.name == KAKFA_TOPIC_NAME
    assert kafka_topic.connector_name == AtlanConnectorType.KAFKA
    assert kafka_topic.connection_qualified_name == connection.qualified_name


@pytest.fixture(scope="module")
def consumer_group(
    client: AtlanClient, kafka_topic: KafkaTopic
) -> Generator[KafkaConsumerGroup, None, None]:
    assert kafka_topic.qualified_name
    to_create = KafkaConsumerGroup.creator(
        name=KAKFA_CONSUMER_GROUP_NAME,
        kafka_topic_qualified_names=[kafka_topic.qualified_name],
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=KafkaConsumerGroup)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=KafkaConsumerGroup)


def test_kafka_consumer_group(
    client: AtlanClient,
    kafka_topic: KafkaTopic,
    consumer_group: KafkaConsumerGroup,
):
    assert consumer_group
    assert consumer_group.guid
    assert consumer_group.qualified_name
    assert consumer_group.name == KAKFA_CONSUMER_GROUP_NAME
    assert consumer_group.connector_name == AtlanConnectorType.KAFKA
    assert (
        kafka_topic.qualified_name
        and consumer_group.kafka_topic_qualified_names
        and kafka_topic.qualified_name in consumer_group.kafka_topic_qualified_names
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


def test_update_kafka_assets(
    client: AtlanClient,
    kafka_topic: KafkaTopic,
    consumer_group: KafkaConsumerGroup,
):
    _update_cert_and_annoucement(client, kafka_topic, KafkaTopic)
    _update_cert_and_annoucement(client, consumer_group, KafkaConsumerGroup)


def _retrieve_kafka_assets(client, asset, asset_type):
    retrieved = client.asset.get_by_guid(asset.guid, asset_type=asset_type)
    assert retrieved
    assert not retrieved.is_incomplete
    assert retrieved.guid == asset.guid
    assert retrieved.qualified_name == asset.qualified_name
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.KAFKA
    assert retrieved.certificate_status == CERTIFICATE_STATUS
    assert retrieved.certificate_status_message == CERTIFICATE_MESSAGE


@pytest.mark.order(after="test_update_kafka_assets")
def test_retrieve_kafka_assets(
    client: AtlanClient,
    kafka_topic: KafkaTopic,
    consumer_group: KafkaConsumerGroup,
):
    _retrieve_kafka_assets(client, kafka_topic, KafkaTopic)
    _retrieve_kafka_assets(client, consumer_group, KafkaConsumerGroup)


@pytest.mark.order(after="test_retrieve_kafka_assets")
def test_delete_kafka_consumer_group(
    client: AtlanClient,
    consumer_group: KafkaConsumerGroup,
):
    response = client.asset.delete_by_guid(guid=consumer_group.guid)
    assert response
    assert not response.assets_created(asset_type=KafkaConsumerGroup)
    assert not response.assets_updated(asset_type=KafkaConsumerGroup)
    deleted = response.assets_deleted(asset_type=KafkaConsumerGroup)

    assert deleted
    assert len(deleted) == 1
    assert deleted[0].guid == consumer_group.guid
    assert deleted[0].delete_handler == "SOFT"
    assert deleted[0].status == EntityStatus.DELETED
    assert deleted[0].qualified_name == consumer_group.qualified_name


@pytest.mark.order(after="test_delete_kafka_consumer_group")
def test_read_deleted_kafka_consumer_group(
    client: AtlanClient,
    consumer_group: KafkaConsumerGroup,
):
    deleted = client.asset.get_by_guid(
        consumer_group.guid, asset_type=KafkaConsumerGroup
    )
    assert deleted
    assert deleted.status == EntityStatus.DELETED
    assert deleted.guid == consumer_group.guid
    assert deleted.qualified_name == consumer_group.qualified_name


@pytest.mark.order(after="test_read_deleted_kafka_consumer_group")
def test_restore_kafka_consumer_group(
    client: AtlanClient,
    consumer_group: KafkaConsumerGroup,
):
    assert consumer_group.qualified_name
    assert client.asset.restore(
        asset_type=KafkaConsumerGroup, qualified_name=consumer_group.qualified_name
    )
    assert consumer_group.qualified_name
    restored = client.asset.get_by_qualified_name(
        asset_type=KafkaConsumerGroup, qualified_name=consumer_group.qualified_name
    )
    assert restored
    assert restored.guid == consumer_group.guid
    assert restored.status == EntityStatus.ACTIVE
    assert restored.qualified_name == consumer_group.qualified_name
