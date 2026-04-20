# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from .context_studio import ContextStudio


class ContextMetric(ContextStudio):
    """Description"""

    type_name: str = Field(default="ContextMetric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ContextMetric":
            raise ValueError("must be ContextMetric")
        return v

    def __setattr__(self, name, value):
        if name in ContextMetric._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []


ContextMetric.Attributes.update_forward_refs()
