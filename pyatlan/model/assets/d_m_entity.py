# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
)

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

    D_M_ATTRIBUTE_COUNT: ClassVar[NumericField] = NumericField(
        "dMAttributeCount", "dMAttributeCount"
    )
    """
    Number of attributes in the entity.
    """
    D_M_SUBJECT_AREA: ClassVar[KeywordField] = KeywordField(
        "dMSubjectArea", "dMSubjectArea"
    )
    """
    Subject area of the entity.
    """
    D_M_IS_ROOT: ClassVar[BooleanField] = BooleanField("dMIsRoot", "dMIsRoot")
    """
    Whether this is a root entity or not.
    """
    D_M_ENTITY_TYPE: ClassVar[KeywordField] = KeywordField(
        "dMEntityType", "dMEntityType"
    )
    """
    Type of the data entity.
    """

    D_M_MAPPED_TO_ENTITIES: ClassVar[RelationField] = RelationField(
        "dMMappedToEntities"
    )
    """
    TBC
    """
    D_M_VERSION: ClassVar[RelationField] = RelationField("dMVersion")
    """
    TBC
    """
    D_M_ATTRIBUTES: ClassVar[RelationField] = RelationField("dMAttributes")
    """
    TBC
    """
    D_M_MAPPED_FROM_ENTITIES: ClassVar[RelationField] = RelationField(
        "dMMappedFromEntities"
    )
    """
    TBC
    """
    D_M_RELATED_FROM_ENTITIES: ClassVar[RelationField] = RelationField(
        "dMRelatedFromEntities"
    )
    """
    TBC
    """
    D_M_RELATED_TO_ENTITIES: ClassVar[RelationField] = RelationField(
        "dMRelatedToEntities"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "d_m_attribute_count",
        "d_m_subject_area",
        "d_m_is_root",
        "d_m_entity_type",
        "d_m_mapped_to_entities",
        "d_m_version",
        "d_m_attributes",
        "d_m_mapped_from_entities",
        "d_m_related_from_entities",
        "d_m_related_to_entities",
    ]

    @property
    def d_m_attribute_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.d_m_attribute_count

    @d_m_attribute_count.setter
    def d_m_attribute_count(self, d_m_attribute_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_attribute_count = d_m_attribute_count

    @property
    def d_m_subject_area(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_subject_area

    @d_m_subject_area.setter
    def d_m_subject_area(self, d_m_subject_area: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_subject_area = d_m_subject_area

    @property
    def d_m_is_root(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.d_m_is_root

    @d_m_is_root.setter
    def d_m_is_root(self, d_m_is_root: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_is_root = d_m_is_root

    @property
    def d_m_entity_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_entity_type

    @d_m_entity_type.setter
    def d_m_entity_type(self, d_m_entity_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_entity_type = d_m_entity_type

    @property
    def d_m_mapped_to_entities(self) -> Optional[List[DMEntity]]:
        return (
            None if self.attributes is None else self.attributes.d_m_mapped_to_entities
        )

    @d_m_mapped_to_entities.setter
    def d_m_mapped_to_entities(self, d_m_mapped_to_entities: Optional[List[DMEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_mapped_to_entities = d_m_mapped_to_entities

    @property
    def d_m_version(self) -> Optional[DMVersion]:
        return None if self.attributes is None else self.attributes.d_m_version

    @d_m_version.setter
    def d_m_version(self, d_m_version: Optional[DMVersion]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_version = d_m_version

    @property
    def d_m_attributes(self) -> Optional[List[DMAttribute]]:
        return None if self.attributes is None else self.attributes.d_m_attributes

    @d_m_attributes.setter
    def d_m_attributes(self, d_m_attributes: Optional[List[DMAttribute]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_attributes = d_m_attributes

    @property
    def d_m_mapped_from_entities(self) -> Optional[List[DMEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_mapped_from_entities
        )

    @d_m_mapped_from_entities.setter
    def d_m_mapped_from_entities(
        self, d_m_mapped_from_entities: Optional[List[DMEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_mapped_from_entities = d_m_mapped_from_entities

    @property
    def d_m_related_from_entities(self) -> Optional[List[DMEntityAssociation]]:
        return (
            None
            if self.attributes is None
            else self.attributes.d_m_related_from_entities
        )

    @d_m_related_from_entities.setter
    def d_m_related_from_entities(
        self, d_m_related_from_entities: Optional[List[DMEntityAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_related_from_entities = d_m_related_from_entities

    @property
    def d_m_related_to_entities(self) -> Optional[List[DMEntityAssociation]]:
        return (
            None if self.attributes is None else self.attributes.d_m_related_to_entities
        )

    @d_m_related_to_entities.setter
    def d_m_related_to_entities(
        self, d_m_related_to_entities: Optional[List[DMEntityAssociation]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_related_to_entities = d_m_related_to_entities

    class Attributes(DM.Attributes):
        d_m_attribute_count: Optional[int] = Field(default=None, description="")
        d_m_subject_area: Optional[str] = Field(default=None, description="")
        d_m_is_root: Optional[bool] = Field(default=None, description="")
        d_m_entity_type: Optional[str] = Field(default=None, description="")
        d_m_mapped_to_entities: Optional[List[DMEntity]] = Field(
            default=None, description=""
        )  # relationship
        d_m_version: Optional[DMVersion] = Field(
            default=None, description=""
        )  # relationship
        d_m_attributes: Optional[List[DMAttribute]] = Field(
            default=None, description=""
        )  # relationship
        d_m_mapped_from_entities: Optional[List[DMEntity]] = Field(
            default=None, description=""
        )  # relationship
        d_m_related_from_entities: Optional[List[DMEntityAssociation]] = Field(
            default=None, description=""
        )  # relationship
        d_m_related_to_entities: Optional[List[DMEntityAssociation]] = Field(
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
