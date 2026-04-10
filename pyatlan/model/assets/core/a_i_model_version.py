# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AIModelVersionStage
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .a_i import AI


class AIModelVersion(AI):
    """Description"""

    type_name: str = Field(default="AIModelVersion", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AIModelVersion":
            raise ValueError("must be AIModelVersion")
        return v

    def __setattr__(self, name, value):
        if name in AIModelVersion._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AI_MODEL_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "aiModelQualifiedName", "aiModelQualifiedName"
    )
    """
    Unique name of the AI model to which this version belongs, used to navigate from a version back to its parent model.
    """
    AI_MODEL_VERSION_STAGE: ClassVar[KeywordField] = KeywordField(
        "aiModelVersionStage", "aiModelVersionStage"
    )
    """
    Lifecycle deployment stage of this AI model version, indicating its readiness for production use.
    """
    AI_MODEL_VERSION_METRICS: ClassVar[KeywordField] = KeywordField(
        "aiModelVersionMetrics", "aiModelVersionMetrics"
    )
    """
    Evaluation and performance metrics recorded for this AI model version, stored as key-value pairs (e.g. accuracy, F1 score, precision, recall).
    """  # noqa: E501

    AI_MODEL: ClassVar[RelationField] = RelationField("aiModel")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ai_model_qualified_name",
        "ai_model_version_stage",
        "ai_model_version_metrics",
        "ai_model",
    ]

    @property
    def ai_model_qualified_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.ai_model_qualified_name
        )

    @ai_model_qualified_name.setter
    def ai_model_qualified_name(self, ai_model_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_qualified_name = ai_model_qualified_name

    @property
    def ai_model_version_stage(self) -> Optional[AIModelVersionStage]:
        return (
            None if self.attributes is None else self.attributes.ai_model_version_stage
        )

    @ai_model_version_stage.setter
    def ai_model_version_stage(
        self, ai_model_version_stage: Optional[AIModelVersionStage]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_version_stage = ai_model_version_stage

    @property
    def ai_model_version_metrics(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.ai_model_version_metrics
        )

    @ai_model_version_metrics.setter
    def ai_model_version_metrics(
        self, ai_model_version_metrics: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model_version_metrics = ai_model_version_metrics

    @property
    def ai_model(self) -> Optional[AIModel]:
        return None if self.attributes is None else self.attributes.ai_model

    @ai_model.setter
    def ai_model(self, ai_model: Optional[AIModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model = ai_model

    class Attributes(AI.Attributes):
        ai_model_qualified_name: Optional[str] = Field(default=None, description="")
        ai_model_version_stage: Optional[AIModelVersionStage] = Field(
            default=None, description=""
        )
        ai_model_version_metrics: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        ai_model: Optional[AIModel] = Field(
            default=None, description=""
        )  # relationship

    attributes: AIModelVersion.Attributes = Field(
        default_factory=lambda: AIModelVersion.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .a_i_model import AIModel  # noqa: E402, F401
