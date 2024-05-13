# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .azure_service_bus import AzureServiceBus


class AzureServiceBusNamespace(AzureServiceBus):
    """Description"""

    type_name: str = Field(default="AzureServiceBusNamespace", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AzureServiceBusNamespace":
            raise ValueError("must be AzureServiceBusNamespace")
        return v

    def __setattr__(self, name, value):
        if name in AzureServiceBusNamespace._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AZURE_SERVICE_BUS_TOPICS: ClassVar[RelationField] = RelationField(
        "azureServiceBusTopics"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "azure_service_bus_topics",
    ]

    @property
    def azure_service_bus_topics(self) -> Optional[List[AzureServiceBusTopic]]:
        return (
            None
            if self.attributes is None
            else self.attributes.azure_service_bus_topics
        )

    @azure_service_bus_topics.setter
    def azure_service_bus_topics(
        self, azure_service_bus_topics: Optional[List[AzureServiceBusTopic]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_service_bus_topics = azure_service_bus_topics

    class Attributes(AzureServiceBus.Attributes):
        azure_service_bus_topics: Optional[List[AzureServiceBusTopic]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AzureServiceBusNamespace.Attributes = Field(
        default_factory=lambda: AzureServiceBusNamespace.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .azure_service_bus_topic import AzureServiceBusTopic  # noqa
