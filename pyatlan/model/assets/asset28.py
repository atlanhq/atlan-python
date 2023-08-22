# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField
from pyatlan.model.structs import AzureTag

from .asset08 import Cloud


class Azure(Cloud):
    """Description"""

    type_name: str = Field("Azure", allow_mutation=False)

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
    TBC
    """
    AZURE_LOCATION: ClassVar[KeywordField] = KeywordField(
        "azureLocation", "azureLocation"
    )
    """
    TBC
    """
    ADLS_ACCOUNT_SECONDARY_LOCATION: ClassVar[KeywordField] = KeywordField(
        "adlsAccountSecondaryLocation", "adlsAccountSecondaryLocation"
    )
    """
    TBC
    """
    AZURE_TAGS: ClassVar[KeywordField] = KeywordField("azureTags", "azureTags")
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
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
    def azure_tags(self) -> Optional[list[AzureTag]]:
        return None if self.attributes is None else self.attributes.azure_tags

    @azure_tags.setter
    def azure_tags(self, azure_tags: Optional[list[AzureTag]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_tags = azure_tags

    class Attributes(Cloud.Attributes):
        azure_resource_id: Optional[str] = Field(
            None, description="", alias="azureResourceId"
        )
        azure_location: Optional[str] = Field(
            None, description="", alias="azureLocation"
        )
        adls_account_secondary_location: Optional[str] = Field(
            None, description="", alias="adlsAccountSecondaryLocation"
        )
        azure_tags: Optional[list[AzureTag]] = Field(
            None, description="", alias="azureTags"
        )

    attributes: "Azure.Attributes" = Field(
        default_factory=lambda: Azure.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


Azure.Attributes.update_forward_refs()
