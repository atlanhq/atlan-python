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

    D_M_CARDINALITY: ClassVar[KeywordField] = KeywordField(
        "dMCardinality", "dMCardinality"
    )
    """
    Cardinality of the data entity association.
    """
    D_M_LABEL: ClassVar[KeywordField] = KeywordField("dMLabel", "dMLabel")
    """
    Label of the data entity association.
    """

    D_M_ENTITY_FROM: ClassVar[RelationField] = RelationField("dMEntityFrom")
    """
    TBC
    """
    D_M_ENTITY_TO: ClassVar[RelationField] = RelationField("dMEntityTo")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "d_m_cardinality",
        "d_m_label",
        "d_m_entity_from",
        "d_m_entity_to",
    ]

    @property
    def d_m_cardinality(self) -> Optional[DMCardinalityType]:
        return None if self.attributes is None else self.attributes.d_m_cardinality

    @d_m_cardinality.setter
    def d_m_cardinality(self, d_m_cardinality: Optional[DMCardinalityType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_cardinality = d_m_cardinality

    @property
    def d_m_label(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.d_m_label

    @d_m_label.setter
    def d_m_label(self, d_m_label: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_label = d_m_label

    @property
    def d_m_entity_from(self) -> Optional[DMEntity]:
        return None if self.attributes is None else self.attributes.d_m_entity_from

    @d_m_entity_from.setter
    def d_m_entity_from(self, d_m_entity_from: Optional[DMEntity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_entity_from = d_m_entity_from

    @property
    def d_m_entity_to(self) -> Optional[DMEntity]:
        return None if self.attributes is None else self.attributes.d_m_entity_to

    @d_m_entity_to.setter
    def d_m_entity_to(self, d_m_entity_to: Optional[DMEntity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_entity_to = d_m_entity_to

    class Attributes(DM.Attributes):
        d_m_cardinality: Optional[DMCardinalityType] = Field(
            default=None, description=""
        )
        d_m_label: Optional[str] = Field(default=None, description="")
        d_m_entity_from: Optional[DMEntity] = Field(
            default=None, description=""
        )  # relationship
        d_m_entity_to: Optional[DMEntity] = Field(
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
