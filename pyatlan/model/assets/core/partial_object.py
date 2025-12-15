# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .partial import Partial


class PartialObject(Partial):
    """Description"""

    type_name: str = Field(default="PartialObject", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "PartialObject":
            raise ValueError("must be PartialObject")
        return v

    def __setattr__(self, name, value):
        if name in PartialObject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    PARTIAL_PARENT_ASSET: ClassVar[RelationField] = RelationField("partialParentAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "partial_parent_asset",
    ]

    @property
    def partial_parent_asset(self) -> Optional[Catalog]:
        return None if self.attributes is None else self.attributes.partial_parent_asset

    @partial_parent_asset.setter
    def partial_parent_asset(self, partial_parent_asset: Optional[Catalog]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_parent_asset = partial_parent_asset

    class Attributes(Partial.Attributes):
        partial_parent_asset: Optional[Catalog] = Field(
            default=None, description=""
        )  # relationship

    attributes: PartialObject.Attributes = Field(
        default_factory=lambda: PartialObject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .catalog import Catalog  # noqa: E402, F401
