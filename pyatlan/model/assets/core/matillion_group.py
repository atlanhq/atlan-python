# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import NumericField, RelationField

from .matillion import Matillion


class MatillionGroup(Matillion):
    """Description"""

    type_name: str = Field(default="MatillionGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MatillionGroup":
            raise ValueError("must be MatillionGroup")
        return v

    def __setattr__(self, name, value):
        if name in MatillionGroup._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_PROJECT_COUNT: ClassVar[NumericField] = NumericField(
        "matillionProjectCount", "matillionProjectCount"
    )
    """
    Number of projects within the group.
    """

    MATILLION_PROJECTS: ClassVar[RelationField] = RelationField("matillionProjects")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "matillion_project_count",
        "matillion_projects",
    ]

    @property
    def matillion_project_count(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.matillion_project_count
        )

    @matillion_project_count.setter
    def matillion_project_count(self, matillion_project_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project_count = matillion_project_count

    @property
    def matillion_projects(self) -> Optional[List[MatillionProject]]:
        return None if self.attributes is None else self.attributes.matillion_projects

    @matillion_projects.setter
    def matillion_projects(self, matillion_projects: Optional[List[MatillionProject]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_projects = matillion_projects

    class Attributes(Matillion.Attributes):
        matillion_project_count: Optional[int] = Field(default=None, description="")
        matillion_projects: Optional[List[MatillionProject]] = Field(
            default=None, description=""
        )  # relationship

    attributes: MatillionGroup.Attributes = Field(
        default_factory=lambda: MatillionGroup.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .matillion_project import MatillionProject  # noqa
