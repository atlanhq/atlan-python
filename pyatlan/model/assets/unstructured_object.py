# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .unstructured import Unstructured


class UnstructuredObject(Unstructured):
    """Description"""

    type_name: str = Field(default="UnstructuredObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "UnstructuredObject":
            raise ValueError("must be UnstructuredObject")
        return v

    def __setattr__(self, name, value):
        if name in UnstructuredObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    UNSTRUCTURED_OBJECT_KEY: ClassVar[KeywordField] = KeywordField(
        "unstructuredObjectKey", "unstructuredObjectKey"
    )
    """
    Unique identity of this object within its container — typically the concatenation of any folder path and the object's own filename.
    """  # noqa: E501
    UNSTRUCTURED_OBJECT_SIZE: ClassVar[NumericField] = NumericField(
        "unstructuredObjectSize", "unstructuredObjectSize"
    )
    """
    Object size in bytes.
    """
    UNSTRUCTURED_OBJECT_EXTENSION: ClassVar[KeywordField] = KeywordField(
        "unstructuredObjectExtension", "unstructuredObjectExtension"
    )
    """
    File extension of this object without the leading dot, for example: pdf, docx, csv.
    """
    UNSTRUCTURED_OBJECT_MIME_TYPE: ClassVar[KeywordField] = KeywordField(
        "unstructuredObjectMimeType", "unstructuredObjectMimeType"
    )
    """
    MIME type of this object's content, for example: text/plain, application/json, application/pdf.
    """
    UNSTRUCTURED_OBJECT_CONTENT_LANGUAGE: ClassVar[KeywordField] = KeywordField(
        "unstructuredObjectContentLanguage", "unstructuredObjectContentLanguage"
    )
    """
    Natural (human) language of this object's content, as detected at the source. For example: English, Spanish, French. This is the language the content is written in — not a programming language.
    """  # noqa: E501

    UNSTRUCTURED_CONTAINER: ClassVar[RelationField] = RelationField(
        "unstructuredContainer"
    )
    """
    TBC
    """
    UNSTRUCTURED_PARENT_FOLDER: ClassVar[RelationField] = RelationField(
        "unstructuredParentFolder"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "unstructured_object_key",
        "unstructured_object_size",
        "unstructured_object_extension",
        "unstructured_object_mime_type",
        "unstructured_object_content_language",
        "unstructured_container",
        "unstructured_parent_folder",
    ]

    @property
    def unstructured_object_key(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.unstructured_object_key
        )

    @unstructured_object_key.setter
    def unstructured_object_key(self, unstructured_object_key: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_object_key = unstructured_object_key

    @property
    def unstructured_object_size(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_object_size
        )

    @unstructured_object_size.setter
    def unstructured_object_size(self, unstructured_object_size: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_object_size = unstructured_object_size

    @property
    def unstructured_object_extension(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_object_extension
        )

    @unstructured_object_extension.setter
    def unstructured_object_extension(
        self, unstructured_object_extension: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_object_extension = unstructured_object_extension

    @property
    def unstructured_object_mime_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_object_mime_type
        )

    @unstructured_object_mime_type.setter
    def unstructured_object_mime_type(
        self, unstructured_object_mime_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_object_mime_type = unstructured_object_mime_type

    @property
    def unstructured_object_content_language(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_object_content_language
        )

    @unstructured_object_content_language.setter
    def unstructured_object_content_language(
        self, unstructured_object_content_language: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_object_content_language = (
            unstructured_object_content_language
        )

    @property
    def unstructured_container(self) -> Optional[UnstructuredContainer]:
        return (
            None if self.attributes is None else self.attributes.unstructured_container
        )

    @unstructured_container.setter
    def unstructured_container(
        self, unstructured_container: Optional[UnstructuredContainer]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_container = unstructured_container

    @property
    def unstructured_parent_folder(self) -> Optional[UnstructuredFolder]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_parent_folder
        )

    @unstructured_parent_folder.setter
    def unstructured_parent_folder(
        self, unstructured_parent_folder: Optional[UnstructuredFolder]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_parent_folder = unstructured_parent_folder

    class Attributes(Unstructured.Attributes):
        unstructured_object_key: Optional[str] = Field(default=None, description="")
        unstructured_object_size: Optional[int] = Field(default=None, description="")
        unstructured_object_extension: Optional[str] = Field(
            default=None, description=""
        )
        unstructured_object_mime_type: Optional[str] = Field(
            default=None, description=""
        )
        unstructured_object_content_language: Optional[str] = Field(
            default=None, description=""
        )
        unstructured_container: Optional[UnstructuredContainer] = Field(
            default=None, description=""
        )  # relationship
        unstructured_parent_folder: Optional[UnstructuredFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: UnstructuredObject.Attributes = Field(
        default_factory=lambda: UnstructuredObject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .unstructured_container import UnstructuredContainer  # noqa: E402, F401
from .unstructured_folder import UnstructuredFolder  # noqa: E402, F401

UnstructuredObject.Attributes.update_forward_refs()
