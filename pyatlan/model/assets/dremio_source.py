# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .core.dremio import Dremio


class DremioSource(Dremio):
    """Description"""

    type_name: str = Field(default="DremioSource", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DremioSource":
            raise ValueError("must be DremioSource")
        return v

    def __setattr__(self, name, value):
        if name in DremioSource._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DREMIO_SOURCE_TYPE: ClassVar[KeywordField] = KeywordField(
        "dremioSourceType", "dremioSourceType"
    )
    """
    Type of external source.
    """
    DREMIO_SOURCE_CONNECTION_CONFIGS: ClassVar[KeywordField] = KeywordField(
        "dremioSourceConnectionConfigs", "dremioSourceConnectionConfigs"
    )
    """
    Configuration parameters for connecting to the external source.
    """
    DREMIO_SOURCE_ACCELERATION_SETTINGS: ClassVar[KeywordField] = KeywordField(
        "dremioSourceAccelerationSettings", "dremioSourceAccelerationSettings"
    )
    """
    Default acceleration settings for datasets in this source.
    """
    DREMIO_SOURCE_METADATA_POLICIES: ClassVar[KeywordField] = KeywordField(
        "dremioSourceMetadataPolicies", "dremioSourceMetadataPolicies"
    )
    """
    Metadata refresh and caching policies.
    """
    DREMIO_SOURCE_HEALTH_STATUS: ClassVar[KeywordField] = KeywordField(
        "dremioSourceHealthStatus", "dremioSourceHealthStatus"
    )
    """
    Current health status of the source connection.
    """
    DREMIO_SOURCE_HEALTH_STATUS_MESSAGE: ClassVar[KeywordField] = KeywordField(
        "dremioSourceHealthStatusMessage", "dremioSourceHealthStatusMessage"
    )
    """
    Current health status message of the source connection.
    """

    DREMIO_PHYSICAL_DATASETS: ClassVar[RelationField] = RelationField(
        "dremioPhysicalDatasets"
    )
    """
    TBC
    """
    DREMIO_FOLDERS: ClassVar[RelationField] = RelationField("dremioFolders")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "dremio_source_type",
        "dremio_source_connection_configs",
        "dremio_source_acceleration_settings",
        "dremio_source_metadata_policies",
        "dremio_source_health_status",
        "dremio_source_health_status_message",
        "dremio_physical_datasets",
        "dremio_folders",
    ]

    @property
    def dremio_source_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.dremio_source_type

    @dremio_source_type.setter
    def dremio_source_type(self, dremio_source_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_type = dremio_source_type

    @property
    def dremio_source_connection_configs(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_source_connection_configs
        )

    @dremio_source_connection_configs.setter
    def dremio_source_connection_configs(
        self, dremio_source_connection_configs: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_connection_configs = (
            dremio_source_connection_configs
        )

    @property
    def dremio_source_acceleration_settings(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_source_acceleration_settings
        )

    @dremio_source_acceleration_settings.setter
    def dremio_source_acceleration_settings(
        self, dremio_source_acceleration_settings: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_acceleration_settings = (
            dremio_source_acceleration_settings
        )

    @property
    def dremio_source_metadata_policies(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_source_metadata_policies
        )

    @dremio_source_metadata_policies.setter
    def dremio_source_metadata_policies(
        self, dremio_source_metadata_policies: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_metadata_policies = (
            dremio_source_metadata_policies
        )

    @property
    def dremio_source_health_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_source_health_status
        )

    @dremio_source_health_status.setter
    def dremio_source_health_status(self, dremio_source_health_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_health_status = dremio_source_health_status

    @property
    def dremio_source_health_status_message(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_source_health_status_message
        )

    @dremio_source_health_status_message.setter
    def dremio_source_health_status_message(
        self, dremio_source_health_status_message: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_source_health_status_message = (
            dremio_source_health_status_message
        )

    @property
    def dremio_physical_datasets(self) -> Optional[List[DremioPhysicalDataset]]:
        return (
            None
            if self.attributes is None
            else self.attributes.dremio_physical_datasets
        )

    @dremio_physical_datasets.setter
    def dremio_physical_datasets(
        self, dremio_physical_datasets: Optional[List[DremioPhysicalDataset]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_physical_datasets = dremio_physical_datasets

    @property
    def dremio_folders(self) -> Optional[List[DremioFolder]]:
        return None if self.attributes is None else self.attributes.dremio_folders

    @dremio_folders.setter
    def dremio_folders(self, dremio_folders: Optional[List[DremioFolder]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.dremio_folders = dremio_folders

    class Attributes(Dremio.Attributes):
        dremio_source_type: Optional[str] = Field(default=None, description="")
        dremio_source_connection_configs: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        dremio_source_acceleration_settings: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        dremio_source_metadata_policies: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        dremio_source_health_status: Optional[str] = Field(default=None, description="")
        dremio_source_health_status_message: Optional[str] = Field(
            default=None, description=""
        )
        dremio_physical_datasets: Optional[List[DremioPhysicalDataset]] = Field(
            default=None, description=""
        )  # relationship
        dremio_folders: Optional[List[DremioFolder]] = Field(
            default=None, description=""
        )  # relationship

    attributes: DremioSource.Attributes = Field(
        default_factory=lambda: DremioSource.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .dremio_folder import DremioFolder  # noqa: E402, F401
from .dremio_physical_dataset import DremioPhysicalDataset  # noqa: E402, F401

DremioSource.Attributes.update_forward_refs()
