# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)
from pyatlan.model.structs import AzureTag

from .azure import Azure


class ADLS(Azure):
    """Description"""

    type_name: str = Field(default="ADLS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "ADLS":
            raise ValueError("must be ADLS")
        return v

    def __setattr__(self, name, value):
        if name in ADLS._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADLS_ACCOUNT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsAccountQualifiedName",
        "adlsAccountQualifiedName",
        "adlsAccountQualifiedName.text",
    )
    """
    Unique name of the account for this ADLS asset.
    """
    ADLS_ACCOUNT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "adlsAccountName", "adlsAccountName.keyword", "adlsAccountName"
    )
    """
    Name of the account for this ADLS asset.
    """
    AZURE_RESOURCE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "azureResourceId", "azureResourceId", "azureResourceId.text"
    )
    """
    Resource identifier of this asset in Azure.
    """
    AZURE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "azureLocation", "azureLocation"
    )
    """
    Location of this asset in Azure.
    """
    ADLS_ACCOUNT_SECONDARY_LOCATION: ClassVar[KeywordField] = KeywordField(
        "adlsAccountSecondaryLocation", "adlsAccountSecondaryLocation"
    )
    """
    Secondary location of the ADLS account.
    """
    AZURE_TAGS: ClassVar[KeywordField] = KeywordField("azureTags", "azureTags")
    """
    Tags that have been applied to this asset in Azure.
    """

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
        "adls_account_qualified_name",
        "adls_account_name",
        "azure_resource_id",
        "azure_location",
        "adls_account_secondary_location",
        "azure_tags",
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
    def adls_account_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_qualified_name
        )

    @adls_account_qualified_name.setter
    def adls_account_qualified_name(self, adls_account_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_qualified_name = adls_account_qualified_name

    @property
    def adls_account_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adls_account_name

    @adls_account_name.setter
    def adls_account_name(self, adls_account_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_name = adls_account_name

    @property
    def azure_resource_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_resource_id

    @azure_resource_id.setter
    def azure_resource_id(self, azure_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_resource_id = azure_resource_id

    @property
    def azure_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_location

    @azure_location.setter
    def azure_location(self, azure_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_location = azure_location

    @property
    def adls_account_secondary_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_secondary_location
        )

    @adls_account_secondary_location.setter
    def adls_account_secondary_location(
        self, adls_account_secondary_location: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_secondary_location = (
            adls_account_secondary_location
        )

    @property
    def azure_tags(self) -> Optional[List[AzureTag]]:
        return None if self.attributes is None else self.attributes.azure_tags

    @azure_tags.setter
    def azure_tags(self, azure_tags: Optional[List[AzureTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_tags = azure_tags

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

    class Attributes(Azure.Attributes):
        adls_account_qualified_name: Optional[str] = Field(default=None, description="")
        adls_account_name: Optional[str] = Field(default=None, description="")
        azure_resource_id: Optional[str] = Field(default=None, description="")
        azure_location: Optional[str] = Field(default=None, description="")
        adls_account_secondary_location: Optional[str] = Field(
            default=None, description=""
        )
        azure_tags: Optional[List[AzureTag]] = Field(default=None, description="")
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

    attributes: ADLS.Attributes = Field(
        default_factory=lambda: ADLS.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .core.airflow_task import AirflowTask  # noqa: E402, F401
from .core.model_attribute import ModelAttribute  # noqa: E402, F401
from .core.model_entity import ModelEntity  # noqa: E402, F401
from .core.process import Process  # noqa: E402, F401
from .core.spark_job import SparkJob  # noqa: E402, F401

ADLS.Attributes.update_forward_refs()
