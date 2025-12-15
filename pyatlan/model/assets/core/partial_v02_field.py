# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .partial_v02 import PartialV02


class PartialV02Field(PartialV02):
    """Description"""

    type_name: str = Field(default="PartialV02Field", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PartialV02Field":
            raise ValueError("must be PartialV02Field")
        return v

    def __setattr__(self, name, value):
        if name in PartialV02Field._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARTIAL_V02DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "partialV02DataType", "partialV02DataType"
    )
    """
    Type of data captured as values in the field.
    """

    PARTIAL_V02PARENT_ASSET: ClassVar[RelationField] = RelationField(
        "partialV02ParentAsset"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "partial_v02_data_type",
        "partial_v02_parent_asset",
    ]

    @property
    def partial_v02_data_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.partial_v02_data_type
        )

    @partial_v02_data_type.setter
    def partial_v02_data_type(self, partial_v02_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v02_data_type = partial_v02_data_type

    @property
    def partial_v02_parent_asset(self) -> Optional[Catalog]:
        return (
            None
            if self.attributes is None
            else self.attributes.partial_v02_parent_asset
        )

    @partial_v02_parent_asset.setter
    def partial_v02_parent_asset(self, partial_v02_parent_asset: Optional[Catalog]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_v02_parent_asset = partial_v02_parent_asset

    class Attributes(PartialV02.Attributes):
        partial_v02_data_type: Optional[str] = Field(default=None, description="")
        partial_v02_parent_asset: Optional[Catalog] = Field(
            default=None, description=""
        )  # relationship

    attributes: PartialV02Field.Attributes = Field(
        default_factory=lambda: PartialV02Field.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa: E402, F401
