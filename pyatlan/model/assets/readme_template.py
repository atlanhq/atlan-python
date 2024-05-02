# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import IconType
from pyatlan.model.fields.atlan_fields import KeywordField

from .resource import Resource


class ReadmeTemplate(Resource):
    """Description"""

    type_name: str = Field(default="ReadmeTemplate", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ReadmeTemplate":
            raise ValueError("must be ReadmeTemplate")
        return v

    def __setattr__(self, name, value):
        if name in ReadmeTemplate._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ICON: ClassVar[KeywordField] = KeywordField("icon", "icon")
    """
    Icon to use for the README template.
    """
    ICON_TYPE: ClassVar[KeywordField] = KeywordField("iconType", "iconType")
    """
    Type of icon, for example: image or emoji.
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

    class Attributes(Resource.Attributes):
        icon: Optional[str] = Field(default=None, description="")
        icon_type: Optional[IconType] = Field(default=None, description="")

    attributes: ReadmeTemplate.Attributes = Field(
        default_factory=lambda: ReadmeTemplate.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
