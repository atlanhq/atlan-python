# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .looker import Looker


class LookerField(Looker):
    """Description"""

    type_name: str = Field(default="LookerField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerField":
            raise ValueError("must be LookerField")
        return v

    def __setattr__(self, name, value):
        if name in LookerField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PROJECT_NAME: ClassVar[KeywordField] = KeywordField("projectName", "projectName")
    """
    Name of the project in which this field exists.
    """
    LOOKER_EXPLORE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "lookerExploreQualifiedName",
        "lookerExploreQualifiedName",
        "lookerExploreQualifiedName.text",
    )
    """
    Unique name of the Explore in which this field exists.
    """
    LOOKER_VIEW_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "lookerViewQualifiedName",
        "lookerViewQualifiedName",
        "lookerViewQualifiedName.text",
    )
    """
    Unique name of the view in which this field exists.
    """
    MODEL_NAME: ClassVar[KeywordField] = KeywordField("modelName", "modelName")
    """
    Name of the model in which this field exists.
    """
    SOURCE_DEFINITION: ClassVar[KeywordField] = KeywordField(
        "sourceDefinition", "sourceDefinition"
    )
    """
    Deprecated.
    """
    LOOKER_FIELD_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "lookerFieldDataType", "lookerFieldDataType"
    )
    """
    Deprecated.
    """
    LOOKER_TIMES_USED: ClassVar[NumericField] = NumericField(
        "lookerTimesUsed", "lookerTimesUsed"
    )
    """
    Deprecated.
    """

    EXPLORE: ClassVar[RelationField] = RelationField("explore")
    """
    TBC
    """
    PROJECT: ClassVar[RelationField] = RelationField("project")
    """
    TBC
    """
    VIEW: ClassVar[RelationField] = RelationField("view")
    """
    TBC
    """
    MODEL: ClassVar[RelationField] = RelationField("model")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "project_name",
        "looker_explore_qualified_name",
        "looker_view_qualified_name",
        "model_name",
        "source_definition",
        "looker_field_data_type",
        "looker_times_used",
        "explore",
        "project",
        "view",
        "model",
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
    def looker_explore_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.looker_explore_qualified_name
        )

    @looker_explore_qualified_name.setter
    def looker_explore_qualified_name(
        self, looker_explore_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_explore_qualified_name = looker_explore_qualified_name

    @property
    def looker_view_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.looker_view_qualified_name
        )

    @looker_view_qualified_name.setter
    def looker_view_qualified_name(self, looker_view_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_view_qualified_name = looker_view_qualified_name

    @property
    def model_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_name

    @model_name.setter
    def model_name(self, model_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_name = model_name

    @property
    def source_definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.source_definition

    @source_definition.setter
    def source_definition(self, source_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.source_definition = source_definition

    @property
    def looker_field_data_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.looker_field_data_type
        )

    @looker_field_data_type.setter
    def looker_field_data_type(self, looker_field_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_field_data_type = looker_field_data_type

    @property
    def looker_times_used(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.looker_times_used

    @looker_times_used.setter
    def looker_times_used(self, looker_times_used: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.looker_times_used = looker_times_used

    @property
    def explore(self) -> Optional[LookerExplore]:
        return None if self.attributes is None else self.attributes.explore

    @explore.setter
    def explore(self, explore: Optional[LookerExplore]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explore = explore

    @property
    def project(self) -> Optional[LookerProject]:
        return None if self.attributes is None else self.attributes.project

    @project.setter
    def project(self, project: Optional[LookerProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.project = project

    @property
    def view(self) -> Optional[LookerView]:
        return None if self.attributes is None else self.attributes.view

    @view.setter
    def view(self, view: Optional[LookerView]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.view = view

    @property
    def model(self) -> Optional[LookerModel]:
        return None if self.attributes is None else self.attributes.model

    @model.setter
    def model(self, model: Optional[LookerModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model = model

    class Attributes(Looker.Attributes):
        project_name: Optional[str] = Field(default=None, description="")
        looker_explore_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        looker_view_qualified_name: Optional[str] = Field(default=None, description="")
        model_name: Optional[str] = Field(default=None, description="")
        source_definition: Optional[str] = Field(default=None, description="")
        looker_field_data_type: Optional[str] = Field(default=None, description="")
        looker_times_used: Optional[int] = Field(default=None, description="")
        explore: Optional[LookerExplore] = Field(
            default=None, description=""
        )  # relationship
        project: Optional[LookerProject] = Field(
            default=None, description=""
        )  # relationship
        view: Optional[LookerView] = Field(default=None, description="")  # relationship
        model: Optional[LookerModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: LookerField.Attributes = Field(
        default_factory=lambda: LookerField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .looker_explore import LookerExplore  # noqa
from .looker_model import LookerModel  # noqa
from .looker_project import LookerProject  # noqa
from .looker_view import LookerView  # noqa
