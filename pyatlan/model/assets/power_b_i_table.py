# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .power_b_i import PowerBI


class PowerBITable(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBITable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBITable":
            raise ValueError("must be PowerBITable")
        return v

    def __setattr__(self, name, value):
        if name in PowerBITable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this table exists.
    """
    DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasetQualifiedName", "datasetQualifiedName"
    )
    """
    Unique name of the dataset in which this table exists.
    """
    POWER_BI_TABLE_SOURCE_EXPRESSIONS: ClassVar[KeywordField] = KeywordField(
        "powerBITableSourceExpressions", "powerBITableSourceExpressions"
    )
    """
    Power Query M expressions for the table.
    """
    POWER_BI_TABLE_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "powerBITableColumnCount", "powerBITableColumnCount"
    )
    """
    Number of columns in this table.
    """
    POWER_BI_TABLE_MEASURE_COUNT: ClassVar[NumericField] = NumericField(
        "powerBITableMeasureCount", "powerBITableMeasureCount"
    )
    """
    Number of measures in this table.
    """

    COLUMNS: ClassVar[RelationField] = RelationField("columns")
    """
    TBC
    """
    MEASURES: ClassVar[RelationField] = RelationField("measures")
    """
    TBC
    """
    DATASET: ClassVar[RelationField] = RelationField("dataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "power_b_i_table_source_expressions",
        "power_b_i_table_column_count",
        "power_b_i_table_measure_count",
        "columns",
        "measures",
        "dataset",
    ]

    @property
    def workspace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workspace_qualified_name
        )

    @workspace_qualified_name.setter
    def workspace_qualified_name(self, workspace_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace_qualified_name = workspace_qualified_name

    @property
    def dataset_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dataset_qualified_name
        )

    @dataset_qualified_name.setter
    def dataset_qualified_name(self, dataset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_qualified_name = dataset_qualified_name

    @property
    def power_b_i_table_source_expressions(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_source_expressions
        )

    @power_b_i_table_source_expressions.setter
    def power_b_i_table_source_expressions(
        self, power_b_i_table_source_expressions: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_source_expressions = (
            power_b_i_table_source_expressions
        )

    @property
    def power_b_i_table_column_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_column_count
        )

    @power_b_i_table_column_count.setter
    def power_b_i_table_column_count(self, power_b_i_table_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_column_count = power_b_i_table_column_count

    @property
    def power_b_i_table_measure_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_measure_count
        )

    @power_b_i_table_measure_count.setter
    def power_b_i_table_measure_count(
        self, power_b_i_table_measure_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_measure_count = power_b_i_table_measure_count

    @property
    def columns(self) -> Optional[List[PowerBIColumn]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[List[PowerBIColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def measures(self) -> Optional[List[PowerBIMeasure]]:
        return None if self.attributes is None else self.attributes.measures

    @measures.setter
    def measures(self, measures: Optional[List[PowerBIMeasure]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.measures = measures

    @property
    def dataset(self) -> Optional[PowerBIDataset]:
        return None if self.attributes is None else self.attributes.dataset

    @dataset.setter
    def dataset(self, dataset: Optional[PowerBIDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset = dataset

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        dataset_qualified_name: Optional[str] = Field(default=None, description="")
        power_b_i_table_source_expressions: Optional[Set[str]] = Field(
            default=None, description=""
        )
        power_b_i_table_column_count: Optional[int] = Field(
            default=None, description=""
        )
        power_b_i_table_measure_count: Optional[int] = Field(
            default=None, description=""
        )
        columns: Optional[List[PowerBIColumn]] = Field(
            default=None, description=""
        )  # relationship
        measures: Optional[List[PowerBIMeasure]] = Field(
            default=None, description=""
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBITable.Attributes = Field(
        default_factory=lambda: PowerBITable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_column import PowerBIColumn  # noqa
from .power_b_i_dataset import PowerBIDataset  # noqa
from .power_b_i_measure import PowerBIMeasure  # noqa
