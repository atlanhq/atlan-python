# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.model.structs import GoogleLabel, GoogleTag

from .google import Google


class GCS(Google):
    """Description"""

    type_name: str = Field(default="GCS", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "GCS":
            raise ValueError("must be GCS")
        return v

    def __setattr__(self, name, value):
        if name in GCS._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    GCS_STORAGE_CLASS: ClassVar[KeywordField] = KeywordField(
        "gcsStorageClass", "gcsStorageClass"
    )
    """
    Storage class of this asset.
    """
    GCS_ENCRYPTION_TYPE: ClassVar[KeywordField] = KeywordField(
        "gcsEncryptionType", "gcsEncryptionType"
    )
    """
    Encryption algorithm used to encrypt this asset.
    """
    GCS_E_TAG: ClassVar[KeywordField] = KeywordField("gcsETag", "gcsETag")
    """
    Entity tag for the asset. An entity tag is a hash of the object and represents changes to the contents of an object only, not its metadata.
    """  # noqa: E501
    GCS_REQUESTER_PAYS: ClassVar[BooleanField] = BooleanField(
        "gcsRequesterPays", "gcsRequesterPays"
    )
    """
    Whether the requester pays header was sent when this asset was created (true) or not (false).
    """
    GCS_ACCESS_CONTROL: ClassVar[KeywordField] = KeywordField(
        "gcsAccessControl", "gcsAccessControl"
    )
    """
    Access control list for this asset.
    """
    GCS_META_GENERATION_ID: ClassVar[NumericField] = NumericField(
        "gcsMetaGenerationId", "gcsMetaGenerationId"
    )
    """
    Version of metadata for this asset at this generation. Used for preconditions and detecting changes in metadata. A metageneration number is only meaningful in the context of a particular generation of a particular asset.
    """  # noqa: E501
    GOOGLE_SERVICE: ClassVar[KeywordField] = KeywordField(
        "googleService", "googleService"
    )
    """
    Service in Google in which the asset exists.
    """
    GOOGLE_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "googleProjectName", "googleProjectName", "googleProjectName.text"
    )
    """
    Name of the project in which the asset exists.
    """
    GOOGLE_PROJECT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "googleProjectId", "googleProjectId", "googleProjectId.text"
    )
    """
    ID of the project in which the asset exists.
    """
    GOOGLE_PROJECT_NUMBER: ClassVar[NumericField] = NumericField(
        "googleProjectNumber", "googleProjectNumber"
    )
    """
    Number of the project in which the asset exists.
    """
    GOOGLE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "googleLocation", "googleLocation"
    )
    """
    Location of this asset in Google.
    """
    GOOGLE_LOCATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "googleLocationType", "googleLocationType"
    )
    """
    Type of location of this asset in Google.
    """
    GOOGLE_LABELS: ClassVar[KeywordField] = KeywordField("googleLabels", "googleLabels")
    """
    List of labels that have been applied to the asset in Google.
    """
    GOOGLE_TAGS: ClassVar[KeywordField] = KeywordField("googleTags", "googleTags")
    """
    List of tags that have been applied to the asset in Google.
    """

    INPUT_TO_PROCESSES: ClassVar[RelationField] = RelationField("inputToProcesses")
    """
    TBC
    """
    OUTPUT_FROM_AIRFLOW_TASKS: ClassVar[RelationField] = RelationField(
        "outputFromAirflowTasks"
    )
    """
    TBC
    """
    INPUT_TO_SPARK_JOBS: ClassVar[RelationField] = RelationField("inputToSparkJobs")
    """
    TBC
    """
    OUTPUT_FROM_SPARK_JOBS: ClassVar[RelationField] = RelationField(
        "outputFromSparkJobs"
    )
    """
    TBC
    """
    INPUT_TO_AIRFLOW_TASKS: ClassVar[RelationField] = RelationField(
        "inputToAirflowTasks"
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
        "gcs_storage_class",
        "gcs_encryption_type",
        "gcs_e_tag",
        "gcs_requester_pays",
        "gcs_access_control",
        "gcs_meta_generation_id",
        "google_service",
        "google_project_name",
        "google_project_id",
        "google_project_number",
        "google_location",
        "google_location_type",
        "google_labels",
        "google_tags",
        "input_to_processes",
        "output_from_airflow_tasks",
        "input_to_spark_jobs",
        "output_from_spark_jobs",
        "input_to_airflow_tasks",
        "output_from_processes",
    ]

    @property
    def gcs_storage_class(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_storage_class

    @gcs_storage_class.setter
    def gcs_storage_class(self, gcs_storage_class: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_storage_class = gcs_storage_class

    @property
    def gcs_encryption_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_encryption_type

    @gcs_encryption_type.setter
    def gcs_encryption_type(self, gcs_encryption_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_encryption_type = gcs_encryption_type

    @property
    def gcs_e_tag(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_e_tag

    @gcs_e_tag.setter
    def gcs_e_tag(self, gcs_e_tag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_e_tag = gcs_e_tag

    @property
    def gcs_requester_pays(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.gcs_requester_pays

    @gcs_requester_pays.setter
    def gcs_requester_pays(self, gcs_requester_pays: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_requester_pays = gcs_requester_pays

    @property
    def gcs_access_control(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.gcs_access_control

    @gcs_access_control.setter
    def gcs_access_control(self, gcs_access_control: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_access_control = gcs_access_control

    @property
    def gcs_meta_generation_id(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.gcs_meta_generation_id
        )

    @gcs_meta_generation_id.setter
    def gcs_meta_generation_id(self, gcs_meta_generation_id: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.gcs_meta_generation_id = gcs_meta_generation_id

    @property
    def google_service(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_service

    @google_service.setter
    def google_service(self, google_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_service = google_service

    @property
    def google_project_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_name

    @google_project_name.setter
    def google_project_name(self, google_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_name = google_project_name

    @property
    def google_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_project_id

    @google_project_id.setter
    def google_project_id(self, google_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_id = google_project_id

    @property
    def google_project_number(self) -> Optional[int]:
        return (
            None if self.attributes is None else self.attributes.google_project_number
        )

    @google_project_number.setter
    def google_project_number(self, google_project_number: Optional[int]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_project_number = google_project_number

    @property
    def google_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location

    @google_location.setter
    def google_location(self, google_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location = google_location

    @property
    def google_location_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.google_location_type

    @google_location_type.setter
    def google_location_type(self, google_location_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_location_type = google_location_type

    @property
    def google_labels(self) -> Optional[List[GoogleLabel]]:
        return None if self.attributes is None else self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[List[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[List[GoogleTag]]:
        return None if self.attributes is None else self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[List[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

    @property
    def input_to_processes(self) -> Optional[List[Process]]:
        return None if self.attributes is None else self.attributes.input_to_processes

    @input_to_processes.setter
    def input_to_processes(self, input_to_processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_processes = input_to_processes

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
    def input_to_spark_jobs(self) -> Optional[List[SparkJob]]:
        return None if self.attributes is None else self.attributes.input_to_spark_jobs

    @input_to_spark_jobs.setter
    def input_to_spark_jobs(self, input_to_spark_jobs: Optional[List[SparkJob]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_spark_jobs = input_to_spark_jobs

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
    def output_from_processes(self) -> Optional[List[Process]]:
        return (
            None if self.attributes is None else self.attributes.output_from_processes
        )

    @output_from_processes.setter
    def output_from_processes(self, output_from_processes: Optional[List[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_processes = output_from_processes

    class Attributes(Google.Attributes):
        gcs_storage_class: Optional[str] = Field(default=None, description="")
        gcs_encryption_type: Optional[str] = Field(default=None, description="")
        gcs_e_tag: Optional[str] = Field(default=None, description="")
        gcs_requester_pays: Optional[bool] = Field(default=None, description="")
        gcs_access_control: Optional[str] = Field(default=None, description="")
        gcs_meta_generation_id: Optional[int] = Field(default=None, description="")
        google_service: Optional[str] = Field(default=None, description="")
        google_project_name: Optional[str] = Field(default=None, description="")
        google_project_id: Optional[str] = Field(default=None, description="")
        google_project_number: Optional[int] = Field(default=None, description="")
        google_location: Optional[str] = Field(default=None, description="")
        google_location_type: Optional[str] = Field(default=None, description="")
        google_labels: Optional[List[GoogleLabel]] = Field(default=None, description="")
        google_tags: Optional[List[GoogleTag]] = Field(default=None, description="")
        input_to_processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship
        output_from_airflow_tasks: Optional[List[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        input_to_spark_jobs: Optional[List[SparkJob]] = Field(
            default=None, description=""
        )  # relationship
        output_from_spark_jobs: Optional[List[SparkJob]] = Field(
            default=None, description=""
        )  # relationship
        input_to_airflow_tasks: Optional[List[AirflowTask]] = Field(
            default=None, description=""
        )  # relationship
        output_from_processes: Optional[List[Process]] = Field(
            default=None, description=""
        )  # relationship

    attributes: GCS.Attributes = Field(
        default_factory=lambda: GCS.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .airflow_task import AirflowTask  # noqa
from .process import Process  # noqa
from .spark_job import SparkJob  # noqa
