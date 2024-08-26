# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .d_m import DM


class DMVersion(DM):
    """Description"""

    type_name: str = Field(default="DMVersion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DMVersion":
            raise ValueError("must be DMVersion")
        return v

    def __setattr__(self, name, value):
        if name in DMVersion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    D_M_ENTITY_COUNT: ClassVar[NumericField] = NumericField(
        "dMEntityCount", "dMEntityCount"
    )
    """
    Number of entities in the version.
    """

    D_M_DATA_MODEL: ClassVar[RelationField] = RelationField("dMDataModel")
    """
    TBC
    """
    D_M_ENTITIES: ClassVar[RelationField] = RelationField("dMEntities")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "d_m_entity_count",
        "d_m_data_model",
        "d_m_entities",
    ]

    @property
    def d_m_entity_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.d_m_entity_count

    @d_m_entity_count.setter
    def d_m_entity_count(self, d_m_entity_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_entity_count = d_m_entity_count

    @property
    def d_m_data_model(self) -> Optional[DMDataModel]:
        return None if self.attributes is None else self.attributes.d_m_data_model

    @d_m_data_model.setter
    def d_m_data_model(self, d_m_data_model: Optional[DMDataModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_data_model = d_m_data_model

    @property
    def d_m_entities(self) -> Optional[List[DMEntity]]:
        return None if self.attributes is None else self.attributes.d_m_entities

    @d_m_entities.setter
    def d_m_entities(self, d_m_entities: Optional[List[DMEntity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.d_m_entities = d_m_entities

    class Attributes(DM.Attributes):
        d_m_entity_count: Optional[int] = Field(default=None, description="")
        d_m_data_model: Optional[DMDataModel] = Field(
            default=None, description=""
        )  # relationship
        d_m_entities: Optional[List[DMEntity]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DMVersion.Attributes = Field(
        default_factory=lambda: DMVersion.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .d_m_data_model import DMDataModel  # noqa
from .d_m_entity import DMEntity  # noqa

DMVersion.Attributes.update_forward_refs()
