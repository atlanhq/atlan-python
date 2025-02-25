# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, overload

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .anaplan import Anaplan


class AnaplanDimension(Anaplan):
    """Description"""

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        model_qualified_name: str,
    ) -> AnaplanDimension: ...

    @overload
    @classmethod
    def creator(
        cls,
        *,
        name: str,
        model_qualified_name: str,
        connection_qualified_name: str,
    ) -> AnaplanDimension: ...

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        model_qualified_name: str,
        connection_qualified_name: Optional[str] = None,
    ) -> AnaplanDimension:
        validate_required_fields(
            ["name", "model_qualified_name"], [name, model_qualified_name]
        )
        attributes = AnaplanDimension.Attributes.create(
            name=name,
            model_qualified_name=model_qualified_name,
            connection_qualified_name=connection_qualified_name,
        )
        return cls(attributes=attributes)

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

        @classmethod
        @init_guid
        def create(
            cls,
            *,
            name: str,
            model_qualified_name: str,
            connection_qualified_name: Optional[str] = None,
        ) -> AnaplanDimension.Attributes:
            validate_required_fields(
                ["name", "model_qualified_name"],
                [name, model_qualified_name],
            )
            if connection_qualified_name:
                connector_name = AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                )
            else:
                connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                    model_qualified_name, "model_qualified_name", 5
                )

            fields = model_qualified_name.split("/")
            workspace_name = fields[3]
            model_name = fields[4]

            return AnaplanDimension.Attributes(
                name=name,
                qualified_name=f"{model_qualified_name}/{name}",
                connection_qualified_name=connection_qualified_name or connection_qn,
                connector_name=connector_name,
                anaplan_workspace_qualified_name=f"{fields[0]}/{fields[1]}/{fields[2]}/{fields[3]}",
                anaplan_workspace_name=workspace_name,
                anaplan_model_qualified_name=model_qualified_name,
                anaplan_model_name=model_name,
                anaplan_model=AnaplanModel.ref_by_qualified_name(model_qualified_name),
            )

    attributes: AnaplanDimension.Attributes = Field(
        default_factory=lambda: AnaplanDimension.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .anaplan_line_item import AnaplanLineItem  # noqa: E402, F401
from .anaplan_model import AnaplanModel  # noqa: E402, F401
from .anaplan_view import AnaplanView  # noqa: E402, F401

AnaplanDimension.Attributes.update_forward_refs()
