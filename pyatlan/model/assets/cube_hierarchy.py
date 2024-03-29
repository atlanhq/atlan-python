# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .multi_dimensional_dataset import MultiDimensionalDataset


class CubeHierarchy(MultiDimensionalDataset):
    """Description"""

    type_name: str = Field(default="CubeHierarchy", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CubeHierarchy":
            raise ValueError("must be CubeHierarchy")
        return v

    def __setattr__(self, name, value):
        if name in CubeHierarchy._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUBE_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "cubeFieldCount", "cubeFieldCount"
    )
    """
    Number of total fields in the cube hierarchy.
    """

    CUBE_FIELDS: ClassVar[RelationField] = RelationField("cubeFields")
    """
    TBC
    """
    CUBE_DIMENSION: ClassVar[RelationField] = RelationField("cubeDimension")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cube_field_count",
        "cube_fields",
        "cube_dimension",
    ]

    @property
    def cube_field_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.cube_field_count

    @cube_field_count.setter
    def cube_field_count(self, cube_field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_field_count = cube_field_count

    @property
    def cube_fields(self) -> Optional[List[CubeField]]:
        return None if self.attributes is None else self.attributes.cube_fields

    @cube_fields.setter
    def cube_fields(self, cube_fields: Optional[List[CubeField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_fields = cube_fields

    @property
    def cube_dimension(self) -> Optional[CubeDimension]:
        return None if self.attributes is None else self.attributes.cube_dimension

    @cube_dimension.setter
    def cube_dimension(self, cube_dimension: Optional[CubeDimension]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_dimension = cube_dimension

    class Attributes(MultiDimensionalDataset.Attributes):
        cube_field_count: Optional[int] = Field(default=None, description="")
        cube_fields: Optional[List[CubeField]] = Field(
            default=None, description=""
        )  # relationship
        cube_dimension: Optional[CubeDimension] = Field(
            default=None, description=""
        )  # relationship

    attributes: CubeHierarchy.Attributes = Field(
        default_factory=lambda: CubeHierarchy.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cube_dimension import CubeDimension  # noqa
from .cube_field import CubeField  # noqa
