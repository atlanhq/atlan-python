# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import RelationField

from .azure_service_bus import AzureServiceBus


class AzureServiceBusTopic(AzureServiceBus):
    """Description"""

    type_name: str = Field(default="AzureServiceBusTopic", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AzureServiceBusTopic":
            raise ValueError("must be AzureServiceBusTopic")
        return v

    def __setattr__(self, name, value):
        if name in AzureServiceBusTopic._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AZURE_SERVICE_BUS_NAMESPACE: ClassVar[RelationField] = RelationField(
        "azureServiceBusNamespace"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "azure_service_bus_namespace",
    ]

    @property
    def azure_service_bus_namespace(self) -> Optional[AzureServiceBusNamespace]:
        return (
            None
            if self.attributes is None
            else self.attributes.azure_service_bus_namespace
        )

    @azure_service_bus_namespace.setter
    def azure_service_bus_namespace(
        self, azure_service_bus_namespace: Optional[AzureServiceBusNamespace]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_service_bus_namespace = azure_service_bus_namespace

    class Attributes(AzureServiceBus.Attributes):
        azure_service_bus_namespace: Optional[AzureServiceBusNamespace] = Field(
            default=None, description=""
        )  # relationship

    attributes: AzureServiceBusTopic.Attributes = Field(
        default_factory=lambda: AzureServiceBusTopic.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .azure_service_bus_namespace import AzureServiceBusNamespace  # noqa
