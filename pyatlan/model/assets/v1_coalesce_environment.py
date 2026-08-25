# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .v1_coalesce import V1Coalesce


class V1CoalesceEnvironment(V1Coalesce):
    """Description"""

    type_name: str = Field(default="V1CoalesceEnvironment", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "V1CoalesceEnvironment":
            raise ValueError("must be V1CoalesceEnvironment")
        return v

    def __setattr__(self, name, value):
        if name in V1CoalesceEnvironment._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_ENVIRONMENT_ID: ClassVar[KeywordField] = KeywordField(
        "coalesceEnvironmentId", "coalesceEnvironmentId"
    )
    """
    Unique identifier of this Coalesce environment.
    """
    COALESCE_SOURCE_DATABASE: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceSourceDatabase",
        "coalesceSourceDatabase.keyword",
        "coalesceSourceDatabase",
    )
    """
    Source database configured in this Coalesce environment's storage mapping.
    """
    COALESCE_SOURCE_SCHEMA: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceSourceSchema", "coalesceSourceSchema.keyword", "coalesceSourceSchema"
    )
    """
    Source schema configured in this Coalesce environment's storage mapping.
    """
    COALESCE_TARGET_DATABASE: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceTargetDatabase",
        "coalesceTargetDatabase.keyword",
        "coalesceTargetDatabase",
    )
    """
    Target database configured in this Coalesce environment's storage mapping.
    """
    COALESCE_TARGET_SCHEMA: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceTargetSchema", "coalesceTargetSchema.keyword", "coalesceTargetSchema"
    )
    """
    Target schema configured in this Coalesce environment's storage mapping.
    """

    V1COALESCE_NODES: ClassVar[RelationField] = RelationField("v1CoalesceNodes")
    """
    TBC
    """
    V1COALESCE_RUNS: ClassVar[RelationField] = RelationField("v1CoalesceRuns")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "coalesce_environment_id",
        "coalesce_source_database",
        "coalesce_source_schema",
        "coalesce_target_database",
        "coalesce_target_schema",
        "v1_coalesce_nodes",
        "v1_coalesce_runs",
    ]

    @property
    def coalesce_environment_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_environment_id
        )

    @coalesce_environment_id.setter
    def coalesce_environment_id(self, coalesce_environment_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_environment_id = coalesce_environment_id

    @property
    def coalesce_source_database(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.coalesce_source_database
        )

    @coalesce_source_database.setter
    def coalesce_source_database(self, coalesce_source_database: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_source_database = coalesce_source_database

    @property
    def coalesce_source_schema(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_source_schema
        )

    @coalesce_source_schema.setter
    def coalesce_source_schema(self, coalesce_source_schema: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_source_schema = coalesce_source_schema

    @property
    def coalesce_target_database(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.coalesce_target_database
        )

    @coalesce_target_database.setter
    def coalesce_target_database(self, coalesce_target_database: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_target_database = coalesce_target_database

    @property
    def coalesce_target_schema(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_target_schema
        )

    @coalesce_target_schema.setter
    def coalesce_target_schema(self, coalesce_target_schema: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_target_schema = coalesce_target_schema

    @property
    def v1_coalesce_nodes(self) -> Optional[List[V1CoalesceNode]]:
        return None if self.attributes is None else self.attributes.v1_coalesce_nodes

    @v1_coalesce_nodes.setter
    def v1_coalesce_nodes(self, v1_coalesce_nodes: Optional[List[V1CoalesceNode]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.v1_coalesce_nodes = v1_coalesce_nodes

    @property
    def v1_coalesce_runs(self) -> Optional[List[V1CoalesceRun]]:
        return None if self.attributes is None else self.attributes.v1_coalesce_runs

    @v1_coalesce_runs.setter
    def v1_coalesce_runs(self, v1_coalesce_runs: Optional[List[V1CoalesceRun]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.v1_coalesce_runs = v1_coalesce_runs

    class Attributes(V1Coalesce.Attributes):
        coalesce_environment_id: Optional[str] = Field(default=None, description="")
        coalesce_source_database: Optional[str] = Field(default=None, description="")
        coalesce_source_schema: Optional[str] = Field(default=None, description="")
        coalesce_target_database: Optional[str] = Field(default=None, description="")
        coalesce_target_schema: Optional[str] = Field(default=None, description="")
        v1_coalesce_nodes: Optional[List[V1CoalesceNode]] = Field(
            default=None, description=""
        )  # relationship
        v1_coalesce_runs: Optional[List[V1CoalesceRun]] = Field(
            default=None, description=""
        )  # relationship

    attributes: V1CoalesceEnvironment.Attributes = Field(
        default_factory=lambda: V1CoalesceEnvironment.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .v1_coalesce_node import V1CoalesceNode  # noqa: E402, F401
from .v1_coalesce_run import V1CoalesceRun  # noqa: E402, F401

V1CoalesceEnvironment.Attributes.update_forward_refs()
