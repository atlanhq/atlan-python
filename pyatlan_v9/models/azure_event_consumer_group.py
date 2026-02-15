# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""AzureEventHubConsumerGroup asset model for pyatlan_v9."""

from __future__ import annotations

from pyatlan_v9.transform import register_asset
from pyatlan_v9.utils import init_guid, validate_required_fields

from .kafka_consumer_group import KafkaConsumerGroup


@register_asset
class AzureEventHubConsumerGroup(KafkaConsumerGroup):
    """Instance of an Azure Event Hub consumer group in Atlan."""

    type_name: str = "AzureEventHubConsumerGroup"

    @classmethod
    @init_guid
    def creator(
        cls, *, name: str, event_hub_qualified_names: list[str]
    ) -> "AzureEventHubConsumerGroup":
        """Create a new AzureEventHubConsumerGroup asset."""
        validate_required_fields(
            ["name", "event_hub_qualified_names"], [name, event_hub_qualified_names]
        )
        first_event_hub_qn = event_hub_qualified_names[0]
        fields = first_event_hub_qn.split("/")
        connector_name = fields[1] if len(fields) > 1 else None
        connection_qualified_name = (
            "/".join(fields[:3]) if len(fields) >= 3 else first_event_hub_qn
        )
        first_event_hub_name = fields[4] if len(fields) > 4 else fields[-1]
        return cls(
            name=name,
            connector_name=connector_name,
            connection_qualified_name=connection_qualified_name,
            kafka_topic_qualified_names=set(event_hub_qualified_names),
            qualified_name=f"{connection_qualified_name}/consumer-group/{first_event_hub_name}/{name}",
        )

    @classmethod
    def updater(cls, *, qualified_name: str, name: str) -> "AzureEventHubConsumerGroup":
        """Create an AzureEventHubConsumerGroup instance for update operations."""
        validate_required_fields(["qualified_name", "name"], [qualified_name, name])
        return cls(qualified_name=qualified_name, name=name)

    def trim_to_required(self) -> "AzureEventHubConsumerGroup":
        """Return only fields required for update operations."""
        return AzureEventHubConsumerGroup.updater(
            qualified_name=self.qualified_name, name=self.name
        )
