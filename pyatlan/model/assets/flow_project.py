# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from .core.flow import Flow


class FlowProject(Flow):
    """Description"""

    type_name: str = Field(default="FlowProject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "FlowProject":
            raise ValueError("must be FlowProject")
        return v

    def __setattr__(self, name, value):
        if name in FlowProject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []


FlowProject.Attributes.update_forward_refs()
