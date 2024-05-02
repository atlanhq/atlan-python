# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .catalog import Catalog


class MultiDimensionalDataset(Catalog):
    """Description"""

    type_name: str = Field(default="MultiDimensionalDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MultiDimensionalDataset":
            raise ValueError("must be MultiDimensionalDataset")
        return v

    def __setattr__(self, name, value):
        if name in MultiDimensionalDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUBE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "cubeName", "cubeName.keyword", "cubeName"
    )
    """
    Simple name of the cube in which this asset exists, or empty if it is itself a cube.
    """
    CUBE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "cubeQualifiedName", "cubeQualifiedName"
    )
    """
    Unique name of the cube in which this asset exists, or empty if it is itself a cube.
    """
    CUBE_DIMENSION_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "cubeDimensionName", "cubeDimensionName.keyword", "cubeDimensionName"
    )
    """
    Simple name of the cube dimension in which this asset exists, or empty if it is itself a dimension.
    """
    CUBE_DIMENSION_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "cubeDimensionQualifiedName", "cubeDimensionQualifiedName"
    )
    """
    Unique name of the cube dimension in which this asset exists, or empty if it is itself a dimension.
    """
    CUBE_HIERARCHY_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "cubeHierarchyName", "cubeHierarchyName.keyword", "cubeHierarchyName"
    )
    """
    Simple name of the dimension hierarchy in which this asset exists, or empty if it is itself a hierarchy.
    """
    CUBE_HIERARCHY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "cubeHierarchyQualifiedName", "cubeHierarchyQualifiedName"
    )
    """
    Unique name of the dimension hierarchy in which this asset exists, or empty if it is itself a hierarchy.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cube_name",
        "cube_qualified_name",
        "cube_dimension_name",
        "cube_dimension_qualified_name",
        "cube_hierarchy_name",
        "cube_hierarchy_qualified_name",
    ]

    @property
    def cube_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cube_name

    @cube_name.setter
    def cube_name(self, cube_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_name = cube_name

    @property
    def cube_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cube_qualified_name

    @cube_qualified_name.setter
    def cube_qualified_name(self, cube_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_qualified_name = cube_qualified_name

    @property
    def cube_dimension_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cube_dimension_name

    @cube_dimension_name.setter
    def cube_dimension_name(self, cube_dimension_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_dimension_name = cube_dimension_name

    @property
    def cube_dimension_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cube_dimension_qualified_name
        )

    @cube_dimension_qualified_name.setter
    def cube_dimension_qualified_name(
        self, cube_dimension_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_dimension_qualified_name = cube_dimension_qualified_name

    @property
    def cube_hierarchy_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.cube_hierarchy_name

    @cube_hierarchy_name.setter
    def cube_hierarchy_name(self, cube_hierarchy_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_hierarchy_name = cube_hierarchy_name

    @property
    def cube_hierarchy_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cube_hierarchy_qualified_name
        )

    @cube_hierarchy_qualified_name.setter
    def cube_hierarchy_qualified_name(
        self, cube_hierarchy_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_hierarchy_qualified_name = cube_hierarchy_qualified_name

    class Attributes(Catalog.Attributes):
        cube_name: Optional[str] = Field(default=None, description="")
        cube_qualified_name: Optional[str] = Field(default=None, description="")
        cube_dimension_name: Optional[str] = Field(default=None, description="")
        cube_dimension_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        cube_hierarchy_name: Optional[str] = Field(default=None, description="")
        cube_hierarchy_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: MultiDimensionalDataset.Attributes = Field(
        default_factory=lambda: MultiDimensionalDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
