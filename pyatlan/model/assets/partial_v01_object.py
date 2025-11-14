# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from .core.partial_v01 import PartialV01


class PartialV01Object(PartialV01):
    """Description"""

    type_name: str = Field(default="PartialV01Object", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PartialV01Object":
            raise ValueError("must be PartialV01Object")
        return v

    def __setattr__(self, name, value):
        if name in PartialV01Object._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []


PartialV01Object.Attributes.update_forward_refs()
