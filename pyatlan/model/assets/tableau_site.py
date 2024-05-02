# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .tableau import Tableau


class TableauSite(Tableau):
    """Description"""

    type_name: str = Field(default="TableauSite", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "TableauSite":
            raise ValueError("must be TableauSite")
        return v

    def __setattr__(self, name, value):
        if name in TableauSite._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECTS: ClassVar[RelationField] = RelationField("projects")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "projects",
    ]

    @property
    def projects(self) -> Optional[List[TableauProject]]:
        return None if self.attributes is None else self.attributes.projects

    @projects.setter
    def projects(self, projects: Optional[List[TableauProject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.projects = projects

    class Attributes(Tableau.Attributes):
        projects: Optional[List[TableauProject]] = Field(
            default=None, description=""
        )  # relationship

    attributes: TableauSite.Attributes = Field(
        default_factory=lambda: TableauSite.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .tableau_project import TableauProject  # noqa
