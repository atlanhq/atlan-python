# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .sage_maker_unified_studio_asset import SageMakerUnifiedStudioAsset


class SageMakerUnifiedStudioPublishedAsset(SageMakerUnifiedStudioAsset):
    """Description"""

    type_name: str = Field(
        default="SageMakerUnifiedStudioPublishedAsset", allow_mutation=False
    )

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerUnifiedStudioPublishedAsset":
            raise ValueError("must be SageMakerUnifiedStudioPublishedAsset")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerUnifiedStudioPublishedAsset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SMUS_PUBLISHED_ASSET_SUBSCRIPTIONS_COUNT: ClassVar[NumericField] = NumericField(
        "smusPublishedAssetSubscriptionsCount", "smusPublishedAssetSubscriptionsCount"
    )
    """
    The count of subscriptions for a Published Asset in AWS SMUS
    """
    SMUS_ASSET_SUMMARY: ClassVar[KeywordField] = KeywordField(
        "smusAssetSummary", "smusAssetSummary"
    )
    """
    The summary text for a Published Asset in AWS SMUS
    """
    SMUS_ASSET_TECHNICAL_NAME: ClassVar[KeywordField] = KeywordField(
        "smusAssetTechnicalName", "smusAssetTechnicalName"
    )
    """
    The technical name for a Published Asset in AWS SMUS
    """
    SMUS_ASSET_TYPE: ClassVar[KeywordField] = KeywordField(
        "smusAssetType", "smusAssetType"
    )
    """
    The Asset Type for a Published Asset in AWS SMUS
    """
    SMUS_ASSET_REVISION: ClassVar[KeywordField] = KeywordField(
        "smusAssetRevision", "smusAssetRevision"
    )
    """
    The latest published version for a Published Asset in AWS SMUS
    """
    SMUS_ASSET_SOURCE_IDENTIFIER: ClassVar[KeywordField] = KeywordField(
        "smusAssetSourceIdentifier", "smusAssetSourceIdentifier"
    )
    """
    The asset source Identifier for a Published Asset in AWS SMUS
    """
    SMUS_DOMAIN_NAME: ClassVar[KeywordField] = KeywordField(
        "smusDomainName", "smusDomainName"
    )
    """
    AWS SMUS Domain Name
    """
    SMUS_DOMAIN_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "smusDomainId", "smusDomainId.keyword", "smusDomainId"
    )
    """
    AWS SMUS Domain ID
    """
    SMUS_DOMAIN_UNIT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "smusDomainUnitName", "smusDomainUnitName.keyword", "smusDomainUnitName"
    )
    """
    AWS SMUS Domain Unit Name
    """
    SMUS_DOMAIN_UNIT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "smusDomainUnitId", "smusDomainUnitId.keyword", "smusDomainUnitId"
    )
    """
    AWS SMUS Domain Unit ID
    """
    SMUS_PROJECT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "smusProjectId", "smusProjectId.keyword", "smusProjectId"
    )
    """
    Unique ID of the AWS SMUS Project
    """
    SMUS_OWNING_PROJECT_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "smusOwningProjectId", "smusOwningProjectId.keyword", "smusOwningProjectId"
    )
    """
    Unique ID of the AWS SMUS Project which owns an Asset
    """

    SMUS_SUBSCRIBED_ASSETS: ClassVar[RelationField] = RelationField(
        "smusSubscribedAssets"
    )
    """
    TBC
    """
    SMUS_PROJECT: ClassVar[RelationField] = RelationField("smusProject")
    """
    TBC
    """
    SMUS_ASSET_SCHEMAS: ClassVar[RelationField] = RelationField("smusAssetSchemas")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "smus_published_asset_subscriptions_count",
        "smus_asset_summary",
        "smus_asset_technical_name",
        "smus_asset_type",
        "smus_asset_revision",
        "smus_asset_source_identifier",
        "smus_domain_name",
        "smus_domain_id",
        "smus_domain_unit_name",
        "smus_domain_unit_id",
        "smus_project_id",
        "smus_owning_project_id",
        "smus_subscribed_assets",
        "smus_project",
        "smus_asset_schemas",
    ]

    @property
    def smus_published_asset_subscriptions_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_published_asset_subscriptions_count
        )

    @smus_published_asset_subscriptions_count.setter
    def smus_published_asset_subscriptions_count(
        self, smus_published_asset_subscriptions_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_published_asset_subscriptions_count = (
            smus_published_asset_subscriptions_count
        )

    @property
    def smus_asset_summary(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_asset_summary

    @smus_asset_summary.setter
    def smus_asset_summary(self, smus_asset_summary: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_summary = smus_asset_summary

    @property
    def smus_asset_technical_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_asset_technical_name
        )

    @smus_asset_technical_name.setter
    def smus_asset_technical_name(self, smus_asset_technical_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_technical_name = smus_asset_technical_name

    @property
    def smus_asset_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_asset_type

    @smus_asset_type.setter
    def smus_asset_type(self, smus_asset_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_type = smus_asset_type

    @property
    def smus_asset_revision(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_asset_revision

    @smus_asset_revision.setter
    def smus_asset_revision(self, smus_asset_revision: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_revision = smus_asset_revision

    @property
    def smus_asset_source_identifier(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_asset_source_identifier
        )

    @smus_asset_source_identifier.setter
    def smus_asset_source_identifier(self, smus_asset_source_identifier: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_source_identifier = smus_asset_source_identifier

    @property
    def smus_domain_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_domain_name

    @smus_domain_name.setter
    def smus_domain_name(self, smus_domain_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_domain_name = smus_domain_name

    @property
    def smus_domain_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_domain_id

    @smus_domain_id.setter
    def smus_domain_id(self, smus_domain_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_domain_id = smus_domain_id

    @property
    def smus_domain_unit_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.smus_domain_unit_name
        )

    @smus_domain_unit_name.setter
    def smus_domain_unit_name(self, smus_domain_unit_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_domain_unit_name = smus_domain_unit_name

    @property
    def smus_domain_unit_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_domain_unit_id

    @smus_domain_unit_id.setter
    def smus_domain_unit_id(self, smus_domain_unit_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_domain_unit_id = smus_domain_unit_id

    @property
    def smus_project_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_project_id

    @smus_project_id.setter
    def smus_project_id(self, smus_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_project_id = smus_project_id

    @property
    def smus_owning_project_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.smus_owning_project_id
        )

    @smus_owning_project_id.setter
    def smus_owning_project_id(self, smus_owning_project_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_owning_project_id = smus_owning_project_id

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
    def smus_project(self) -> Optional[SageMakerUnifiedStudioProject]:
        return None if self.attributes is None else self.attributes.smus_project

    @smus_project.setter
    def smus_project(self, smus_project: Optional[SageMakerUnifiedStudioProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_project = smus_project

    @property
    def smus_asset_schemas(self) -> Optional[List[SageMakerUnifiedStudioAssetSchema]]:
        return None if self.attributes is None else self.attributes.smus_asset_schemas

    @smus_asset_schemas.setter
    def smus_asset_schemas(
        self, smus_asset_schemas: Optional[List[SageMakerUnifiedStudioAssetSchema]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_schemas = smus_asset_schemas

    class Attributes(SageMakerUnifiedStudioAsset.Attributes):
        smus_published_asset_subscriptions_count: Optional[int] = Field(
            default=None, description=""
        )
        smus_asset_summary: Optional[str] = Field(default=None, description="")
        smus_asset_technical_name: Optional[str] = Field(default=None, description="")
        smus_asset_type: Optional[str] = Field(default=None, description="")
        smus_asset_revision: Optional[str] = Field(default=None, description="")
        smus_asset_source_identifier: Optional[str] = Field(
            default=None, description=""
        )
        smus_domain_name: Optional[str] = Field(default=None, description="")
        smus_domain_id: Optional[str] = Field(default=None, description="")
        smus_domain_unit_name: Optional[str] = Field(default=None, description="")
        smus_domain_unit_id: Optional[str] = Field(default=None, description="")
        smus_project_id: Optional[str] = Field(default=None, description="")
        smus_owning_project_id: Optional[str] = Field(default=None, description="")
        smus_subscribed_assets: Optional[
            List[SageMakerUnifiedStudioSubscribedAsset]
        ] = Field(default=None, description="")  # relationship
        smus_project: Optional[SageMakerUnifiedStudioProject] = Field(
            default=None, description=""
        )  # relationship
        smus_asset_schemas: Optional[List[SageMakerUnifiedStudioAssetSchema]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerUnifiedStudioPublishedAsset.Attributes = Field(
        default_factory=lambda: SageMakerUnifiedStudioPublishedAsset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sage_maker_unified_studio_asset_schema import (
    SageMakerUnifiedStudioAssetSchema,  # noqa: E402, F401
)
from .sage_maker_unified_studio_project import (
    SageMakerUnifiedStudioProject,  # noqa: E402, F401
)
from .sage_maker_unified_studio_subscribed_asset import (
    SageMakerUnifiedStudioSubscribedAsset,  # noqa: E402, F401
)
