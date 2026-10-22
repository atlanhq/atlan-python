# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    KafkaCluster,
    KafkaConsumerGroup,
    KafkaField,
    KafkaTopic,
    SchemaRegistrySubject,
    SchemaRegistryVersion,
)
from pyatlan_v9.model.core import Announcement
from pyatlan_v9.model.enums import (
    AnnouncementType,
    AtlanConnectorType,
    CertificateStatus,
    EntityStatus,
)
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("KAFKA")

KAKFA_TOPIC_NAME = f"test_topic_{MODULE_NAME}"
KAKFA_CONSUMER_GROUP_NAME = f"test_consumer_group_{MODULE_NAME}"
KAFKA_CLUSTER_NAME = f"test_cluster_{MODULE_NAME}"
KAFKA_FIELD_PARENT_NAME = "customer"
KAFKA_FIELD_NAME = "customer.city"
SCHEMA_REGISTRY_SUBJECT_NAME = f"test_subject_{MODULE_NAME}-value"
CERTIFICATE_STATUS = CertificateStatus.VERIFIED

ANNOUNCEMENT_TITLE = "Python SDK testing."
ANNOUNCEMENT_TYPE = AnnouncementType.INFORMATION
CERTIFICATE_MESSAGE = "Automated testing of the Python SDK."
ANNOUNCEMENT_MESSAGE = "Automated testing of the Python SDK."


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
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
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
        consumer_group.guid, asset_type=KafkaConsumerGroup, ignore_relationships=False
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
        asset_type=KafkaConsumerGroup,
        qualified_name=consumer_group.qualified_name,
        ignore_relationships=False,
    )
    assert restored
    assert restored.guid == consumer_group.guid
    assert restored.status == EntityStatus.ACTIVE
    assert restored.qualified_name == consumer_group.qualified_name


@pytest.fixture(scope="module")
def kafka_cluster(
    client: AtlanClient, connection: Connection
) -> Generator[KafkaCluster, None, None]:
    assert connection.qualified_name
    to_create = KafkaCluster.creator(
        name=KAFKA_CLUSTER_NAME, connection_qualified_name=connection.qualified_name
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=KafkaCluster)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=KafkaCluster)


def test_kafka_cluster(
    client: AtlanClient, connection: Connection, kafka_cluster: KafkaCluster
):
    assert kafka_cluster.guid
    assert (
        kafka_cluster.qualified_name
        == f"{connection.qualified_name}/cluster/{KAFKA_CLUSTER_NAME}"
    )
    assert kafka_cluster.name == KAFKA_CLUSTER_NAME
    assert kafka_cluster.connector_name == AtlanConnectorType.KAFKA
    assert kafka_cluster.connection_qualified_name == connection.qualified_name


@pytest.fixture(scope="module")
def kafka_parent_field(
    client: AtlanClient, kafka_topic: KafkaTopic
) -> Generator[KafkaField, None, None]:
    assert kafka_topic.qualified_name
    to_create = KafkaField.creator(
        name=KAFKA_FIELD_PARENT_NAME,
        kafka_topic_qualified_name=kafka_topic.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=KafkaField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=KafkaField)


@pytest.fixture(scope="module")
def kafka_field(
    client: AtlanClient, kafka_topic: KafkaTopic, kafka_parent_field: KafkaField
) -> Generator[KafkaField, None, None]:
    assert kafka_topic.qualified_name
    to_create = KafkaField.creator(
        name=KAFKA_FIELD_NAME,
        kafka_topic_qualified_name=kafka_topic.qualified_name,
        parent_field_path=KAFKA_FIELD_PARENT_NAME,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=KafkaField)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=KafkaField)


def test_kafka_field(
    client: AtlanClient,
    connection: Connection,
    kafka_topic: KafkaTopic,
    kafka_parent_field: KafkaField,
    kafka_field: KafkaField,
):
    assert kafka_parent_field.guid
    assert (
        kafka_parent_field.qualified_name
        == f"{kafka_topic.qualified_name}/field/{KAFKA_FIELD_PARENT_NAME}"
    )
    assert kafka_field.guid
    assert (
        kafka_field.qualified_name
        == f"{kafka_topic.qualified_name}/field/{KAFKA_FIELD_NAME}"
    )
    assert kafka_field.name == KAFKA_FIELD_NAME
    assert kafka_field.connector_name == AtlanConnectorType.KAFKA
    assert kafka_field.connection_qualified_name == connection.qualified_name

    assert kafka_field.qualified_name
    retrieved = client.asset.get_by_qualified_name(
        asset_type=KafkaField,
        qualified_name=kafka_field.qualified_name,
        ignore_relationships=False,
    )
    assert retrieved.guid == kafka_field.guid
    assert retrieved.kafka_topic_qualified_name == kafka_topic.qualified_name
    assert (
        retrieved.kafka_parent_field_qualified_name == kafka_parent_field.qualified_name
    )
    assert retrieved.kafka_parent_field_name == KAFKA_FIELD_PARENT_NAME
    assert retrieved.kafka_topic
    assert retrieved.kafka_topic.guid == kafka_topic.guid


@pytest.fixture(scope="module")
def schema_registry_subject(
    client: AtlanClient, connection: Connection
) -> Generator[SchemaRegistrySubject, None, None]:
    # SchemaRegistrySubject has no creator yet; build it as atlan-kafka-app does.
    assert connection.qualified_name
    to_create = SchemaRegistrySubject(
        name=SCHEMA_REGISTRY_SUBJECT_NAME,
        qualified_name=f"{connection.qualified_name}/subject/{SCHEMA_REGISTRY_SUBJECT_NAME}",
        connection_qualified_name=connection.qualified_name,
        connector_name=AtlanConnectorType.KAFKA.value,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SchemaRegistrySubject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SchemaRegistrySubject)


@pytest.fixture(scope="module")
def schema_registry_version(
    client: AtlanClient, schema_registry_subject: SchemaRegistrySubject
) -> Generator[SchemaRegistryVersion, None, None]:
    assert schema_registry_subject.qualified_name
    to_create = SchemaRegistryVersion.creator(
        schema_registry_version_number=1,
        schema_registry_subject_qualified_name=schema_registry_subject.qualified_name,
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=SchemaRegistryVersion)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=SchemaRegistryVersion)


def test_schema_registry_version(
    client: AtlanClient,
    connection: Connection,
    schema_registry_subject: SchemaRegistrySubject,
    schema_registry_version: SchemaRegistryVersion,
):
    assert schema_registry_version.guid
    assert (
        schema_registry_version.qualified_name
        == f"{schema_registry_subject.qualified_name}/version/1"
    )
    assert schema_registry_version.name == f"{SCHEMA_REGISTRY_SUBJECT_NAME}.v1"
    assert schema_registry_version.connector_name == AtlanConnectorType.KAFKA
    assert (
        schema_registry_version.connection_qualified_name == connection.qualified_name
    )

    assert schema_registry_version.qualified_name
    retrieved = client.asset.get_by_qualified_name(
        asset_type=SchemaRegistryVersion,
        qualified_name=schema_registry_version.qualified_name,
        ignore_relationships=False,
    )
    assert retrieved.guid == schema_registry_version.guid
    assert retrieved.schema_registry_version_number == "1"
    assert (
        retrieved.schema_registry_subject_qualified_name
        == schema_registry_subject.qualified_name
    )
    assert retrieved.schema_registry_subject
    assert retrieved.schema_registry_subject.guid == schema_registry_subject.guid
