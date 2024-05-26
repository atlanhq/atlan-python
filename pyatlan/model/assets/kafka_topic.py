# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import (
    AtlanConnectorType,
    KafkaTopicCleanupPolicy,
    KafkaTopicCompressionType,
)
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)
from pyatlan.utils import init_guid, validate_required_fields

from .kafka import Kafka


class KafkaTopic(Kafka):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> KafkaTopic:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = KafkaTopic.Attributes.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="KafkaTopic", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaTopic":
            raise ValueError("must be KafkaTopic")
        return v

    def __setattr__(self, name, value):
        if name in KafkaTopic._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    KAFKA_TOPIC_IS_INTERNAL: ClassVar[BooleanField] = BooleanField(
        "kafkaTopicIsInternal", "kafkaTopicIsInternal"
    )
    """
    Whether this topic is an internal topic (true) or not (false).
    """
    KAFKA_TOPIC_COMPRESSION_TYPE: ClassVar[KeywordField] = KeywordField(
        "kafkaTopicCompressionType", "kafkaTopicCompressionType"
    )
    """
    Type of compression used for this topic.
    """
    KAFKA_TOPIC_REPLICATION_FACTOR: ClassVar[NumericField] = NumericField(
        "kafkaTopicReplicationFactor", "kafkaTopicReplicationFactor"
    )
    """
    Replication factor for this topic.
    """
    KAFKA_TOPIC_SEGMENT_BYTES: ClassVar[NumericField] = NumericField(
        "kafkaTopicSegmentBytes", "kafkaTopicSegmentBytes"
    )
    """
    Segment size for this topic.
    """
    KAFKA_TOPIC_RETENTION_TIME_IN_MS: ClassVar[NumericField] = NumericField(
        "kafkaTopicRetentionTimeInMs", "kafkaTopicRetentionTimeInMs"
    )
    """
    Amount of time messages will be retained in this topic, in milliseconds.
    """
    KAFKA_TOPIC_PARTITIONS_COUNT: ClassVar[NumericField] = NumericField(
        "kafkaTopicPartitionsCount", "kafkaTopicPartitionsCount"
    )
    """
    Number of partitions for this topic.
    """
    KAFKA_TOPIC_SIZE_IN_BYTES: ClassVar[NumericField] = NumericField(
        "kafkaTopicSizeInBytes", "kafkaTopicSizeInBytes"
    )
    """
    Size of this topic, in bytes.
    """
    KAFKA_TOPIC_RECORD_COUNT: ClassVar[NumericField] = NumericField(
        "kafkaTopicRecordCount", "kafkaTopicRecordCount"
    )
    """
    Number of (unexpired) messages in this topic.
    """
    KAFKA_TOPIC_CLEANUP_POLICY: ClassVar[KeywordField] = KeywordField(
        "kafkaTopicCleanupPolicy", "kafkaTopicCleanupPolicy"
    )
    """
    Cleanup policy for this topic.
    """

    KAFKA_CONSUMER_GROUPS: ClassVar[RelationField] = RelationField(
        "kafkaConsumerGroups"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "kafka_topic_is_internal",
        "kafka_topic_compression_type",
        "kafka_topic_replication_factor",
        "kafka_topic_segment_bytes",
        "kafka_topic_retention_time_in_ms",
        "kafka_topic_partitions_count",
        "kafka_topic_size_in_bytes",
        "kafka_topic_record_count",
        "kafka_topic_cleanup_policy",
        "kafka_consumer_groups",
    ]

    @property
    def kafka_topic_is_internal(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.kafka_topic_is_internal
        )

    @kafka_topic_is_internal.setter
    def kafka_topic_is_internal(self, kafka_topic_is_internal: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_is_internal = kafka_topic_is_internal

    @property
    def kafka_topic_compression_type(self) -> Optional[KafkaTopicCompressionType]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_compression_type
        )

    @kafka_topic_compression_type.setter
    def kafka_topic_compression_type(
        self, kafka_topic_compression_type: Optional[KafkaTopicCompressionType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_compression_type = kafka_topic_compression_type

    @property
    def kafka_topic_replication_factor(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_replication_factor
        )

    @kafka_topic_replication_factor.setter
    def kafka_topic_replication_factor(
        self, kafka_topic_replication_factor: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_replication_factor = kafka_topic_replication_factor

    @property
    def kafka_topic_segment_bytes(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_segment_bytes
        )

    @kafka_topic_segment_bytes.setter
    def kafka_topic_segment_bytes(self, kafka_topic_segment_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_segment_bytes = kafka_topic_segment_bytes

    @property
    def kafka_topic_retention_time_in_ms(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_retention_time_in_ms
        )

    @kafka_topic_retention_time_in_ms.setter
    def kafka_topic_retention_time_in_ms(
        self, kafka_topic_retention_time_in_ms: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_retention_time_in_ms = (
            kafka_topic_retention_time_in_ms
        )

    @property
    def kafka_topic_partitions_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_partitions_count
        )

    @kafka_topic_partitions_count.setter
    def kafka_topic_partitions_count(self, kafka_topic_partitions_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_partitions_count = kafka_topic_partitions_count

    @property
    def kafka_topic_size_in_bytes(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_size_in_bytes
        )

    @kafka_topic_size_in_bytes.setter
    def kafka_topic_size_in_bytes(self, kafka_topic_size_in_bytes: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_size_in_bytes = kafka_topic_size_in_bytes

    @property
    def kafka_topic_record_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_record_count
        )

    @kafka_topic_record_count.setter
    def kafka_topic_record_count(self, kafka_topic_record_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_record_count = kafka_topic_record_count

    @property
    def kafka_topic_cleanup_policy(self) -> Optional[KafkaTopicCleanupPolicy]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_cleanup_policy
        )

    @kafka_topic_cleanup_policy.setter
    def kafka_topic_cleanup_policy(
        self, kafka_topic_cleanup_policy: Optional[KafkaTopicCleanupPolicy]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_cleanup_policy = kafka_topic_cleanup_policy

    @property
    def kafka_consumer_groups(self) -> Optional[List[KafkaConsumerGroup]]:
        return (
            None if self.attributes is None else self.attributes.kafka_consumer_groups
        )

    @kafka_consumer_groups.setter
    def kafka_consumer_groups(
        self, kafka_consumer_groups: Optional[List[KafkaConsumerGroup]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_consumer_groups = kafka_consumer_groups

    class Attributes(Kafka.Attributes):
        kafka_topic_is_internal: Optional[bool] = Field(default=None, description="")
        kafka_topic_compression_type: Optional[KafkaTopicCompressionType] = Field(
            default=None, description=""
        )
        kafka_topic_replication_factor: Optional[int] = Field(
            default=None, description=""
        )
        kafka_topic_segment_bytes: Optional[int] = Field(default=None, description="")
        kafka_topic_retention_time_in_ms: Optional[int] = Field(
            default=None, description=""
        )
        kafka_topic_partitions_count: Optional[int] = Field(
            default=None, description=""
        )
        kafka_topic_size_in_bytes: Optional[int] = Field(default=None, description="")
        kafka_topic_record_count: Optional[int] = Field(default=None, description="")
        kafka_topic_cleanup_policy: Optional[KafkaTopicCleanupPolicy] = Field(
            default=None, description=""
        )
        kafka_consumer_groups: Optional[List[KafkaConsumerGroup]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls, *, name: str, connection_qualified_name: str
        ) -> KafkaTopic.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return KafkaTopic.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/topic/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: KafkaTopic.Attributes = Field(
        default_factory=lambda: KafkaTopic.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .kafka_consumer_group import KafkaConsumerGroup  # noqa
