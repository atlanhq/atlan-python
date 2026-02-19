# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
DataQualityRule asset model with flattened inheritance.

This module provides:
- DataQualityRule: Flat asset class (easy to use)
- DataQualityRuleAttributes: Nested attributes struct (extends AssetAttributes)
- DataQualityRuleNested: Nested API format struct
"""

from __future__ import annotations

import json
import time
import uuid
from typing import TYPE_CHECKING, ClassVar, Optional, Union

from msgspec import UNSET, UnsetType

from pyatlan.errors import ErrorCode
from pyatlan.model.enums import (
    DataQualityDimension,
    DataQualityRuleAlertPriority,
    DataQualityRuleCustomSQLReturnType,
    DataQualityRuleStatus,
    DataQualityRuleTemplateType,
    DataQualityRuleThresholdCompareOperator,
    DataQualityRuleThresholdUnit,
    DataQualitySourceSyncStatus,
)
from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, RelationField
from pyatlan_v9.model.conversion_utils import (
    categorize_relationships,
    merge_relationships,
)
from pyatlan_v9.model.serde import Serde, get_serde
from pyatlan_v9.model.structs import (
    DataQualityRuleConfigArguments,
    DataQualityRuleThresholdObject,
)
from pyatlan_v9.model.transform import register_asset
from pyatlan_v9.utils import init_guid, validate_required_fields

from .asset import Asset, AssetAttributes, AssetNested, AssetRelationshipAttributes
from .asset_related import RelatedAsset
from .data_quality_related import RelatedDataQualityRuleTemplate
from .sql_related import RelatedColumn

if TYPE_CHECKING:
    from pyatlan_v9.client.atlan import AtlanClient

# =============================================================================
# FLAT ASSET CLASS
# =============================================================================


@register_asset
class DataQualityRule(Asset):
    """
    Class to define a rule for the given asset in Atlan.
    """

    # =========================================================================
    # Field Descriptors (class-level, for search query building)
    # =========================================================================

    DQ_RULE_BASE_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dqRuleBaseDatasetQualifiedName", "dqRuleBaseDatasetQualifiedName"
    )
    DQ_RULE_BASE_COLUMN_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "dqRuleBaseColumnQualifiedName", "dqRuleBaseColumnQualifiedName"
    )
    DQ_RULE_SOURCE_SYNC_STATUS: ClassVar[KeywordField] = KeywordField(
        "dqRuleSourceSyncStatus", "dqRuleSourceSyncStatus"
    )
    DQ_RULE_LATEST_RESULT: ClassVar[KeywordField] = KeywordField(
        "dqRuleLatestResult", "dqRuleLatestResult"
    )
    DQ_RULE_DIMENSION: ClassVar[KeywordField] = KeywordField(
        "dqRuleDimension", "dqRuleDimension"
    )
    DQ_RULE_TEMPLATE_NAME: ClassVar[KeywordField] = KeywordField(
        "dqRuleTemplateName", "dqRuleTemplateName"
    )
    DQ_RULE_STATUS: ClassVar[KeywordField] = KeywordField(
        "dqRuleStatus", "dqRuleStatus"
    )
    DQ_RULE_ALERT_PRIORITY: ClassVar[KeywordField] = KeywordField(
        "dqRuleAlertPriority", "dqRuleAlertPriority"
    )
    DQ_RULE_CONFIG_ARGUMENTS: ClassVar[KeywordField] = KeywordField(
        "dqRuleConfigArguments", "dqRuleConfigArguments"
    )
    DQ_RULE_CUSTOM_SQL: ClassVar[KeywordField] = KeywordField(
        "dqRuleCustomSQL", "dqRuleCustomSQL"
    )
    DQ_RULE_CUSTOM_SQL_RETURN_TYPE: ClassVar[KeywordField] = KeywordField(
        "dqRuleCustomSQLReturnType", "dqRuleCustomSQLReturnType"
    )
    DQ_RULE_ROW_SCOPE_FILTERING_ENABLED: ClassVar[BooleanField] = BooleanField(
        "dqRuleRowScopeFilteringEnabled", "dqRuleRowScopeFilteringEnabled"
    )
    DQ_RULE_TEMPLATE: ClassVar[RelationField] = RelationField("dqRuleTemplate")
    DQ_RULE_BASE_DATASET: ClassVar[RelationField] = RelationField("dqRuleBaseDataset")
    DQ_RULE_BASE_COLUMN: ClassVar[RelationField] = RelationField("dqRuleBaseColumn")

    # =========================================================================
    # Instance Fields
    # =========================================================================

    # Override type_name with DataQualityRule-specific default
    type_name: Union[str, UnsetType] = "DataQualityRule"

    dq_rule_base_dataset_qualified_name: Union[str, None, UnsetType] = UNSET
    """Base dataset qualified name that attached to this rule."""

    dq_rule_base_column_qualified_name: Union[str, None, UnsetType] = UNSET
    """Base column qualified name that attached to this rule."""

    dq_rule_reference_dataset_qualified_names: Union[list[str], None, UnsetType] = UNSET
    """List of unique reference dataset's qualified names related to this rule."""

    dq_rule_reference_column_qualified_names: Union[list[str], None, UnsetType] = UNSET
    """List of unique reference column's qualified names related to this rule."""

    dq_rule_source_sync_status: Union[str, None, UnsetType] = UNSET
    """Latest sync status of the rule to the source."""

    dq_rule_source_sync_error_code: Union[str, None, UnsetType] = UNSET
    """Error code in the case of state being "failure"."""

    dq_rule_source_sync_error_message: Union[str, None, UnsetType] = UNSET
    """Error message in the case of state being "error"."""

    dq_rule_source_sync_raw_error: Union[str, None, UnsetType] = UNSET
    """Raw error message from the source."""

    dq_rule_source_synced_at: Union[int, None, UnsetType] = UNSET
    """Time (epoch) at which the rule synced to the source."""

    dq_rule_latest_result: Union[str, None, UnsetType] = UNSET
    """Latest result of the rule."""

    dq_rule_latest_result_computed_at: Union[int, None, UnsetType] = UNSET
    """Time (epoch) at which the latest rule result was evaluated."""

    dq_rule_latest_result_fetched_at: Union[int, None, UnsetType] = UNSET
    """Time (epoch) at which the latest rule result was fetched."""

    dq_rule_latest_metric_value: Union[str, None, UnsetType] = UNSET
    """Last result metrics value of the rule."""

    dq_rule_latest_metric_value_computed_at: Union[int, None, UnsetType] = UNSET
    """Time (epoch) at which the latest metric value was evaluated in the source."""

    dq_rule_dimension: Union[str, None, UnsetType] = UNSET
    """Dimension of the data quality rule."""

    dq_rule_template_name: Union[str, None, UnsetType] = UNSET
    """Name of the rule template corresponding to the rule."""

    dq_rule_status: Union[str, None, UnsetType] = UNSET
    """Status of the rule."""

    dq_rule_alert_priority: Union[str, None, UnsetType] = UNSET
    """Default priority level for alerts involving this rule."""

    dq_rule_config_arguments: Union[DataQualityRuleConfigArguments, None, UnsetType] = (
        UNSET
    )
    """Rule config that contains the rule definitions."""

    dq_rule_custom_sql: Union[str, None, UnsetType] = UNSET
    """SQL code for custom SQL rules."""

    dq_rule_custom_sql_return_type: Union[str, None, UnsetType] = UNSET
    """Type of result returned by the custom SQL (number of rows or numeric value)."""

    dq_rule_failed_rows_sql: Union[str, None, UnsetType] = UNSET
    """SQL query used to retrieve failed rows."""

    dq_rule_row_scope_filtering_enabled: Union[bool, None, UnsetType] = UNSET
    """Whether row scope filtering is enabled for this data quality rule (true) or not (false)."""

    dq_is_part_of_contract: Union[bool, None, UnsetType] = UNSET
    """Whether this data quality is part of contract (true) or not (false)."""

    dq_rule_template: Union[RelatedDataQualityRuleTemplate, None, UnsetType] = UNSET
    """Template used to create this rule."""

    dq_rule_base_dataset: Union[RelatedAsset, None, UnsetType] = UNSET
    """Base dataset attached to this rule."""

    dq_rule_base_column: Union[RelatedColumn, None, UnsetType] = UNSET
    """Base column attached to this rule."""

    dq_rule_reference_datasets: Union[list[RelatedAsset], None, UnsetType] = UNSET
    """Datasets referenced in this rule."""

    dq_rule_reference_columns: Union[list[RelatedColumn], None, UnsetType] = UNSET
    """Columns referenced in this rule."""

    # =========================================================================
    # Creator / Factory Methods
    # =========================================================================

    @classmethod
    @init_guid
    def custom_sql_creator(
        cls,
        *,
        client: "AtlanClient",
        rule_name: str,
        asset: Asset,
        custom_sql: str,
        threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        dimension: DataQualityDimension,
        custom_sql_return_type: Optional[DataQualityRuleCustomSQLReturnType] = None,
        description: Optional[str] = None,
    ) -> "DataQualityRule":
        validate_required_fields(
            [
                "client",
                "rule_name",
                "asset",
                "threshold_compare_operator",
                "threshold_value",
                "alert_priority",
                "dimension",
                "custom_sql",
            ],
            [
                client,
                rule_name,
                asset,
                threshold_compare_operator,
                threshold_value,
                alert_priority,
                dimension,
                custom_sql,
            ],
        )
        return cls._build_rule(
            client=client,
            rule_name=rule_name,
            rule_type=DataQualityRuleTemplateType.CUSTOM_SQL,
            asset=asset,
            threshold_compare_operator=threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            dimension=dimension,
            custom_sql=custom_sql,
            custom_sql_return_type=custom_sql_return_type,
            description=description,
            column=None,
            threshold_unit=None,
        )

    @classmethod
    @init_guid
    def table_level_rule_creator(
        cls,
        *,
        client: "AtlanClient",
        rule_type: DataQualityRuleTemplateType,
        asset: Asset,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> "DataQualityRule":
        validate_required_fields(
            ["client", "rule_type", "asset", "threshold_value", "alert_priority"],
            [client, rule_type, asset, threshold_value, alert_priority],
        )
        template_config = client.dq_template_config_cache.get_template_config(
            rule_type.value
        )
        asset_for_validation, target_table_asset = (
            cls._fetch_assets_for_row_scope_validation(
                client, asset, rule_conditions, row_scope_filtering_enabled or False
            )
        )
        validated_threshold_operator = cls._validate_template_features(
            rule_type,
            rule_conditions,
            row_scope_filtering_enabled,
            template_config,
            threshold_compare_operator,
            asset_for_validation,
            target_table_asset,
        )
        final_threshold_compare_operator = (
            validated_threshold_operator
            or threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )
        return cls._build_rule(
            client=client,
            rule_type=rule_type,
            asset=asset,
            threshold_compare_operator=final_threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            rule_name=None,
            column=None,
            threshold_unit=threshold_unit,
            dimension=None,
            custom_sql=None,
            description=None,
            rule_conditions=rule_conditions,
            row_scope_filtering_enabled=row_scope_filtering_enabled,
        )

    @classmethod
    @init_guid
    def column_level_rule_creator(
        cls,
        *,
        client: "AtlanClient",
        rule_type: DataQualityRuleTemplateType,
        asset: Asset,
        column: Asset,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> "DataQualityRule":
        validate_required_fields(
            [
                "client",
                "rule_type",
                "asset",
                "column",
                "threshold_value",
                "alert_priority",
            ],
            [client, rule_type, asset, column, threshold_value, alert_priority],
        )
        template_config = client.dq_template_config_cache.get_template_config(
            rule_type.value
        )
        asset_for_validation, target_table_asset = (
            cls._fetch_assets_for_row_scope_validation(
                client, asset, rule_conditions, row_scope_filtering_enabled or False
            )
        )
        validated_threshold_operator = cls._validate_template_features(
            rule_type,
            rule_conditions,
            row_scope_filtering_enabled,
            template_config,
            threshold_compare_operator,
            asset_for_validation,
            target_table_asset,
        )
        final_threshold_compare_operator = (
            validated_threshold_operator
            or threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )
        return cls._build_rule(
            client=client,
            rule_type=rule_type,
            asset=asset,
            column=column,
            threshold_compare_operator=final_threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            threshold_unit=threshold_unit,
            rule_name=None,
            dimension=None,
            custom_sql=None,
            description=None,
            rule_conditions=rule_conditions,
            row_scope_filtering_enabled=row_scope_filtering_enabled,
        )

    @classmethod
    @init_guid
    def updater(
        cls,
        client: "AtlanClient",
        qualified_name: str,
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        threshold_value: Optional[int] = None,
        alert_priority: Optional[DataQualityRuleAlertPriority] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        dimension: Optional[DataQualityDimension] = None,
        custom_sql: Optional[str] = None,
        custom_sql_return_type: Optional[DataQualityRuleCustomSQLReturnType] = None,
        rule_name: Optional[str] = None,
        description: Optional[str] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> "DataQualityRule":
        from pyatlan.model.fluent_search import FluentSearch

        validate_required_fields(
            ["client", "qualified_name"],
            [client, qualified_name],
        )
        request = (
            FluentSearch()
            .where(DataQualityRule.QUALIFIED_NAME.eq(qualified_name))
            .include_on_results(DataQualityRule.NAME)
            .include_on_results(DataQualityRule.DQ_RULE_TEMPLATE_NAME)
            .include_on_results(DataQualityRule.DQ_RULE_TEMPLATE)
            .include_on_results(DataQualityRule.DQ_RULE_BASE_DATASET)
            .include_on_results(DataQualityRule.DQ_RULE_BASE_COLUMN)
            .include_on_results(DataQualityRule.DQ_RULE_ALERT_PRIORITY)
            .include_on_results(DataQualityRule.DISPLAY_NAME)
            .include_on_results(DataQualityRule.DQ_RULE_CUSTOM_SQL)
            .include_on_results(DataQualityRule.DQ_RULE_CUSTOM_SQL_RETURN_TYPE)
            .include_on_results(DataQualityRule.USER_DESCRIPTION)
            .include_on_results(DataQualityRule.DQ_RULE_DIMENSION)
            .include_on_results(DataQualityRule.DQ_RULE_CONFIG_ARGUMENTS)
            .include_on_results(DataQualityRule.DQ_RULE_ROW_SCOPE_FILTERING_ENABLED)
            .include_on_results(DataQualityRule.DQ_RULE_SOURCE_SYNC_STATUS)
            .include_on_results(DataQualityRule.DQ_RULE_STATUS)
        ).to_request()

        results = client.asset.search(request)

        if results.count != 1:
            raise ValueError(
                f"Expected exactly 1 asset for qualified_name: {qualified_name}, "
                f"but found: {results.count}"
            )
        search_result = results.current_page()[0]

        retrieved_custom_sql = getattr(search_result, "dq_rule_custom_sql", None)
        retrieved_custom_sql_return_type = getattr(
            search_result, "dq_rule_custom_sql_return_type", None
        )
        retrieved_rule_name = getattr(search_result, "display_name", None)
        retrieved_dimension = getattr(search_result, "dq_rule_dimension", None)
        retrieved_column = getattr(search_result, "dq_rule_base_column", None)
        retrieved_alert_priority = getattr(
            search_result, "dq_rule_alert_priority", None
        )
        retrieved_row_scope_filtering_enabled = getattr(
            search_result, "dq_rule_row_scope_filtering_enabled", None
        )
        retrieved_description = getattr(search_result, "user_description", None)
        retrieved_asset = getattr(search_result, "dq_rule_base_dataset", None)
        retrieved_template_rule_name = getattr(
            search_result, "dq_rule_template_name", None
        )
        retrieved_template = getattr(search_result, "dq_rule_template", None)

        config_args = getattr(search_result, "dq_rule_config_arguments", None)
        threshold_obj = (
            getattr(config_args, "dq_rule_threshold_object", None)
            if config_args
            else None
        )
        retrieved_threshold_compare_operator = (
            getattr(threshold_obj, "dq_rule_threshold_compare_operator", None)
            if threshold_obj
            else None
        )
        retrieved_threshold_value = (
            getattr(threshold_obj, "dq_rule_threshold_value", None)
            if threshold_obj
            else None
        )
        retrieved_threshold_unit = (
            getattr(threshold_obj, "dq_rule_threshold_unit", None)
            if threshold_obj
            else None
        )

        template_config = None
        if retrieved_template_rule_name:
            template_config = client.dq_template_config_cache.get_template_config(
                retrieved_template_rule_name
            )

        if rule_conditions:
            final_rule_conditions = rule_conditions
        elif config_args is not None:
            final_rule_conditions = getattr(
                config_args, "dq_rule_config_rule_conditions", None
            )
        else:
            final_rule_conditions = None

        final_row_scope_filtering_enabled = (
            row_scope_filtering_enabled or retrieved_row_scope_filtering_enabled
        )
        if retrieved_asset:
            retrieved_asset, target_table_asset = (
                cls._fetch_assets_for_row_scope_validation(
                    client,
                    retrieved_asset,
                    final_rule_conditions,
                    final_row_scope_filtering_enabled,
                )
            )
        else:
            target_table_asset = None

        validated_threshold_operator = None
        if retrieved_template_rule_name and template_config:
            try:
                retrieved_rule_type = DataQualityRuleTemplateType(
                    retrieved_template_rule_name
                )
                validated_threshold_operator = cls._validate_template_features(
                    retrieved_rule_type,
                    final_rule_conditions,
                    final_row_scope_filtering_enabled,
                    template_config,
                    threshold_compare_operator or retrieved_threshold_compare_operator,
                    retrieved_asset,
                    target_table_asset,
                )
            except ValueError:
                pass

        final_compare_operator = (
            validated_threshold_operator
            or threshold_compare_operator
            or retrieved_threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )

        rule = cls(
            name="",
            dq_rule_config_arguments=DataQualityRuleConfigArguments(
                dq_rule_threshold_object=DataQualityRuleThresholdObject(
                    dq_rule_threshold_compare_operator=final_compare_operator,
                    dq_rule_threshold_value=threshold_value
                    or retrieved_threshold_value,
                    dq_rule_threshold_unit=threshold_unit or retrieved_threshold_unit,
                ),
                dq_rule_config_rule_conditions=final_rule_conditions,
            ),
            dq_rule_base_dataset_qualified_name=(
                retrieved_asset.qualified_name if retrieved_asset else None
            ),
            dq_rule_alert_priority=alert_priority or retrieved_alert_priority,
            dq_rule_row_scope_filtering_enabled=final_row_scope_filtering_enabled,
            dq_rule_base_dataset=retrieved_asset,
            qualified_name=qualified_name,
            dq_rule_dimension=dimension or retrieved_dimension,
            dq_rule_template_name=retrieved_template_rule_name,
            dq_rule_template=(
                DataQualityRuleTemplate.ref_by_qualified_name(
                    qualified_name=retrieved_template.qualified_name
                )
                if retrieved_template
                else None
            ),
        )

        if retrieved_column is not None:
            rule.dq_rule_base_column_qualified_name = retrieved_column.qualified_name
            rule.dq_rule_base_column = retrieved_column

        final_custom_sql = custom_sql or retrieved_custom_sql
        if final_custom_sql is not None:
            rule.dq_rule_custom_sql = final_custom_sql
            rule.display_name = rule_name or retrieved_rule_name
            rule.dq_rule_custom_sql_return_type = (
                custom_sql_return_type or retrieved_custom_sql_return_type
            )
            if description is not None:
                rule.user_description = description or retrieved_description

        return rule

    # =========================================================================
    # Internal Builder & Validation Helpers
    # =========================================================================

    @classmethod
    def _build_rule(
        cls,
        *,
        client: "AtlanClient",
        rule_type: DataQualityRuleTemplateType,
        asset: Asset,
        threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        rule_name: Optional[str] = None,
        column: Optional[Asset] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        dimension: Optional[DataQualityDimension] = None,
        custom_sql: Optional[str] = None,
        custom_sql_return_type: Optional[DataQualityRuleCustomSQLReturnType] = None,
        description: Optional[str] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> "DataQualityRule":
        """Internal helper that mirrors the legacy ``Attributes.creator`` logic."""
        template_config = client.dq_template_config_cache.get_template_config(
            rule_type.value
        )
        if template_config is None:
            raise ErrorCode.DQ_RULE_NOT_FOUND.exception_with_parameters(rule_type.value)

        template_rule_name = template_config.get("name")
        template_qualified_name = template_config.get("qualified_name")

        if dimension is None:
            dimension = template_config.get("dimension")

        if threshold_unit is None:
            config = template_config.get("config")
            if config is not None:
                threshold_unit = cls._get_template_config_value(
                    config.dq_rule_template_config_threshold_object,
                    "dqRuleTemplateConfigThresholdUnit",
                    "default",
                )

        rule = cls(
            name="",
            dq_rule_config_arguments=DataQualityRuleConfigArguments(
                dq_rule_threshold_object=DataQualityRuleThresholdObject(
                    dq_rule_threshold_compare_operator=threshold_compare_operator,
                    dq_rule_threshold_value=threshold_value,
                    dq_rule_threshold_unit=threshold_unit,
                ),
                dq_rule_config_rule_conditions=rule_conditions,
            ),
            dq_rule_base_dataset_qualified_name=asset.qualified_name,
            dq_rule_alert_priority=alert_priority,
            dq_rule_row_scope_filtering_enabled=row_scope_filtering_enabled,
            dq_rule_source_sync_status=DataQualitySourceSyncStatus.IN_PROGRESS,
            dq_rule_status=DataQualityRuleStatus.ACTIVE,
            dq_rule_base_dataset=asset,
            qualified_name=f"{asset.qualified_name}/rule/{cls._generate_uuid()}",
            dq_rule_dimension=dimension,
            dq_rule_template_name=template_rule_name,
            dq_rule_template=DataQualityRuleTemplate.ref_by_qualified_name(
                qualified_name=template_qualified_name,
            ),
        )

        if column is not None:
            rule.dq_rule_base_column_qualified_name = column.qualified_name
            rule.dq_rule_base_column = column

        if custom_sql is not None:
            rule.dq_rule_custom_sql = custom_sql
            rule.display_name = rule_name
            if custom_sql_return_type is not None:
                rule.dq_rule_custom_sql_return_type = custom_sql_return_type
            if description is not None:
                rule.user_description = description

        return rule

    @staticmethod
    def _generate_uuid() -> str:
        d = int(time.time() * 1000)
        random_bytes = uuid.uuid4().bytes
        rand_index = 0

        def replace_char(c: str) -> str:
            nonlocal d, rand_index
            r = (d + random_bytes[rand_index % 16]) % 16
            rand_index += 1
            d = d // 16
            if c == "x":
                return hex(r)[2:]
            elif c == "y":
                return hex((r & 0x3) | 0x8)[2:]
            else:
                return c

        template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
        return "".join(replace_char(c) if c in "xy" else c for c in template)

    @staticmethod
    def _get_template_config_value(
        config_value: str,
        property_name: Optional[str] = None,
        value_key: str = "default",
    ):
        if not config_value:
            return None
        try:
            config_json = json.loads(config_value)
            if property_name:
                properties = config_json.get("properties", {})
                field = properties.get(property_name, {})
                return field.get(value_key)
            else:
                return config_json.get(value_key)
        except (json.JSONDecodeError, KeyError):
            return None

    @staticmethod
    def _validate_template_features(
        rule_type: DataQualityRuleTemplateType,
        rule_conditions: Optional[str],
        row_scope_filtering_enabled: Optional[bool],
        template_config: Optional[dict],
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        asset: Optional[Asset] = None,
        target_table_asset: Optional[Asset] = None,
    ) -> Optional[DataQualityRuleThresholdCompareOperator]:
        if not template_config or not template_config.get("config"):
            return None

        config = template_config["config"]

        if rule_conditions and config.dq_rule_template_config_rule_conditions is None:
            raise ErrorCode.DQ_RULE_TYPE_NOT_SUPPORTED.exception_with_parameters(
                rule_type.value, "rule conditions"
            )

        if row_scope_filtering_enabled:
            advanced_settings = config.dq_rule_template_config_advanced_settings or ""
            if "dqRuleRowScopeFilteringEnabled" not in str(advanced_settings):
                raise ErrorCode.DQ_RULE_TYPE_NOT_SUPPORTED.exception_with_parameters(
                    rule_type.value, "row scope filtering"
                )
            if asset and not getattr(
                asset,
                "asset_dq_row_scope_filter_column_qualified_name",
                None,
            ):
                raise ErrorCode.DQ_ROW_SCOPE_FILTER_COLUMN_MISSING.exception_with_parameters(
                    getattr(asset, "qualified_name", "unknown")
                )
            if target_table_asset:
                if not getattr(
                    target_table_asset,
                    "asset_dq_row_scope_filter_column_qualified_name",
                    None,
                ):
                    raise ErrorCode.DQ_ROW_SCOPE_FILTER_COLUMN_MISSING.exception_with_parameters(
                        getattr(target_table_asset, "qualified_name", "unknown")
                    )

        if rule_conditions:
            allowed_rule_conditions = DataQualityRule._get_template_config_value(
                config.dq_rule_template_config_rule_conditions or "",
                None,
                "enum",
            )
            if allowed_rule_conditions:
                try:
                    rule_conditions_json = json.loads(rule_conditions)
                    conditions = rule_conditions_json.get("conditions", [])
                    if len(conditions) != 1:
                        raise ErrorCode.DQ_RULE_CONDITIONS_INVALID.exception_with_parameters(
                            f"exactly one condition required, found {len(conditions)}"
                        )
                    condition_type = conditions[0].get("type")
                except json.JSONDecodeError:
                    condition_type = rule_conditions

                if condition_type not in allowed_rule_conditions:
                    raise ErrorCode.DQ_RULE_CONDITIONS_INVALID.exception_with_parameters(
                        f"condition type '{condition_type}' not supported, allowed: {allowed_rule_conditions}"
                    )

            if threshold_compare_operator is None:
                return DataQualityRuleThresholdCompareOperator.EQUAL
            elif (
                threshold_compare_operator
                != DataQualityRuleThresholdCompareOperator.EQUAL
            ):
                raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                    f"threshold_compare_operator={threshold_compare_operator.value}",
                    "threshold_compare_operator",
                    "EQUAL when rule_conditions are provided",
                )

        if threshold_compare_operator is not None:
            allowed_operators = DataQualityRule._get_template_config_value(
                config.dq_rule_template_config_threshold_object,
                "dqRuleTemplateConfigThresholdCompareOperator",
                "enum",
            )
            if (
                allowed_operators
                and threshold_compare_operator.value not in allowed_operators
            ):
                raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                    f"threshold_compare_operator={threshold_compare_operator.value}",
                    "threshold_compare_operator",
                    f"must be one of {allowed_operators}",
                )
        elif threshold_compare_operator is None:
            default_value = DataQualityRule._get_template_config_value(
                config.dq_rule_template_config_threshold_object,
                "dqRuleTemplateConfigThresholdCompareOperator",
                "default",
            )
            if default_value:
                threshold_compare_operator = DataQualityRuleThresholdCompareOperator(
                    default_value
                )

        return (
            threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )

    @staticmethod
    def _fetch_assets_for_row_scope_validation(
        client: "AtlanClient",
        base_asset: Asset,
        rule_conditions: Optional[str],
        row_scope_filtering_enabled: bool,
    ) -> tuple[Asset, Optional[Asset]]:
        asset_for_validation = base_asset
        target_table_asset = None

        if not row_scope_filtering_enabled:
            return asset_for_validation, target_table_asset

        # Extract target_table from rule_conditions
        target_table_qualified_name = None
        if rule_conditions:
            try:
                rule_conditions_json = json.loads(rule_conditions)
                conditions = rule_conditions_json.get("conditions", [])
                if conditions:
                    condition_value = conditions[0].get("value", {})
                    target_table_qualified_name = condition_value.get("target_table")
            except (json.JSONDecodeError, KeyError, TypeError, AttributeError):
                pass

        qualified_names_to_search = []
        if base_asset.qualified_name:
            qualified_names_to_search.append(base_asset.qualified_name)
        if target_table_qualified_name:
            qualified_names_to_search.append(target_table_qualified_name)

        if qualified_names_to_search:
            from pyatlan.model.fluent_search import FluentSearch

            search_request = (
                FluentSearch()
                .where(Asset.QUALIFIED_NAME.within(qualified_names_to_search))
                .include_on_results(
                    Asset.ASSET_DQ_ROW_SCOPE_FILTER_COLUMN_QUALIFIED_NAME
                )
            ).to_request()
            results = client.asset.search(search_request)

            for result in results.current_page():
                if result.qualified_name == base_asset.qualified_name:
                    asset_for_validation = result
                elif (
                    target_table_qualified_name
                    and result.qualified_name == target_table_qualified_name
                ):
                    target_table_asset = result

        return asset_for_validation, target_table_asset

    # =========================================================================
    # Optimized Serialization Methods (override Asset base class)
    # =========================================================================

    def to_json(self, nested: bool = True, serde: Serde | None = None) -> str:
        """
        Convert to JSON string using optimized nested struct serialization.

        Args:
            nested: If True (default), use nested API format. If False, use flat format.
            serde: Optional Serde instance for encoder reuse. Uses shared singleton if None.

        Returns:
            JSON string representation
        """
        if serde is None:
            serde = get_serde()
        if nested:
            return _data_quality_rule_to_nested_bytes(self, serde).decode("utf-8")
        else:
            return serde.encode(self).decode("utf-8")

    @staticmethod
    def from_json(
        json_data: Union[str, bytes], serde: Serde | None = None
    ) -> "DataQualityRule":
        """
        Create from JSON string or bytes using optimized nested struct deserialization.

        Args:
            json_data: JSON string or bytes to deserialize
            serde: Optional Serde instance for decoder reuse. Uses shared singleton if None.

        Returns:
            DataQualityRule instance
        """
        if isinstance(json_data, str):
            json_data = json_data.encode("utf-8")
        if serde is None:
            serde = get_serde()
        return _data_quality_rule_from_nested_bytes(json_data, serde)


# =============================================================================
# NESTED FORMAT CLASSES
# =============================================================================


class DataQualityRuleAttributes(AssetAttributes):
    """DataQualityRule-specific attributes for nested API format."""

    dq_rule_base_dataset_qualified_name: Union[str, None, UnsetType] = UNSET
    """Base dataset qualified name that attached to this rule."""

    dq_rule_base_column_qualified_name: Union[str, None, UnsetType] = UNSET
    """Base column qualified name that attached to this rule."""

    dq_rule_reference_dataset_qualified_names: Union[list[str], None, UnsetType] = UNSET
    """List of unique reference dataset's qualified names related to this rule."""

    dq_rule_reference_column_qualified_names: Union[list[str], None, UnsetType] = UNSET
    """List of unique reference column's qualified names related to this rule."""

    dq_rule_source_sync_status: Union[str, None, UnsetType] = UNSET
    """Latest sync status of the rule to the source."""

    dq_rule_source_sync_error_code: Union[str, None, UnsetType] = UNSET
    """Error code in the case of state being "failure"."""

    dq_rule_source_sync_error_message: Union[str, None, UnsetType] = UNSET
    """Error message in the case of state being "error"."""

    dq_rule_source_sync_raw_error: Union[str, None, UnsetType] = UNSET
    """Raw error message from the source."""

    dq_rule_source_synced_at: Union[int, None, UnsetType] = UNSET
    """Time (epoch) at which the rule synced to the source."""

    dq_rule_latest_result: Union[str, None, UnsetType] = UNSET
    """Latest result of the rule."""

    dq_rule_latest_result_computed_at: Union[int, None, UnsetType] = UNSET
    """Time (epoch) at which the latest rule result was evaluated."""

    dq_rule_latest_result_fetched_at: Union[int, None, UnsetType] = UNSET
    """Time (epoch) at which the latest rule result was fetched."""

    dq_rule_latest_metric_value: Union[str, None, UnsetType] = UNSET
    """Last result metrics value of the rule."""

    dq_rule_latest_metric_value_computed_at: Union[int, None, UnsetType] = UNSET
    """Time (epoch) at which the latest metric value was evaluated in the source."""

    dq_rule_dimension: Union[str, None, UnsetType] = UNSET
    """Dimension of the data quality rule."""

    dq_rule_template_name: Union[str, None, UnsetType] = UNSET
    """Name of the rule template corresponding to the rule."""

    dq_rule_status: Union[str, None, UnsetType] = UNSET
    """Status of the rule."""

    dq_rule_alert_priority: Union[str, None, UnsetType] = UNSET
    """Default priority level for alerts involving this rule."""

    dq_rule_config_arguments: Union[DataQualityRuleConfigArguments, None, UnsetType] = (
        UNSET
    )
    """Rule config that contains the rule definitions."""

    dq_rule_custom_sql: Union[str, None, UnsetType] = UNSET
    """SQL code for custom SQL rules."""

    dq_rule_custom_sql_return_type: Union[str, None, UnsetType] = UNSET
    """Type of result returned by the custom SQL (number of rows or numeric value)."""

    dq_rule_failed_rows_sql: Union[str, None, UnsetType] = UNSET
    """SQL query used to retrieve failed rows."""

    dq_rule_row_scope_filtering_enabled: Union[bool, None, UnsetType] = UNSET
    """Whether row scope filtering is enabled for this data quality rule (true) or not (false)."""

    dq_is_part_of_contract: Union[bool, None, UnsetType] = UNSET
    """Whether this data quality is part of contract (true) or not (false)."""


class DataQualityRuleRelationshipAttributes(AssetRelationshipAttributes):
    """DataQualityRule-specific relationship attributes for nested API format."""

    dq_rule_template: Union[RelatedDataQualityRuleTemplate, None, UnsetType] = UNSET
    """Template used to create this rule."""

    dq_rule_base_dataset: Union[RelatedAsset, None, UnsetType] = UNSET
    """Base dataset attached to this rule."""

    dq_rule_base_column: Union[RelatedColumn, None, UnsetType] = UNSET
    """Base column attached to this rule."""

    dq_rule_reference_datasets: Union[list[RelatedAsset], None, UnsetType] = UNSET
    """Datasets referenced in this rule."""

    dq_rule_reference_columns: Union[list[RelatedColumn], None, UnsetType] = UNSET
    """Columns referenced in this rule."""


class DataQualityRuleNested(AssetNested):
    """DataQualityRule in nested API format for high-performance serialization."""

    attributes: Union[DataQualityRuleAttributes, UnsetType] = UNSET
    relationship_attributes: Union[DataQualityRuleRelationshipAttributes, UnsetType] = (
        UNSET
    )
    append_relationship_attributes: Union[
        DataQualityRuleRelationshipAttributes, UnsetType
    ] = UNSET
    remove_relationship_attributes: Union[
        DataQualityRuleRelationshipAttributes, UnsetType
    ] = UNSET


# =============================================================================
# CONVERSION FUNCTIONS
# =============================================================================


def _data_quality_rule_to_nested(
    data_quality_rule: DataQualityRule,
) -> DataQualityRuleNested:
    """Convert flat DataQualityRule to nested format."""
    attrs = DataQualityRuleAttributes(
        dq_rule_base_dataset_qualified_name=data_quality_rule.dq_rule_base_dataset_qualified_name,
        dq_rule_base_column_qualified_name=data_quality_rule.dq_rule_base_column_qualified_name,
        dq_rule_reference_dataset_qualified_names=data_quality_rule.dq_rule_reference_dataset_qualified_names,
        dq_rule_reference_column_qualified_names=data_quality_rule.dq_rule_reference_column_qualified_names,
        dq_rule_source_sync_status=data_quality_rule.dq_rule_source_sync_status,
        dq_rule_source_sync_error_code=data_quality_rule.dq_rule_source_sync_error_code,
        dq_rule_source_sync_error_message=data_quality_rule.dq_rule_source_sync_error_message,
        dq_rule_source_sync_raw_error=data_quality_rule.dq_rule_source_sync_raw_error,
        dq_rule_source_synced_at=data_quality_rule.dq_rule_source_synced_at,
        dq_rule_latest_result=data_quality_rule.dq_rule_latest_result,
        dq_rule_latest_result_computed_at=data_quality_rule.dq_rule_latest_result_computed_at,
        dq_rule_latest_result_fetched_at=data_quality_rule.dq_rule_latest_result_fetched_at,
        dq_rule_latest_metric_value=data_quality_rule.dq_rule_latest_metric_value,
        dq_rule_latest_metric_value_computed_at=data_quality_rule.dq_rule_latest_metric_value_computed_at,
        dq_rule_dimension=data_quality_rule.dq_rule_dimension,
        dq_rule_template_name=data_quality_rule.dq_rule_template_name,
        dq_rule_status=data_quality_rule.dq_rule_status,
        dq_rule_alert_priority=data_quality_rule.dq_rule_alert_priority,
        dq_rule_config_arguments=data_quality_rule.dq_rule_config_arguments,
        dq_rule_custom_sql=data_quality_rule.dq_rule_custom_sql,
        dq_rule_custom_sql_return_type=data_quality_rule.dq_rule_custom_sql_return_type,
        dq_rule_failed_rows_sql=data_quality_rule.dq_rule_failed_rows_sql,
        dq_rule_row_scope_filtering_enabled=data_quality_rule.dq_rule_row_scope_filtering_enabled,
        dq_is_part_of_contract=data_quality_rule.dq_is_part_of_contract,
    )
    # Categorize relationships by save semantic (REPLACE, APPEND, REMOVE)
    rel_fields: list[str] = [
        "dq_rule_template",
        "dq_rule_base_dataset",
        "dq_rule_base_column",
        "dq_rule_reference_datasets",
        "dq_rule_reference_columns",
    ]
    replace_rels, append_rels, remove_rels = categorize_relationships(
        data_quality_rule, rel_fields, DataQualityRuleRelationshipAttributes
    )
    return DataQualityRuleNested(
        guid=data_quality_rule.guid,
        type_name=data_quality_rule.type_name,
        status=data_quality_rule.status,
        version=data_quality_rule.version,
        create_time=data_quality_rule.create_time,
        update_time=data_quality_rule.update_time,
        created_by=data_quality_rule.created_by,
        updated_by=data_quality_rule.updated_by,
        classifications=data_quality_rule.classifications,
        classification_names=data_quality_rule.classification_names,
        meanings=data_quality_rule.meanings,
        labels=data_quality_rule.labels,
        business_attributes=data_quality_rule.business_attributes,
        custom_attributes=data_quality_rule.custom_attributes,
        pending_tasks=data_quality_rule.pending_tasks,
        proxy=data_quality_rule.proxy,
        is_incomplete=data_quality_rule.is_incomplete,
        provenance_type=data_quality_rule.provenance_type,
        home_id=data_quality_rule.home_id,
        attributes=attrs,
        relationship_attributes=replace_rels,
        append_relationship_attributes=append_rels,
        remove_relationship_attributes=remove_rels,
    )


def _data_quality_rule_from_nested(nested: DataQualityRuleNested) -> DataQualityRule:
    """Convert nested format to flat DataQualityRule."""
    attrs = (
        nested.attributes
        if nested.attributes is not UNSET
        else DataQualityRuleAttributes()
    )
    # Merge relationships from all three buckets
    rel_fields: list[str] = [
        "dq_rule_template",
        "dq_rule_base_dataset",
        "dq_rule_base_column",
        "dq_rule_reference_datasets",
        "dq_rule_reference_columns",
    ]
    merged_rels = merge_relationships(
        nested.relationship_attributes,
        nested.append_relationship_attributes,
        nested.remove_relationship_attributes,
        rel_fields,
        DataQualityRuleRelationshipAttributes,
    )
    return DataQualityRule(
        guid=nested.guid,
        type_name=nested.type_name,
        status=nested.status,
        version=nested.version,
        create_time=nested.create_time,
        update_time=nested.update_time,
        created_by=nested.created_by,
        updated_by=nested.updated_by,
        classifications=nested.classifications,
        classification_names=nested.classification_names,
        meanings=nested.meanings,
        labels=nested.labels,
        business_attributes=nested.business_attributes,
        custom_attributes=nested.custom_attributes,
        pending_tasks=nested.pending_tasks,
        proxy=nested.proxy,
        is_incomplete=nested.is_incomplete,
        provenance_type=nested.provenance_type,
        home_id=nested.home_id,
        dq_rule_base_dataset_qualified_name=attrs.dq_rule_base_dataset_qualified_name,
        dq_rule_base_column_qualified_name=attrs.dq_rule_base_column_qualified_name,
        dq_rule_reference_dataset_qualified_names=attrs.dq_rule_reference_dataset_qualified_names,
        dq_rule_reference_column_qualified_names=attrs.dq_rule_reference_column_qualified_names,
        dq_rule_source_sync_status=attrs.dq_rule_source_sync_status,
        dq_rule_source_sync_error_code=attrs.dq_rule_source_sync_error_code,
        dq_rule_source_sync_error_message=attrs.dq_rule_source_sync_error_message,
        dq_rule_source_sync_raw_error=attrs.dq_rule_source_sync_raw_error,
        dq_rule_source_synced_at=attrs.dq_rule_source_synced_at,
        dq_rule_latest_result=attrs.dq_rule_latest_result,
        dq_rule_latest_result_computed_at=attrs.dq_rule_latest_result_computed_at,
        dq_rule_latest_result_fetched_at=attrs.dq_rule_latest_result_fetched_at,
        dq_rule_latest_metric_value=attrs.dq_rule_latest_metric_value,
        dq_rule_latest_metric_value_computed_at=attrs.dq_rule_latest_metric_value_computed_at,
        dq_rule_dimension=attrs.dq_rule_dimension,
        dq_rule_template_name=attrs.dq_rule_template_name,
        dq_rule_status=attrs.dq_rule_status,
        dq_rule_alert_priority=attrs.dq_rule_alert_priority,
        dq_rule_config_arguments=attrs.dq_rule_config_arguments,
        dq_rule_custom_sql=attrs.dq_rule_custom_sql,
        dq_rule_custom_sql_return_type=attrs.dq_rule_custom_sql_return_type,
        dq_rule_failed_rows_sql=attrs.dq_rule_failed_rows_sql,
        dq_rule_row_scope_filtering_enabled=attrs.dq_rule_row_scope_filtering_enabled,
        dq_is_part_of_contract=attrs.dq_is_part_of_contract,
        # Merged relationship attributes
        **merged_rels,
    )


def _data_quality_rule_to_nested_bytes(
    data_quality_rule: DataQualityRule, serde: Serde
) -> bytes:
    """Convert flat DataQualityRule to nested JSON bytes."""
    return serde.encode(_data_quality_rule_to_nested(data_quality_rule))


def _data_quality_rule_from_nested_bytes(data: bytes, serde: Serde) -> DataQualityRule:
    """Convert nested JSON bytes to flat DataQualityRule."""
    nested = serde.decode(data, DataQualityRuleNested)
    return _data_quality_rule_from_nested(nested)


# Deferred import to avoid circular dependency
from .data_quality_rule_template import DataQualityRuleTemplate  # noqa: E402, F401
