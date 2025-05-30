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


class TableauDashboard(Tableau):
    """Description"""

    type_name: str = Field(default="TableauDashboard", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauDashboard":
            raise ValueError("must be TableauDashboard")
        return v

    def __setattr__(self, name, value):
        if name in TableauDashboard._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SITE_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "siteQualifiedName", "siteQualifiedName"
    )
    """
    Unique name of the site in which this dashboard exists.
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "projectQualifiedName", "projectQualifiedName.keyword", "projectQualifiedName"
    )
    """
    Unique name of the project in which this dashboard exists.
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    Unique name of the workbook in which this dashboard exists.
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this dashboard exists.
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    List of top-level projects and their nested child projects.
    """

    TABLEAU_DASHBOARD_FIELDS: ClassVar[RelationField] = RelationField(
        "tableauDashboardFields"
    )
    """
    TBC
    """
    WORKBOOK: ClassVar[RelationField] = RelationField("workbook")
    """
    TBC
    """
    TABLEAU_PARENT_DASHBOARDS: ClassVar[RelationField] = RelationField(
        "tableauParentDashboards"
    )
    """
    TBC
    """
    TABLEAU_EMBEDDED_DASHBOARDS: ClassVar[RelationField] = RelationField(
        "tableauEmbeddedDashboards"
    )
    """
    TBC
    """
    WORKSHEETS: ClassVar[RelationField] = RelationField("worksheets")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "site_qualified_name",
        "project_qualified_name",
        "workbook_qualified_name",
        "top_level_project_qualified_name",
        "project_hierarchy",
        "tableau_dashboard_fields",
        "workbook",
        "tableau_parent_dashboards",
        "tableau_embedded_dashboards",
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
    def project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def tableau_dashboard_fields(self) -> Optional[List[TableauDashboardField]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_dashboard_fields
        )

    @tableau_dashboard_fields.setter
    def tableau_dashboard_fields(
        self, tableau_dashboard_fields: Optional[List[TableauDashboardField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_dashboard_fields = tableau_dashboard_fields

    @property
    def workbook(self) -> Optional[TableauWorkbook]:
        return None if self.attributes is None else self.attributes.workbook

    @workbook.setter
    def workbook(self, workbook: Optional[TableauWorkbook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbook = workbook

    @property
    def tableau_parent_dashboards(self) -> Optional[List[TableauDashboard]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_parent_dashboards
        )

    @tableau_parent_dashboards.setter
    def tableau_parent_dashboards(
        self, tableau_parent_dashboards: Optional[List[TableauDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_parent_dashboards = tableau_parent_dashboards

    @property
    def tableau_embedded_dashboards(self) -> Optional[List[TableauDashboard]]:
        return (
            None
            if self.attributes is None
            else self.attributes.tableau_embedded_dashboards
        )

    @tableau_embedded_dashboards.setter
    def tableau_embedded_dashboards(
        self, tableau_embedded_dashboards: Optional[List[TableauDashboard]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.tableau_embedded_dashboards = tableau_embedded_dashboards

    @property
    def worksheets(self) -> Optional[List[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[List[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(default=None, description="")
        project_qualified_name: Optional[str] = Field(default=None, description="")
        workbook_qualified_name: Optional[str] = Field(default=None, description="")
        top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        tableau_dashboard_fields: Optional[List[TableauDashboardField]] = Field(
            default=None, description=""
        )  # relationship
        workbook: Optional[TableauWorkbook] = Field(
            default=None, description=""
        )  # relationship
        tableau_parent_dashboards: Optional[List[TableauDashboard]] = Field(
            default=None, description=""
        )  # relationship
        tableau_embedded_dashboards: Optional[List[TableauDashboard]] = Field(
            default=None, description=""
        )  # relationship
        worksheets: Optional[List[TableauWorksheet]] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauDashboard.Attributes = Field(
        default_factory=lambda: TableauDashboard.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_dashboard_field import TableauDashboardField  # noqa: E402, F401
from .tableau_workbook import TableauWorkbook  # noqa: E402, F401
from .tableau_worksheet import TableauWorksheet  # noqa: E402, F401

TableauDashboard.Attributes.update_forward_refs()
