# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar

from pydantic import Field, validator

from .asset18 import BI


class Tableau(BI):
    """Description"""

    type_name: str = Field("Tableau", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Tableau":
            raise ValueError("must be Tableau")
        return v

    def __setattr__(self, name, value):
        if name in Tableau._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = []


Tableau.Attributes.update_forward_refs()
