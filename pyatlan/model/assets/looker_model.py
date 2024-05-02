# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .looker import Looker


class LookerModel(Looker):
    """Description"""

    type_name: str = Field(default="LookerModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerModel":
            raise ValueError("must be LookerModel")
        return v

    def __setattr__(self, name, value):
        if name in LookerModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECT_NAME: ClassVar[KeywordField] = KeywordField("projectName", "projectName")
    """
    Name of the project in which the model exists.
    """

    EXPLORES: ClassVar[RelationField] = RelationField("explores")
    """
    TBC
    """
    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    LOOK: ClassVar[RelationField] = RelationField("look")
    """
    TBC
    """
    QUERIES: ClassVar[RelationField] = RelationField("queries")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "project_name",
        "explores",
        "project",
        "look",
        "queries",
        "fields",
    ]

    @property
    def project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.project_name

    @project_name.setter
    def project_name(self, project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project_name = project_name

    @property
    def explores(self) -> Optional[List[LookerExplore]]:
        return None if self.attributes is None else self.attributes.explores

    @explores.setter
    def explores(self, explores: Optional[List[LookerExplore]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explores = explores

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def look(self) -> Optional[LookerLook]:
        return None if self.attributes is None else self.attributes.look

    @look.setter
    def look(self, look: Optional[LookerLook]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.look = look

    @property
    def queries(self) -> Optional[List[LookerQuery]]:
        return None if self.attributes is None else self.attributes.queries

    @queries.setter
    def queries(self, queries: Optional[List[LookerQuery]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.queries = queries

    @property
    def fields(self) -> Optional[List[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[List[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(default=None, description="")
        explores: Optional[List[LookerExplore]] = Field(
            default=None, description=""
        )  # relationship
        project: Optional[LookerProject] = Field(
            default=None, description=""
        )  # relationship
        look: Optional[LookerLook] = Field(default=None, description="")  # relationship
        queries: Optional[List[LookerQuery]] = Field(
            default=None, description=""
        )  # relationship
        fields: Optional[List[LookerField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerModel.Attributes = Field(
        default_factory=lambda: LookerModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_explore import LookerExplore  # noqa
from .looker_field import LookerField  # noqa
from .looker_look import LookerLook  # noqa
from .looker_project import LookerProject  # noqa
from .looker_query import LookerQuery  # noqa
