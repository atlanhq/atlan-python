# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .data_modeling import DataModeling


class DataAttribute(DataModeling):
    """Description"""

    type_name: str = Field(default="DataAttribute", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataAttribute":
            raise ValueError("must be DataAttribute")
        return v

    def __setattr__(self, name, value):
        if name in DataAttribute._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_ENTITY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dataEntityQualifiedName", "dataEntityQualifiedName"
    )
    """

    """
    DATA_ATTRIBUTE_ID: ClassVar[KeywordField] = KeywordField(
        "dataAttributeId", "dataAttributeId"
    )
    """

    """
    DATA_ATTRIBUTE_FULLY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dataAttributeFullyQualifiedName", "dataAttributeFullyQualifiedName"
    )
    """

    """
    DATA_ATTRIBUTE_TYPE: ClassVar[KeywordField] = KeywordField(
        "dataAttributeType", "dataAttributeType"
    )
    """

    """
    DATA_ATTRIBUTE_NULLABILITY: ClassVar[BooleanField] = BooleanField(
        "dataAttributeNullability", "dataAttributeNullability"
    )
    """

    """
    DATA_ATTRIBUTE_PRIMARY_KEY_INDICATOR: ClassVar[BooleanField] = BooleanField(
        "dataAttributePrimaryKeyIndicator", "dataAttributePrimaryKeyIndicator"
    )
    """

    """
    DATA_ATTRIBUTE_FOREIGN_KEY_INDICATOR: ClassVar[BooleanField] = BooleanField(
        "dataAttributeForeignKeyIndicator", "dataAttributeForeignKeyIndicator"
    )
    """

    """
    DATA_ATTRIBUTE_MULTIPLICITY: ClassVar[KeywordField] = KeywordField(
        "dataAttributeMultiplicity", "dataAttributeMultiplicity"
    )
    """

    """
    DATA_ATTRIBUTE_DERIVED_INDICATOR: ClassVar[BooleanField] = BooleanField(
        "dataAttributeDerivedIndicator", "dataAttributeDerivedIndicator"
    )
    """

    """
    DATA_ATTRIBUTE_PERSONAL_IDENTIFIER_INDICATOR: ClassVar[BooleanField] = BooleanField(
        "dataAttributePersonalIdentifierIndicator",
        "dataAttributePersonalIdentifierIndicator",
    )
    """

    """
    DATA_ATTRIBUTE_DIRECT_IDENTIFIER_INDICATOR: ClassVar[BooleanField] = BooleanField(
        "dataAttributeDirectIdentifierIndicator",
        "dataAttributeDirectIdentifierIndicator",
    )
    """

    """

    MAPPED_GLOSSARY_TERMS: ClassVar[RelationField] = RelationField(
        "mappedGlossaryTerms"
    )
    """
    TBC
    """
    SOURCE_DATA_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "sourceDataAttributes"
    )
    """
    TBC
    """
    TARGET_DATA_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "targetDataAttributes"
    )
    """
    TBC
    """
    DATA_ENTITIES: ClassVar[RelationField] = RelationField("dataEntities")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_entity_qualified_name",
        "data_attribute_id",
        "data_attribute_fully_qualified_name",
        "data_attribute_type",
        "data_attribute_nullability",
        "data_attribute_primary_key_indicator",
        "data_attribute_foreign_key_indicator",
        "data_attribute_multiplicity",
        "data_attribute_derived_indicator",
        "data_attribute_personal_identifier_indicator",
        "data_attribute_direct_identifier_indicator",
        "mapped_glossary_terms",
        "source_data_attributes",
        "target_data_attributes",
        "data_entities",
    ]

    @property
    def data_entity_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_entity_qualified_name
        )

    @data_entity_qualified_name.setter
    def data_entity_qualified_name(self, data_entity_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_entity_qualified_name = data_entity_qualified_name

    @property
    def data_attribute_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_attribute_id

    @data_attribute_id.setter
    def data_attribute_id(self, data_attribute_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_id = data_attribute_id

    @property
    def data_attribute_fully_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_attribute_fully_qualified_name
        )

    @data_attribute_fully_qualified_name.setter
    def data_attribute_fully_qualified_name(
        self, data_attribute_fully_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_fully_qualified_name = (
            data_attribute_fully_qualified_name
        )

    @property
    def data_attribute_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_attribute_type

    @data_attribute_type.setter
    def data_attribute_type(self, data_attribute_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_type = data_attribute_type

    @property
    def data_attribute_nullability(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_attribute_nullability
        )

    @data_attribute_nullability.setter
    def data_attribute_nullability(self, data_attribute_nullability: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_nullability = data_attribute_nullability

    @property
    def data_attribute_primary_key_indicator(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_attribute_primary_key_indicator
        )

    @data_attribute_primary_key_indicator.setter
    def data_attribute_primary_key_indicator(
        self, data_attribute_primary_key_indicator: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_primary_key_indicator = (
            data_attribute_primary_key_indicator
        )

    @property
    def data_attribute_foreign_key_indicator(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_attribute_foreign_key_indicator
        )

    @data_attribute_foreign_key_indicator.setter
    def data_attribute_foreign_key_indicator(
        self, data_attribute_foreign_key_indicator: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_foreign_key_indicator = (
            data_attribute_foreign_key_indicator
        )

    @property
    def data_attribute_multiplicity(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_attribute_multiplicity
        )

    @data_attribute_multiplicity.setter
    def data_attribute_multiplicity(self, data_attribute_multiplicity: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_multiplicity = data_attribute_multiplicity

    @property
    def data_attribute_derived_indicator(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_attribute_derived_indicator
        )

    @data_attribute_derived_indicator.setter
    def data_attribute_derived_indicator(
        self, data_attribute_derived_indicator: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_derived_indicator = (
            data_attribute_derived_indicator
        )

    @property
    def data_attribute_personal_identifier_indicator(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_attribute_personal_identifier_indicator
        )

    @data_attribute_personal_identifier_indicator.setter
    def data_attribute_personal_identifier_indicator(
        self, data_attribute_personal_identifier_indicator: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_personal_identifier_indicator = (
            data_attribute_personal_identifier_indicator
        )

    @property
    def data_attribute_direct_identifier_indicator(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_attribute_direct_identifier_indicator
        )

    @data_attribute_direct_identifier_indicator.setter
    def data_attribute_direct_identifier_indicator(
        self, data_attribute_direct_identifier_indicator: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attribute_direct_identifier_indicator = (
            data_attribute_direct_identifier_indicator
        )

    @property
    def mapped_glossary_terms(self) -> Optional[List[AtlasGlossaryTerm]]:
        return (
            None if self.attributes is None else self.attributes.mapped_glossary_terms
        )

    @mapped_glossary_terms.setter
    def mapped_glossary_terms(
        self, mapped_glossary_terms: Optional[List[AtlasGlossaryTerm]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mapped_glossary_terms = mapped_glossary_terms

    @property
    def source_data_attributes(self) -> Optional[List[DataAttribute]]:
        return (
            None if self.attributes is None else self.attributes.source_data_attributes
        )

    @source_data_attributes.setter
    def source_data_attributes(
        self, source_data_attributes: Optional[List[DataAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_data_attributes = source_data_attributes

    @property
    def target_data_attributes(self) -> Optional[List[DataAttribute]]:
        return (
            None if self.attributes is None else self.attributes.target_data_attributes
        )

    @target_data_attributes.setter
    def target_data_attributes(
        self, target_data_attributes: Optional[List[DataAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.target_data_attributes = target_data_attributes

    @property
    def data_entities(self) -> Optional[List[DataEntity]]:
        return None if self.attributes is None else self.attributes.data_entities

    @data_entities.setter
    def data_entities(self, data_entities: Optional[List[DataEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_entities = data_entities

    class Attributes(DataModeling.Attributes):
        data_entity_qualified_name: Optional[str] = Field(default=None, description="")
        data_attribute_id: Optional[str] = Field(default=None, description="")
        data_attribute_fully_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        data_attribute_type: Optional[str] = Field(default=None, description="")
        data_attribute_nullability: Optional[bool] = Field(default=None, description="")
        data_attribute_primary_key_indicator: Optional[bool] = Field(
            default=None, description=""
        )
        data_attribute_foreign_key_indicator: Optional[bool] = Field(
            default=None, description=""
        )
        data_attribute_multiplicity: Optional[str] = Field(default=None, description="")
        data_attribute_derived_indicator: Optional[bool] = Field(
            default=None, description=""
        )
        data_attribute_personal_identifier_indicator: Optional[bool] = Field(
            default=None, description=""
        )
        data_attribute_direct_identifier_indicator: Optional[bool] = Field(
            default=None, description=""
        )
        mapped_glossary_terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship
        source_data_attributes: Optional[List[DataAttribute]] = Field(
            default=None, description=""
        )  # relationship
        target_data_attributes: Optional[List[DataAttribute]] = Field(
            default=None, description=""
        )  # relationship
        data_entities: Optional[List[DataEntity]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DataAttribute.Attributes = Field(
        default_factory=lambda: DataAttribute.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlas_glossary_term import AtlasGlossaryTerm  # noqa
from .data_entity import DataEntity  # noqa
