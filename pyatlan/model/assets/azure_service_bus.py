# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import KeywordField, KeywordTextField

from .event_store import EventStore


class AzureServiceBus(EventStore):
    """Description"""

    type_name: str = Field(default="AzureServiceBus", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AzureServiceBus":
            raise ValueError("must be AzureServiceBus")
        return v

    def __setattr__(self, name, value):
        if name in AzureServiceBus._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    AZURE_SERVICE_BUS_NAMESPACE_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "azureServiceBusNamespaceQualifiedName", "azureServiceBusNamespaceQualifiedName"
    )
    """
    Unique name of the AzureServiceBus Namespace in which this asset exists.
    """
    AZURE_SERVICE_BUS_NAMESPACE_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "azureServiceBusNamespaceName",
        "azureServiceBusNamespaceName.keyword",
        "azureServiceBusNamespaceName",
    )
    """
    Simple name of the AzureServiceBus Namespace in which this asset exists.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "azure_service_bus_namespace_qualified_name",
        "azure_service_bus_namespace_name",
    ]

    @property
    def azure_service_bus_namespace_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.azure_service_bus_namespace_qualified_name
        )

    @azure_service_bus_namespace_qualified_name.setter
    def azure_service_bus_namespace_qualified_name(
        self, azure_service_bus_namespace_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_service_bus_namespace_qualified_name = (
            azure_service_bus_namespace_qualified_name
        )

    @property
    def azure_service_bus_namespace_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.azure_service_bus_namespace_name
        )

    @azure_service_bus_namespace_name.setter
    def azure_service_bus_namespace_name(
        self, azure_service_bus_namespace_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.azure_service_bus_namespace_name = (
            azure_service_bus_namespace_name
        )

    class Attributes(EventStore.Attributes):
        azure_service_bus_namespace_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        azure_service_bus_namespace_name: Optional[str] = Field(
            default=None, description=""
        )

    attributes: AzureServiceBus.Attributes = Field(
        default_factory=lambda: AzureServiceBus.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
