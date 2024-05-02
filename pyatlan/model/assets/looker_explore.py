# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .looker import Looker


class LookerExplore(Looker):
    """Description"""

    type_name: str = Field(default="LookerExplore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerExplore":
            raise ValueError("must be LookerExplore")
        return v

    def __setattr__(self, name, value):
        if name in LookerExplore._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECT_NAME: ClassVar[KeywordField] = KeywordField("projectName", "projectName")
    """
    Name of the parent project of this Explore.
    """
    MODEL_NAME: ClassVar[KeywordField] = KeywordField("modelName", "modelName")
    """
    Name of the parent model of this Explore.
    """
    SOURCE_CONNECTION_NAME: ClassVar[KeywordField] = KeywordField(
        "sourceConnectionName", "sourceConnectionName"
    )
    """
    Connection name for the Explore, from Looker.
    """
    VIEW_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "viewName", "viewName.keyword", "viewName"
    )
    """
    Name of the view for the Explore.
    """
    SQL_TABLE_NAME: ClassVar[KeywordField] = KeywordField(
        "sqlTableName", "sqlTableName"
    )
    """
    Name of the SQL table used to declare the Explore.
    """

    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    MODEL: ClassVar[RelationField] = RelationField("model")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "project_name",
        "model_name",
        "source_connection_name",
        "view_name",
        "sql_table_name",
        "project",
        "model",
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
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def source_connection_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.source_connection_name
        )

    @source_connection_name.setter
    def source_connection_name(self, source_connection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_connection_name = source_connection_name

    @property
    def view_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.view_name

    @view_name.setter
    def view_name(self, view_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view_name = view_name

    @property
    def sql_table_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql_table_name

    @sql_table_name.setter
    def sql_table_name(self, sql_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_table_name = sql_table_name

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

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
        model_name: Optional[str] = Field(default=None, description="")
        source_connection_name: Optional[str] = Field(default=None, description="")
        view_name: Optional[str] = Field(default=None, description="")
        sql_table_name: Optional[str] = Field(default=None, description="")
        project: Optional[LookerProject] = Field(
            default=None, description=""
        )  # relationship
        model: Optional[LookerModel] = Field(
            default=None, description=""
        )  # relationship
        fields: Optional[List[LookerField]] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerExplore.Attributes = Field(
        default_factory=lambda: LookerExplore.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_field import LookerField  # noqa
from .looker_model import LookerModel  # noqa
from .looker_project import LookerProject  # noqa
