# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .unstructured import Unstructured


class UnstructuredContainer(Unstructured):
    """Description"""

    type_name: str = Field(default="UnstructuredContainer", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "UnstructuredContainer":
            raise ValueError("must be UnstructuredContainer")
        return v

    def __setattr__(self, name, value):
        if name in UnstructuredContainer._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    UNSTRUCTURED_OBJECT_COUNT: ClassVar[NumericField] = NumericField(
        "unstructuredObjectCount", "unstructuredObjectCount"
    )
    """
    Total count of objects within this container, including those nested under folders at any depth.
    """
    UNSTRUCTURED_FOLDER_COUNT: ClassVar[NumericField] = NumericField(
        "unstructuredFolderCount", "unstructuredFolderCount"
    )
    """
    Total count of folders within this container, including nested sub-folders at any depth.
    """

    UNSTRUCTURED_FOLDERS: ClassVar[RelationField] = RelationField("unstructuredFolders")
    """
    TBC
    """
    UNSTRUCTURED_OBJECTS: ClassVar[RelationField] = RelationField("unstructuredObjects")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "unstructured_object_count",
        "unstructured_folder_count",
        "unstructured_folders",
        "unstructured_objects",
    ]

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
    def unstructured_folders(self) -> Optional[List[UnstructuredFolder]]:
        return None if self.attributes is None else self.attributes.unstructured_folders

    @unstructured_folders.setter
    def unstructured_folders(
        self, unstructured_folders: Optional[List[UnstructuredFolder]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_folders = unstructured_folders

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

    class Attributes(Unstructured.Attributes):
        unstructured_object_count: Optional[int] = Field(default=None, description="")
        unstructured_folder_count: Optional[int] = Field(default=None, description="")
        unstructured_folders: Optional[List[UnstructuredFolder]] = Field(
            default=None, description=""
        )  # relationship
        unstructured_objects: Optional[List[UnstructuredObject]] = Field(
            default=None, description=""
        )  # relationship

    attributes: UnstructuredContainer.Attributes = Field(
        default_factory=lambda: UnstructuredContainer.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .unstructured_folder import UnstructuredFolder  # noqa: E402, F401
from .unstructured_object import UnstructuredObject  # noqa: E402, F401

UnstructuredContainer.Attributes.update_forward_refs()
