# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .core.custom import Custom


class CustomDataset(Custom):
    """Description"""

    type_name: str = Field(default="CustomDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CustomDataset":
            raise ValueError("must be CustomDataset")
        return v

    def __setattr__(self, name, value):
        if name in CustomDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    CUSTOM_TABLES: ClassVar[RelationField] = RelationField("customTables")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "custom_tables",
    ]

    @property
    def custom_tables(self) -> Optional[List[CustomTable]]:
        return None if self.attributes is None else self.attributes.custom_tables

    @custom_tables.setter
    def custom_tables(self, custom_tables: Optional[List[CustomTable]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.custom_tables = custom_tables

    class Attributes(Custom.Attributes):
        custom_tables: Optional[List[CustomTable]] = Field(
            default=None, description=""
        )  # relationship

    attributes: CustomDataset.Attributes = Field(
        default_factory=lambda: CustomDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .custom_table import CustomTable  # noqa

CustomDataset.Attributes.update_forward_refs()
