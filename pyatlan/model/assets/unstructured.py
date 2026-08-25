# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.catalog import Catalog


class Unstructured(Catalog):
    """Description"""

    type_name: str = Field(default="Unstructured", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Unstructured":
            raise ValueError("must be Unstructured")
        return v

    def __setattr__(self, name, value):
        if name in Unstructured._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    UNSTRUCTURED_CONTAINER_NAME: ClassVar[KeywordField] = KeywordField(
        "unstructuredContainerName", "unstructuredContainerName"
    )
    """
    Simple name of the data container that holds this asset.
    """
    UNSTRUCTURED_CONTAINER_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "unstructuredContainerQualifiedName", "unstructuredContainerQualifiedName"
    )
    """
    Unique name of the data container that holds this asset.
    """
    UNSTRUCTURED_PARENT_FOLDER_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "unstructuredParentFolderQualifiedName", "unstructuredParentFolderQualifiedName"
    )
    """
    Unique name of the immediate parent folder containing this asset.
    """
    UNSTRUCTURED_FOLDER_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "unstructuredFolderHierarchy", "unstructuredFolderHierarchy"
    )
    """
    Ordered list of ancestor folders for this asset, from immediate parent (index 0) up to the top-level folder under the container (last index). Each entry is a `{qualifiedName, name}` pair.
    """  # noqa: E501

    _convenience_properties: ClassVar[List[str]] = [
        "unstructured_container_name",
        "unstructured_container_qualified_name",
        "unstructured_parent_folder_qualified_name",
        "unstructured_folder_hierarchy",
    ]

    @property
    def unstructured_container_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_container_name
        )

    @unstructured_container_name.setter
    def unstructured_container_name(self, unstructured_container_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_container_name = unstructured_container_name

    @property
    def unstructured_container_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_container_qualified_name
        )

    @unstructured_container_qualified_name.setter
    def unstructured_container_qualified_name(
        self, unstructured_container_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_container_qualified_name = (
            unstructured_container_qualified_name
        )

    @property
    def unstructured_parent_folder_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_parent_folder_qualified_name
        )

    @unstructured_parent_folder_qualified_name.setter
    def unstructured_parent_folder_qualified_name(
        self, unstructured_parent_folder_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_parent_folder_qualified_name = (
            unstructured_parent_folder_qualified_name
        )

    @property
    def unstructured_folder_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.unstructured_folder_hierarchy
        )

    @unstructured_folder_hierarchy.setter
    def unstructured_folder_hierarchy(
        self, unstructured_folder_hierarchy: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.unstructured_folder_hierarchy = unstructured_folder_hierarchy

    class Attributes(Catalog.Attributes):
        unstructured_container_name: Optional[str] = Field(default=None, description="")
        unstructured_container_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        unstructured_parent_folder_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        unstructured_folder_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )

    attributes: Unstructured.Attributes = Field(
        default_factory=lambda: Unstructured.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Unstructured.Attributes.update_forward_refs()
