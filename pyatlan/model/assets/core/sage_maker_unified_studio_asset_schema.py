# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordTextField, RelationField

from .sage_maker_unified_studio import SageMakerUnifiedStudio


class SageMakerUnifiedStudioAssetSchema(SageMakerUnifiedStudio):
    """Description"""

    type_name: str = Field(
        default="SageMakerUnifiedStudioAssetSchema", allow_mutation=False
    )

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "SageMakerUnifiedStudioAssetSchema":
            raise ValueError("must be SageMakerUnifiedStudioAssetSchema")
        return v

    def __setattr__(self, name, value):
        if name in SageMakerUnifiedStudioAssetSchema._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    SMUS_DATA_TYPE: ClassVar[KeywordTextField] = KeywordTextField(
        "smusDataType", "smusDataType.keyword", "smusDataType"
    )
    """
    Data Type of the Schema/Column
    """
    SMUS_ASSET_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "smusAssetQualifiedName",
        "smusAssetQualifiedName.keyword",
        "smusAssetQualifiedName",
    )
    """
    Unique name of the Atlan AWS SMUS Published/Subscribed Asset that contains this schema
    """
    SMUS_ASSET_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "smusAssetName", "smusAssetName.keyword", "smusAssetName"
    )
    """
    Name of the Atlan AWS SMUS Published/Subscribed Asset that contains this schema
    """

    SMUS_PUBLISHED_ASSET: ClassVar[RelationField] = RelationField("smusPublishedAsset")
    """
    TBC
    """
    SMUS_SUBSCRIBED_ASSET: ClassVar[RelationField] = RelationField(
        "smusSubscribedAsset"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "smus_data_type",
        "smus_asset_qualified_name",
        "smus_asset_name",
        "smus_published_asset",
        "smus_subscribed_asset",
    ]

    @property
    def smus_data_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_data_type

    @smus_data_type.setter
    def smus_data_type(self, smus_data_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_data_type = smus_data_type

    @property
    def smus_asset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.smus_asset_qualified_name
        )

    @smus_asset_qualified_name.setter
    def smus_asset_qualified_name(self, smus_asset_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_qualified_name = smus_asset_qualified_name

    @property
    def smus_asset_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.smus_asset_name

    @smus_asset_name.setter
    def smus_asset_name(self, smus_asset_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset_name = smus_asset_name

    @property
    def smus_published_asset(self) -> Optional[SageMakerUnifiedStudioPublishedAsset]:
        return None if self.attributes is None else self.attributes.smus_published_asset

    @smus_published_asset.setter
    def smus_published_asset(
        self, smus_published_asset: Optional[SageMakerUnifiedStudioPublishedAsset]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_published_asset = smus_published_asset

    @property
    def smus_subscribed_asset(self) -> Optional[SageMakerUnifiedStudioSubscribedAsset]:
        return (
            None if self.attributes is None else self.attributes.smus_subscribed_asset
        )

    @smus_subscribed_asset.setter
    def smus_subscribed_asset(
        self, smus_subscribed_asset: Optional[SageMakerUnifiedStudioSubscribedAsset]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_subscribed_asset = smus_subscribed_asset

    class Attributes(SageMakerUnifiedStudio.Attributes):
        smus_data_type: Optional[str] = Field(default=None, description="")
        smus_asset_qualified_name: Optional[str] = Field(default=None, description="")
        smus_asset_name: Optional[str] = Field(default=None, description="")
        smus_published_asset: Optional[SageMakerUnifiedStudioPublishedAsset] = Field(
            default=None, description=""
        )  # relationship
        smus_subscribed_asset: Optional[SageMakerUnifiedStudioSubscribedAsset] = Field(
            default=None, description=""
        )  # relationship

    attributes: SageMakerUnifiedStudioAssetSchema.Attributes = Field(
        default_factory=lambda: SageMakerUnifiedStudioAssetSchema.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .sage_maker_unified_studio_published_asset import (
    SageMakerUnifiedStudioPublishedAsset,  # noqa: E402, F401
)
from .sage_maker_unified_studio_subscribed_asset import (
    SageMakerUnifiedStudioSubscribedAsset,  # noqa: E402, F401
)
