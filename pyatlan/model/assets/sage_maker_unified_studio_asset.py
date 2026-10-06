# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

from .sage_maker_unified_studio import SageMakerUnifiedStudio


class SageMakerUnifiedStudioAsset(SageMakerUnifiedStudio):
    """Description"""

    type_name: str = Field(default="SageMakerUnifiedStudioAsset", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerUnifiedStudioAsset":
            raise ValueError("must be SageMakerUnifiedStudioAsset")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerUnifiedStudioAsset._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SMUS_ASSET_SUMMARY: ClassVar[KeywordField] = KeywordField(
        "smusAssetSummary", "smusAssetSummary"
    )
    """
    Summary text for the asset in SageMaker Unified Studio.
    """
    SMUS_ASSET_TECHNICAL_NAME: ClassVar[KeywordField] = KeywordField(
        "smusAssetTechnicalName", "smusAssetTechnicalName"
    )
    """
    Technical name for the asset in SageMaker Unified Studio.
    """
    SMUS_ASSET_TYPE: ClassVar[KeywordField] = KeywordField(
        "smusAssetType", "smusAssetType"
    )
    """
    Type of asset in SageMaker Unified Studio.
    """
    SMUS_ASSET_REVISION: ClassVar[KeywordField] = KeywordField(
        "smusAssetRevision", "smusAssetRevision"
    )
    """
    Latest published version of the asset in SageMaker Unified Studio.
    """
    SMUS_ASSET_SOURCE_IDENTIFIER: ClassVar[KeywordField] = KeywordField(
        "smusAssetSourceIdentifier", "smusAssetSourceIdentifier"
    )
    """
    Unique source identifier for the asset in SageMaker Unified Studio.
    """

    SMUS_ASSET_SCHEMAS: ClassVar[RelationField] = RelationField("smusAssetSchemas")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "smus_asset_summary",
        "smus_asset_technical_name",
        "smus_asset_type",
        "smus_asset_revision",
        "smus_asset_source_identifier",
        "smus_asset_schemas",
    ]

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
    def smus_asset_schemas(self) -> Optional[List[SageMakerUnifiedStudioAssetSchema]]:
        return None if self.attributes is None else self.attributes.smus_asset_schemas

    @smus_asset_schemas.setter
    def smus_asset_schemas(
        self, smus_asset_schemas: Optional[List[SageMakerUnifiedStudioAssetSchema]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_schemas = smus_asset_schemas

    class Attributes(SageMakerUnifiedStudio.Attributes):
        smus_asset_summary: Optional[str] = Field(default=None, description="")
        smus_asset_technical_name: Optional[str] = Field(default=None, description="")
        smus_asset_type: Optional[str] = Field(default=None, description="")
        smus_asset_revision: Optional[str] = Field(default=None, description="")
        smus_asset_source_identifier: Optional[str] = Field(
            default=None, description=""
        )
        smus_asset_schemas: Optional[List[SageMakerUnifiedStudioAssetSchema]] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerUnifiedStudioAsset.Attributes = Field(
        default_factory=lambda: SageMakerUnifiedStudioAsset.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sage_maker_unified_studio_asset_schema import (
    SageMakerUnifiedStudioAssetSchema,  # noqa: E402, F401
)

SageMakerUnifiedStudioAsset.Attributes.update_forward_refs()
