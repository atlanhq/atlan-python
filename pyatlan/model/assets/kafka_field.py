# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .kafka import Kafka


class KafkaField(Kafka):
    """Description"""

    type_name: str = Field(default="KafkaField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "KafkaField":
            raise ValueError("must be KafkaField")
        return v

    def __setattr__(self, name, value):
        if name in KafkaField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    KAFKA_FIELD_DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "kafkaFieldDataType", "kafkaFieldDataType.keyword", "kafkaFieldDataType"
    )
    """
    Data type of this field as defined in the schema, for example: string, int, record.
    """
    KAFKA_FIELD_IS_OPTIONAL: ClassVar[BooleanField] = BooleanField(
        "kafkaFieldIsOptional", "kafkaFieldIsOptional"
    )
    """
    Whether this field is optional (true) or required (false) in the schema.
    """
    KAFKA_FIELD_DEFAULT_VALUE: ClassVar[KeywordField] = KeywordField(
        "kafkaFieldDefaultValue", "kafkaFieldDefaultValue"
    )
    """
    Default value for this field if one is defined in the schema.
    """
    KAFKA_FIELD_VERSION_INTRODUCED: ClassVar[KeywordField] = KeywordField(
        "kafkaFieldVersionIntroduced", "kafkaFieldVersionIntroduced"
    )
    """
    Schema version in which this field was first introduced.
    """
    KAFKA_FIELD_ORDER: ClassVar[NumericField] = NumericField(
        "kafkaFieldOrder", "kafkaFieldOrder"
    )
    """
    Position (0-based) of this field in the schema definition.
    """
    KAFKA_TOPIC_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "kafkaTopicQualifiedName", "kafkaTopicQualifiedName"
    )
    """
    Unique name of the Kafka topic in which this field exists.
    """
    KAFKA_FIELD_SCHEMA_TYPE: ClassVar[KeywordField] = KeywordField(
        "kafkaFieldSchemaType", "kafkaFieldSchemaType"
    )
    """
    Type of schema from which this field is derived, for example: key or value.
    """

    KAFKA_TOPIC: ClassVar[RelationField] = RelationField("kafkaTopic")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "kafka_field_data_type",
        "kafka_field_is_optional",
        "kafka_field_default_value",
        "kafka_field_version_introduced",
        "kafka_field_order",
        "kafka_topic_qualified_name",
        "kafka_field_schema_type",
        "kafka_topic",
    ]

    @property
    def kafka_field_data_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.kafka_field_data_type
        )

    @kafka_field_data_type.setter
    def kafka_field_data_type(self, kafka_field_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_data_type = kafka_field_data_type

    @property
    def kafka_field_is_optional(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.kafka_field_is_optional
        )

    @kafka_field_is_optional.setter
    def kafka_field_is_optional(self, kafka_field_is_optional: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_is_optional = kafka_field_is_optional

    @property
    def kafka_field_default_value(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_field_default_value
        )

    @kafka_field_default_value.setter
    def kafka_field_default_value(self, kafka_field_default_value: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_default_value = kafka_field_default_value

    @property
    def kafka_field_version_introduced(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_field_version_introduced
        )

    @kafka_field_version_introduced.setter
    def kafka_field_version_introduced(
        self, kafka_field_version_introduced: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_version_introduced = kafka_field_version_introduced

    @property
    def kafka_field_order(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.kafka_field_order

    @kafka_field_order.setter
    def kafka_field_order(self, kafka_field_order: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_order = kafka_field_order

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
    def kafka_field_schema_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.kafka_field_schema_type
        )

    @kafka_field_schema_type.setter
    def kafka_field_schema_type(self, kafka_field_schema_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_schema_type = kafka_field_schema_type

    @property
    def kafka_topic(self) -> Optional[KafkaTopic]:
        return None if self.attributes is None else self.attributes.kafka_topic

    @kafka_topic.setter
    def kafka_topic(self, kafka_topic: Optional[KafkaTopic]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic = kafka_topic

    class Attributes(Kafka.Attributes):
        kafka_field_data_type: Optional[str] = Field(default=None, description="")
        kafka_field_is_optional: Optional[bool] = Field(default=None, description="")
        kafka_field_default_value: Optional[str] = Field(default=None, description="")
        kafka_field_version_introduced: Optional[str] = Field(
            default=None, description=""
        )
        kafka_field_order: Optional[int] = Field(default=None, description="")
        kafka_topic_qualified_name: Optional[str] = Field(default=None, description="")
        kafka_field_schema_type: Optional[str] = Field(default=None, description="")
        kafka_topic: Optional[KafkaTopic] = Field(
            default=None, description=""
        )  # relationship

    attributes: KafkaField.Attributes = Field(
        default_factory=lambda: KafkaField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .kafka_topic import KafkaTopic  # noqa: E402, F401

KafkaField.Attributes.update_forward_refs()
