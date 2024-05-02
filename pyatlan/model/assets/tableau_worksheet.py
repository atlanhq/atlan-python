# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .tableau import Tableau


class TableauWorksheet(Tableau):
    """Description"""

    type_name: str = Field(default="TableauWorksheet", allow_mutation=False)

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
    Unique name of the site in which this worksheet exists.
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    Unique name of the project in which this worksheet exists.
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this worksheet exists.
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    List of top-level projects with their nested child projects.
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    Unique name of the workbook in which this worksheet exists.
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

    _convenience_properties: ClassVar[List[str]] = [
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
    def project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[List[Dict[str, str]]]):
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
    def datasource_fields(self) -> Optional[List[TableauDatasourceField]]:
        return None if self.attributes is None else self.attributes.datasource_fields

    @datasource_fields.setter
    def datasource_fields(
        self, datasource_fields: Optional[List[TableauDatasourceField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.datasource_fields = datasource_fields

    @property
    def calculated_fields(self) -> Optional[List[TableauCalculatedField]]:
        return None if self.attributes is None else self.attributes.calculated_fields

    @calculated_fields.setter
    def calculated_fields(
        self, calculated_fields: Optional[List[TableauCalculatedField]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.calculated_fields = calculated_fields

    @property
    def dashboards(self) -> Optional[List[TableauDashboard]]:
        return None if self.attributes is None else self.attributes.dashboards

    @dashboards.setter
    def dashboards(self, dashboards: Optional[List[TableauDashboard]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dashboards = dashboards

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(default=None, description="")
        project_qualified_name: Optional[str] = Field(default=None, description="")
        top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        workbook_qualified_name: Optional[str] = Field(default=None, description="")
        workbook: Optional[TableauWorkbook] = Field(
            default=None, description=""
        )  # relationship
        datasource_fields: Optional[List[TableauDatasourceField]] = Field(
            default=None, description=""
        )  # relationship
        calculated_fields: Optional[List[TableauCalculatedField]] = Field(
            default=None, description=""
        )  # relationship
        dashboards: Optional[List[TableauDashboard]] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauWorksheet.Attributes = Field(
        default_factory=lambda: TableauWorksheet.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_calculated_field import TableauCalculatedField  # noqa
from .tableau_dashboard import TableauDashboard  # noqa
from .tableau_datasource_field import TableauDatasourceField  # noqa
from .tableau_workbook import TableauWorkbook  # noqa
