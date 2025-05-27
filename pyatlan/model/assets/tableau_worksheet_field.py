# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
    TextField,
)

from .tableau import Tableau


class TableauWorksheetField(Tableau):
    """Description"""

    type_name: str = Field(default="TableauWorksheetField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauWorksheetField":
            raise ValueError("must be TableauWorksheetField")
        return v

    def __setattr__(self, name, value):
        if name in TableauWorksheetField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TABLEAU_SITE_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "tableauSiteQualifiedName", "tableauSiteQualifiedName"
    )
    """
    Unique name of the site in which this worksheet field exists.
    """
    TABLEAU_PROJECT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableauProjectQualifiedName",
        "tableauProjectQualifiedName.keyword",
        "tableauProjectQualifiedName",
    )
    """
    Unique name of the project in which this worksheet field exists.
    """
    TABLEAU_TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "tableauTopLevelProjectQualifiedName", "tableauTopLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this worksheet field exists.
    """
    TABLEAU_WORKBOOK_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "tableauWorkbookQualifiedName", "tableauWorkbookQualifiedName"
    )
    """
    Unique name of the workbook in which this worksheet field exists.
    """
    TABLEAU_WORKSHEET_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "tableauWorksheetQualifiedName", "tableauWorksheetQualifiedName"
    )
    """
    Unique name of the datasource in which this worksheet field exists.
    """
    TABLEAU_PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "tableauProjectHierarchy", "tableauProjectHierarchy"
    )
    """
    List of top-level projects and their nested child projects.
    """
    TABLEAU_FULLY_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "tableauFullyQualifiedName", "tableauFullyQualifiedName"
    )
    """
    Name used internally in Tableau to uniquely identify this field.
    """
    TABLEAU_WORKSHEET_FIELD_DATA_CATEGORY: ClassVar[TextField] = TextField(
        "tableauWorksheetFieldDataCategory", "tableauWorksheetFieldDataCategory"
    )
    """
    Data category of this field.
    """
    TABLEAU_WORKSHEET_FIELD_ROLE: ClassVar[TextField] = TextField(
        "tableauWorksheetFieldRole", "tableauWorksheetFieldRole"
    )
    """
    Role of this field, for example: 'dimension', 'measure', or 'unknown'.
    """
    TABLEAU_WORKSHEET_FIELD_DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "tableauWorksheetFieldDataType",
        "tableauWorksheetFieldDataType",
        "tableauWorksheetFieldDataType.text",
    )
    """
    Data type of this field.
    """
    TABLEAU_WORKSHEET_FIELD_UPSTREAM_TABLES: ClassVar[KeywordField] = KeywordField(
        "tableauWorksheetFieldUpstreamTables", "tableauWorksheetFieldUpstreamTables"
    )
    """
    Tables upstream to this worksheet field.
    """
    TABLEAU_WORKSHEET_FIELD_FORMULA: ClassVar[TextField] = TextField(
        "tableauWorksheetFieldFormula", "tableauWorksheetFieldFormula"
    )
    """
    Formula for this field.
    """
    TABLEAU_WORKSHEET_FIELD_BIN_SIZE: ClassVar[TextField] = TextField(
        "tableauWorksheetFieldBinSize", "tableauWorksheetFieldBinSize"
    )
    """
    Bin size of this field.
    """
    TABLEAU_WORKSHEET_FIELD_UPSTREAM_COLUMNS: ClassVar[KeywordField] = KeywordField(
        "tableauWorksheetFieldUpstreamColumns", "tableauWorksheetFieldUpstreamColumns"
    )
    """
    Columns upstream to this field.
    """
    TABLEAU_WORKSHEET_FIELD_UPSTREAM_FIELDS: ClassVar[KeywordField] = KeywordField(
        "tableauWorksheetFieldUpstreamFields", "tableauWorksheetFieldUpstreamFields"
    )
    """
    Fields upstream to this field.
    """
    TABLEAU_WORKSHEET_FIELD_TYPE: ClassVar[TextField] = TextField(
        "tableauWorksheetFieldType", "tableauWorksheetFieldType"
    )
    """
    Type of this worksheet field.
    """

    TABLEAU_DATASOURCE_FIELD: ClassVar[RelationField] = RelationField(
        "tableauDatasourceField"
    )
    """
    TBC
    """
    TABLEAU_CALCULATED_FIELD: ClassVar[RelationField] = RelationField(
        "tableauCalculatedField"
    )
    """
    TBC
    """
    TABLEAU_DASHBOARD_FIELD: ClassVar[RelationField] = RelationField(
        "tableauDashboardField"
    )
    """
    TBC
    """
    TABLEAU_WORKSHEET: ClassVar[RelationField] = RelationField("tableauWorksheet")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "tableau_site_qualified_name",
        "tableau_project_qualified_name",
        "tableau_top_level_project_qualified_name",
        "tableau_workbook_qualified_name",
        "tableau_worksheet_qualified_name",
        "tableau_project_hierarchy",
        "tableau_fully_qualified_name",
        "tableau_worksheet_field_data_category",
        "tableau_worksheet_field_role",
        "tableau_worksheet_field_data_type",
        "tableau_worksheet_field_upstream_tables",
        "tableau_worksheet_field_formula",
        "tableau_worksheet_field_bin_size",
        "tableau_worksheet_field_upstream_columns",
        "tableau_worksheet_field_upstream_fields",
        "tableau_worksheet_field_type",
        "tableau_datasource_field",
        "tableau_calculated_field",
        "tableau_dashboard_field",
        "tableau_worksheet",
    ]

    @property
    def tableau_site_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_site_qualified_name
        )

    @tableau_site_qualified_name.setter
    def tableau_site_qualified_name(self, tableau_site_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_site_qualified_name = tableau_site_qualified_name

    @property
    def tableau_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_project_qualified_name
        )

    @tableau_project_qualified_name.setter
    def tableau_project_qualified_name(
        self, tableau_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_project_qualified_name = tableau_project_qualified_name

    @property
    def tableau_top_level_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_top_level_project_qualified_name
        )

    @tableau_top_level_project_qualified_name.setter
    def tableau_top_level_project_qualified_name(
        self, tableau_top_level_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_top_level_project_qualified_name = (
            tableau_top_level_project_qualified_name
        )

    @property
    def tableau_workbook_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_workbook_qualified_name
        )

    @tableau_workbook_qualified_name.setter
    def tableau_workbook_qualified_name(
        self, tableau_workbook_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_workbook_qualified_name = (
            tableau_workbook_qualified_name
        )

    @property
    def tableau_worksheet_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_qualified_name
        )

    @tableau_worksheet_qualified_name.setter
    def tableau_worksheet_qualified_name(
        self, tableau_worksheet_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_qualified_name = (
            tableau_worksheet_qualified_name
        )

    @property
    def tableau_project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_project_hierarchy
        )

    @tableau_project_hierarchy.setter
    def tableau_project_hierarchy(
        self, tableau_project_hierarchy: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_project_hierarchy = tableau_project_hierarchy

    @property
    def tableau_fully_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_fully_qualified_name
        )

    @tableau_fully_qualified_name.setter
    def tableau_fully_qualified_name(self, tableau_fully_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_fully_qualified_name = tableau_fully_qualified_name

    @property
    def tableau_worksheet_field_data_category(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_data_category
        )

    @tableau_worksheet_field_data_category.setter
    def tableau_worksheet_field_data_category(
        self, tableau_worksheet_field_data_category: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_data_category = (
            tableau_worksheet_field_data_category
        )

    @property
    def tableau_worksheet_field_role(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_role
        )

    @tableau_worksheet_field_role.setter
    def tableau_worksheet_field_role(self, tableau_worksheet_field_role: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_role = tableau_worksheet_field_role

    @property
    def tableau_worksheet_field_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_data_type
        )

    @tableau_worksheet_field_data_type.setter
    def tableau_worksheet_field_data_type(
        self, tableau_worksheet_field_data_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_data_type = (
            tableau_worksheet_field_data_type
        )

    @property
    def tableau_worksheet_field_upstream_tables(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_upstream_tables
        )

    @tableau_worksheet_field_upstream_tables.setter
    def tableau_worksheet_field_upstream_tables(
        self, tableau_worksheet_field_upstream_tables: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_upstream_tables = (
            tableau_worksheet_field_upstream_tables
        )

    @property
    def tableau_worksheet_field_formula(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_formula
        )

    @tableau_worksheet_field_formula.setter
    def tableau_worksheet_field_formula(
        self, tableau_worksheet_field_formula: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_formula = (
            tableau_worksheet_field_formula
        )

    @property
    def tableau_worksheet_field_bin_size(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_bin_size
        )

    @tableau_worksheet_field_bin_size.setter
    def tableau_worksheet_field_bin_size(
        self, tableau_worksheet_field_bin_size: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_bin_size = (
            tableau_worksheet_field_bin_size
        )

    @property
    def tableau_worksheet_field_upstream_columns(
        self,
    ) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_upstream_columns
        )

    @tableau_worksheet_field_upstream_columns.setter
    def tableau_worksheet_field_upstream_columns(
        self, tableau_worksheet_field_upstream_columns: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_upstream_columns = (
            tableau_worksheet_field_upstream_columns
        )

    @property
    def tableau_worksheet_field_upstream_fields(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_upstream_fields
        )

    @tableau_worksheet_field_upstream_fields.setter
    def tableau_worksheet_field_upstream_fields(
        self, tableau_worksheet_field_upstream_fields: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_upstream_fields = (
            tableau_worksheet_field_upstream_fields
        )

    @property
    def tableau_worksheet_field_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_worksheet_field_type
        )

    @tableau_worksheet_field_type.setter
    def tableau_worksheet_field_type(self, tableau_worksheet_field_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field_type = tableau_worksheet_field_type

    @property
    def tableau_datasource_field(self) -> Optional[TableauDatasourceField]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_datasource_field
        )

    @tableau_datasource_field.setter
    def tableau_datasource_field(
        self, tableau_datasource_field: Optional[TableauDatasourceField]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_datasource_field = tableau_datasource_field

    @property
    def tableau_calculated_field(self) -> Optional[TableauCalculatedField]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_calculated_field
        )

    @tableau_calculated_field.setter
    def tableau_calculated_field(
        self, tableau_calculated_field: Optional[TableauCalculatedField]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_calculated_field = tableau_calculated_field

    @property
    def tableau_dashboard_field(self) -> Optional[TableauDashboardField]:
        return (
            None if self.attributes is None else self.attributes.tableau_dashboard_field
        )

    @tableau_dashboard_field.setter
    def tableau_dashboard_field(
        self, tableau_dashboard_field: Optional[TableauDashboardField]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field = tableau_dashboard_field

    @property
    def tableau_worksheet(self) -> Optional[TableauWorksheet]:
        return None if self.attributes is None else self.attributes.tableau_worksheet

    @tableau_worksheet.setter
    def tableau_worksheet(self, tableau_worksheet: Optional[TableauWorksheet]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet = tableau_worksheet

    class Attributes(Tableau.Attributes):
        tableau_site_qualified_name: Optional[str] = Field(default=None, description="")
        tableau_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_workbook_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_worksheet_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        tableau_fully_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_worksheet_field_data_category: Optional[str] = Field(
            default=None, description=""
        )
        tableau_worksheet_field_role: Optional[str] = Field(
            default=None, description=""
        )
        tableau_worksheet_field_data_type: Optional[str] = Field(
            default=None, description=""
        )
        tableau_worksheet_field_upstream_tables: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        tableau_worksheet_field_formula: Optional[str] = Field(
            default=None, description=""
        )
        tableau_worksheet_field_bin_size: Optional[str] = Field(
            default=None, description=""
        )
        tableau_worksheet_field_upstream_columns: Optional[List[Dict[str, str]]] = (
            Field(default=None, description="")
        )
        tableau_worksheet_field_upstream_fields: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        tableau_worksheet_field_type: Optional[str] = Field(
            default=None, description=""
        )
        tableau_datasource_field: Optional[TableauDatasourceField] = Field(
            default=None, description=""
        )  # relationship
        tableau_calculated_field: Optional[TableauCalculatedField] = Field(
            default=None, description=""
        )  # relationship
        tableau_dashboard_field: Optional[TableauDashboardField] = Field(
            default=None, description=""
        )  # relationship
        tableau_worksheet: Optional[TableauWorksheet] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauWorksheetField.Attributes = Field(
        default_factory=lambda: TableauWorksheetField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_calculated_field import TableauCalculatedField  # noqa: E402, F401
from .tableau_dashboard_field import TableauDashboardField  # noqa: E402, F401
from .tableau_datasource_field import TableauDatasourceField  # noqa: E402, F401
from .tableau_worksheet import TableauWorksheet  # noqa: E402, F401

TableauWorksheetField.Attributes.update_forward_refs()
