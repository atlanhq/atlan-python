# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .model import Model


class ModelDataModel(Model):
    """Description"""

    type_name: str = Field(default="ModelDataModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ModelDataModel":
            raise ValueError("must be ModelDataModel")
        return v

    def __setattr__(self, name, value):
        if name in ModelDataModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MODEL_VERSION_COUNT: ClassVar[NumericField] = NumericField(
        "modelVersionCount", "modelVersionCount"
    )
    """
    Number of versions of the data model.
    """
    MODEL_TOOL: ClassVar[KeywordField] = KeywordField("modelTool", "modelTool")
    """
    Tool used to create this data model.
    """

    MODEL_VERSIONS: ClassVar[RelationField] = RelationField("modelVersions")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "model_version_count",
        "model_tool",
        "model_versions",
    ]

    @property
    def model_version_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.model_version_count

    @model_version_count.setter
    def model_version_count(self, model_version_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_version_count = model_version_count

    @property
    def model_tool(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.model_tool

    @model_tool.setter
    def model_tool(self, model_tool: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_tool = model_tool

    @property
    def model_versions(self) -> Optional[List[ModelVersion]]:
        return None if self.attributes is None else self.attributes.model_versions

    @model_versions.setter
    def model_versions(self, model_versions: Optional[List[ModelVersion]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_versions = model_versions

    class Attributes(Model.Attributes):
        model_version_count: Optional[int] = Field(default=None, description="")
        model_tool: Optional[str] = Field(default=None, description="")
        model_versions: Optional[List[ModelVersion]] = Field(
            default=None, description=""
        )  # relationship

    attributes: ModelDataModel.Attributes = Field(
        default_factory=lambda: ModelDataModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .model_version import ModelVersion  # noqa

ModelDataModel.Attributes.update_forward_refs()
