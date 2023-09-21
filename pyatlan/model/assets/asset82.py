# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Optional

from pydantic import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField

from .asset80 import KafkaTopic


class AzureEventHub(KafkaTopic):
    """Description"""

    type_name: str = Field("AzureEventHub", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AzureEventHub":
            raise ValueError("must be AzureEventHub")
        return v

    def __setattr__(self, name, value):
        if name in AzureEventHub._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AZURE_EVENT_HUB_STATUS: ClassVar[KeywordField] = KeywordField(
        "azureEventHubStatus", "azureEventHubStatus"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[list[str]] = [
        "azure_event_hub_status",
    ]

    @property
    def azure_event_hub_status(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.azure_event_hub_status
        )

    @azure_event_hub_status.setter
    def azure_event_hub_status(self, azure_event_hub_status: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_event_hub_status = azure_event_hub_status

    class Attributes(KafkaTopic.Attributes):
        azure_event_hub_status: Optional[str] = Field(
            None, description="", alias="azureEventHubStatus"
        )

    attributes: "AzureEventHub.Attributes" = Field(
        default_factory=lambda: AzureEventHub.Attributes(),
        description="Map of attributes in the instance and their values. The specific keys of this map will vary by "
        "type, so are described in the sub-types of this schema.\n",
    )


AzureEventHub.Attributes.update_forward_refs()
