# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

import hashlib
from io import StringIO
from typing import ClassVar, List, Optional, Set
from warnings import warn

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AIDatasetType
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField
from pyatlan.utils import init_guid, validate_required_fields

from .asset import Asset


class Process(Asset, type_name="Process"):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        name: str,
        connection_qualified_name: str,
        inputs: List["Catalog"],
        outputs: List["Catalog"],
        process_id: Optional[str] = None,
        parent: Optional[Process] = None,
    ) -> Process:
        return Process(
            attributes=Process.Attributes.create(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
        )

    @classmethod
    @init_guid
    def create(
        cls,
        name: str,
        connection_qualified_name: str,
        inputs: List["Catalog"],
        outputs: List["Catalog"],
        process_id: Optional[str] = None,
        parent: Optional[Process] = None,
    ) -> Process:
        warn(
            (
                "This method is deprecated, please use 'creator' "
                "instead, which offers identical functionality."
            ),
            DeprecationWarning,
            stacklevel=2,
        )
        return cls.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            inputs=inputs,
            outputs=outputs,
            process_id=process_id,
            parent=parent,
        )

    type_name: str = Field(default="Process", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Process":
            raise ValueError("must be Process")
        return v

    def __setattr__(self, name, value):
        if name in Process._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

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

    class Attributes(Asset.Attributes):
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

        @staticmethod
        def generate_qualified_name(
            name: str,
            connection_qualified_name: str,
            inputs: List["Catalog"],
            outputs: List["Catalog"],
            parent: Optional["Process"] = None,
            process_id: Optional[str] = None,
        ) -> str:
            def append_relationship(output: StringIO, relationship: Asset):
                if relationship.guid:
                    output.write(relationship.guid)

            def append_relationships(output: StringIO, relationships: List["Catalog"]):
                for catalog in relationships:
                    append_relationship(output, catalog)

            validate_required_fields(
                ["name", "connection_qualified_name", "inputs", "outputs"],
                [name, connection_qualified_name, inputs, outputs],
            )
            if process_id and process_id.strip():
                return f"{connection_qualified_name}/{process_id}"
            buffer = StringIO()
            buffer.write(name)
            buffer.write(connection_qualified_name)
            if parent:
                append_relationship(buffer, parent)
            append_relationships(buffer, inputs)
            append_relationships(buffer, outputs)
            ret_value = hashlib.md5(  # noqa: S303, S324
                buffer.getvalue().encode()
            ).hexdigest()
            buffer.close()
            return f"{connection_qualified_name}/{ret_value}"

        @classmethod
        @init_guid
        def create(
            cls,
            name: str,
            connection_qualified_name: str,
            inputs: List["Catalog"],
            outputs: List["Catalog"],
            process_id: Optional[str] = None,
            parent: Optional[Process] = None,
        ) -> Process.Attributes:
            qualified_name = Process.Attributes.generate_qualified_name(
                name=name,
                connection_qualified_name=connection_qualified_name,
                process_id=process_id,
                inputs=inputs,
                outputs=outputs,
                parent=parent,
            )
            connector_name = connection_qualified_name.split("/")[1]
            return Process.Attributes(
                name=name,
                qualified_name=qualified_name,
                connector_name=connector_name,
                connection_qualified_name=connection_qualified_name,
                inputs=inputs,
                outputs=outputs,
            )

    attributes: Process.Attributes = Field(
        default_factory=lambda: Process.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .adf_activity import AdfActivity  # noqa: E402, F401
from .airflow_task import AirflowTask  # noqa: E402, F401
from .catalog import Catalog  # noqa: E402, F401
from .column_process import ColumnProcess  # noqa: E402, F401
from .fivetran_connector import FivetranConnector  # noqa: E402, F401
from .flow_control_operation import FlowControlOperation  # noqa: E402, F401
from .matillion_component import MatillionComponent  # noqa: E402, F401
from .power_b_i_dataflow import PowerBIDataflow  # noqa: E402, F401
from .spark_job import SparkJob  # noqa: E402, F401
