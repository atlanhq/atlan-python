# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, NumericField, RelationField

from .dbt import Dbt


class DbtModel(Dbt):
    """Description"""

    type_name: str = Field(default="DbtModel", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtModel":
            raise ValueError("must be DbtModel")
        return v

    def __setattr__(self, name, value):
        if name in DbtModel._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_STATUS: ClassVar[KeywordField] = KeywordField("dbtStatus", "dbtStatus")
    """

    """
    DBT_ERROR: ClassVar[KeywordField] = KeywordField("dbtError", "dbtError")
    """

    """
    DBT_RAW_SQL: ClassVar[KeywordField] = KeywordField("dbtRawSQL", "dbtRawSQL")
    """

    """
    DBT_COMPILED_SQL: ClassVar[KeywordField] = KeywordField(
        "dbtCompiledSQL", "dbtCompiledSQL"
    )
    """

    """
    DBT_STATS: ClassVar[KeywordField] = KeywordField("dbtStats", "dbtStats")
    """

    """
    DBT_MATERIALIZATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "dbtMaterializationType", "dbtMaterializationType"
    )
    """

    """
    DBT_MODEL_COMPILE_STARTED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelCompileStartedAt", "dbtModelCompileStartedAt"
    )
    """

    """
    DBT_MODEL_COMPILE_COMPLETED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelCompileCompletedAt", "dbtModelCompileCompletedAt"
    )
    """

    """
    DBT_MODEL_EXECUTE_STARTED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelExecuteStartedAt", "dbtModelExecuteStartedAt"
    )
    """

    """
    DBT_MODEL_EXECUTE_COMPLETED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelExecuteCompletedAt", "dbtModelExecuteCompletedAt"
    )
    """

    """
    DBT_MODEL_EXECUTION_TIME: ClassVar[NumericField] = NumericField(
        "dbtModelExecutionTime", "dbtModelExecutionTime"
    )
    """

    """
    DBT_MODEL_RUN_GENERATED_AT: ClassVar[NumericField] = NumericField(
        "dbtModelRunGeneratedAt", "dbtModelRunGeneratedAt"
    )
    """

    """
    DBT_MODEL_RUN_ELAPSED_TIME: ClassVar[NumericField] = NumericField(
        "dbtModelRunElapsedTime", "dbtModelRunElapsedTime"
    )
    """

    """

    DBT_METRICS: ClassVar[RelationField] = RelationField("dbtMetrics")
    """
    TBC
    """
    DBT_TESTS: ClassVar[RelationField] = RelationField("dbtTests")
    """
    TBC
    """
    DBT_MODEL_SQL_ASSETS: ClassVar[RelationField] = RelationField("dbtModelSqlAssets")
    """
    TBC
    """
    DBT_MODEL_COLUMNS: ClassVar[RelationField] = RelationField("dbtModelColumns")
    """
    TBC
    """
    SQL_ASSET: ClassVar[RelationField] = RelationField("sqlAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dbt_status",
        "dbt_error",
        "dbt_raw_s_q_l",
        "dbt_compiled_s_q_l",
        "dbt_stats",
        "dbt_materialization_type",
        "dbt_model_compile_started_at",
        "dbt_model_compile_completed_at",
        "dbt_model_execute_started_at",
        "dbt_model_execute_completed_at",
        "dbt_model_execution_time",
        "dbt_model_run_generated_at",
        "dbt_model_run_elapsed_time",
        "dbt_metrics",
        "dbt_tests",
        "dbt_model_sql_assets",
        "dbt_model_columns",
        "sql_asset",
    ]

    @property
    def dbt_status(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_status

    @dbt_status.setter
    def dbt_status(self, dbt_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_status = dbt_status

    @property
    def dbt_error(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_error

    @dbt_error.setter
    def dbt_error(self, dbt_error: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_error = dbt_error

    @property
    def dbt_raw_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_raw_s_q_l

    @dbt_raw_s_q_l.setter
    def dbt_raw_s_q_l(self, dbt_raw_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_raw_s_q_l = dbt_raw_s_q_l

    @property
    def dbt_compiled_s_q_l(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_compiled_s_q_l

    @dbt_compiled_s_q_l.setter
    def dbt_compiled_s_q_l(self, dbt_compiled_s_q_l: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_compiled_s_q_l = dbt_compiled_s_q_l

    @property
    def dbt_stats(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dbt_stats

    @dbt_stats.setter
    def dbt_stats(self, dbt_stats: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_stats = dbt_stats

    @property
    def dbt_materialization_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_materialization_type
        )

    @dbt_materialization_type.setter
    def dbt_materialization_type(self, dbt_materialization_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_materialization_type = dbt_materialization_type

    @property
    def dbt_model_compile_started_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_compile_started_at
        )

    @dbt_model_compile_started_at.setter
    def dbt_model_compile_started_at(
        self, dbt_model_compile_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_compile_started_at = dbt_model_compile_started_at

    @property
    def dbt_model_compile_completed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_compile_completed_at
        )

    @dbt_model_compile_completed_at.setter
    def dbt_model_compile_completed_at(
        self, dbt_model_compile_completed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_compile_completed_at = dbt_model_compile_completed_at

    @property
    def dbt_model_execute_started_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_execute_started_at
        )

    @dbt_model_execute_started_at.setter
    def dbt_model_execute_started_at(
        self, dbt_model_execute_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execute_started_at = dbt_model_execute_started_at

    @property
    def dbt_model_execute_completed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_execute_completed_at
        )

    @dbt_model_execute_completed_at.setter
    def dbt_model_execute_completed_at(
        self, dbt_model_execute_completed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execute_completed_at = dbt_model_execute_completed_at

    @property
    def dbt_model_execution_time(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_execution_time
        )

    @dbt_model_execution_time.setter
    def dbt_model_execution_time(self, dbt_model_execution_time: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_execution_time = dbt_model_execution_time

    @property
    def dbt_model_run_generated_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_run_generated_at
        )

    @dbt_model_run_generated_at.setter
    def dbt_model_run_generated_at(
        self, dbt_model_run_generated_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_run_generated_at = dbt_model_run_generated_at

    @property
    def dbt_model_run_elapsed_time(self) -> Optional[float]:
        return (
            None
            if self.attributes is None
            else self.attributes.dbt_model_run_elapsed_time
        )

    @dbt_model_run_elapsed_time.setter
    def dbt_model_run_elapsed_time(self, dbt_model_run_elapsed_time: Optional[float]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_run_elapsed_time = dbt_model_run_elapsed_time

    @property
    def dbt_metrics(self) -> Optional[List[DbtMetric]]:
        return None if self.attributes is None else self.attributes.dbt_metrics

    @dbt_metrics.setter
    def dbt_metrics(self, dbt_metrics: Optional[List[DbtMetric]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_metrics = dbt_metrics

    @property
    def dbt_tests(self) -> Optional[List[DbtTest]]:
        return None if self.attributes is None else self.attributes.dbt_tests

    @dbt_tests.setter
    def dbt_tests(self, dbt_tests: Optional[List[DbtTest]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_tests = dbt_tests

    @property
    def dbt_model_sql_assets(self) -> Optional[List[SQL]]:
        return None if self.attributes is None else self.attributes.dbt_model_sql_assets

    @dbt_model_sql_assets.setter
    def dbt_model_sql_assets(self, dbt_model_sql_assets: Optional[List[SQL]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_sql_assets = dbt_model_sql_assets

    @property
    def dbt_model_columns(self) -> Optional[List[DbtModelColumn]]:
        return None if self.attributes is None else self.attributes.dbt_model_columns

    @dbt_model_columns.setter
    def dbt_model_columns(self, dbt_model_columns: Optional[List[DbtModelColumn]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_model_columns = dbt_model_columns

    @property
    def sql_asset(self) -> Optional[SQL]:
        return None if self.attributes is None else self.attributes.sql_asset

    @sql_asset.setter
    def sql_asset(self, sql_asset: Optional[SQL]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_asset = sql_asset

    class Attributes(Dbt.Attributes):
        dbt_status: Optional[str] = Field(default=None, description="")
        dbt_error: Optional[str] = Field(default=None, description="")
        dbt_raw_s_q_l: Optional[str] = Field(default=None, description="")
        dbt_compiled_s_q_l: Optional[str] = Field(default=None, description="")
        dbt_stats: Optional[str] = Field(default=None, description="")
        dbt_materialization_type: Optional[str] = Field(default=None, description="")
        dbt_model_compile_started_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_compile_completed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_execute_started_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_execute_completed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_execution_time: Optional[float] = Field(default=None, description="")
        dbt_model_run_generated_at: Optional[datetime] = Field(
            default=None, description=""
        )
        dbt_model_run_elapsed_time: Optional[float] = Field(
            default=None, description=""
        )
        dbt_metrics: Optional[List[DbtMetric]] = Field(
            default=None, description=""
        )  # relationship
        dbt_tests: Optional[List[DbtTest]] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_sql_assets: Optional[List[SQL]] = Field(
            default=None, description=""
        )  # relationship
        dbt_model_columns: Optional[List[DbtModelColumn]] = Field(
            default=None, description=""
        )  # relationship
        sql_asset: Optional[SQL] = Field(default=None, description="")  # relationship

    attributes: DbtModel.Attributes = Field(
        default_factory=lambda: DbtModel.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dbt_metric import DbtMetric  # noqa
from .dbt_model_column import DbtModelColumn  # noqa
from .dbt_test import DbtTest  # noqa
from .s_q_l import SQL  # noqa
