# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import SchemaRegistrySchemaType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .schema_registry import SchemaRegistry


class SchemaRegistryVersion(SchemaRegistry):
    """Description"""

    type_name: str = Field(default="SchemaRegistryVersion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SchemaRegistryVersion":
            raise ValueError("must be SchemaRegistryVersion")
        return v

    def __setattr__(self, name, value):
        if name in SchemaRegistryVersion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SCHEMA_REGISTRY_VERSION_NUMBER: ClassVar[KeywordField] = KeywordField(
        "schemaRegistryVersionNumber", "schemaRegistryVersionNumber"
    )
    """
    Version number of this schema version.
    """
    SCHEMA_REGISTRY_VERSION_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "schemaRegistryVersionSchemaDefinition", "schemaRegistryVersionSchemaDefinition"
    )
    """
    Full schema definition for this specific version.
    """
    SCHEMA_REGISTRY_VERSION_SCHEMA_TYPE: ClassVar[KeywordField] = KeywordField(
        "schemaRegistryVersionSchemaType", "schemaRegistryVersionSchemaType"
    )
    """
    Type of schema language used in this version.
    """
    SCHEMA_REGISTRY_SUBJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySubjectQualifiedName", "schemaRegistrySubjectQualifiedName"
    )
    """
    Unique name of the schema registry subject to which this version belongs.
    """

    SCHEMA_REGISTRY_SUBJECT: ClassVar[RelationField] = RelationField(
        "schemaRegistrySubject"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "schema_registry_version_number",
        "schema_registry_version_schema_definition",
        "schema_registry_version_schema_type",
        "schema_registry_subject_qualified_name",
        "schema_registry_subject",
    ]

    @property
    def schema_registry_version_number(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_version_number
        )

    @schema_registry_version_number.setter
    def schema_registry_version_number(
        self, schema_registry_version_number: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_version_number = schema_registry_version_number

    @property
    def schema_registry_version_schema_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_version_schema_definition
        )

    @schema_registry_version_schema_definition.setter
    def schema_registry_version_schema_definition(
        self, schema_registry_version_schema_definition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_version_schema_definition = (
            schema_registry_version_schema_definition
        )

    @property
    def schema_registry_version_schema_type(self) -> Optional[SchemaRegistrySchemaType]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_version_schema_type
        )

    @schema_registry_version_schema_type.setter
    def schema_registry_version_schema_type(
        self, schema_registry_version_schema_type: Optional[SchemaRegistrySchemaType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_version_schema_type = (
            schema_registry_version_schema_type
        )

    @property
    def schema_registry_subject_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_qualified_name
        )

    @schema_registry_subject_qualified_name.setter
    def schema_registry_subject_qualified_name(
        self, schema_registry_subject_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_qualified_name = (
            schema_registry_subject_qualified_name
        )

    @property
    def schema_registry_subject(self) -> Optional[SchemaRegistrySubject]:
        return (
            None if self.attributes is None else self.attributes.schema_registry_subject
        )

    @schema_registry_subject.setter
    def schema_registry_subject(
        self, schema_registry_subject: Optional[SchemaRegistrySubject]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject = schema_registry_subject

    class Attributes(SchemaRegistry.Attributes):
        schema_registry_version_number: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_version_schema_definition: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_version_schema_type: Optional[SchemaRegistrySchemaType] = Field(
            default=None, description=""
        )
        schema_registry_subject_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_subject: Optional[SchemaRegistrySubject] = Field(
            default=None, description=""
        )  # relationship

    attributes: SchemaRegistryVersion.Attributes = Field(
        default_factory=lambda: SchemaRegistryVersion.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .schema_registry_subject import SchemaRegistrySubject  # noqa: E402, F401
