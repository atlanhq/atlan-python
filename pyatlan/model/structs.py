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

    mc_rule_schedule_type: Optional[str] = Field(None, description="")
    mc_rule_schedule_interval_in_minutes: Optional[int] = Field(None, description="")
    mc_rule_schedule_start_time: Optional[datetime] = Field(None, description="")
    mc_rule_schedule_crontab: Optional[str] = Field(None, description="")


class AwsCloudWatchMetric(AtlanObject):
    """Description"""

    aws_cloud_watch_metric_name: str = Field(description="")
    aws_cloud_watch_metric_scope: str = Field(description="")


class Histogram(AtlanObject):
    """Description"""

    boundaries: set[float] = Field(description="")
    frequencies: set[float] = Field(description="")


class KafkaTopicConsumption(AtlanObject):
    """Description"""

    topic_name: Optional[str] = Field(None, description="")
    topic_partition: Optional[str] = Field(None, description="")
    topic_lag: Optional[int] = Field(None, description="")
    topic_current_offset: Optional[int] = Field(None, description="")


class ColumnValueFrequencyMap(AtlanObject):
    """Description"""

    column_value: Optional[str] = Field(None, description="")
    column_value_frequency: Optional[int] = Field(None, description="")


class SourceTagAttachment(AtlanObject):
    """Description"""

    source_tag_name: Optional[str] = Field(None, description="")
    source_tag_qualified_name: Optional[str] = Field(None, description="")
    source_tag_guid: Optional[str] = Field(None, description="")
    source_tag_connector_name: Optional[str] = Field(None, description="")
    source_tag_value: Optional[list[SourceTagAttachmentValue]] = Field(
        None, description=""
    )
    is_source_tag_synced: Optional[bool] = Field(None, description="")
    source_tag_sync_timestamp: Optional[datetime] = Field(None, description="")
    source_tag_sync_error: Optional[str] = Field(None, description="")


class SourceTagAttachmentValue(AtlanObject):
    """Description"""

    tag_attachment_key: Optional[str] = Field(None, description="")
    tag_attachment_value: Optional[str] = Field(None, description="")


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

    badge_condition_operator: Optional[str] = Field(None, description="")
    badge_condition_value: Optional[str] = Field(None, description="")
    badge_condition_colorhex: Optional[str] = Field(None, description="")


class AzureTag(AtlanObject):
    """Description"""

    azure_tag_key: str = Field(description="")
    azure_tag_value: str = Field(description="")


class StarredDetails(AtlanObject):
    """Description"""

    asset_starred_by: Optional[str] = Field(None, description="")
    asset_starred_at: Optional[datetime] = Field(None, description="")


class AuthPolicyCondition(AtlanObject):
    """Description"""

    policy_condition_type: str = Field(description="")
    policy_condition_values: set[str] = Field(description="")


class AwsTag(AtlanObject):
    """Description"""

    aws_tag_key: str = Field(description="")
    aws_tag_value: str = Field(description="")


class DbtMetricFilter(AtlanObject):
    """Description"""

    dbt_metric_filter_column_qualified_name: Optional[str] = Field(None, description="")
    dbt_metric_filter_field: Optional[str] = Field(None, description="")
    dbt_metric_filter_operator: Optional[str] = Field(None, description="")
    dbt_metric_filter_value: Optional[str] = Field(None, description="")


class GoogleTag(AtlanObject):
    """Description"""

    google_tag_key: str = Field(description="")
    google_tag_value: str = Field(description="")


class AuthPolicyValiditySchedule(AtlanObject):
    """Description"""

    policy_validity_schedule_start_time: str = Field(description="")
    policy_validity_schedule_end_time: str = Field(description="")
    policy_validity_schedule_timezone: str = Field(description="")


class MCRuleComparison(AtlanObject):
    """Description"""

    mc_rule_comparison_type: Optional[str] = Field(None, description="")
    mc_rule_comparison_field: Optional[str] = Field(None, description="")
    mc_rule_comparison_metric: Optional[str] = Field(None, description="")
    mc_rule_comparison_operator: Optional[str] = Field(None, description="")
    mc_rule_comparison_threshold: Optional[float] = Field(None, description="")
    mc_rule_comparison_is_threshold_relative: Optional[bool] = Field(
        None, description=""
    )


class GoogleLabel(AtlanObject):
    """Description"""

    google_label_key: str = Field(description="")
    google_label_value: str = Field(description="")


class PopularityInsights(AtlanObject):
    """Description"""

    record_user: Optional[str] = Field(None, description="")
    record_query: Optional[str] = Field(None, description="")
    record_query_duration: Optional[int] = Field(None, description="")
    record_query_count: Optional[int] = Field(None, description="")
    record_total_user_count: Optional[int] = Field(None, description="")
    record_compute_cost: Optional[float] = Field(None, description="")
    record_max_compute_cost: Optional[float] = Field(None, description="")
    record_compute_cost_unit: Optional[SourceCostUnitType] = Field(None, description="")
    record_last_timestamp: Optional[datetime] = Field(None, description="")
    record_warehouse: Optional[str] = Field(None, description="")


class SourceTagAttribute(AtlanObject):
    """Description"""

    tag_attribute_key: Optional[str] = Field(None, description="")
    tag_attribute_value: Optional[str] = Field(None, description="")
    tag_attribute_properties: Optional[dict[str, str]] = Field(None, description="")


MCRuleSchedule.update_forward_refs()

AwsCloudWatchMetric.update_forward_refs()

Histogram.update_forward_refs()

KafkaTopicConsumption.update_forward_refs()

ColumnValueFrequencyMap.update_forward_refs()

SourceTagAttachment.update_forward_refs()

SourceTagAttachmentValue.update_forward_refs()

BadgeCondition.update_forward_refs()

AzureTag.update_forward_refs()

StarredDetails.update_forward_refs()

AuthPolicyCondition.update_forward_refs()

AwsTag.update_forward_refs()

DbtMetricFilter.update_forward_refs()

GoogleTag.update_forward_refs()

AuthPolicyValiditySchedule.update_forward_refs()

MCRuleComparison.update_forward_refs()

GoogleLabel.update_forward_refs()

PopularityInsights.update_forward_refs()

SourceTagAttribute.update_forward_refs()
