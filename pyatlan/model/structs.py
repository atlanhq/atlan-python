# Copyright 2022 Atlan Pte. Ltd.
from __future__ import annotations

from datetime import datetime
from typing import Optional, Union

from pydantic import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import (
    BadgeComparisonOperator,
    BadgeConditionColor,
    SourceCostUnitType,
)
from pyatlan.utils import validate_required_fields


class MCRuleSchedule(AtlanObject):
    """Description"""

    mc_rule_schedule_type: Optional[str] = Field(
        None, description="", alias="mcRuleScheduleType"
    )
    mc_rule_schedule_interval_in_minutes: Optional[int] = Field(
        None, description="", alias="mcRuleScheduleIntervalInMinutes"
    )
    mc_rule_schedule_start_time: Optional[datetime] = Field(
        None, description="", alias="mcRuleScheduleStartTime"
    )
    mc_rule_schedule_crontab: Optional[str] = Field(
        None, description="", alias="mcRuleScheduleCrontab"
    )


class AwsCloudWatchMetric(AtlanObject):
    """Description"""

    aws_cloud_watch_metric_name: str = Field(
        description="", alias="awsCloudWatchMetricName"
    )
    aws_cloud_watch_metric_scope: str = Field(
        description="", alias="awsCloudWatchMetricScope"
    )


class Histogram(AtlanObject):
    """Description"""

    boundaries: set[float] = Field(description="", alias="boundaries")
    frequencies: set[float] = Field(description="", alias="frequencies")


class KafkaTopicConsumption(AtlanObject):
    """Description"""

    topic_name: Optional[str] = Field(None, description="", alias="topicName")
    topic_partition: Optional[str] = Field(None, description="", alias="topicPartition")
    topic_lag: Optional[int] = Field(None, description="", alias="topicLag")
    topic_current_offset: Optional[int] = Field(
        None, description="", alias="topicCurrentOffset"
    )


class ColumnValueFrequencyMap(AtlanObject):
    """Description"""

    column_value: Optional[str] = Field(None, description="", alias="columnValue")
    column_value_frequency: Optional[int] = Field(
        None, description="", alias="columnValueFrequency"
    )


class SourceTagAttachment(AtlanObject):
    """Description"""

    source_tag_name: Optional[str] = Field(None, description="", alias="sourceTagName")
    source_tag_qualified_name: Optional[str] = Field(
        None, description="", alias="sourceTagQualifiedName"
    )
    source_tag_guid: Optional[str] = Field(None, description="", alias="sourceTagGuid")
    source_tag_connector_name: Optional[str] = Field(
        None, description="", alias="sourceTagConnectorName"
    )
    source_tag_value: Optional[list[SourceTagAttachmentValue]] = Field(
        None, description="", alias="sourceTagValue"
    )
    is_source_tag_synced: Optional[bool] = Field(
        None, description="", alias="isSourceTagSynced"
    )
    source_tag_sync_timestamp: Optional[datetime] = Field(
        None, description="", alias="sourceTagSyncTimestamp"
    )
    source_tag_sync_error: Optional[str] = Field(
        None, description="", alias="sourceTagSyncError"
    )


class SourceTagAttachmentValue(AtlanObject):
    """Description"""

    tag_attachment_key: Optional[str] = Field(
        None, description="", alias="tagAttachmentKey"
    )
    tag_attachment_value: Optional[str] = Field(
        None, description="", alias="tagAttachmentValue"
    )


class BadgeCondition(AtlanObject):
    """Description"""

    @classmethod
    # @validate_arguments()
    def create(
        cls,
        *,
        badge_condition_operator: BadgeComparisonOperator,
        badge_condition_value: str,
        badge_condition_colorhex: Union[BadgeConditionColor, str],
    ) -> "BadgeCondition":
        validate_required_fields(
            [
                "badge_condition_operator",
                "badge_condition_value",
                "badge_condition_colorhex",
            ],
            [badge_condition_operator, badge_condition_value, badge_condition_colorhex],
        )
        return cls(
            badge_condition_operator=badge_condition_operator.value,
            badge_condition_value=badge_condition_value,
            badge_condition_colorhex=badge_condition_colorhex.value
            if isinstance(badge_condition_colorhex, BadgeConditionColor)
            else badge_condition_colorhex,
        )

    badge_condition_operator: Optional[str] = Field(
        None, description="", alias="badgeConditionOperator"
    )
    badge_condition_value: Optional[str] = Field(
        None, description="", alias="badgeConditionValue"
    )
    badge_condition_colorhex: Optional[str] = Field(
        None, description="", alias="badgeConditionColorhex"
    )


class StarredDetails(AtlanObject):
    """Description"""

    asset_starred_by: Optional[str] = Field(
        None, description="", alias="assetStarredBy"
    )
    asset_starred_at: Optional[datetime] = Field(
        None, description="", alias="assetStarredAt"
    )


class AzureTag(AtlanObject):
    """Description"""

    azure_tag_key: str = Field(description="", alias="azureTagKey")
    azure_tag_value: str = Field(description="", alias="azureTagValue")


class AuthPolicyCondition(AtlanObject):
    """Description"""

    policy_condition_type: str = Field(description="", alias="policyConditionType")
    policy_condition_values: set[str] = Field(
        description="", alias="policyConditionValues"
    )


class AwsTag(AtlanObject):
    """Description"""

    aws_tag_key: str = Field(description="", alias="awsTagKey")
    aws_tag_value: str = Field(description="", alias="awsTagValue")


class DbtMetricFilter(AtlanObject):
    """Description"""

    dbt_metric_filter_column_qualified_name: Optional[str] = Field(
        None, description="", alias="dbtMetricFilterColumnQualifiedName"
    )
    dbt_metric_filter_field: Optional[str] = Field(
        None, description="", alias="dbtMetricFilterField"
    )
    dbt_metric_filter_operator: Optional[str] = Field(
        None, description="", alias="dbtMetricFilterOperator"
    )
    dbt_metric_filter_value: Optional[str] = Field(
        None, description="", alias="dbtMetricFilterValue"
    )


class GoogleTag(AtlanObject):
    """Description"""

    google_tag_key: str = Field(description="", alias="googleTagKey")
    google_tag_value: str = Field(description="", alias="googleTagValue")


class AuthPolicyValiditySchedule(AtlanObject):
    """Description"""

    policy_validity_schedule_start_time: str = Field(
        description="", alias="policyValidityScheduleStartTime"
    )
    policy_validity_schedule_end_time: str = Field(
        description="", alias="policyValidityScheduleEndTime"
    )
    policy_validity_schedule_timezone: str = Field(
        description="", alias="policyValidityScheduleTimezone"
    )


class MCRuleComparison(AtlanObject):
    """Description"""

    mc_rule_comparison_type: Optional[str] = Field(
        None, description="", alias="mcRuleComparisonType"
    )
    mc_rule_comparison_field: Optional[str] = Field(
        None, description="", alias="mcRuleComparisonField"
    )
    mc_rule_comparison_metric: Optional[str] = Field(
        None, description="", alias="mcRuleComparisonMetric"
    )
    mc_rule_comparison_operator: Optional[str] = Field(
        None, description="", alias="mcRuleComparisonOperator"
    )
    mc_rule_comparison_threshold: Optional[float] = Field(
        None, description="", alias="mcRuleComparisonThreshold"
    )
    mc_rule_comparison_is_threshold_relative: Optional[bool] = Field(
        None, description="", alias="mcRuleComparisonIsThresholdRelative"
    )


class GoogleLabel(AtlanObject):
    """Description"""

    google_label_key: str = Field(description="", alias="googleLabelKey")
    google_label_value: str = Field(description="", alias="googleLabelValue")


class PopularityInsights(AtlanObject):
    """Description"""

    record_user: Optional[str] = Field(None, description="", alias="recordUser")
    record_query: Optional[str] = Field(None, description="", alias="recordQuery")
    record_query_duration: Optional[int] = Field(
        None, description="", alias="recordQueryDuration"
    )
    record_query_count: Optional[int] = Field(
        None, description="", alias="recordQueryCount"
    )
    record_total_user_count: Optional[int] = Field(
        None, description="", alias="recordTotalUserCount"
    )
    record_compute_cost: Optional[float] = Field(
        None, description="", alias="recordComputeCost"
    )
    record_max_compute_cost: Optional[float] = Field(
        None, description="", alias="recordMaxComputeCost"
    )
    record_compute_cost_unit: Optional[SourceCostUnitType] = Field(
        None, description="", alias="recordComputeCostUnit"
    )
    record_last_timestamp: Optional[datetime] = Field(
        None, description="", alias="recordLastTimestamp"
    )
    record_warehouse: Optional[str] = Field(
        None, description="", alias="recordWarehouse"
    )


class SourceTagAttribute(AtlanObject):
    """Description"""

    tag_attribute_key: Optional[str] = Field(
        None, description="", alias="tagAttributeKey"
    )
    tag_attribute_value: Optional[str] = Field(
        None, description="", alias="tagAttributeValue"
    )
    tag_attribute_properties: Optional[dict[str, str]] = Field(
        None, description="", alias="tagAttributeProperties"
    )


MCRuleSchedule.update_forward_refs()

AwsCloudWatchMetric.update_forward_refs()

Histogram.update_forward_refs()

KafkaTopicConsumption.update_forward_refs()

ColumnValueFrequencyMap.update_forward_refs()

SourceTagAttachment.update_forward_refs()

SourceTagAttachmentValue.update_forward_refs()

BadgeCondition.update_forward_refs()

StarredDetails.update_forward_refs()

AzureTag.update_forward_refs()

AuthPolicyCondition.update_forward_refs()

AwsTag.update_forward_refs()

DbtMetricFilter.update_forward_refs()

GoogleTag.update_forward_refs()

AuthPolicyValiditySchedule.update_forward_refs()

MCRuleComparison.update_forward_refs()

GoogleLabel.update_forward_refs()

PopularityInsights.update_forward_refs()

SourceTagAttribute.update_forward_refs()
