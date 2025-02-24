# SPDX-License-Identifier: Apache-2.0
# Copyright 2023 Atlan Pte. Ltd.
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic.v1 import Field

from pyatlan.model.assets import Asset
from pyatlan.model.core import AtlanObject, AtlanTag


class AtlanEventPayload(AtlanObject):
    _subtypes_: Dict[str, type] = dict()

    def __init_subclass__(
        cls, event_type="ENTITY_NOTIFICATION_V2", operation_type=None
    ):
        cls._subtypes_[operation_type or cls.__name__.lower()] = cls

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["type", "operation_type"])

    event_type: Optional[str] = Field(
        default=None, description="Type of the event payload.", alias="type"
    )
    operation_type: Literal[
        "ENTITY_CREATE",
        "ENTITY_UPDATE",
        "ENTITY_DELETE",
        "BUSINESS_ATTRIBUTE_UPDATE",
        "CLASSIFICATION_ADD",
        "CLASSIFICATION_DELETE",
    ] = Field(description="Type of the operation the event contains a payload for.")
    event_time: Optional[int] = Field(
        description="Time (epoch) the event was triggered in the source system, in milliseconds."
    )
    asset: Optional[Asset] = Field(
        description="Details of the asset that was impacted by the event."
        "Note that the details of some operations (like custom metadata changes)"
        "are NOT included in this object, but only tin the associated mutated_details.",
        alias="entity",
    )


class AssetCreatePayload(AtlanEventPayload):
    operation_type: Literal["ENTITY_CREATE"] = Field(
        description="Type of the operation the event contains a payload for."
    )


class AssetUpdatePayload(AtlanEventPayload):
    operation_type: Literal["ENTITY_UPDATE"] = Field(
        description="Type of the operation the event contains a payload for."
    )
    mutated_details: Optional[Asset] = Field(
        description="Details of what was updated on the asset."
    )


class AssetDeletePayload(AtlanEventPayload):
    operation_type: Literal["ENTITY_DELETE"] = Field(
        description="Type of the operation the event contains a payload for."
    )


class CustomMetadataUpdatePayload(
    AtlanEventPayload,
):
    operation_type: Literal["BUSINESS_ATTRIBUTE_UPDATE"] = Field(
        description="Type of the operation the event contains a payload for."
    )
    # TODO: Need to create a more specific type
    mutated_details: Optional[Dict[str, Any]] = Field(
        description="Map of custom metadata attributes and values defined on the asset."
        "The map is keyed by the human-readable name of the custom metadata set,"
        "and the values are a further mapping from human-readable attribute name"
        "to the value for that attribute as provided when updating this asset."
    )


class AtlanTagAddPayload(
    AtlanEventPayload,
):
    operation_type: Literal["CLASSIFICATION_ADD"] = Field(
        description="Type of the operation the event contains a payload for."
    )
    mutated_details: Optional[List[AtlanTag]] = Field(
        description="Atlan tags that were added to the asset by this event."
    )


class AtlanTagDeletePayload(
    AtlanEventPayload,
):
    operation_type: Literal["CLASSIFICATION_DELETE"] = Field(
        description="Type of the operation the event contains a payload for."
    )
    mutated_details: Optional[List[AtlanTag]] = Field(
        description="Atlan tags that were removed from the asset by this event."
    )


class AtlanEvent(AtlanObject):
    source: Optional[Any] = Field(description="TBC")
    version: Optional[Any] = Field(description="TBC")
    msg_compression_kind: Optional[str] = Field(default=None, description="TBC")
    msg_split_idx: Optional[int] = Field(description="TBC")
    msg_split_count: Optional[int] = Field(description="TBC")
    msg_source_ip: Optional[str] = Field(
        default=None, description="Originating IP address for the event."
    )
    msg_created_by: Optional[str] = Field(default=None, description="TBC")
    msg_creation_time: Optional[int] = Field(
        description="Timestamp (epoch) for when the event was created, in milliseconds."
    )
    spooled: Optional[bool] = Field(description="TBC")
    payload: Optional[
        Union[
            AssetCreatePayload,
            AssetUpdatePayload,
            AssetDeletePayload,
            AtlanTagAddPayload,
            AtlanTagDeletePayload,
            CustomMetadataUpdatePayload,
        ]
    ] = Field(
        description="Detailed contents (payload) of the event.",
        alias="message",
        discriminator="operation_type",
    )


class AwsRequestContext(AtlanObject):
    account_id: Optional[str] = Field(
        default=None, description="Account from which the request originated."
    )
    api_id: Optional[str] = Field(default=None, description="TBC")
    domain_name: Optional[str] = Field(default=None, description="TBC")
    domain_prefix: Optional[str] = Field(default=None, description="TBC")
    http: Optional[Dict[str, str]] = Field(description="TBC")
    request_id: Optional[str] = Field(default=None, description="TBC")
    route_key: Optional[str] = Field(default=None, description="TBC")
    stage: Optional[str] = Field(default=None, description="TBC")
    time: Optional[str] = Field(
        default=None,
        description="Time at which the event was received, as a formatted string.",
    )
    time_epoch: Optional[int] = Field(
        description="Time at which the event was received, epoch-based, in milliseconds."
    )


class AwsEventWrapper(AtlanObject):
    version: Optional[str] = Field(default=None, description="TBC")
    route_key: Optional[str] = Field(default=None, description="TBC")
    raw_path: Optional[str] = Field(default=None, description="TBC")
    raw_query_string: Optional[str] = Field(default=None, description="TBC")
    headers: Optional[Dict[str, str]] = Field(
        description="Headers that were used when sending the event through to the Lambda URL."
    )
    request_context: Optional[AwsRequestContext] = Field(description="TBC")
    body: Optional[str] = Field(
        default=None, description="Actual contents of the event that was sent by Atlan."
    )
    is_base_64_encoded: Optional[bool] = Field(
        description="Whether the contents are base64-encoded (True) or plain text (False)."
    )
