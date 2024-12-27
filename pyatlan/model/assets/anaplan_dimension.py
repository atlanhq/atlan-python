# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .anaplan import Anaplan


class AnaplanDimension(Anaplan):
    """Description"""

    type_name: str = Field(default="AnaplanDimension", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnaplanDimension":
            raise ValueError("must be AnaplanDimension")
        return v

    def __setattr__(self, name, value):
        if name in AnaplanDimension._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANAPLAN_PAGE_VIEWS: ClassVar[RelationField] = RelationField("anaplanPageViews")
    """
    TBC
    """
    ANAPLAN_COLUMN_VIEWS: ClassVar[RelationField] = RelationField("anaplanColumnViews")
    """
    TBC
    """
    ANAPLAN_LINE_ITEMS: ClassVar[RelationField] = RelationField("anaplanLineItems")
    """
    TBC
    """
    ANAPLAN_MODEL: ClassVar[RelationField] = RelationField("anaplanModel")
    """
    TBC
    """
    ANAPLAN_ROW_VIEWS: ClassVar[RelationField] = RelationField("anaplanRowViews")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anaplan_page_views",
        "anaplan_column_views",
        "anaplan_line_items",
        "anaplan_model",
        "anaplan_row_views",
    ]

    @property
    def anaplan_page_views(self) -> Optional[List[AnaplanView]]:
        return None if self.attributes is None else self.attributes.anaplan_page_views

    @anaplan_page_views.setter
    def anaplan_page_views(self, anaplan_page_views: Optional[List[AnaplanView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_page_views = anaplan_page_views

    @property
    def anaplan_column_views(self) -> Optional[List[AnaplanView]]:
        return None if self.attributes is None else self.attributes.anaplan_column_views

    @anaplan_column_views.setter
    def anaplan_column_views(self, anaplan_column_views: Optional[List[AnaplanView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_column_views = anaplan_column_views

    @property
    def anaplan_line_items(self) -> Optional[List[AnaplanLineItem]]:
        return None if self.attributes is None else self.attributes.anaplan_line_items

    @anaplan_line_items.setter
    def anaplan_line_items(self, anaplan_line_items: Optional[List[AnaplanLineItem]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_line_items = anaplan_line_items

    @property
    def anaplan_model(self) -> Optional[AnaplanModel]:
        return None if self.attributes is None else self.attributes.anaplan_model

    @anaplan_model.setter
    def anaplan_model(self, anaplan_model: Optional[AnaplanModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_model = anaplan_model

    @property
    def anaplan_row_views(self) -> Optional[List[AnaplanView]]:
        return None if self.attributes is None else self.attributes.anaplan_row_views

    @anaplan_row_views.setter
    def anaplan_row_views(self, anaplan_row_views: Optional[List[AnaplanView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_row_views = anaplan_row_views

    class Attributes(Anaplan.Attributes):
        anaplan_page_views: Optional[List[AnaplanView]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_column_views: Optional[List[AnaplanView]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_line_items: Optional[List[AnaplanLineItem]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_model: Optional[AnaplanModel] = Field(
            default=None, description=""
        )  # relationship
        anaplan_row_views: Optional[List[AnaplanView]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AnaplanDimension.Attributes = Field(
        default_factory=lambda: AnaplanDimension.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .anaplan_line_item import AnaplanLineItem  # noqa
from .anaplan_model import AnaplanModel  # noqa
from .anaplan_view import AnaplanView  # noqa

AnaplanDimension.Attributes.update_forward_refs()
