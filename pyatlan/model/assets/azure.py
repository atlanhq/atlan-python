# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField
from pyatlan.model.structs import AzureTag

from .cloud import Cloud


class Azure(Cloud):
    """Description"""

    type_name: str = Field(default="Azure", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Azure":
            raise ValueError("must be Azure")
        return v

    def __setattr__(self, name, value):
        if name in Azure._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AZURE_RESOURCE_ID: ClassVar[KeywordTextField] = KeywordTextField(
        "azureResourceId", "azureResourceId", "azureResourceId.text"
    )
    """
    Resource identifier of this asset in Azure.
    """
    AZURE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "azureLocation", "azureLocation"
    )
    """
    Location of this asset in Azure.
    """
    ADLS_ACCOUNT_SECONDARY_LOCATION: ClassVar[KeywordField] = KeywordField(
        "adlsAccountSecondaryLocation", "adlsAccountSecondaryLocation"
    )
    """
    Secondary location of the ADLS account.
    """
    AZURE_TAGS: ClassVar[KeywordField] = KeywordField("azureTags", "azureTags")
    """
    Tags that have been applied to this asset in Azure.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "azure_resource_id",
        "azure_location",
        "adls_account_secondary_location",
        "azure_tags",
    ]

    @property
    def azure_resource_id(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_resource_id

    @azure_resource_id.setter
    def azure_resource_id(self, azure_resource_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_resource_id = azure_resource_id

    @property
    def azure_location(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.azure_location

    @azure_location.setter
    def azure_location(self, azure_location: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_location = azure_location

    @property
    def adls_account_secondary_location(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.adls_account_secondary_location
        )

    @adls_account_secondary_location.setter
    def adls_account_secondary_location(
        self, adls_account_secondary_location: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.adls_account_secondary_location = (
            adls_account_secondary_location
        )

    @property
    def azure_tags(self) -> Optional[List[AzureTag]]:
        return None if self.attributes is None else self.attributes.azure_tags

    @azure_tags.setter
    def azure_tags(self, azure_tags: Optional[List[AzureTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_tags = azure_tags

    class Attributes(Cloud.Attributes):
        azure_resource_id: Optional[str] = Field(default=None, description="")
        azure_location: Optional[str] = Field(default=None, description="")
        adls_account_secondary_location: Optional[str] = Field(
            default=None, description=""
        )
        azure_tags: Optional[List[AzureTag]] = Field(default=None, description="")

    attributes: Azure.Attributes = Field(
        default_factory=lambda: Azure.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
