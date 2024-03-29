# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .tableau import Tableau


class TableauWorkbook(Tableau):
    """Description"""

    type_name: str = Field(default="TableauWorkbook", allow_mutation=False)

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
    Unique name of the site in which this workbook exists.
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    Unique name of the project in which this workbook exists.
    """
    TOP_LEVEL_PROJECT_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectName", "topLevelProjectName"
    )
    """
    Simple name of the top-level project in which this workbook exists.
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this workbook exists.
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    List of top-level projects with their nested child projects.
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

    _convenience_properties: ClassVar[List[str]] = [
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
    def project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[List[Dict[str, str]]]):
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
    def dashboards(self) -> Optional[List[TableauDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[List[TableauDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    @property
    def worksheets(self) -> Optional[List[TableauWorksheet]]:
        return None if self.attributes is None else self.attributes.worksheets

    @worksheets.setter
    def worksheets(self, worksheets: Optional[List[TableauWorksheet]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.worksheets = worksheets

    @property
    def datasources(self) -> Optional[List[TableauDatasource]]:
        return None if self.attributes is None else self.attributes.datasources

    @datasources.setter
    def datasources(self, datasources: Optional[List[TableauDatasource]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasources = datasources

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(default=None, description="")
        project_qualified_name: Optional[str] = Field(default=None, description="")
        top_level_project_name: Optional[str] = Field(default=None, description="")
        top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        project: Optional[TableauProject] = Field(
            default=None, description=""
        )  # relationship
        dashboards: Optional[List[TableauDashboard]] = Field(
            default=None, description=""
        )  # relationship
        worksheets: Optional[List[TableauWorksheet]] = Field(
            default=None, description=""
        )  # relationship
        datasources: Optional[List[TableauDatasource]] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauWorkbook.Attributes = Field(
        default_factory=lambda: TableauWorkbook.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_dashboard import TableauDashboard  # noqa
from .tableau_datasource import TableauDatasource  # noqa
from .tableau_project import TableauProject  # noqa
from .tableau_worksheet import TableauWorksheet  # noqa
