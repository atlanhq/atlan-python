# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AssetGroupingStrategySource, AssetGroupingStrategyType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .asset_grouping import AssetGrouping


class AssetGroupingStrategy(AssetGrouping):
    """Description"""

    type_name: str = Field(default="AssetGroupingStrategy", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AssetGroupingStrategy":
            raise ValueError("must be AssetGroupingStrategy")
        return v

    def __setattr__(self, name, value):
        if name in AssetGroupingStrategy._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ASSET_GROUPING_STRATEGY_TYPE: ClassVar[KeywordField] = KeywordField(
        "assetGroupingStrategyType", "assetGroupingStrategyType"
    )
    """
    Type of criteria used by this grouping strategy to identify assets.
    """
    ASSET_GROUPING_STRATEGY_CONFIG: ClassVar[KeywordField] = KeywordField(
        "assetGroupingStrategyConfig", "assetGroupingStrategyConfig"
    )
    """
    Stringified JSON configuration of the criteria used by this grouping strategy.
    """
    ASSET_GROUPING_STRATEGY_LAST_EVALUATED_ASSET_COUNT: ClassVar[NumericField] = (
        NumericField(
            "assetGroupingStrategyLastEvaluatedAssetCount",
            "assetGroupingStrategyLastEvaluatedAssetCount",
        )
    )
    """
    Number of assets matching this strategy at last evaluation.
    """
    ASSET_GROUPING_STRATEGY_LAST_EVALUATED_TIMESTAMP: ClassVar[NumericField] = (
        NumericField(
            "assetGroupingStrategyLastEvaluatedTimestamp",
            "assetGroupingStrategyLastEvaluatedTimestamp",
        )
    )
    """
    Time (epoch) at which this strategy was last evaluated.
    """
    ASSET_GROUPING_STRATEGY_SOURCE: ClassVar[KeywordField] = KeywordField(
        "assetGroupingStrategySource", "assetGroupingStrategySource"
    )
    """
    Source of this grouping strategy.
    """

    ASSET_GROUPING_COLLECTIONS: ClassVar[RelationField] = RelationField(
        "assetGroupingCollections"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "asset_grouping_strategy_type",
        "asset_grouping_strategy_config",
        "asset_grouping_strategy_last_evaluated_asset_count",
        "asset_grouping_strategy_last_evaluated_timestamp",
        "asset_grouping_strategy_source",
        "asset_grouping_collections",
    ]

    @property
    def asset_grouping_strategy_type(self) -> Optional[AssetGroupingStrategyType]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_grouping_strategy_type
        )

    @asset_grouping_strategy_type.setter
    def asset_grouping_strategy_type(
        self, asset_grouping_strategy_type: Optional[AssetGroupingStrategyType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_strategy_type = asset_grouping_strategy_type

    @property
    def asset_grouping_strategy_config(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_grouping_strategy_config
        )

    @asset_grouping_strategy_config.setter
    def asset_grouping_strategy_config(
        self, asset_grouping_strategy_config: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_strategy_config = asset_grouping_strategy_config

    @property
    def asset_grouping_strategy_last_evaluated_asset_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_grouping_strategy_last_evaluated_asset_count
        )

    @asset_grouping_strategy_last_evaluated_asset_count.setter
    def asset_grouping_strategy_last_evaluated_asset_count(
        self, asset_grouping_strategy_last_evaluated_asset_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_strategy_last_evaluated_asset_count = (
            asset_grouping_strategy_last_evaluated_asset_count
        )

    @property
    def asset_grouping_strategy_last_evaluated_timestamp(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_grouping_strategy_last_evaluated_timestamp
        )

    @asset_grouping_strategy_last_evaluated_timestamp.setter
    def asset_grouping_strategy_last_evaluated_timestamp(
        self, asset_grouping_strategy_last_evaluated_timestamp: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_strategy_last_evaluated_timestamp = (
            asset_grouping_strategy_last_evaluated_timestamp
        )

    @property
    def asset_grouping_strategy_source(self) -> Optional[AssetGroupingStrategySource]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_grouping_strategy_source
        )

    @asset_grouping_strategy_source.setter
    def asset_grouping_strategy_source(
        self, asset_grouping_strategy_source: Optional[AssetGroupingStrategySource]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_strategy_source = asset_grouping_strategy_source

    @property
    def asset_grouping_collections(self) -> Optional[List[AssetGroupingCollection]]:
        return (
            None
            if self.attributes is None
            else self.attributes.asset_grouping_collections
        )

    @asset_grouping_collections.setter
    def asset_grouping_collections(
        self, asset_grouping_collections: Optional[List[AssetGroupingCollection]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.asset_grouping_collections = asset_grouping_collections

    class Attributes(AssetGrouping.Attributes):
        asset_grouping_strategy_type: Optional[AssetGroupingStrategyType] = Field(
            default=None, description=""
        )
        asset_grouping_strategy_config: Optional[str] = Field(
            default=None, description=""
        )
        asset_grouping_strategy_last_evaluated_asset_count: Optional[int] = Field(
            default=None, description=""
        )
        asset_grouping_strategy_last_evaluated_timestamp: Optional[datetime] = Field(
            default=None, description=""
        )
        asset_grouping_strategy_source: Optional[AssetGroupingStrategySource] = Field(
            default=None, description=""
        )
        asset_grouping_collections: Optional[List[AssetGroupingCollection]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AssetGroupingStrategy.Attributes = Field(
        default_factory=lambda: AssetGroupingStrategy.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset_grouping_collection import AssetGroupingCollection  # noqa: E402, F401

AssetGroupingStrategy.Attributes.update_forward_refs()
