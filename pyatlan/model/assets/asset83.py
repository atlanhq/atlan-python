# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar

from pydantic import Field, validator

from .asset80 import KafkaConsumerGroup


class AzureEventHubConsumerGroup(KafkaConsumerGroup):
    """Description"""

    type_name: str = Field("AzureEventHubConsumerGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AzureEventHubConsumerGroup":
            raise ValueError("must be AzureEventHubConsumerGroup")
        return v

    def __setattr__(self, name, value):
        if name in AzureEventHubConsumerGroup._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[list[str]] = []


AzureEventHubConsumerGroup.Attributes.update_forward_refs()
