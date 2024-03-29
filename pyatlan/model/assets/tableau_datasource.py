# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField

from .tableau import Tableau


class TableauDatasource(Tableau):
    """Description"""

    type_name: str = Field(default="TableauDatasource", allow_mutation=False)

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
    Unique name of the site in which this datasource exists.
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    Unique name of the project in which this datasource exists.
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this datasource exists.
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    Unique name of the workbook in which this datasource exists.
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    List of top-level projects with their nested child projects.
    """
    IS_PUBLISHED: ClassVar[BooleanField] = BooleanField("isPublished", "isPublished")
    """
    Whether this datasource is published (true) or embedded (false).
    """
    HAS_EXTRACTS: ClassVar[BooleanField] = BooleanField("hasExtracts", "hasExtracts")
    """
    Whether this datasource has extracts (true) or not (false).
    """
    IS_CERTIFIED: ClassVar[BooleanField] = BooleanField("isCertified", "isCertified")
    """
    Whether this datasource is certified in Tableau (true) or not (false).
    """
    CERTIFIER: ClassVar[KeywordField] = KeywordField("certifier", "certifier")
    """
    Users that have marked this datasource as cerified, in Tableau.
    """
    CERTIFICATION_NOTE: ClassVar[KeywordField] = KeywordField(
        "certificationNote", "certificationNote"
    )
    """
    Notes related to this datasource being cerfified, in Tableau.
    """
    CERTIFIER_DISPLAY_NAME: ClassVar[KeywordField] = KeywordField(
        "certifierDisplayName", "certifierDisplayName"
    )
    """
    Name of the user who cerified this datasource, in Tableau.
    """
    UPSTREAM_TABLES: ClassVar[KeywordField] = KeywordField(
        "upstreamTables", "upstreamTables"
    )
    """
    List of tables that are upstream of this datasource.
    """
    UPSTREAM_DATASOURCES: ClassVar[KeywordField] = KeywordField(
        "upstreamDatasources", "upstreamDatasources"
    )
    """
    List of datasources that are upstream of this datasource.
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

    _convenience_properties: ClassVar[List[str]] = [
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
    def project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[List[Dict[str, str]]]):
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
    def certifier(self) -> Optional[Dict[str, str]]:
        return None if self.attributes is None else self.attributes.certifier

    @certifier.setter
    def certifier(self, certifier: Optional[Dict[str, str]]):
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
    def upstream_tables(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_tables

    @upstream_tables.setter
    def upstream_tables(self, upstream_tables: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_tables = upstream_tables

    @property
    def upstream_datasources(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_datasources

    @upstream_datasources.setter
    def upstream_datasources(
        self, upstream_datasources: Optional[List[Dict[str, str]]]
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
    def fields(self) -> Optional[List[TableauDatasourceField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[List[TableauDatasourceField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Tableau.Attributes):
        site_qualified_name: Optional[str] = Field(default=None, description="")
        project_qualified_name: Optional[str] = Field(default=None, description="")
        top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        workbook_qualified_name: Optional[str] = Field(default=None, description="")
        project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        is_published: Optional[bool] = Field(default=None, description="")
        has_extracts: Optional[bool] = Field(default=None, description="")
        is_certified: Optional[bool] = Field(default=None, description="")
        certifier: Optional[Dict[str, str]] = Field(default=None, description="")
        certification_note: Optional[str] = Field(default=None, description="")
        certifier_display_name: Optional[str] = Field(default=None, description="")
        upstream_tables: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        upstream_datasources: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        workbook: Optional[TableauWorkbook] = Field(
            default=None, description=""
        )  # relationship
        project: Optional[TableauProject] = Field(
            default=None, description=""
        )  # relationship
        fields: Optional[List[TableauDatasourceField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauDatasource.Attributes = Field(
        default_factory=lambda: TableauDatasource.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_datasource_field import TableauDatasourceField  # noqa
from .tableau_project import TableauProject  # noqa
from .tableau_workbook import TableauWorkbook  # noqa
