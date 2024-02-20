# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from .catalog import Catalog


class EventStore(Catalog):
    """Description"""

    type_name: str = Field(default="EventStore", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "EventStore":
            raise ValueError("must be EventStore")
        return v

    def __setattr__(self, name, value):
        if name in EventStore._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []
