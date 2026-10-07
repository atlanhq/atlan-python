# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
)

from .core.asset import Asset


class TagAttachment(Asset, type_name="TagAttachment"):
    """
    Represents Source tag association asset.

    Only tagQualifiedName and tagAttachmentStringValue are Atlas typedef attributes.
    The other attributes are the source tag contract that atlan-publish-app reads
    to attach the tag to the asset; Atlas does not store them.
    """

    type_name: str = Field(default="TagAttachment", allow_mutation=False)

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
    Represents associated source tag's qualified name.
    """
    OBJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "objectQualifiedName", "objectQualifiedName"
    )
    """
    Qualified name of the asset the source tag is attached to. Read by publish-app; not an Atlas typedef attribute.
    """
    OBJECT_TYPE_NAME: ClassVar[KeywordField] = KeywordField(
        "objectTypeName", "objectTypeName"
    )
    """
    Type name of the asset the source tag is attached to. Read by publish-app; not an Atlas typedef attribute.
    """
    SOURCE_TAG_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "sourceTagQualifiedName", "sourceTagQualifiedName"
    )
    """
    Qualified name of the source tag. Read by publish-app; not an Atlas typedef attribute.
    """
    SOURCE_TAG_DISPLAY_NAME: ClassVar[KeywordField] = KeywordField(
        "sourceTagDisplayName", "sourceTagDisplayName"
    )
    """
    Name of the source tag, used as the Atlan tag name. Read by publish-app; not an Atlas typedef attribute.
    """
    SOURCE_TAG_TYPE_NAME: ClassVar[KeywordField] = KeywordField(
        "sourceTagTypeName", "sourceTagTypeName"
    )
    """
    Type name of the source tag, for example GlueTag. Read by publish-app; not an Atlas typedef attribute.
    """
    VALUE_TYPE: ClassVar[KeywordField] = KeywordField("valueType", "valueType")
    """
    Type of the tag value, for example STRING. Read by publish-app; not an Atlas typedef attribute.
    """
    VALUE: ClassVar[KeywordField] = KeywordField("value", "value")
    """
    Value of the source tag on the asset. Read by publish-app; not an Atlas typedef attribute.
    """
    PROPAGATE: ClassVar[BooleanField] = BooleanField("propagate", "propagate")
    """
    Whether the Atlan tag propagates from the asset. Read by publish-app; not an Atlas typedef attribute.
    """
    TAG_ATTACHMENT_STRING_VALUE: ClassVar[KeywordTextField] = KeywordTextField(
        "tagAttachmentStringValue",
        "tagAttachmentStringValue",
        "tagAttachmentStringValue.text",
    )
    """
    Represents associated tag value.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "tag_qualified_name",
        "object_qualified_name",
        "object_type_name",
        "source_tag_qualified_name",
        "source_tag_display_name",
        "source_tag_type_name",
        "value_type",
        "value",
        "propagate",
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
    def object_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.object_qualified_name
        )

    @object_qualified_name.setter
    def object_qualified_name(self, object_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.object_qualified_name = object_qualified_name

    @property
    def object_type_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.object_type_name

    @object_type_name.setter
    def object_type_name(self, object_type_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.object_type_name = object_type_name

    @property
    def source_tag_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.source_tag_qualified_name
        )

    @source_tag_qualified_name.setter
    def source_tag_qualified_name(self, source_tag_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_tag_qualified_name = source_tag_qualified_name

    @property
    def source_tag_display_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.source_tag_display_name
        )

    @source_tag_display_name.setter
    def source_tag_display_name(self, source_tag_display_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_tag_display_name = source_tag_display_name

    @property
    def source_tag_type_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_tag_type_name

    @source_tag_type_name.setter
    def source_tag_type_name(self, source_tag_type_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_tag_type_name = source_tag_type_name

    @property
    def value_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.value_type

    @value_type.setter
    def value_type(self, value_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.value_type = value_type

    @property
    def value(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.value

    @value.setter
    def value(self, value: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.value = value

    @property
    def propagate(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.propagate

    @propagate.setter
    def propagate(self, propagate: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.propagate = propagate

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
        tag_qualified_name: Optional[str] = Field(default=None, description="")
        object_qualified_name: Optional[str] = Field(default=None, description="")
        object_type_name: Optional[str] = Field(default=None, description="")
        source_tag_qualified_name: Optional[str] = Field(default=None, description="")
        source_tag_display_name: Optional[str] = Field(default=None, description="")
        source_tag_type_name: Optional[str] = Field(default=None, description="")
        value_type: Optional[str] = Field(default=None, description="")
        value: Optional[str] = Field(default=None, description="")
        propagate: Optional[bool] = Field(default=None, description="")
        tag_attachment_string_value: Optional[str] = Field(default=None, description="")

    attributes: TagAttachment.Attributes = Field(
        default_factory=lambda: TagAttachment.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


TagAttachment.Attributes.update_forward_refs()
