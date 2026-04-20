# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from .context_studio import ContextStudio


class ContextFilter(ContextStudio):
    """Description"""

    type_name: str = Field(default="ContextFilter", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ContextFilter":
            raise ValueError("must be ContextFilter")
        return v

    def __setattr__(self, name, value):
        if name in ContextFilter._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []


ContextFilter.Attributes.update_forward_refs()
