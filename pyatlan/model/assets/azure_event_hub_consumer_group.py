# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanConnectorType
from pyatlan.utils import init_guid, validate_required_fields

from .azure_event_hub import AzureEventHub
from .kafka_consumer_group import KafkaConsumerGroup


class AzureEventHubConsumerGroup(KafkaConsumerGroup):
    """Description"""

    @classmethod
    @init_guid
    def creator(
        cls,
        *,
        name: str,
        event_hub_qualified_names: List[str],
    ) -> AzureEventHubConsumerGroup:
        validate_required_fields(
            ["name", "event_hub_qualified_names"],
            [name, event_hub_qualified_names],
        )
        event_hubs = []
        for event_hub_qn in event_hub_qualified_names:
            connection_qn, connector_name = AtlanConnectorType.get_connector_name(
                event_hub_qn, "event_hub_qualified_names", 5
            )
            event_hubs.append(AzureEventHub.ref_by_qualified_name(event_hub_qn))

        # Following a similar approach to construct the qualified name:
        # https://github.com/atlanhq/marketplace-packages/blob/master/packages/atlan/azure-event-hub/transformers/eh-consumer-group.jinja2#L9
        first_event_hub_name = event_hub_qualified_names[0].split("/")[4]

        attributes = AzureEventHubConsumerGroup.Attributes(
            name=name,
            connector_name=connector_name,
            connection_qualified_name=connection_qn,
            kafka_topics=event_hubs,  # type:ignore[arg-type]
            kafka_topic_qualified_names=set(event_hub_qualified_names),
            qualified_name=f"{connection_qn}/consumer-group/{first_event_hub_name}/{name}",
        )
        return cls(attributes=attributes)

    type_name: str = Field(default="AzureEventHubConsumerGroup", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AzureEventHubConsumerGroup":
            raise ValueError("must be AzureEventHubConsumerGroup")
        return v

    def __setattr__(self, name, value):
        if name in AzureEventHubConsumerGroup._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    _convenience_properties: ClassVar[List[str]] = []
