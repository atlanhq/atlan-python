# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import DbtMetricFilter

from .dbt import Dbt


class DbtMetric(Dbt):
    """Description"""

    type_name: str = Field(default="DbtMetric", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtMetric":
            raise ValueError("must be DbtMetric")
        return v

    def __setattr__(self, name, value):
        if name in DbtMetric._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_METRIC_FILTERS: ClassVar[KeywordField] = KeywordField(
        "dbtMetricFilters", "dbtMetricFilters"
    )
    """

    """
    DBT_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAlias", "dbtAlias.keyword", "dbtAlias"
    )
    """

    """
    DBT_META: ClassVar[KeywordField] = KeywordField("dbtMeta", "dbtMeta")
    """

    """
    DBT_UNIQUE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtUniqueId", "dbtUniqueId.keyword", "dbtUniqueId"
    )
    """

    """
    DBT_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAccountName", "dbtAccountName.keyword", "dbtAccountName"
    )
    """

    """
    DBT_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtProjectName", "dbtProjectName.keyword", "dbtProjectName"
    )
    """

    """
    DBT_PACKAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtPackageName", "dbtPackageName.keyword", "dbtPackageName"
    )
    """

    """
    DBT_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobName", "dbtJobName.keyword", "dbtJobName"
    )
    """

    """
    DBT_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "dbtJobSchedule", "dbtJobSchedule"
    )
    """

    """
    DBT_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dbtJobStatus", "dbtJobStatus"
    )
    """

    """
    DBT_JOB_SCHEDULE_CRON_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobScheduleCronHumanized",
        "dbtJobScheduleCronHumanized.keyword",
        "dbtJobScheduleCronHumanized",
    )
    """

    """
    DBT_JOB_LAST_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobLastRun", "dbtJobLastRun"
    )
    """

    """
    DBT_JOB_NEXT_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobNextRun", "dbtJobNextRun"
    )
    """

    """
    DBT_JOB_NEXT_RUN_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobNextRunHumanized",
        "dbtJobNextRunHumanized.keyword",
        "dbtJobNextRunHumanized",
    )
    """

    """
    DBT_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentName", "dbtEnvironmentName.keyword", "dbtEnvironmentName"
    )
    """

    """
    DBT_ENVIRONMENT_DBT_VERSION: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentDbtVersion",
        "dbtEnvironmentDbtVersion.keyword",
        "dbtEnvironmentDbtVersion",
    )
    """

    """
    DBT_TAGS: ClassVar[KeywordField] = KeywordField("dbtTags", "dbtTags")
    """

    """
    DBT_CONNECTION_CONTEXT: ClassVar[KeywordField] = KeywordField(
        "dbtConnectionContext", "dbtConnectionContext"
    )
    """

    """
    DBT_SEMANTIC_LAYER_PROXY_URL: ClassVar[KeywordField] = KeywordField(
        "dbtSemanticLayerProxyUrl", "dbtSemanticLayerProxyUrl"
    )
    """

    """
    METRIC_TYPE: ClassVar[KeywordField] = KeywordField("metricType", "metricType")
    """
    Type of the metric.
    """
    METRIC_SQL: ClassVar[KeywordField] = KeywordField("metricSQL", "metricSQL")
    """
    SQL query used to compute the metric.
    """
    METRIC_FILTERS: ClassVar[TextField] = TextField("metricFilters", "metricFilters")
    """
    Filters to be applied to the metric query.
    """
    METRIC_TIME_GRAINS: ClassVar[TextField] = TextField(
        "metricTimeGrains", "metricTimeGrains"
    )
    """
    List of time grains to be applied to the metric query.
    """

    METRIC_TIMESTAMP_COLUMN: ClassVar[RelationField] = RelationField(
        "metricTimestampColumn"
    )
    """
    TBC
    """
    DBT_MODEL: ClassVar[RelationField] = RelationField("dbtModel")
    """
    TBC
    """
    ASSETS: ClassVar[RelationField] = RelationField("assets")
    """
    TBC
    """
    METRIC_DIMENSION_COLUMNS: ClassVar[RelationField] = RelationField(
        "metricDimensionColumns"
    )
    """
    TBC
    """
    DBT_METRIC_FILTER_COLUMNS: ClassVar[RelationField] = RelationField(
        "dbtMetricFilterColumns"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dbt_metric_filters",
        "dbt_alias",
        "dbt_meta",
        "dbt_unique_id",
        "dbt_account_name",
        "dbt_project_name",
        "dbt_package_name",
        "dbt_job_name",
        "dbt_job_schedule",
        "dbt_job_status",
        "dbt_job_schedule_cron_humanized",
        "dbt_job_last_run",
        "dbt_job_next_run",
        "dbt_job_next_run_humanized",
        "dbt_environment_name",
        "dbt_environment_dbt_version",
        "dbt_tags",
        "dbt_connection_context",
        "dbt_semantic_layer_proxy_url",
        "metric_type",
        "metric_s_q_l",
        "metric_filters",
        "metric_time_grains",
        "metric_timestamp_column",
        "dbt_model",
        "assets",
        "metric_dimension_columns",
        "dbt_metric_filter_columns",
    ]

    @property
    def dbt_metric_filters(self) -> Optional[List[DbtMetricFilter]]:
        return None if self.attributes is None else self.attributes.dbt_metric_filters

    @dbt_metric_filters.setter
    def dbt_metric_filters(self, dbt_metric_filters: Optional[List[DbtMetricFilter]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metric_filters = dbt_metric_filters

    @property
    def dbt_alias(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_alias

    @dbt_alias.setter
    def dbt_alias(self, dbt_alias: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_alias = dbt_alias

    @property
    def dbt_meta(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_meta

    @dbt_meta.setter
    def dbt_meta(self, dbt_meta: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_meta = dbt_meta

    @property
    def dbt_unique_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_unique_id

    @dbt_unique_id.setter
    def dbt_unique_id(self, dbt_unique_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_unique_id = dbt_unique_id

    @property
    def dbt_account_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_account_name

    @dbt_account_name.setter
    def dbt_account_name(self, dbt_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_account_name = dbt_account_name

    @property
    def dbt_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_project_name

    @dbt_project_name.setter
    def dbt_project_name(self, dbt_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_project_name = dbt_project_name

    @property
    def dbt_package_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_package_name

    @dbt_package_name.setter
    def dbt_package_name(self, dbt_package_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_package_name = dbt_package_name

    @property
    def dbt_job_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_name

    @dbt_job_name.setter
    def dbt_job_name(self, dbt_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_name = dbt_job_name

    @property
    def dbt_job_schedule(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_schedule

    @dbt_job_schedule.setter
    def dbt_job_schedule(self, dbt_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule = dbt_job_schedule

    @property
    def dbt_job_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_job_status

    @dbt_job_status.setter
    def dbt_job_status(self, dbt_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_status = dbt_job_status

    @property
    def dbt_job_schedule_cron_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_job_schedule_cron_humanized
        )

    @dbt_job_schedule_cron_humanized.setter
    def dbt_job_schedule_cron_humanized(
        self, dbt_job_schedule_cron_humanized: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_schedule_cron_humanized = (
            dbt_job_schedule_cron_humanized
        )

    @property
    def dbt_job_last_run(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.dbt_job_last_run

    @dbt_job_last_run.setter
    def dbt_job_last_run(self, dbt_job_last_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_last_run = dbt_job_last_run

    @property
    def dbt_job_next_run(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.dbt_job_next_run

    @dbt_job_next_run.setter
    def dbt_job_next_run(self, dbt_job_next_run: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run = dbt_job_next_run

    @property
    def dbt_job_next_run_humanized(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_job_next_run_humanized
        )

    @dbt_job_next_run_humanized.setter
    def dbt_job_next_run_humanized(self, dbt_job_next_run_humanized: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_next_run_humanized = dbt_job_next_run_humanized

    @property
    def dbt_environment_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_environment_name

    @dbt_environment_name.setter
    def dbt_environment_name(self, dbt_environment_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_name = dbt_environment_name

    @property
    def dbt_environment_dbt_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_environment_dbt_version
        )

    @dbt_environment_dbt_version.setter
    def dbt_environment_dbt_version(self, dbt_environment_dbt_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_environment_dbt_version = dbt_environment_dbt_version

    @property
    def dbt_tags(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.dbt_tags

    @dbt_tags.setter
    def dbt_tags(self, dbt_tags: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tags = dbt_tags

    @property
    def dbt_connection_context(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dbt_connection_context
        )

    @dbt_connection_context.setter
    def dbt_connection_context(self, dbt_connection_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_connection_context = dbt_connection_context

    @property
    def dbt_semantic_layer_proxy_url(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_semantic_layer_proxy_url
        )

    @dbt_semantic_layer_proxy_url.setter
    def dbt_semantic_layer_proxy_url(self, dbt_semantic_layer_proxy_url: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_semantic_layer_proxy_url = dbt_semantic_layer_proxy_url

    @property
    def metric_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_type

    @metric_type.setter
    def metric_type(self, metric_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_type = metric_type

    @property
    def metric_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_s_q_l

    @metric_s_q_l.setter
    def metric_s_q_l(self, metric_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_s_q_l = metric_s_q_l

    @property
    def metric_filters(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.metric_filters

    @metric_filters.setter
    def metric_filters(self, metric_filters: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_filters = metric_filters

    @property
    def metric_time_grains(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.metric_time_grains

    @metric_time_grains.setter
    def metric_time_grains(self, metric_time_grains: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_time_grains = metric_time_grains

    @property
    def metric_timestamp_column(self) -> Optional[Column]:
        return (
            None if self.attributes is None else self.attributes.metric_timestamp_column
        )

    @metric_timestamp_column.setter
    def metric_timestamp_column(self, metric_timestamp_column: Optional[Column]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_timestamp_column = metric_timestamp_column

    @property
    def dbt_model(self) -> Optional[DbtModel]:
        return None if self.attributes is None else self.attributes.dbt_model

    @dbt_model.setter
    def dbt_model(self, dbt_model: Optional[DbtModel]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model = dbt_model

    @property
    def assets(self) -> Optional[List[Asset]]:
        return None if self.attributes is None else self.attributes.assets

    @assets.setter
    def assets(self, assets: Optional[List[Asset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.assets = assets

    @property
    def metric_dimension_columns(self) -> Optional[List[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.metric_dimension_columns
        )

    @metric_dimension_columns.setter
    def metric_dimension_columns(
        self, metric_dimension_columns: Optional[List[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.metric_dimension_columns = metric_dimension_columns

    @property
    def dbt_metric_filter_columns(self) -> Optional[List[Column]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_metric_filter_columns
        )

    @dbt_metric_filter_columns.setter
    def dbt_metric_filter_columns(
        self, dbt_metric_filter_columns: Optional[List[Column]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metric_filter_columns = dbt_metric_filter_columns

    class Attributes(Dbt.Attributes):
        dbt_metric_filters: Optional[List[DbtMetricFilter]] = Field(
            default=None, description=""
        )
        dbt_alias: Optional[str] = Field(default=None, description="")
        dbt_meta: Optional[str] = Field(default=None, description="")
        dbt_unique_id: Optional[str] = Field(default=None, description="")
        dbt_account_name: Optional[str] = Field(default=None, description="")
        dbt_project_name: Optional[str] = Field(default=None, description="")
        dbt_package_name: Optional[str] = Field(default=None, description="")
        dbt_job_name: Optional[str] = Field(default=None, description="")
        dbt_job_schedule: Optional[str] = Field(default=None, description="")
        dbt_job_status: Optional[str] = Field(default=None, description="")
        dbt_job_schedule_cron_humanized: Optional[str] = Field(
            default=None, description=""
        )
        dbt_job_last_run: Optional[datetime] = Field(default=None, description="")
        dbt_job_next_run: Optional[datetime] = Field(default=None, description="")
        dbt_job_next_run_humanized: Optional[str] = Field(default=None, description="")
        dbt_environment_name: Optional[str] = Field(default=None, description="")
        dbt_environment_dbt_version: Optional[str] = Field(default=None, description="")
        dbt_tags: Optional[Set[str]] = Field(default=None, description="")
        dbt_connection_context: Optional[str] = Field(default=None, description="")
        dbt_semantic_layer_proxy_url: Optional[str] = Field(
            default=None, description=""
        )
        metric_type: Optional[str] = Field(default=None, description="")
        metric_s_q_l: Optional[str] = Field(default=None, description="")
        metric_filters: Optional[str] = Field(default=None, description="")
        metric_time_grains: Optional[Set[str]] = Field(default=None, description="")
        metric_timestamp_column: Optional[Column] = Field(
            default=None, description=""
        )  # relationship
        dbt_model: Optional[DbtModel] = Field(
            default=None, description=""
        )  # relationship
        assets: Optional[List[Asset]] = Field(
            default=None, description=""
        )  # relationship
        metric_dimension_columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship
        dbt_metric_filter_columns: Optional[List[Column]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DbtMetric.Attributes = Field(
        default_factory=lambda: DbtMetric.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .asset import Asset  # noqa
from .column import Column  # noqa
from .dbt_model import DbtModel  # noqa
