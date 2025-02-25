# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AdfActivityState
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
    TextField,
)

from .a_d_f import ADF


class AdfActivity(ADF):
    """Description"""

    type_name: str = Field(default="AdfActivity", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AdfActivity":
            raise ValueError("must be AdfActivity")
        return v

    def __setattr__(self, name, value):
        if name in AdfActivity._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADF_ACTIVITY_TYPE: ClassVar[KeywordField] = KeywordField(
        "adfActivityType", "adfActivityType"
    )
    """
    The type of the ADF activity.
    """
    ADF_ACTIVITY_PRECEDING_DEPENDENCY: ClassVar[TextField] = TextField(
        "adfActivityPrecedingDependency", "adfActivityPrecedingDependency"
    )
    """
    The list of ADF activities on which this ADF activity depends on.
    """
    ADF_ACTIVITY_POLICY_TIMEOUT: ClassVar[TextField] = TextField(
        "adfActivityPolicyTimeout", "adfActivityPolicyTimeout"
    )
    """
    The timout defined for the ADF activity.
    """
    ADF_ACTIVITY_POLICT_RETRY_INTERVAL: ClassVar[NumericField] = NumericField(
        "adfActivityPolictRetryInterval", "adfActivityPolictRetryInterval"
    )
    """
    The retry interval in seconds for the ADF activity.
    """
    ADF_ACTIVITY_STATE: ClassVar[KeywordField] = KeywordField(
        "adfActivityState", "adfActivityState"
    )
    """
    Defines the state (Active or Inactive) of an ADF activity whether it is active or not.
    """
    ADF_ACTIVITY_SOURCES: ClassVar[TextField] = TextField(
        "adfActivitySources", "adfActivitySources"
    )
    """
    The list of names of sources for the ADF activity.
    """
    ADF_ACTIVITY_SINKS: ClassVar[TextField] = TextField(
        "adfActivitySinks", "adfActivitySinks"
    )
    """
    The list of names of sinks for the ADF activity.
    """
    ADF_ACTIVITY_SOURCE_TYPE: ClassVar[TextField] = TextField(
        "adfActivitySourceType", "adfActivitySourceType"
    )
    """
    Defines the type of the source of the ADF activtity.
    """
    ADF_ACTIVITY_SINK_TYPE: ClassVar[TextField] = TextField(
        "adfActivitySinkType", "adfActivitySinkType"
    )
    """
    Defines the type of the sink of the ADF activtity.
    """
    ADF_ACTIVITY_RUNS: ClassVar[KeywordField] = KeywordField(
        "adfActivityRuns", "adfActivityRuns"
    )
    """
    List of objects of activity runs for a particular activity.
    """
    ADF_ACTIVITY_NOTEBOOK_PATH: ClassVar[TextField] = TextField(
        "adfActivityNotebookPath", "adfActivityNotebookPath"
    )
    """
    Defines the path of the notebook in the databricks notebook activity.
    """
    ADF_ACTIVITY_MAIN_CLASS_NAME: ClassVar[TextField] = TextField(
        "adfActivityMainClassName", "adfActivityMainClassName"
    )
    """
    Defines the main class of the databricks spark activity.
    """
    ADF_ACTIVITY_PYTHON_FILE_PATH: ClassVar[TextField] = TextField(
        "adfActivityPythonFilePath", "adfActivityPythonFilePath"
    )
    """
    Defines the python file path for databricks python activity.
    """
    ADF_ACTIVITY_FIRST_ROW_ONLY: ClassVar[BooleanField] = BooleanField(
        "adfActivityFirstRowOnly", "adfActivityFirstRowOnly"
    )
    """
    Indicates whether to import only first row only or not in Lookup activity.
    """
    ADF_ACTIVITY_BATCH_COUNT: ClassVar[NumericField] = NumericField(
        "adfActivityBatchCount", "adfActivityBatchCount"
    )
    """
    Defines the batch count of activity to runs in ForEach activity.
    """
    ADF_ACTIVITY_IS_SEQUENTIAL: ClassVar[BooleanField] = BooleanField(
        "adfActivityIsSequential", "adfActivityIsSequential"
    )
    """
    Indicates whether the activity processing is sequential or not inside the ForEach activity.
    """
    ADF_ACTIVITY_SUB_ACTIVITIES: ClassVar[TextField] = TextField(
        "adfActivitySubActivities", "adfActivitySubActivities"
    )
    """
    The list of activities to be run inside a ForEach activity.
    """
    ADF_ACTIVITY_REFERENCE_DATAFLOW: ClassVar[TextField] = TextField(
        "adfActivityReferenceDataflow", "adfActivityReferenceDataflow"
    )
    """
    Defines the dataflow that is to be used in dataflow activity.
    """
    ADF_PIPELINE_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "adfPipelineQualifiedName",
        "adfPipelineQualifiedName",
        "adfPipelineQualifiedName.text",
    )
    """
    Unique name of the pipeline in which this activity exists.
    """

    ADF_LINKEDSERVICES: ClassVar[RelationField] = RelationField("adfLinkedservices")
    """
    TBC
    """
    ADF_DATASETS: ClassVar[RelationField] = RelationField("adfDatasets")
    """
    TBC
    """
    PROCESSES: ClassVar[RelationField] = RelationField("processes")
    """
    TBC
    """
    ADF_PIPELINE: ClassVar[RelationField] = RelationField("adfPipeline")
    """
    TBC
    """
    ADF_DATAFLOW: ClassVar[RelationField] = RelationField("adfDataflow")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adf_activity_type",
        "adf_activity_preceding_dependency",
        "adf_activity_policy_timeout",
        "adf_activity_polict_retry_interval",
        "adf_activity_state",
        "adf_activity_sources",
        "adf_activity_sinks",
        "adf_activity_source_type",
        "adf_activity_sink_type",
        "adf_activity_runs",
        "adf_activity_notebook_path",
        "adf_activity_main_class_name",
        "adf_activity_python_file_path",
        "adf_activity_first_row_only",
        "adf_activity_batch_count",
        "adf_activity_is_sequential",
        "adf_activity_sub_activities",
        "adf_activity_reference_dataflow",
        "adf_pipeline_qualified_name",
        "adf_linkedservices",
        "adf_datasets",
        "processes",
        "adf_pipeline",
        "adf_dataflow",
    ]

    @property
    def adf_activity_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adf_activity_type

    @adf_activity_type.setter
    def adf_activity_type(self, adf_activity_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_type = adf_activity_type

    @property
    def adf_activity_preceding_dependency(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_preceding_dependency
        )

    @adf_activity_preceding_dependency.setter
    def adf_activity_preceding_dependency(
        self, adf_activity_preceding_dependency: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_preceding_dependency = (
            adf_activity_preceding_dependency
        )

    @property
    def adf_activity_policy_timeout(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_policy_timeout
        )

    @adf_activity_policy_timeout.setter
    def adf_activity_policy_timeout(self, adf_activity_policy_timeout: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_policy_timeout = adf_activity_policy_timeout

    @property
    def adf_activity_polict_retry_interval(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_polict_retry_interval
        )

    @adf_activity_polict_retry_interval.setter
    def adf_activity_polict_retry_interval(
        self, adf_activity_polict_retry_interval: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_polict_retry_interval = (
            adf_activity_polict_retry_interval
        )

    @property
    def adf_activity_state(self) -> Optional[AdfActivityState]:
        return None if self.attributes is None else self.attributes.adf_activity_state

    @adf_activity_state.setter
    def adf_activity_state(self, adf_activity_state: Optional[AdfActivityState]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_state = adf_activity_state

    @property
    def adf_activity_sources(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.adf_activity_sources

    @adf_activity_sources.setter
    def adf_activity_sources(self, adf_activity_sources: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_sources = adf_activity_sources

    @property
    def adf_activity_sinks(self) -> Optional[Set[str]]:
        return None if self.attributes is None else self.attributes.adf_activity_sinks

    @adf_activity_sinks.setter
    def adf_activity_sinks(self, adf_activity_sinks: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_sinks = adf_activity_sinks

    @property
    def adf_activity_source_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_source_type
        )

    @adf_activity_source_type.setter
    def adf_activity_source_type(self, adf_activity_source_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_source_type = adf_activity_source_type

    @property
    def adf_activity_sink_type(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adf_activity_sink_type
        )

    @adf_activity_sink_type.setter
    def adf_activity_sink_type(self, adf_activity_sink_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_sink_type = adf_activity_sink_type

    @property
    def adf_activity_runs(self) -> Optional[List[Dict[str, str]]]:
        return None if self.attributes is None else self.attributes.adf_activity_runs

    @adf_activity_runs.setter
    def adf_activity_runs(self, adf_activity_runs: Optional[List[Dict[str, str]]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_runs = adf_activity_runs

    @property
    def adf_activity_notebook_path(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_notebook_path
        )

    @adf_activity_notebook_path.setter
    def adf_activity_notebook_path(self, adf_activity_notebook_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_notebook_path = adf_activity_notebook_path

    @property
    def adf_activity_main_class_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_main_class_name
        )

    @adf_activity_main_class_name.setter
    def adf_activity_main_class_name(self, adf_activity_main_class_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_main_class_name = adf_activity_main_class_name

    @property
    def adf_activity_python_file_path(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_python_file_path
        )

    @adf_activity_python_file_path.setter
    def adf_activity_python_file_path(
        self, adf_activity_python_file_path: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_python_file_path = adf_activity_python_file_path

    @property
    def adf_activity_first_row_only(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_first_row_only
        )

    @adf_activity_first_row_only.setter
    def adf_activity_first_row_only(self, adf_activity_first_row_only: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_first_row_only = adf_activity_first_row_only

    @property
    def adf_activity_batch_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_batch_count
        )

    @adf_activity_batch_count.setter
    def adf_activity_batch_count(self, adf_activity_batch_count: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_batch_count = adf_activity_batch_count

    @property
    def adf_activity_is_sequential(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_is_sequential
        )

    @adf_activity_is_sequential.setter
    def adf_activity_is_sequential(self, adf_activity_is_sequential: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_is_sequential = adf_activity_is_sequential

    @property
    def adf_activity_sub_activities(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_sub_activities
        )

    @adf_activity_sub_activities.setter
    def adf_activity_sub_activities(
        self, adf_activity_sub_activities: Optional[Set[str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_sub_activities = adf_activity_sub_activities

    @property
    def adf_activity_reference_dataflow(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_activity_reference_dataflow
        )

    @adf_activity_reference_dataflow.setter
    def adf_activity_reference_dataflow(
        self, adf_activity_reference_dataflow: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activity_reference_dataflow = (
            adf_activity_reference_dataflow
        )

    @property
    def adf_pipeline_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_pipeline_qualified_name
        )

    @adf_pipeline_qualified_name.setter
    def adf_pipeline_qualified_name(self, adf_pipeline_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_pipeline_qualified_name = adf_pipeline_qualified_name

    @property
    def adf_linkedservices(self) -> Optional[List[AdfLinkedservice]]:
        return None if self.attributes is None else self.attributes.adf_linkedservices

    @adf_linkedservices.setter
    def adf_linkedservices(self, adf_linkedservices: Optional[List[AdfLinkedservice]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservices = adf_linkedservices

    @property
    def adf_datasets(self) -> Optional[List[AdfDataset]]:
        return None if self.attributes is None else self.attributes.adf_datasets

    @adf_datasets.setter
    def adf_datasets(self, adf_datasets: Optional[List[AdfDataset]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_datasets = adf_datasets

    @property
    def processes(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.processes

    @processes.setter
    def processes(self, processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.processes = processes

    @property
    def adf_pipeline(self) -> Optional[AdfPipeline]:
        return None if self.attributes is None else self.attributes.adf_pipeline

    @adf_pipeline.setter
    def adf_pipeline(self, adf_pipeline: Optional[AdfPipeline]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_pipeline = adf_pipeline

    @property
    def adf_dataflow(self) -> Optional[AdfDataflow]:
        return None if self.attributes is None else self.attributes.adf_dataflow

    @adf_dataflow.setter
    def adf_dataflow(self, adf_dataflow: Optional[AdfDataflow]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataflow = adf_dataflow

    class Attributes(ADF.Attributes):
        adf_activity_type: Optional[str] = Field(default=None, description="")
        adf_activity_preceding_dependency: Optional[Set[str]] = Field(
            default=None, description=""
        )
        adf_activity_policy_timeout: Optional[str] = Field(default=None, description="")
        adf_activity_polict_retry_interval: Optional[int] = Field(
            default=None, description=""
        )
        adf_activity_state: Optional[AdfActivityState] = Field(
            default=None, description=""
        )
        adf_activity_sources: Optional[Set[str]] = Field(default=None, description="")
        adf_activity_sinks: Optional[Set[str]] = Field(default=None, description="")
        adf_activity_source_type: Optional[str] = Field(default=None, description="")
        adf_activity_sink_type: Optional[str] = Field(default=None, description="")
        adf_activity_runs: Optional[List[Dict[str, str]]] = Field(
            default=None, description=""
        )
        adf_activity_notebook_path: Optional[str] = Field(default=None, description="")
        adf_activity_main_class_name: Optional[str] = Field(
            default=None, description=""
        )
        adf_activity_python_file_path: Optional[str] = Field(
            default=None, description=""
        )
        adf_activity_first_row_only: Optional[bool] = Field(
            default=None, description=""
        )
        adf_activity_batch_count: Optional[int] = Field(default=None, description="")
        adf_activity_is_sequential: Optional[bool] = Field(default=None, description="")
        adf_activity_sub_activities: Optional[Set[str]] = Field(
            default=None, description=""
        )
        adf_activity_reference_dataflow: Optional[str] = Field(
            default=None, description=""
        )
        adf_pipeline_qualified_name: Optional[str] = Field(default=None, description="")
        adf_linkedservices: Optional[List[AdfLinkedservice]] = Field(
            default=None, description=""
        )  # relationship
        adf_datasets: Optional[List[AdfDataset]] = Field(
            default=None, description=""
        )  # relationship
        processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship
        adf_pipeline: Optional[AdfPipeline] = Field(
            default=None, description=""
        )  # relationship
        adf_dataflow: Optional[AdfDataflow] = Field(
            default=None, description=""
        )  # relationship

    attributes: AdfActivity.Attributes = Field(
        default_factory=lambda: AdfActivity.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .adf_dataflow import AdfDataflow  # noqa: E402, F401
from .adf_dataset import AdfDataset  # noqa: E402, F401
from .adf_linkedservice import AdfLinkedservice  # noqa: E402, F401
from .adf_pipeline import AdfPipeline  # noqa: E402, F401
from .process import Process  # noqa: E402, F401
