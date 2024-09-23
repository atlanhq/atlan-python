# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .d_m import DM


class DMEntity(DM):
    """Description"""

    type_name: str = Field(default="DMEntity", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DMEntity":
            raise ValueError("must be DMEntity")
        return v

    def __setattr__(self, name, value):
        if name in DMEntity._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DM_ATTRIBUTE_COUNT: ClassVar[NumericField] = NumericField(
        "dmAttributeCount", "dmAttributeCount"
    )
    """
    Number of attributes in the entity.
    """
    DM_SUBJECT_AREA: ClassVar[KeywordField] = KeywordField(
        "dmSubjectArea", "dmSubjectArea"
    )
    """
    Subject area of the entity.
    """
    DM_ENTITY_TYPE: ClassVar[KeywordField] = KeywordField(
        "dmEntityType", "dmEntityType"
    )
    """
    Type of the data entity.
    """

    DM_RELATED_TO_ENTITIES: ClassVar[RelationField] = RelationField(
        "dmRelatedToEntities"
    )
    """
    TBC
    """
    DM_ATTRIBUTES: ClassVar[RelationField] = RelationField("dmAttributes")
    """
    TBC
    """
    DM_RELATED_FROM_ENTITIES: ClassVar[RelationField] = RelationField(
        "dmRelatedFromEntities"
    )
    """
    TBC
    """
    DM_VERSIONS: ClassVar[RelationField] = RelationField("dmVersions")
    """
    TBC
    """
    DM_MAPPED_FROM_ENTITIES: ClassVar[RelationField] = RelationField(
        "dmMappedFromEntities"
    )
    """
    TBC
    """
    DM_MAPPED_TO_ENTITIES: ClassVar[RelationField] = RelationField("dmMappedToEntities")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dm_attribute_count",
        "dm_subject_area",
        "dm_entity_type",
        "dm_related_to_entities",
        "dm_attributes",
        "dm_related_from_entities",
        "dm_versions",
        "dm_mapped_from_entities",
        "dm_mapped_to_entities",
    ]

    @property
    def dm_attribute_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dm_attribute_count

    @dm_attribute_count.setter
    def dm_attribute_count(self, dm_attribute_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_attribute_count = dm_attribute_count

    @property
    def dm_subject_area(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_subject_area

    @dm_subject_area.setter
    def dm_subject_area(self, dm_subject_area: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_subject_area = dm_subject_area

    @property
    def dm_entity_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_entity_type

    @dm_entity_type.setter
    def dm_entity_type(self, dm_entity_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_entity_type = dm_entity_type

    @property
    def dm_related_to_entities(self) -> Optional[List[DMEntityAssociation]]:
        return (
            None if self.attributes is None else self.attributes.dm_related_to_entities
        )

    @dm_related_to_entities.setter
    def dm_related_to_entities(
        self, dm_related_to_entities: Optional[List[DMEntityAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_related_to_entities = dm_related_to_entities

    @property
    def dm_attributes(self) -> Optional[List[DMAttribute]]:
        return None if self.attributes is None else self.attributes.dm_attributes

    @dm_attributes.setter
    def dm_attributes(self, dm_attributes: Optional[List[DMAttribute]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_attributes = dm_attributes

    @property
    def dm_related_from_entities(self) -> Optional[List[DMEntityAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_related_from_entities
        )

    @dm_related_from_entities.setter
    def dm_related_from_entities(
        self, dm_related_from_entities: Optional[List[DMEntityAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_related_from_entities = dm_related_from_entities

    @property
    def dm_versions(self) -> Optional[List[DMVersion]]:
        return None if self.attributes is None else self.attributes.dm_versions

    @dm_versions.setter
    def dm_versions(self, dm_versions: Optional[List[DMVersion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_versions = dm_versions

    @property
    def dm_mapped_from_entities(self) -> Optional[List[DMEntity]]:
        return (
            None if self.attributes is None else self.attributes.dm_mapped_from_entities
        )

    @dm_mapped_from_entities.setter
    def dm_mapped_from_entities(
        self, dm_mapped_from_entities: Optional[List[DMEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_mapped_from_entities = dm_mapped_from_entities

    @property
    def dm_mapped_to_entities(self) -> Optional[List[DMEntity]]:
        return (
            None if self.attributes is None else self.attributes.dm_mapped_to_entities
        )

    @dm_mapped_to_entities.setter
    def dm_mapped_to_entities(self, dm_mapped_to_entities: Optional[List[DMEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_mapped_to_entities = dm_mapped_to_entities

    class Attributes(DM.Attributes):
        dm_attribute_count: Optional[int] = Field(default=None, description="")
        dm_subject_area: Optional[str] = Field(default=None, description="")
        dm_entity_type: Optional[str] = Field(default=None, description="")
        dm_related_to_entities: Optional[List[DMEntityAssociation]] = Field(
            default=None, description=""
        )  # relationship
        dm_attributes: Optional[List[DMAttribute]] = Field(
            default=None, description=""
        )  # relationship
        dm_related_from_entities: Optional[List[DMEntityAssociation]] = Field(
            default=None, description=""
        )  # relationship
        dm_versions: Optional[List[DMVersion]] = Field(
            default=None, description=""
        )  # relationship
        dm_mapped_from_entities: Optional[List[DMEntity]] = Field(
            default=None, description=""
        )  # relationship
        dm_mapped_to_entities: Optional[List[DMEntity]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DMEntity.Attributes = Field(
        default_factory=lambda: DMEntity.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .d_m_attribute import DMAttribute  # noqa
from .d_m_entity_association import DMEntityAssociation  # noqa
from .d_m_version import DMVersion  # noqa

DMEntity.Attributes.update_forward_refs()
