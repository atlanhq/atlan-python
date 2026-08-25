# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import TextField

from .coalesce import Coalesce


class CoalesceRun(Coalesce):
    """Description"""

    type_name: str = Field(default="CoalesceRun", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CoalesceRun":
            raise ValueError("must be CoalesceRun")
        return v

    def __setattr__(self, name, value):
        if name in CoalesceRun._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_RUN_STATUS: ClassVar[TextField] = TextField(
        "coalesceRunStatus", "coalesceRunStatus"
    )
    """
    TBC
    """
    COALESCE_ENVIRONMENT_QUALIFIED_NAME: ClassVar[TextField] = TextField(
        "coalesceEnvironmentQualifiedName", "coalesceEnvironmentQualifiedName"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "coalesce_run_status",
        "coalesce_environment_qualified_name",
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

    class Attributes(Coalesce.Attributes):
        coalesce_run_status: Optional[str] = Field(default=None, description="")
        coalesce_environment_qualified_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: CoalesceRun.Attributes = Field(
        default_factory=lambda: CoalesceRun.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


CoalesceRun.Attributes.update_forward_refs()
