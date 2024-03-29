# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .multi_dimensional_dataset import MultiDimensionalDataset


class CubeField(MultiDimensionalDataset):
    """Description"""

    type_name: str = Field(default="CubeField", allow_mutation=False)

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

    _convenience_properties: ClassVar[List[str]] = [
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
    def cube_nested_fields(self) -> Optional[List[CubeField]]:
        return None if self.attributes is None else self.attributes.cube_nested_fields

    @cube_nested_fields.setter
    def cube_nested_fields(self, cube_nested_fields: Optional[List[CubeField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cube_nested_fields = cube_nested_fields

    class Attributes(MultiDimensionalDataset.Attributes):
        cube_parent_field_name: Optional[str] = Field(default=None, description="")
        cube_parent_field_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        cube_field_level: Optional[int] = Field(default=None, description="")
        cube_field_measure_expression: Optional[str] = Field(
            default=None, description=""
        )
        cube_sub_field_count: Optional[int] = Field(default=None, description="")
        cube_parent_field: Optional[CubeField] = Field(
            default=None, description=""
        )  # relationship
        cube_hierarchy: Optional[CubeHierarchy] = Field(
            default=None, description=""
        )  # relationship
        cube_nested_fields: Optional[List[CubeField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CubeField.Attributes = Field(
        default_factory=lambda: CubeField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cube_hierarchy import CubeHierarchy  # noqa
