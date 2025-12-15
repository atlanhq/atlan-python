# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .partial import Partial


class PartialField(Partial):
    """Description"""

    type_name: str = Field(default="PartialField", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PartialField":
            raise ValueError("must be PartialField")
        return v

    def __setattr__(self, name, value):
        if name in PartialField._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARTIAL_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "partialDataType", "partialDataType"
    )
    """
    Type of data captured as values in the field.
    """

    PARTIAL_PARENT_ASSET: ClassVar[RelationField] = RelationField("partialParentAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "partial_data_type",
        "partial_parent_asset",
    ]

    @property
    def partial_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.partial_data_type

    @partial_data_type.setter
    def partial_data_type(self, partial_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_data_type = partial_data_type

    @property
    def partial_parent_asset(self) -> Optional[Catalog]:
        return None if self.attributes is None else self.attributes.partial_parent_asset

    @partial_parent_asset.setter
    def partial_parent_asset(self, partial_parent_asset: Optional[Catalog]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_parent_asset = partial_parent_asset

    class Attributes(Partial.Attributes):
        partial_data_type: Optional[str] = Field(default=None, description="")
        partial_parent_asset: Optional[Catalog] = Field(
            default=None, description=""
        )  # relationship

    attributes: PartialField.Attributes = Field(
        default_factory=lambda: PartialField.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa: E402, F401
