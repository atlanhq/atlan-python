# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Literal, Union

import msgspec

from pyatlan_v9.model.assets.asset import Asset
from pyatlan_v9.model.core import AtlanTag

# =============================================================================
# EVENT PAYLOAD TYPES
# =============================================================================


class AtlanEventPayload(msgspec.Struct, kw_only=True, rename="camel"):
    """Base payload for Atlan events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    """Type of the event payload."""

    operation_type: str = ""
    """Type of the operation the event contains a payload for."""

    event_time: Union[int, None] = None
    """Time (epoch) the event was triggered in the source system, in milliseconds."""

    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    """Details of the asset that was impacted by the event."""


class AssetCreatePayload(msgspec.Struct, kw_only=True, rename="camel"):
    """Payload for asset creation events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["ENTITY_CREATE"] = "ENTITY_CREATE"


class AssetUpdatePayload(msgspec.Struct, kw_only=True, rename="camel"):
    """Payload for asset update events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["ENTITY_UPDATE"] = "ENTITY_UPDATE"
    mutated_details: Union[Asset, None] = None
    """Details of what was updated on the asset."""


class AssetDeletePayload(msgspec.Struct, kw_only=True, rename="camel"):
    """Payload for asset deletion events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["ENTITY_DELETE"] = "ENTITY_DELETE"


class CustomMetadataUpdatePayload(msgspec.Struct, kw_only=True, rename="camel"):
    """Payload for custom metadata update events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["BUSINESS_ATTRIBUTE_UPDATE"] = "BUSINESS_ATTRIBUTE_UPDATE"
    mutated_details: Union[dict[str, Any], None] = None
    """Map of custom metadata attributes and values defined on the asset."""


class AtlanTagAddPayload(msgspec.Struct, kw_only=True, rename="camel"):
    """Payload for Atlan tag addition events."""

    event_type: Union[str, None] = msgspec.field(default=None, name="type")
    event_time: Union[int, None] = None
    asset: Union[Asset, None] = msgspec.field(default=None, name="entity")
    operation_type: Literal["CLASSIFICATION_ADD"] = "CLASSIFICATION_ADD"
    mutated_details: Union[list[AtlanTag], None] = None
    """Atlan tags that were added to the asset by this event."""


class AtlanTagDeletePayload(msgspec.Struct, kw_only=True, rename="camel"):
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


def _atlan_tag_from_dict(data: dict[str, Any]) -> AtlanTag:
    """Construct an AtlanTag from a camelCase dict.

    Uses manual construction to avoid ``msgspec.convert`` schema
    validation issues with ``Union[str, AtlanTagName, None]``.
    """
    return AtlanTag(
        type_name=data.get("typeName"),
        entity_guid=data.get("entityGuid"),
        entity_status=data.get("entityStatus"),
        propagate=data.get("propagate"),
        remove_propagations_on_entity_delete=data.get(
            "removePropagationsOnEntityDelete"
        ),
        restrict_propagation_through_lineage=data.get(
            "restrictPropagationThroughLineage"
        ),
        restrict_propagation_through_hierarchy=data.get(
            "restrictPropagationThroughHierarchy"
        ),
        validity_periods=data.get("validityPeriods"),
        attributes=data.get("attributes"),
    )


# Map of operation type string to payload class
_PAYLOAD_MAP: dict[str, type] = {
    "ENTITY_CREATE": AssetCreatePayload,
    "ENTITY_UPDATE": AssetUpdatePayload,
    "ENTITY_DELETE": AssetDeletePayload,
    "BUSINESS_ATTRIBUTE_UPDATE": CustomMetadataUpdatePayload,
    "CLASSIFICATION_ADD": AtlanTagAddPayload,
    "CLASSIFICATION_DELETE": AtlanTagDeletePayload,
}


# =============================================================================
# ATLAN EVENT
# =============================================================================


class AtlanEvent(msgspec.Struct, kw_only=True, rename="camel"):
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

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AtlanEvent:
        """Deserialize from a dict, handling polymorphic asset dispatch
        and payload type discrimination.

        This is the primary deserialization entry point for v9 events.
        It uses :func:`~pyatlan_v9.model.transform.from_atlas_format` to
        resolve the correct Asset subclass based on ``typeName``, and a
        simple lookup on ``operationType`` to pick the right payload type.

        :param data: Raw event dict (camelCase keys as received from the API).
        :returns: A fully-constructed AtlanEvent with typed payload and asset.
        """
        # Ensure v9 assets are registered in the type registry
        import pyatlan_v9.model.assets  # noqa: F401
        from pyatlan_v9.model.transform import from_atlas_format

        message = data.get("message")
        payload = None

        if message:
            op_type = message.get("operationType", "")
            payload_cls = _PAYLOAD_MAP.get(op_type)

            if payload_cls:
                # Convert entity using the v9 asset registry
                entity_data = message.get("entity")
                asset = from_atlas_format(entity_data) if entity_data else None

                # Build common payload kwargs
                kwargs: dict[str, Any] = {
                    "event_type": message.get("type"),
                    "event_time": message.get("eventTime"),
                    "asset": asset,
                    "operation_type": op_type,
                }

                # Handle mutated_details based on payload type
                mutated_details_raw = message.get("mutatedDetails")
                if mutated_details_raw is not None:
                    if op_type == "ENTITY_UPDATE":
                        # mutated_details is another asset in Atlas API format
                        kwargs["mutated_details"] = from_atlas_format(
                            mutated_details_raw
                        )
                    elif op_type == "BUSINESS_ATTRIBUTE_UPDATE":
                        # mutated_details is a dict of custom metadata
                        kwargs["mutated_details"] = mutated_details_raw
                    elif op_type in (
                        "CLASSIFICATION_ADD",
                        "CLASSIFICATION_DELETE",
                    ):
                        # mutated_details is a list of classification dicts;
                        # construct AtlanTag manually to avoid msgspec.convert
                        # schema issues with Union[str, AtlanTagName, None]
                        kwargs["mutated_details"] = [
                            _atlan_tag_from_dict(item) for item in mutated_details_raw
                        ]

                payload = payload_cls(**kwargs)

        # Build the event directly (avoids msgspec.convert schema validation
        # issues with complex Union types like AtlanTagName in nested models)
        return cls(
            source=data.get("source"),
            version=data.get("version"),
            msg_compression_kind=data.get("msgCompressionKind"),
            msg_split_idx=data.get("msgSplitIdx"),
            msg_split_count=data.get("msgSplitCount"),
            msg_source_ip=data.get("msgSourceIP"),
            msg_created_by=data.get("msgCreatedBy"),
            msg_creation_time=data.get("msgCreationTime"),
            spooled=data.get("spooled"),
            payload=payload,
        )


# =============================================================================
# AWS WRAPPER TYPES
# =============================================================================


class AwsRequestContext(msgspec.Struct, kw_only=True, rename="camel"):
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


class AwsEventWrapper(msgspec.Struct, kw_only=True, rename="camel"):
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
