# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .anaplan import Anaplan


class AnaplanPage(Anaplan):
    """Description"""

    type_name: str = Field(default="AnaplanPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnaplanPage":
            raise ValueError("must be AnaplanPage")
        return v

    def __setattr__(self, name, value):
        if name in AnaplanPage._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ANAPLAN_APP_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "anaplanAppQualifiedName", "anaplanAppQualifiedName"
    )
    """
    Unique name of the AnaplanApp asset that contains this asset.
    """
    ANAPLAN_PAGE_CATEGORY_NAME: ClassVar[KeywordField] = KeywordField(
        "anaplanPageCategoryName", "anaplanPageCategoryName"
    )
    """
    Category Name of the AnaplanPage from the source system.
    """
    ANAPLAN_PAGE_TYPE: ClassVar[KeywordField] = KeywordField(
        "anaplanPageType", "anaplanPageType"
    )
    """
    Type of the AnaplanPage from the source system.
    """

    ANAPLAN_MODELS: ClassVar[RelationField] = RelationField("anaplanModels")
    """
    TBC
    """
    ANAPLAN_APP: ClassVar[RelationField] = RelationField("anaplanApp")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "anaplan_app_qualified_name",
        "anaplan_page_category_name",
        "anaplan_page_type",
        "anaplan_models",
        "anaplan_app",
    ]

    @property
    def anaplan_app_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_app_qualified_name
        )

    @anaplan_app_qualified_name.setter
    def anaplan_app_qualified_name(self, anaplan_app_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_app_qualified_name = anaplan_app_qualified_name

    @property
    def anaplan_page_category_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.anaplan_page_category_name
        )

    @anaplan_page_category_name.setter
    def anaplan_page_category_name(self, anaplan_page_category_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_page_category_name = anaplan_page_category_name

    @property
    def anaplan_page_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.anaplan_page_type

    @anaplan_page_type.setter
    def anaplan_page_type(self, anaplan_page_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_page_type = anaplan_page_type

    @property
    def anaplan_models(self) -> Optional[List[AnaplanModel]]:
        return None if self.attributes is None else self.attributes.anaplan_models

    @anaplan_models.setter
    def anaplan_models(self, anaplan_models: Optional[List[AnaplanModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_models = anaplan_models

    @property
    def anaplan_app(self) -> Optional[AnaplanApp]:
        return None if self.attributes is None else self.attributes.anaplan_app

    @anaplan_app.setter
    def anaplan_app(self, anaplan_app: Optional[AnaplanApp]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.anaplan_app = anaplan_app

    class Attributes(Anaplan.Attributes):
        anaplan_app_qualified_name: Optional[str] = Field(default=None, description="")
        anaplan_page_category_name: Optional[str] = Field(default=None, description="")
        anaplan_page_type: Optional[str] = Field(default=None, description="")
        anaplan_models: Optional[List[AnaplanModel]] = Field(
            default=None, description=""
        )  # relationship
        anaplan_app: Optional[AnaplanApp] = Field(
            default=None, description=""
        )  # relationship

    attributes: AnaplanPage.Attributes = Field(
        default_factory=lambda: AnaplanPage.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .anaplan_app import AnaplanApp  # noqa
from .anaplan_model import AnaplanModel  # noqa

AnaplanPage.Attributes.update_forward_refs()
