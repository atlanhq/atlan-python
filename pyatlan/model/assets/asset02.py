# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField

from .asset00 import Asset


class TagAttachment(Asset, type_name="TagAttachment"):
    """Description"""

    type_name: str = Field("TagAttachment", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TagAttachment":
            raise ValueError("must be TagAttachment")
        return v

    def __setattr__(self, name, value):
        if name in TagAttachment._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TAG_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tagQualifiedName", "tagQualifiedName", "tagQualifiedName.text"
    )
    """
    Represents associated source tag's qualified name
    """
    TAG_ATTACHMENT_STRING_VALUE: ClassVar[KeywordTextField] = KeywordTextField(
        "tagAttachmentStringValue",
        "tagAttachmentStringValue",
        "tagAttachmentStringValue.text",
    )
    """
    Represents associated tag value
    """

    _convenience_properties: ClassVar[list[str]] = [
        "tag_qualified_name",
        "tag_attachment_string_value",
    ]

    @property
    def tag_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tag_qualified_name

    @tag_qualified_name.setter
    def tag_qualified_name(self, tag_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_qualified_name = tag_qualified_name

    @property
    def tag_attachment_string_value(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tag_attachment_string_value
        )

    @tag_attachment_string_value.setter
    def tag_attachment_string_value(self, tag_attachment_string_value: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tag_attachment_string_value = tag_attachment_string_value

    class Attributes(Asset.Attributes):
        tag_qualified_name: Optional[str] = Field(
            None, description="", alias="tagQualifiedName"
        )
        tag_attachment_string_value: Optional[str] = Field(
            None, description="", alias="tagAttachmentStringValue"
        )

    attributes: "TagAttachment.Attributes" = Field(
        default_factory=lambda: TagAttachment.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


TagAttachment.Attributes.update_forward_refs()
