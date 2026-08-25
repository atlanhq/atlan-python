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


class V1CoalesceRun(V1Coalesce):
    """Description"""

    type_name: str = Field(default="V1CoalesceRun", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "V1CoalesceRun":
            raise ValueError("must be V1CoalesceRun")
        return v

    def __setattr__(self, name, value):
        if name in V1CoalesceRun._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_RUN_STATUS: ClassVar[KeywordField] = KeywordField(
        "coalesceRunStatus", "coalesceRunStatus"
    )
    """
    Status of this Coalesce run.
    """
    COALESCE_ENVIRONMENT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceEnvironmentQualifiedName",
        "coalesceEnvironmentQualifiedName.keyword",
        "coalesceEnvironmentQualifiedName",
    )
    """
    Qualified name of the Coalesce environment in which this run was executed.
    """

    V1COALESCE_ENVIRONMENT: ClassVar[RelationField] = RelationField(
        "v1CoalesceEnvironment"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "coalesce_run_status",
        "coalesce_environment_qualified_name",
        "v1_coalesce_environment",
    ]

    @property
    def coalesce_run_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.coalesce_run_status

    @coalesce_run_status.setter
    def coalesce_run_status(self, coalesce_run_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_run_status = coalesce_run_status

    @property
    def coalesce_environment_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.coalesce_environment_qualified_name
        )

    @coalesce_environment_qualified_name.setter
    def coalesce_environment_qualified_name(
        self, coalesce_environment_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_environment_qualified_name = (
            coalesce_environment_qualified_name
        )

    @property
    def v1_coalesce_environment(self) -> Optional[V1CoalesceEnvironment]:
        return (
            None if self.attributes is None else self.attributes.v1_coalesce_environment
        )

    @v1_coalesce_environment.setter
    def v1_coalesce_environment(
        self, v1_coalesce_environment: Optional[V1CoalesceEnvironment]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.v1_coalesce_environment = v1_coalesce_environment

    class Attributes(V1Coalesce.Attributes):
        coalesce_run_status: Optional[str] = Field(default=None, description="")
        coalesce_environment_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        v1_coalesce_environment: Optional[V1CoalesceEnvironment] = Field(
            default=None, description=""
        )  # relationship

    attributes: V1CoalesceRun.Attributes = Field(
        default_factory=lambda: V1CoalesceRun.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .v1_coalesce_environment import V1CoalesceEnvironment  # noqa: E402, F401

V1CoalesceRun.Attributes.update_forward_refs()
