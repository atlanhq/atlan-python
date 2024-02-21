# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .looker import Looker


class LookerProject(Looker):
    """Description"""

    type_name: str = Field(default="LookerProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "LookerProject":
            raise ValueError("must be LookerProject")
        return v

    def __setattr__(self, name, value):
        if name in LookerProject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODELS: ClassVar[RelationField] = RelationField("models")
    """
    TBC
    """
    EXPLORES: ClassVar[RelationField] = RelationField("explores")
    """
    TBC
    """
    FIELDS: ClassVar[RelationField] = RelationField("fields")
    """
    TBC
    """
    VIEWS: ClassVar[RelationField] = RelationField("views")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "models",
        "explores",
        "fields",
        "views",
    ]

    @property
    def models(self) -> Optional[List[LookerModel]]:
        return None if self.attributes is None else self.attributes.models

    @models.setter
    def models(self, models: Optional[List[LookerModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.models = models

    @property
    def explores(self) -> Optional[List[LookerExplore]]:
        return None if self.attributes is None else self.attributes.explores

    @explores.setter
    def explores(self, explores: Optional[List[LookerExplore]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.explores = explores

    @property
    def fields(self) -> Optional[List[LookerField]]:
        return None if self.attributes is None else self.attributes.fields

    @fields.setter
    def fields(self, fields: Optional[List[LookerField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fields = fields

    @property
    def views(self) -> Optional[List[LookerView]]:
        return None if self.attributes is None else self.attributes.views

    @views.setter
    def views(self, views: Optional[List[LookerView]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.views = views

    class Attributes(Looker.Attributes):
        models: Optional[List[LookerModel]] = Field(
            default=None, description=""
        )  # relationship
        explores: Optional[List[LookerExplore]] = Field(
            default=None, description=""
        )  # relationship
        fields: Optional[List[LookerField]] = Field(
            default=None, description=""
        )  # relationship
        views: Optional[List[LookerView]] = Field(
            default=None, description=""
        )  # relationship

    attributes: "LookerProject.Attributes" = Field(
        default_factory=lambda: LookerProject.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


from .looker_explore import LookerExplore  # noqa
from .looker_field import LookerField  # noqa
from .looker_model import LookerModel  # noqa
from .looker_view import LookerView  # noqa
