# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .sage_maker_unified_studio_asset import SageMakerUnifiedStudioAsset


class SageMakerUnifiedStudioSubscribedAsset(SageMakerUnifiedStudioAsset):
    """Description"""

    type_name: str = Field(
        default="SageMakerUnifiedStudioSubscribedAsset", allow_mutation=False
    )

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerUnifiedStudioSubscribedAsset":
            raise ValueError("must be SageMakerUnifiedStudioSubscribedAsset")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerUnifiedStudioSubscribedAsset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SMUS_SUBSCRIBED_ASSET_PROJECT_NAME: ClassVar[KeywordField] = KeywordField(
        "smusSubscribedAssetProjectName", "smusSubscribedAssetProjectName"
    )
    """
    Name of the AWS SMUS Project from which this asset is subscribed
    """
    SMUS_SUBSCRIBED_ASSET_REQUESTOR_NAME: ClassVar[KeywordField] = KeywordField(
        "smusSubscribedAssetRequestorName", "smusSubscribedAssetRequestorName"
    )
    """
    Name of the user who requested access to this subscribed asset
    """
    SMUS_SUBSCRIBED_ASSET_REQUEST_REASON: ClassVar[KeywordField] = KeywordField(
        "smusSubscribedAssetRequestReason", "smusSubscribedAssetRequestReason"
    )
    """
    Reason provided by the requestor for this subscribed asset
    """
    SMUS_SUBSCRIBED_ASSET_REQUEST_DATE: ClassVar[NumericField] = NumericField(
        "smusSubscribedAssetRequestDate", "smusSubscribedAssetRequestDate"
    )
    """
    Date when the subscription request was submitted
    """
    SMUS_SUBSCRIBED_ASSET_APPROVER_NAME: ClassVar[KeywordField] = KeywordField(
        "smusSubscribedAssetApproverName", "smusSubscribedAssetApproverName"
    )
    """
    Name of the user who approved the subscription request
    """
    SMUS_SUBSCRIBED_ASSET_APPROVED_REASON: ClassVar[KeywordField] = KeywordField(
        "smusSubscribedAssetApprovedReason", "smusSubscribedAssetApprovedReason"
    )
    """
    Reason provided by the approver for approving the subscription
    """
    SMUS_SUBSCRIBED_ASSET_APPROVAL_DATE: ClassVar[NumericField] = NumericField(
        "smusSubscribedAssetApprovalDate", "smusSubscribedAssetApprovalDate"
    )
    """
    Date when the subscription request was approved
    """
    SMUS_SUBSCRIBED_ASSET_COLUMN_ACCESS_INFO: ClassVar[KeywordField] = KeywordField(
        "smusSubscribedAssetColumnAccessInfo", "smusSubscribedAssetColumnAccessInfo"
    )
    """
    Number of Columns provided access grant for this subscribed asset. Example : 3 out of 23
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

    SMUS_PUBLISHED_ASSETS: ClassVar[RelationField] = RelationField(
        "smusPublishedAssets"
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
        "smus_subscribed_asset_project_name",
        "smus_subscribed_asset_requestor_name",
        "smus_subscribed_asset_request_reason",
        "smus_subscribed_asset_request_date",
        "smus_subscribed_asset_approver_name",
        "smus_subscribed_asset_approved_reason",
        "smus_subscribed_asset_approval_date",
        "smus_subscribed_asset_column_access_info",
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
        "smus_published_assets",
        "smus_project",
        "smus_asset_schemas",
    ]

    @property
    def smus_subscribed_asset_project_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_subscribed_asset_project_name
        )

    @smus_subscribed_asset_project_name.setter
    def smus_subscribed_asset_project_name(
        self, smus_subscribed_asset_project_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset_project_name = (
            smus_subscribed_asset_project_name
        )

    @property
    def smus_subscribed_asset_requestor_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_subscribed_asset_requestor_name
        )

    @smus_subscribed_asset_requestor_name.setter
    def smus_subscribed_asset_requestor_name(
        self, smus_subscribed_asset_requestor_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset_requestor_name = (
            smus_subscribed_asset_requestor_name
        )

    @property
    def smus_subscribed_asset_request_reason(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_subscribed_asset_request_reason
        )

    @smus_subscribed_asset_request_reason.setter
    def smus_subscribed_asset_request_reason(
        self, smus_subscribed_asset_request_reason: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset_request_reason = (
            smus_subscribed_asset_request_reason
        )

    @property
    def smus_subscribed_asset_request_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_subscribed_asset_request_date
        )

    @smus_subscribed_asset_request_date.setter
    def smus_subscribed_asset_request_date(
        self, smus_subscribed_asset_request_date: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset_request_date = (
            smus_subscribed_asset_request_date
        )

    @property
    def smus_subscribed_asset_approver_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_subscribed_asset_approver_name
        )

    @smus_subscribed_asset_approver_name.setter
    def smus_subscribed_asset_approver_name(
        self, smus_subscribed_asset_approver_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset_approver_name = (
            smus_subscribed_asset_approver_name
        )

    @property
    def smus_subscribed_asset_approved_reason(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_subscribed_asset_approved_reason
        )

    @smus_subscribed_asset_approved_reason.setter
    def smus_subscribed_asset_approved_reason(
        self, smus_subscribed_asset_approved_reason: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset_approved_reason = (
            smus_subscribed_asset_approved_reason
        )

    @property
    def smus_subscribed_asset_approval_date(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_subscribed_asset_approval_date
        )

    @smus_subscribed_asset_approval_date.setter
    def smus_subscribed_asset_approval_date(
        self, smus_subscribed_asset_approval_date: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset_approval_date = (
            smus_subscribed_asset_approval_date
        )

    @property
    def smus_subscribed_asset_column_access_info(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_subscribed_asset_column_access_info
        )

    @smus_subscribed_asset_column_access_info.setter
    def smus_subscribed_asset_column_access_info(
        self, smus_subscribed_asset_column_access_info: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset_column_access_info = (
            smus_subscribed_asset_column_access_info
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
        smus_subscribed_asset_project_name: Optional[str] = Field(
            default=None, description=""
        )
        smus_subscribed_asset_requestor_name: Optional[str] = Field(
            default=None, description=""
        )
        smus_subscribed_asset_request_reason: Optional[str] = Field(
            default=None, description=""
        )
        smus_subscribed_asset_request_date: Optional[datetime] = Field(
            default=None, description=""
        )
        smus_subscribed_asset_approver_name: Optional[str] = Field(
            default=None, description=""
        )
        smus_subscribed_asset_approved_reason: Optional[str] = Field(
            default=None, description=""
        )
        smus_subscribed_asset_approval_date: Optional[datetime] = Field(
            default=None, description=""
        )
        smus_subscribed_asset_column_access_info: Optional[str] = Field(
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
        smus_published_assets: Optional[List[SageMakerUnifiedStudioPublishedAsset]] = (
            Field(default=None, description="")
        )  # relationship
        smus_project: Optional[SageMakerUnifiedStudioProject] = Field(
            default=None, description=""
        )  # relationship
        smus_asset_schemas: Optional[List[SageMakerUnifiedStudioAssetSchema]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerUnifiedStudioSubscribedAsset.Attributes = Field(
        default_factory=lambda: SageMakerUnifiedStudioSubscribedAsset.Attributes(),
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
from .sage_maker_unified_studio_published_asset import (
    SageMakerUnifiedStudioPublishedAsset,  # noqa: E402, F401
)
