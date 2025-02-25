# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .cognite import Cognite


class CogniteSequence(Cognite):
    """Description"""

    type_name: str = Field(default="CogniteSequence", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CogniteSequence":
            raise ValueError("must be CogniteSequence")
        return v

    def __setattr__(self, name, value):
        if name in CogniteSequence._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COGNITE_ASSET: ClassVar[RelationField] = RelationField("cogniteAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "cognite_asset",
    ]

    @property
    def cognite_asset(self) -> Optional[CogniteAsset]:
        return None if self.attributes is None else self.attributes.cognite_asset

    @cognite_asset.setter
    def cognite_asset(self, cognite_asset: Optional[CogniteAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.cognite_asset = cognite_asset

    class Attributes(Cognite.Attributes):
        cognite_asset: Optional[CogniteAsset] = Field(
            default=None, description=""
        )  # relationship

    attributes: CogniteSequence.Attributes = Field(
        default_factory=lambda: CogniteSequence.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognite_asset import CogniteAsset  # noqa: I001, E402, F401 # isort:skip


CogniteSequence.Attributes.update_forward_refs()
