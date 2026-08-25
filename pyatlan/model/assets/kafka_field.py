# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
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
    KAFKA_PARENT_FIELD_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "kafkaParentFieldQualifiedName", "kafkaParentFieldQualifiedName"
    )
    """
    Unique name of the parent KafkaField in which this field is nested.
    """
    KAFKA_PARENT_FIELD_NAME: ClassVar[TextField] = TextField(
        "kafkaParentFieldName", "kafkaParentFieldName"
    )
    """
    Simple name of the parent KafkaField in which this field is nested.
    """
    KAFKA_FIELD_DEPTH_LEVEL: ClassVar[NumericField] = NumericField(
        "kafkaFieldDepthLevel", "kafkaFieldDepthLevel"
    )
    """
    Level of nesting of this field (1 = direct child of topic schema, 2 = nested one level, etc.).
    """
    KAFKA_NESTED_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "kafkaNestedFieldCount", "kafkaNestedFieldCount"
    )
    """
    Number of KafkaField assets directly nested within this field.
    """
    KAFKA_NESTED_FIELD_ORDER: ClassVar[TextField] = TextField(
        "kafkaNestedFieldOrder", "kafkaNestedFieldOrder"
    )
    """
    Order (position) in which this field appears within its parent nested field (nest level starts at 1).
    """
    KAFKA_FIELD_HIERARCHIES: ClassVar[KeywordField] = KeywordField(
        "kafkaFieldHierarchies", "kafkaFieldHierarchies"
    )
    """
    List of top-level upstream nested fields.
    """
    KAFKA_FIELD_NESTED_ORDER: ClassVar[KeywordTextField] = KeywordTextField(
        "kafkaFieldNestedOrder",
        "kafkaFieldNestedOrder.keyword",
        "kafkaFieldNestedOrder",
    )
    """
    Order (position) in which this field appears within its parent nested field, as a dotted ordinal path such as '1.2.10'. Carries the same value as kafkaNestedFieldOrder, which it supersedes; sortable in schema-declaration order via its version sub-field.
    """  # noqa: E501

    KAFKA_NESTED_FIELDS: ClassVar[RelationField] = RelationField("kafkaNestedFields")
    """
    TBC
    """
    KAFKA_TOPIC: ClassVar[RelationField] = RelationField("kafkaTopic")
    """
    TBC
    """
    KAFKA_PARENT_FIELD: ClassVar[RelationField] = RelationField("kafkaParentField")
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
        "kafka_parent_field_qualified_name",
        "kafka_parent_field_name",
        "kafka_field_depth_level",
        "kafka_nested_field_count",
        "kafka_nested_field_order",
        "kafka_field_hierarchies",
        "kafka_field_nested_order",
        "kafka_nested_fields",
        "kafka_topic",
        "kafka_parent_field",
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
    def kafka_parent_field_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_parent_field_qualified_name
        )

    @kafka_parent_field_qualified_name.setter
    def kafka_parent_field_qualified_name(
        self, kafka_parent_field_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_parent_field_qualified_name = (
            kafka_parent_field_qualified_name
        )

    @property
    def kafka_parent_field_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.kafka_parent_field_name
        )

    @kafka_parent_field_name.setter
    def kafka_parent_field_name(self, kafka_parent_field_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_parent_field_name = kafka_parent_field_name

    @property
    def kafka_field_depth_level(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.kafka_field_depth_level
        )

    @kafka_field_depth_level.setter
    def kafka_field_depth_level(self, kafka_field_depth_level: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_depth_level = kafka_field_depth_level

    @property
    def kafka_nested_field_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_nested_field_count
        )

    @kafka_nested_field_count.setter
    def kafka_nested_field_count(self, kafka_nested_field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_nested_field_count = kafka_nested_field_count

    @property
    def kafka_nested_field_order(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_nested_field_order
        )

    @kafka_nested_field_order.setter
    def kafka_nested_field_order(self, kafka_nested_field_order: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_nested_field_order = kafka_nested_field_order

    @property
    def kafka_field_hierarchies(self) -> Optional[List[Dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.kafka_field_hierarchies
        )

    @kafka_field_hierarchies.setter
    def kafka_field_hierarchies(
        self, kafka_field_hierarchies: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_hierarchies = kafka_field_hierarchies

    @property
    def kafka_field_nested_order(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.kafka_field_nested_order
        )

    @kafka_field_nested_order.setter
    def kafka_field_nested_order(self, kafka_field_nested_order: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_field_nested_order = kafka_field_nested_order

    @property
    def kafka_nested_fields(self) -> Optional[List[KafkaField]]:
        return None if self.attributes is None else self.attributes.kafka_nested_fields

    @kafka_nested_fields.setter
    def kafka_nested_fields(self, kafka_nested_fields: Optional[List[KafkaField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_nested_fields = kafka_nested_fields

    @property
    def kafka_topic(self) -> Optional[KafkaTopic]:
        return None if self.attributes is None else self.attributes.kafka_topic

    @kafka_topic.setter
    def kafka_topic(self, kafka_topic: Optional[KafkaTopic]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_topic = kafka_topic

    @property
    def kafka_parent_field(self) -> Optional[KafkaField]:
        return None if self.attributes is None else self.attributes.kafka_parent_field

    @kafka_parent_field.setter
    def kafka_parent_field(self, kafka_parent_field: Optional[KafkaField]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.kafka_parent_field = kafka_parent_field

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
        kafka_parent_field_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        kafka_parent_field_name: Optional[str] = Field(default=None, description="")
        kafka_field_depth_level: Optional[int] = Field(default=None, description="")
        kafka_nested_field_count: Optional[int] = Field(default=None, description="")
        kafka_nested_field_order: Optional[str] = Field(default=None, description="")
        kafka_field_hierarchies: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        kafka_field_nested_order: Optional[str] = Field(default=None, description="")
        kafka_nested_fields: Optional[List[KafkaField]] = Field(
            default=None, description=""
        )  # relationship
        kafka_topic: Optional[KafkaTopic] = Field(
            default=None, description=""
        )  # relationship
        kafka_parent_field: Optional[KafkaField] = Field(
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
