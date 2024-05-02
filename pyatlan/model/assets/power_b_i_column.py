# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .power_b_i import PowerBI


class PowerBIColumn(PowerBI):
    """Description"""

    type_name: str = Field(default="PowerBIColumn", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIColumn":
            raise ValueError("must be PowerBIColumn")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIColumn._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    Unique name of the workspace in which this column exists.
    """
    DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasetQualifiedName", "datasetQualifiedName"
    )
    """
    Unique name of the dataset in which this column exists.
    """
    POWER_BI_COLUMN_DATA_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "powerBIColumnDataCategory", "powerBIColumnDataCategory"
    )
    """
    Data category that describes the data in this column.
    """
    POWER_BI_COLUMN_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "powerBIColumnDataType", "powerBIColumnDataType"
    )
    """
    Data type of this column.
    """
    POWER_BI_SORT_BY_COLUMN: ClassVar[KeywordField] = KeywordField(
        "powerBISortByColumn", "powerBISortByColumn"
    )
    """
    Name of a column in the same table to use to order this column.
    """
    POWER_BI_COLUMN_SUMMARIZE_BY: ClassVar[KeywordField] = KeywordField(
        "powerBIColumnSummarizeBy", "powerBIColumnSummarizeBy"
    )
    """
    Aggregate function to use for summarizing this column.
    """

    TABLE: ClassVar[RelationField] = RelationField("table")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "power_b_i_column_data_category",
        "power_b_i_column_data_type",
        "power_b_i_sort_by_column",
        "power_b_i_column_summarize_by",
        "table",
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
    def power_b_i_column_data_category(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_column_data_category
        )

    @power_b_i_column_data_category.setter
    def power_b_i_column_data_category(
        self, power_b_i_column_data_category: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_data_category = power_b_i_column_data_category

    @property
    def power_b_i_column_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_column_data_type
        )

    @power_b_i_column_data_type.setter
    def power_b_i_column_data_type(self, power_b_i_column_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_data_type = power_b_i_column_data_type

    @property
    def power_b_i_sort_by_column(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_sort_by_column
        )

    @power_b_i_sort_by_column.setter
    def power_b_i_sort_by_column(self, power_b_i_sort_by_column: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_sort_by_column = power_b_i_sort_by_column

    @property
    def power_b_i_column_summarize_by(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_column_summarize_by
        )

    @power_b_i_column_summarize_by.setter
    def power_b_i_column_summarize_by(
        self, power_b_i_column_summarize_by: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_column_summarize_by = power_b_i_column_summarize_by

    @property
    def table(self) -> Optional[PowerBITable]:
        return None if self.attributes is None else self.attributes.table

    @table.setter
    def table(self, table: Optional[PowerBITable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table = table

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(default=None, description="")
        dataset_qualified_name: Optional[str] = Field(default=None, description="")
        power_b_i_column_data_category: Optional[str] = Field(
            default=None, description=""
        )
        power_b_i_column_data_type: Optional[str] = Field(default=None, description="")
        power_b_i_sort_by_column: Optional[str] = Field(default=None, description="")
        power_b_i_column_summarize_by: Optional[str] = Field(
            default=None, description=""
        )
        table: Optional[PowerBITable] = Field(
            default=None, description=""
        )  # relationship

    attributes: PowerBIColumn.Attributes = Field(
        default_factory=lambda: PowerBIColumn.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .power_b_i_table import PowerBITable  # noqa
