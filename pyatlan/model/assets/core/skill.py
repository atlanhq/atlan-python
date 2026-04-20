# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from nanoid import generate as generate_nanoid  # type: ignore
from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .agentic import Agentic


class Skill(Agentic):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str) -> Skill:
        validate_required_fields(["name"], [name])
        return Skill(attributes=Skill.Attributes.creator(name=name))

    type_name: str = Field(default="Skill", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Skill":
            raise ValueError("must be Skill")
        return v

    def __setattr__(self, name, value):
        if name in Skill._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SKILL_VERSION: ClassVar[KeywordField] = KeywordField("skillVersion", "skillVersion")
    """
    Version identifier for this skill.
    """

    SKILL_ARTIFACTS: ClassVar[RelationField] = RelationField("skillArtifacts")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "skill_version",
        "skill_artifacts",
    ]

    @property
    def skill_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.skill_version

    @skill_version.setter
    def skill_version(self, skill_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_version = skill_version

    @property
    def skill_artifacts(self) -> Optional[List[SkillArtifact]]:
        return None if self.attributes is None else self.attributes.skill_artifacts

    @skill_artifacts.setter
    def skill_artifacts(self, skill_artifacts: Optional[List[SkillArtifact]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_artifacts = skill_artifacts

    class Attributes(Agentic.Attributes):
        skill_version: Optional[str] = Field(default=None, description="")
        skill_artifacts: Optional[List[SkillArtifact]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(cls, *, name: str) -> Skill.Attributes:
            validate_required_fields(["name"], [name])
            return Skill.Attributes(
                name=name,
                qualified_name=f"default/skill/{generate_nanoid()}",
            )

    attributes: Skill.Attributes = Field(
        default_factory=lambda: Skill.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .skill_artifact import SkillArtifact  # noqa: E402, F401
