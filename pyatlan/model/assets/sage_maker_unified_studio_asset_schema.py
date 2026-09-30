# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, RelationField

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

    SMUS_DATA_TYPE: ClassVar[KeywordField] = KeywordField(
        "smusDataType", "smusDataType"
    )
    """
    Data type of the schema/column.
    """
    SMUS_ASSET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "smusAssetQualifiedName", "smusAssetQualifiedName"
    )
    """
    Unique name of the Atlan SageMaker Unified Studio published/subscribed asset that contains this schema.
    """
    SMUS_ASSET_NAME: ClassVar[KeywordField] = KeywordField(
        "smusAssetName", "smusAssetName"
    )
    """
    Simple name of the Atlan SageMaker Unified Studio published/subscribed asset that contains this schema.
    """

    SMUS_ASSET: ClassVar[RelationField] = RelationField("smusAsset")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "smus_data_type",
        "smus_asset_qualified_name",
        "smus_asset_name",
        "smus_asset",
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
    def smus_asset(self) -> Optional[SageMakerUnifiedStudioAsset]:
        return None if self.attributes is None else self.attributes.smus_asset

    @smus_asset.setter
    def smus_asset(self, smus_asset: Optional[SageMakerUnifiedStudioAsset]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.smus_asset = smus_asset

    class Attributes(SageMakerUnifiedStudio.Attributes):
        smus_data_type: Optional[str] = Field(default=None, description="")
        smus_asset_qualified_name: Optional[str] = Field(default=None, description="")
        smus_asset_name: Optional[str] = Field(default=None, description="")
        smus_asset: Optional[SageMakerUnifiedStudioAsset] = Field(
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


from .sage_maker_unified_studio_asset import (
    SageMakerUnifiedStudioAsset,  # noqa: E402, F401
)

SageMakerUnifiedStudioAssetSchema.Attributes.update_forward_refs()
