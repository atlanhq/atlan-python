# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .kafka import Kafka


class KafkaCluster(Kafka):
    """Description"""

    type_name: str = Field(default="KafkaCluster", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaCluster":
            raise ValueError("must be KafkaCluster")
        return v

    def __setattr__(self, name, value):
        if name in KafkaCluster._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    KAFKA_TOPIC_COUNT: ClassVar[NumericField] = NumericField(
        "kafkaTopicCount", "kafkaTopicCount"
    )
    """
    Number of topics in this cluster.
    """
    KAFKA_PARTITION_COUNT: ClassVar[NumericField] = NumericField(
        "kafkaPartitionCount", "kafkaPartitionCount"
    )
    """
    Total number of partitions across all topics in this cluster.
    """
    KAFKA_BROKER_COUNT: ClassVar[NumericField] = NumericField(
        "kafkaBrokerCount", "kafkaBrokerCount"
    )
    """
    Total number of brokers in this cluster.
    """
    KAFKA_BOOTSTRAP_SERVERS: ClassVar[KeywordField] = KeywordField(
        "kafkaBootstrapServers", "kafkaBootstrapServers"
    )
    """
    Bootstrap server addresses for this cluster.
    """
    KAFKA_CLUSTER_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "kafkaClusterType", "kafkaClusterType.keyword", "kafkaClusterType"
    )
    """
    Distribution type of this Kafka cluster, for example: Apache, Confluent, MSK, Aiven, Redpanda.
    """
    KAFKA_SCHEMA_REGISTRY_URL: ClassVar[KeywordField] = KeywordField(
        "kafkaSchemaRegistryUrl", "kafkaSchemaRegistryUrl"
    )
    """
    URL of the schema registry associated with this cluster.
    """
    KAFKA_AUTHENTICATION_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "kafkaAuthenticationType",
        "kafkaAuthenticationType.keyword",
        "kafkaAuthenticationType",
    )
    """
    Authentication type used to connect to this Kafka cluster, for example: SASL_PLAIN, SASL_SCRAM, TLS, IAM.
    """
    KAFKA_ENVIRONMENT: ClassVar[KeywordTextField] = KeywordTextField(
        "kafkaEnvironment", "kafkaEnvironment.keyword", "kafkaEnvironment"
    )
    """
    Environment classification of this Kafka cluster, for example: DEV, STAGING, PROD.
    """

    KAFKA_TOPICS: ClassVar[RelationField] = RelationField("kafkaTopics")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "kafka_topic_count",
        "kafka_partition_count",
        "kafka_broker_count",
        "kafka_bootstrap_servers",
        "kafka_cluster_type",
        "kafka_schema_registry_url",
        "kafka_authentication_type",
        "kafka_environment",
        "kafka_topics",
    ]

    @property
    def kafka_topic_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.kafka_topic_count

    @kafka_topic_count.setter
    def kafka_topic_count(self, kafka_topic_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic_count = kafka_topic_count

    @property
    def kafka_partition_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.kafka_partition_count
        )

    @kafka_partition_count.setter
    def kafka_partition_count(self, kafka_partition_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_partition_count = kafka_partition_count

    @property
    def kafka_broker_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.kafka_broker_count

    @kafka_broker_count.setter
    def kafka_broker_count(self, kafka_broker_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_broker_count = kafka_broker_count

    @property
    def kafka_bootstrap_servers(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.kafka_bootstrap_servers
        )

    @kafka_bootstrap_servers.setter
    def kafka_bootstrap_servers(self, kafka_bootstrap_servers: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_bootstrap_servers = kafka_bootstrap_servers

    @property
    def kafka_cluster_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.kafka_cluster_type

    @kafka_cluster_type.setter
    def kafka_cluster_type(self, kafka_cluster_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_cluster_type = kafka_cluster_type

    @property
    def kafka_schema_registry_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_schema_registry_url
        )

    @kafka_schema_registry_url.setter
    def kafka_schema_registry_url(self, kafka_schema_registry_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_schema_registry_url = kafka_schema_registry_url

    @property
    def kafka_authentication_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_authentication_type
        )

    @kafka_authentication_type.setter
    def kafka_authentication_type(self, kafka_authentication_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_authentication_type = kafka_authentication_type

    @property
    def kafka_environment(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.kafka_environment

    @kafka_environment.setter
    def kafka_environment(self, kafka_environment: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_environment = kafka_environment

    @property
    def kafka_topics(self) -> Optional[List[KafkaTopic]]:
        return None if self.attributes is None else self.attributes.kafka_topics

    @kafka_topics.setter
    def kafka_topics(self, kafka_topics: Optional[List[KafkaTopic]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topics = kafka_topics

    class Attributes(Kafka.Attributes):
        kafka_topic_count: Optional[int] = Field(default=None, description="")
        kafka_partition_count: Optional[int] = Field(default=None, description="")
        kafka_broker_count: Optional[int] = Field(default=None, description="")
        kafka_bootstrap_servers: Optional[Set[str]] = Field(
            default=None, description=""
        )
        kafka_cluster_type: Optional[str] = Field(default=None, description="")
        kafka_schema_registry_url: Optional[str] = Field(default=None, description="")
        kafka_authentication_type: Optional[str] = Field(default=None, description="")
        kafka_environment: Optional[str] = Field(default=None, description="")
        kafka_topics: Optional[List[KafkaTopic]] = Field(
            default=None, description=""
        )  # relationship

    attributes: KafkaCluster.Attributes = Field(
        default_factory=lambda: KafkaCluster.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .kafka_topic import KafkaTopic  # noqa: E402, F401

KafkaCluster.Attributes.update_forward_refs()
