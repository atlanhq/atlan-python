# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AIDatasetType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    RelationField,
    TextField,
)

from .v1_coalesce import V1Coalesce


class V1CoalesceColumnProcess(V1Coalesce):
    """Description"""

    type_name: str = Field(default="V1CoalesceColumnProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "V1CoalesceColumnProcess":
            raise ValueError("must be V1CoalesceColumnProcess")
        return v

    def __setattr__(self, name, value):
        if name in V1CoalesceColumnProcess._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    COALESCE_PROJECT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceProjectId", "coalesceProjectId.keyword", "coalesceProjectId"
    )
    """
    Unique identifier of the project in which this Coalesce asset exists.
    """
    COALESCE_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceProjectName", "coalesceProjectName.keyword", "coalesceProjectName"
    )
    """
    Name of the project in which this Coalesce asset exists.
    """
    COALESCE_WORKSPACE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceWorkspaceId", "coalesceWorkspaceId.keyword", "coalesceWorkspaceId"
    )
    """
    Unique identifier of the workspace in which this Coalesce asset exists.
    """
    COALESCE_WORKSPACE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "coalesceWorkspaceName",
        "coalesceWorkspaceName.keyword",
        "coalesceWorkspaceName",
    )
    """
    Name of the workspace in which this Coalesce asset exists.
    """
    CATALOG_DATASET_GUID: ClassVar[KeywordField] = KeywordField(
        "catalogDatasetGuid", "catalogDatasetGuid"
    )
    """
    Unique identifier of the dataset this asset belongs to.
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
    IS_PASS_THROUGH: ClassVar[BooleanField] = BooleanField(
        "isPassThrough", "isPassThrough"
    )
    """
    Whether this process represents a pass-through data flow where data is moved without transformation, as opposed to a flow where data is actively modified.
    """  # noqa: E501

    FLOW_ORCHESTRATED_BY: ClassVar[RelationField] = RelationField("flowOrchestratedBy")
    """
    TBC
    """
    SQL_PROCEDURES: ClassVar[RelationField] = RelationField("sqlProcedures")
    """
    TBC
    """
    FABRIC_ACTIVITIES: ClassVar[RelationField] = RelationField("fabricActivities")
    """
    TBC
    """
    ADF_ACTIVITY: ClassVar[RelationField] = RelationField("adfActivity")
    """
    TBC
    """
    BIGQUERY_ROUTINES: ClassVar[RelationField] = RelationField("bigqueryRoutines")
    """
    TBC
    """
    SPARK_JOBS: ClassVar[RelationField] = RelationField("sparkJobs")
    """
    TBC
    """
    SQL_FUNCTIONS: ClassVar[RelationField] = RelationField("sqlFunctions")
    """
    TBC
    """
    MATILLION_COMPONENT: ClassVar[RelationField] = RelationField("matillionComponent")
    """
    TBC
    """
    PROCESS: ClassVar[RelationField] = RelationField("process")
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
        "coalesce_project_id",
        "coalesce_project_name",
        "coalesce_workspace_id",
        "coalesce_workspace_name",
        "catalog_dataset_guid",
        "inputs",
        "outputs",
        "code",
        "sql",
        "parent_connection_process_qualified_name",
        "ast",
        "additional_etl_context",
        "ai_dataset_type",
        "is_pass_through",
        "flow_orchestrated_by",
        "sql_procedures",
        "fabric_activities",
        "adf_activity",
        "bigquery_routines",
        "spark_jobs",
        "sql_functions",
        "matillion_component",
        "process",
        "airflow_tasks",
        "fivetran_connector",
        "power_b_i_dataflow",
        "column_processes",
    ]

    @property
    def coalesce_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.coalesce_project_id

    @coalesce_project_id.setter
    def coalesce_project_id(self, coalesce_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_project_id = coalesce_project_id

    @property
    def coalesce_project_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_project_name
        )

    @coalesce_project_name.setter
    def coalesce_project_name(self, coalesce_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_project_name = coalesce_project_name

    @property
    def coalesce_workspace_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_workspace_id
        )

    @coalesce_workspace_id.setter
    def coalesce_workspace_id(self, coalesce_workspace_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_workspace_id = coalesce_workspace_id

    @property
    def coalesce_workspace_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.coalesce_workspace_name
        )

    @coalesce_workspace_name.setter
    def coalesce_workspace_name(self, coalesce_workspace_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.coalesce_workspace_name = coalesce_workspace_name

    @property
    def catalog_dataset_guid(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.catalog_dataset_guid

    @catalog_dataset_guid.setter
    def catalog_dataset_guid(self, catalog_dataset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.catalog_dataset_guid = catalog_dataset_guid

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
    def is_pass_through(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_pass_through

    @is_pass_through.setter
    def is_pass_through(self, is_pass_through: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_pass_through = is_pass_through

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
    def sql_procedures(self) -> Optional[List[Procedure]]:
        return None if self.attributes is None else self.attributes.sql_procedures

    @sql_procedures.setter
    def sql_procedures(self, sql_procedures: Optional[List[Procedure]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_procedures = sql_procedures

    @property
    def fabric_activities(self) -> Optional[List[FabricActivity]]:
        return None if self.attributes is None else self.attributes.fabric_activities

    @fabric_activities.setter
    def fabric_activities(self, fabric_activities: Optional[List[FabricActivity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.fabric_activities = fabric_activities

    @property
    def adf_activity(self) -> Optional[AdfActivity]:
        return None if self.attributes is None else self.attributes.adf_activity

    @adf_activity.setter
    def adf_activity(self, adf_activity: Optional[AdfActivity]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity = adf_activity

    @property
    def bigquery_routines(self) -> Optional[List[BigqueryRoutine]]:
        return None if self.attributes is None else self.attributes.bigquery_routines

    @bigquery_routines.setter
    def bigquery_routines(self, bigquery_routines: Optional[List[BigqueryRoutine]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.bigquery_routines = bigquery_routines

    @property
    def spark_jobs(self) -> Optional[List[SparkJob]]:
        return None if self.attributes is None else self.attributes.spark_jobs

    @spark_jobs.setter
    def spark_jobs(self, spark_jobs: Optional[List[SparkJob]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.spark_jobs = spark_jobs

    @property
    def sql_functions(self) -> Optional[List[Function]]:
        return None if self.attributes is None else self.attributes.sql_functions

    @sql_functions.setter
    def sql_functions(self, sql_functions: Optional[List[Function]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.sql_functions = sql_functions

    @property
    def matillion_component(self) -> Optional[MatillionComponent]:
        return None if self.attributes is None else self.attributes.matillion_component

    @matillion_component.setter
    def matillion_component(self, matillion_component: Optional[MatillionComponent]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component = matillion_component

    @property
    def process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.process

    @process.setter
    def process(self, process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.process = process

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

    class Attributes(V1Coalesce.Attributes):
        coalesce_project_id: Optional[str] = Field(default=None, description="")
        coalesce_project_name: Optional[str] = Field(default=None, description="")
        coalesce_workspace_id: Optional[str] = Field(default=None, description="")
        coalesce_workspace_name: Optional[str] = Field(default=None, description="")
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
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
        is_pass_through: Optional[bool] = Field(default=None, description="")
        flow_orchestrated_by: Optional[FlowControlOperation] = Field(
            default=None, description=""
        )  # relationship
        sql_procedures: Optional[List[Procedure]] = Field(
            default=None, description=""
        )  # relationship
        fabric_activities: Optional[List[FabricActivity]] = Field(
            default=None, description=""
        )  # relationship
        adf_activity: Optional[AdfActivity] = Field(
            default=None, description=""
        )  # relationship
        bigquery_routines: Optional[List[BigqueryRoutine]] = Field(
            default=None, description=""
        )  # relationship
        spark_jobs: Optional[List[SparkJob]] = Field(
            default=None, description=""
        )  # relationship
        sql_functions: Optional[List[Function]] = Field(
            default=None, description=""
        )  # relationship
        matillion_component: Optional[MatillionComponent] = Field(
            default=None, description=""
        )  # relationship
        process: Optional[Process] = Field(default=None, description="")  # relationship
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

    attributes: V1CoalesceColumnProcess.Attributes = Field(
        default_factory=lambda: V1CoalesceColumnProcess.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.adf_activity import AdfActivity  # noqa: E402, F401
from .core.airflow_task import AirflowTask  # noqa: E402, F401
from .core.bigquery_routine import BigqueryRoutine  # noqa: E402, F401
from .core.catalog import Catalog  # noqa: E402, F401
from .core.column_process import ColumnProcess  # noqa: E402, F401
from .core.fabric_activity import FabricActivity  # noqa: E402, F401
from .core.fivetran_connector import FivetranConnector  # noqa: E402, F401
from .core.flow_control_operation import FlowControlOperation  # noqa: E402, F401
from .core.function import Function  # noqa: E402, F401
from .core.matillion_component import MatillionComponent  # noqa: E402, F401
from .core.power_b_i_dataflow import PowerBIDataflow  # noqa: E402, F401
from .core.procedure import Procedure  # noqa: E402, F401
from .core.process import Process  # noqa: E402, F401
from .core.spark_job import SparkJob  # noqa: E402, F401

V1CoalesceColumnProcess.Attributes.update_forward_refs()
