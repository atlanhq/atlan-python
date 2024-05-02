# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .multi_dimensional_dataset import MultiDimensionalDataset


class CubeDimension(MultiDimensionalDataset):
    """Description"""

    type_name: str = Field(default="CubeDimension", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CubeDimension":
            raise ValueError("must be CubeDimension")
        return v

    def __setattr__(self, name, value):
        if name in CubeDimension._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUBE_HIERARCHY_COUNT: ClassVar[NumericField] = NumericField(
        "cubeHierarchyCount", "cubeHierarchyCount"
    )
    """
    Number of hierarchies in the cube dimension.
    """

    CUBE_HIERARCHIES: ClassVar[RelationField] = RelationField("cubeHierarchies")
    """
    TBC
    """
    CUBE: ClassVar[RelationField] = RelationField("cube")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cube_hierarchy_count",
        "cube_hierarchies",
        "cube",
    ]

    @property
    def cube_hierarchy_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.cube_hierarchy_count

    @cube_hierarchy_count.setter
    def cube_hierarchy_count(self, cube_hierarchy_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_hierarchy_count = cube_hierarchy_count

    @property
    def cube_hierarchies(self) -> Optional[List[CubeHierarchy]]:
        return None if self.attributes is None else self.attributes.cube_hierarchies

    @cube_hierarchies.setter
    def cube_hierarchies(self, cube_hierarchies: Optional[List[CubeHierarchy]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_hierarchies = cube_hierarchies

    @property
    def cube(self) -> Optional[Cube]:
        return None if self.attributes is None else self.attributes.cube

    @cube.setter
    def cube(self, cube: Optional[Cube]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube = cube

    class Attributes(MultiDimensionalDataset.Attributes):
        cube_hierarchy_count: Optional[int] = Field(default=None, description="")
        cube_hierarchies: Optional[List[CubeHierarchy]] = Field(
            default=None, description=""
        )  # relationship
        cube: Optional[Cube] = Field(default=None, description="")  # relationship

    attributes: CubeDimension.Attributes = Field(
        default_factory=lambda: CubeDimension.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cube import Cube  # noqa
from .cube_hierarchy import CubeHierarchy  # noqa
