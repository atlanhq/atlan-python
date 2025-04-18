# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .model import Model


class ModelEntity(Model):
    """Description"""

    type_name: str = Field(default="ModelEntity", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModelEntity":
            raise ValueError("must be ModelEntity")
        return v

    def __setattr__(self, name, value):
        if name in ModelEntity._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODEL_ENTITY_ATTRIBUTE_COUNT: ClassVar[NumericField] = NumericField(
        "modelEntityAttributeCount", "modelEntityAttributeCount"
    )
    """
    Number of attributes in the entity.
    """
    MODEL_ENTITY_SUBJECT_AREA: ClassVar[KeywordField] = KeywordField(
        "modelEntitySubjectArea", "modelEntitySubjectArea"
    )
    """
    Subject area of the entity.
    """
    MODEL_ENTITY_GENERALIZATION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "modelEntityGeneralizationName",
        "modelEntityGeneralizationName.keyword",
        "modelEntityGeneralizationName",
    )
    """
    Name of the general entity.
    """
    MODEL_ENTITY_GENERALIZATION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "modelEntityGeneralizationQualifiedName",
        "modelEntityGeneralizationQualifiedName",
    )
    """
    Unique identifier for the general entity.
    """

    MODEL_ENTITY_RELATED_TO_ENTITIES: ClassVar[RelationField] = RelationField(
        "modelEntityRelatedToEntities"
    )
    """
    TBC
    """
    MODEL_ENTITY_GENERALIZATION_ENTITY: ClassVar[RelationField] = RelationField(
        "modelEntityGeneralizationEntity"
    )
    """
    TBC
    """
    MODEL_ENTITY_IMPLEMENTED_BY_ASSETS: ClassVar[RelationField] = RelationField(
        "modelEntityImplementedByAssets"
    )
    """
    TBC
    """
    MODEL_ENTITY_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "modelEntityAttributes"
    )
    """
    TBC
    """
    MODEL_ENTITY_MAPPED_TO_ENTITIES: ClassVar[RelationField] = RelationField(
        "modelEntityMappedToEntities"
    )
    """
    TBC
    """
    MODEL_ENTITY_RELATED_FROM_ENTITIES: ClassVar[RelationField] = RelationField(
        "modelEntityRelatedFromEntities"
    )
    """
    TBC
    """
    MODEL_VERSIONS: ClassVar[RelationField] = RelationField("modelVersions")
    """
    TBC
    """
    MODEL_ENTITY_MAPPED_FROM_ENTITIES: ClassVar[RelationField] = RelationField(
        "modelEntityMappedFromEntities"
    )
    """
    TBC
    """
    MODEL_ENTITY_SPECIALIZATION_ENTITIES: ClassVar[RelationField] = RelationField(
        "modelEntitySpecializationEntities"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "model_entity_attribute_count",
        "model_entity_subject_area",
        "model_entity_generalization_name",
        "model_entity_generalization_qualified_name",
        "model_entity_related_to_entities",
        "model_entity_generalization_entity",
        "model_entity_implemented_by_assets",
        "model_entity_attributes",
        "model_entity_mapped_to_entities",
        "model_entity_related_from_entities",
        "model_versions",
        "model_entity_mapped_from_entities",
        "model_entity_specialization_entities",
    ]

    @property
    def model_entity_attribute_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_attribute_count
        )

    @model_entity_attribute_count.setter
    def model_entity_attribute_count(self, model_entity_attribute_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_attribute_count = model_entity_attribute_count

    @property
    def model_entity_subject_area(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_subject_area
        )

    @model_entity_subject_area.setter
    def model_entity_subject_area(self, model_entity_subject_area: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_subject_area = model_entity_subject_area

    @property
    def model_entity_generalization_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_generalization_name
        )

    @model_entity_generalization_name.setter
    def model_entity_generalization_name(
        self, model_entity_generalization_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_generalization_name = (
            model_entity_generalization_name
        )

    @property
    def model_entity_generalization_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_generalization_qualified_name
        )

    @model_entity_generalization_qualified_name.setter
    def model_entity_generalization_qualified_name(
        self, model_entity_generalization_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_generalization_qualified_name = (
            model_entity_generalization_qualified_name
        )

    @property
    def model_entity_related_to_entities(
        self,
    ) -> Optional[List[ModelEntityAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_related_to_entities
        )

    @model_entity_related_to_entities.setter
    def model_entity_related_to_entities(
        self, model_entity_related_to_entities: Optional[List[ModelEntityAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_related_to_entities = (
            model_entity_related_to_entities
        )

    @property
    def model_entity_generalization_entity(self) -> Optional[ModelEntity]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_generalization_entity
        )

    @model_entity_generalization_entity.setter
    def model_entity_generalization_entity(
        self, model_entity_generalization_entity: Optional[ModelEntity]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_generalization_entity = (
            model_entity_generalization_entity
        )

    @property
    def model_entity_implemented_by_assets(self) -> Optional[List[Catalog]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_implemented_by_assets
        )

    @model_entity_implemented_by_assets.setter
    def model_entity_implemented_by_assets(
        self, model_entity_implemented_by_assets: Optional[List[Catalog]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_implemented_by_assets = (
            model_entity_implemented_by_assets
        )

    @property
    def model_entity_attributes(self) -> Optional[List[ModelAttribute]]:
        return (
            None if self.attributes is None else self.attributes.model_entity_attributes
        )

    @model_entity_attributes.setter
    def model_entity_attributes(
        self, model_entity_attributes: Optional[List[ModelAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_attributes = model_entity_attributes

    @property
    def model_entity_mapped_to_entities(self) -> Optional[List[ModelEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_mapped_to_entities
        )

    @model_entity_mapped_to_entities.setter
    def model_entity_mapped_to_entities(
        self, model_entity_mapped_to_entities: Optional[List[ModelEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_mapped_to_entities = (
            model_entity_mapped_to_entities
        )

    @property
    def model_entity_related_from_entities(
        self,
    ) -> Optional[List[ModelEntityAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_related_from_entities
        )

    @model_entity_related_from_entities.setter
    def model_entity_related_from_entities(
        self, model_entity_related_from_entities: Optional[List[ModelEntityAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_related_from_entities = (
            model_entity_related_from_entities
        )

    @property
    def model_versions(self) -> Optional[List[ModelVersion]]:
        return None if self.attributes is None else self.attributes.model_versions

    @model_versions.setter
    def model_versions(self, model_versions: Optional[List[ModelVersion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_versions = model_versions

    @property
    def model_entity_mapped_from_entities(self) -> Optional[List[ModelEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_mapped_from_entities
        )

    @model_entity_mapped_from_entities.setter
    def model_entity_mapped_from_entities(
        self, model_entity_mapped_from_entities: Optional[List[ModelEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_mapped_from_entities = (
            model_entity_mapped_from_entities
        )

    @property
    def model_entity_specialization_entities(self) -> Optional[List[ModelEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_entity_specialization_entities
        )

    @model_entity_specialization_entities.setter
    def model_entity_specialization_entities(
        self, model_entity_specialization_entities: Optional[List[ModelEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_entity_specialization_entities = (
            model_entity_specialization_entities
        )

    class Attributes(Model.Attributes):
        model_entity_attribute_count: Optional[int] = Field(
            default=None, description=""
        )
        model_entity_subject_area: Optional[str] = Field(default=None, description="")
        model_entity_generalization_name: Optional[str] = Field(
            default=None, description=""
        )
        model_entity_generalization_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        model_entity_related_to_entities: Optional[List[ModelEntityAssociation]] = (
            Field(default=None, description="")
        )  # relationship
        model_entity_generalization_entity: Optional[ModelEntity] = Field(
            default=None, description=""
        )  # relationship
        model_entity_implemented_by_assets: Optional[List[Catalog]] = Field(
            default=None, description=""
        )  # relationship
        model_entity_attributes: Optional[List[ModelAttribute]] = Field(
            default=None, description=""
        )  # relationship
        model_entity_mapped_to_entities: Optional[List[ModelEntity]] = Field(
            default=None, description=""
        )  # relationship
        model_entity_related_from_entities: Optional[List[ModelEntityAssociation]] = (
            Field(default=None, description="")
        )  # relationship
        model_versions: Optional[List[ModelVersion]] = Field(
            default=None, description=""
        )  # relationship
        model_entity_mapped_from_entities: Optional[List[ModelEntity]] = Field(
            default=None, description=""
        )  # relationship
        model_entity_specialization_entities: Optional[List[ModelEntity]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModelEntity.Attributes = Field(
        default_factory=lambda: ModelEntity.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa: E402, F401
from .model_attribute import ModelAttribute  # noqa: E402, F401
from .model_entity_association import ModelEntityAssociation  # noqa: E402, F401
from .model_version import ModelVersion  # noqa: E402, F401
