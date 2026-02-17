# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Literal, Union

import msgspec

from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanTag


class AtlanEventPayload(msgspec.Struct, kw_only=True):
    """Base payload for Atlan events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    """Type of the event payload."""

    operation_type: str = ""
    """Type of the operation the event contains a payload for."""

    event_time: Union[int, None] = None
    """Time (epoch) the event was triggered in the source system, in milliseconds."""

    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    """Details of the asset that was impacted by the event."""


class AssetCreatePayload(msgspec.Struct, kw_only=True):
    """Payload for asset creation events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["ENTITY_CREATE"] = "ENTITY_CREATE"


class AssetUpdatePayload(msgspec.Struct, kw_only=True):
    """Payload for asset update events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["ENTITY_UPDATE"] = "ENTITY_UPDATE"
    mutated_details: Union[Asset, None] = None
    """Details of what was updated on the asset."""


class AssetDeletePayload(msgspec.Struct, kw_only=True):
    """Payload for asset deletion events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["ENTITY_DELETE"] = "ENTITY_DELETE"


class CustomMetadataUpdatePayload(msgspec.Struct, kw_only=True):
    """Payload for custom metadata update events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["BUSINESS_ATTRIBUTE_UPDATE"] = "BUSINESS_ATTRIBUTE_UPDATE"
    mutated_details: Union[dict[str, Any], None] = None
    """Map of custom metadata attributes and values defined on the asset."""


class AtlanTagAddPayload(msgspec.Struct, kw_only=True):
    """Payload for Atlan tag addition events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["CLASSIFICATION_ADD"] = "CLASSIFICATION_ADD"
    mutated_details: Union[list[AtlanTag], None] = None
    """Atlan tags that were added to the asset by this event."""


class AtlanTagDeletePayload(msgspec.Struct, kw_only=True):
    """Payload for Atlan tag deletion events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["CLASSIFICATION_DELETE"] = "CLASSIFICATION_DELETE"
    mutated_details: Union[list[AtlanTag], None] = None
    """Atlan tags that were removed from the asset by this event."""


# Union of all event payload types
EventPayload = Union[
    AssetCreatePayload,
    AssetUpdatePayload,
    AssetDeletePayload,
    AtlanTagAddPayload,
    AtlanTagDeletePayload,
    CustomMetadataUpdatePayload,
]


class AtlanEvent(msgspec.Struct, kw_only=True):
    """Wrapper for an Atlan event."""

    source: Union[Any, None] = None
    version: Union[Any, None] = None
    msg_compression_kind: Union[str, None] = None
    msg_split_idx: Union[int, None] = None
    msg_split_count: Union[int, None] = None
    msg_source_ip: Union[str, None] = None
    """Originating IP address for the event."""
    msg_created_by: Union[str, None] = None
    msg_creation_time: Union[int, None] = None
    """Timestamp (epoch) for when the event was created, in milliseconds."""
    spooled: Union[bool, None] = None
    payload: Union[EventPayload, None] = msgspec.field(default=None, name="message")
    """Detailed contents (payload) of the event."""


class AwsRequestContext(msgspec.Struct, kw_only=True):
    """AWS API Gateway request context."""

    account_id: Union[str, None] = None
    """Account from which the request originated."""
    api_id: Union[str, None] = None
    domain_name: Union[str, None] = None
    domain_prefix: Union[str, None] = None
    http: Union[dict[str, str], None] = None
    request_id: Union[str, None] = None
    route_key: Union[str, None] = None
    stage: Union[str, None] = None
    time: Union[str, None] = None
    """Time at which the event was received, as a formatted string."""
    time_epoch: Union[int, None] = None
    """Time at which the event was received, epoch-based, in milliseconds."""


class AwsEventWrapper(msgspec.Struct, kw_only=True):
    """AWS Lambda event wrapper."""

    version: Union[str, None] = None
    route_key: Union[str, None] = None
    raw_path: Union[str, None] = None
    raw_query_string: Union[str, None] = None
    headers: Union[dict[str, str], None] = None
    """Headers used when sending the event through to the Lambda URL."""
    request_context: Union[AwsRequestContext, None] = None
    body: Union[str, None] = None
    """Actual contents of the event that was sent by Atlan."""
    is_base_64_encoded: Union[bool, None] = None
    """Whether the contents are base64-encoded (True) or plain text (False)."""
