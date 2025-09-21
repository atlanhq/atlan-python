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
    alpha_DQDimension,
    alpha_DQResult,
    alpha_DQRuleAlertPriority,
    alpha_DQRuleStatus,
    alpha_DQRuleThresholdCompareOperator,
    alpha_DQRuleThresholdUnit,
    alpha_DQSourceSyncStatus,
)
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import (
    alpha_DQRuleConfigArguments,
    alpha_DQRuleThresholdObject,
)
from pyatlan.utils import init_guid, validate_required_fields

from .asset import SelfAsset
from .data_quality import DataQuality

if TYPE_CHECKING:
    from pyatlan.client.atlan import AtlanClient
    from pyatlan.model.assets import Asset, Column


class alpha_DQRule(DataQuality):
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
        threshold_compare_operator: alpha_DQRuleThresholdCompareOperator,
        threshold_value: int,
        alert_priority: alpha_DQRuleAlertPriority,
        dimension: alpha_DQDimension,
        description: Optional[str] = None,
    ) -> alpha_DQRule:
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

        attributes = alpha_DQRule.Attributes.creator(
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
        threshold_compare_operator: alpha_DQRuleThresholdCompareOperator,
        threshold_value: int,
        alert_priority: alpha_DQRuleAlertPriority,
    ) -> alpha_DQRule:
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

        attributes = alpha_DQRule.Attributes.creator(
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
        alert_priority: alpha_DQRuleAlertPriority,
        threshold_compare_operator: Optional[
            alpha_DQRuleThresholdCompareOperator
        ] = None,
        threshold_unit: Optional[alpha_DQRuleThresholdUnit] = None,
        rule_conditions: Optional[str] = None,
        row_scope_filtering_enabled: Optional[bool] = False,
    ) -> alpha_DQRule:
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
                    Asset.ALPHAASSET_DQ_ROW_SCOPE_FILTER_COLUMN_QUALIFIED_NAME
                )
            ).to_request()
            results = client.asset.search(search_request)
            if results.count == 1:
                asset_for_validation = results.current_page()[0]

        threshold_compare_operator = (
            alpha_DQRule.Attributes._validate_template_features(
                rule_type,
                rule_conditions,
                row_scope_filtering_enabled,
                template_config,
                threshold_compare_operator,
                asset_for_validation,
            )
        )

        attributes = alpha_DQRule.Attributes.creator(
            client=client,
            rule_type=rule_type,
            asset=asset,
            column=column,
            threshold_compare_operator=threshold_compare_operator,
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
            alpha_DQRuleThresholdCompareOperator
        ] = None,
        threshold_value: Optional[int] = None,
        alert_priority: Optional[alpha_DQRuleAlertPriority] = None,
        threshold_unit: Optional[alpha_DQRuleThresholdUnit] = None,
        dimension: Optional[alpha_DQDimension] = None,
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
            .where(alpha_DQRule.QUALIFIED_NAME.eq(qualified_name))
            .include_on_results(alpha_DQRule.NAME)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_TEMPLATE_NAME)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_TEMPLATE)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_BASE_DATASET)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_BASE_COLUMN)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_ALERT_PRIORITY)
            .include_on_results(alpha_DQRule.DISPLAY_NAME)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_CUSTOM_SQL)
            .include_on_results(alpha_DQRule.USER_DESCRIPTION)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_DIMENSION)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_CONFIG_ARGUMENTS)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_ROW_SCOPE_FILTERING_ENABLED)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_SOURCE_SYNC_STATUS)
            .include_on_results(alpha_DQRule.ALPHADQ_RULE_STATUS)
        ).to_request()

        results = client.asset.search(request)

        if results.count != 1:
            raise ValueError(
                f"Expected exactly 1 asset for qualified_name: {qualified_name}, "
                f"but found: {results.count}"
            )
        search_result = results.current_page()[0]

        retrieved_custom_sql = search_result.alpha_dq_rule_custom_s_q_l  # type: ignore[attr-defined]
        retrieved_rule_name = search_result.display_name
        retrieved_dimension = search_result.alpha_dq_rule_dimension  # type: ignore[attr-defined]
        retrieved_column = search_result.alpha_dq_rule_base_column  # type: ignore[attr-defined]
        retrieved_alert_priority = search_result.alpha_dq_rule_alert_priority  # type: ignore[attr-defined]
        retrieved_row_scope_filtering_enabled = (
            search_result.alpha_dq_rule_row_scope_filtering_enabled  # type: ignore[attr-defined]
        )
        retrieved_description = search_result.user_description
        retrieved_asset = search_result.alpha_dq_rule_base_dataset  # type: ignore[attr-defined]
        retrieved_template_rule_name = search_result.alpha_dq_rule_template_name  # type: ignore[attr-defined]
        retrieved_template = search_result.alpha_dq_rule_template  # type: ignore[attr-defined]
        retrieved_threshold_compare_operator = (
            search_result.alpha_dq_rule_config_arguments.alpha_dq_rule_threshold_object.alpha_dq_rule_threshold_compare_operator  # type: ignore[attr-defined]
            if search_result.alpha_dq_rule_config_arguments is not None  # type: ignore[attr-defined]
            and search_result.alpha_dq_rule_config_arguments.alpha_dq_rule_threshold_object  # type: ignore[attr-defined]
            is not None
            else None
        )
        retrieved_threshold_value = (
            search_result.alpha_dq_rule_config_arguments.alpha_dq_rule_threshold_object.alpha_dq_rule_threshold_value  # type: ignore[attr-defined]
            if search_result.alpha_dq_rule_config_arguments is not None  # type: ignore[attr-defined]
            and search_result.alpha_dq_rule_config_arguments.alpha_dq_rule_threshold_object  # type: ignore[attr-defined]
            is not None
            else None
        )  # type: ignore[attr-defined]
        retrieved_threshold_unit = (
            search_result.alpha_dq_rule_config_arguments.alpha_dq_rule_threshold_object.alpha_dq_rule_threshold_unit  # type: ignore[attr-defined]
            if search_result.alpha_dq_rule_config_arguments is not None  # type: ignore[attr-defined]
            and search_result.alpha_dq_rule_config_arguments.alpha_dq_rule_threshold_object  # type: ignore[attr-defined]
            is not None
            else None
        )  # type: ignore[attr-defined]

        retrieved_rule_type = retrieved_template_rule_name
        template_config = client.dq_template_config_cache.get_template_config(
            retrieved_rule_type
        )
        validated_threshold_operator = (
            alpha_DQRule.Attributes._validate_template_features(
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
        )

        config_arguments_raw = alpha_DQRule.Attributes._generate_config_arguments_raw(
            is_alert_enabled=True,
            custom_sql=custom_sql or retrieved_custom_sql,
            display_name=rule_name or retrieved_rule_name,
            dimension=dimension or retrieved_dimension,
            compare_operator=final_compare_operator,
            threshold_value=threshold_value or retrieved_threshold_value,
            threshold_unit=threshold_unit or retrieved_threshold_unit,
            column=retrieved_column,
            dq_priority=alert_priority or retrieved_alert_priority,
            description=description or retrieved_description,
            rule_conditions=rule_conditions,
            row_scope_filtering_enabled=row_scope_filtering_enabled,
        )

        attr_dq = cls.Attributes(
            name="",
            alpha_dq_rule_config_arguments=alpha_DQRuleConfigArguments(
                alpha_dq_rule_threshold_object=alpha_DQRuleThresholdObject(
                    alpha_dq_rule_threshold_compare_operator=final_compare_operator,
                    alpha_dq_rule_threshold_value=threshold_value
                    or retrieved_threshold_value,
                    alpha_dq_rule_threshold_unit=threshold_unit
                    or retrieved_threshold_unit,
                ),
                alpha_dq_rule_config_arguments_raw=config_arguments_raw,
                alpha_dq_rule_config_rule_conditions=rule_conditions,
            ),
            alpha_dq_rule_base_dataset_qualified_name=retrieved_asset.qualified_name,
            alpha_dq_rule_alert_priority=alert_priority or retrieved_alert_priority,
            alpha_dq_rule_row_scope_filtering_enabled=row_scope_filtering_enabled
            or retrieved_row_scope_filtering_enabled,
            alpha_dq_rule_base_dataset=retrieved_asset,
            qualified_name=qualified_name,
            alpha_dq_rule_dimension=dimension or retrieved_dimension,
            alpha_dq_rule_template_name=retrieved_template_rule_name,
            alpha_dq_rule_template=alpha_DQRuleTemplate.ref_by_qualified_name(
                qualified_name=retrieved_template.qualified_name
            ),
        )

        if retrieved_column is not None:
            attr_dq.alpha_dq_rule_base_column_qualified_name = (
                retrieved_column.qualified_name
            )
            attr_dq.alpha_dq_rule_base_column = retrieved_column  # type: ignore

        custom_sql = custom_sql or retrieved_custom_sql
        if custom_sql is not None:
            attr_dq.alpha_dq_rule_custom_s_q_l = custom_sql
            attr_dq.display_name = rule_name or retrieved_rule_name
            if description is not None:
                attr_dq.user_description = description or retrieved_description

        return cls(attributes=attr_dq)

    type_name: str = Field(default="alpha_DQRule", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "alpha_DQRule":
            raise ValueError("must be alpha_DQRule")
        return v

    def __setattr__(self, name, value):
        if name in alpha_DQRule._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ALPHADQ_RULE_BASE_DATASET_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "alpha_dqRuleBaseDatasetQualifiedName",
            "alpha_dqRuleBaseDatasetQualifiedName",
            "alpha_dqRuleBaseDatasetQualifiedName.text",
        )
    )
    """
    Base dataset qualified name that attached to this rule.
    """
    ALPHADQ_RULE_BASE_COLUMN_QUALIFIED_NAME: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "alpha_dqRuleBaseColumnQualifiedName",
            "alpha_dqRuleBaseColumnQualifiedName",
            "alpha_dqRuleBaseColumnQualifiedName.text",
        )
    )
    """
    Base column qualified name that attached to this rule.
    """
    ALPHADQ_RULE_REFERENCE_DATASET_QUALIFIED_NAMES: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "alpha_dqRuleReferenceDatasetQualifiedNames",
            "alpha_dqRuleReferenceDatasetQualifiedNames",
            "alpha_dqRuleReferenceDatasetQualifiedNames.text",
        )
    )
    """
    List of unique reference dataset's qualified names related to this rule.
    """
    ALPHADQ_RULE_REFERENCE_COLUMN_QUALIFIED_NAMES: ClassVar[KeywordTextField] = (
        KeywordTextField(
            "alpha_dqRuleReferenceColumnQualifiedNames",
            "alpha_dqRuleReferenceColumnQualifiedNames",
            "alpha_dqRuleReferenceColumnQualifiedNames.text",
        )
    )
    """
    List of unique reference dataset's qualified names related to this rule.
    """
    ALPHADQ_RULE_ROW_SCOPE_FILTERING_ENABLED: ClassVar[BooleanField] = BooleanField(
        "alpha_dqRuleRowScopeFilteringEnabled", "alpha_dqRuleRowScopeFilteringEnabled"
    )
    """
    Flag to enable row scope filtering for the rule
    """
    ALPHADQ_RULE_SOURCE_SYNC_STATUS: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleSourceSyncStatus", "alpha_dqRuleSourceSyncStatus"
    )
    """
    Latest sync status of the rule to the source.
    """
    ALPHADQ_RULE_SOURCE_SYNC_ERROR_CODE: ClassVar[TextField] = TextField(
        "alpha_dqRuleSourceSyncErrorCode", "alpha_dqRuleSourceSyncErrorCode"
    )
    """
    Error code in the case of state being "failure".
    """
    ALPHADQ_RULE_SOURCE_SYNC_ERROR_MESSAGE: ClassVar[TextField] = TextField(
        "alpha_dqRuleSourceSyncErrorMessage", "alpha_dqRuleSourceSyncErrorMessage"
    )
    """
    Error message in the case of state being "error".
    """
    ALPHADQ_RULE_SOURCE_SYNCED_AT: ClassVar[NumericField] = NumericField(
        "alpha_dqRuleSourceSyncedAt", "alpha_dqRuleSourceSyncedAt"
    )
    """
    Time (epoch) at which the rule synced to the source.
    """
    ALPHADQ_RULE_LATEST_RESULT: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleLatestResult", "alpha_dqRuleLatestResult"
    )
    """
    Latest result of the rule.
    """
    ALPHADQ_RULE_LATEST_RESULT_COMPUTED_AT: ClassVar[NumericField] = NumericField(
        "alpha_dqRuleLatestResultComputedAt", "alpha_dqRuleLatestResultComputedAt"
    )
    """
    Time (epoch) at which the latest rule result was evaluated.
    """
    ALPHADQ_RULE_LATEST_RESULT_FETCHED_AT: ClassVar[NumericField] = NumericField(
        "alpha_dqRuleLatestResultFetchedAt", "alpha_dqRuleLatestResultFetchedAt"
    )
    """
    Time (epoch) at which the latest rule result was fetched.
    """
    ALPHADQ_RULE_LATEST_METRIC_VALUE: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleLatestMetricValue", "alpha_dqRuleLatestMetricValue"
    )
    """
    Last Result metrics value of the rule.
    """
    ALPHADQ_RULE_LATEST_METRIC_VALUE_COMPUTED_AT: ClassVar[NumericField] = NumericField(
        "alpha_dqRuleLatestMetricValueComputedAt",
        "alpha_dqRuleLatestMetricValueComputedAt",
    )
    """
    Time (epoch) at which the latest metric value was evaluated in the source.
    """
    ALPHADQ_RULE_DIMENSION: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleDimension", "alpha_dqRuleDimension"
    )
    """
    dimension of the data quality rule
    """
    ALPHADQ_RULE_TEMPLATE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "alpha_dqRuleTemplateName",
        "alpha_dqRuleTemplateName",
        "alpha_dqRuleTemplateName.text",
    )
    """
    Name of the rule template corresponding to the rule.
    """
    ALPHADQ_RULE_STATUS: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleStatus", "alpha_dqRuleStatus"
    )
    """
    Status of the rule.
    """
    ALPHADQ_RULE_ALERT_PRIORITY: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleAlertPriority", "alpha_dqRuleAlertPriority"
    )
    """
    Default priority level for alerts involving this rule.
    """
    ALPHADQ_RULE_CONFIG_ARGUMENTS: ClassVar[KeywordField] = KeywordField(
        "alpha_dqRuleConfigArguments", "alpha_dqRuleConfigArguments"
    )
    """
    Json string of the rule config that contains the rule definitions.
    """
    ALPHADQ_RULE_CUSTOM_SQL: ClassVar[TextField] = TextField(
        "alpha_dqRuleCustomSQL", "alpha_dqRuleCustomSQL"
    )
    """
    SQL code for custom SQL rules
    """

    ALPHADQ_RULE_REFERENCE_COLUMNS: ClassVar[RelationField] = RelationField(
        "alpha_dqRuleReferenceColumns"
    )
    """
    TBC
    """
    ALPHADQ_RULE_BASE_COLUMN: ClassVar[RelationField] = RelationField(
        "alpha_dqRuleBaseColumn"
    )
    """
    TBC
    """
    ALPHADQ_RULE_BASE_DATASET: ClassVar[RelationField] = RelationField(
        "alpha_dqRuleBaseDataset"
    )
    """
    TBC
    """
    ALPHADQ_RULE_TEMPLATE: ClassVar[RelationField] = RelationField(
        "alpha_dqRuleTemplate"
    )
    """
    TBC
    """
    ALPHADQ_RULE_REFERENCE_DATASETS: ClassVar[RelationField] = RelationField(
        "alpha_dqRuleReferenceDatasets"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "alpha_dq_rule_base_dataset_qualified_name",
        "alpha_dq_rule_base_column_qualified_name",
        "alpha_dq_rule_reference_dataset_qualified_names",
        "alpha_dq_rule_reference_column_qualified_names",
        "alpha_dq_rule_row_scope_filtering_enabled",
        "alpha_dq_rule_source_sync_status",
        "alpha_dq_rule_source_sync_error_code",
        "alpha_dq_rule_source_sync_error_message",
        "alpha_dq_rule_source_synced_at",
        "alpha_dq_rule_latest_result",
        "alpha_dq_rule_latest_result_computed_at",
        "alpha_dq_rule_latest_result_fetched_at",
        "alpha_dq_rule_latest_metric_value",
        "alpha_dq_rule_latest_metric_value_computed_at",
        "alpha_dq_rule_dimension",
        "alpha_dq_rule_template_name",
        "alpha_dq_rule_status",
        "alpha_dq_rule_alert_priority",
        "alpha_dq_rule_config_arguments",
        "alpha_dq_rule_custom_s_q_l",
        "alpha_dq_rule_reference_columns",
        "alpha_dq_rule_base_column",
        "alpha_dq_rule_base_dataset",
        "alpha_dq_rule_template",
        "alpha_dq_rule_reference_datasets",
    ]

    @property
    def alpha_dq_rule_base_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_base_dataset_qualified_name
        )

    @alpha_dq_rule_base_dataset_qualified_name.setter
    def alpha_dq_rule_base_dataset_qualified_name(
        self, alpha_dq_rule_base_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_base_dataset_qualified_name = (
            alpha_dq_rule_base_dataset_qualified_name
        )

    @property
    def alpha_dq_rule_base_column_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_base_column_qualified_name
        )

    @alpha_dq_rule_base_column_qualified_name.setter
    def alpha_dq_rule_base_column_qualified_name(
        self, alpha_dq_rule_base_column_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_base_column_qualified_name = (
            alpha_dq_rule_base_column_qualified_name
        )

    @property
    def alpha_dq_rule_reference_dataset_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_reference_dataset_qualified_names
        )

    @alpha_dq_rule_reference_dataset_qualified_names.setter
    def alpha_dq_rule_reference_dataset_qualified_names(
        self, alpha_dq_rule_reference_dataset_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_reference_dataset_qualified_names = (
            alpha_dq_rule_reference_dataset_qualified_names
        )

    @property
    def alpha_dq_rule_reference_column_qualified_names(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_reference_column_qualified_names
        )

    @alpha_dq_rule_reference_column_qualified_names.setter
    def alpha_dq_rule_reference_column_qualified_names(
        self, alpha_dq_rule_reference_column_qualified_names: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_reference_column_qualified_names = (
            alpha_dq_rule_reference_column_qualified_names
        )

    @property
    def alpha_dq_rule_row_scope_filtering_enabled(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_row_scope_filtering_enabled
        )

    @alpha_dq_rule_row_scope_filtering_enabled.setter
    def alpha_dq_rule_row_scope_filtering_enabled(
        self, alpha_dq_rule_row_scope_filtering_enabled: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_row_scope_filtering_enabled = (
            alpha_dq_rule_row_scope_filtering_enabled
        )

    @property
    def alpha_dq_rule_source_sync_status(self) -> Optional[alpha_DQSourceSyncStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_source_sync_status
        )

    @alpha_dq_rule_source_sync_status.setter
    def alpha_dq_rule_source_sync_status(
        self, alpha_dq_rule_source_sync_status: Optional[alpha_DQSourceSyncStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_source_sync_status = (
            alpha_dq_rule_source_sync_status
        )

    @property
    def alpha_dq_rule_source_sync_error_code(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_source_sync_error_code
        )

    @alpha_dq_rule_source_sync_error_code.setter
    def alpha_dq_rule_source_sync_error_code(
        self, alpha_dq_rule_source_sync_error_code: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_source_sync_error_code = (
            alpha_dq_rule_source_sync_error_code
        )

    @property
    def alpha_dq_rule_source_sync_error_message(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_source_sync_error_message
        )

    @alpha_dq_rule_source_sync_error_message.setter
    def alpha_dq_rule_source_sync_error_message(
        self, alpha_dq_rule_source_sync_error_message: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_source_sync_error_message = (
            alpha_dq_rule_source_sync_error_message
        )

    @property
    def alpha_dq_rule_source_synced_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_source_synced_at
        )

    @alpha_dq_rule_source_synced_at.setter
    def alpha_dq_rule_source_synced_at(
        self, alpha_dq_rule_source_synced_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_source_synced_at = alpha_dq_rule_source_synced_at

    @property
    def alpha_dq_rule_latest_result(self) -> Optional[alpha_DQResult]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_latest_result
        )

    @alpha_dq_rule_latest_result.setter
    def alpha_dq_rule_latest_result(
        self, alpha_dq_rule_latest_result: Optional[alpha_DQResult]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_latest_result = alpha_dq_rule_latest_result

    @property
    def alpha_dq_rule_latest_result_computed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_latest_result_computed_at
        )

    @alpha_dq_rule_latest_result_computed_at.setter
    def alpha_dq_rule_latest_result_computed_at(
        self, alpha_dq_rule_latest_result_computed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_latest_result_computed_at = (
            alpha_dq_rule_latest_result_computed_at
        )

    @property
    def alpha_dq_rule_latest_result_fetched_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_latest_result_fetched_at
        )

    @alpha_dq_rule_latest_result_fetched_at.setter
    def alpha_dq_rule_latest_result_fetched_at(
        self, alpha_dq_rule_latest_result_fetched_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_latest_result_fetched_at = (
            alpha_dq_rule_latest_result_fetched_at
        )

    @property
    def alpha_dq_rule_latest_metric_value(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_latest_metric_value
        )

    @alpha_dq_rule_latest_metric_value.setter
    def alpha_dq_rule_latest_metric_value(
        self, alpha_dq_rule_latest_metric_value: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_latest_metric_value = (
            alpha_dq_rule_latest_metric_value
        )

    @property
    def alpha_dq_rule_latest_metric_value_computed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_latest_metric_value_computed_at
        )

    @alpha_dq_rule_latest_metric_value_computed_at.setter
    def alpha_dq_rule_latest_metric_value_computed_at(
        self, alpha_dq_rule_latest_metric_value_computed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_latest_metric_value_computed_at = (
            alpha_dq_rule_latest_metric_value_computed_at
        )

    @property
    def alpha_dq_rule_dimension(self) -> Optional[alpha_DQDimension]:
        return (
            None if self.attributes is None else self.attributes.alpha_dq_rule_dimension
        )

    @alpha_dq_rule_dimension.setter
    def alpha_dq_rule_dimension(
        self, alpha_dq_rule_dimension: Optional[alpha_DQDimension]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_dimension = alpha_dq_rule_dimension

    @property
    def alpha_dq_rule_template_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_template_name
        )

    @alpha_dq_rule_template_name.setter
    def alpha_dq_rule_template_name(self, alpha_dq_rule_template_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_template_name = alpha_dq_rule_template_name

    @property
    def alpha_dq_rule_status(self) -> Optional[alpha_DQRuleStatus]:
        return None if self.attributes is None else self.attributes.alpha_dq_rule_status

    @alpha_dq_rule_status.setter
    def alpha_dq_rule_status(self, alpha_dq_rule_status: Optional[alpha_DQRuleStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_status = alpha_dq_rule_status

    @property
    def alpha_dq_rule_alert_priority(self) -> Optional[alpha_DQRuleAlertPriority]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_alert_priority
        )

    @alpha_dq_rule_alert_priority.setter
    def alpha_dq_rule_alert_priority(
        self, alpha_dq_rule_alert_priority: Optional[alpha_DQRuleAlertPriority]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_alert_priority = alpha_dq_rule_alert_priority

    @property
    def alpha_dq_rule_config_arguments(self) -> Optional[alpha_DQRuleConfigArguments]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_config_arguments
        )

    @alpha_dq_rule_config_arguments.setter
    def alpha_dq_rule_config_arguments(
        self, alpha_dq_rule_config_arguments: Optional[alpha_DQRuleConfigArguments]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_config_arguments = alpha_dq_rule_config_arguments

    @property
    def alpha_dq_rule_custom_s_q_l(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_custom_s_q_l
        )

    @alpha_dq_rule_custom_s_q_l.setter
    def alpha_dq_rule_custom_s_q_l(self, alpha_dq_rule_custom_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_custom_s_q_l = alpha_dq_rule_custom_s_q_l

    @property
    def alpha_dq_rule_reference_columns(self) -> Optional[List[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_reference_columns
        )

    @alpha_dq_rule_reference_columns.setter
    def alpha_dq_rule_reference_columns(
        self, alpha_dq_rule_reference_columns: Optional[List[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_reference_columns = (
            alpha_dq_rule_reference_columns
        )

    @property
    def alpha_dq_rule_base_column(self) -> Optional[Column]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_base_column
        )

    @alpha_dq_rule_base_column.setter
    def alpha_dq_rule_base_column(self, alpha_dq_rule_base_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_base_column = alpha_dq_rule_base_column

    @property
    def alpha_dq_rule_base_dataset(self) -> Optional[Asset]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_base_dataset
        )

    @alpha_dq_rule_base_dataset.setter
    def alpha_dq_rule_base_dataset(self, alpha_dq_rule_base_dataset: Optional[Asset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_base_dataset = alpha_dq_rule_base_dataset

    @property
    def alpha_dq_rule_template(self) -> Optional[alpha_DQRuleTemplate]:
        return (
            None if self.attributes is None else self.attributes.alpha_dq_rule_template
        )

    @alpha_dq_rule_template.setter
    def alpha_dq_rule_template(
        self, alpha_dq_rule_template: Optional[alpha_DQRuleTemplate]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_template = alpha_dq_rule_template

    @property
    def alpha_dq_rule_reference_datasets(self) -> Optional[List[Asset]]:
        return (
            None
            if self.attributes is None
            else self.attributes.alpha_dq_rule_reference_datasets
        )

    @alpha_dq_rule_reference_datasets.setter
    def alpha_dq_rule_reference_datasets(
        self, alpha_dq_rule_reference_datasets: Optional[List[Asset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.alpha_dq_rule_reference_datasets = (
            alpha_dq_rule_reference_datasets
        )

    class Attributes(DataQuality.Attributes):
        alpha_dq_rule_base_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        alpha_dq_rule_base_column_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        alpha_dq_rule_reference_dataset_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        alpha_dq_rule_reference_column_qualified_names: Optional[Set[str]] = Field(
            default=None, description=""
        )
        alpha_dq_rule_row_scope_filtering_enabled: Optional[bool] = Field(
            default=None, description=""
        )
        alpha_dq_rule_source_sync_status: Optional[alpha_DQSourceSyncStatus] = Field(
            default=None, description=""
        )
        alpha_dq_rule_source_sync_error_code: Optional[str] = Field(
            default=None, description=""
        )
        alpha_dq_rule_source_sync_error_message: Optional[str] = Field(
            default=None, description=""
        )
        alpha_dq_rule_source_synced_at: Optional[datetime] = Field(
            default=None, description=""
        )
        alpha_dq_rule_latest_result: Optional[alpha_DQResult] = Field(
            default=None, description=""
        )
        alpha_dq_rule_latest_result_computed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        alpha_dq_rule_latest_result_fetched_at: Optional[datetime] = Field(
            default=None, description=""
        )
        alpha_dq_rule_latest_metric_value: Optional[str] = Field(
            default=None, description=""
        )
        alpha_dq_rule_latest_metric_value_computed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        alpha_dq_rule_dimension: Optional[alpha_DQDimension] = Field(
            default=None, description=""
        )
        alpha_dq_rule_template_name: Optional[str] = Field(default=None, description="")
        alpha_dq_rule_status: Optional[alpha_DQRuleStatus] = Field(
            default=None, description=""
        )
        alpha_dq_rule_alert_priority: Optional[alpha_DQRuleAlertPriority] = Field(
            default=None, description=""
        )
        alpha_dq_rule_config_arguments: Optional[alpha_DQRuleConfigArguments] = Field(
            default=None, description=""
        )
        alpha_dq_rule_custom_s_q_l: Optional[str] = Field(default=None, description="")
        alpha_dq_rule_reference_columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        alpha_dq_rule_base_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        alpha_dq_rule_base_dataset: Optional[Asset] = Field(
            default=None, description=""
        )  # relationship
        alpha_dq_rule_template: Optional[alpha_DQRuleTemplate] = Field(
            default=None, description=""
        )  # relationship
        alpha_dq_rule_reference_datasets: Optional[List[Asset]] = Field(
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
                alpha_DQRuleThresholdCompareOperator
            ] = None,
            asset: Optional[Asset] = None,
        ) -> Optional[alpha_DQRuleThresholdCompareOperator]:
            if not template_config or not template_config.get("config"):
                return None

            config = template_config["config"]

            if (
                rule_conditions
                and config.alpha_dq_rule_template_config_rule_conditions is None
            ):
                raise ErrorCode.DQ_RULE_TYPE_NOT_SUPPORTED.exception_with_parameters(
                    rule_type, "rule conditions"
                )

            if row_scope_filtering_enabled:
                advanced_settings = (
                    config.alpha_dq_rule_template_advanced_settings or ""
                )
                if "alpha_dqRuleRowScopeFilteringEnabled" not in str(advanced_settings):
                    raise ErrorCode.DQ_RULE_TYPE_NOT_SUPPORTED.exception_with_parameters(
                        rule_type, "row scope filtering"
                    )

                if asset and not getattr(
                    asset,
                    "alpha_asset_d_q_row_scope_filter_column_qualified_name",
                    None,
                ):
                    raise ErrorCode.DQ_ROW_SCOPE_FILTER_COLUMN_MISSING.exception_with_parameters(
                        getattr(asset, "qualified_name", "unknown")
                    )

            if rule_conditions:
                allowed_rule_conditions = (
                    alpha_DQRule.Attributes._get_template_config_value(
                        config.alpha_dq_rule_template_config_rule_conditions or "",
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
                    return alpha_DQRuleThresholdCompareOperator.EQUAL
                elif (
                    threshold_compare_operator
                    != alpha_DQRuleThresholdCompareOperator.EQUAL
                ):
                    raise ErrorCode.INVALID_PARAMETER_VALUE.exception_with_parameters(
                        f"threshold_compare_operator={threshold_compare_operator.value}",
                        "threshold_compare_operator",
                        "EQUAL when rule_conditions are provided",
                    )

            if threshold_compare_operator is not None:
                allowed_operators = alpha_DQRule.Attributes._get_template_config_value(
                    config.alpha_dq_rule_template_config_threshold_object,
                    "alpha_dqRuleTemplateConfigThresholdCompareOperator",
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
                default_value = alpha_DQRule.Attributes._get_template_config_value(
                    config.alpha_dq_rule_template_config_threshold_object,
                    "alpha_dqRuleTemplateConfigThresholdCompareOperator",
                    "default",
                )
                if default_value:
                    threshold_compare_operator = alpha_DQRuleThresholdCompareOperator(
                        default_value
                    )

            return (
                threshold_compare_operator
                or alpha_DQRuleThresholdCompareOperator.LESS_THAN_EQUAL
            )

        @staticmethod
        def _generate_config_arguments_raw(
            *,
            is_alert_enabled: bool = True,
            custom_sql: Optional[str] = None,
            display_name: Optional[str] = None,
            dimension: Optional[alpha_DQDimension] = None,
            compare_operator: alpha_DQRuleThresholdCompareOperator,
            threshold_value: int,
            threshold_unit: Optional[alpha_DQRuleThresholdUnit] = None,
            column: Optional[Asset] = None,
            dq_priority: alpha_DQRuleAlertPriority,
            description: Optional[str] = None,
            rule_conditions: Optional[str] = None,
            row_scope_filtering_enabled: Optional[bool] = None,
        ) -> str:
            config = {
                "isAlertEnabled": is_alert_enabled,
                "alpha_dqRuleTemplateConfigThresholdObject": {
                    "alpha_dqRuleTemplateConfigThresholdCompareOperator": compare_operator,
                    "alpha_dqRuleTemplateConfigThresholdValue": threshold_value,
                    "alpha_dqRuleTemplateConfigThresholdUnit": threshold_unit,
                },
                "alpha_dqRuleTemplateAdvancedSettings.dqPriority": dq_priority,
            }

            if column is not None:
                config["alpha_dqRuleTemplateConfigBaseColumnQualifiedName"] = (
                    column.qualified_name
                )

            if description is not None:
                config["alpha_dqRuleTemplateConfigUserDescription"] = description

            if custom_sql is not None:
                config["alpha_dqRuleTemplateConfigCustomSQL"] = custom_sql

            if display_name is not None:
                config["alpha_dqRuleTemplateConfigDisplayName"] = display_name

            if dimension is not None:
                config["alpha_dqRuleTemplateConfigDimension"] = dimension

            if rule_conditions is not None:
                config["alpha_dqRuleTemplateConfigRuleConditions"] = json.loads(
                    rule_conditions
                )

            if row_scope_filtering_enabled is not None:
                config[
                    "alpha_dqRuleTemplateAdvancedSettings.alpha_dqRuleRowScopeFilteringEnabled"
                ] = row_scope_filtering_enabled

            return json.dumps(config)

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
            threshold_compare_operator: alpha_DQRuleThresholdCompareOperator,
            threshold_value: int,
            alert_priority: alpha_DQRuleAlertPriority,
            column: Optional[Asset] = None,
            threshold_unit: Optional[alpha_DQRuleThresholdUnit] = None,
            dimension: Optional[alpha_DQDimension] = None,
            custom_sql: Optional[str] = None,
            description: Optional[str] = None,
            rule_conditions: Optional[str] = None,
            row_scope_filtering_enabled: Optional[bool] = False,
        ) -> alpha_DQRule.Attributes:
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
                    threshold_unit = alpha_DQRule.Attributes._get_template_config_value(
                        config.alpha_dq_rule_template_config_threshold_object,
                        "alpha_dqRuleTemplateConfigThresholdUnit",
                        "default",
                    )

            config_arguments_raw = (
                alpha_DQRule.Attributes._generate_config_arguments_raw(
                    is_alert_enabled=True,
                    custom_sql=custom_sql,
                    display_name=rule_name,
                    dimension=dimension,
                    compare_operator=threshold_compare_operator,
                    threshold_value=threshold_value,
                    threshold_unit=threshold_unit,
                    column=column,
                    dq_priority=alert_priority,
                    description=description,
                    rule_conditions=rule_conditions,
                    row_scope_filtering_enabled=row_scope_filtering_enabled,
                )
            )

            attr_dq = alpha_DQRule.Attributes(
                name="",
                alpha_dq_rule_config_arguments=alpha_DQRuleConfigArguments(
                    alpha_dq_rule_threshold_object=alpha_DQRuleThresholdObject(
                        alpha_dq_rule_threshold_compare_operator=threshold_compare_operator,
                        alpha_dq_rule_threshold_value=threshold_value,
                        alpha_dq_rule_threshold_unit=threshold_unit,
                    ),
                    alpha_dq_rule_config_arguments_raw=config_arguments_raw,
                    alpha_dq_rule_config_rule_conditions=rule_conditions,
                ),
                alpha_dq_rule_base_dataset_qualified_name=asset.qualified_name,
                alpha_dq_rule_alert_priority=alert_priority,
                alpha_dq_rule_row_scope_filtering_enabled=row_scope_filtering_enabled,
                alpha_dq_rule_source_sync_status=alpha_DQSourceSyncStatus.IN_PROGRESS,
                alpha_dq_rule_status=alpha_DQRuleStatus.ACTIVE,
                alpha_dq_rule_base_dataset=asset,
                qualified_name=f"{asset.qualified_name}/rule/{str(cls._generate_uuid())}",
                alpha_dq_rule_dimension=dimension,
                alpha_dq_rule_template_name=template_rule_name,
                alpha_dq_rule_template=alpha_DQRuleTemplate.ref_by_qualified_name(
                    qualified_name=template_qualified_name  # type: ignore
                ),
            )

            if column is not None:
                attr_dq.alpha_dq_rule_base_column_qualified_name = column.qualified_name
                attr_dq.alpha_dq_rule_base_column = column  # type: ignore

            if custom_sql is not None:
                attr_dq.alpha_dq_rule_custom_s_q_l = custom_sql
                attr_dq.display_name = rule_name
                if description is not None:
                    attr_dq.user_description = description

            return attr_dq

    attributes: alpha_DQRule.Attributes = Field(
        default_factory=lambda: alpha_DQRule.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .alpha__d_q_rule_template import alpha_DQRuleTemplate  # noqa: E402, F401
from .asset import Asset  # noqa: E402, F401
# from .column import co
