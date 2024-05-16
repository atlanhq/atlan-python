# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .asset22 import MultiDimensionalDataset


class Cube(MultiDimensionalDataset):
    """Description"""

    type_name: str = Field("Cube", allow_mutation=False)

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

    _convenience_properties: ClassVar[list[str]] = [
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
    def cube_dimensions(self) -> Optional[list[CubeDimension]]:
        return None if self.attributes is None else self.attributes.cube_dimensions

    @cube_dimensions.setter
    def cube_dimensions(self, cube_dimensions: Optional[list[CubeDimension]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_dimensions = cube_dimensions

    class Attributes(MultiDimensionalDataset.Attributes):
        cube_dimension_count: Optional[int] = Field(
            None, description="", alias="cubeDimensionCount"
        )
        cube_dimensions: Optional[list[CubeDimension]] = Field(
            None, description="", alias="cubeDimensions"
        )  # relationship

    attributes: "Cube.Attributes" = Field(
        default_factory=lambda: Cube.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class CubeHierarchy(MultiDimensionalDataset):
    """Description"""

    type_name: str = Field("CubeHierarchy", allow_mutation=False)

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

    _convenience_properties: ClassVar[list[str]] = [
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
    def cube_fields(self) -> Optional[list[CubeField]]:
        return None if self.attributes is None else self.attributes.cube_fields

    @cube_fields.setter
    def cube_fields(self, cube_fields: Optional[list[CubeField]]):
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
        cube_field_count: Optional[int] = Field(
            None, description="", alias="cubeFieldCount"
        )
        cube_fields: Optional[list[CubeField]] = Field(
            None, description="", alias="cubeFields"
        )  # relationship
        cube_dimension: Optional[CubeDimension] = Field(
            None, description="", alias="cubeDimension"
        )  # relationship

    attributes: "CubeHierarchy.Attributes" = Field(
        default_factory=lambda: CubeHierarchy.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class CubeField(MultiDimensionalDataset):
    """Description"""

    type_name: str = Field("CubeField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CubeField":
            raise ValueError("must be CubeField")
        return v

    def __setattr__(self, name, value):
        if name in CubeField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUBE_PARENT_FIELD_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "cubeParentFieldName", "cubeParentFieldName.keyword", "cubeParentFieldName"
    )
    """
    Name of the parent field in which this field is nested.
    """
    CUBE_PARENT_FIELD_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "cubeParentFieldQualifiedName", "cubeParentFieldQualifiedName"
    )
    """
    Unique name of the parent field in which this field is nested.
    """
    CUBE_FIELD_LEVEL: ClassVar[NumericField] = NumericField(
        "cubeFieldLevel", "cubeFieldLevel"
    )
    """
    Level of the field in the cube hierarchy.
    """
    CUBE_FIELD_MEASURE_EXPRESSION: ClassVar[KeywordTextField] = KeywordTextField(
        "cubeFieldMeasureExpression",
        "cubeFieldMeasureExpression.keyword",
        "cubeFieldMeasureExpression",
    )
    """
    Expression used to calculate this measure.
    """
    CUBE_SUB_FIELD_COUNT: ClassVar[NumericField] = NumericField(
        "cubeSubFieldCount", "cubeSubFieldCount"
    )
    """
    Number of sub-fields that are direct children of this field.
    """

    CUBE_PARENT_FIELD: ClassVar[RelationField] = RelationField("cubeParentField")
    """
    TBC
    """
    CUBE_HIERARCHY: ClassVar[RelationField] = RelationField("cubeHierarchy")
    """
    TBC
    """
    CUBE_NESTED_FIELDS: ClassVar[RelationField] = RelationField("cubeNestedFields")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "cube_parent_field_name",
        "cube_parent_field_qualified_name",
        "cube_field_level",
        "cube_field_measure_expression",
        "cube_sub_field_count",
        "cube_parent_field",
        "cube_hierarchy",
        "cube_nested_fields",
    ]

    @property
    def cube_parent_field_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.cube_parent_field_name
        )

    @cube_parent_field_name.setter
    def cube_parent_field_name(self, cube_parent_field_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_parent_field_name = cube_parent_field_name

    @property
    def cube_parent_field_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cube_parent_field_qualified_name
        )

    @cube_parent_field_qualified_name.setter
    def cube_parent_field_qualified_name(
        self, cube_parent_field_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_parent_field_qualified_name = (
            cube_parent_field_qualified_name
        )

    @property
    def cube_field_level(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.cube_field_level

    @cube_field_level.setter
    def cube_field_level(self, cube_field_level: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_field_level = cube_field_level

    @property
    def cube_field_measure_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.cube_field_measure_expression
        )

    @cube_field_measure_expression.setter
    def cube_field_measure_expression(
        self, cube_field_measure_expression: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_field_measure_expression = cube_field_measure_expression

    @property
    def cube_sub_field_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.cube_sub_field_count

    @cube_sub_field_count.setter
    def cube_sub_field_count(self, cube_sub_field_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_sub_field_count = cube_sub_field_count

    @property
    def cube_parent_field(self) -> Optional[CubeField]:
        return None if self.attributes is None else self.attributes.cube_parent_field

    @cube_parent_field.setter
    def cube_parent_field(self, cube_parent_field: Optional[CubeField]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_parent_field = cube_parent_field

    @property
    def cube_hierarchy(self) -> Optional[CubeHierarchy]:
        return None if self.attributes is None else self.attributes.cube_hierarchy

    @cube_hierarchy.setter
    def cube_hierarchy(self, cube_hierarchy: Optional[CubeHierarchy]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_hierarchy = cube_hierarchy

    @property
    def cube_nested_fields(self) -> Optional[list[CubeField]]:
        return None if self.attributes is None else self.attributes.cube_nested_fields

    @cube_nested_fields.setter
    def cube_nested_fields(self, cube_nested_fields: Optional[list[CubeField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_nested_fields = cube_nested_fields

    class Attributes(MultiDimensionalDataset.Attributes):
        cube_parent_field_name: Optional[str] = Field(
            None, description="", alias="cubeParentFieldName"
        )
        cube_parent_field_qualified_name: Optional[str] = Field(
            None, description="", alias="cubeParentFieldQualifiedName"
        )
        cube_field_level: Optional[int] = Field(
            None, description="", alias="cubeFieldLevel"
        )
        cube_field_measure_expression: Optional[str] = Field(
            None, description="", alias="cubeFieldMeasureExpression"
        )
        cube_sub_field_count: Optional[int] = Field(
            None, description="", alias="cubeSubFieldCount"
        )
        cube_parent_field: Optional[CubeField] = Field(
            None, description="", alias="cubeParentField"
        )  # relationship
        cube_hierarchy: Optional[CubeHierarchy] = Field(
            None, description="", alias="cubeHierarchy"
        )  # relationship
        cube_nested_fields: Optional[list[CubeField]] = Field(
            None, description="", alias="cubeNestedFields"
        )  # relationship

    attributes: "CubeField.Attributes" = Field(
        default_factory=lambda: CubeField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class CubeDimension(MultiDimensionalDataset):
    """Description"""

    type_name: str = Field("CubeDimension", allow_mutation=False)

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

    _convenience_properties: ClassVar[list[str]] = [
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
    def cube_hierarchies(self) -> Optional[list[CubeHierarchy]]:
        return None if self.attributes is None else self.attributes.cube_hierarchies

    @cube_hierarchies.setter
    def cube_hierarchies(self, cube_hierarchies: Optional[list[CubeHierarchy]]):
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
        cube_hierarchy_count: Optional[int] = Field(
            None, description="", alias="cubeHierarchyCount"
        )
        cube_hierarchies: Optional[list[CubeHierarchy]] = Field(
            None, description="", alias="cubeHierarchies"
        )  # relationship
        cube: Optional[Cube] = Field(None, description="", alias="cube")  # relationship

    attributes: "CubeDimension.Attributes" = Field(
        default_factory=lambda: CubeDimension.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Cube.Attributes.update_forward_refs()


CubeHierarchy.Attributes.update_forward_refs()


CubeField.Attributes.update_forward_refs()


CubeDimension.Attributes.update_forward_refs()
