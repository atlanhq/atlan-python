# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from nanoid import generate as generate_nanoid  # type: ignore
from pydantic.v1 import Field, validator

from pyatlan.model.enums import ContextLifecycleStatus
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField
from pyatlan.utils import init_guid, validate_required_fields

from .context import Context


class ContextRepository(Context):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str) -> ContextRepository:
        validate_required_fields(["name"], [name])
        return ContextRepository(
            attributes=ContextRepository.Attributes.creator(name=name)
        )

    type_name: str = Field(default="ContextRepository", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ContextRepository":
            raise ValueError("must be ContextRepository")
        return v

    def __setattr__(self, name, value):
        if name in ContextRepository._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CONTEXT_REPOSITORY_LIFECYCLE_STATUS: ClassVar[KeywordField] = KeywordField(
        "contextRepositoryLifecycleStatus", "contextRepositoryLifecycleStatus"
    )
    """
    Lifecycle status of the context repository.
    """
    CONTEXT_REPOSITORY_AGENT_INSTRUCTIONS: ClassVar[TextField] = TextField(
        "contextRepositoryAgentInstructions", "contextRepositoryAgentInstructions"
    )
    """
    LLM guidance and constraints for NL2SQL generation using this repository's context.
    """
    CONTEXT_REPOSITORY_TARGET_CONNECTION_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "contextRepositoryTargetConnectionQualifiedName",
            "contextRepositoryTargetConnectionQualifiedName",
        )
    )
    """
    Qualified name of the connection used as the execution engine for deploying and running queries against this repository.
    """  # noqa: E501
    CONTEXT_REPOSITORY_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "contextRepositoryQualifiedName", "contextRepositoryQualifiedName"
    )
    """
    Qualified name of the context repository to which this asset belongs.
    """
    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
    """
    SKILL_VERSION: ClassVar[KeywordField] = KeywordField("skillVersion", "skillVersion")
    """
    Version identifier for this skill.
    """
    CONTEXT_REPOSITORY_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "contextRepositoryQualifiedNames", "contextRepositoryQualifiedNames"
    )
    """
    Qualified names of the context repositories to which this asset belongs.
    """

    CONTEXT_ARTIFACTS: ClassVar[RelationField] = RelationField("contextArtifacts")
    """
    TBC
    """
    SKILL_ARTIFACTS: ClassVar[RelationField] = RelationField("skillArtifacts")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "context_repository_lifecycle_status",
        "context_repository_agent_instructions",
        "context_repository_target_connection_qualified_name",
        "context_repository_qualified_name",
        "catalog_dataset_guid",
        "skill_version",
        "context_repository_qualified_names",
        "context_artifacts",
        "skill_artifacts",
    ]

    @property
    def context_repository_lifecycle_status(self) -> Optional[ContextLifecycleStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_repository_lifecycle_status
        )

    @context_repository_lifecycle_status.setter
    def context_repository_lifecycle_status(
        self, context_repository_lifecycle_status: Optional[ContextLifecycleStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_repository_lifecycle_status = (
            context_repository_lifecycle_status
        )

    @property
    def context_repository_agent_instructions(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_repository_agent_instructions
        )

    @context_repository_agent_instructions.setter
    def context_repository_agent_instructions(
        self, context_repository_agent_instructions: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_repository_agent_instructions = (
            context_repository_agent_instructions
        )

    @property
    def context_repository_target_connection_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_repository_target_connection_qualified_name
        )

    @context_repository_target_connection_qualified_name.setter
    def context_repository_target_connection_qualified_name(
        self, context_repository_target_connection_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_repository_target_connection_qualified_name = (
            context_repository_target_connection_qualified_name
        )

    @property
    def context_repository_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_repository_qualified_name
        )

    @context_repository_qualified_name.setter
    def context_repository_qualified_name(
        self, context_repository_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_repository_qualified_name = (
            context_repository_qualified_name
        )

    @property
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

    @property
    def skill_version(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.skill_version

    @skill_version.setter
    def skill_version(self, skill_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_version = skill_version

    @property
    def context_repository_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.context_repository_qualified_names
        )

    @context_repository_qualified_names.setter
    def context_repository_qualified_names(
        self, context_repository_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_repository_qualified_names = (
            context_repository_qualified_names
        )

    @property
    def context_artifacts(self) -> Optional[List[ContextArtifact]]:
        return None if self.attributes is None else self.attributes.context_artifacts

    @context_artifacts.setter
    def context_artifacts(self, context_artifacts: Optional[List[ContextArtifact]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_artifacts = context_artifacts

    @property
    def skill_artifacts(self) -> Optional[List[SkillArtifact]]:
        return None if self.attributes is None else self.attributes.skill_artifacts

    @skill_artifacts.setter
    def skill_artifacts(self, skill_artifacts: Optional[List[SkillArtifact]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.skill_artifacts = skill_artifacts

    class Attributes(Context.Attributes):
        context_repository_lifecycle_status: Optional[ContextLifecycleStatus] = Field(
            default=None, description=""
        )
        context_repository_agent_instructions: Optional[str] = Field(
            default=None, description=""
        )
        context_repository_target_connection_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        context_repository_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
        skill_version: Optional[str] = Field(default=None, description="")
        context_repository_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        context_artifacts: Optional[List[ContextArtifact]] = Field(
            default=None, description=""
        )  # relationship
        skill_artifacts: Optional[List[SkillArtifact]] = Field(
            default=None, description=""
        )  # relationship

        @classmethod
        @init_guid
        def creator(cls, *, name: str) -> ContextRepository.Attributes:
            validate_required_fields(["name"], [name])
            return ContextRepository.Attributes(
                name=name,
                qualified_name=f"default/context/{generate_nanoid()}",
            )

    attributes: ContextRepository.Attributes = Field(
        default_factory=lambda: ContextRepository.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .context_artifact import ContextArtifact  # noqa: E402, F401
from .skill_artifact import SkillArtifact  # noqa: E402, F401
