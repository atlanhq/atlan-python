# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.utils import init_guid, validate_required_fields

from .anaplan import Anaplan


class AnaplanSystemDimension(Anaplan):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls, *, name: str, connection_qualified_name: str
    ) -> AnaplanSystemDimension:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = AnaplanSystemDimension.Attributes(
            name=name,
            qualified_name=f"{connection_qualified_name}/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=AtlanConnectorType.get_connector_name(
                connection_qualified_name
            ),
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="AnaplanSystemDimension", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AnaplanSystemDimension":
            raise ValueError("must be AnaplanSystemDimension")
        return v

    def __setattr__(self, name, value):
        if name in AnaplanSystemDimension._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []


AnaplanSystemDimension.Attributes.update_forward_refs()
