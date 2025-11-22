# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import SageMakerUnifiedStudioProjectStatus
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .sage_maker_unified_studio import SageMakerUnifiedStudio


class SageMakerUnifiedStudioProject(SageMakerUnifiedStudio):
    """Description"""

    type_name: str = Field(
        default="SageMakerUnifiedStudioProject", allow_mutation=False
    )

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerUnifiedStudioProject":
            raise ValueError("must be SageMakerUnifiedStudioProject")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerUnifiedStudioProject._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SMUS_PROJECT_STATUS: ClassVar[KeywordField] = KeywordField(
        "smusProjectStatus", "smusProjectStatus"
    )
    """
    Status of the AWS SMUS Project
    """
    SMUS_PROJECT_PROFILE_NAME: ClassVar[KeywordField] = KeywordField(
        "smusProjectProfileName", "smusProjectProfileName"
    )
    """
    Project Profile Name of the AWS SMUS Project
    """
    SMUS_PROJECT_ROLE_ARN: ClassVar[KeywordField] = KeywordField(
        "smusProjectRoleArn", "smusProjectRoleArn"
    )
    """
    Amazon IAM Role ARN of the AWS SMUS Project
    """
    SMUS_PROJECT_S3LOCATION: ClassVar[KeywordField] = KeywordField(
        "smusProjectS3Location", "smusProjectS3Location"
    )
    """
    Amazon s3 location of the AWS SMUS Project
    """

    SMUS_PUBLISHED_ASSETS: ClassVar[RelationField] = RelationField(
        "smusPublishedAssets"
    )
    """
    TBC
    """
    SMUS_SUBSCRIBED_ASSETS: ClassVar[RelationField] = RelationField(
        "smusSubscribedAssets"
    )
    """
    TBC
    """
    SMUS_DATA_PRODUCTS: ClassVar[RelationField] = RelationField("smusDataProducts")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "smus_project_status",
        "smus_project_profile_name",
        "smus_project_role_arn",
        "smus_project_s3_location",
        "smus_published_assets",
        "smus_subscribed_assets",
        "smus_data_products",
    ]

    @property
    def smus_project_status(self) -> Optional[SageMakerUnifiedStudioProjectStatus]:
        return None if self.attributes is None else self.attributes.smus_project_status

    @smus_project_status.setter
    def smus_project_status(
        self, smus_project_status: Optional[SageMakerUnifiedStudioProjectStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_project_status = smus_project_status

    @property
    def smus_project_profile_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_project_profile_name
        )

    @smus_project_profile_name.setter
    def smus_project_profile_name(self, smus_project_profile_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_project_profile_name = smus_project_profile_name

    @property
    def smus_project_role_arn(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.smus_project_role_arn
        )

    @smus_project_role_arn.setter
    def smus_project_role_arn(self, smus_project_role_arn: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_project_role_arn = smus_project_role_arn

    @property
    def smus_project_s3_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_project_s3_location
        )

    @smus_project_s3_location.setter
    def smus_project_s3_location(self, smus_project_s3_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_project_s3_location = smus_project_s3_location

    @property
    def smus_published_assets(
        self,
    ) -> Optional[List[SageMakerUnifiedStudioPublishedAsset]]:
        return (
            None if self.attributes is None else self.attributes.smus_published_assets
        )

    @smus_published_assets.setter
    def smus_published_assets(
        self,
        smus_published_assets: Optional[List[SageMakerUnifiedStudioPublishedAsset]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_published_assets = smus_published_assets

    @property
    def smus_subscribed_assets(
        self,
    ) -> Optional[List[SageMakerUnifiedStudioSubscribedAsset]]:
        return (
            None if self.attributes is None else self.attributes.smus_subscribed_assets
        )

    @smus_subscribed_assets.setter
    def smus_subscribed_assets(
        self,
        smus_subscribed_assets: Optional[List[SageMakerUnifiedStudioSubscribedAsset]],
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_assets = smus_subscribed_assets

    @property
    def smus_data_products(self) -> Optional[List[DataProduct]]:
        return None if self.attributes is None else self.attributes.smus_data_products

    @smus_data_products.setter
    def smus_data_products(self, smus_data_products: Optional[List[DataProduct]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_data_products = smus_data_products

    class Attributes(SageMakerUnifiedStudio.Attributes):
        smus_project_status: Optional[SageMakerUnifiedStudioProjectStatus] = Field(
            default=None, description=""
        )
        smus_project_profile_name: Optional[str] = Field(default=None, description="")
        smus_project_role_arn: Optional[str] = Field(default=None, description="")
        smus_project_s3_location: Optional[str] = Field(default=None, description="")
        smus_published_assets: Optional[List[SageMakerUnifiedStudioPublishedAsset]] = (
            Field(default=None, description="")
        )  # relationship
        smus_subscribed_assets: Optional[
            List[SageMakerUnifiedStudioSubscribedAsset]
        ] = Field(default=None, description="")  # relationship
        smus_data_products: Optional[List[DataProduct]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerUnifiedStudioProject.Attributes = Field(
        default_factory=lambda: SageMakerUnifiedStudioProject.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .data_product import DataProduct  # noqa: E402, F401
from .sage_maker_unified_studio_published_asset import (
    SageMakerUnifiedStudioPublishedAsset,  # noqa: E402, F401
)
from .sage_maker_unified_studio_subscribed_asset import (
    SageMakerUnifiedStudioSubscribedAsset,  # noqa: E402, F401
)
