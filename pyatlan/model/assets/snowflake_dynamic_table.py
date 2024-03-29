# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .table import Table


class SnowflakeDynamicTable(Table):
    """Description"""

    type_name: str = Field(default="SnowflakeDynamicTable", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SnowflakeDynamicTable":
            raise ValueError("must be SnowflakeDynamicTable")
        return v

    def __setattr__(self, name, value):
        if name in SnowflakeDynamicTable._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DEFINITION: ClassVar[KeywordField] = KeywordField("definition", "definition")
    """
    SQL statements used to define the dynamic table.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "definition",
    ]

    @property
    def definition(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.definition

    @definition.setter
    def definition(self, definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.definition = definition

    class Attributes(Table.Attributes):
        definition: Optional[str] = Field(default=None, description="")

    attributes: SnowflakeDynamicTable.Attributes = Field(
        default_factory=lambda: SnowflakeDynamicTable.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
