# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .domo import Domo


class DomoDatasetColumn(Domo):
    """Description"""

    type_name: str = Field(default="DomoDatasetColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DomoDatasetColumn":
            raise ValueError("must be DomoDatasetColumn")
        return v

    def __setattr__(self, name, value):
        if name in DomoDatasetColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DOMO_DATASET_COLUMN_TYPE: ClassVar[KeywordField] = KeywordField(
        "domoDatasetColumnType", "domoDatasetColumnType"
    )
    """
    Type of Domo Dataset Column.
    """
    DOMO_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "domoDatasetQualifiedName", "domoDatasetQualifiedName"
    )
    """
    Qualified name of domo dataset of this column.
    """
    DOMO_DATASET_COLUMN_EXPRESSION: ClassVar[KeywordField] = KeywordField(
        "domoDatasetColumnExpression", "domoDatasetColumnExpression"
    )
    """
    Expression used to create this calculated column.
    """
    DOMO_DATASET_COLUMN_IS_CALCULATED: ClassVar[BooleanField] = BooleanField(
        "domoDatasetColumnIsCalculated", "domoDatasetColumnIsCalculated"
    )
    """
    If the column is a calculated column.
    """

    DOMO_DATASET: ClassVar[RelationField] = RelationField("domoDataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "domo_dataset_column_type",
        "domo_dataset_qualified_name",
        "domo_dataset_column_expression",
        "domo_dataset_column_is_calculated",
        "domo_dataset",
    ]

    @property
    def domo_dataset_column_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_dataset_column_type
        )

    @domo_dataset_column_type.setter
    def domo_dataset_column_type(self, domo_dataset_column_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_column_type = domo_dataset_column_type

    @property
    def domo_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_dataset_qualified_name
        )

    @domo_dataset_qualified_name.setter
    def domo_dataset_qualified_name(self, domo_dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_qualified_name = domo_dataset_qualified_name

    @property
    def domo_dataset_column_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_dataset_column_expression
        )

    @domo_dataset_column_expression.setter
    def domo_dataset_column_expression(
        self, domo_dataset_column_expression: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_column_expression = domo_dataset_column_expression

    @property
    def domo_dataset_column_is_calculated(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.domo_dataset_column_is_calculated
        )

    @domo_dataset_column_is_calculated.setter
    def domo_dataset_column_is_calculated(
        self, domo_dataset_column_is_calculated: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset_column_is_calculated = (
            domo_dataset_column_is_calculated
        )

    @property
    def domo_dataset(self) -> Optional[DomoDataset]:
        return None if self.attributes is None else self.attributes.domo_dataset

    @domo_dataset.setter
    def domo_dataset(self, domo_dataset: Optional[DomoDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.domo_dataset = domo_dataset

    class Attributes(Domo.Attributes):
        domo_dataset_column_type: Optional[str] = Field(default=None, description="")
        domo_dataset_qualified_name: Optional[str] = Field(default=None, description="")
        domo_dataset_column_expression: Optional[str] = Field(
            default=None, description=""
        )
        domo_dataset_column_is_calculated: Optional[bool] = Field(
            default=None, description=""
        )
        domo_dataset: Optional[DomoDataset] = Field(
            default=None, description=""
        )  # relationship

    attributes: DomoDatasetColumn.Attributes = Field(
        default_factory=lambda: DomoDatasetColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .domo_dataset import DomoDataset  # noqa: E402, F401

DomoDatasetColumn.Attributes.update_forward_refs()
