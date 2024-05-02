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


class TableauCalculatedField(Tableau):
    """Description"""

    type_name: str = Field(default="TableauCalculatedField", allow_mutation=False)

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
    Unique name of the site in which this calculated field exists.
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    Unique name of the project in which this calculated field exists.
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this calculated field exists.
    """
    WORKBOOK_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "workbookQualifiedName", "workbookQualifiedName"
    )
    """
    Unique name of the workbook in which this calculated field exists.
    """
    DATASOURCE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "datasourceQualifiedName", "datasourceQualifiedName"
    )
    """
    Unique name of the datasource in which this calculated field exists.
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    List of top-level projects and their nested projects.
    """
    DATA_CATEGORY: ClassVar[KeywordField] = KeywordField("dataCategory", "dataCategory")
    """
    Data category of this field.
    """
    ROLE: ClassVar[KeywordField] = KeywordField("role", "role")
    """
    Role of this field, for example: 'dimension', 'measure', or 'unknown'.
    """
    TABLEAU_DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "tableauDataType", "tableauDataType", "tableauDataType.text"
    )
    """
    Data type of the field, from Tableau.
    """
    FORMULA: ClassVar[KeywordField] = KeywordField("formula", "formula")
    """
    Formula for this calculated field.
    """
    UPSTREAM_FIELDS: ClassVar[KeywordField] = KeywordField(
        "upstreamFields", "upstreamFields"
    )
    """
    List of fields that are upstream to this calculated field.
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
    def project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[List[Dict[str, str]]]):
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
    def upstream_fields(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.upstream_fields

    @upstream_fields.setter
    def upstream_fields(self, upstream_fields: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.upstream_fields = upstream_fields

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
        data_category: Optional[str] = Field(default=None, description="")
        role: Optional[str] = Field(default=None, description="")
        tableau_data_type: Optional[str] = Field(default=None, description="")
        formula: Optional[str] = Field(default=None, description="")
        upstream_fields: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        worksheets: Optional[List[TableauWorksheet]] = Field(
            default=None, description=""
        )  # relationship
        datasource: Optional[TableauDatasource] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauCalculatedField.Attributes = Field(
        default_factory=lambda: TableauCalculatedField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_datasource import TableauDatasource  # noqa
from .tableau_worksheet import TableauWorksheet  # noqa
