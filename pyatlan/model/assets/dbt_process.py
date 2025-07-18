# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AIDatasetType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import DbtJobRun

from .core.dbt import Dbt


class DbtProcess(Dbt):
    """Description"""

    type_name: str = Field(default="DbtProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DbtProcess":
            raise ValueError("must be DbtProcess")
        return v

    def __setattr__(self, name, value):
        if name in DbtProcess._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DBT_PROCESS_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dbtProcessJobStatus", "dbtProcessJobStatus"
    )
    """
    Status of the dbt process job.
    """
    DBT_ALIAS: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAlias", "dbtAlias.keyword", "dbtAlias"
    )
    """
    Alias of this asset in dbt.
    """
    DBT_META: ClassVar[TextField] = TextField("dbtMeta", "dbtMeta")
    """
    Metadata for this asset in dbt, specifically everything under the 'meta' key in the dbt object.
    """
    DBT_UNIQUE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtUniqueId", "dbtUniqueId.keyword", "dbtUniqueId"
    )
    """
    Unique identifier of this asset in dbt.
    """
    DBT_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtAccountName", "dbtAccountName.keyword", "dbtAccountName"
    )
    """
    Name of the account in which this asset exists in dbt.
    """
    DBT_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtProjectName", "dbtProjectName.keyword", "dbtProjectName"
    )
    """
    Name of the project in which this asset exists in dbt.
    """
    DBT_PACKAGE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtPackageName", "dbtPackageName.keyword", "dbtPackageName"
    )
    """
    Name of the package in which this asset exists in dbt.
    """
    DBT_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobName", "dbtJobName.keyword", "dbtJobName"
    )
    """
    Name of the job that materialized this asset in dbt.
    """
    DBT_JOB_SCHEDULE: ClassVar[TextField] = TextField(
        "dbtJobSchedule", "dbtJobSchedule"
    )
    """
    Schedule of the job that materialized this asset in dbt.
    """
    DBT_JOB_STATUS: ClassVar[KeywordField] = KeywordField(
        "dbtJobStatus", "dbtJobStatus"
    )
    """
    Status of the job that materialized this asset in dbt.
    """
    DBT_JOB_SCHEDULE_CRON_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobScheduleCronHumanized",
        "dbtJobScheduleCronHumanized.keyword",
        "dbtJobScheduleCronHumanized",
    )
    """
    Human-readable cron schedule of the job that materialized this asset in dbt.
    """
    DBT_JOB_LAST_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobLastRun", "dbtJobLastRun"
    )
    """
    Time (epoch) at which the job that materialized this asset in dbt last ran, in milliseconds.
    """
    DBT_JOB_NEXT_RUN: ClassVar[NumericField] = NumericField(
        "dbtJobNextRun", "dbtJobNextRun"
    )
    """
    Time (epoch) at which the job that materialized this asset in dbt will next run, in milliseconds.
    """
    DBT_JOB_NEXT_RUN_HUMANIZED: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtJobNextRunHumanized",
        "dbtJobNextRunHumanized.keyword",
        "dbtJobNextRunHumanized",
    )
    """
    Human-readable time at which the job that materialized this asset in dbt will next run.
    """
    DBT_ENVIRONMENT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentName", "dbtEnvironmentName.keyword", "dbtEnvironmentName"
    )
    """
    Name of the environment in which this asset exists in dbt.
    """
    DBT_ENVIRONMENT_DBT_VERSION: ClassVar[KeywordTextField] = KeywordTextField(
        "dbtEnvironmentDbtVersion",
        "dbtEnvironmentDbtVersion.keyword",
        "dbtEnvironmentDbtVersion",
    )
    """
    Version of dbt used in the environment.
    """
    DBT_TAGS: ClassVar[TextField] = TextField("dbtTags", "dbtTags")
    """
    List of tags attached to this asset in dbt.
    """
    DBT_CONNECTION_CONTEXT: ClassVar[TextField] = TextField(
        "dbtConnectionContext", "dbtConnectionContext"
    )
    """
    Connection context for this asset in dbt.
    """
    DBT_SEMANTIC_LAYER_PROXY_URL: ClassVar[KeywordField] = KeywordField(
        "dbtSemanticLayerProxyUrl", "dbtSemanticLayerProxyUrl"
    )
    """
    URL of the semantic layer proxy for this asset in dbt.
    """
    DBT_JOB_RUNS: ClassVar[KeywordField] = KeywordField("dbtJobRuns", "dbtJobRuns")
    """
    List of latest dbt job runs across all environments.
    """
    CODE: ClassVar[TextField] = TextField("code", "code")
    """
    Code that ran within the process.
    """
    SQL: ClassVar[TextField] = TextField("sql", "sql")
    """
    SQL query that ran to produce the outputs.
    """
    PARENT_CONNECTION_PROCESS_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "parentConnectionProcessQualifiedName", "parentConnectionProcessQualifiedName"
    )
    """

    """
    AST: ClassVar[TextField] = TextField("ast", "ast")
    """
    Parsed AST of the code or SQL statements that describe the logic of this process.
    """
    ADDITIONAL_ETL_CONTEXT: ClassVar[TextField] = TextField(
        "additionalEtlContext", "additionalEtlContext"
    )
    """
    Additional Context of the ETL pipeline/notebook which creates the process.
    """
    AI_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "aiDatasetType", "aiDatasetType"
    )
    """
    Dataset type for AI Model - dataset process.
    """

    FLOW_ORCHESTRATED_BY: ClassVar[RelationField] = RelationField("flowOrchestratedBy")
    """
    TBC
    """
    ADF_ACTIVITY: ClassVar[RelationField] = RelationField("adfActivity")
    """
    TBC
    """
    SPARK_JOBS: ClassVar[RelationField] = RelationField("sparkJobs")
    """
    TBC
    """
    MATILLION_COMPONENT: ClassVar[RelationField] = RelationField("matillionComponent")
    """
    TBC
    """
    AIRFLOW_TASKS: ClassVar[RelationField] = RelationField("airflowTasks")
    """
    TBC
    """
    FIVETRAN_CONNECTOR: ClassVar[RelationField] = RelationField("fivetranConnector")
    """
    TBC
    """
    POWER_BI_DATAFLOW: ClassVar[RelationField] = RelationField("powerBIDataflow")
    """
    TBC
    """
    COLUMN_PROCESSES: ClassVar[RelationField] = RelationField("columnProcesses")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dbt_process_job_status",
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
        "dbt_job_runs",
        "inputs",
        "outputs",
        "code",
        "sql",
        "parent_connection_process_qualified_name",
        "ast",
        "additional_etl_context",
        "ai_dataset_type",
        "flow_orchestrated_by",
        "adf_activity",
        "spark_jobs",
        "matillion_component",
        "airflow_tasks",
        "fivetran_connector",
        "power_b_i_dataflow",
        "column_processes",
    ]

    @property
    def dbt_process_job_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.dbt_process_job_status
        )

    @dbt_process_job_status.setter
    def dbt_process_job_status(self, dbt_process_job_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_process_job_status = dbt_process_job_status

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
    def dbt_job_runs(self) -> Optional[List[DbtJobRun]]:
        return None if self.attributes is None else self.attributes.dbt_job_runs

    @dbt_job_runs.setter
    def dbt_job_runs(self, dbt_job_runs: Optional[List[DbtJobRun]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dbt_job_runs = dbt_job_runs

    @property
    def inputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.inputs

    @inputs.setter
    def inputs(self, inputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.inputs = inputs

    @property
    def outputs(self) -> Optional[List[Catalog]]:
        return None if self.attributes is None else self.attributes.outputs

    @outputs.setter
    def outputs(self, outputs: Optional[List[Catalog]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.outputs = outputs

    @property
    def code(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.code

    @code.setter
    def code(self, code: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.code = code

    @property
    def sql(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.sql

    @sql.setter
    def sql(self, sql: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql = sql

    @property
    def parent_connection_process_qualified_name(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.parent_connection_process_qualified_name
        )

    @parent_connection_process_qualified_name.setter
    def parent_connection_process_qualified_name(
        self, parent_connection_process_qualified_name: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.parent_connection_process_qualified_name = (
            parent_connection_process_qualified_name
        )

    @property
    def ast(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.ast

    @ast.setter
    def ast(self, ast: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ast = ast

    @property
    def additional_etl_context(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.additional_etl_context
        )

    @additional_etl_context.setter
    def additional_etl_context(self, additional_etl_context: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.additional_etl_context = additional_etl_context

    @property
    def ai_dataset_type(self) -> Optional[AIDatasetType]:
        return None if self.attributes is None else self.attributes.ai_dataset_type

    @ai_dataset_type.setter
    def ai_dataset_type(self, ai_dataset_type: Optional[AIDatasetType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.ai_dataset_type = ai_dataset_type

    @property
    def flow_orchestrated_by(self) -> Optional[FlowControlOperation]:
        return None if self.attributes is None else self.attributes.flow_orchestrated_by

    @flow_orchestrated_by.setter
    def flow_orchestrated_by(
        self, flow_orchestrated_by: Optional[FlowControlOperation]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.flow_orchestrated_by = flow_orchestrated_by

    @property
    def adf_activity(self) -> Optional[AdfActivity]:
        return None if self.attributes is None else self.attributes.adf_activity

    @adf_activity.setter
    def adf_activity(self, adf_activity: Optional[AdfActivity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity = adf_activity

    @property
    def spark_jobs(self) -> Optional[List[SparkJob]]:
        return None if self.attributes is None else self.attributes.spark_jobs

    @spark_jobs.setter
    def spark_jobs(self, spark_jobs: Optional[List[SparkJob]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_jobs = spark_jobs

    @property
    def matillion_component(self) -> Optional[MatillionComponent]:
        return None if self.attributes is None else self.attributes.matillion_component

    @matillion_component.setter
    def matillion_component(self, matillion_component: Optional[MatillionComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component = matillion_component

    @property
    def airflow_tasks(self) -> Optional[List[AirflowTask]]:
        return None if self.attributes is None else self.attributes.airflow_tasks

    @airflow_tasks.setter
    def airflow_tasks(self, airflow_tasks: Optional[List[AirflowTask]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.airflow_tasks = airflow_tasks

    @property
    def fivetran_connector(self) -> Optional[FivetranConnector]:
        return None if self.attributes is None else self.attributes.fivetran_connector

    @fivetran_connector.setter
    def fivetran_connector(self, fivetran_connector: Optional[FivetranConnector]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fivetran_connector = fivetran_connector

    @property
    def power_b_i_dataflow(self) -> Optional[PowerBIDataflow]:
        return None if self.attributes is None else self.attributes.power_b_i_dataflow

    @power_b_i_dataflow.setter
    def power_b_i_dataflow(self, power_b_i_dataflow: Optional[PowerBIDataflow]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.power_b_i_dataflow = power_b_i_dataflow

    @property
    def column_processes(self) -> Optional[List[ColumnProcess]]:
        return None if self.attributes is None else self.attributes.column_processes

    @column_processes.setter
    def column_processes(self, column_processes: Optional[List[ColumnProcess]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.column_processes = column_processes

    class Attributes(Dbt.Attributes):
        dbt_process_job_status: Optional[str] = Field(default=None, description="")
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
        dbt_job_runs: Optional[List[DbtJobRun]] = Field(default=None, description="")
        inputs: Optional[List[Catalog]] = Field(default=None, description="")
        outputs: Optional[List[Catalog]] = Field(default=None, description="")
        code: Optional[str] = Field(default=None, description="")
        sql: Optional[str] = Field(default=None, description="")
        parent_connection_process_qualified_name: Optional[Set[str]] = Field(
            default=None, description=""
        )
        ast: Optional[str] = Field(default=None, description="")
        additional_etl_context: Optional[str] = Field(default=None, description="")
        ai_dataset_type: Optional[AIDatasetType] = Field(default=None, description="")
        flow_orchestrated_by: Optional[FlowControlOperation] = Field(
            default=None, description=""
        )  # relationship
        adf_activity: Optional[AdfActivity] = Field(
            default=None, description=""
        )  # relationship
        spark_jobs: Optional[List[SparkJob]] = Field(
            default=None, description=""
        )  # relationship
        matillion_component: Optional[MatillionComponent] = Field(
            default=None, description=""
        )  # relationship
        airflow_tasks: Optional[List[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        fivetran_connector: Optional[FivetranConnector] = Field(
            default=None, description=""
        )  # relationship
        power_b_i_dataflow: Optional[PowerBIDataflow] = Field(
            default=None, description=""
        )  # relationship
        column_processes: Optional[List[ColumnProcess]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DbtProcess.Attributes = Field(
        default_factory=lambda: DbtProcess.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.adf_activity import AdfActivity  # noqa: E402, F401
from .core.airflow_task import AirflowTask  # noqa: E402, F401
from .core.catalog import Catalog  # noqa: E402, F401
from .core.column_process import ColumnProcess  # noqa: E402, F401
from .core.fivetran_connector import FivetranConnector  # noqa: E402, F401
from .core.flow_control_operation import FlowControlOperation  # noqa: E402, F401
from .core.matillion_component import MatillionComponent  # noqa: E402, F401
from .core.power_b_i_dataflow import PowerBIDataflow  # noqa: E402, F401
from .core.spark_job import SparkJob  # noqa: E402, F401

DbtProcess.Attributes.update_forward_refs()
