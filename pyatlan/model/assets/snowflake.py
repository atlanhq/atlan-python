# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from .core.s_q_l import SQL


class Snowflake(SQL):
    """Description"""

    type_name: str = Field(default="Snowflake", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Snowflake":
            raise ValueError("must be Snowflake")
        return v

    def __setattr__(self, name, value):
        if name in Snowflake._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []


Snowflake.Attributes.update_forward_refs()
