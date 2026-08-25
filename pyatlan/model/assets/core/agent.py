# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AgenticLifecycleStatus, AgentType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .agentic import Agentic


class Agent(Agentic):
    """Description"""

    type_name: str = Field(default="Agent", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Agent":
            raise ValueError("must be Agent")
        return v

    def __setattr__(self, name, value):
        if name in Agent._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AGENT_SLUG: ClassVar[KeywordField] = KeywordField("agentSlug", "agentSlug")
    """
    URL-safe unique identifier for this agent (for example, my-data-agent).
    """
    AGENT_TYPE: ClassVar[KeywordField] = KeywordField("agentType", "agentType")
    """
    Origin type of this agent — system-provided or custom user-created.
    """
    AGENT_STATUS: ClassVar[KeywordField] = KeywordField("agentStatus", "agentStatus")
    """
    Lifecycle status of this agent version (draft or published).
    """
    AGENT_SYSTEM_PROMPT: ClassVar[TextField] = TextField(
        "agentSystemPrompt", "agentSystemPrompt"
    )
    """
    System prompt for this agent version.
    """
    AGENT_LLM_CONFIG: ClassVar[KeywordField] = KeywordField(
        "agentLlmConfig", "agentLlmConfig"
    )
    """
    JSON-serialized LLMConfig (model, temperature, maxTokens, maxTurns, baseUrl).
    """
    AGENT_MCP_SERVERS: ClassVar[KeywordField] = KeywordField(
        "agentMcpServers", "agentMcpServers"
    )
    """
    JSON list of MCPServerConfig entries (name, url, headers, enabled).
    """
    AGENT_SCHEDULES: ClassVar[TextField] = TextField("agentSchedules", "agentSchedules")
    """
    JSON-serialized agent schedule configuration, including kickoff message, cron expression, timezone, version policy, status, and Temporal schedule identifier.
    """  # noqa: E501
    AGENT_SKILL_NAMES: ClassVar[KeywordField] = KeywordField(
        "agentSkillNames", "agentSkillNames"
    )
    """
    Denormalized list of names of the skills bound to this agent version.
    """
    AGENT_SKILL_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "agentSkillQualifiedNames", "agentSkillQualifiedNames"
    )
    """
    Denormalized list of qualifiedNames of the skills bound to this agent version.
    """

    AGENT_SKILLS: ClassVar[RelationField] = RelationField("agentSkills")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "agent_slug",
        "agent_type",
        "agent_status",
        "agent_system_prompt",
        "agent_llm_config",
        "agent_mcp_servers",
        "agent_schedules",
        "agent_skill_names",
        "agent_skill_qualified_names",
        "agent_skills",
    ]

    @property
    def agent_slug(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.agent_slug

    @agent_slug.setter
    def agent_slug(self, agent_slug: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_slug = agent_slug

    @property
    def agent_type(self) -> Optional[AgentType]:
        return None if self.attributes is None else self.attributes.agent_type

    @agent_type.setter
    def agent_type(self, agent_type: Optional[AgentType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_type = agent_type

    @property
    def agent_status(self) -> Optional[AgenticLifecycleStatus]:
        return None if self.attributes is None else self.attributes.agent_status

    @agent_status.setter
    def agent_status(self, agent_status: Optional[AgenticLifecycleStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_status = agent_status

    @property
    def agent_system_prompt(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.agent_system_prompt

    @agent_system_prompt.setter
    def agent_system_prompt(self, agent_system_prompt: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_system_prompt = agent_system_prompt

    @property
    def agent_llm_config(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.agent_llm_config

    @agent_llm_config.setter
    def agent_llm_config(self, agent_llm_config: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_llm_config = agent_llm_config

    @property
    def agent_mcp_servers(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.agent_mcp_servers

    @agent_mcp_servers.setter
    def agent_mcp_servers(self, agent_mcp_servers: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_mcp_servers = agent_mcp_servers

    @property
    def agent_schedules(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.agent_schedules

    @agent_schedules.setter
    def agent_schedules(self, agent_schedules: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_schedules = agent_schedules

    @property
    def agent_skill_names(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.agent_skill_names

    @agent_skill_names.setter
    def agent_skill_names(self, agent_skill_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_skill_names = agent_skill_names

    @property
    def agent_skill_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.agent_skill_qualified_names
        )

    @agent_skill_qualified_names.setter
    def agent_skill_qualified_names(
        self, agent_skill_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_skill_qualified_names = agent_skill_qualified_names

    @property
    def agent_skills(self) -> Optional[List[Skill]]:
        return None if self.attributes is None else self.attributes.agent_skills

    @agent_skills.setter
    def agent_skills(self, agent_skills: Optional[List[Skill]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.agent_skills = agent_skills

    class Attributes(Agentic.Attributes):
        agent_slug: Optional[str] = Field(default=None, description="")
        agent_type: Optional[AgentType] = Field(default=None, description="")
        agent_status: Optional[AgenticLifecycleStatus] = Field(
            default=None, description=""
        )
        agent_system_prompt: Optional[str] = Field(default=None, description="")
        agent_llm_config: Optional[str] = Field(default=None, description="")
        agent_mcp_servers: Optional[str] = Field(default=None, description="")
        agent_schedules: Optional[str] = Field(default=None, description="")
        agent_skill_names: Optional[Set[str]] = Field(default=None, description="")
        agent_skill_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        agent_skills: Optional[List[Skill]] = Field(
            default=None, description=""
        )  # relationship

    attributes: Agent.Attributes = Field(
        default_factory=lambda: Agent.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .skill import Skill  # noqa: E402, F401
