# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from nanoid import generate as generate_nanoid  # type: ignore
from pydantic.v1 import Field, validator

from pyatlan.model.enums import FileType
from pyatlan.model.fields.atlan_fields import RelationField
from pyatlan.utils import init_guid, validate_required_fields

from .artifact import Artifact


class SkillArtifact(Artifact):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls, *, name: str, skill_qualified_name: str, file_type: FileType
    ) -> SkillArtifact:
        validate_required_fields(
            ["name", "skill_qualified_name", "file_type"],
            [name, skill_qualified_name, file_type],
        )
        return SkillArtifact(
            attributes=SkillArtifact.Attributes.creator(
                name=name,
                skill_qualified_name=skill_qualified_name,
                file_type=file_type,
            )
        )

    type_name: str = Field(default="SkillArtifact", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SkillArtifact":
            raise ValueError("must be SkillArtifact")
        return v

    def __setattr__(self, name, value):
        if name in SkillArtifact._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SKILL_SOURCE: ClassVar[RelationField] = RelationField("skillSource")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "skill_source",
    ]

    @property
    def skill_source(self) -> Optional[Skill]:
        return None if self.attributes is None else self.attributes.skill_source

    @skill_source.setter
    def skill_source(self, skill_source: Optional[Skill]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_source = skill_source

    class Attributes(Artifact.Attributes):
        skill_source: Optional[Skill] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(
            cls, *, name: str, skill_qualified_name: str, file_type: FileType
        ) -> SkillArtifact.Attributes:
            validate_required_fields(
                ["name", "skill_qualified_name", "file_type"],
                [name, skill_qualified_name, file_type],
            )
            return SkillArtifact.Attributes(
                name=name,
                qualified_name=(
                    f"{skill_qualified_name}/artifact/{file_type.value}"
                    f"/{generate_nanoid()}"
                ),
                file_type=file_type,
                skill_source=Skill.ref_by_qualified_name(skill_qualified_name),
            )

    attributes: SkillArtifact.Attributes = Field(
        default_factory=lambda: SkillArtifact.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .skill import Skill  # noqa: E402, F401
