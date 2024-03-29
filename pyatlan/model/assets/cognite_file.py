# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .cognite import Cognite


class CogniteFile(Cognite):
    """Description"""

    type_name: str = Field(default="CogniteFile", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "CogniteFile":
            raise ValueError("must be CogniteFile")
        return v

    def __setattr__(self, name, value):
        if name in CogniteFile._convenience_properties:
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

    attributes: CogniteFile.Attributes = Field(
        default_factory=lambda: CogniteFile.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .cognite_asset import CogniteAsset  # noqa
