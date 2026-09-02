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

from .process import Process


class V1CoalesceProcess(Process):
    """Description"""

    type_name: str = Field(default="V1CoalesceProcess", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "V1CoalesceProcess":
            raise ValueError("must be V1CoalesceProcess")
        return v

    def __setattr__(self, name, value):
        if name in V1CoalesceProcess._convenience_properties:
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
    IS_PASS_THROUGH: ClassVar[BooleanField] = BooleanField(
        "isPassThrough", "isPassThrough"
    )
    """
    Whether this process represents a pass-through data flow where data is moved without transformation, as opposed to a flow where data is actively modified.
    """  # noqa: E501
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

    INPUT_TO_SPARK_JOBS: ClassVar[RelationField] = RelationField("inputToSparkJobs")
    """
    TBC
    """
    PARTIAL_CHILD_FIELDS: ClassVar[RelationField] = RelationField("partialChildFields")
    """
    TBC
    """
    INPUT_TO_AIRFLOW_TASKS: ClassVar[RelationField] = RelationField(
        "inputToAirflowTasks"
    )
    """
    TBC
    """
    INPUT_TO_PROCESSES: ClassVar[RelationField] = RelationField("inputToProcesses")
    """
    TBC
    """
    MODEL_IMPLEMENTED_ATTRIBUTES: ClassVar[RelationField] = RelationField(
        "modelImplementedAttributes"
    )
    """
    TBC
    """
    OUTPUT_FROM_AIRFLOW_TASKS: ClassVar[RelationField] = RelationField(
        "outputFromAirflowTasks"
    )
    """
    TBC
    """
    OUTPUT_FROM_SPARK_JOBS: ClassVar[RelationField] = RelationField(
        "outputFromSparkJobs"
    )
    """
    TBC
    """
    MODEL_IMPLEMENTED_ENTITIES: ClassVar[RelationField] = RelationField(
        "modelImplementedEntities"
    )
    """
    TBC
    """
    PARTIAL_CHILD_OBJECTS: ClassVar[RelationField] = RelationField(
        "partialChildObjects"
    )
    """
    TBC
    """
    OUTPUT_FROM_PROCESSES: ClassVar[RelationField] = RelationField(
        "outputFromProcesses"
    )
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
        "is_pass_through",
        "coalesce_project_id",
        "coalesce_project_name",
        "coalesce_workspace_id",
        "coalesce_workspace_name",
        "catalog_dataset_guid",
        "input_to_spark_jobs",
        "partial_child_fields",
        "input_to_airflow_tasks",
        "input_to_processes",
        "model_implemented_attributes",
        "output_from_airflow_tasks",
        "output_from_spark_jobs",
        "model_implemented_entities",
        "partial_child_objects",
        "output_from_processes",
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
    def is_pass_through(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.is_pass_through

    @is_pass_through.setter
    def is_pass_through(self, is_pass_through: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_pass_through = is_pass_through

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
    def input_to_spark_jobs(self) -> Optional[List[SparkJob]]:
        return None if self.attributes is None else self.attributes.input_to_spark_jobs

    @input_to_spark_jobs.setter
    def input_to_spark_jobs(self, input_to_spark_jobs: Optional[List[SparkJob]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_spark_jobs = input_to_spark_jobs

    @property
    def partial_child_fields(self) -> Optional[List[PartialField]]:
        return None if self.attributes is None else self.attributes.partial_child_fields

    @partial_child_fields.setter
    def partial_child_fields(self, partial_child_fields: Optional[List[PartialField]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_child_fields = partial_child_fields

    @property
    def input_to_airflow_tasks(self) -> Optional[List[AirflowTask]]:
        return (
            None if self.attributes is None else self.attributes.input_to_airflow_tasks
        )

    @input_to_airflow_tasks.setter
    def input_to_airflow_tasks(
        self, input_to_airflow_tasks: Optional[List[AirflowTask]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_airflow_tasks = input_to_airflow_tasks

    @property
    def input_to_processes(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.input_to_processes

    @input_to_processes.setter
    def input_to_processes(self, input_to_processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_processes = input_to_processes

    @property
    def model_implemented_attributes(self) -> Optional[List[ModelAttribute]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_implemented_attributes
        )

    @model_implemented_attributes.setter
    def model_implemented_attributes(
        self, model_implemented_attributes: Optional[List[ModelAttribute]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_implemented_attributes = model_implemented_attributes

    @property
    def output_from_airflow_tasks(self) -> Optional[List[AirflowTask]]:
        return (
            None
            if self.attributes is None
            else self.attributes.output_from_airflow_tasks
        )

    @output_from_airflow_tasks.setter
    def output_from_airflow_tasks(
        self, output_from_airflow_tasks: Optional[List[AirflowTask]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_airflow_tasks = output_from_airflow_tasks

    @property
    def output_from_spark_jobs(self) -> Optional[List[SparkJob]]:
        return (
            None if self.attributes is None else self.attributes.output_from_spark_jobs
        )

    @output_from_spark_jobs.setter
    def output_from_spark_jobs(self, output_from_spark_jobs: Optional[List[SparkJob]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_spark_jobs = output_from_spark_jobs

    @property
    def model_implemented_entities(self) -> Optional[List[ModelEntity]]:
        return (
            None
            if self.attributes is None
            else self.attributes.model_implemented_entities
        )

    @model_implemented_entities.setter
    def model_implemented_entities(
        self, model_implemented_entities: Optional[List[ModelEntity]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.model_implemented_entities = model_implemented_entities

    @property
    def partial_child_objects(self) -> Optional[List[PartialObject]]:
        return (
            None if self.attributes is None else self.attributes.partial_child_objects
        )

    @partial_child_objects.setter
    def partial_child_objects(
        self, partial_child_objects: Optional[List[PartialObject]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.partial_child_objects = partial_child_objects

    @property
    def output_from_processes(self) -> Optional[List[Process]]:
        return (
            None if self.attributes is None else self.attributes.output_from_processes
        )

    @output_from_processes.setter
    def output_from_processes(self, output_from_processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_processes = output_from_processes

    class Attributes(Process.Attributes):
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
        coalesce_project_id: Optional[str] = Field(default=None, description="")
        coalesce_project_name: Optional[str] = Field(default=None, description="")
        coalesce_workspace_id: Optional[str] = Field(default=None, description="")
        coalesce_workspace_name: Optional[str] = Field(default=None, description="")
        catalog_dataset_guid: Optional[str] = Field(default=None, description="")
        input_to_spark_jobs: Optional[List[SparkJob]] = Field(
            default=None, description=""
        )  # relationship
        partial_child_fields: Optional[List[PartialField]] = Field(
            default=None, description=""
        )  # relationship
        input_to_airflow_tasks: Optional[List[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        input_to_processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship
        model_implemented_attributes: Optional[List[ModelAttribute]] = Field(
            default=None, description=""
        )  # relationship
        output_from_airflow_tasks: Optional[List[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        output_from_spark_jobs: Optional[List[SparkJob]] = Field(
            default=None, description=""
        )  # relationship
        model_implemented_entities: Optional[List[ModelEntity]] = Field(
            default=None, description=""
        )  # relationship
        partial_child_objects: Optional[List[PartialObject]] = Field(
            default=None, description=""
        )  # relationship
        output_from_processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: V1CoalesceProcess.Attributes = Field(
        default_factory=lambda: V1CoalesceProcess.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .airflow_task import AirflowTask  # noqa: E402, F401
from .catalog import Catalog  # noqa: E402, F401
from .model_attribute import ModelAttribute  # noqa: E402, F401
from .model_entity import ModelEntity  # noqa: E402, F401
from .partial_field import PartialField  # noqa: E402, F401
from .partial_object import PartialObject  # noqa: E402, F401
from .process import Process  # noqa: E402, F401
from .spark_job import SparkJob  # noqa: E402, F401
