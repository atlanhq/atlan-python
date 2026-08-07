# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject


class AtlanRequest(AtlanObject):
    """A request (Metadata Inbox item) in Atlan, such as a suggested
    attribute change, term link, or Atlan tag attachment, that can be
    approved or rejected."""

    id: Optional[str] = Field(
        default=None, description="Unique identifier for the request (GUID)."
    )
    version: Optional[str] = Field(
        default=None, description="Version of the request in Atlan's internal store."
    )
    is_active: Optional[bool] = Field(
        default=None, description="Whether the request is still open (True) or not."
    )
    created_at: Optional[int] = Field(
        default=None,
        description="Time (epoch millis) at which the request was created.",
    )
    updated_at: Optional[int] = Field(
        default=None,
        description="Time (epoch millis) at which the request was last updated.",
    )
    created_by: Optional[str] = Field(
        default=None, description="User who created the request."
    )
    tenant_id: Optional[str] = Field(
        default=None, description="Name of the tenant (usually `default`)."
    )
    source_type: Optional[str] = Field(
        default=None,
        description=(
            "`static` for ATTRIBUTE and CUSTOM_METADATA request types, "
            "`atlas` for other request types."
        ),
    )
    source_guid: Optional[str] = Field(
        default=None, description="GUID of the source asset, if any."
    )
    source_qualified_name: Optional[str] = Field(
        default=None, description="Qualified name of the source asset, if any."
    )
    source_attribute: Optional[str] = Field(
        default=None, description="Attribute on the source asset, if any."
    )
    destination_guid: Optional[str] = Field(
        default=None, description="GUID of the asset the request was made against."
    )
    destination_qualified_name: Optional[str] = Field(
        default=None,
        description="Qualified name of the asset the request was made against.",
    )
    destination_attribute: Optional[str] = Field(
        default=None, description="Attribute the request was made against, if any."
    )
    destination_value: Optional[str] = Field(
        default=None, description="Requested value for the attribute."
    )
    destination_value_type: Optional[str] = Field(
        default=None, description="Type of the destination attribute value."
    )
    entity_type: Optional[str] = Field(
        default=None, description="Type of the asset the request was made against."
    )
    request_type: Optional[str] = Field(
        default=None,
        description=(
            "Type of the request: `attribute`, `term_link`, "
            "`attach_classification`, or `bm_attribute`."
        ),
    )
    approval_type: Optional[str] = Field(
        default=None,
        description="How the request must be approved: `single`, `unanimous` or `consesus`.",
    )
    approved_by: Optional[str] = Field(
        default=None, description="User who approved the request, if approved."
    )
    rejected_by: Optional[str] = Field(
        default=None, description="User who rejected the request, if rejected."
    )
    status: Optional[str] = Field(
        default=None,
        description="Status of the request: `active`, `approved` or `rejected`.",
    )
    message: Optional[str] = Field(
        default=None, description="Message to include with the request, if any."
    )
    payload: Optional[Dict[str, Any]] = Field(
        default=None,
        description=(
            "Payload for requests that carry one (Atlan tag details for "
            "`attach_classification`, custom metadata values for `bm_attribute`)."
        ),
    )
    destination_entity: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Limited details of the asset the request was made against.",
    )


class AttributeRequest(AtlanRequest):
    """A request to change a single attribute value on an asset."""

    @classmethod
    def creator(
        cls,
        *,
        destination_guid: str,
        destination_qualified_name: str,
        destination_attribute: str,
        destination_value: str,
        entity_type: str,
    ) -> AttributeRequest:
        """Create a request to set an attribute value on an asset.

        All wire-required fields are passed explicitly so that pyatlan's
        exclude_unset serialization sends them (declared defaults are never
        serialized — see BLDX-1589).

        :param destination_guid: GUID of the asset to change
        :param destination_qualified_name: qualified name of the asset to change
        :param destination_attribute: attribute to change (e.g. `userDescription`)
        :param destination_value: value requested for the attribute
        :param entity_type: type of the asset (e.g. `AtlasGlossaryTerm`)
        """
        return cls(
            request_type="attribute",
            source_type="static",
            approval_type="single",
            destination_guid=destination_guid,
            destination_qualified_name=destination_qualified_name,
            destination_attribute=destination_attribute,
            destination_value=destination_value,
            entity_type=entity_type,
        )


class AtlanRequestAction(AtlanObject):
    """Body for approving or rejecting a request."""

    action: str = Field(description="Action to take: `approved` or `rejected`.")
    message: Optional[str] = Field(
        default=None, description="Optional message to include with the action."
    )


class AtlanRequestResponse(AtlanObject):
    """Paged response of requests."""

    total_record: Optional[int] = Field(
        default=None, description="Total number of requests."
    )
    filter_record: Optional[int] = Field(
        default=None, description="Number of requests matching the filter."
    )
    records: Optional[List[AtlanRequest]] = Field(
        default=None, description="Requests in this page of results."
    )
