# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""Struct classes for pyatlan_v9, migrated from Pydantic to msgspec."""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Union

import msgspec

from pyatlan.model.enums import (
    AppWorkflowRunStatus,
    AssetSmusMetadataFormStatus,
    AtlanConnectorType,
    DataQualityRuleThresholdUnit,
    FormFieldDimension,
    FormFieldType,
    SourceCostUnitType,
)
from pyatlan.utils import select_optional_set_fields
from pyatlan_v9.model.assets.badge_condition import BadgeCondition

if TYPE_CHECKING:
    from pyatlan.cache.aio.source_tag_cache import AsyncSourceTagName
    from pyatlan.cache.source_tag_cache import SourceTagName
    from pyatlan.client.aio import AsyncAtlanClient
    from pyatlan.client.atlan import AtlanClient


class AssetExternalDQMetadata(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    asset_external_d_q_system_name: Union[str, None] = None
    asset_external_d_q_source_logo: Union[str, None] = None
    asset_external_d_q_source_url: Union[str, None] = None
    asset_external_d_q_last_sync_run_at: Union[datetime, None] = None
    asset_external_d_q_test_entity_name: Union[str, None] = None
    asset_external_d_q_test_total_count: Union[int, None] = None
    asset_external_d_q_test_last_run_success_count: Union[int, None] = None
    asset_external_d_q_test_last_run_failure_count: Union[int, None] = None
    asset_external_d_q_overall_score_value: Union[str, None] = None
    asset_external_d_q_overall_score_type: Union[str, None] = None
    asset_external_d_q_score_dimensions: Union[
        list[AssetExternalDQScoreBreakdownByDimension], None
    ] = None
    asset_external_d_q_tests: Union[list[AssetExternalDQTestDetails], None] = None


class MCRuleSchedule(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    mc_rule_schedule_type: Union[str, None] = None
    mc_rule_schedule_interval_in_minutes: Union[int, None] = None
    mc_rule_schedule_start_time: Union[datetime, None] = None
    mc_rule_schedule_crontab: Union[str, None] = None


class DbtJobRun(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    dbt_job_id: Union[str, None] = None
    dbt_job_name: Union[str, None] = None
    dbt_environment_id: Union[str, None] = None
    dbt_environment_name: Union[str, None] = None
    dbt_job_run_id: Union[str, None] = None
    dbt_job_run_completed_at: Union[datetime, None] = None
    dbt_job_run_status: Union[str, None] = None
    dbt_test_run_status: Union[str, None] = None
    dbt_model_run_status: Union[str, None] = None
    dbt_compiled_s_q_l: Union[str, None] = None
    dbt_compiled_code: Union[str, None] = None


class AwsCloudWatchMetric(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    aws_cloud_watch_metric_name: str
    aws_cloud_watch_metric_scope: str


class Action(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    task_action_fulfillment_url: Union[str, None] = None
    task_action_fulfillment_method: Union[str, None] = None
    task_action_fulfillment_payload: Union[str, None] = None
    task_action_display_text: Union[str, None] = None


class Histogram(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    boundaries: set[float]
    frequencies: set[float]


class AssetExternalDQTestRunHistory(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    asset_external_d_q_test_run_started_at: Union[datetime, None] = None
    asset_external_d_q_test_run_ended_at: Union[datetime, None] = None
    asset_external_d_q_test_run_status: Union[str, None] = None
    asset_external_d_q_test_metric_info: Union[AssetExternalDQTestMetric, None] = None


class ColumnValueFrequencyMap(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    column_value: Union[str, None] = None
    column_value_frequency: Union[int, None] = None


class AssetExternalDQTestMetric(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    asset_external_d_q_test_metric_observed_value: Union[str, None] = None
    asset_external_d_q_test_metric_upper_bound: Union[str, None] = None
    asset_external_d_q_test_metric_lower_bound: Union[str, None] = None


class SourceTagAttachmentValue(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    tag_attachment_key: Union[str, None] = None
    tag_attachment_value: Union[str, None] = None


class StarredDetails(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    asset_starred_by: Union[str, None] = None
    asset_starred_at: Union[datetime, None] = None


class AwsTag(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    aws_tag_key: str
    aws_tag_value: str


class GoogleTag(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    google_tag_key: str
    google_tag_value: str


class AssetExternalDQTestDetails(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    asset_external_d_q_test_name: Union[str, None] = None
    asset_external_d_q_test_id: Union[str, None] = None
    asset_external_d_q_test_description: Union[str, None] = None
    asset_external_d_q_test_schedule_type: Union[str, None] = None
    asset_external_d_q_test_last_run_status: Union[str, None] = None
    asset_external_d_q_test_runs: Union[list[AssetExternalDQTestRunHistory], None] = (
        None
    )


class BusinessPolicyRule(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    bpr_id: Union[str, None] = None
    bpr_name: Union[str, None] = None
    bpr_sequence: Union[str, None] = None
    bpr_operand: Union[str, None] = None
    bpr_operator: Union[str, None] = None
    bpr_value: Union[set[str], None] = None
    bpr_query: Union[str, None] = None


class ResponseValue(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    response_field_id: Union[str, None] = None
    response_value_string: Union[str, None] = None
    response_value_int: Union[int, None] = None
    response_value_boolean: Union[bool, None] = None
    response_value_json: Union[str, None] = None
    response_value_long: Union[int, None] = None
    response_value_date: Union[datetime, None] = None
    response_value_arr_string: Union[set[str], None] = None
    response_value_arr_int: Union[set[int], None] = None
    response_value_arr_boolean: Union[set[bool], None] = None
    response_value_arr_json: Union[set[str], None] = None
    response_value_arr_long: Union[set[int], None] = None
    response_value_arr_date: Union[set[datetime], None] = None
    response_value_options: Union[dict[str, str], None] = None


class FormField(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    form_field_id: Union[str, None] = None
    form_field_name: Union[str, None] = None
    form_field_type: Union[FormFieldType, None] = None
    form_field_dimension: Union[FormFieldDimension, None] = None
    form_field_options: Union[dict[str, str], None] = None


class DbtInputContext(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    dbt_input_context_name: Union[str, None] = None
    dbt_input_context_qualified_name: Union[str, None] = None
    dbt_input_context_type: Union[str, None] = None
    dbt_input_context_alias: Union[str, None] = None
    dbt_input_context_filter: Union[str, None] = None
    dbt_input_context_offset_window: Union[str, None] = None
    dbt_input_context_offset_to_grain: Union[str, None] = None


class AssetSmusMetadataFormDetails(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    asset_metadata_form_name: Union[str, None] = None
    asset_metadata_form_description: Union[str, None] = None
    asset_metadata_form_domain_id: Union[str, None] = None
    asset_metadata_form_project_id: Union[str, None] = None
    asset_metadata_form_status: Union[AssetSmusMetadataFormStatus, None] = None
    asset_metadata_form_revision: Union[str, None] = None
    asset_metadata_form_fields: Union[list[dict[str, str]], None] = None


class DatabricksAIModelVersionMetric(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    databricks_a_i_model_version_metric_key: Union[str, None] = None
    databricks_a_i_model_version_metric_value: Union[float, None] = None
    databricks_a_i_model_version_metric_timestamp: Union[datetime, None] = None
    databricks_a_i_model_version_metric_step: Union[int, None] = None


class KafkaTopicConsumption(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    topic_name: Union[str, None] = None
    topic_partition: Union[str, None] = None
    topic_lag: Union[int, None] = None
    topic_current_offset: Union[int, None] = None


class SQLProcedureReturn(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    sql_return_type: Union[str, None] = None
    sql_return_character_maximum_length: Union[int, None] = None
    sql_return_character_octet_length: Union[int, None] = None
    sql_return_numeric_precision: Union[int, None] = None
    sql_return_numeric_precision_radix: Union[int, None] = None


class SourceTagAttachment(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    source_tag_name: Union[str, None] = None
    source_tag_qualified_name: Union[str, None] = None
    source_tag_guid: Union[str, None] = None
    source_tag_connector_name: Union[str, None] = None
    source_tag_value: Union[list[SourceTagAttachmentValue], None] = None
    is_source_tag_synced: Union[bool, None] = None
    source_tag_sync_timestamp: Union[datetime, None] = None
    source_tag_sync_error: Union[str, None] = None
    source_tag_type: Union[str, None] = None

    @classmethod
    def by_name(
        cls,
        client: AtlanClient,
        name: SourceTagName,
        source_tag_values: list[SourceTagAttachmentValue],
        source_tag_sync_timestamp: Union[datetime, None] = None,
        is_source_tag_synced: Union[bool, None] = None,
        source_tag_sync_error: Union[str, None] = None,
    ):
        """
        Create a source-synced tag attachment with
        a particular value when the attachment is synced to the source.

        :param client: connectivity to an Atlan tenant
        :param name: unique name of the source tag in Atlan
        :param source_tag_values: value of the tag attachment from the source
        :param is_source_tag_synced: whether the tag attachment has been synced at the source (True) or not (False)
        :param source_tag_sync_timestamp: time (epoch) when the tag attachment was synced at the source, in milliseconds
        :param source_tag_sync_error: error message if the tag attachment sync at the source failed
        :returns: a SourceTagAttachment with the provided information
        :raises AtlanError: on any error communicating via the underlying APIs
        :raises NotFoundError: if the source-synced tag cannot be resolved
        """
        tag = client.source_tag_cache.get_by_name(name)
        tag_connector_name = AtlanConnectorType._get_connector_type_from_qualified_name(
            tag.qualified_name or ""
        )
        return cls.of(
            source_tag_name=tag.name,
            source_tag_qualified_name=tag.qualified_name,
            source_tag_guid=tag.guid,
            source_tag_connector_name=tag_connector_name,
            source_tag_values=source_tag_values,
            **select_optional_set_fields(
                dict(
                    is_source_tag_synced=is_source_tag_synced,
                    source_tag_sync_timestamp=source_tag_sync_timestamp,
                    source_tag_sync_error=source_tag_sync_error,
                )
            ),
        )

    @classmethod
    async def by_name_async(
        cls,
        client: AsyncAtlanClient,
        name: AsyncSourceTagName,
        source_tag_values: list[SourceTagAttachmentValue],
        source_tag_sync_timestamp: Union[datetime, None] = None,
        is_source_tag_synced: Union[bool, None] = None,
        source_tag_sync_error: Union[str, None] = None,
    ):
        """
        Async version of by_name that creates a source-synced tag attachment with
        a particular value when the attachment is synced to the source.

        :param client: async connectivity to an Atlan tenant
        :param name: unique name of the source tag in Atlan
        :param source_tag_values: value of the tag attachment from the source
        :param is_source_tag_synced: whether the tag attachment has been synced at the source (True) or not (False)
        :param source_tag_sync_timestamp: time (epoch) when the tag attachment was synced at the source, in milliseconds
        :param source_tag_sync_error: error message if the tag attachment sync at the source failed
        :returns: a SourceTagAttachment with the provided information
        :raises AtlanError: on any error communicating via the underlying APIs
        :raises NotFoundError: if the source-synced tag cannot be resolved
        """
        tag = await client.source_tag_cache.get_by_name(name)
        tag_connector_name = AtlanConnectorType._get_connector_type_from_qualified_name(
            tag.qualified_name or ""
        )
        return cls.of(
            source_tag_name=tag.name,
            source_tag_qualified_name=tag.qualified_name,
            source_tag_guid=tag.guid,
            source_tag_connector_name=tag_connector_name,
            source_tag_values=source_tag_values,
            **select_optional_set_fields(
                dict(
                    is_source_tag_synced=is_source_tag_synced,
                    source_tag_sync_timestamp=source_tag_sync_timestamp,
                    source_tag_sync_error=source_tag_sync_error,
                )
            ),
        )

    @classmethod
    def by_qualified_name(
        cls,
        client: AtlanClient,
        source_tag_qualified_name: str,
        source_tag_values: list[SourceTagAttachmentValue],
        source_tag_sync_timestamp: Union[datetime, None] = None,
        is_source_tag_synced: Union[bool, None] = None,
        source_tag_sync_error: Union[str, None] = None,
    ):
        """
        Create a source-synced tag attachment with
        a particular value when the attachment is synced to the source.

        :param client: connectivity to an Atlan tenant
        :param source_tag_qualified_name: unique name of the source tag in Atlan
        :param source_tag_values: value of the tag attachment from the source
        :param is_source_tag_synced: whether the tag attachment has been synced at the source (True) or not (False)
        :param source_tag_sync_timestamp: time (epoch) when the tag attachment was synced at the source, in milliseconds
        :param source_tag_sync_error: error message if the tag attachment sync at the source failed
        :returns: a SourceTagAttachment with the provided information
        :raises AtlanError: on any error communicating via the underlying APIs
        :raises NotFoundError: if the source-synced tag cannot be resolved
        """
        tag = client.source_tag_cache.get_by_qualified_name(source_tag_qualified_name)
        tag_connector_name = AtlanConnectorType._get_connector_type_from_qualified_name(
            source_tag_qualified_name or ""
        )
        return cls.of(
            source_tag_name=tag.name,
            source_tag_qualified_name=source_tag_qualified_name,
            source_tag_guid=tag.guid,
            source_tag_connector_name=tag_connector_name,
            source_tag_values=source_tag_values,
            **select_optional_set_fields(
                dict(
                    is_source_tag_synced=is_source_tag_synced,
                    source_tag_sync_timestamp=source_tag_sync_timestamp,
                    source_tag_sync_error=source_tag_sync_error,
                )
            ),
        )

    @classmethod
    def of(
        cls,
        source_tag_name: Union[str, None] = None,
        source_tag_qualified_name: Union[str, None] = None,
        source_tag_guid: Union[str, None] = None,
        source_tag_connector_name: Union[str, None] = None,
        source_tag_values: Union[list[SourceTagAttachmentValue], None] = None,
        is_source_tag_synced: Union[bool, None] = None,
        source_tag_sync_timestamp: Union[datetime, None] = None,
        source_tag_sync_error: Union[str, None] = None,
    ):
        """
        Quickly create a new SourceTagAttachment.

        :param source_tag_name: simple name of the source tag
        :param source_tag_qualified_name: unique name of the source tag in Atlan
        :param source_tag_guid: unique identifier (GUID) of the source tag in Atlan
        :param source_tag_connector_name: connector that is the source of the tag
        :param source_tag_values: value of the tag attachment from the source
        :param is_source_tag_synced: whether the tag attachment has been synced at the source (True) or not (False)
        :param source_tag_sync_timestamp: time (epoch) when the tag attachment was synced at the source, in milliseconds
        :param source_tag_sync_error: error message if the tag attachment sync at the source failed
        :returns: a SourceTagAttachment with the provided information
        """
        return SourceTagAttachment(
            **select_optional_set_fields(
                dict(
                    source_tag_name=source_tag_name,
                    source_tag_qualified_name=source_tag_qualified_name,
                    source_tag_guid=source_tag_guid,
                    source_tag_connector_name=source_tag_connector_name,
                    source_tag_value=source_tag_values,
                    is_source_tag_synced=is_source_tag_synced,
                    source_tag_sync_timestamp=source_tag_sync_timestamp,
                    source_tag_sync_error=source_tag_sync_error,
                )
            ),
        )


class AzureTag(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    azure_tag_key: str
    azure_tag_value: str


class AssetExternalDQScoreBreakdownByDimension(
    msgspec.Struct, kw_only=True, rename="camel"
):
    """Description"""

    asset_external_d_q_score_dimension_name: Union[str, None] = None
    asset_external_d_q_score_dimension_description: Union[str, None] = None
    asset_external_d_q_score_dimension_score_value: Union[str, None] = None
    asset_external_d_q_score_dimension_score_type: Union[str, None] = None


class AuthPolicyCondition(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    policy_condition_type: str
    policy_condition_values: set[str]


class DataQualityRuleConfigArguments(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    dq_rule_threshold_object: Union[DataQualityRuleThresholdObject, None] = None
    dq_rule_config_arguments_raw: Union[str, None] = None
    dq_rule_config_rule_conditions: Union[str, None] = None


class SQLProcedureArgument(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    sql_argument_name: Union[str, None] = None
    sql_argument_type: Union[str, None] = None


class DbtMetricFilter(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    dbt_metric_filter_column_qualified_name: Union[str, None] = None
    dbt_metric_filter_field: Union[str, None] = None
    dbt_metric_filter_operator: Union[str, None] = None
    dbt_metric_filter_value: Union[str, None] = None


class AssetHistogram(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    asset_histogram_boundaries: Union[set[float], None] = None
    asset_histogram_frequencies: Union[set[float], None] = None


class DataQualityRuleTemplateConfig(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    dq_rule_template_config_base_dataset_qualified_name: Union[str, None] = None
    dq_rule_template_config_base_column_qualified_name: Union[str, None] = None
    dq_rule_template_config_reference_dataset_qualified_names: Union[str, None] = None
    dq_rule_template_config_reference_column_qualified_names: Union[str, None] = None
    dq_rule_template_config_threshold_object: Union[str, None] = None
    dq_rule_template_config_display_name: Union[str, None] = None
    dq_rule_template_config_custom_s_q_l: Union[str, None] = None
    dq_rule_template_config_dimension: Union[str, None] = None
    dq_rule_template_config_user_description: Union[str, None] = None
    dq_rule_template_config_advanced_settings: Union[str, None] = None
    dq_rule_template_config_rule_conditions: Union[str, None] = None
    dq_rule_template_config_preflight_check: Union[str, None] = None


class AppWorkflowRunStep(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    app_workflow_run_label: Union[str, None] = None
    app_workflow_run_status: Union[AppWorkflowRunStatus, None] = None
    app_workflow_run_started_at: Union[datetime, None] = None
    app_workflow_run_completed_at: Union[datetime, None] = None
    app_workflow_run_outputs: Union[dict[str, str], None] = None


class AuthPolicyValiditySchedule(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    policy_validity_schedule_start_time: str
    policy_validity_schedule_end_time: str
    policy_validity_schedule_timezone: str


class MCRuleComparison(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    mc_rule_comparison_type: Union[str, None] = None
    mc_rule_comparison_field: Union[str, None] = None
    mc_rule_comparison_metric: Union[str, None] = None
    mc_rule_comparison_operator: Union[str, None] = None
    mc_rule_comparison_threshold: Union[float, None] = None
    mc_rule_comparison_is_threshold_relative: Union[bool, None] = None


class DataQualityRuleThresholdObject(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    dq_rule_threshold_compare_operator: Union[str, None] = None
    dq_rule_threshold_value: Union[float, None] = None
    dq_rule_threshold_unit: Union[DataQualityRuleThresholdUnit, None] = None


class GoogleLabel(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    google_label_key: str
    google_label_value: str


class PopularityInsights(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    record_user: Union[str, None] = None
    record_query: Union[str, None] = None
    record_query_duration: Union[int, None] = None
    record_query_count: Union[int, None] = None
    record_total_user_count: Union[int, None] = None
    record_compute_cost: Union[float, None] = None
    record_max_compute_cost: Union[float, None] = None
    record_compute_cost_unit: Union[SourceCostUnitType, None] = None
    record_last_timestamp: Union[datetime, None] = None
    record_warehouse: Union[str, None] = None


class SourceTagAttribute(msgspec.Struct, kw_only=True, rename="camel"):
    """Description"""

    tag_attribute_key: Union[str, None] = None
    tag_attribute_value: Union[str, None] = None
    tag_attribute_properties: Union[dict[str, str], None] = None


__all__ = [
    "AssetExternalDQMetadata",
    "MCRuleSchedule",
    "DbtJobRun",
    "AwsCloudWatchMetric",
    "Action",
    "Histogram",
    "AssetExternalDQTestRunHistory",
    "ColumnValueFrequencyMap",
    "AssetExternalDQTestMetric",
    "BadgeCondition",
    "SourceTagAttachmentValue",
    "StarredDetails",
    "AwsTag",
    "GoogleTag",
    "AssetExternalDQTestDetails",
    "BusinessPolicyRule",
    "ResponseValue",
    "FormField",
    "DbtInputContext",
    "AssetSmusMetadataFormDetails",
    "DatabricksAIModelVersionMetric",
    "KafkaTopicConsumption",
    "SQLProcedureReturn",
    "SourceTagAttachment",
    "AzureTag",
    "AssetExternalDQScoreBreakdownByDimension",
    "AuthPolicyCondition",
    "DataQualityRuleConfigArguments",
    "SQLProcedureArgument",
    "DbtMetricFilter",
    "AssetHistogram",
    "DataQualityRuleTemplateConfig",
    "AppWorkflowRunStep",
    "AuthPolicyValiditySchedule",
    "MCRuleComparison",
    "DataQualityRuleThresholdObject",
    "GoogleLabel",
    "PopularityInsights",
    "SourceTagAttribute",
]
