# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .multi_dimensional_dataset import MultiDimensionalDataset


class Cube(MultiDimensionalDataset):
    """Description"""

    type_name: str = Field(default="Cube", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Cube":
            raise ValueError("must be Cube")
        return v

    def __setattr__(self, name, value):
        if name in Cube._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUBE_DIMENSION_COUNT: ClassVar[NumericField] = NumericField(
        "cubeDimensionCount", "cubeDimensionCount"
    )
    """
    Number of dimensions in the cube.
    """

    CUBE_DIMENSIONS: ClassVar[RelationField] = RelationField("cubeDimensions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cube_dimension_count",
        "cube_dimensions",
    ]

    @property
    def cube_dimension_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.cube_dimension_count

    @cube_dimension_count.setter
    def cube_dimension_count(self, cube_dimension_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_dimension_count = cube_dimension_count

    @property
    def cube_dimensions(self) -> Optional[List[CubeDimension]]:
        return None if self.attributes is None else self.attributes.cube_dimensions

    @cube_dimensions.setter
    def cube_dimensions(self, cube_dimensions: Optional[List[CubeDimension]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_dimensions = cube_dimensions

    class Attributes(MultiDimensionalDataset.Attributes):
        cube_dimension_count: Optional[int] = Field(default=None, description="")
        cube_dimensions: Optional[List[CubeDimension]] = Field(
            default=None, description=""
        )  # relationship

    attributes: Cube.Attributes = Field(
        default_factory=lambda: Cube.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cube_dimension import CubeDimension  # noqa
