# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from datetime import datetime
from typing import Optional

from pydantic import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import SourceCostUnitType


class MCRuleSchedule(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
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

    class Attributes(AtlanObject):
        aws_cloud_watch_metric_name: str = Field(
            None, description="", alias="awsCloudWatchMetricName"
        )
        aws_cloud_watch_metric_scope: str = Field(
            None, description="", alias="awsCloudWatchMetricScope"
        )


class Histogram(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        boundaries: set[float] = Field(None, description="", alias="boundaries")
        frequencies: set[float] = Field(None, description="", alias="frequencies")


class KafkaTopicConsumption(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        topic_name: Optional[str] = Field(None, description="", alias="topicName")
        topic_partition: Optional[str] = Field(
            None, description="", alias="topicPartition"
        )
        topic_lag: Optional[int] = Field(None, description="", alias="topicLag")
        topic_current_offset: Optional[int] = Field(
            None, description="", alias="topicCurrentOffset"
        )


class ColumnValueFrequencyMap(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        column_value: Optional[str] = Field(None, description="", alias="columnValue")
        column_value_frequency: Optional[int] = Field(
            None, description="", alias="columnValueFrequency"
        )


class BadgeCondition(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        badge_condition_operator: Optional[str] = Field(
            None, description="", alias="badgeConditionOperator"
        )
        badge_condition_value: Optional[str] = Field(
            None, description="", alias="badgeConditionValue"
        )
        badge_condition_colorhex: Optional[str] = Field(
            None, description="", alias="badgeConditionColorhex"
        )


class SourceTagAttachmentValue(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        tag_attachment_key: Optional[str] = Field(
            None, description="", alias="tagAttachmentKey"
        )
        tag_attachment_value: Optional[str] = Field(
            None, description="", alias="tagAttachmentValue"
        )


class SourceTagAttachment(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        source_tag_name: Optional[str] = Field(
            None, description="", alias="sourceTagName"
        )
        source_tag_qualified_name: Optional[str] = Field(
            None, description="", alias="sourceTagQualifiedName"
        )
        source_tag_guid: Optional[str] = Field(
            None, description="", alias="sourceTagGuid"
        )
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


class AzureTag(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        azure_tag_key: str = Field(None, description="", alias="azureTagKey")
        azure_tag_value: str = Field(None, description="", alias="azureTagValue")


class AwsTag(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        aws_tag_key: str = Field(None, description="", alias="awsTagKey")
        aws_tag_value: str = Field(None, description="", alias="awsTagValue")


class DbtMetricFilter(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
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

    class Attributes(AtlanObject):
        google_tag_key: str = Field(None, description="", alias="googleTagKey")
        google_tag_value: str = Field(None, description="", alias="googleTagValue")


class MCRuleComparison(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
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

    class Attributes(AtlanObject):
        google_label_key: str = Field(None, description="", alias="googleLabelKey")
        google_label_value: str = Field(None, description="", alias="googleLabelValue")


class PopularityInsights(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
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

    class Attributes(AtlanObject):
        tag_attribute_key: Optional[str] = Field(
            None, description="", alias="tagAttributeKey"
        )
        tag_attribute_value: Optional[str] = Field(
            None, description="", alias="tagAttributeValue"
        )
        tag_attribute_properties: Optional[dict[str, str]] = Field(
            None, description="", alias="tagAttributeProperties"
        )
