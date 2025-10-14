# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

import json
import time
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.errors import ErrorCode
from pyatlan.model.enums import (
    DataQualityDimension,
    DataQualityResult,
    DataQualityRuleAlertPriority,
    DataQualityRuleStatus,
    DataQualityRuleThresholdCompareOperator,
    DataQualityRuleThresholdUnit,
    DataQualitySourceSyncStatus,
)
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.model.structs import (
    DataQualityRuleConfigArguments,
    DataQualityRuleThresholdObject,
)
from pyatlan.utils import init_guid, validate_required_fields

from .asset import SelfAsset
from .data_quality import DataQuality

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.assets import Column


class DataQualityRule(DataQuality):
    """Description"""

    @classmethod
    @init_guid
    def custom_sql_creator(
        cls,
        *,
        client: AtlanClient,
        rule_name: str,
        asset: Asset,
        custom_sql: str,
        threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
        dimension: DataQualityDimension,
        description: Optional[str] = None,
    ) -> DataQualityRule:
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

        attributes = DataQualityRule.Attributes.creator(
            client=client,
            rule_name=rule_name,
            rule_type="Custom SQL",
            asset=asset,
            threshold_compare_operator=threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            dimension=dimension,
            custom_sql=custom_sql,
            description=description,
            column=None,
            threshold_unit=None,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def table_level_rule_creator(
        cls,
        *,
        client: AtlanClient,
        rule_type: str,
        asset: Asset,
        threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
        threshold_value: int,
        alert_priority: DataQualityRuleAlertPriority,
    ) -> DataQualityRule:
        validate_required_fields(
            [
                "client",
                "rule_type",
                "asset",
                "threshold_compare_operator",
                "threshold_value",
                "alert_priority",
            ],
            [
                client,
                rule_type,
                asset,
                threshold_compare_operator,
                threshold_value,
                alert_priority,
            ],
        )

        attributes = DataQualityRule.Attributes.creator(
            client=client,
            rule_type=rule_type,
            asset=asset,
            threshold_compare_operator=threshold_compare_operator,
            threshold_value=threshold_value,
            alert_priority=alert_priority,
            rule_name=None,
            column=None,
            threshold_unit=None,
            dimension=None,
            custom_sql=None,
            description=None,
        )
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def column_level_rule_creator(
        cls,
        *,
        client: AtlanClient,
        rule_type: str,
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
    ) -> DataQualityRule:
        validate_required_fields(
            [
                "client",
                "rule_type",
                "asset",
                "column",
                "threshold_value",
                "alert_priority",
            ],
            [
                client,
                rule_type,
                asset,
                column,
                threshold_value,
                alert_priority,
            ],
        )
        template_config = client.dq_template_config_cache.get_template_config(rule_type)

        asset_for_validation = asset
        if row_scope_filtering_enabled and asset.qualified_name:
            from pyatlan.model.fluent_search import FluentSearch

            search_request = (
                FluentSearch()
                .where(Asset.QUALIFIED_NAME.eq(asset.qualified_name))
                .include_on_results(
                    Asset.ASSET_DQ_ROW_SCOPE_FILTER_COLUMN_QUALIFIED_NAME
                )
            ).to_request()
            results = client.asset.search(search_request)
            if results.count == 1:
                asset_for_validation = results.current_page()[0]

        validated_threshold_operator = (
            DataQualityRule.Attributes._validate_template_features(
                rule_type,
                rule_conditions,
                row_scope_filtering_enabled,
                template_config,
                threshold_compare_operator,
                asset_for_validation,
            )
        )

        final_threshold_compare_operator = (
            validated_threshold_operator
            or threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )

        attributes = DataQualityRule.Attributes.creator(
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
        return cls(attributes=attributes)

    @classmethod
    @init_guid
    def updater(
        cls: type[SelfAsset],
        client: AtlanClient,
        qualified_name: str,
        threshold_compare_operator: Optional[
            DataQualityRuleThresholdCompareOperator
        ] = None,
        threshold_value: Optional[int] = None,
        alert_priority: Optional[DataQualityRuleAlertPriority] = None,
        threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
        dimension: Optional[DataQualityDimension] = None,
        custom_sql: Optional[str] = None,
        rule_name: Optional[str] = None,
        description: Optional[str] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> SelfAsset:
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

        retrieved_custom_sql = search_result.dq_rule_custom_s_q_l  # type: ignore[attr-defined]
        retrieved_rule_name = search_result.display_name
        retrieved_dimension = search_result.dq_rule_dimension  # type: ignore[attr-defined]
        retrieved_column = search_result.dq_rule_base_column  # type: ignore[attr-defined]
        retrieved_alert_priority = search_result.dq_rule_alert_priority  # type: ignore[attr-defined]
        retrieved_row_scope_filtering_enabled = (
            search_result.dq_rule_row_scope_filtering_enabled  # type: ignore[attr-defined]
        )
        retrieved_description = search_result.user_description
        retrieved_asset = search_result.dq_rule_base_dataset  # type: ignore[attr-defined]
        retrieved_template_rule_name = search_result.dq_rule_template_name  # type: ignore[attr-defined]
        retrieved_template = search_result.dq_rule_template  # type: ignore[attr-defined]
        retrieved_threshold_compare_operator = (
            search_result.dq_rule_config_arguments.dq_rule_threshold_object.dq_rule_threshold_compare_operator  # type: ignore[attr-defined]
            if search_result.dq_rule_config_arguments is not None  # type: ignore[attr-defined]
            and search_result.dq_rule_config_arguments.dq_rule_threshold_object  # type: ignore[attr-defined]
            is not None
            else None
        )
        retrieved_threshold_value = (
            search_result.dq_rule_config_arguments.dq_rule_threshold_object.dq_rule_threshold_value  # type: ignore[attr-defined]
            if search_result.dq_rule_config_arguments is not None  # type: ignore[attr-defined]
            and search_result.dq_rule_config_arguments.dq_rule_threshold_object  # type: ignore[attr-defined]
            is not None
            else None
        )  # type: ignore[attr-defined]
        retrieved_threshold_unit = (
            search_result.dq_rule_config_arguments.dq_rule_threshold_object.dq_rule_threshold_unit  # type: ignore[attr-defined]
            if search_result.dq_rule_config_arguments is not None  # type: ignore[attr-defined]
            and search_result.dq_rule_config_arguments.dq_rule_threshold_object  # type: ignore[attr-defined]
            is not None
            else None
        )  # type: ignore[attr-defined]

        retrieved_rule_type = retrieved_template_rule_name
        template_config = client.dq_template_config_cache.get_template_config(
            retrieved_rule_type
        )
        validated_threshold_operator = (
            DataQualityRule.Attributes._validate_template_features(
                retrieved_rule_type,
                rule_conditions,
                row_scope_filtering_enabled,
                template_config,
                threshold_compare_operator or retrieved_threshold_compare_operator,
                retrieved_asset,
            )
        )

        final_compare_operator = (
            validated_threshold_operator
            or threshold_compare_operator
            or retrieved_threshold_compare_operator
            or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
        )

        attr_dq = cls.Attributes(
            name="",
            dq_rule_config_arguments=DataQualityRuleConfigArguments(
                dq_rule_threshold_object=DataQualityRuleThresholdObject(
                    dq_rule_threshold_compare_operator=final_compare_operator,
                    dq_rule_threshold_value=threshold_value
                    or retrieved_threshold_value,
                    dq_rule_threshold_unit=threshold_unit or retrieved_threshold_unit,
                ),
                dq_rule_config_rule_conditions=rule_conditions,
            ),
            dq_rule_base_dataset_qualified_name=retrieved_asset.qualified_name,
            dq_rule_alert_priority=alert_priority or retrieved_alert_priority,
            dq_rule_row_scope_filtering_enabled=row_scope_filtering_enabled
            or retrieved_row_scope_filtering_enabled,
            dq_rule_base_dataset=retrieved_asset,
            qualified_name=qualified_name,
            dq_rule_dimension=dimension or retrieved_dimension,
            dq_rule_template_name=retrieved_template_rule_name,
            dq_rule_template=DataQualityRuleTemplate.ref_by_qualified_name(
                qualified_name=retrieved_template.qualified_name
            ),
        )

        if retrieved_column is not None:
            attr_dq.dq_rule_base_column_qualified_name = retrieved_column.qualified_name
            attr_dq.dq_rule_base_column = retrieved_column  # type: ignore

        custom_sql = custom_sql or retrieved_custom_sql
        if custom_sql is not None:
            attr_dq.dq_rule_custom_s_q_l = custom_sql
            attr_dq.display_name = rule_name or retrieved_rule_name
            if description is not None:
                attr_dq.user_description = description or retrieved_description

        return cls(attributes=attr_dq)

    type_name: str = Field(default="DataQualityRule", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataQualityRule":
            raise ValueError("must be DataQualityRule")
        return v

    def __setattr__(self, name, value):
        if name in DataQualityRule._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DQ_RULE_BASE_DATASET_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dqRuleBaseDatasetQualifiedName",
        "dqRuleBaseDatasetQualifiedName",
        "dqRuleBaseDatasetQualifiedName.text",
    )
    """
    Base dataset qualified name that attached to this rule.
    """
    DQ_RULE_BASE_COLUMN_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dqRuleBaseColumnQualifiedName",
        "dqRuleBaseColumnQualifiedName",
        "dqRuleBaseColumnQualifiedName.text",
    )
    """
    Base column qualified name that attached to this rule.
    """
    DQ_RULE_REFERENCE_DATASET_QUALIFIED_NAMES: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "dqRuleReferenceDatasetQualifiedNames",
            "dqRuleReferenceDatasetQualifiedNames",
            "dqRuleReferenceDatasetQualifiedNames.text",
        )
    )
    """
    List of unique reference dataset's qualified names related to this rule.
    """
    DQ_RULE_REFERENCE_COLUMN_QUALIFIED_NAMES: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "dqRuleReferenceColumnQualifiedNames",
            "dqRuleReferenceColumnQualifiedNames",
            "dqRuleReferenceColumnQualifiedNames.text",
        )
    )
    """
    List of unique reference column's qualified names related to this rule.
    """
    DQ_RULE_SOURCE_SYNC_STATUS: ClassVar[KeywordField] = KeywordField(
        "dqRuleSourceSyncStatus", "dqRuleSourceSyncStatus"
    )
    """
    Latest sync status of the rule to the source.
    """
    DQ_RULE_SOURCE_SYNC_ERROR_CODE: ClassVar[KeywordField] = KeywordField(
        "dqRuleSourceSyncErrorCode", "dqRuleSourceSyncErrorCode"
    )
    """
    Error code in the case of state being "failure".
    """
    DQ_RULE_SOURCE_SYNC_ERROR_MESSAGE: ClassVar[KeywordField] = KeywordField(
        "dqRuleSourceSyncErrorMessage", "dqRuleSourceSyncErrorMessage"
    )
    """
    Error message in the case of state being "error".
    """
    DQ_RULE_SOURCE_SYNC_RAW_ERROR: ClassVar[KeywordField] = KeywordField(
        "dqRuleSourceSyncRawError", "dqRuleSourceSyncRawError"
    )
    """
    Raw error message from the source.
    """
    DQ_RULE_SOURCE_SYNCED_AT: ClassVar[NumericField] = NumericField(
        "dqRuleSourceSyncedAt", "dqRuleSourceSyncedAt"
    )
    """
    Time (epoch) at which the rule synced to the source.
    """
    DQ_RULE_LATEST_RESULT: ClassVar[KeywordField] = KeywordField(
        "dqRuleLatestResult", "dqRuleLatestResult"
    )
    """
    Latest result of the rule.
    """
    DQ_RULE_LATEST_RESULT_COMPUTED_AT: ClassVar[NumericField] = NumericField(
        "dqRuleLatestResultComputedAt", "dqRuleLatestResultComputedAt"
    )
    """
    Time (epoch) at which the latest rule result was evaluated.
    """
    DQ_RULE_LATEST_RESULT_FETCHED_AT: ClassVar[NumericField] = NumericField(
        "dqRuleLatestResultFetchedAt", "dqRuleLatestResultFetchedAt"
    )
    """
    Time (epoch) at which the latest rule result was fetched.
    """
    DQ_RULE_LATEST_METRIC_VALUE: ClassVar[KeywordField] = KeywordField(
        "dqRuleLatestMetricValue", "dqRuleLatestMetricValue"
    )
    """
    Last result metrics value of the rule.
    """
    DQ_RULE_LATEST_METRIC_VALUE_COMPUTED_AT: ClassVar[NumericField] = NumericField(
        "dqRuleLatestMetricValueComputedAt", "dqRuleLatestMetricValueComputedAt"
    )
    """
    Time (epoch) at which the latest metric value was evaluated in the source.
    """
    DQ_RULE_DIMENSION: ClassVar[KeywordField] = KeywordField(
        "dqRuleDimension", "dqRuleDimension"
    )
    """
    Dimension of the data quality rule.
    """
    DQ_RULE_TEMPLATE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dqRuleTemplateName", "dqRuleTemplateName", "dqRuleTemplateName.text"
    )
    """
    Name of the rule template corresponding to the rule.
    """
    DQ_RULE_STATUS: ClassVar[KeywordField] = KeywordField(
        "dqRuleStatus", "dqRuleStatus"
    )
    """
    Status of the rule.
    """
    DQ_RULE_ALERT_PRIORITY: ClassVar[KeywordField] = KeywordField(
        "dqRuleAlertPriority", "dqRuleAlertPriority"
    )
    """
    Default priority level for alerts involving this rule.
    """
    DQ_RULE_CONFIG_ARGUMENTS: ClassVar[KeywordField] = KeywordField(
        "dqRuleConfigArguments", "dqRuleConfigArguments"
    )
    """
    Json string of the rule config that contains the rule definitions.
    """
    DQ_RULE_CUSTOM_SQL: ClassVar[KeywordField] = KeywordField(
        "dqRuleCustomSQL", "dqRuleCustomSQL"
    )
    """
    SQL code for custom SQL rules.
    """
    DQ_RULE_ROW_SCOPE_FILTERING_ENABLED: ClassVar[BooleanField] = BooleanField(
        "dqRuleRowScopeFilteringEnabled", "dqRuleRowScopeFilteringEnabled"
    )
    """
    Whether row scope filtering is enabled for this data quality rule (true) or not (false).
    """

    DQ_RULE_BASE_DATASET: ClassVar[RelationField] = RelationField("dqRuleBaseDataset")
    """
    TBC
    """
    DQ_RULE_REFERENCE_DATASETS: ClassVar[RelationField] = RelationField(
        "dqRuleReferenceDatasets"
    )
    """
    TBC
    """
    DQ_RULE_TEMPLATE: ClassVar[RelationField] = RelationField("dqRuleTemplate")
    """
    TBC
    """
    DQ_RULE_BASE_COLUMN: ClassVar[RelationField] = RelationField("dqRuleBaseColumn")
    """
    TBC
    """
    DQ_RULE_REFERENCE_COLUMNS: ClassVar[RelationField] = RelationField(
        "dqRuleReferenceColumns"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dq_rule_base_dataset_qualified_name",
        "dq_rule_base_column_qualified_name",
        "dq_rule_reference_dataset_qualified_names",
        "dq_rule_reference_column_qualified_names",
        "dq_rule_source_sync_status",
        "dq_rule_source_sync_error_code",
        "dq_rule_source_sync_error_message",
        "dq_rule_source_sync_raw_error",
        "dq_rule_source_synced_at",
        "dq_rule_latest_result",
        "dq_rule_latest_result_computed_at",
        "dq_rule_latest_result_fetched_at",
        "dq_rule_latest_metric_value",
        "dq_rule_latest_metric_value_computed_at",
        "dq_rule_dimension",
        "dq_rule_template_name",
        "dq_rule_status",
        "dq_rule_alert_priority",
        "dq_rule_config_arguments",
        "dq_rule_custom_s_q_l",
        "dq_rule_row_scope_filtering_enabled",
        "dq_rule_base_dataset",
        "dq_rule_reference_datasets",
        "dq_rule_template",
        "dq_rule_base_column",
        "dq_rule_reference_columns",
    ]

    @property
    def dq_rule_base_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_base_dataset_qualified_name
        )

    @dq_rule_base_dataset_qualified_name.setter
    def dq_rule_base_dataset_qualified_name(
        self, dq_rule_base_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_base_dataset_qualified_name = (
            dq_rule_base_dataset_qualified_name
        )

    @property
    def dq_rule_base_column_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_base_column_qualified_name
        )

    @dq_rule_base_column_qualified_name.setter
    def dq_rule_base_column_qualified_name(
        self, dq_rule_base_column_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_base_column_qualified_name = (
            dq_rule_base_column_qualified_name
        )

    @property
    def dq_rule_reference_dataset_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_reference_dataset_qualified_names
        )

    @dq_rule_reference_dataset_qualified_names.setter
    def dq_rule_reference_dataset_qualified_names(
        self, dq_rule_reference_dataset_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_reference_dataset_qualified_names = (
            dq_rule_reference_dataset_qualified_names
        )

    @property
    def dq_rule_reference_column_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_reference_column_qualified_names
        )

    @dq_rule_reference_column_qualified_names.setter
    def dq_rule_reference_column_qualified_names(
        self, dq_rule_reference_column_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_reference_column_qualified_names = (
            dq_rule_reference_column_qualified_names
        )

    @property
    def dq_rule_source_sync_status(self) -> Optional[DataQualitySourceSyncStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_source_sync_status
        )

    @dq_rule_source_sync_status.setter
    def dq_rule_source_sync_status(
        self, dq_rule_source_sync_status: Optional[DataQualitySourceSyncStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_source_sync_status = dq_rule_source_sync_status

    @property
    def dq_rule_source_sync_error_code(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_source_sync_error_code
        )

    @dq_rule_source_sync_error_code.setter
    def dq_rule_source_sync_error_code(
        self, dq_rule_source_sync_error_code: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_source_sync_error_code = dq_rule_source_sync_error_code

    @property
    def dq_rule_source_sync_error_message(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_source_sync_error_message
        )

    @dq_rule_source_sync_error_message.setter
    def dq_rule_source_sync_error_message(
        self, dq_rule_source_sync_error_message: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_source_sync_error_message = (
            dq_rule_source_sync_error_message
        )

    @property
    def dq_rule_source_sync_raw_error(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_source_sync_raw_error
        )

    @dq_rule_source_sync_raw_error.setter
    def dq_rule_source_sync_raw_error(
        self, dq_rule_source_sync_raw_error: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_source_sync_raw_error = dq_rule_source_sync_raw_error

    @property
    def dq_rule_source_synced_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_source_synced_at
        )

    @dq_rule_source_synced_at.setter
    def dq_rule_source_synced_at(self, dq_rule_source_synced_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_source_synced_at = dq_rule_source_synced_at

    @property
    def dq_rule_latest_result(self) -> Optional[DataQualityResult]:
        return (
            None if self.attributes is None else self.attributes.dq_rule_latest_result
        )

    @dq_rule_latest_result.setter
    def dq_rule_latest_result(self, dq_rule_latest_result: Optional[DataQualityResult]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_latest_result = dq_rule_latest_result

    @property
    def dq_rule_latest_result_computed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_latest_result_computed_at
        )

    @dq_rule_latest_result_computed_at.setter
    def dq_rule_latest_result_computed_at(
        self, dq_rule_latest_result_computed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_latest_result_computed_at = (
            dq_rule_latest_result_computed_at
        )

    @property
    def dq_rule_latest_result_fetched_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_latest_result_fetched_at
        )

    @dq_rule_latest_result_fetched_at.setter
    def dq_rule_latest_result_fetched_at(
        self, dq_rule_latest_result_fetched_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_latest_result_fetched_at = (
            dq_rule_latest_result_fetched_at
        )

    @property
    def dq_rule_latest_metric_value(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_latest_metric_value
        )

    @dq_rule_latest_metric_value.setter
    def dq_rule_latest_metric_value(self, dq_rule_latest_metric_value: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_latest_metric_value = dq_rule_latest_metric_value

    @property
    def dq_rule_latest_metric_value_computed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_latest_metric_value_computed_at
        )

    @dq_rule_latest_metric_value_computed_at.setter
    def dq_rule_latest_metric_value_computed_at(
        self, dq_rule_latest_metric_value_computed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_latest_metric_value_computed_at = (
            dq_rule_latest_metric_value_computed_at
        )

    @property
    def dq_rule_dimension(self) -> Optional[DataQualityDimension]:
        return None if self.attributes is None else self.attributes.dq_rule_dimension

    @dq_rule_dimension.setter
    def dq_rule_dimension(self, dq_rule_dimension: Optional[DataQualityDimension]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_dimension = dq_rule_dimension

    @property
    def dq_rule_template_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dq_rule_template_name
        )

    @dq_rule_template_name.setter
    def dq_rule_template_name(self, dq_rule_template_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_template_name = dq_rule_template_name

    @property
    def dq_rule_status(self) -> Optional[DataQualityRuleStatus]:
        return None if self.attributes is None else self.attributes.dq_rule_status

    @dq_rule_status.setter
    def dq_rule_status(self, dq_rule_status: Optional[DataQualityRuleStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_status = dq_rule_status

    @property
    def dq_rule_alert_priority(self) -> Optional[DataQualityRuleAlertPriority]:
        return (
            None if self.attributes is None else self.attributes.dq_rule_alert_priority
        )

    @dq_rule_alert_priority.setter
    def dq_rule_alert_priority(
        self, dq_rule_alert_priority: Optional[DataQualityRuleAlertPriority]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_alert_priority = dq_rule_alert_priority

    @property
    def dq_rule_config_arguments(self) -> Optional[DataQualityRuleConfigArguments]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_config_arguments
        )

    @dq_rule_config_arguments.setter
    def dq_rule_config_arguments(
        self, dq_rule_config_arguments: Optional[DataQualityRuleConfigArguments]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_config_arguments = dq_rule_config_arguments

    @property
    def dq_rule_custom_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dq_rule_custom_s_q_l

    @dq_rule_custom_s_q_l.setter
    def dq_rule_custom_s_q_l(self, dq_rule_custom_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_custom_s_q_l = dq_rule_custom_s_q_l

    @property
    def dq_rule_row_scope_filtering_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_row_scope_filtering_enabled
        )

    @dq_rule_row_scope_filtering_enabled.setter
    def dq_rule_row_scope_filtering_enabled(
        self, dq_rule_row_scope_filtering_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_row_scope_filtering_enabled = (
            dq_rule_row_scope_filtering_enabled
        )

    @property
    def dq_rule_base_dataset(self) -> Optional[Asset]:
        return None if self.attributes is None else self.attributes.dq_rule_base_dataset

    @dq_rule_base_dataset.setter
    def dq_rule_base_dataset(self, dq_rule_base_dataset: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_base_dataset = dq_rule_base_dataset

    @property
    def dq_rule_reference_datasets(self) -> Optional[List[Asset]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_reference_datasets
        )

    @dq_rule_reference_datasets.setter
    def dq_rule_reference_datasets(
        self, dq_rule_reference_datasets: Optional[List[Asset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_reference_datasets = dq_rule_reference_datasets

    @property
    def dq_rule_template(self) -> Optional[DataQualityRuleTemplate]:
        return None if self.attributes is None else self.attributes.dq_rule_template

    @dq_rule_template.setter
    def dq_rule_template(self, dq_rule_template: Optional[DataQualityRuleTemplate]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_template = dq_rule_template

    @property
    def dq_rule_base_column(self) -> Optional[Column]:
        return None if self.attributes is None else self.attributes.dq_rule_base_column

    @dq_rule_base_column.setter
    def dq_rule_base_column(self, dq_rule_base_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_base_column = dq_rule_base_column

    @property
    def dq_rule_reference_columns(self) -> Optional[List[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dq_rule_reference_columns
        )

    @dq_rule_reference_columns.setter
    def dq_rule_reference_columns(
        self, dq_rule_reference_columns: Optional[List[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dq_rule_reference_columns = dq_rule_reference_columns

    class Attributes(DataQuality.Attributes):
        dq_rule_base_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dq_rule_base_column_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        dq_rule_reference_dataset_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        dq_rule_reference_column_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        dq_rule_source_sync_status: Optional[DataQualitySourceSyncStatus] = Field(
            default=None, description=""
        )
        dq_rule_source_sync_error_code: Optional[str] = Field(
            default=None, description=""
        )
        dq_rule_source_sync_error_message: Optional[str] = Field(
            default=None, description=""
        )
        dq_rule_source_sync_raw_error: Optional[str] = Field(
            default=None, description=""
        )
        dq_rule_source_synced_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dq_rule_latest_result: Optional[DataQualityResult] = Field(
            default=None, description=""
        )
        dq_rule_latest_result_computed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dq_rule_latest_result_fetched_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dq_rule_latest_metric_value: Optional[str] = Field(default=None, description="")
        dq_rule_latest_metric_value_computed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dq_rule_dimension: Optional[DataQualityDimension] = Field(
            default=None, description=""
        )
        dq_rule_template_name: Optional[str] = Field(default=None, description="")
        dq_rule_status: Optional[DataQualityRuleStatus] = Field(
            default=None, description=""
        )
        dq_rule_alert_priority: Optional[DataQualityRuleAlertPriority] = Field(
            default=None, description=""
        )
        dq_rule_config_arguments: Optional[DataQualityRuleConfigArguments] = Field(
            default=None, description=""
        )
        dq_rule_custom_s_q_l: Optional[str] = Field(default=None, description="")
        dq_rule_row_scope_filtering_enabled: Optional[bool] = Field(
            default=None, description=""
        )
        dq_rule_base_dataset: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship
        dq_rule_reference_datasets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship
        dq_rule_template: Optional[DataQualityRuleTemplate] = Field(
            default=None, description=""
        )  # relationship
        dq_rule_base_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        dq_rule_reference_columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship

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
            rule_type: str,
            rule_conditions: Optional[str],
            row_scope_filtering_enabled: Optional[bool],
            template_config: Optional[dict],
            threshold_compare_operator: Optional[
                DataQualityRuleThresholdCompareOperator
            ] = None,
            asset: Optional[Asset] = None,
        ) -> Optional[DataQualityRuleThresholdCompareOperator]:
            if not template_config or not template_config.get("config"):
                return None

            config = template_config["config"]

            if (
                rule_conditions
                and config.dq_rule_template_config_rule_conditions is None
            ):
                raise ErrorCode.DQ_RULE_TYPE_NOT_SUPPORTED.exception_with_parameters(
                    rule_type, "rule conditions"
                )

            if row_scope_filtering_enabled:
                advanced_settings = (
                    config.dq_rule_template_config_advanced_settings or ""
                )
                if "dqRuleRowScopeFilteringEnabled" not in str(advanced_settings):
                    raise ErrorCode.DQ_RULE_TYPE_NOT_SUPPORTED.exception_with_parameters(
                        rule_type, "row scope filtering"
                    )

                if asset and not getattr(
                    asset,
                    "asset_d_q_row_scope_filter_column_qualified_name",
                    None,
                ):
                    raise ErrorCode.DQ_ROW_SCOPE_FILTER_COLUMN_MISSING.exception_with_parameters(
                        getattr(asset, "qualified_name", "unknown")
                    )

            if rule_conditions:
                allowed_rule_conditions = (
                    DataQualityRule.Attributes._get_template_config_value(
                        config.dq_rule_template_config_rule_conditions or "",
                        None,
                        "enum",
                    )
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
                allowed_operators = (
                    DataQualityRule.Attributes._get_template_config_value(
                        config.dq_rule_template_config_threshold_object,
                        "dqRuleTemplateConfigThresholdCompareOperator",
                        "enum",
                    )
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
                default_value = DataQualityRule.Attributes._get_template_config_value(
                    config.dq_rule_template_config_threshold_object,
                    "dqRuleTemplateConfigThresholdCompareOperator",
                    "default",
                )
                if default_value:
                    threshold_compare_operator = (
                        DataQualityRuleThresholdCompareOperator(default_value)
                    )

            return (
                threshold_compare_operator
                or DataQualityRuleThresholdCompareOperator.LESS_THAN_EQUAL
            )

        @staticmethod
        def _generate_uuid():
            d = int(time.time() * 1000)
            random_bytes = uuid.uuid4().bytes
            rand_index = 0

            def replace_char(c):
                nonlocal d, rand_index
                r = (d + random_bytes[rand_index % 16]) % 16
                rand_index += 1
                d = d // 16
                if c == "x":
                    return hex(r)[2:]
                elif c == "y":
                    return hex((r & 0x3) | 0x8)[2:]  # y -> 8 to b
                else:
                    return c

            template = "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx"
            uuid_str = "".join(replace_char(c) if c in "xy" else c for c in template)
            return uuid_str

        @classmethod
        @init_guid
        def creator(
            cls,
            *,
            client: AtlanClient,
            rule_name: str,
            rule_type: str,
            asset: Asset,
            threshold_compare_operator: DataQualityRuleThresholdCompareOperator,
            threshold_value: int,
            alert_priority: DataQualityRuleAlertPriority,
            column: Optional[Asset] = None,
            threshold_unit: Optional[DataQualityRuleThresholdUnit] = None,
            dimension: Optional[DataQualityDimension] = None,
            custom_sql: Optional[str] = None,
            description: Optional[str] = None,
            rule_conditions: Optional[str] = None,
            row_scope_filtering_enabled: Optional[bool] = False,
        ) -> DataQualityRule.Attributes:
            template_config = client.dq_template_config_cache.get_template_config(
                rule_type
            )

            if template_config is None:
                raise ErrorCode.DQ_RULE_NOT_FOUND.exception_with_parameters(rule_type)

            template_rule_name = template_config.get("name")
            template_qualified_name = template_config.get("qualified_name")

            if dimension is None:
                dimension = template_config.get("dimension")

            if threshold_unit is None:
                config = template_config.get("config")
                if config is not None:
                    threshold_unit = (
                        DataQualityRule.Attributes._get_template_config_value(
                            config.dq_rule_template_config_threshold_object,
                            "dqRuleTemplateConfigThresholdUnit",
                            "default",
                        )
                    )

            attr_dq = DataQualityRule.Attributes(
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
                qualified_name=f"{asset.qualified_name}/rule/{str(cls._generate_uuid())}",
                dq_rule_dimension=dimension,
                dq_rule_template_name=template_rule_name,
                dq_rule_template=DataQualityRuleTemplate.ref_by_qualified_name(
                    qualified_name=template_qualified_name  # type: ignore
                ),
            )

            if column is not None:
                attr_dq.dq_rule_base_column_qualified_name = column.qualified_name
                attr_dq.dq_rule_base_column = column  # type: ignore

            if custom_sql is not None:
                attr_dq.dq_rule_custom_s_q_l = custom_sql
                attr_dq.display_name = rule_name
                if description is not None:
                    attr_dq.user_description = description

            return attr_dq

    attributes: DataQualityRule.Attributes = Field(
        default_factory=lambda: DataQualityRule.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa: E402, F401

# from .column import Column  # noqa: E402, F401
from .data_quality_rule_template import DataQualityRuleTemplate  # noqa: E402, F401
