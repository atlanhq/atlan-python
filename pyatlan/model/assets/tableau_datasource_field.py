# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .tableau import Tableau


class TableauDatasourceField(Tableau):
    """Description"""

    type_name: str = Field(default="TableauDatasourceField", allow_mutation=False)

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
    Unique name of the site in which this datasource field exists.
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    Unique name of the project in which this datasource field exists.
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this datasource field exists.
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    Unique name of the workbook in which this datasource field exists.
    """
    DATASOURCE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasourceQualifiedName", "datasourceQualifiedName"
    )
    """
    Unique name of the datasource in which this datasource field exists.
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    List of top-level projects and their nested child projects.
    """
    FULLY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "fullyQualifiedName", "fullyQualifiedName"
    )
    """
    Name used internally in Tableau to uniquely identify this field.
    """
    TABLEAU_DATASOURCE_FIELD_DATA_CATEGORY: ClassVar[KeywordField] = KeywordField(
        "tableauDatasourceFieldDataCategory", "tableauDatasourceFieldDataCategory"
    )
    """
    Data category of this field.
    """
    TABLEAU_DATASOURCE_FIELD_ROLE: ClassVar[KeywordField] = KeywordField(
        "tableauDatasourceFieldRole", "tableauDatasourceFieldRole"
    )
    """
    Role of this field, for example: 'dimension', 'measure', or 'unknown'.
    """
    TABLEAU_DATASOURCE_FIELD_DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "tableauDatasourceFieldDataType",
        "tableauDatasourceFieldDataType",
        "tableauDatasourceFieldDataType.text",
    )
    """
    Data type of this field.
    """
    UPSTREAM_TABLES: ClassVar[KeywordField] = KeywordField(
        "upstreamTables", "upstreamTables"
    )
    """
    Tables upstream to this datasource field.
    """
    TABLEAU_DATASOURCE_FIELD_FORMULA: ClassVar[KeywordField] = KeywordField(
        "tableauDatasourceFieldFormula", "tableauDatasourceFieldFormula"
    )
    """
    Formula for this field.
    """
    TABLEAU_DATASOURCE_FIELD_BIN_SIZE: ClassVar[KeywordField] = KeywordField(
        "tableauDatasourceFieldBinSize", "tableauDatasourceFieldBinSize"
    )
    """
    Bin size of this field.
    """
    UPSTREAM_COLUMNS: ClassVar[KeywordField] = KeywordField(
        "upstreamColumns", "upstreamColumns"
    )
    """
    Columns upstream to this field.
    """
    UPSTREAM_FIELDS: ClassVar[KeywordField] = KeywordField(
        "upstreamFields", "upstreamFields"
    )
    """
    Fields upstream to this field.
    """
    DATASOURCE_FIELD_TYPE: ClassVar[KeywordField] = KeywordField(
        "datasourceFieldType", "datasourceFieldType"
    )
    """
    Type of this datasource field.
    """

    WORKSHEETS: ClassVar[RelationField] = RelationField("worksheets")
    """
    TBC
    """
    DATASOURCE: ClassVar[RelationField] = RelationField("datasource")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[List[Dict[str, str]]]):
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
    def upstream_tables(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_tables

    @upstream_tables.setter
    def upstream_tables(self, upstream_tables: Optional[List[Dict[str, str]]]):
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
    def upstream_columns(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_columns

    @upstream_columns.setter
    def upstream_columns(self, upstream_columns: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_columns = upstream_columns

    @property
    def upstream_fields(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_fields

    @upstream_fields.setter
    def upstream_fields(self, upstream_fields: Optional[List[Dict[str, str]]]):
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
    def worksheets(self) -> Optional[List[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[List[TableauWorksheet]]):
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
        site_qualified_name: Optional[str] = Field(default=None, description="")
        project_qualified_name: Optional[str] = Field(default=None, description="")
        top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        workbook_qualified_name: Optional[str] = Field(default=None, description="")
        datasource_qualified_name: Optional[str] = Field(default=None, description="")
        project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        fully_qualified_name: Optional[str] = Field(default=None, description="")
        tableau_datasource_field_data_category: Optional[str] = Field(
            default=None, description=""
        )
        tableau_datasource_field_role: Optional[str] = Field(
            default=None, description=""
        )
        tableau_datasource_field_data_type: Optional[str] = Field(
            default=None, description=""
        )
        upstream_tables: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        tableau_datasource_field_formula: Optional[str] = Field(
            default=None, description=""
        )
        tableau_datasource_field_bin_size: Optional[str] = Field(
            default=None, description=""
        )
        upstream_columns: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        upstream_fields: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        datasource_field_type: Optional[str] = Field(default=None, description="")
        worksheets: Optional[List[TableauWorksheet]] = Field(
            default=None, description=""
        )  # relationship
        datasource: Optional[TableauDatasource] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauDatasourceField.Attributes = Field(
        default_factory=lambda: TableauDatasourceField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_datasource import TableauDatasource  # noqa
from .tableau_worksheet import TableauWorksheet  # noqa
