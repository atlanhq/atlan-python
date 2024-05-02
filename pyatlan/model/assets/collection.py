# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import IconType
from pyatlan.model.fields.atlan_fields import KeywordField

from .namespace import Namespace


class Collection(Namespace):
    """Description"""

    type_name: str = Field(default="Collection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Collection":
            raise ValueError("must be Collection")
        return v

    def __setattr__(self, name, value):
        if name in Collection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ICON: ClassVar[KeywordField] = KeywordField("icon", "icon")
    """
    Image used to represent this collection.
    """
    ICON_TYPE: ClassVar[KeywordField] = KeywordField("iconType", "iconType")
    """
    Type of image used to represent the collection (for example, an emoji).
    """

    _convenience_properties: ClassVar[List[str]] = [
        "icon",
        "icon_type",
    ]

    @property
    def icon(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.icon

    @icon.setter
    def icon(self, icon: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon = icon

    @property
    def icon_type(self) -> Optional[IconType]:
        return None if self.attributes is None else self.attributes.icon_type

    @icon_type.setter
    def icon_type(self, icon_type: Optional[IconType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.icon_type = icon_type

    class Attributes(Namespace.Attributes):
        icon: Optional[str] = Field(default=None, description="")
        icon_type: Optional[IconType] = Field(default=None, description="")

    attributes: Collection.Attributes = Field(
        default_factory=lambda: Collection.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
