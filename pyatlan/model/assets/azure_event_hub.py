# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.model.fields.atlan_fields import KeywordField
from pyatlan.utils import init_guid, validate_required_fields

from .kafka_topic import KafkaTopic


class AzureEventHub(KafkaTopic):
    """Description"""

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> AzureEventHub:
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        attributes = AzureEventHub.Attributes.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="AzureEventHub", allow_mutation=False)

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

    """

    _convenience_properties: ClassVar[List[str]] = [
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
        azure_event_hub_status: Optional[str] = Field(default=None, description="")

        @classmethod
        @init_guid
        def creator(
            cls, *, name: str, connection_qualified_name: str
        ) -> AzureEventHub.Attributes:
            validate_required_fields(
                ["name", "connection_qualified_name"], [name, connection_qualified_name]
            )
            return AzureEventHub.Attributes(
                name=name,
                qualified_name=f"{connection_qualified_name}/topic/{name}",
                connection_qualified_name=connection_qualified_name,
                connector_name=AtlanConnectorType.get_connector_name(
                    connection_qualified_name
                ),
            )

    attributes: AzureEventHub.Attributes = Field(
        default_factory=lambda: AzureEventHub.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
