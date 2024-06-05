# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Set, Union

from pydantic.v1 import BaseModel, Extra, Field, root_validator

from pyatlan.model.enums import (
    BadgeComparisonOperator,
    BadgeConditionColor,
    SourceCostUnitType,
)
from pyatlan.model.utils import to_camel_case
from pyatlan.utils import validate_required_fields


class AtlanObject(BaseModel):
    class Config:
        allow_population_by_field_name = True
        alias_generator = to_camel_case
        extra = Extra.ignore
        json_encoders = {datetime: lambda v: int(v.timestamp() * 1000)}
        validate_assignment = True

    @root_validator(pre=True)
    def flatten_structs_attributes(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Flatten the 'attributes' of the struct models.

        :param values: dictionary containing the attributes.
        :returns: modified dictionary with attributes flattened.
        """
        attributes = values.pop("attributes", {})
        values = {**values, **attributes}
        return values


class MCRuleSchedule(AtlanObject):
    """Description"""

    mc_rule_schedule_type: Optional[str] = Field(default=None, description="")
    mc_rule_schedule_interval_in_minutes: Optional[int] = Field(
        default=None, description=""
    )
    mc_rule_schedule_start_time: Optional[datetime] = Field(
        default=None, description=""
    )
    mc_rule_schedule_crontab: Optional[str] = Field(default=None, description="")


class AwsCloudWatchMetric(AtlanObject):
    """Description"""

    aws_cloud_watch_metric_name: str = Field(description="")
    aws_cloud_watch_metric_scope: str = Field(description="")


class KafkaTopicConsumption(AtlanObject):
    """Description"""

    topic_name: Optional[str] = Field(default=None, description="")
    topic_partition: Optional[str] = Field(default=None, description="")
    topic_lag: Optional[int] = Field(default=None, description="")
    topic_current_offset: Optional[int] = Field(default=None, description="")


class Action(AtlanObject):
    """Description"""

    task_action_fulfillment_url: Optional[str] = Field(default=None, description="")
    task_action_fulfillment_method: Optional[str] = Field(default=None, description="")
    task_action_fulfillment_payload: Optional[str] = Field(default=None, description="")
    task_action_display_text: Optional[str] = Field(default=None, description="")


class Histogram(AtlanObject):
    """Description"""

    boundaries: Set[float] = Field(description="")
    frequencies: Set[float] = Field(description="")


class ColumnValueFrequencyMap(AtlanObject):
    """Description"""

    column_value: Optional[str] = Field(default=None, description="")
    column_value_frequency: Optional[int] = Field(default=None, description="")


class SourceTagAttachmentValue(AtlanObject):
    """Description"""

    tag_attachment_key: Optional[str] = Field(default=None, description="")
    tag_attachment_value: Optional[str] = Field(default=None, description="")


class BadgeCondition(AtlanObject):
    """Description"""

    @classmethod
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
            badge_condition_colorhex=(
                badge_condition_colorhex.value
                if isinstance(badge_condition_colorhex, BadgeConditionColor)
                else badge_condition_colorhex
            ),
        )

    badge_condition_operator: Optional[str] = Field(default=None, description="")
    badge_condition_value: Optional[str] = Field(default=None, description="")
    badge_condition_colorhex: Optional[str] = Field(default=None, description="")


class SourceTagAttachment(AtlanObject):
    """Description"""

    source_tag_name: Optional[str] = Field(default=None, description="")
    source_tag_qualified_name: Optional[str] = Field(default=None, description="")
    source_tag_guid: Optional[str] = Field(default=None, description="")
    source_tag_connector_name: Optional[str] = Field(default=None, description="")
    source_tag_value: Optional[List[SourceTagAttachmentValue]] = Field(
        default=None, description=""
    )
    is_source_tag_synced: Optional[bool] = Field(default=None, description="")
    source_tag_sync_timestamp: Optional[datetime] = Field(default=None, description="")
    source_tag_sync_error: Optional[str] = Field(default=None, description="")


class AzureTag(AtlanObject):
    """Description"""

    azure_tag_key: str = Field(description="")
    azure_tag_value: str = Field(description="")


class StarredDetails(AtlanObject):
    """Description"""

    asset_starred_by: Optional[str] = Field(default=None, description="")
    asset_starred_at: Optional[datetime] = Field(default=None, description="")


class AuthPolicyCondition(AtlanObject):
    """Description"""

    policy_condition_type: str = Field(description="")
    policy_condition_values: Set[str] = Field(description="")


class AwsTag(AtlanObject):
    """Description"""

    aws_tag_key: str = Field(description="")
    aws_tag_value: str = Field(description="")


class DbtMetricFilter(AtlanObject):
    """Description"""

    dbt_metric_filter_column_qualified_name: Optional[str] = Field(
        default=None, description=""
    )
    dbt_metric_filter_field: Optional[str] = Field(default=None, description="")
    dbt_metric_filter_operator: Optional[str] = Field(default=None, description="")
    dbt_metric_filter_value: Optional[str] = Field(default=None, description="")


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

    mc_rule_comparison_type: Optional[str] = Field(default=None, description="")
    mc_rule_comparison_field: Optional[str] = Field(default=None, description="")
    mc_rule_comparison_metric: Optional[str] = Field(default=None, description="")
    mc_rule_comparison_operator: Optional[str] = Field(default=None, description="")
    mc_rule_comparison_threshold: Optional[float] = Field(default=None, description="")
    mc_rule_comparison_is_threshold_relative: Optional[bool] = Field(
        default=None, description=""
    )


class GoogleLabel(AtlanObject):
    """Description"""

    google_label_key: str = Field(description="")
    google_label_value: str = Field(description="")


class PopularityInsights(AtlanObject):
    """Description"""

    record_user: Optional[str] = Field(default=None, description="")
    record_query: Optional[str] = Field(default=None, description="")
    record_query_duration: Optional[int] = Field(default=None, description="")
    record_query_count: Optional[int] = Field(default=None, description="")
    record_total_user_count: Optional[int] = Field(default=None, description="")
    record_compute_cost: Optional[float] = Field(default=None, description="")
    record_max_compute_cost: Optional[float] = Field(default=None, description="")
    record_compute_cost_unit: Optional[SourceCostUnitType] = Field(
        default=None, description=""
    )
    record_last_timestamp: Optional[datetime] = Field(default=None, description="")
    record_warehouse: Optional[str] = Field(default=None, description="")


class SourceTagAttribute(AtlanObject):
    """Description"""

    tag_attribute_key: Optional[str] = Field(default=None, description="")
    tag_attribute_value: Optional[str] = Field(default=None, description="")
    tag_attribute_properties: Optional[Dict[str, str]] = Field(
        default=None, description=""
    )


MCRuleSchedule.update_forward_refs()

AwsCloudWatchMetric.update_forward_refs()

KafkaTopicConsumption.update_forward_refs()

Action.update_forward_refs()

Histogram.update_forward_refs()

ColumnValueFrequencyMap.update_forward_refs()

SourceTagAttachmentValue.update_forward_refs()

BadgeCondition.update_forward_refs()

SourceTagAttachment.update_forward_refs()

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
