# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .anaplan import Anaplan


class AnaplanView(Anaplan):
    """Description"""

    type_name: str = Field(default="AnaplanView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnaplanView":
            raise ValueError("must be AnaplanView")
        return v

    def __setattr__(self, name, value):
        if name in AnaplanView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANAPLAN_MODULE: ClassVar[RelationField] = RelationField("anaplanModule")
    """
    TBC
    """
    ANAPLAN_PAGE_DIMENSIONS: ClassVar[RelationField] = RelationField(
        "anaplanPageDimensions"
    )
    """
    TBC
    """
    ANAPLAN_ROW_DIMENSIONS: ClassVar[RelationField] = RelationField(
        "anaplanRowDimensions"
    )
    """
    TBC
    """
    ANAPLAN_COLUMN_DIMENSIONS: ClassVar[RelationField] = RelationField(
        "anaplanColumnDimensions"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anaplan_module",
        "anaplan_page_dimensions",
        "anaplan_row_dimensions",
        "anaplan_column_dimensions",
    ]

    @property
    def anaplan_module(self) -> Optional[AnaplanModule]:
        return None if self.attributes is None else self.attributes.anaplan_module

    @anaplan_module.setter
    def anaplan_module(self, anaplan_module: Optional[AnaplanModule]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_module = anaplan_module

    @property
    def anaplan_page_dimensions(self) -> Optional[List[AnaplanDimension]]:
        return (
            None if self.attributes is None else self.attributes.anaplan_page_dimensions
        )

    @anaplan_page_dimensions.setter
    def anaplan_page_dimensions(
        self, anaplan_page_dimensions: Optional[List[AnaplanDimension]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_page_dimensions = anaplan_page_dimensions

    @property
    def anaplan_row_dimensions(self) -> Optional[List[AnaplanDimension]]:
        return (
            None if self.attributes is None else self.attributes.anaplan_row_dimensions
        )

    @anaplan_row_dimensions.setter
    def anaplan_row_dimensions(
        self, anaplan_row_dimensions: Optional[List[AnaplanDimension]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_row_dimensions = anaplan_row_dimensions

    @property
    def anaplan_column_dimensions(self) -> Optional[List[AnaplanDimension]]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_column_dimensions
        )

    @anaplan_column_dimensions.setter
    def anaplan_column_dimensions(
        self, anaplan_column_dimensions: Optional[List[AnaplanDimension]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_column_dimensions = anaplan_column_dimensions

    class Attributes(Anaplan.Attributes):
        anaplan_module: Optional[AnaplanModule] = Field(
            default=None, description=""
        )  # relationship
        anaplan_page_dimensions: Optional[List[AnaplanDimension]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_row_dimensions: Optional[List[AnaplanDimension]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_column_dimensions: Optional[List[AnaplanDimension]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AnaplanView.Attributes = Field(
        default_factory=lambda: AnaplanView.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .anaplan_dimension import AnaplanDimension  # noqa
from .anaplan_module import AnaplanModule  # noqa

AnaplanView.Attributes.update_forward_refs()
