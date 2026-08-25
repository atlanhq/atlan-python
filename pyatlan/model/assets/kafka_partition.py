# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .kafka import Kafka


class KafkaPartition(Kafka):
    """Description"""

    type_name: str = Field(default="KafkaPartition", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaPartition":
            raise ValueError("must be KafkaPartition")
        return v

    def __setattr__(self, name, value):
        if name in KafkaPartition._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    KAFKA_PARTITION_ID: ClassVar[NumericField] = NumericField(
        "kafkaPartitionId", "kafkaPartitionId"
    )
    """
    Identifier of this partition within its topic.
    """
    KAFKA_PARTITION_LEADER_BROKER: ClassVar[NumericField] = NumericField(
        "kafkaPartitionLeaderBroker", "kafkaPartitionLeaderBroker"
    )
    """
    Broker ID of the leader for this partition.
    """
    KAFKA_PARTITION_IN_SYNC_REPLICAS: ClassVar[NumericField] = NumericField(
        "kafkaPartitionInSyncReplicas", "kafkaPartitionInSyncReplicas"
    )
    """
    Broker IDs of the in-sync replicas for this partition.
    """
    KAFKA_PARTITION_EARLIEST_OFFSET: ClassVar[NumericField] = NumericField(
        "kafkaPartitionEarliestOffset", "kafkaPartitionEarliestOffset"
    )
    """
    Earliest available offset for this partition.
    """
    KAFKA_PARTITION_LATEST_OFFSET: ClassVar[NumericField] = NumericField(
        "kafkaPartitionLatestOffset", "kafkaPartitionLatestOffset"
    )
    """
    Latest (high watermark) offset for this partition.
    """
    KAFKA_TOPIC_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "kafkaTopicQualifiedName", "kafkaTopicQualifiedName"
    )
    """
    Unique name of the Kafka topic to which this partition belongs.
    """

    KAFKA_TOPIC: ClassVar[RelationField] = RelationField("kafkaTopic")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "kafka_partition_id",
        "kafka_partition_leader_broker",
        "kafka_partition_in_sync_replicas",
        "kafka_partition_earliest_offset",
        "kafka_partition_latest_offset",
        "kafka_topic_qualified_name",
        "kafka_topic",
    ]

    @property
    def kafka_partition_id(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.kafka_partition_id

    @kafka_partition_id.setter
    def kafka_partition_id(self, kafka_partition_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_partition_id = kafka_partition_id

    @property
    def kafka_partition_leader_broker(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_partition_leader_broker
        )

    @kafka_partition_leader_broker.setter
    def kafka_partition_leader_broker(
        self, kafka_partition_leader_broker: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_partition_leader_broker = kafka_partition_leader_broker

    @property
    def kafka_partition_in_sync_replicas(self) -> Optional[Set[int]]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_partition_in_sync_replicas
        )

    @kafka_partition_in_sync_replicas.setter
    def kafka_partition_in_sync_replicas(
        self, kafka_partition_in_sync_replicas: Optional[Set[int]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_partition_in_sync_replicas = (
            kafka_partition_in_sync_replicas
        )

    @property
    def kafka_partition_earliest_offset(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_partition_earliest_offset
        )

    @kafka_partition_earliest_offset.setter
    def kafka_partition_earliest_offset(
        self, kafka_partition_earliest_offset: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_partition_earliest_offset = (
            kafka_partition_earliest_offset
        )

    @property
    def kafka_partition_latest_offset(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_partition_latest_offset
        )

    @kafka_partition_latest_offset.setter
    def kafka_partition_latest_offset(
        self, kafka_partition_latest_offset: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_partition_latest_offset = kafka_partition_latest_offset

    @property
    def kafka_topic_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_qualified_name
        )

    @kafka_topic_qualified_name.setter
    def kafka_topic_qualified_name(self, kafka_topic_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_qualified_name = kafka_topic_qualified_name

    @property
    def kafka_topic(self) -> Optional[KafkaTopic]:
        return None if self.attributes is None else self.attributes.kafka_topic

    @kafka_topic.setter
    def kafka_topic(self, kafka_topic: Optional[KafkaTopic]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic = kafka_topic

    class Attributes(Kafka.Attributes):
        kafka_partition_id: Optional[int] = Field(default=None, description="")
        kafka_partition_leader_broker: Optional[int] = Field(
            default=None, description=""
        )
        kafka_partition_in_sync_replicas: Optional[Set[int]] = Field(
            default=None, description=""
        )
        kafka_partition_earliest_offset: Optional[int] = Field(
            default=None, description=""
        )
        kafka_partition_latest_offset: Optional[int] = Field(
            default=None, description=""
        )
        kafka_topic_qualified_name: Optional[str] = Field(default=None, description="")
        kafka_topic: Optional[KafkaTopic] = Field(
            default=None, description=""
        )  # relationship

    attributes: KafkaPartition.Attributes = Field(
        default_factory=lambda: KafkaPartition.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .kafka_topic import KafkaTopic  # noqa: E402, F401

KafkaPartition.Attributes.update_forward_refs()
