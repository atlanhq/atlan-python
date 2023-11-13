# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

import uuid
from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.enums import AtlanConnectorType, GoogleDatastudioAssetType
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    KeywordTextField,
    KeywordTextStemmedField,
    NumericField,
)
from pyatlan.model.structs import GoogleLabel, GoogleTag
from pyatlan.utils import init_guid, validate_required_fields

from .asset45 import DataStudio


class DataStudioAsset(DataStudio):
    """Description"""

    @classmethod
    # @validate_arguments()
    @init_guid
    def create(
        cls,
        *,
        name: str,
        connection_qualified_name: str,
        data_studio_asset_type: GoogleDatastudioAssetType,
    ) -> DataStudioAsset:
        validate_required_fields(
            ["name", "connection_qualified_name", "data_studio_asset_type"],
            [name, connection_qualified_name, data_studio_asset_type],
        )
        attributes = DataStudioAsset.Attributes.create(
            name=name,
            connection_qualified_name=connection_qualified_name,
            data_studio_asset_type=data_studio_asset_type,
            gdsid=str(uuid.uuid4()),
        )
        return cls(attributes=attributes)

    type_name: str = Field("DataStudioAsset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "DataStudioAsset":
            raise ValueError("must be DataStudioAsset")
        return v

    def __setattr__(self, name, value):
        if name in DataStudioAsset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    DATA_STUDIO_ASSET_TYPE: ClassVar[KeywordField] = KeywordField(
        "dataStudioAssetType", "dataStudioAssetType"
    )
    """
    Type of the Google Data Studio asset, for example: REPORT or DATA_SOURCE.
    """
    DATA_STUDIO_ASSET_TITLE: ClassVar[
        KeywordTextStemmedField
    ] = KeywordTextStemmedField(
        "dataStudioAssetTitle",
        "dataStudioAssetTitle.keyword",
        "dataStudioAssetTitle",
        "dataStudioAssetTitle.stemmed",
    )
    """
    Title of the Google Data Studio asset.
    """
    DATA_STUDIO_ASSET_OWNER: ClassVar[KeywordField] = KeywordField(
        "dataStudioAssetOwner", "dataStudioAssetOwner"
    )
    """
    Owner of the asset, from Google Data Studio.
    """
    IS_TRASHED_DATA_STUDIO_ASSET: ClassVar[BooleanField] = BooleanField(
        "isTrashedDataStudioAsset", "isTrashedDataStudioAsset"
    )
    """
    Whether the Google Data Studio asset has been trashed (true) or not (false).
    """
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

    _convenience_properties: ClassVar[list[str]] = [
        "data_studio_asset_type",
        "data_studio_asset_title",
        "data_studio_asset_owner",
        "is_trashed_data_studio_asset",
        "google_service",
        "google_project_name",
        "google_project_id",
        "google_project_number",
        "google_location",
        "google_location_type",
        "google_labels",
        "google_tags",
    ]

    @property
    def data_studio_asset_type(self) -> Optional[GoogleDatastudioAssetType]:
        return (
            None if self.attributes is None else self.attributes.data_studio_asset_type
        )

    @data_studio_asset_type.setter
    def data_studio_asset_type(
        self, data_studio_asset_type: Optional[GoogleDatastudioAssetType]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_type = data_studio_asset_type

    @property
    def data_studio_asset_title(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.data_studio_asset_title
        )

    @data_studio_asset_title.setter
    def data_studio_asset_title(self, data_studio_asset_title: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_title = data_studio_asset_title

    @property
    def data_studio_asset_owner(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.data_studio_asset_owner
        )

    @data_studio_asset_owner.setter
    def data_studio_asset_owner(self, data_studio_asset_owner: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.data_studio_asset_owner = data_studio_asset_owner

    @property
    def is_trashed_data_studio_asset(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.is_trashed_data_studio_asset
        )

    @is_trashed_data_studio_asset.setter
    def is_trashed_data_studio_asset(
        self, is_trashed_data_studio_asset: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.is_trashed_data_studio_asset = is_trashed_data_studio_asset

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

    class Attributes(DataStudio.Attributes):
        data_studio_asset_type: Optional[GoogleDatastudioAssetType] = Field(
            None, description="", alias="dataStudioAssetType"
        )
        data_studio_asset_title: Optional[str] = Field(
            None, description="", alias="dataStudioAssetTitle"
        )
        data_studio_asset_owner: Optional[str] = Field(
            None, description="", alias="dataStudioAssetOwner"
        )
        is_trashed_data_studio_asset: Optional[bool] = Field(
            None, description="", alias="isTrashedDataStudioAsset"
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

        @classmethod
        # @validate_arguments()
        @init_guid
        def create(
            cls,
            *,
            name: str,
            connection_qualified_name: str,
            data_studio_asset_type: GoogleDatastudioAssetType,
            gdsid: str,
        ) -> DataStudioAsset.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name", "data_studio_asset_type"],
                [name, connection_qualified_name, data_studio_asset_type],
            )

            # Split the connection_qualified_name to extract necessary information
            fields = connection_qualified_name.split("/")
            if len(fields) != 3:
                raise ValueError("Invalid connection_qualified_name")

            try:
                connector_type = AtlanConnectorType(fields[1])  # type:ignore
            except ValueError as e:
                raise ValueError("Invalid connection_qualified_name") from e

            return DataStudioAsset.Attributes(
                name=name,
                gdsid=gdsid,
                qualified_name=f"{connection_qualified_name}/{gdsid}",
                connection_qualified_name=connection_qualified_name,
                connector_name=connector_type.value,
                data_studio_asset_type=data_studio_asset_type,
            )

    attributes: "DataStudioAsset.Attributes" = Field(
        default_factory=lambda: DataStudioAsset.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


DataStudioAsset.Attributes.update_forward_refs()
