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


class TableauDashboardField(Tableau):
    """Description"""

    type_name: str = Field(default="TableauDashboardField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDashboardField":
            raise ValueError("must be TableauDashboardField")
        return v

    def __setattr__(self, name, value):
        if name in TableauDashboardField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TABLEAU_SITE_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "tableauSiteQualifiedName", "tableauSiteQualifiedName"
    )
    """
    Unique name of the site in which this dashboard field exists.
    """
    TABLEAU_PROJECT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "tableauProjectQualifiedName",
        "tableauProjectQualifiedName.keyword",
        "tableauProjectQualifiedName",
    )
    """
    Unique name of the project in which this dashboard field exists.
    """
    TABLEAU_TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "tableauTopLevelProjectQualifiedName", "tableauTopLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this dashboard field exists.
    """
    TABLEAU_DASHBOARD_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "tableauDashboardQualifiedName", "tableauDashboardQualifiedName"
    )
    """
    Unique name of the datasource in which this dashboard field exists.
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
    TABLEAU_DASHBOARD_FIELD_DATA_CATEGORY: ClassVar[TextField] = TextField(
        "tableauDashboardFieldDataCategory", "tableauDashboardFieldDataCategory"
    )
    """
    Data category of this field.
    """
    TABLEAU_DASHBOARD_FIELD_ROLE: ClassVar[TextField] = TextField(
        "tableauDashboardFieldRole", "tableauDashboardFieldRole"
    )
    """
    Role of this field, for example: 'dimension', 'measure', or 'unknown'.
    """
    TABLEAU_DASHBOARD_FIELD_DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "tableauDashboardFieldDataType",
        "tableauDashboardFieldDataType",
        "tableauDashboardFieldDataType.text",
    )
    """
    Data type of this field.
    """
    TABLEAU_UPSTREAM_TABLES: ClassVar[KeywordField] = KeywordField(
        "tableauUpstreamTables", "tableauUpstreamTables"
    )
    """
    Tables upstream to this worksheet field.
    """
    TABLEAU_DASHBOARD_FIELD_FORMULA: ClassVar[TextField] = TextField(
        "tableauDashboardFieldFormula", "tableauDashboardFieldFormula"
    )
    """
    Formula for this field.
    """
    TABLEAU_DASHBOARD_FIELD_BIN_SIZE: ClassVar[TextField] = TextField(
        "tableauDashboardFieldBinSize", "tableauDashboardFieldBinSize"
    )
    """
    Bin size of this field.
    """
    TABLEAU_DASHBOARD_FIELD_UPSTREAM_COLUMNS: ClassVar[KeywordField] = KeywordField(
        "tableauDashboardFieldUpstreamColumns", "tableauDashboardFieldUpstreamColumns"
    )
    """
    Columns upstream to this field.
    """
    TABLEAU_DASHBOARD_FIELD_UPSTREAM_FIELDS: ClassVar[KeywordField] = KeywordField(
        "tableauDashboardFieldUpstreamFields", "tableauDashboardFieldUpstreamFields"
    )
    """
    Fields upstream to this field.
    """
    TABLEAU_DASHBOARD_FIELD_TYPE: ClassVar[TextField] = TextField(
        "tableauDashboardFieldType", "tableauDashboardFieldType"
    )
    """
    Type of this dashboard field.
    """

    TABLEAU_WORKSHEET_FIELD: ClassVar[RelationField] = RelationField(
        "tableauWorksheetField"
    )
    """
    TBC
    """
    TABLEAU_DASHBOARD: ClassVar[RelationField] = RelationField("tableauDashboard")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "tableau_site_qualified_name",
        "tableau_project_qualified_name",
        "tableau_top_level_project_qualified_name",
        "tableau_dashboard_qualified_name",
        "tableau_project_hierarchy",
        "tableau_fully_qualified_name",
        "tableau_dashboard_field_data_category",
        "tableau_dashboard_field_role",
        "tableau_dashboard_field_data_type",
        "tableau_upstream_tables",
        "tableau_dashboard_field_formula",
        "tableau_dashboard_field_bin_size",
        "tableau_dashboard_field_upstream_columns",
        "tableau_dashboard_field_upstream_fields",
        "tableau_dashboard_field_type",
        "tableau_worksheet_field",
        "tableau_dashboard",
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
    def tableau_dashboard_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_qualified_name
        )

    @tableau_dashboard_qualified_name.setter
    def tableau_dashboard_qualified_name(
        self, tableau_dashboard_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_qualified_name = (
            tableau_dashboard_qualified_name
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
    def tableau_dashboard_field_data_category(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_field_data_category
        )

    @tableau_dashboard_field_data_category.setter
    def tableau_dashboard_field_data_category(
        self, tableau_dashboard_field_data_category: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field_data_category = (
            tableau_dashboard_field_data_category
        )

    @property
    def tableau_dashboard_field_role(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_field_role
        )

    @tableau_dashboard_field_role.setter
    def tableau_dashboard_field_role(self, tableau_dashboard_field_role: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field_role = tableau_dashboard_field_role

    @property
    def tableau_dashboard_field_data_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_field_data_type
        )

    @tableau_dashboard_field_data_type.setter
    def tableau_dashboard_field_data_type(
        self, tableau_dashboard_field_data_type: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field_data_type = (
            tableau_dashboard_field_data_type
        )

    @property
    def tableau_upstream_tables(self) -> Optional[List[Dict[str, str]]]:
        return (
            None if self.attributes is None else self.attributes.tableau_upstream_tables
        )

    @tableau_upstream_tables.setter
    def tableau_upstream_tables(
        self, tableau_upstream_tables: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_upstream_tables = tableau_upstream_tables

    @property
    def tableau_dashboard_field_formula(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_field_formula
        )

    @tableau_dashboard_field_formula.setter
    def tableau_dashboard_field_formula(
        self, tableau_dashboard_field_formula: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field_formula = (
            tableau_dashboard_field_formula
        )

    @property
    def tableau_dashboard_field_bin_size(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_field_bin_size
        )

    @tableau_dashboard_field_bin_size.setter
    def tableau_dashboard_field_bin_size(
        self, tableau_dashboard_field_bin_size: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field_bin_size = (
            tableau_dashboard_field_bin_size
        )

    @property
    def tableau_dashboard_field_upstream_columns(
        self,
    ) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_field_upstream_columns
        )

    @tableau_dashboard_field_upstream_columns.setter
    def tableau_dashboard_field_upstream_columns(
        self, tableau_dashboard_field_upstream_columns: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field_upstream_columns = (
            tableau_dashboard_field_upstream_columns
        )

    @property
    def tableau_dashboard_field_upstream_fields(self) -> Optional[List[Dict[str, str]]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_field_upstream_fields
        )

    @tableau_dashboard_field_upstream_fields.setter
    def tableau_dashboard_field_upstream_fields(
        self, tableau_dashboard_field_upstream_fields: Optional[List[Dict[str, str]]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field_upstream_fields = (
            tableau_dashboard_field_upstream_fields
        )

    @property
    def tableau_dashboard_field_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_field_type
        )

    @tableau_dashboard_field_type.setter
    def tableau_dashboard_field_type(self, tableau_dashboard_field_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_field_type = tableau_dashboard_field_type

    @property
    def tableau_worksheet_field(self) -> Optional[TableauWorksheetField]:
        return (
            None if self.attributes is None else self.attributes.tableau_worksheet_field
        )

    @tableau_worksheet_field.setter
    def tableau_worksheet_field(
        self, tableau_worksheet_field: Optional[TableauWorksheetField]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_worksheet_field = tableau_worksheet_field

    @property
    def tableau_dashboard(self) -> Optional[TableauDashboard]:
        return None if self.attributes is None else self.attributes.tableau_dashboard

    @tableau_dashboard.setter
    def tableau_dashboard(self, tableau_dashboard: Optional[TableauDashboard]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard = tableau_dashboard

    class Attributes(Tableau.Attributes):
        tableau_site_qualified_name: Optional[str] = Field(default=None, description="")
        tableau_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_dashboard_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        tableau_fully_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        tableau_dashboard_field_data_category: Optional[str] = Field(
            default=None, description=""
        )
        tableau_dashboard_field_role: Optional[str] = Field(
            default=None, description=""
        )
        tableau_dashboard_field_data_type: Optional[str] = Field(
            default=None, description=""
        )
        tableau_upstream_tables: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        tableau_dashboard_field_formula: Optional[str] = Field(
            default=None, description=""
        )
        tableau_dashboard_field_bin_size: Optional[str] = Field(
            default=None, description=""
        )
        tableau_dashboard_field_upstream_columns: Optional[List[Dict[str, str]]] = (
            Field(default=None, description="")
        )
        tableau_dashboard_field_upstream_fields: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        tableau_dashboard_field_type: Optional[str] = Field(
            default=None, description=""
        )
        tableau_worksheet_field: Optional[TableauWorksheetField] = Field(
            default=None, description=""
        )  # relationship
        tableau_dashboard: Optional[TableauDashboard] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauDashboardField.Attributes = Field(
        default_factory=lambda: TableauDashboardField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_dashboard import TableauDashboard  # noqa: E402, F401
from .tableau_worksheet_field import TableauWorksheetField  # noqa: E402, F401

TableauDashboardField.Attributes.update_forward_refs()
