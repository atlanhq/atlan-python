# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)
from pyatlan.model.structs import GoogleLabel, GoogleTag

from .asset00 import AirflowTask, Process
from .asset27 import Google


class GCS(Google):
    """Description"""

    type_name: str = Field("GCS", allow_mutation=False)

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
    TBC
    """
    GCS_ENCRYPTION_TYPE: ClassVar[KeywordField] = KeywordField(
        "gcsEncryptionType", "gcsEncryptionType"
    )
    """
    TBC
    """
    GCS_E_TAG: ClassVar[KeywordField] = KeywordField("gcsETag", "gcsETag")
    """
    TBC
    """
    GCS_REQUESTER_PAYS: ClassVar[BooleanField] = BooleanField(
        "gcsRequesterPays", "gcsRequesterPays"
    )
    """
    TBC
    """
    GCS_ACCESS_CONTROL: ClassVar[KeywordField] = KeywordField(
        "gcsAccessControl", "gcsAccessControl"
    )
    """
    TBC
    """
    GCS_META_GENERATION_ID: ClassVar[NumericField] = NumericField(
        "gcsMetaGenerationId", "gcsMetaGenerationId"
    )
    """
    TBC
    """
    GOOGLE_SERVICE: ClassVar[KeywordField] = KeywordField(
        "googleService", "googleService"
    )
    """
    TBC
    """
    GOOGLE_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "googleProjectName", "googleProjectName", "googleProjectName.text"
    )
    """
    TBC
    """
    GOOGLE_PROJECT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "googleProjectId", "googleProjectId", "googleProjectId.text"
    )
    """
    TBC
    """
    GOOGLE_PROJECT_NUMBER: ClassVar[NumericField] = NumericField(
        "googleProjectNumber", "googleProjectNumber"
    )
    """
    TBC
    """
    GOOGLE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "googleLocation", "googleLocation"
    )
    """
    TBC
    """
    GOOGLE_LOCATION_TYPE: ClassVar[KeywordField] = KeywordField(
        "googleLocationType", "googleLocationType"
    )
    """
    TBC
    """
    GOOGLE_LABELS: ClassVar[KeywordField] = KeywordField("googleLabels", "googleLabels")
    """
    TBC
    """
    GOOGLE_TAGS: ClassVar[KeywordField] = KeywordField("googleTags", "googleTags")
    """
    TBC
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

    _convenience_properties: ClassVar[list[str]] = [
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
    def google_labels(self) -> Optional[list[GoogleLabel]]:
        return None if self.attributes is None else self.attributes.google_labels

    @google_labels.setter
    def google_labels(self, google_labels: Optional[list[GoogleLabel]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_labels = google_labels

    @property
    def google_tags(self) -> Optional[list[GoogleTag]]:
        return None if self.attributes is None else self.attributes.google_tags

    @google_tags.setter
    def google_tags(self, google_tags: Optional[list[GoogleTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.google_tags = google_tags

    @property
    def input_to_processes(self) -> Optional[list[Process]]:
        return None if self.attributes is None else self.attributes.input_to_processes

    @input_to_processes.setter
    def input_to_processes(self, input_to_processes: Optional[list[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_processes = input_to_processes

    @property
    def output_from_airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return (
            None
            if self.attributes is None
            else self.attributes.output_from_airflow_tasks
        )

    @output_from_airflow_tasks.setter
    def output_from_airflow_tasks(
        self, output_from_airflow_tasks: Optional[list[AirflowTask]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_airflow_tasks = output_from_airflow_tasks

    @property
    def input_to_airflow_tasks(self) -> Optional[list[AirflowTask]]:
        return (
            None if self.attributes is None else self.attributes.input_to_airflow_tasks
        )

    @input_to_airflow_tasks.setter
    def input_to_airflow_tasks(
        self, input_to_airflow_tasks: Optional[list[AirflowTask]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.input_to_airflow_tasks = input_to_airflow_tasks

    @property
    def output_from_processes(self) -> Optional[list[Process]]:
        return (
            None if self.attributes is None else self.attributes.output_from_processes
        )

    @output_from_processes.setter
    def output_from_processes(self, output_from_processes: Optional[list[Process]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.output_from_processes = output_from_processes

    class Attributes(Google.Attributes):
        gcs_storage_class: Optional[str] = Field(
            None, description="", alias="gcsStorageClass"
        )
        gcs_encryption_type: Optional[str] = Field(
            None, description="", alias="gcsEncryptionType"
        )
        gcs_e_tag: Optional[str] = Field(None, description="", alias="gcsETag")
        gcs_requester_pays: Optional[bool] = Field(
            None, description="", alias="gcsRequesterPays"
        )
        gcs_access_control: Optional[str] = Field(
            None, description="", alias="gcsAccessControl"
        )
        gcs_meta_generation_id: Optional[int] = Field(
            None, description="", alias="gcsMetaGenerationId"
        )
        google_service: Optional[str] = Field(
            None, description="", alias="googleService"
        )
        google_project_name: Optional[str] = Field(
            None, description="", alias="googleProjectName"
        )
        google_project_id: Optional[str] = Field(
            None, description="", alias="googleProjectId"
        )
        google_project_number: Optional[int] = Field(
            None, description="", alias="googleProjectNumber"
        )
        google_location: Optional[str] = Field(
            None, description="", alias="googleLocation"
        )
        google_location_type: Optional[str] = Field(
            None, description="", alias="googleLocationType"
        )
        google_labels: Optional[list[GoogleLabel]] = Field(
            None, description="", alias="googleLabels"
        )
        google_tags: Optional[list[GoogleTag]] = Field(
            None, description="", alias="googleTags"
        )
        input_to_processes: Optional[list[Process]] = Field(
            None, description="", alias="inputToProcesses"
        )  # relationship
        output_from_airflow_tasks: Optional[list[AirflowTask]] = Field(
            None, description="", alias="outputFromAirflowTasks"
        )  # relationship
        input_to_airflow_tasks: Optional[list[AirflowTask]] = Field(
            None, description="", alias="inputToAirflowTasks"
        )  # relationship
        output_from_processes: Optional[list[Process]] = Field(
            None, description="", alias="outputFromProcesses"
        )  # relationship

    attributes: "GCS.Attributes" = Field(
        default_factory=lambda: GCS.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


GCS.Attributes.update_forward_refs()
