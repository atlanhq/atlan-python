# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AIModelStatus
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .a_i import AI


class AIModel(AI):
    """Description"""

    type_name: str = Field(default="AIModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AIModel":
            raise ValueError("must be AIModel")
        return v

    def __setattr__(self, name, value):
        if name in AIModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AI_MODEL_DATASETS_DSL: ClassVar[TextField] = TextField(
        "aiModelDatasetsDSL", "aiModelDatasetsDSL"
    )
    """
    Search DSL used to define which assets/datasets are part of the AI model.
    """
    AI_MODEL_STATUS: ClassVar[KeywordField] = KeywordField(
        "aiModelStatus", "aiModelStatus"
    )
    """
    Status of the AI model
    """
    AI_MODEL_VERSION: ClassVar[KeywordField] = KeywordField(
        "aiModelVersion", "aiModelVersion"
    )
    """
    Version of the AI model
    """

    APPLICATIONS: ClassVar[RelationField] = RelationField("applications")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ai_model_datasets_d_s_l",
        "ai_model_status",
        "ai_model_version",
        "applications",
    ]

    @property
    def ai_model_datasets_d_s_l(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ai_model_datasets_d_s_l
        )

    @ai_model_datasets_d_s_l.setter
    def ai_model_datasets_d_s_l(self, ai_model_datasets_d_s_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_datasets_d_s_l = ai_model_datasets_d_s_l

    @property
    def ai_model_status(self) -> Optional[AIModelStatus]:
        return None if self.attributes is None else self.attributes.ai_model_status

    @ai_model_status.setter
    def ai_model_status(self, ai_model_status: Optional[AIModelStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_status = ai_model_status

    @property
    def ai_model_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ai_model_version

    @ai_model_version.setter
    def ai_model_version(self, ai_model_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_version = ai_model_version

    @property
    def applications(self) -> Optional[List[AIApplication]]:
        return None if self.attributes is None else self.attributes.applications

    @applications.setter
    def applications(self, applications: Optional[List[AIApplication]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.applications = applications

    class Attributes(AI.Attributes):
        ai_model_datasets_d_s_l: Optional[str] = Field(default=None, description="")
        ai_model_status: Optional[AIModelStatus] = Field(default=None, description="")
        ai_model_version: Optional[str] = Field(default=None, description="")
        applications: Optional[List[AIApplication]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AIModel.Attributes = Field(
        default_factory=lambda: AIModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_i_application import AIApplication  # noqa: E402, F401

AIModel.Attributes.update_forward_refs()
