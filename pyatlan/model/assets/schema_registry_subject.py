# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import SchemaRegistrySchemaCompatibility
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    RelationField,
    TextField,
)

from .schema_registry import SchemaRegistry


class SchemaRegistrySubject(SchemaRegistry):
    """Description"""

    type_name: str = Field(default="SchemaRegistrySubject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SchemaRegistrySubject":
            raise ValueError("must be SchemaRegistrySubject")
        return v

    def __setattr__(self, name, value):
        if name in SchemaRegistrySubject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SCHEMA_REGISTRY_SUBJECT_BASE_NAME: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySubjectBaseName", "schemaRegistrySubjectBaseName"
    )
    """
    Base name of the subject, without -key, -value prefixes.
    """
    SCHEMA_REGISTRY_SUBJECT_IS_KEY_SCHEMA: ClassVar[BooleanField] = BooleanField(
        "schemaRegistrySubjectIsKeySchema", "schemaRegistrySubjectIsKeySchema"
    )
    """
    Whether the subject is a schema for the keys of the messages (true) or not (false).
    """
    SCHEMA_REGISTRY_SUBJECT_SCHEMA_COMPATIBILITY: ClassVar[KeywordField] = KeywordField(
        "schemaRegistrySubjectSchemaCompatibility",
        "schemaRegistrySubjectSchemaCompatibility",
    )
    """
    Compatibility of the schema across versions.
    """
    SCHEMA_REGISTRY_SUBJECT_LATEST_SCHEMA_VERSION: ClassVar[KeywordField] = (
        KeywordField(
            "schemaRegistrySubjectLatestSchemaVersion",
            "schemaRegistrySubjectLatestSchemaVersion",
        )
    )
    """
    Latest schema version of the subject.
    """
    SCHEMA_REGISTRY_SUBJECT_LATEST_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "schemaRegistrySubjectLatestSchemaDefinition",
        "schemaRegistrySubjectLatestSchemaDefinition",
    )
    """
    Definition of the latest schema in the subject.
    """
    SCHEMA_REGISTRY_SUBJECT_GOVERNING_ASSET_QUALIFIED_NAMES: ClassVar[KeywordField] = (
        KeywordField(
            "schemaRegistrySubjectGoverningAssetQualifiedNames",
            "schemaRegistrySubjectGoverningAssetQualifiedNames",
        )
    )
    """
    List of asset qualified names that this subject is governing/validating.
    """

    ASSETS: ClassVar[RelationField] = RelationField("assets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "schema_registry_subject_base_name",
        "schema_registry_subject_is_key_schema",
        "schema_registry_subject_schema_compatibility",
        "schema_registry_subject_latest_schema_version",
        "schema_registry_subject_latest_schema_definition",
        "schema_registry_subject_governing_asset_qualified_names",
        "assets",
    ]

    @property
    def schema_registry_subject_base_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_base_name
        )

    @schema_registry_subject_base_name.setter
    def schema_registry_subject_base_name(
        self, schema_registry_subject_base_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_base_name = (
            schema_registry_subject_base_name
        )

    @property
    def schema_registry_subject_is_key_schema(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_is_key_schema
        )

    @schema_registry_subject_is_key_schema.setter
    def schema_registry_subject_is_key_schema(
        self, schema_registry_subject_is_key_schema: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_is_key_schema = (
            schema_registry_subject_is_key_schema
        )

    @property
    def schema_registry_subject_schema_compatibility(
        self,
    ) -> Optional[SchemaRegistrySchemaCompatibility]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_schema_compatibility
        )

    @schema_registry_subject_schema_compatibility.setter
    def schema_registry_subject_schema_compatibility(
        self,
        schema_registry_subject_schema_compatibility: Optional[
            SchemaRegistrySchemaCompatibility
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_schema_compatibility = (
            schema_registry_subject_schema_compatibility
        )

    @property
    def schema_registry_subject_latest_schema_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_latest_schema_version
        )

    @schema_registry_subject_latest_schema_version.setter
    def schema_registry_subject_latest_schema_version(
        self, schema_registry_subject_latest_schema_version: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_latest_schema_version = (
            schema_registry_subject_latest_schema_version
        )

    @property
    def schema_registry_subject_latest_schema_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_latest_schema_definition
        )

    @schema_registry_subject_latest_schema_definition.setter
    def schema_registry_subject_latest_schema_definition(
        self, schema_registry_subject_latest_schema_definition: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_latest_schema_definition = (
            schema_registry_subject_latest_schema_definition
        )

    @property
    def schema_registry_subject_governing_asset_qualified_names(
        self,
    ) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.schema_registry_subject_governing_asset_qualified_names
        )

    @schema_registry_subject_governing_asset_qualified_names.setter
    def schema_registry_subject_governing_asset_qualified_names(
        self,
        schema_registry_subject_governing_asset_qualified_names: Optional[Set[str]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.schema_registry_subject_governing_asset_qualified_names = (
            schema_registry_subject_governing_asset_qualified_names
        )

    @property
    def assets(self) -> Optional[List[Asset]]:
        return None if self.attributes is None else self.attributes.assets

    @assets.setter
    def assets(self, assets: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.assets = assets

    class Attributes(SchemaRegistry.Attributes):
        schema_registry_subject_base_name: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_subject_is_key_schema: Optional[bool] = Field(
            default=None, description=""
        )
        schema_registry_subject_schema_compatibility: Optional[
            SchemaRegistrySchemaCompatibility
        ] = Field(default=None, description="")
        schema_registry_subject_latest_schema_version: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_subject_latest_schema_definition: Optional[str] = Field(
            default=None, description=""
        )
        schema_registry_subject_governing_asset_qualified_names: Optional[Set[str]] = (
            Field(default=None, description="")
        )
        assets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SchemaRegistrySubject.Attributes = Field(
        default_factory=lambda: SchemaRegistrySubject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
