# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .asset46 import PowerBI


class PowerBIReport(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIReport", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIReport":
            raise ValueError("must be PowerBIReport")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIReport._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    TBC
    """
    DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasetQualifiedName", "datasetQualifiedName"
    )
    """
    TBC
    """
    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    TBC
    """
    PAGE_COUNT: ClassVar[NumericField] = NumericField("pageCount", "pageCount")
    """
    TBC
    """

    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    TILES: ClassVar[RelationField] = RelationField("tiles")
    """
    TBC
    """
    PAGES: ClassVar[RelationField] = RelationField("pages")
    """
    TBC
    """
    DATASET: ClassVar[RelationField] = RelationField("dataset")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "web_url",
        "page_count",
        "workspace",
        "tiles",
        "pages",
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
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def page_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.page_count

    @page_count.setter
    def page_count(self, page_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.page_count = page_count

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def tiles(self) -> Optional[list[PowerBITile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[PowerBITile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def pages(self) -> Optional[list[PowerBIPage]]:
        return None if self.attributes is None else self.attributes.pages

    @pages.setter
    def pages(self, pages: Optional[list[PowerBIPage]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.pages = pages

    @property
    def dataset(self) -> Optional[PowerBIDataset]:
        return None if self.attributes is None else self.attributes.dataset

    @dataset.setter
    def dataset(self, dataset: Optional[PowerBIDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset = dataset

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        page_count: Optional[int] = Field(None, description="", alias="pageCount")
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        pages: Optional[list[PowerBIPage]] = Field(
            None, description="", alias="pages"
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship

    attributes: "PowerBIReport.Attributes" = Field(
        default_factory=lambda: PowerBIReport.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIMeasure(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIMeasure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIMeasure":
            raise ValueError("must be PowerBIMeasure")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIMeasure._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    TBC
    """
    DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasetQualifiedName", "datasetQualifiedName"
    )
    """
    TBC
    """
    POWER_BI_MEASURE_EXPRESSION: ClassVar[TextField] = TextField(
        "powerBIMeasureExpression", "powerBIMeasureExpression"
    )
    """
    TBC
    """
    POWER_BI_IS_EXTERNAL_MEASURE: ClassVar[BooleanField] = BooleanField(
        "powerBIIsExternalMeasure", "powerBIIsExternalMeasure"
    )
    """
    TBC
    """

    TABLE: ClassVar[RelationField] = RelationField("table")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dataset_qualified_name",
        "power_b_i_measure_expression",
        "power_b_i_is_external_measure",
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
    def power_b_i_measure_expression(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_measure_expression
        )

    @power_b_i_measure_expression.setter
    def power_b_i_measure_expression(self, power_b_i_measure_expression: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_measure_expression = power_b_i_measure_expression

    @property
    def power_b_i_is_external_measure(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_is_external_measure
        )

    @power_b_i_is_external_measure.setter
    def power_b_i_is_external_measure(
        self, power_b_i_is_external_measure: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_is_external_measure = power_b_i_is_external_measure

    @property
    def table(self) -> Optional[PowerBITable]:
        return None if self.attributes is None else self.attributes.table

    @table.setter
    def table(self, table: Optional[PowerBITable]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.table = table

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        power_b_i_measure_expression: Optional[str] = Field(
            None, description="", alias="powerBIMeasureExpression"
        )
        power_b_i_is_external_measure: Optional[bool] = Field(
            None, description="", alias="powerBIIsExternalMeasure"
        )
        table: Optional[PowerBITable] = Field(
            None, description="", alias="table"
        )  # relationship

    attributes: "PowerBIMeasure.Attributes" = Field(
        default_factory=lambda: PowerBIMeasure.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIColumn(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIColumn", allow_mutation=False)

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
    TBC
    """
    DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasetQualifiedName", "datasetQualifiedName"
    )
    """
    TBC
    """
    POWER_BI_COLUMN_DATA_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "powerBIColumnDataCategory", "powerBIColumnDataCategory"
    )
    """
    TBC
    """
    POWER_BI_COLUMN_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "powerBIColumnDataType", "powerBIColumnDataType"
    )
    """
    TBC
    """
    POWER_BI_SORT_BY_COLUMN: ClassVar[KeywordField] = KeywordField(
        "powerBISortByColumn", "powerBISortByColumn"
    )
    """
    TBC
    """
    POWER_BI_COLUMN_SUMMARIZE_BY: ClassVar[KeywordField] = KeywordField(
        "powerBIColumnSummarizeBy", "powerBIColumnSummarizeBy"
    )
    """
    TBC
    """

    TABLE: ClassVar[RelationField] = RelationField("table")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
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
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        power_b_i_column_data_category: Optional[str] = Field(
            None, description="", alias="powerBIColumnDataCategory"
        )
        power_b_i_column_data_type: Optional[str] = Field(
            None, description="", alias="powerBIColumnDataType"
        )
        power_b_i_sort_by_column: Optional[str] = Field(
            None, description="", alias="powerBISortByColumn"
        )
        power_b_i_column_summarize_by: Optional[str] = Field(
            None, description="", alias="powerBIColumnSummarizeBy"
        )
        table: Optional[PowerBITable] = Field(
            None, description="", alias="table"
        )  # relationship

    attributes: "PowerBIColumn.Attributes" = Field(
        default_factory=lambda: PowerBIColumn.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBITable(PowerBI):
    """Description"""

    type_name: str = Field("PowerBITable", allow_mutation=False)

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
    TBC
    """
    DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasetQualifiedName", "datasetQualifiedName"
    )
    """
    TBC
    """
    POWER_BI_TABLE_SOURCE_EXPRESSIONS: ClassVar[KeywordField] = KeywordField(
        "powerBITableSourceExpressions", "powerBITableSourceExpressions"
    )
    """
    TBC
    """
    POWER_BI_TABLE_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "powerBITableColumnCount", "powerBITableColumnCount"
    )
    """
    TBC
    """
    POWER_BI_TABLE_MEASURE_COUNT: ClassVar[NumericField] = NumericField(
        "powerBITableMeasureCount", "powerBITableMeasureCount"
    )
    """
    TBC
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

    _convenience_properties: ClassVar[list[str]] = [
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
    def power_b_i_table_source_expressions(self) -> Optional[set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_source_expressions
        )

    @power_b_i_table_source_expressions.setter
    def power_b_i_table_source_expressions(
        self, power_b_i_table_source_expressions: Optional[set[str]]
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
    def columns(self) -> Optional[list[PowerBIColumn]]:
        return None if self.attributes is None else self.attributes.columns

    @columns.setter
    def columns(self, columns: Optional[list[PowerBIColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.columns = columns

    @property
    def measures(self) -> Optional[list[PowerBIMeasure]]:
        return None if self.attributes is None else self.attributes.measures

    @measures.setter
    def measures(self, measures: Optional[list[PowerBIMeasure]]):
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
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dataset_qualified_name: Optional[str] = Field(
            None, description="", alias="datasetQualifiedName"
        )
        power_b_i_table_source_expressions: Optional[set[str]] = Field(
            None, description="", alias="powerBITableSourceExpressions"
        )
        power_b_i_table_column_count: Optional[int] = Field(
            None, description="", alias="powerBITableColumnCount"
        )
        power_b_i_table_measure_count: Optional[int] = Field(
            None, description="", alias="powerBITableMeasureCount"
        )
        columns: Optional[list[PowerBIColumn]] = Field(
            None, description="", alias="columns"
        )  # relationship
        measures: Optional[list[PowerBIMeasure]] = Field(
            None, description="", alias="measures"
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship

    attributes: "PowerBITable.Attributes" = Field(
        default_factory=lambda: PowerBITable.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBITile(PowerBI):
    """Description"""

    type_name: str = Field("PowerBITile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBITile":
            raise ValueError("must be PowerBITile")
        return v

    def __setattr__(self, name, value):
        if name in PowerBITile._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    TBC
    """
    DASHBOARD_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dashboardQualifiedName", "dashboardQualifiedName"
    )
    """
    TBC
    """

    REPORT: ClassVar[RelationField] = RelationField("report")
    """
    TBC
    """
    DATASET: ClassVar[RelationField] = RelationField("dataset")
    """
    TBC
    """
    DASHBOARD: ClassVar[RelationField] = RelationField("dashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "dashboard_qualified_name",
        "report",
        "dataset",
        "dashboard",
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
    def dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dashboard_qualified_name
        )

    @dashboard_qualified_name.setter
    def dashboard_qualified_name(self, dashboard_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_qualified_name = dashboard_qualified_name

    @property
    def report(self) -> Optional[PowerBIReport]:
        return None if self.attributes is None else self.attributes.report

    @report.setter
    def report(self, report: Optional[PowerBIReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report = report

    @property
    def dataset(self) -> Optional[PowerBIDataset]:
        return None if self.attributes is None else self.attributes.dataset

    @dataset.setter
    def dataset(self, dataset: Optional[PowerBIDataset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset = dataset

    @property
    def dashboard(self) -> Optional[PowerBIDashboard]:
        return None if self.attributes is None else self.attributes.dashboard

    @dashboard.setter
    def dashboard(self, dashboard: Optional[PowerBIDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard = dashboard

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        dashboard_qualified_name: Optional[str] = Field(
            None, description="", alias="dashboardQualifiedName"
        )
        report: Optional[PowerBIReport] = Field(
            None, description="", alias="report"
        )  # relationship
        dataset: Optional[PowerBIDataset] = Field(
            None, description="", alias="dataset"
        )  # relationship
        dashboard: Optional[PowerBIDashboard] = Field(
            None, description="", alias="dashboard"
        )  # relationship

    attributes: "PowerBITile.Attributes" = Field(
        default_factory=lambda: PowerBITile.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDatasource(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIDatasource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDatasource":
            raise ValueError("must be PowerBIDatasource")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDatasource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONNECTION_DETAILS: ClassVar[KeywordField] = KeywordField(
        "connectionDetails", "connectionDetails"
    )
    """
    TBC
    """

    DATASETS: ClassVar[RelationField] = RelationField("datasets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "connection_details",
        "datasets",
    ]

    @property
    def connection_details(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.connection_details

    @connection_details.setter
    def connection_details(self, connection_details: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.connection_details = connection_details

    @property
    def datasets(self) -> Optional[list[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[list[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    class Attributes(PowerBI.Attributes):
        connection_details: Optional[dict[str, str]] = Field(
            None, description="", alias="connectionDetails"
        )
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship

    attributes: "PowerBIDatasource.Attributes" = Field(
        default_factory=lambda: PowerBIDatasource.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIWorkspace(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIWorkspace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIWorkspace":
            raise ValueError("must be PowerBIWorkspace")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIWorkspace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    TBC
    """
    REPORT_COUNT: ClassVar[NumericField] = NumericField("reportCount", "reportCount")
    """
    TBC
    """
    DASHBOARD_COUNT: ClassVar[NumericField] = NumericField(
        "dashboardCount", "dashboardCount"
    )
    """
    TBC
    """
    DATASET_COUNT: ClassVar[NumericField] = NumericField("datasetCount", "datasetCount")
    """
    TBC
    """
    DATAFLOW_COUNT: ClassVar[NumericField] = NumericField(
        "dataflowCount", "dataflowCount"
    )
    """
    TBC
    """

    REPORTS: ClassVar[RelationField] = RelationField("reports")
    """
    TBC
    """
    DATASETS: ClassVar[RelationField] = RelationField("datasets")
    """
    TBC
    """
    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """
    DATAFLOWS: ClassVar[RelationField] = RelationField("dataflows")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "web_url",
        "report_count",
        "dashboard_count",
        "dataset_count",
        "dataflow_count",
        "reports",
        "datasets",
        "dashboards",
        "dataflows",
    ]

    @property
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def report_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.report_count

    @report_count.setter
    def report_count(self, report_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_count = report_count

    @property
    def dashboard_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dashboard_count

    @dashboard_count.setter
    def dashboard_count(self, dashboard_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboard_count = dashboard_count

    @property
    def dataset_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dataset_count

    @dataset_count.setter
    def dataset_count(self, dataset_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataset_count = dataset_count

    @property
    def dataflow_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.dataflow_count

    @dataflow_count.setter
    def dataflow_count(self, dataflow_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflow_count = dataflow_count

    @property
    def reports(self) -> Optional[list[PowerBIReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[list[PowerBIReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def datasets(self) -> Optional[list[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[list[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    @property
    def dashboards(self) -> Optional[list[PowerBIDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[PowerBIDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def dataflows(self) -> Optional[list[PowerBIDataflow]]:
        return None if self.attributes is None else self.attributes.dataflows

    @dataflows.setter
    def dataflows(self, dataflows: Optional[list[PowerBIDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflows = dataflows

    class Attributes(PowerBI.Attributes):
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        report_count: Optional[int] = Field(None, description="", alias="reportCount")
        dashboard_count: Optional[int] = Field(
            None, description="", alias="dashboardCount"
        )
        dataset_count: Optional[int] = Field(None, description="", alias="datasetCount")
        dataflow_count: Optional[int] = Field(
            None, description="", alias="dataflowCount"
        )
        reports: Optional[list[PowerBIReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship
        dashboards: Optional[list[PowerBIDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        dataflows: Optional[list[PowerBIDataflow]] = Field(
            None, description="", alias="dataflows"
        )  # relationship

    attributes: "PowerBIWorkspace.Attributes" = Field(
        default_factory=lambda: PowerBIWorkspace.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDataset(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataset":
            raise ValueError("must be PowerBIDataset")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    TBC
    """
    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    TBC
    """

    REPORTS: ClassVar[RelationField] = RelationField("reports")
    """
    TBC
    """
    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    DATAFLOWS: ClassVar[RelationField] = RelationField("dataflows")
    """
    TBC
    """
    TILES: ClassVar[RelationField] = RelationField("tiles")
    """
    TBC
    """
    TABLES: ClassVar[RelationField] = RelationField("tables")
    """
    TBC
    """
    DATASOURCES: ClassVar[RelationField] = RelationField("datasources")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "reports",
        "workspace",
        "dataflows",
        "tiles",
        "tables",
        "datasources",
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
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def reports(self) -> Optional[list[PowerBIReport]]:
        return None if self.attributes is None else self.attributes.reports

    @reports.setter
    def reports(self, reports: Optional[list[PowerBIReport]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.reports = reports

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def dataflows(self) -> Optional[list[PowerBIDataflow]]:
        return None if self.attributes is None else self.attributes.dataflows

    @dataflows.setter
    def dataflows(self, dataflows: Optional[list[PowerBIDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dataflows = dataflows

    @property
    def tiles(self) -> Optional[list[PowerBITile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[PowerBITile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    @property
    def tables(self) -> Optional[list[PowerBITable]]:
        return None if self.attributes is None else self.attributes.tables

    @tables.setter
    def tables(self, tables: Optional[list[PowerBITable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tables = tables

    @property
    def datasources(self) -> Optional[list[PowerBIDatasource]]:
        return None if self.attributes is None else self.attributes.datasources

    @datasources.setter
    def datasources(self, datasources: Optional[list[PowerBIDatasource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasources = datasources

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        reports: Optional[list[PowerBIReport]] = Field(
            None, description="", alias="reports"
        )  # relationship
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        dataflows: Optional[list[PowerBIDataflow]] = Field(
            None, description="", alias="dataflows"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship
        tables: Optional[list[PowerBITable]] = Field(
            None, description="", alias="tables"
        )  # relationship
        datasources: Optional[list[PowerBIDatasource]] = Field(
            None, description="", alias="datasources"
        )  # relationship

    attributes: "PowerBIDataset.Attributes" = Field(
        default_factory=lambda: PowerBIDataset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDashboard(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDashboard":
            raise ValueError("must be PowerBIDashboard")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    TBC
    """
    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    TBC
    """
    TILE_COUNT: ClassVar[NumericField] = NumericField("tileCount", "tileCount")
    """
    TBC
    """

    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    TILES: ClassVar[RelationField] = RelationField("tiles")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "tile_count",
        "workspace",
        "tiles",
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
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def tile_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.tile_count

    @tile_count.setter
    def tile_count(self, tile_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tile_count = tile_count

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def tiles(self) -> Optional[list[PowerBITile]]:
        return None if self.attributes is None else self.attributes.tiles

    @tiles.setter
    def tiles(self, tiles: Optional[list[PowerBITile]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tiles = tiles

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        tile_count: Optional[int] = Field(None, description="", alias="tileCount")
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        tiles: Optional[list[PowerBITile]] = Field(
            None, description="", alias="tiles"
        )  # relationship

    attributes: "PowerBIDashboard.Attributes" = Field(
        default_factory=lambda: PowerBIDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIDataflow(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIDataflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIDataflow":
            raise ValueError("must be PowerBIDataflow")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIDataflow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    TBC
    """
    WEB_URL: ClassVar[KeywordField] = KeywordField("webUrl", "webUrl")
    """
    TBC
    """

    WORKSPACE: ClassVar[RelationField] = RelationField("workspace")
    """
    TBC
    """
    DATASETS: ClassVar[RelationField] = RelationField("datasets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "web_url",
        "workspace",
        "datasets",
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
    def web_url(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.web_url

    @web_url.setter
    def web_url(self, web_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.web_url = web_url

    @property
    def workspace(self) -> Optional[PowerBIWorkspace]:
        return None if self.attributes is None else self.attributes.workspace

    @workspace.setter
    def workspace(self, workspace: Optional[PowerBIWorkspace]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workspace = workspace

    @property
    def datasets(self) -> Optional[list[PowerBIDataset]]:
        return None if self.attributes is None else self.attributes.datasets

    @datasets.setter
    def datasets(self, datasets: Optional[list[PowerBIDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasets = datasets

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        web_url: Optional[str] = Field(None, description="", alias="webUrl")
        workspace: Optional[PowerBIWorkspace] = Field(
            None, description="", alias="workspace"
        )  # relationship
        datasets: Optional[list[PowerBIDataset]] = Field(
            None, description="", alias="datasets"
        )  # relationship

    attributes: "PowerBIDataflow.Attributes" = Field(
        default_factory=lambda: PowerBIDataflow.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class PowerBIPage(PowerBI):
    """Description"""

    type_name: str = Field("PowerBIPage", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PowerBIPage":
            raise ValueError("must be PowerBIPage")
        return v

    def __setattr__(self, name, value):
        if name in PowerBIPage._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKSPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workspaceQualifiedName", "workspaceQualifiedName"
    )
    """
    TBC
    """
    REPORT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "reportQualifiedName", "reportQualifiedName"
    )
    """
    TBC
    """

    REPORT: ClassVar[RelationField] = RelationField("report")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "workspace_qualified_name",
        "report_qualified_name",
        "report",
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
    def report_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.report_qualified_name
        )

    @report_qualified_name.setter
    def report_qualified_name(self, report_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report_qualified_name = report_qualified_name

    @property
    def report(self) -> Optional[PowerBIReport]:
        return None if self.attributes is None else self.attributes.report

    @report.setter
    def report(self, report: Optional[PowerBIReport]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.report = report

    class Attributes(PowerBI.Attributes):
        workspace_qualified_name: Optional[str] = Field(
            None, description="", alias="workspaceQualifiedName"
        )
        report_qualified_name: Optional[str] = Field(
            None, description="", alias="reportQualifiedName"
        )
        report: Optional[PowerBIReport] = Field(
            None, description="", alias="report"
        )  # relationship

    attributes: "PowerBIPage.Attributes" = Field(
        default_factory=lambda: PowerBIPage.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


PowerBIReport.Attributes.update_forward_refs()


PowerBIMeasure.Attributes.update_forward_refs()


PowerBIColumn.Attributes.update_forward_refs()


PowerBITable.Attributes.update_forward_refs()


PowerBITile.Attributes.update_forward_refs()


PowerBIDatasource.Attributes.update_forward_refs()


PowerBIWorkspace.Attributes.update_forward_refs()


PowerBIDataset.Attributes.update_forward_refs()


PowerBIDashboard.Attributes.update_forward_refs()


PowerBIDataflow.Attributes.update_forward_refs()


PowerBIPage.Attributes.update_forward_refs()
