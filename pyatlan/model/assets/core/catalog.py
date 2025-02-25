# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .asset import Asset


class Catalog(Asset, type_name="Catalog"):
    """Description"""

    type_name: str = Field(default="Catalog", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Catalog":
            raise ValueError("must be Catalog")
        return v

    def __setattr__(self, name, value):
        if name in Catalog._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    INPUT_TO_SPARK_JOBS: ClassVar[RelationField] = RelationField("inputToSparkJobs")
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
    OUTPUT_FROM_PROCESSES: ClassVar[RelationField] = RelationField(
        "outputFromProcesses"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "input_to_spark_jobs",
        "input_to_airflow_tasks",
        "input_to_processes",
        "model_implemented_attributes",
        "output_from_airflow_tasks",
        "output_from_spark_jobs",
        "model_implemented_entities",
        "output_from_processes",
    ]

    @property
    def input_to_spark_jobs(self) -> Optional[List[SparkJob]]:
        return None if self.attributes is None else self.attributes.input_to_spark_jobs

    @input_to_spark_jobs.setter
    def input_to_spark_jobs(self, input_to_spark_jobs: Optional[List[SparkJob]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_spark_jobs = input_to_spark_jobs

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
    def output_from_processes(self) -> Optional[List[Process]]:
        return (
            None if self.attributes is None else self.attributes.output_from_processes
        )

    @output_from_processes.setter
    def output_from_processes(self, output_from_processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_processes = output_from_processes

    class Attributes(Asset.Attributes):
        input_to_spark_jobs: Optional[List[SparkJob]] = Field(
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
        output_from_processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: Catalog.Attributes = Field(
        default_factory=lambda: Catalog.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .airflow_task import AirflowTask  # noqa: E402, F401
from .model_attribute import ModelAttribute  # noqa: E402, F401
from .model_entity import ModelEntity  # noqa: E402, F401
from .process import Process  # noqa: E402, F401
from .spark_job import SparkJob  # noqa: E402, F401
