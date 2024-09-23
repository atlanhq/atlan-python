# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import DMCardinalityType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .d_m import DM


class DMEntityAssociation(DM):
    """Description"""

    type_name: str = Field(default="DMEntityAssociation", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DMEntityAssociation":
            raise ValueError("must be DMEntityAssociation")
        return v

    def __setattr__(self, name, value):
        if name in DMEntityAssociation._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DM_CARDINALITY: ClassVar[KeywordField] = KeywordField(
        "dmCardinality", "dmCardinality"
    )
    """
    Cardinality of the data entity association.
    """
    DM_LABEL: ClassVar[KeywordField] = KeywordField("dmLabel", "dmLabel")
    """
    Label of the data entity association.
    """
    DM_ENTITY_TO_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dmEntityToQualifiedName", "dmEntityToQualifiedName"
    )
    """
    Unique name of the association to which this entity is related.
    """
    DM_ENTITY_FROM_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dmEntityFromQualifiedName", "dmEntityFromQualifiedName"
    )
    """
    Unique name of the association from this entity is related.
    """

    DM_ENTITY_TO: ClassVar[RelationField] = RelationField("dmEntityTo")
    """
    TBC
    """
    DM_ENTITY_FROM: ClassVar[RelationField] = RelationField("dmEntityFrom")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dm_cardinality",
        "dm_label",
        "dm_entity_to_qualified_name",
        "dm_entity_from_qualified_name",
        "dm_entity_to",
        "dm_entity_from",
    ]

    @property
    def dm_cardinality(self) -> Optional[DMCardinalityType]:
        return None if self.attributes is None else self.attributes.dm_cardinality

    @dm_cardinality.setter
    def dm_cardinality(self, dm_cardinality: Optional[DMCardinalityType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_cardinality = dm_cardinality

    @property
    def dm_label(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dm_label

    @dm_label.setter
    def dm_label(self, dm_label: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_label = dm_label

    @property
    def dm_entity_to_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_entity_to_qualified_name
        )

    @dm_entity_to_qualified_name.setter
    def dm_entity_to_qualified_name(self, dm_entity_to_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_entity_to_qualified_name = dm_entity_to_qualified_name

    @property
    def dm_entity_from_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dm_entity_from_qualified_name
        )

    @dm_entity_from_qualified_name.setter
    def dm_entity_from_qualified_name(
        self, dm_entity_from_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_entity_from_qualified_name = dm_entity_from_qualified_name

    @property
    def dm_entity_to(self) -> Optional[DMEntity]:
        return None if self.attributes is None else self.attributes.dm_entity_to

    @dm_entity_to.setter
    def dm_entity_to(self, dm_entity_to: Optional[DMEntity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_entity_to = dm_entity_to

    @property
    def dm_entity_from(self) -> Optional[DMEntity]:
        return None if self.attributes is None else self.attributes.dm_entity_from

    @dm_entity_from.setter
    def dm_entity_from(self, dm_entity_from: Optional[DMEntity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dm_entity_from = dm_entity_from

    class Attributes(DM.Attributes):
        dm_cardinality: Optional[DMCardinalityType] = Field(
            default=None, description=""
        )
        dm_label: Optional[str] = Field(default=None, description="")
        dm_entity_to_qualified_name: Optional[str] = Field(default=None, description="")
        dm_entity_from_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dm_entity_to: Optional[DMEntity] = Field(
            default=None, description=""
        )  # relationship
        dm_entity_from: Optional[DMEntity] = Field(
            default=None, description=""
        )  # relationship

    attributes: DMEntityAssociation.Attributes = Field(
        default_factory=lambda: DMEntityAssociation.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .d_m_entity import DMEntity  # noqa

DMEntityAssociation.Attributes.update_forward_refs()
