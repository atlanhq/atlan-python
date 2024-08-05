# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .data_modeling import DataModeling


class DataEntity(DataModeling):
    """Description"""

    type_name: str = Field(default="DataEntity", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataEntity":
            raise ValueError("must be DataEntity")
        return v

    def __setattr__(self, name, value):
        if name in DataEntity._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_ENTITY_SUBJECT_AREA: ClassVar[KeywordField] = KeywordField(
        "dataEntitySubjectArea", "dataEntitySubjectArea"
    )
    """

    """
    DATA_ENTITY_FULLY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dataEntityFullyQualifiedName", "dataEntityFullyQualifiedName"
    )
    """

    """

    DATA_ATTRIBUTES: ClassVar[RelationField] = RelationField("dataAttributes")
    """
    TBC
    """
    TARGET_DATA_ENTITIES: ClassVar[RelationField] = RelationField("targetDataEntities")
    """
    TBC
    """
    TARGET_RELATED_DATA_ENTITIES: ClassVar[RelationField] = RelationField(
        "targetRelatedDataEntities"
    )
    """
    TBC
    """
    SOURCE_RELATED_DATA_ENTITIES: ClassVar[RelationField] = RelationField(
        "sourceRelatedDataEntities"
    )
    """
    TBC
    """
    DATA_MODEL_VERSIONS: ClassVar[RelationField] = RelationField("dataModelVersions")
    """
    TBC
    """
    SOURCE_DATA_ENTITIES: ClassVar[RelationField] = RelationField("sourceDataEntities")
    """
    TBC
    """
    MAPPED_GLOSSARY_TERMS: ClassVar[RelationField] = RelationField(
        "mappedGlossaryTerms"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "data_entity_subject_area",
        "data_entity_fully_qualified_name",
        "data_attributes",
        "target_data_entities",
        "target_related_data_entities",
        "source_related_data_entities",
        "data_model_versions",
        "source_data_entities",
        "mapped_glossary_terms",
    ]

    @property
    def data_entity_subject_area(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_entity_subject_area
        )

    @data_entity_subject_area.setter
    def data_entity_subject_area(self, data_entity_subject_area: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_entity_subject_area = data_entity_subject_area

    @property
    def data_entity_fully_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.data_entity_fully_qualified_name
        )

    @data_entity_fully_qualified_name.setter
    def data_entity_fully_qualified_name(
        self, data_entity_fully_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_entity_fully_qualified_name = (
            data_entity_fully_qualified_name
        )

    @property
    def data_attributes(self) -> Optional[List[DataAttribute]]:
        return None if self.attributes is None else self.attributes.data_attributes

    @data_attributes.setter
    def data_attributes(self, data_attributes: Optional[List[DataAttribute]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_attributes = data_attributes

    @property
    def target_data_entities(self) -> Optional[List[DataEntity]]:
        return None if self.attributes is None else self.attributes.target_data_entities

    @target_data_entities.setter
    def target_data_entities(self, target_data_entities: Optional[List[DataEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.target_data_entities = target_data_entities

    @property
    def target_related_data_entities(self) -> Optional[List[DataEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.target_related_data_entities
        )

    @target_related_data_entities.setter
    def target_related_data_entities(
        self, target_related_data_entities: Optional[List[DataEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.target_related_data_entities = target_related_data_entities

    @property
    def source_related_data_entities(self) -> Optional[List[DataEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_related_data_entities
        )

    @source_related_data_entities.setter
    def source_related_data_entities(
        self, source_related_data_entities: Optional[List[DataEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_related_data_entities = source_related_data_entities

    @property
    def data_model_versions(self) -> Optional[List[DataModelVersion]]:
        return None if self.attributes is None else self.attributes.data_model_versions

    @data_model_versions.setter
    def data_model_versions(
        self, data_model_versions: Optional[List[DataModelVersion]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_model_versions = data_model_versions

    @property
    def source_data_entities(self) -> Optional[List[DataEntity]]:
        return None if self.attributes is None else self.attributes.source_data_entities

    @source_data_entities.setter
    def source_data_entities(self, source_data_entities: Optional[List[DataEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_data_entities = source_data_entities

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

    class Attributes(DataModeling.Attributes):
        data_entity_subject_area: Optional[str] = Field(default=None, description="")
        data_entity_fully_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        data_attributes: Optional[List[DataAttribute]] = Field(
            default=None, description=""
        )  # relationship
        target_data_entities: Optional[List[DataEntity]] = Field(
            default=None, description=""
        )  # relationship
        target_related_data_entities: Optional[List[DataEntity]] = Field(
            default=None, description=""
        )  # relationship
        source_related_data_entities: Optional[List[DataEntity]] = Field(
            default=None, description=""
        )  # relationship
        data_model_versions: Optional[List[DataModelVersion]] = Field(
            default=None, description=""
        )  # relationship
        source_data_entities: Optional[List[DataEntity]] = Field(
            default=None, description=""
        )  # relationship
        mapped_glossary_terms: Optional[List[AtlasGlossaryTerm]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DataEntity.Attributes = Field(
        default_factory=lambda: DataEntity.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlas_glossary_term import AtlasGlossaryTerm  # noqa
from .data_attribute import DataAttribute  # noqa
from .data_model_version import DataModelVersion  # noqa
