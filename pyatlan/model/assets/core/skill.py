# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from nanoid import generate as generate_nanoid  # type: ignore
from pydantic.v1 import Field, validator

from pyatlan.model.enums import AgenticLifecycleStatus, SkillType
from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField
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
    String version identifier for this skill. Will be superseded by agenticVersion (long, epoch-ms) on the Agentic supertype in a future release; continue using this for now.
    """  # noqa: E501
    SKILL_SLUG: ClassVar[KeywordField] = KeywordField("skillSlug", "skillSlug")
    """
    URL-safe unique identifier for this skill (for example, my-sql-skill).
    """
    SKILL_TYPE: ClassVar[KeywordField] = KeywordField("skillType", "skillType")
    """
    Origin type of this skill — system-provided, context repository output, custom user/agent created, or connector-synced from an external system.
    """  # noqa: E501
    SKILL_STATUS: ClassVar[KeywordField] = KeywordField("skillStatus", "skillStatus")
    """
    Lifecycle status of this skill version (draft or published).
    """
    SKILL_ARTIFACT_PATHS: ClassVar[KeywordField] = KeywordField(
        "skillArtifactPaths", "skillArtifactPaths"
    )
    """
    Denormalized list of file paths of the SkillArtifact entities belonging to this skill version.
    """
    SKILL_ARTIFACT_FILE_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "skillArtifactFileQualifiedNames", "skillArtifactFileQualifiedNames"
    )
    """
    Denormalized list of qualifiedNames of the SkillArtifact entities belonging to this skill version.
    """
    SKILL_IS_DORMANT: ClassVar[BooleanField] = BooleanField(
        "skillIsDormant", "skillIsDormant"
    )
    """
    Health signal — true when the skill was discovered with a missing, empty, or insufficiently descriptive description and is surfaced for governance review. Orthogonal to status: a published skill can also be dormant.
    """  # noqa: E501
    SKILL_SOURCE_PATH: ClassVar[KeywordField] = KeywordField(
        "skillSourcePath", "skillSourcePath"
    )
    """
    Source-system path the skill was synced from (for example, the Databricks workspace SKILL.md path).
    """
    SKILL_SCOPE: ClassVar[KeywordField] = KeywordField("skillScope", "skillScope")
    """
    Scope under which the skill was discovered, as a keyword string (for example, user or workspace).
    """
    SKILL_CHECKSUM: ClassVar[KeywordField] = KeywordField(
        "skillChecksum", "skillChecksum"
    )
    """
    SHA-256 hex digest of the source SKILL.md content (UTF-8), used for change detection across crawls.
    """

    CONTEXT_SOURCE_REPOSITORY: ClassVar[RelationField] = RelationField(
        "contextSourceRepository"
    )
    """
    TBC
    """
    SKILL_ARTIFACTS: ClassVar[RelationField] = RelationField("skillArtifacts")
    """
    TBC
    """
    AGENT_AGENTS: ClassVar[RelationField] = RelationField("agentAgents")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "skill_version",
        "skill_slug",
        "skill_type",
        "skill_status",
        "skill_artifact_paths",
        "skill_artifact_file_qualified_names",
        "skill_is_dormant",
        "skill_source_path",
        "skill_scope",
        "skill_checksum",
        "context_source_repository",
        "skill_artifacts",
        "agent_agents",
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
    def skill_slug(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.skill_slug

    @skill_slug.setter
    def skill_slug(self, skill_slug: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_slug = skill_slug

    @property
    def skill_type(self) -> Optional[SkillType]:
        return None if self.attributes is None else self.attributes.skill_type

    @skill_type.setter
    def skill_type(self, skill_type: Optional[SkillType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_type = skill_type

    @property
    def skill_status(self) -> Optional[AgenticLifecycleStatus]:
        return None if self.attributes is None else self.attributes.skill_status

    @skill_status.setter
    def skill_status(self, skill_status: Optional[AgenticLifecycleStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_status = skill_status

    @property
    def skill_artifact_paths(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.skill_artifact_paths

    @skill_artifact_paths.setter
    def skill_artifact_paths(self, skill_artifact_paths: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_artifact_paths = skill_artifact_paths

    @property
    def skill_artifact_file_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.skill_artifact_file_qualified_names
        )

    @skill_artifact_file_qualified_names.setter
    def skill_artifact_file_qualified_names(
        self, skill_artifact_file_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_artifact_file_qualified_names = (
            skill_artifact_file_qualified_names
        )

    @property
    def skill_is_dormant(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.skill_is_dormant

    @skill_is_dormant.setter
    def skill_is_dormant(self, skill_is_dormant: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_is_dormant = skill_is_dormant

    @property
    def skill_source_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.skill_source_path

    @skill_source_path.setter
    def skill_source_path(self, skill_source_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_source_path = skill_source_path

    @property
    def skill_scope(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.skill_scope

    @skill_scope.setter
    def skill_scope(self, skill_scope: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_scope = skill_scope

    @property
    def skill_checksum(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.skill_checksum

    @skill_checksum.setter
    def skill_checksum(self, skill_checksum: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_checksum = skill_checksum

    @property
    def context_source_repository(self) -> Optional[ContextRepository]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_source_repository
        )

    @context_source_repository.setter
    def context_source_repository(
        self, context_source_repository: Optional[ContextRepository]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_source_repository = context_source_repository

    @property
    def skill_artifacts(self) -> Optional[List[SkillArtifact]]:
        return None if self.attributes is None else self.attributes.skill_artifacts

    @skill_artifacts.setter
    def skill_artifacts(self, skill_artifacts: Optional[List[SkillArtifact]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_artifacts = skill_artifacts

    @property
    def agent_agents(self) -> Optional[List[Agent]]:
        return None if self.attributes is None else self.attributes.agent_agents

    @agent_agents.setter
    def agent_agents(self, agent_agents: Optional[List[Agent]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_agents = agent_agents

    class Attributes(Agentic.Attributes):
        skill_version: Optional[str] = Field(default=None, description="")
        skill_slug: Optional[str] = Field(default=None, description="")
        skill_type: Optional[SkillType] = Field(default=None, description="")
        skill_status: Optional[AgenticLifecycleStatus] = Field(
            default=None, description=""
        )
        skill_artifact_paths: Optional[Set[str]] = Field(default=None, description="")
        skill_artifact_file_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        skill_is_dormant: Optional[bool] = Field(default=None, description="")
        skill_source_path: Optional[str] = Field(default=None, description="")
        skill_scope: Optional[str] = Field(default=None, description="")
        skill_checksum: Optional[str] = Field(default=None, description="")
        context_source_repository: Optional[ContextRepository] = Field(
            default=None, description=""
        )  # relationship
        skill_artifacts: Optional[List[SkillArtifact]] = Field(
            default=None, description=""
        )  # relationship
        agent_agents: Optional[List[Agent]] = Field(
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


from .agent import Agent  # noqa: E402, F401
from .context_repository import ContextRepository  # noqa: E402, F401
from .skill_artifact import SkillArtifact  # noqa: E402, F401
