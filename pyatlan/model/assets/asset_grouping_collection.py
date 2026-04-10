# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AssetGroupingTrackedCategories
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .asset_grouping import AssetGrouping


class AssetGroupingCollection(AssetGrouping):
    """Description"""

    type_name: str = Field(default="AssetGroupingCollection", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AssetGroupingCollection":
            raise ValueError("must be AssetGroupingCollection")
        return v

    def __setattr__(self, name, value):
        if name in AssetGroupingCollection._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ASSET_GROUPING_COLLECTION_STRATEGY_QUALIFIED_NAME: ClassVar[KeywordField] = (
        KeywordField(
            "assetGroupingCollectionStrategyQualifiedName",
            "assetGroupingCollectionStrategyQualifiedName",
        )
    )
    """
    Qualified name of the grouping strategy from which this collection was created.
    """
    ASSET_GROUPING_COLLECTION_TRACKED_CATEGORIES: ClassVar[KeywordField] = KeywordField(
        "assetGroupingCollectionTrackedCategories",
        "assetGroupingCollectionTrackedCategories",
    )
    """
    Metadata categories the user explicitly selected for tracking.
    """

    ASSET_GROUPING_STRATEGY: ClassVar[RelationField] = RelationField(
        "assetGroupingStrategy"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "asset_grouping_collection_strategy_qualified_name",
        "asset_grouping_collection_tracked_categories",
        "asset_grouping_strategy",
    ]

    @property
    def asset_grouping_collection_strategy_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_grouping_collection_strategy_qualified_name
        )

    @asset_grouping_collection_strategy_qualified_name.setter
    def asset_grouping_collection_strategy_qualified_name(
        self, asset_grouping_collection_strategy_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_collection_strategy_qualified_name = (
            asset_grouping_collection_strategy_qualified_name
        )

    @property
    def asset_grouping_collection_tracked_categories(
        self,
    ) -> Optional[List[AssetGroupingTrackedCategories]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_grouping_collection_tracked_categories
        )

    @asset_grouping_collection_tracked_categories.setter
    def asset_grouping_collection_tracked_categories(
        self,
        asset_grouping_collection_tracked_categories: Optional[
            List[AssetGroupingTrackedCategories]
        ],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_collection_tracked_categories = (
            asset_grouping_collection_tracked_categories
        )

    @property
    def asset_grouping_strategy(self) -> Optional[AssetGroupingStrategy]:
        return (
            None if self.attributes is None else self.attributes.asset_grouping_strategy
        )

    @asset_grouping_strategy.setter
    def asset_grouping_strategy(
        self, asset_grouping_strategy: Optional[AssetGroupingStrategy]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_strategy = asset_grouping_strategy

    class Attributes(AssetGrouping.Attributes):
        asset_grouping_collection_strategy_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        asset_grouping_collection_tracked_categories: Optional[
            List[AssetGroupingTrackedCategories]
        ] = Field(default=None, description="")
        asset_grouping_strategy: Optional[AssetGroupingStrategy] = Field(
            default=None, description=""
        )  # relationship

    attributes: AssetGroupingCollection.Attributes = Field(
        default_factory=lambda: AssetGroupingCollection.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset_grouping_strategy import AssetGroupingStrategy  # noqa: E402, F401

AssetGroupingCollection.Attributes.update_forward_refs()
