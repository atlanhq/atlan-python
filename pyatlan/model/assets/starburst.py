# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .core.s_q_l import SQL


class Starburst(SQL):
    """Description"""

    type_name: str = Field(default="Starburst", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Starburst":
            raise ValueError("must be Starburst")
        return v

    def __setattr__(self, name, value):
        if name in Starburst._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    STARBURST_DATA_PRODUCT_NAME: ClassVar[KeywordField] = KeywordField(
        "starburstDataProductName", "starburstDataProductName"
    )
    """
    Name of the Starburst Data Product that contains this asset.
    """
    STARBURST_DATASET_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "starburstDatasetQualifiedName", "starburstDatasetQualifiedName"
    )
    """
    Unique name of the Starburst Dataset that contains this asset, or this asset's own qualified name if it is a Dataset.
    """  # noqa: E501
    STARBURST_DATASET_NAME: ClassVar[KeywordField] = KeywordField(
        "starburstDatasetName", "starburstDatasetName"
    )
    """
    Simple name of the Starburst Dataset that contains this asset, or this asset's own name if it is a Dataset.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "starburst_data_product_name",
        "starburst_dataset_qualified_name",
        "starburst_dataset_name",
    ]

    @property
    def starburst_data_product_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.starburst_data_product_name
        )

    @starburst_data_product_name.setter
    def starburst_data_product_name(self, starburst_data_product_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.starburst_data_product_name = starburst_data_product_name

    @property
    def starburst_dataset_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.starburst_dataset_qualified_name
        )

    @starburst_dataset_qualified_name.setter
    def starburst_dataset_qualified_name(
        self, starburst_dataset_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.starburst_dataset_qualified_name = (
            starburst_dataset_qualified_name
        )

    @property
    def starburst_dataset_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.starburst_dataset_name
        )

    @starburst_dataset_name.setter
    def starburst_dataset_name(self, starburst_dataset_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.starburst_dataset_name = starburst_dataset_name

    class Attributes(SQL.Attributes):
        starburst_data_product_name: Optional[str] = Field(default=None, description="")
        starburst_dataset_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        starburst_dataset_name: Optional[str] = Field(default=None, description="")

    attributes: Starburst.Attributes = Field(
        default_factory=lambda: Starburst.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


Starburst.Attributes.update_forward_refs()
