# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .tableau import Tableau


class TableauFlow(Tableau):
    """Description"""

    type_name: str = Field(default="TableauFlow", allow_mutation=False)

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
    Unique name of the site in which this flow exists.
    """
    PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "projectQualifiedName", "projectQualifiedName"
    )
    """
    Unique name of the project in which this flow exists.
    """
    TOP_LEVEL_PROJECT_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "topLevelProjectQualifiedName", "topLevelProjectQualifiedName"
    )
    """
    Unique name of the top-level project in which this flow exists.
    """
    PROJECT_HIERARCHY: ClassVar[KeywordField] = KeywordField(
        "projectHierarchy", "projectHierarchy"
    )
    """
    List of top-level projects with their nested child projects.
    """
    INPUT_FIELDS: ClassVar[KeywordField] = KeywordField("inputFields", "inputFields")
    """
    List of fields that are inputs to this flow.
    """
    OUTPUT_FIELDS: ClassVar[KeywordField] = KeywordField("outputFields", "outputFields")
    """
    List of fields that are outputs from this flow.
    """
    OUTPUT_STEPS: ClassVar[KeywordField] = KeywordField("outputSteps", "outputSteps")
    """
    List of steps that are outputs from this flow.
    """

    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
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
    def project_hierarchy(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.project_hierarchy

    @project_hierarchy.setter
    def project_hierarchy(self, project_hierarchy: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_hierarchy = project_hierarchy

    @property
    def input_fields(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.input_fields

    @input_fields.setter
    def input_fields(self, input_fields: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_fields = input_fields

    @property
    def output_fields(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.output_fields

    @output_fields.setter
    def output_fields(self, output_fields: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_fields = output_fields

    @property
    def output_steps(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.output_steps

    @output_steps.setter
    def output_steps(self, output_steps: Optional[List[Dict[str, str]]]):
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
        site_qualified_name: Optional[str] = Field(default=None, description="")
        project_qualified_name: Optional[str] = Field(default=None, description="")
        top_level_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        project_hierarchy: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        input_fields: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        output_fields: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        output_steps: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        project: Optional[TableauProject] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauFlow.Attributes = Field(
        default_factory=lambda: TableauFlow.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_project import TableauProject  # noqa
