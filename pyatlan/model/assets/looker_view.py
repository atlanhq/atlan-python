# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .looker import Looker


class LookerView(Looker):
    """Description"""

    type_name: str = Field(default="LookerView", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerView":
            raise ValueError("must be LookerView")
        return v

    def __setattr__(self, name, value):
        if name in LookerView._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECT_NAME: ClassVar[KeywordField] = KeywordField("projectName", "projectName")
    """
    Name of the project in which this view exists.
    """
    LOOKER_VIEW_FILE_PATH: ClassVar[KeywordField] = KeywordField(
        "lookerViewFilePath", "lookerViewFilePath"
    )
    """
    File path of this view within the project.
    """
    LOOKER_VIEW_FILE_NAME: ClassVar[KeywordField] = KeywordField(
        "lookerViewFileName", "lookerViewFileName"
    )
    """
    File name of this view.
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
        "project_name",
        "looker_view_file_path",
        "looker_view_file_name",
        "project",
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
    def looker_view_file_path(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.looker_view_file_path
        )

    @looker_view_file_path.setter
    def looker_view_file_path(self, looker_view_file_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_view_file_path = looker_view_file_path

    @property
    def looker_view_file_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.looker_view_file_name
        )

    @looker_view_file_name.setter
    def looker_view_file_name(self, looker_view_file_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_view_file_name = looker_view_file_name

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

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
        looker_view_file_path: Optional[str] = Field(default=None, description="")
        looker_view_file_name: Optional[str] = Field(default=None, description="")
        project: Optional[LookerProject] = Field(
            default=None, description=""
        )  # relationship
        fields: Optional[List[LookerField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerView.Attributes = Field(
        default_factory=lambda: LookerView.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_field import LookerField  # noqa
from .looker_project import LookerProject  # noqa
