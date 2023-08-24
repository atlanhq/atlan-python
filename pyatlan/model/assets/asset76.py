# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar

from pydantic import Field, field_validator

from .asset73 import QlikSpace


class QlikStream(QlikSpace):
    """Description"""

    type_name: str = Field("QlikStream", frozen=False)

    @field_validator("type_name")
    @classmethod
    def validate_type_name(cls, v):
        if v != "QlikStream":
            raise ValueError("must be QlikStream")
        return v

    def __setattr__(self, name, value):
        if name in QlikStream._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = []


QlikStream.Attributes.update_forward_refs()
