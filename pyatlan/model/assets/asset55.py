# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar

from pydantic import Field, validator

from .asset22 import NoSQL


class MongoDB(NoSQL):
    """Description"""

    type_name: str = Field("MongoDB", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MongoDB":
            raise ValueError("must be MongoDB")
        return v

    def __setattr__(self, name, value):
        if name in MongoDB._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = []


MongoDB.Attributes.update_forward_refs()
