# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Azure Event Hub asset model."""

from __future__ import annotations

from typing import Union

from msgspec import UNSET, UnsetType

from pyatlan_v9.transform import register_asset
from pyatlan_v9.utils import init_guid, validate_required_fields

from .kafka_topic import KafkaTopic


@register_asset
class AzureEventHub(KafkaTopic):
    """Instance of an Azure Event Hub topic in Atlan."""

    type_name: Union[str, UnsetType] = "AzureEventHub"
    azure_event_hub_status: Union[str, None, UnsetType] = UNSET

    @classmethod
    @init_guid
    def creator(cls, *, name: str, connection_qualified_name: str) -> "AzureEventHub":
        """Create a new AzureEventHub asset."""
        validate_required_fields(
            ["name", "connection_qualified_name"], [name, connection_qualified_name]
        )
        fields = connection_qualified_name.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        return cls(
            name=name,
            qualified_name=f"{connection_qualified_name}/topic/{name}",
            connection_qualified_name=connection_qualified_name,
            connector_name=connector_name,
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AzureEventHub":
        """Create an AzureEventHub instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AzureEventHub":
        """Return only fields required for update operations."""
        return AzureEventHub.updater(qualified_name=self.qualified_name, name=self.name)
