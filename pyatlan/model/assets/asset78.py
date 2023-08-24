# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar

from pydantic import Field, validator

from .asset76 import KafkaTopic


class AzureEventHub(KafkaTopic):
    """Description"""

    type_name: str = Field("AzureEventHub", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AzureEventHub":
            raise ValueError("must be AzureEventHub")
        return v

    def __setattr__(self, name, value):
        if name in AzureEventHub._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = []


AzureEventHub.Attributes.update_forward_refs()
