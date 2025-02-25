# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AIApplicationDevelopmentStage
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .a_i import AI


class AIApplication(AI):
    """Description"""

    type_name: str = Field(default="AIApplication", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AIApplication":
            raise ValueError("must be AIApplication")
        return v

    def __setattr__(self, name, value):
        if name in AIApplication._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AI_APPLICATION_VERSION: ClassVar[KeywordField] = KeywordField(
        "aiApplicationVersion", "aiApplicationVersion"
    )
    """
    Version of the AI application
    """
    AI_APPLICATION_DEVELOPMENT_STAGE: ClassVar[KeywordField] = KeywordField(
        "aiApplicationDevelopmentStage", "aiApplicationDevelopmentStage"
    )
    """
    Development stage of the AI application
    """

    MODELS: ClassVar[RelationField] = RelationField("models")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ai_application_version",
        "ai_application_development_stage",
        "models",
    ]

    @property
    def ai_application_version(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ai_application_version
        )

    @ai_application_version.setter
    def ai_application_version(self, ai_application_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_application_version = ai_application_version

    @property
    def ai_application_development_stage(
        self,
    ) -> Optional[AIApplicationDevelopmentStage]:
        return (
            None
            if self.attributes is None
            else self.attributes.ai_application_development_stage
        )

    @ai_application_development_stage.setter
    def ai_application_development_stage(
        self, ai_application_development_stage: Optional[AIApplicationDevelopmentStage]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_application_development_stage = (
            ai_application_development_stage
        )

    @property
    def models(self) -> Optional[List[AIModel]]:
        return None if self.attributes is None else self.attributes.models

    @models.setter
    def models(self, models: Optional[List[AIModel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.models = models

    class Attributes(AI.Attributes):
        ai_application_version: Optional[str] = Field(default=None, description="")
        ai_application_development_stage: Optional[AIApplicationDevelopmentStage] = (
            Field(default=None, description="")
        )
        models: Optional[List[AIModel]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AIApplication.Attributes = Field(
        default_factory=lambda: AIApplication.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_i_model import AIModel  # noqa: E402, F401

AIApplication.Attributes.update_forward_refs()
