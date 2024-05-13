# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .tableau import Tableau


class TableauProject(Tableau):
    """Description"""

    type_name: str = Field(default="TableauProject", allow_mutation=False)

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
    Unique name of the site in which this project exists.
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this project exists, if this is a nested project.
    """
    IS_TOP_LEVEL_PROJECT: ClassVar[BooleanField] = BooleanField(
        "isTopLevelProject", "isTopLevelProject"
    )
    """
    Whether this project is a top-level project (true) or not (false).
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    List of top-level projects with their nested child projects.
    """

    WORKBOOKS: ClassVar[RelationField] = RelationField("workbooks")
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
    PARENT_PROJECT: ClassVar[RelationField] = RelationField("parentProject")
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

    _convenience_properties: ClassVar[List[str]] = [
        "site_qualified_name",
        "top_level_project_qualified_name",
        "is_top_level_project",
        "project_hierarchy",
        "workbooks",
        "flows",
        "child_projects",
        "parent_project",
        "site",
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
    def project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def workbooks(self) -> Optional[List[TableauWorkbook]]:
        return None if self.attributes is None else self.attributes.workbooks

    @workbooks.setter
    def workbooks(self, workbooks: Optional[List[TableauWorkbook]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workbooks = workbooks

    @property
    def flows(self) -> Optional[List[TableauFlow]]:
        return None if self.attributes is None else self.attributes.flows

    @flows.setter
    def flows(self, flows: Optional[List[TableauFlow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flows = flows

    @property
    def child_projects(self) -> Optional[List[TableauProject]]:
        return None if self.attributes is None else self.attributes.child_projects

    @child_projects.setter
    def child_projects(self, child_projects: Optional[List[TableauProject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.child_projects = child_projects

    @property
    def parent_project(self) -> Optional[TableauProject]:
        return None if self.attributes is None else self.attributes.parent_project

    @parent_project.setter
    def parent_project(self, parent_project: Optional[TableauProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_project = parent_project

    @property
    def site(self) -> Optional[TableauSite]:
        return None if self.attributes is None else self.attributes.site

    @site.setter
    def site(self, site: Optional[TableauSite]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.site = site

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
        top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        is_top_level_project: Optional[bool] = Field(default=None, description="")
        project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        workbooks: Optional[List[TableauWorkbook]] = Field(
            default=None, description=""
        )  # relationship
        flows: Optional[List[TableauFlow]] = Field(
            default=None, description=""
        )  # relationship
        child_projects: Optional[List[TableauProject]] = Field(
            default=None, description=""
        )  # relationship
        parent_project: Optional[TableauProject] = Field(
            default=None, description=""
        )  # relationship
        site: Optional[TableauSite] = Field(
            default=None, description=""
        )  # relationship
        datasources: Optional[List[TableauDatasource]] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauProject.Attributes = Field(
        default_factory=lambda: TableauProject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_datasource import TableauDatasource  # noqa
from .tableau_flow import TableauFlow  # noqa
from .tableau_site import TableauSite  # noqa
from .tableau_workbook import TableauWorkbook  # noqa
