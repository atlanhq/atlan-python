# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

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

    CONTEXT_INPUT_ASSETS: ClassVar[RelationField] = RelationField("contextInputAssets")
    """
    TBC
    """
    CONTEXT_ARTIFACTS: ClassVar[RelationField] = RelationField("contextArtifacts")
    """
    TBC
    """
    CONTEXT_OUTPUT_SKILL: ClassVar[RelationField] = RelationField("contextOutputSkill")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "context_repository_lifecycle_status",
        "context_repository_agent_instructions",
        "context_repository_target_connection_qualified_name",
        "context_input_assets",
        "context_artifacts",
        "context_output_skill",
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
    def context_input_assets(self) -> Optional[List[Asset]]:
        return None if self.attributes is None else self.attributes.context_input_assets

    @context_input_assets.setter
    def context_input_assets(self, context_input_assets: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_input_assets = context_input_assets

    @property
    def context_artifacts(self) -> Optional[List[ContextArtifact]]:
        return None if self.attributes is None else self.attributes.context_artifacts

    @context_artifacts.setter
    def context_artifacts(self, context_artifacts: Optional[List[ContextArtifact]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_artifacts = context_artifacts

    @property
    def context_output_skill(self) -> Optional[Skill]:
        return None if self.attributes is None else self.attributes.context_output_skill

    @context_output_skill.setter
    def context_output_skill(self, context_output_skill: Optional[Skill]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.context_output_skill = context_output_skill

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
        context_input_assets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship
        context_artifacts: Optional[List[ContextArtifact]] = Field(
            default=None, description=""
        )  # relationship
        context_output_skill: Optional[Skill] = Field(
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


from .asset import Asset  # noqa: E402, F401
from .context_artifact import ContextArtifact  # noqa: E402, F401
from .skill import Skill  # noqa: E402, F401
