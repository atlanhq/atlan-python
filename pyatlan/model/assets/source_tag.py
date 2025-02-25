# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.tag import Tag


class SourceTag(Tag):
    """Description"""

    type_name: str = Field(default="SourceTag", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SourceTag":
            raise ValueError("must be SourceTag")
        return v

    def __setattr__(self, name, value):
        if name in SourceTag._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUSTOM_CONFIGURATION: ClassVar[KeywordField] = KeywordField(
        "customConfiguration", "customConfiguration"
    )
    """
    Specifies custom configuration elements based on the system the tag is being sourced from.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "custom_configuration",
    ]

    @property
    def custom_configuration(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.custom_configuration

    @custom_configuration.setter
    def custom_configuration(self, custom_configuration: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_configuration = custom_configuration

    class Attributes(Tag.Attributes):
        custom_configuration: Optional[str] = Field(default=None, description="")

    attributes: SourceTag.Attributes = Field(
        default_factory=lambda: SourceTag.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


SourceTag.Attributes.update_forward_refs()
