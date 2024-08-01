# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import SchemaRegistrySchemaType
from pyatlan.model.fields.atlan_fields import KeywordField

from .catalog import Catalog


class SchemaRegistry(Catalog):
    """Description"""

    type_name: str = Field(default="SchemaRegistry", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SchemaRegistry":
            raise ValueError("must be SchemaRegistry")
        return v

    def __setattr__(self, name, value):
        if name in SchemaRegistry._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SCHEMA_REGISTRY_SCHEMA_TYPE: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySchemaType", "schemaRegistrySchemaType"
    )
    """
    Type of language or specification used to define the schema, for example: JSON, Protobuf, etc.
    """
    SCHEMA_REGISTRY_SCHEMA_ID: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySchemaId", "schemaRegistrySchemaId"
    )
    """
    Unique identifier for schema definition set by the schema registry.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "schema_registry_schema_type",
        "schema_registry_schema_id",
    ]

    @property
    def schema_registry_schema_type(self) -> Optional[SchemaRegistrySchemaType]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_schema_type
        )

    @schema_registry_schema_type.setter
    def schema_registry_schema_type(
        self, schema_registry_schema_type: Optional[SchemaRegistrySchemaType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_schema_type = schema_registry_schema_type

    @property
    def schema_registry_schema_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_schema_id
        )

    @schema_registry_schema_id.setter
    def schema_registry_schema_id(self, schema_registry_schema_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_schema_id = schema_registry_schema_id

    class Attributes(Catalog.Attributes):
        schema_registry_schema_type: Optional[SchemaRegistrySchemaType] = Field(
            default=None, description=""
        )
        schema_registry_schema_id: Optional[str] = Field(default=None, description="")

    attributes: SchemaRegistry.Attributes = Field(
        default_factory=lambda: SchemaRegistry.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
