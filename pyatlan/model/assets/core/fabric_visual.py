# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .fabric import Fabric


class FabricVisual(Fabric):
    """Description"""

    type_name: str = Field(default="FabricVisual", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FabricVisual":
            raise ValueError("must be FabricVisual")
        return v

    def __setattr__(self, name, value):
        if name in FabricVisual._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_PAGE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricPageQualifiedName", "fabricPageQualifiedName"
    )
    """
    Unique name of the Fabric page that contains this asset.
    """
    FABRIC_PAGE_NAME: ClassVar[KeywordField] = KeywordField(
        "fabricPageName", "fabricPageName"
    )
    """
    Name of the Fabric page that contains this asset.
    """
    FABRIC_VISUAL_TYPE: ClassVar[KeywordField] = KeywordField(
        "fabricVisualType", "fabricVisualType"
    )
    """
    Type of visual.
    """

    FABRIC_PAGE: ClassVar[RelationField] = RelationField("fabricPage")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_page_qualified_name",
        "fabric_page_name",
        "fabric_visual_type",
        "fabric_page",
    ]

    @property
    def fabric_page_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.fabric_page_qualified_name
        )

    @fabric_page_qualified_name.setter
    def fabric_page_qualified_name(self, fabric_page_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_page_qualified_name = fabric_page_qualified_name

    @property
    def fabric_page_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.fabric_page_name

    @fabric_page_name.setter
    def fabric_page_name(self, fabric_page_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_page_name = fabric_page_name

    @property
    def fabric_visual_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.fabric_visual_type

    @fabric_visual_type.setter
    def fabric_visual_type(self, fabric_visual_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_visual_type = fabric_visual_type

    @property
    def fabric_page(self) -> Optional[FabricPage]:
        return None if self.attributes is None else self.attributes.fabric_page

    @fabric_page.setter
    def fabric_page(self, fabric_page: Optional[FabricPage]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_page = fabric_page

    class Attributes(Fabric.Attributes):
        fabric_page_qualified_name: Optional[str] = Field(default=None, description="")
        fabric_page_name: Optional[str] = Field(default=None, description="")
        fabric_visual_type: Optional[str] = Field(default=None, description="")
        fabric_page: Optional[FabricPage] = Field(
            default=None, description=""
        )  # relationship

    attributes: FabricVisual.Attributes = Field(
        default_factory=lambda: FabricVisual.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .fabric_page import FabricPage  # noqa: E402, F401
