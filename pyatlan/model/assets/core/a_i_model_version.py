# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

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

    AI_MODEL: ClassVar[RelationField] = RelationField("aiModel")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "ai_model",
    ]

    @property
    def ai_model(self) -> Optional[AIModel]:
        return None if self.attributes is None else self.attributes.ai_model

    @ai_model.setter
    def ai_model(self, ai_model: Optional[AIModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_model = ai_model

    class Attributes(AI.Attributes):
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
