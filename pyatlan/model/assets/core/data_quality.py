# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField

from .catalog import Catalog


class DataQuality(Catalog):
    """Description"""

    type_name: str = Field(default="DataQuality", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataQuality":
            raise ValueError("must be DataQuality")
        return v

    def __setattr__(self, name, value):
        if name in DataQuality._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DQ_IS_PART_OF_CONTRACT: ClassVar[BooleanField] = BooleanField(
        "dqIsPartOfContract", "dqIsPartOfContract"
    )
    """
    Whether this data quality is part of contract (true) or not (false).
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dq_is_part_of_contract",
    ]

    @property
    def dq_is_part_of_contract(self) -> Optional[bool]:
        return (
            None if self.attributes is None else self.attributes.dq_is_part_of_contract
        )

    @dq_is_part_of_contract.setter
    def dq_is_part_of_contract(self, dq_is_part_of_contract: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_is_part_of_contract = dq_is_part_of_contract

    class Attributes(Catalog.Attributes):
        dq_is_part_of_contract: Optional[bool] = Field(default=None, description="")

    attributes: DataQuality.Attributes = Field(
        default_factory=lambda: DataQuality.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
