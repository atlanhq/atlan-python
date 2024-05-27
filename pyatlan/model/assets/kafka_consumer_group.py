# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField
from pyatlan.model.structs import KafkaTopicConsumption
from pyatlan.utils import init_guid, validate_required_fields

from .kafka import Kafka


class KafkaConsumerGroup(Kafka):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        kafka_topic_qualified_names: List[str],
    ) -> KafkaConsumerGroup:
        validate_required_fields(
            ["name", "kafka_topic_qualified_names"],
            [name, kafka_topic_qualified_names],
        )
        attributes = KafkaConsumerGroup.Attributes.creator(
            name=name,
            kafka_topic_qualified_names=kafka_topic_qualified_names,
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="KafkaConsumerGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaConsumerGroup":
            raise ValueError("must be KafkaConsumerGroup")
        return v

    def __setattr__(self, name, value):
        if name in KafkaConsumerGroup._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    KAFKA_CONSUMER_GROUP_TOPIC_CONSUMPTION_PROPERTIES: ClassVar[KeywordField] = (
        KeywordField(
            "kafkaConsumerGroupTopicConsumptionProperties",
            "kafkaConsumerGroupTopicConsumptionProperties",
        )
    )
    """
    List of consumption properties for Kafka topics, for this consumer group.
    """
    KAFKA_CONSUMER_GROUP_MEMBER_COUNT: ClassVar[NumericField] = NumericField(
        "kafkaConsumerGroupMemberCount", "kafkaConsumerGroupMemberCount"
    )
    """
    Number of members in this consumer group.
    """
    KAFKA_TOPIC_NAMES: ClassVar[KeywordField] = KeywordField(
        "kafkaTopicNames", "kafkaTopicNames"
    )
    """
    Simple names of the topics consumed by this consumer group.
    """
    KAFKA_TOPIC_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "kafkaTopicQualifiedNames", "kafkaTopicQualifiedNames"
    )
    """
    Unique names of the topics consumed by this consumer group.
    """

    KAFKA_TOPICS: ClassVar[RelationField] = RelationField("kafkaTopics")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "kafka_consumer_group_topic_consumption_properties",
        "kafka_consumer_group_member_count",
        "kafka_topic_names",
        "kafka_topic_qualified_names",
        "kafka_topics",
    ]

    @property
    def kafka_consumer_group_topic_consumption_properties(
        self,
    ) -> Optional[List[KafkaTopicConsumption]]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_consumer_group_topic_consumption_properties
        )

    @kafka_consumer_group_topic_consumption_properties.setter
    def kafka_consumer_group_topic_consumption_properties(
        self,
        kafka_consumer_group_topic_consumption_properties: Optional[
            List[KafkaTopicConsumption]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_consumer_group_topic_consumption_properties = (
            kafka_consumer_group_topic_consumption_properties
        )

    @property
    def kafka_consumer_group_member_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_consumer_group_member_count
        )

    @kafka_consumer_group_member_count.setter
    def kafka_consumer_group_member_count(
        self, kafka_consumer_group_member_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_consumer_group_member_count = (
            kafka_consumer_group_member_count
        )

    @property
    def kafka_topic_names(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.kafka_topic_names

    @kafka_topic_names.setter
    def kafka_topic_names(self, kafka_topic_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_names = kafka_topic_names

    @property
    def kafka_topic_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_topic_qualified_names
        )

    @kafka_topic_qualified_names.setter
    def kafka_topic_qualified_names(
        self, kafka_topic_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_qualified_names = kafka_topic_qualified_names

    @property
    def kafka_topics(self) -> Optional[List[KafkaTopic]]:
        return None if self.attributes is None else self.attributes.kafka_topics

    @kafka_topics.setter
    def kafka_topics(self, kafka_topics: Optional[List[KafkaTopic]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topics = kafka_topics

    class Attributes(Kafka.Attributes):
        kafka_consumer_group_topic_consumption_properties: Optional[
            List[KafkaTopicConsumption]
        ] = Field(default=None, description="")
        kafka_consumer_group_member_count: Optional[int] = Field(
            default=None, description=""
        )
        kafka_topic_names: Optional[Set[str]] = Field(default=None, description="")
        kafka_topic_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        kafka_topics: Optional[List[KafkaTopic]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            name: str,
            kafka_topic_qualified_names: List[str],
        ) -> KafkaConsumerGroup.Attributes:
            validate_required_fields(
                ["name", "kafka_topic_qualified_names"],
                [name, kafka_topic_qualified_names],
            )
            kafka_topics = []
            for kafka_topic_qn in kafka_topic_qualified_names:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    kafka_topic_qn, "kafka_topic_qualified_names", 5
                )
                kafka_topics.append(KafkaTopic.ref_by_qualified_name(kafka_topic_qn))

            return KafkaConsumerGroup.Attributes(
                name=name,
                connector_name=connector_name,
                connection_qualified_name=connection_qn,
                kafka_topics=kafka_topics,
                kafka_topic_qualified_names=set(kafka_topic_qualified_names),
                qualified_name=f"{connection_qn}/consumer-group/{name}",
            )

    attributes: KafkaConsumerGroup.Attributes = Field(
        default_factory=lambda: KafkaConsumerGroup.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .kafka_topic import KafkaTopic  # noqa
