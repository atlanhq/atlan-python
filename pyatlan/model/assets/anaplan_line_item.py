# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .anaplan import Anaplan


class AnaplanLineItem(Anaplan):
    """Description"""

    type_name: str = Field(default="AnaplanLineItem", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnaplanLineItem":
            raise ValueError("must be AnaplanLineItem")
        return v

    def __setattr__(self, name, value):
        if name in AnaplanLineItem._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANAPLAN_LINE_ITEM_FORMULA: ClassVar[KeywordField] = KeywordField(
        "anaplanLineItemFormula", "anaplanLineItemFormula"
    )
    """
    Formula of the AnaplanLineItem from the source system.
    """

    ANAPLAN_MODULE: ClassVar[RelationField] = RelationField("anaplanModule")
    """
    TBC
    """
    ANAPLAN_LISTS: ClassVar[RelationField] = RelationField("anaplanLists")
    """
    TBC
    """
    ANAPLAN_DIMENSIONS: ClassVar[RelationField] = RelationField("anaplanDimensions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anaplan_line_item_formula",
        "anaplan_module",
        "anaplan_lists",
        "anaplan_dimensions",
    ]

    @property
    def anaplan_line_item_formula(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_line_item_formula
        )

    @anaplan_line_item_formula.setter
    def anaplan_line_item_formula(self, anaplan_line_item_formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_line_item_formula = anaplan_line_item_formula

    @property
    def anaplan_module(self) -> Optional[AnaplanModule]:
        return None if self.attributes is None else self.attributes.anaplan_module

    @anaplan_module.setter
    def anaplan_module(self, anaplan_module: Optional[AnaplanModule]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_module = anaplan_module

    @property
    def anaplan_lists(self) -> Optional[List[AnaplanList]]:
        return None if self.attributes is None else self.attributes.anaplan_lists

    @anaplan_lists.setter
    def anaplan_lists(self, anaplan_lists: Optional[List[AnaplanList]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_lists = anaplan_lists

    @property
    def anaplan_dimensions(self) -> Optional[List[AnaplanDimension]]:
        return None if self.attributes is None else self.attributes.anaplan_dimensions

    @anaplan_dimensions.setter
    def anaplan_dimensions(self, anaplan_dimensions: Optional[List[AnaplanDimension]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_dimensions = anaplan_dimensions

    class Attributes(Anaplan.Attributes):
        anaplan_line_item_formula: Optional[str] = Field(default=None, description="")
        anaplan_module: Optional[AnaplanModule] = Field(
            default=None, description=""
        )  # relationship
        anaplan_lists: Optional[List[AnaplanList]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_dimensions: Optional[List[AnaplanDimension]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AnaplanLineItem.Attributes = Field(
        default_factory=lambda: AnaplanLineItem.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .anaplan_dimension import AnaplanDimension  # noqa
from .anaplan_list import AnaplanList  # noqa
from .anaplan_module import AnaplanModule  # noqa

AnaplanLineItem.Attributes.update_forward_refs()
