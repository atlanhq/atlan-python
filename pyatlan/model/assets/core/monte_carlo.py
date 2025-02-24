# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .data_quality import DataQuality


class MonteCarlo(DataQuality):
    """Description"""

    type_name: str = Field(default="MonteCarlo", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MonteCarlo":
            raise ValueError("must be MonteCarlo")
        return v

    def __setattr__(self, name, value):
        if name in MonteCarlo._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MC_LABELS: ClassVar[KeywordField] = KeywordField("mcLabels", "mcLabels")
    """
    List of labels for this Monte Carlo asset.
    """
    MC_ASSET_QUALIFIED_NAMES: ClassVar[KeywordField] = KeywordField(
        "mcAssetQualifiedNames", "mcAssetQualifiedNames"
    )
    """
    List of unique names of assets that are part of this Monte Carlo asset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "mc_labels",
        "mc_asset_qualified_names",
    ]

    @property
    def mc_labels(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.mc_labels

    @mc_labels.setter
    def mc_labels(self, mc_labels: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_labels = mc_labels

    @property
    def mc_asset_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.mc_asset_qualified_names
        )

    @mc_asset_qualified_names.setter
    def mc_asset_qualified_names(self, mc_asset_qualified_names: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.mc_asset_qualified_names = mc_asset_qualified_names

    class Attributes(DataQuality.Attributes):
        mc_labels: Optional[Set[str]] = Field(default=None, description="")
        mc_asset_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )

    attributes: MonteCarlo.Attributes = Field(
        default_factory=lambda: MonteCarlo.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
