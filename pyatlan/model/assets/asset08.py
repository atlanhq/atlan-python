# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar

from pydantic import Field, field_validator

from .asset00 import Asset


class Cloud(Asset, type_name="Cloud"):
    """Description"""

    type_name: str = Field("Cloud", frozen=False)

    @field_validator("type_name")
    @classmethod
    def validate_type_name(cls, v):
        if v != "Cloud":
            raise ValueError("must be Cloud")
        return v

    def __setattr__(self, name, value):
        if name in Cloud._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = []
