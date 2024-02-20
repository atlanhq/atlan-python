# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from .event_store import EventStore


class Kafka(EventStore):
    """Description"""

    type_name: str = Field(default="Kafka", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Kafka":
            raise ValueError("must be Kafka")
        return v

    def __setattr__(self, name, value):
        if name in Kafka._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []
