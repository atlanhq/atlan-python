# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import TextField

from .catalog import Catalog


class NoSQL(Catalog):
    """Description"""

    type_name: str = Field(default="NoSQL", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "NoSQL":
            raise ValueError("must be NoSQL")
        return v

    def __setattr__(self, name, value):
        if name in NoSQL._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    NO_SQL_SCHEMA_DEFINITION: ClassVar[TextField] = TextField(
        "noSQLSchemaDefinition", "noSQLSchemaDefinition"
    )
    """
    Represents attributes for describing the key schema for the table and indexes.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "no_s_q_l_schema_definition",
    ]

    @property
    def no_s_q_l_schema_definition(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.no_s_q_l_schema_definition
        )

    @no_s_q_l_schema_definition.setter
    def no_s_q_l_schema_definition(self, no_s_q_l_schema_definition: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.no_s_q_l_schema_definition = no_s_q_l_schema_definition

    class Attributes(Catalog.Attributes):
        no_s_q_l_schema_definition: Optional[str] = Field(default=None, description="")

    attributes: NoSQL.Attributes = Field(
        default_factory=lambda: NoSQL.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
