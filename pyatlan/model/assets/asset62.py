# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .asset39 import Tableau


class TableauWorkbook(Tableau):
    """Description"""

    type_name: str = Field("TableauWorkbook", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauWorkbook":
            raise ValueError("must be TableauWorkbook")
        return v

    def __setattr__(self, name, value):
        if name in TableauWorkbook._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    TBC
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectName", "topLevelProjectName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    TBC
    """

    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """
    WORKSHEETS: ClassVar[RelationField] = RelationField("worksheets")
    """
    TBC
    """
    DATASOURCES: ClassVar[RelationField] = RelationField("datasources")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "project",
        "dashboards",
        "worksheets",
        "datasources",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.top_level_project_name
        )

    @top_level_project_name.setter
    def top_level_project_name(self, top_level_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_name = top_level_project_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def dashboards(self) -> Optional[list[TableauDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[TableauDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def worksheets(self) -> Optional[list[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[list[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    @property
    def datasources(self) -> Optional[list[TableauDatasource]]:
        return None if self.attributes is None else self.attributes.datasources

    @datasources.setter
    def datasources(self, datasources: Optional[list[TableauDatasource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasources = datasources

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
        )  # relationship
        dashboards: Optional[list[TableauDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasources: Optional[list[TableauDatasource]] = Field(
            None, description="", alias="datasources"
        )  # relationship

    attributes: "TableauWorkbook.Attributes" = Field(
        default_factory=lambda: TableauWorkbook.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDatasourceField(Tableau):
    """Description"""

    type_name: str = Field("TableauDatasourceField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDatasourceField":
            raise ValueError("must be TableauDatasourceField")
        return v

    def __setattr__(self, name, value):
        if name in TableauDatasourceField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    TBC
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    TBC
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    TBC
    """
    DATASOURCE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasourceQualifiedName", "datasourceQualifiedName"
    )
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    TBC
    """
    FULLY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fullyQualifiedName", "fullyQualifiedName"
    )
    """
    TBC
    """
    TABLEAU_DATASOURCE_FIELD_DATA_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "tableauDatasourceFieldDataCategory", "tableauDatasourceFieldDataCategory"
    )
    """
    TBC
    """
    TABLEAU_DATASOURCE_FIELD_ROLE: ClassVar[KeywordField] = KeywordField(
        "tableauDatasourceFieldRole", "tableauDatasourceFieldRole"
    )
    """
    TBC
    """
    TABLEAU_DATASOURCE_FIELD_DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "tableauDatasourceFieldDataType",
        "tableauDatasourceFieldDataType",
        "tableauDatasourceFieldDataType.text",
    )
    """
    TBC
    """
    UPSTREAM_TABLES: ClassVar[KeywordField] = KeywordField(
        "upstreamTables", "upstreamTables"
    )
    """
    TBC
    """
    TABLEAU_DATASOURCE_FIELD_FORMULA: ClassVar[KeywordField] = KeywordField(
        "tableauDatasourceFieldFormula", "tableauDatasourceFieldFormula"
    )
    """
    TBC
    """
    TABLEAU_DATASOURCE_FIELD_BIN_SIZE: ClassVar[KeywordField] = KeywordField(
        "tableauDatasourceFieldBinSize", "tableauDatasourceFieldBinSize"
    )
    """
    TBC
    """
    UPSTREAM_COLUMNS: ClassVar[KeywordField] = KeywordField(
        "upstreamColumns", "upstreamColumns"
    )
    """
    TBC
    """
    UPSTREAM_FIELDS: ClassVar[KeywordField] = KeywordField(
        "upstreamFields", "upstreamFields"
    )
    """
    TBC
    """
    DATASOURCE_FIELD_TYPE: ClassVar[KeywordField] = KeywordField(
        "datasourceFieldType", "datasourceFieldType"
    )
    """
    TBC
    """

    WORKSHEETS: ClassVar[RelationField] = RelationField("worksheets")
    """
    TBC
    """
    DATASOURCE: ClassVar[RelationField] = RelationField("datasource")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "workbook_qualified_name",
        "datasource_qualified_name",
        "project_hierarchy",
        "fully_qualified_name",
        "tableau_datasource_field_data_category",
        "tableau_datasource_field_role",
        "tableau_datasource_field_data_type",
        "upstream_tables",
        "tableau_datasource_field_formula",
        "tableau_datasource_field_bin_size",
        "upstream_columns",
        "upstream_fields",
        "datasource_field_type",
        "worksheets",
        "datasource",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def datasource_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.datasource_qualified_name
        )

    @datasource_qualified_name.setter
    def datasource_qualified_name(self, datasource_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_qualified_name = datasource_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def fully_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.fully_qualified_name

    @fully_qualified_name.setter
    def fully_qualified_name(self, fully_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fully_qualified_name = fully_qualified_name

    @property
    def tableau_datasource_field_data_category(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_data_category
        )

    @tableau_datasource_field_data_category.setter
    def tableau_datasource_field_data_category(
        self, tableau_datasource_field_data_category: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_data_category = (
            tableau_datasource_field_data_category
        )

    @property
    def tableau_datasource_field_role(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_role
        )

    @tableau_datasource_field_role.setter
    def tableau_datasource_field_role(
        self, tableau_datasource_field_role: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_role = tableau_datasource_field_role

    @property
    def tableau_datasource_field_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_data_type
        )

    @tableau_datasource_field_data_type.setter
    def tableau_datasource_field_data_type(
        self, tableau_datasource_field_data_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_data_type = (
            tableau_datasource_field_data_type
        )

    @property
    def upstream_tables(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_tables

    @upstream_tables.setter
    def upstream_tables(self, upstream_tables: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_tables = upstream_tables

    @property
    def tableau_datasource_field_formula(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_formula
        )

    @tableau_datasource_field_formula.setter
    def tableau_datasource_field_formula(
        self, tableau_datasource_field_formula: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_formula = (
            tableau_datasource_field_formula
        )

    @property
    def tableau_datasource_field_bin_size(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field_bin_size
        )

    @tableau_datasource_field_bin_size.setter
    def tableau_datasource_field_bin_size(
        self, tableau_datasource_field_bin_size: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field_bin_size = (
            tableau_datasource_field_bin_size
        )

    @property
    def upstream_columns(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_columns

    @upstream_columns.setter
    def upstream_columns(self, upstream_columns: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_columns = upstream_columns

    @property
    def upstream_fields(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_fields

    @upstream_fields.setter
    def upstream_fields(self, upstream_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_fields = upstream_fields

    @property
    def datasource_field_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.datasource_field_type
        )

    @datasource_field_type.setter
    def datasource_field_type(self, datasource_field_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_field_type = datasource_field_type

    @property
    def worksheets(self) -> Optional[list[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[list[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    @property
    def datasource(self) -> Optional[TableauDatasource]:
        return None if self.attributes is None else self.attributes.datasource

    @datasource.setter
    def datasource(self, datasource: Optional[TableauDatasource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource = datasource

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        datasource_qualified_name: Optional[str] = Field(
            None, description="", alias="datasourceQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        fully_qualified_name: Optional[str] = Field(
            None, description="", alias="fullyQualifiedName"
        )
        tableau_datasource_field_data_category: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldDataCategory"
        )
        tableau_datasource_field_role: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldRole"
        )
        tableau_datasource_field_data_type: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldDataType"
        )
        upstream_tables: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamTables"
        )
        tableau_datasource_field_formula: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldFormula"
        )
        tableau_datasource_field_bin_size: Optional[str] = Field(
            None, description="", alias="tableauDatasourceFieldBinSize"
        )
        upstream_columns: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamColumns"
        )
        upstream_fields: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamFields"
        )
        datasource_field_type: Optional[str] = Field(
            None, description="", alias="datasourceFieldType"
        )
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasource: Optional[TableauDatasource] = Field(
            None, description="", alias="datasource"
        )  # relationship

    attributes: "TableauDatasourceField.Attributes" = Field(
        default_factory=lambda: TableauDatasourceField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauCalculatedField(Tableau):
    """Description"""

    type_name: str = Field("TableauCalculatedField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauCalculatedField":
            raise ValueError("must be TableauCalculatedField")
        return v

    def __setattr__(self, name, value):
        if name in TableauCalculatedField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    TBC
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    TBC
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    TBC
    """
    DATASOURCE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasourceQualifiedName", "datasourceQualifiedName"
    )
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    TBC
    """
    DATA_CATEGORY: ClassVar[KeywordField] = KeywordField("dataCategory", "dataCategory")
    """
    TBC
    """
    ROLE: ClassVar[KeywordField] = KeywordField("role", "role")
    """
    TBC
    """
    TABLEAU_DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "tableauDataType", "tableauDataType", "tableauDataType.text"
    )
    """
    TBC
    """
    FORMULA: ClassVar[KeywordField] = KeywordField("formula", "formula")
    """
    TBC
    """
    UPSTREAM_FIELDS: ClassVar[KeywordField] = KeywordField(
        "upstreamFields", "upstreamFields"
    )
    """
    TBC
    """

    WORKSHEETS: ClassVar[RelationField] = RelationField("worksheets")
    """
    TBC
    """
    DATASOURCE: ClassVar[RelationField] = RelationField("datasource")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "workbook_qualified_name",
        "datasource_qualified_name",
        "project_hierarchy",
        "data_category",
        "role",
        "tableau_data_type",
        "formula",
        "upstream_fields",
        "worksheets",
        "datasource",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def datasource_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.datasource_qualified_name
        )

    @datasource_qualified_name.setter
    def datasource_qualified_name(self, datasource_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_qualified_name = datasource_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def data_category(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.data_category

    @data_category.setter
    def data_category(self, data_category: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_category = data_category

    @property
    def role(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.role

    @role.setter
    def role(self, role: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.role = role

    @property
    def tableau_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.tableau_data_type

    @tableau_data_type.setter
    def tableau_data_type(self, tableau_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_data_type = tableau_data_type

    @property
    def formula(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.formula

    @formula.setter
    def formula(self, formula: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.formula = formula

    @property
    def upstream_fields(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_fields

    @upstream_fields.setter
    def upstream_fields(self, upstream_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_fields = upstream_fields

    @property
    def worksheets(self) -> Optional[list[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[list[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    @property
    def datasource(self) -> Optional[TableauDatasource]:
        return None if self.attributes is None else self.attributes.datasource

    @datasource.setter
    def datasource(self, datasource: Optional[TableauDatasource]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource = datasource

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        datasource_qualified_name: Optional[str] = Field(
            None, description="", alias="datasourceQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        data_category: Optional[str] = Field(None, description="", alias="dataCategory")
        role: Optional[str] = Field(None, description="", alias="role")
        tableau_data_type: Optional[str] = Field(
            None, description="", alias="tableauDataType"
        )
        formula: Optional[str] = Field(None, description="", alias="formula")
        upstream_fields: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamFields"
        )
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship
        datasource: Optional[TableauDatasource] = Field(
            None, description="", alias="datasource"
        )  # relationship

    attributes: "TableauCalculatedField.Attributes" = Field(
        default_factory=lambda: TableauCalculatedField.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauProject(Tableau):
    """Description"""

    type_name: str = Field("TableauProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauProject":
            raise ValueError("must be TableauProject")
        return v

    def __setattr__(self, name, value):
        if name in TableauProject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    TBC
    """
    IS_TOP_LEVEL_PROJECT: ClassVar[BooleanField] = BooleanField(
        "isTopLevelProject", "isTopLevelProject"
    )
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    TBC
    """

    PARENT_PROJECT: ClassVar[RelationField] = RelationField("parentProject")
    """
    TBC
    """
    WORKBOOKS: ClassVar[RelationField] = RelationField("workbooks")
    """
    TBC
    """
    SITE: ClassVar[RelationField] = RelationField("site")
    """
    TBC
    """
    DATASOURCES: ClassVar[RelationField] = RelationField("datasources")
    """
    TBC
    """
    FLOWS: ClassVar[RelationField] = RelationField("flows")
    """
    TBC
    """
    CHILD_PROJECTS: ClassVar[RelationField] = RelationField("childProjects")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "top_level_project_qualified_name",
        "is_top_level_project",
        "project_hierarchy",
        "parent_project",
        "workbooks",
        "site",
        "datasources",
        "flows",
        "child_projects",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def is_top_level_project(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_top_level_project

    @is_top_level_project.setter
    def is_top_level_project(self, is_top_level_project: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_top_level_project = is_top_level_project

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def parent_project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.parent_project

    @parent_project.setter
    def parent_project(self, parent_project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_project = parent_project

    @property
    def workbooks(self) -> Optional[list[TableauWorkbook]]:
        return None if self.attributes is None else self.attributes.workbooks

    @workbooks.setter
    def workbooks(self, workbooks: Optional[list[TableauWorkbook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbooks = workbooks

    @property
    def site(self) -> Optional[TableauSite]:
        return None if self.attributes is None else self.attributes.site

    @site.setter
    def site(self, site: Optional[TableauSite]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site = site

    @property
    def datasources(self) -> Optional[list[TableauDatasource]]:
        return None if self.attributes is None else self.attributes.datasources

    @datasources.setter
    def datasources(self, datasources: Optional[list[TableauDatasource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasources = datasources

    @property
    def flows(self) -> Optional[list[TableauFlow]]:
        return None if self.attributes is None else self.attributes.flows

    @flows.setter
    def flows(self, flows: Optional[list[TableauFlow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flows = flows

    @property
    def child_projects(self) -> Optional[list[TableauProject]]:
        return None if self.attributes is None else self.attributes.child_projects

    @child_projects.setter
    def child_projects(self, child_projects: Optional[list[TableauProject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.child_projects = child_projects

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        is_top_level_project: Optional[bool] = Field(
            None, description="", alias="isTopLevelProject"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        parent_project: Optional[TableauProject] = Field(
            None, description="", alias="parentProject"
        )  # relationship
        workbooks: Optional[list[TableauWorkbook]] = Field(
            None, description="", alias="workbooks"
        )  # relationship
        site: Optional[TableauSite] = Field(
            None, description="", alias="site"
        )  # relationship
        datasources: Optional[list[TableauDatasource]] = Field(
            None, description="", alias="datasources"
        )  # relationship
        flows: Optional[list[TableauFlow]] = Field(
            None, description="", alias="flows"
        )  # relationship
        child_projects: Optional[list[TableauProject]] = Field(
            None, description="", alias="childProjects"
        )  # relationship

    attributes: "TableauProject.Attributes" = Field(
        default_factory=lambda: TableauProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauSite(Tableau):
    """Description"""

    type_name: str = Field("TableauSite", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauSite":
            raise ValueError("must be TableauSite")
        return v

    def __setattr__(self, name, value):
        if name in TableauSite._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECTS: ClassVar[RelationField] = RelationField("projects")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "projects",
    ]

    @property
    def projects(self) -> Optional[list[TableauProject]]:
        return None if self.attributes is None else self.attributes.projects

    @projects.setter
    def projects(self, projects: Optional[list[TableauProject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.projects = projects

    class Attributes(Tableau.Attributes):
        projects: Optional[list[TableauProject]] = Field(
            None, description="", alias="projects"
        )  # relationship

    attributes: "TableauSite.Attributes" = Field(
        default_factory=lambda: TableauSite.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDatasource(Tableau):
    """Description"""

    type_name: str = Field("TableauDatasource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDatasource":
            raise ValueError("must be TableauDatasource")
        return v

    def __setattr__(self, name, value):
        if name in TableauDatasource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    TBC
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    TBC
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    TBC
    """
    IS_PUBLISHED: ClassVar[BooleanField] = BooleanField("isPublished", "isPublished")
    """
    TBC
    """
    HAS_EXTRACTS: ClassVar[BooleanField] = BooleanField("hasExtracts", "hasExtracts")
    """
    TBC
    """
    IS_CERTIFIED: ClassVar[BooleanField] = BooleanField("isCertified", "isCertified")
    """
    TBC
    """
    CERTIFIER: ClassVar[KeywordField] = KeywordField("certifier", "certifier")
    """
    TBC
    """
    CERTIFICATION_NOTE: ClassVar[KeywordField] = KeywordField(
        "certificationNote", "certificationNote"
    )
    """
    TBC
    """
    CERTIFIER_DISPLAY_NAME: ClassVar[KeywordField] = KeywordField(
        "certifierDisplayName", "certifierDisplayName"
    )
    """
    TBC
    """
    UPSTREAM_TABLES: ClassVar[KeywordField] = KeywordField(
        "upstreamTables", "upstreamTables"
    )
    """
    TBC
    """
    UPSTREAM_DATASOURCES: ClassVar[KeywordField] = KeywordField(
        "upstreamDatasources", "upstreamDatasources"
    )
    """
    TBC
    """

    WORKBOOK: ClassVar[RelationField] = RelationField("workbook")
    """
    TBC
    """
    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "workbook_qualified_name",
        "project_hierarchy",
        "is_published",
        "has_extracts",
        "is_certified",
        "certifier",
        "certification_note",
        "certifier_display_name",
        "upstream_tables",
        "upstream_datasources",
        "workbook",
        "project",
        "fields",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def is_published(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_published

    @is_published.setter
    def is_published(self, is_published: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_published = is_published

    @property
    def has_extracts(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.has_extracts

    @has_extracts.setter
    def has_extracts(self, has_extracts: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.has_extracts = has_extracts

    @property
    def is_certified(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_certified

    @is_certified.setter
    def is_certified(self, is_certified: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_certified = is_certified

    @property
    def certifier(self) -> Optional[dict[str, str]]:
        return None if self.attributes is None else self.attributes.certifier

    @certifier.setter
    def certifier(self, certifier: Optional[dict[str, str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certifier = certifier

    @property
    def certification_note(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.certification_note

    @certification_note.setter
    def certification_note(self, certification_note: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certification_note = certification_note

    @property
    def certifier_display_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.certifier_display_name
        )

    @certifier_display_name.setter
    def certifier_display_name(self, certifier_display_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.certifier_display_name = certifier_display_name

    @property
    def upstream_tables(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_tables

    @upstream_tables.setter
    def upstream_tables(self, upstream_tables: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_tables = upstream_tables

    @property
    def upstream_datasources(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_datasources

    @upstream_datasources.setter
    def upstream_datasources(
        self, upstream_datasources: Optional[list[dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_datasources = upstream_datasources

    @property
    def workbook(self) -> Optional[TableauWorkbook]:
        return None if self.attributes is None else self.attributes.workbook

    @workbook.setter
    def workbook(self, workbook: Optional[TableauWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook = workbook

    @property
    def project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def fields(self) -> Optional[list[TableauDatasourceField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[list[TableauDatasourceField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        is_published: Optional[bool] = Field(None, description="", alias="isPublished")
        has_extracts: Optional[bool] = Field(None, description="", alias="hasExtracts")
        is_certified: Optional[bool] = Field(None, description="", alias="isCertified")
        certifier: Optional[dict[str, str]] = Field(
            None, description="", alias="certifier"
        )
        certification_note: Optional[str] = Field(
            None, description="", alias="certificationNote"
        )
        certifier_display_name: Optional[str] = Field(
            None, description="", alias="certifierDisplayName"
        )
        upstream_tables: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamTables"
        )
        upstream_datasources: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="upstreamDatasources"
        )
        workbook: Optional[TableauWorkbook] = Field(
            None, description="", alias="workbook"
        )  # relationship
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
        )  # relationship
        fields: Optional[list[TableauDatasourceField]] = Field(
            None, description="", alias="fields"
        )  # relationship

    attributes: "TableauDatasource.Attributes" = Field(
        default_factory=lambda: TableauDatasource.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauDashboard(Tableau):
    """Description"""

    type_name: str = Field("TableauDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDashboard":
            raise ValueError("must be TableauDashboard")
        return v

    def __setattr__(self, name, value):
        if name in TableauDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    TBC
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    TBC
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    TBC
    """

    WORKBOOK: ClassVar[RelationField] = RelationField("workbook")
    """
    TBC
    """
    WORKSHEETS: ClassVar[RelationField] = RelationField("worksheets")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "workbook_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "workbook",
        "worksheets",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def workbook(self) -> Optional[TableauWorkbook]:
        return None if self.attributes is None else self.attributes.workbook

    @workbook.setter
    def workbook(self, workbook: Optional[TableauWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook = workbook

    @property
    def worksheets(self) -> Optional[list[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[list[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        workbook: Optional[TableauWorkbook] = Field(
            None, description="", alias="workbook"
        )  # relationship
        worksheets: Optional[list[TableauWorksheet]] = Field(
            None, description="", alias="worksheets"
        )  # relationship

    attributes: "TableauDashboard.Attributes" = Field(
        default_factory=lambda: TableauDashboard.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauFlow(Tableau):
    """Description"""

    type_name: str = Field("TableauFlow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauFlow":
            raise ValueError("must be TableauFlow")
        return v

    def __setattr__(self, name, value):
        if name in TableauFlow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    TBC
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    TBC
    """
    INPUT_FIELDS: ClassVar[KeywordField] = KeywordField("inputFields", "inputFields")
    """
    TBC
    """
    OUTPUT_FIELDS: ClassVar[KeywordField] = KeywordField("outputFields", "outputFields")
    """
    TBC
    """
    OUTPUT_STEPS: ClassVar[KeywordField] = KeywordField("outputSteps", "outputSteps")
    """
    TBC
    """

    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "input_fields",
        "output_fields",
        "output_steps",
        "project",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def input_fields(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.input_fields

    @input_fields.setter
    def input_fields(self, input_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_fields = input_fields

    @property
    def output_fields(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.output_fields

    @output_fields.setter
    def output_fields(self, output_fields: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_fields = output_fields

    @property
    def output_steps(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.output_steps

    @output_steps.setter
    def output_steps(self, output_steps: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_steps = output_steps

    @property
    def project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        input_fields: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="inputFields"
        )
        output_fields: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="outputFields"
        )
        output_steps: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="outputSteps"
        )
        project: Optional[TableauProject] = Field(
            None, description="", alias="project"
        )  # relationship

    attributes: "TableauFlow.Attributes" = Field(
        default_factory=lambda: TableauFlow.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


class TableauWorksheet(Tableau):
    """Description"""

    type_name: str = Field("TableauWorksheet", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauWorksheet":
            raise ValueError("must be TableauWorksheet")
        return v

    def __setattr__(self, name, value):
        if name in TableauWorksheet._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    TBC
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    TBC
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    TBC
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    TBC
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    TBC
    """

    WORKBOOK: ClassVar[RelationField] = RelationField("workbook")
    """
    TBC
    """
    DATASOURCE_FIELDS: ClassVar[RelationField] = RelationField("datasourceFields")
    """
    TBC
    """
    CALCULATED_FIELDS: ClassVar[RelationField] = RelationField("calculatedFields")
    """
    TBC
    """
    DASHBOARDS: ClassVar[RelationField] = RelationField("dashboards")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "workbook_qualified_name",
        "workbook",
        "datasource_fields",
        "calculated_fields",
        "dashboards",
    ]

    @property
    def site_qualified_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.site_qualified_name

    @site_qualified_name.setter
    def site_qualified_name(self, site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site_qualified_name = site_qualified_name

    @property
    def project_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.project_qualified_name
        )

    @project_qualified_name.setter
    def project_qualified_name(self, project_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_qualified_name = project_qualified_name

    @property
    def top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.top_level_project_qualified_name
        )

    @top_level_project_qualified_name.setter
    def top_level_project_qualified_name(
        self, top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.top_level_project_qualified_name = (
            top_level_project_qualified_name
        )

    @property
    def project_hierarchy(self) -> Optional[list[dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[list[dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def workbook_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workbook_qualified_name
        )

    @workbook_qualified_name.setter
    def workbook_qualified_name(self, workbook_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook_qualified_name = workbook_qualified_name

    @property
    def workbook(self) -> Optional[TableauWorkbook]:
        return None if self.attributes is None else self.attributes.workbook

    @workbook.setter
    def workbook(self, workbook: Optional[TableauWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook = workbook

    @property
    def datasource_fields(self) -> Optional[list[TableauDatasourceField]]:
        return None if self.attributes is None else self.attributes.datasource_fields

    @datasource_fields.setter
    def datasource_fields(
        self, datasource_fields: Optional[list[TableauDatasourceField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_fields = datasource_fields

    @property
    def calculated_fields(self) -> Optional[list[TableauCalculatedField]]:
        return None if self.attributes is None else self.attributes.calculated_fields

    @calculated_fields.setter
    def calculated_fields(
        self, calculated_fields: Optional[list[TableauCalculatedField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculated_fields = calculated_fields

    @property
    def dashboards(self) -> Optional[list[TableauDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[list[TableauDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(
            None, description="", alias="siteQualifiedName"
        )
        project_qualified_name: Optional[str] = Field(
            None, description="", alias="projectQualifiedName"
        )
        top_level_project_qualified_name: Optional[str] = Field(
            None, description="", alias="topLevelProjectQualifiedName"
        )
        project_hierarchy: Optional[list[dict[str, str]]] = Field(
            None, description="", alias="projectHierarchy"
        )
        workbook_qualified_name: Optional[str] = Field(
            None, description="", alias="workbookQualifiedName"
        )
        workbook: Optional[TableauWorkbook] = Field(
            None, description="", alias="workbook"
        )  # relationship
        datasource_fields: Optional[list[TableauDatasourceField]] = Field(
            None, description="", alias="datasourceFields"
        )  # relationship
        calculated_fields: Optional[list[TableauCalculatedField]] = Field(
            None, description="", alias="calculatedFields"
        )  # relationship
        dashboards: Optional[list[TableauDashboard]] = Field(
            None, description="", alias="dashboards"
        )  # relationship

    attributes: "TableauWorksheet.Attributes" = Field(
        default_factory=lambda: TableauWorksheet.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


TableauWorkbook.Attributes.update_forward_refs()


TableauDatasourceField.Attributes.update_forward_refs()


TableauCalculatedField.Attributes.update_forward_refs()


TableauProject.Attributes.update_forward_refs()


TableauSite.Attributes.update_forward_refs()


TableauDatasource.Attributes.update_forward_refs()


TableauDashboard.Attributes.update_forward_refs()


TableauFlow.Attributes.update_forward_refs()


TableauWorksheet.Attributes.update_forward_refs()
