# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, field_validator

from pyatlan.model.enums import (
    PowerbiEndorsement,
)
from .asset18 import BI


class PowerBI(BI):
    """Description"""

    type_name: str = Field("PowerBI", frozen=False)

    @field_validator("type_name")
    @classmethod
    def validate_type_name(cls, v):
        if v != "PowerBI":
            raise ValueError("must be PowerBI")
        return v

    def __setattr__(self, name, value):
        if name in PowerBI._convience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convience_properties: ClassVar[list[str]] = [
        "power_b_i_is_hidden",
        "power_b_i_table_qualified_name",
        "power_b_i_format_string",
        "power_b_i_endorsement",
    ]

    @property
    def power_b_i_is_hidden(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.power_b_i_is_hidden

    @power_b_i_is_hidden.setter
    def power_b_i_is_hidden(self, power_b_i_is_hidden: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_is_hidden = power_b_i_is_hidden

    @property
    def power_b_i_table_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.power_b_i_table_qualified_name
        )

    @power_b_i_table_qualified_name.setter
    def power_b_i_table_qualified_name(
        self, power_b_i_table_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_table_qualified_name = power_b_i_table_qualified_name

    @property
    def power_b_i_format_string(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.power_b_i_format_string
        )

    @power_b_i_format_string.setter
    def power_b_i_format_string(self, power_b_i_format_string: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_format_string = power_b_i_format_string

    @property
    def power_b_i_endorsement(self) -> Optional[PowerbiEndorsement]:
        return (
            None if self.attributes is None else self.attributes.power_b_i_endorsement
        )

    @power_b_i_endorsement.setter
    def power_b_i_endorsement(
        self, power_b_i_endorsement: Optional[PowerbiEndorsement]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_endorsement = power_b_i_endorsement

    class Attributes(BI.Attributes):
        power_b_i_is_hidden: Optional[bool] = Field(
            default=None, description="", alias="powerBIIsHidden"
        )

        power_b_i_table_qualified_name: Optional[str] = Field(
            default=None, description="", alias="powerBITableQualifiedName"
        )

        power_b_i_format_string: Optional[str] = Field(
            default=None, description="", alias="powerBIFormatString"
        )

        power_b_i_endorsement: Optional[PowerbiEndorsement] = Field(
            default=None, description="", alias="powerBIEndorsement"
        )

    attributes: "PowerBI.Attributes" = Field(
        default_factory=lambda: PowerBI.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


PowerBI.Attributes.update_forward_refs()
