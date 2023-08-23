# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar

from pydantic import Field, validator

from .asset00 import Asset


class ProcessExecution(Asset, type_name="ProcessExecution"):
    """Description"""

    type_name: str = Field("ProcessExecution", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ProcessExecution":
            raise ValueError("must be ProcessExecution")
        return v

    def __setattr__(self, name, value):
        if name in ProcessExecution._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = []


ProcessExecution.Attributes.update_forward_refs()
