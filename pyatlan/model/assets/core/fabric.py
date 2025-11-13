# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .b_i import BI


class Fabric(BI):
    """Description"""

    type_name: str = Field(default="Fabric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Fabric":
            raise ValueError("must be Fabric")
        return v

    def __setattr__(self, name, value):
        if name in Fabric._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    FABRIC_COLUMN_COUNT: ClassVar[NumericField] = NumericField(
        "fabricColumnCount", "fabricColumnCount"
    )
    """
    Number of columns in this asset.
    """
    FABRIC_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "fabricDataType", "fabricDataType"
    )
    """
    Data type of this asset.
    """
    FABRIC_ORDINAL: ClassVar[NumericField] = NumericField(
        "fabricOrdinal", "fabricOrdinal"
    )
    """
    Order/position of this asset within its parent.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "fabric_column_count",
        "fabric_data_type",
        "fabric_ordinal",
    ]

    @property
    def fabric_column_count(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.fabric_column_count

    @fabric_column_count.setter
    def fabric_column_count(self, fabric_column_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_column_count = fabric_column_count

    @property
    def fabric_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.fabric_data_type

    @fabric_data_type.setter
    def fabric_data_type(self, fabric_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_data_type = fabric_data_type

    @property
    def fabric_ordinal(self) -> Optional[int]:
        return None if self.attributes is None else self.attributes.fabric_ordinal

    @fabric_ordinal.setter
    def fabric_ordinal(self, fabric_ordinal: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_ordinal = fabric_ordinal

    class Attributes(BI.Attributes):
        fabric_column_count: Optional[int] = Field(default=None, description="")
        fabric_data_type: Optional[str] = Field(default=None, description="")
        fabric_ordinal: Optional[int] = Field(default=None, description="")

    attributes: Fabric.Attributes = Field(
        default_factory=lambda: Fabric.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
