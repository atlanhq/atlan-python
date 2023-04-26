# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from datetime import datetime
from typing import Optional

from pydantic import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import SourceCostUnitType


class AwsTag(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        aws_tag_key: str = Field(None, description="", alias="awsTagKey")
        aws_tag_value: str = Field(None, description="", alias="awsTagValue")


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


class AzureTag(AtlanObject):
    """Description"""

    class Attributes(AtlanObject):
        azure_tag_key: str = Field(None, description="", alias="azureTagKey")
        azure_tag_value: str = Field(None, description="", alias="azureTagValue")


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
