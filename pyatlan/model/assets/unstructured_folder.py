# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .unstructured import Unstructured


class UnstructuredFolder(Unstructured):
    """Description"""

    type_name: str = Field(default="UnstructuredFolder", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "UnstructuredFolder":
            raise ValueError("must be UnstructuredFolder")
        return v

    def __setattr__(self, name, value):
        if name in UnstructuredFolder._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    UNSTRUCTURED_FOLDER_COUNT: ClassVar[NumericField] = NumericField(
        "unstructuredFolderCount", "unstructuredFolderCount"
    )
    """
    Count of child folders directly nested under this folder (immediate children only — sub-folders further down the tree are not counted).
    """  # noqa: E501
    UNSTRUCTURED_OBJECT_COUNT: ClassVar[NumericField] = NumericField(
        "unstructuredObjectCount", "unstructuredObjectCount"
    )
    """
    Count of objects directly contained within this folder (immediate children only — objects in sub-folders are not counted).
    """  # noqa: E501

    UNSTRUCTURED_OBJECTS: ClassVar[RelationField] = RelationField("unstructuredObjects")
    """
    TBC
    """
    UNSTRUCTURED_CONTAINER: ClassVar[RelationField] = RelationField(
        "unstructuredContainer"
    )
    """
    TBC
    """
    UNSTRUCTURED_CHILD_FOLDERS: ClassVar[RelationField] = RelationField(
        "unstructuredChildFolders"
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
        "unstructured_folder_count",
        "unstructured_object_count",
        "unstructured_objects",
        "unstructured_container",
        "unstructured_child_folders",
        "unstructured_parent_folder",
    ]

    @property
    def unstructured_folder_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_folder_count
        )

    @unstructured_folder_count.setter
    def unstructured_folder_count(self, unstructured_folder_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_folder_count = unstructured_folder_count

    @property
    def unstructured_object_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_object_count
        )

    @unstructured_object_count.setter
    def unstructured_object_count(self, unstructured_object_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_object_count = unstructured_object_count

    @property
    def unstructured_objects(self) -> Optional[List[UnstructuredObject]]:
        return None if self.attributes is None else self.attributes.unstructured_objects

    @unstructured_objects.setter
    def unstructured_objects(
        self, unstructured_objects: Optional[List[UnstructuredObject]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_objects = unstructured_objects

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
    def unstructured_child_folders(self) -> Optional[List[UnstructuredFolder]]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_child_folders
        )

    @unstructured_child_folders.setter
    def unstructured_child_folders(
        self, unstructured_child_folders: Optional[List[UnstructuredFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_child_folders = unstructured_child_folders

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
        unstructured_folder_count: Optional[int] = Field(default=None, description="")
        unstructured_object_count: Optional[int] = Field(default=None, description="")
        unstructured_objects: Optional[List[UnstructuredObject]] = Field(
            default=None, description=""
        )  # relationship
        unstructured_container: Optional[UnstructuredContainer] = Field(
            default=None, description=""
        )  # relationship
        unstructured_child_folders: Optional[List[UnstructuredFolder]] = Field(
            default=None, description=""
        )  # relationship
        unstructured_parent_folder: Optional[UnstructuredFolder] = Field(
            default=None, description=""
        )  # relationship

    attributes: UnstructuredFolder.Attributes = Field(
        default_factory=lambda: UnstructuredFolder.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .unstructured_container import UnstructuredContainer  # noqa: E402, F401
from .unstructured_object import UnstructuredObject  # noqa: E402, F401

UnstructuredFolder.Attributes.update_forward_refs()
