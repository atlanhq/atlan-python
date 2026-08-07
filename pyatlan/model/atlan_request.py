# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

import json
from typing import Any, Dict, Generator, List, Optional, Union

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanRequestStatus, AtlanRequestType
from pyatlan.utils import API


def build_requests_filter(
    status: Optional[AtlanRequestStatus] = None,
    request_type: Optional[AtlanRequestType] = None,
    destination_guid: Optional[str] = None,
    destination_qualified_name: Optional[str] = None,
    entity_type: Optional[str] = None,
    created_by: Optional[str] = None,
    post_filter: Optional[str] = None,
) -> Optional[str]:
    """Build the JSON filter for listing requests from typed arguments.

    Each argument is an exact match on the corresponding request field;
    multiple arguments are combined with AND. ``post_filter`` is the raw
    escape hatch — when given, it is used as-is and the typed arguments
    must not be combined with it.
    """
    typed: Dict[str, Any] = {}
    if status is not None:
        # status must go through the $in operator — plain equality is
        # ignored by the endpoint (grammar mirrored from the Atlan UI)
        typed["status"] = {"$in": [AtlanRequestStatus(status).value]}
    if request_type is not None:
        typed["requestType"] = {"$in": [AtlanRequestType(request_type).value]}
    if destination_guid is not None:
        typed["destinationGuid"] = destination_guid
    if destination_qualified_name is not None:
        typed["destinationQualifiedName"] = destination_qualified_name
    if entity_type is not None:
        typed["entityType"] = entity_type
    if created_by is not None:
        typed["createdBy"] = created_by
    if post_filter is not None:
        if typed:
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "post_filter", "raw filter cannot be combined with typed filters"
            )
        return post_filter
    if not typed:
        return None
    # Same shape the Atlan UI sends: AND of the duplicate-exclusion clause
    # and the typed conditions.
    return json.dumps({"$and": [{"isDuplicate": False}, typed]})


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
    approved_by: Optional[Union[str, List[str]]] = Field(
        default=None,
        description=(
            "User(s) who approved the request — a list when the request "
            "has multiple approvers."
        ),
    )
    rejected_by: Optional[Union[str, List[str]]] = Field(
        default=None,
        description=(
            "User(s) who rejected the request — a list when the request "
            "has multiple approvers."
        ),
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


class AtlanRequestsCriteria(AtlanObject):
    """Criteria (query parameters) for listing requests, used for paging."""

    post_filter: Optional[str] = Field(
        default=None, description="JSON filter for the list of requests."
    )
    sort: Optional[str] = Field(
        default=None, description="Property by which to sort the results."
    )
    count: bool = Field(
        default=True, description="Whether to include an overall count."
    )
    offset: int = Field(default=0, description="Starting point when paging.")
    limit: int = Field(default=20, description="Maximum requests per page.")

    @property
    def query_params(self) -> dict:
        qp: Dict[str, object] = {}
        if self.post_filter:
            qp["filter"] = self.post_filter
        if self.sort:
            qp["sort"] = self.sort
        qp["count"] = self.count
        qp["offset"] = self.offset
        qp["limit"] = self.limit
        return qp


class AtlanRequestResponse(AtlanObject):
    """Paged response of requests. Iterate it to lazily page through ALL
    matching requests (same pattern as UserResponse / GroupResponse)."""

    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: Any = PrivateAttr()
    _criteria: AtlanRequestsCriteria = PrivateAttr()
    total_record: Optional[int] = Field(
        default=None, description="Total number of requests."
    )
    filter_record: Optional[int] = Field(
        default=None, description="Number of requests matching the filter."
    )
    records: Optional[List[AtlanRequest]] = Field(
        default=None, description="Requests in this page of results."
    )

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._endpoint = data.get("endpoint")  # type: ignore[assignment]
        self._client = data.get("client")
        self._criteria = data.get("criteria")  # type: ignore[assignment]
        self._start = data.get("start") or 0
        self._size = data.get("size") or 20

    def current_page(self) -> Optional[List[AtlanRequest]]:
        return self.records

    def next_page(self, start=None, size=None) -> bool:
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self.records else False

    def _get_next_page(self) -> bool:
        self._criteria.offset = self._start
        self._criteria.limit = self._size
        raw_json = self._client._call_api(
            api=self._endpoint.format_path_with_params(),
            query_params=self._criteria.query_params,
        )
        if not raw_json.get("records"):
            self.records = []
            return False
        try:
            self.records = parse_obj_as(List[AtlanRequest], raw_json.get("records"))
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    def __iter__(self) -> Generator[AtlanRequest, None, None]:  # type: ignore[override]
        while True:
            yield from self.current_page() or []
            if not self.next_page():
                break
