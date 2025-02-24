# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField

from .a_d_f import ADF


class AdfDataset(ADF):
    """Description"""

    type_name: str = Field(default="AdfDataset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AdfDataset":
            raise ValueError("must be AdfDataset")
        return v

    def __setattr__(self, name, value):
        if name in AdfDataset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ADF_DATASET_TYPE: ClassVar[KeywordField] = KeywordField(
        "adfDatasetType", "adfDatasetType"
    )
    """
    Defines the type of the dataset.
    """
    ADF_DATASET_ANNOTATIONS: ClassVar[TextField] = TextField(
        "adfDatasetAnnotations", "adfDatasetAnnotations"
    )
    """
    The list of annotation assigned to a dataset.
    """
    ADF_DATASET_LINKED_SERVICE: ClassVar[KeywordField] = KeywordField(
        "adfDatasetLinkedService", "adfDatasetLinkedService"
    )
    """
    Defines the name of the linked service used to create this dataset.
    """
    ADF_DATASET_COLLECTION_NAME: ClassVar[TextField] = TextField(
        "adfDatasetCollectionName", "adfDatasetCollectionName"
    )
    """
    Defines the name collection in the cosmos dataset.
    """
    ADF_DATASET_STORAGE_TYPE: ClassVar[TextField] = TextField(
        "adfDatasetStorageType", "adfDatasetStorageType"
    )
    """
    Defines the storage type of storage file system dataset.
    """
    ADF_DATASET_FILE_NAME: ClassVar[TextField] = TextField(
        "adfDatasetFileName", "adfDatasetFileName"
    )
    """
    Defines the name of the file in the storage file system dataset.
    """
    ADF_DATASET_FILE_FOLDER_PATH: ClassVar[TextField] = TextField(
        "adfDatasetFileFolderPath", "adfDatasetFileFolderPath"
    )
    """
    Defines the folder path of the file in the storage file system dataset.
    """
    ADF_DATASET_CONTAINER_NAME: ClassVar[TextField] = TextField(
        "adfDatasetContainerName", "adfDatasetContainerName"
    )
    """
    Defines the container or bucket name in the storage file system dataset.
    """
    ADF_DATASET_SCHEMA_NAME: ClassVar[TextField] = TextField(
        "adfDatasetSchemaName", "adfDatasetSchemaName"
    )
    """
    Defines the name of the schema used in the snowflake, mssql, azure sql database type of dataset.
    """
    ADF_DATASET_TABLE_NAME: ClassVar[TextField] = TextField(
        "adfDatasetTableName", "adfDatasetTableName"
    )
    """
    Defines the name of the table used in the snowflake, mssql, azure sql database type of dataset.
    """
    ADF_DATASET_DATABASE_NAME: ClassVar[TextField] = TextField(
        "adfDatasetDatabaseName", "adfDatasetDatabaseName"
    )
    """
    Defines the name of the database used in the azure delta lake type of dataset.
    """

    ADF_LINKEDSERVICE: ClassVar[RelationField] = RelationField("adfLinkedservice")
    """
    TBC
    """
    ADF_ACTIVITIES: ClassVar[RelationField] = RelationField("adfActivities")
    """
    TBC
    """
    ADF_DATAFLOWS: ClassVar[RelationField] = RelationField("adfDataflows")
    """
    TBC
    """
    ADF_PIPELINES: ClassVar[RelationField] = RelationField("adfPipelines")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "adf_dataset_type",
        "adf_dataset_annotations",
        "adf_dataset_linked_service",
        "adf_dataset_collection_name",
        "adf_dataset_storage_type",
        "adf_dataset_file_name",
        "adf_dataset_file_folder_path",
        "adf_dataset_container_name",
        "adf_dataset_schema_name",
        "adf_dataset_table_name",
        "adf_dataset_database_name",
        "adf_linkedservice",
        "adf_activities",
        "adf_dataflows",
        "adf_pipelines",
    ]

    @property
    def adf_dataset_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.adf_dataset_type

    @adf_dataset_type.setter
    def adf_dataset_type(self, adf_dataset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_type = adf_dataset_type

    @property
    def adf_dataset_annotations(self) -> Optional[Set[str]]:
        return (
            None if self.attributes is None else self.attributes.adf_dataset_annotations
        )

    @adf_dataset_annotations.setter
    def adf_dataset_annotations(self, adf_dataset_annotations: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_annotations = adf_dataset_annotations

    @property
    def adf_dataset_linked_service(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_dataset_linked_service
        )

    @adf_dataset_linked_service.setter
    def adf_dataset_linked_service(self, adf_dataset_linked_service: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_linked_service = adf_dataset_linked_service

    @property
    def adf_dataset_collection_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_dataset_collection_name
        )

    @adf_dataset_collection_name.setter
    def adf_dataset_collection_name(self, adf_dataset_collection_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_collection_name = adf_dataset_collection_name

    @property
    def adf_dataset_storage_type(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_dataset_storage_type
        )

    @adf_dataset_storage_type.setter
    def adf_dataset_storage_type(self, adf_dataset_storage_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_storage_type = adf_dataset_storage_type

    @property
    def adf_dataset_file_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adf_dataset_file_name
        )

    @adf_dataset_file_name.setter
    def adf_dataset_file_name(self, adf_dataset_file_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_file_name = adf_dataset_file_name

    @property
    def adf_dataset_file_folder_path(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_dataset_file_folder_path
        )

    @adf_dataset_file_folder_path.setter
    def adf_dataset_file_folder_path(self, adf_dataset_file_folder_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_file_folder_path = adf_dataset_file_folder_path

    @property
    def adf_dataset_container_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_dataset_container_name
        )

    @adf_dataset_container_name.setter
    def adf_dataset_container_name(self, adf_dataset_container_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_container_name = adf_dataset_container_name

    @property
    def adf_dataset_schema_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adf_dataset_schema_name
        )

    @adf_dataset_schema_name.setter
    def adf_dataset_schema_name(self, adf_dataset_schema_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_schema_name = adf_dataset_schema_name

    @property
    def adf_dataset_table_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.adf_dataset_table_name
        )

    @adf_dataset_table_name.setter
    def adf_dataset_table_name(self, adf_dataset_table_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_table_name = adf_dataset_table_name

    @property
    def adf_dataset_database_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adf_dataset_database_name
        )

    @adf_dataset_database_name.setter
    def adf_dataset_database_name(self, adf_dataset_database_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataset_database_name = adf_dataset_database_name

    @property
    def adf_linkedservice(self) -> Optional[AdfLinkedservice]:
        return None if self.attributes is None else self.attributes.adf_linkedservice

    @adf_linkedservice.setter
    def adf_linkedservice(self, adf_linkedservice: Optional[AdfLinkedservice]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_linkedservice = adf_linkedservice

    @property
    def adf_activities(self) -> Optional[List[AdfActivity]]:
        return None if self.attributes is None else self.attributes.adf_activities

    @adf_activities.setter
    def adf_activities(self, adf_activities: Optional[List[AdfActivity]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_activities = adf_activities

    @property
    def adf_dataflows(self) -> Optional[List[AdfDataflow]]:
        return None if self.attributes is None else self.attributes.adf_dataflows

    @adf_dataflows.setter
    def adf_dataflows(self, adf_dataflows: Optional[List[AdfDataflow]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_dataflows = adf_dataflows

    @property
    def adf_pipelines(self) -> Optional[List[AdfPipeline]]:
        return None if self.attributes is None else self.attributes.adf_pipelines

    @adf_pipelines.setter
    def adf_pipelines(self, adf_pipelines: Optional[List[AdfPipeline]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adf_pipelines = adf_pipelines

    class Attributes(ADF.Attributes):
        adf_dataset_type: Optional[str] = Field(default=None, description="")
        adf_dataset_annotations: Optional[Set[str]] = Field(
            default=None, description=""
        )
        adf_dataset_linked_service: Optional[str] = Field(default=None, description="")
        adf_dataset_collection_name: Optional[str] = Field(default=None, description="")
        adf_dataset_storage_type: Optional[str] = Field(default=None, description="")
        adf_dataset_file_name: Optional[str] = Field(default=None, description="")
        adf_dataset_file_folder_path: Optional[str] = Field(
            default=None, description=""
        )
        adf_dataset_container_name: Optional[str] = Field(default=None, description="")
        adf_dataset_schema_name: Optional[str] = Field(default=None, description="")
        adf_dataset_table_name: Optional[str] = Field(default=None, description="")
        adf_dataset_database_name: Optional[str] = Field(default=None, description="")
        adf_linkedservice: Optional[AdfLinkedservice] = Field(
            default=None, description=""
        )  # relationship
        adf_activities: Optional[List[AdfActivity]] = Field(
            default=None, description=""
        )  # relationship
        adf_dataflows: Optional[List[AdfDataflow]] = Field(
            default=None, description=""
        )  # relationship
        adf_pipelines: Optional[List[AdfPipeline]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AdfDataset.Attributes = Field(
        default_factory=lambda: AdfDataset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .adf_activity import AdfActivity  # noqa
from .adf_dataflow import AdfDataflow  # noqa
from .adf_linkedservice import AdfLinkedservice  # noqa
from .adf_pipeline import AdfPipeline  # noqa
