# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    RequestsAction,
    RequestsCreate,
    RequestsGetById,
    RequestsList,
    RequestsListActionable,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.atlan_request import (
    AtlanRequest,
    AtlanRequestResponse,
    AtlanRequestsCriteria,
    build_requests_filter,
)
from pyatlan.model.enums import AtlanRequestStatus, AtlanRequestType


class RequestsClient:
    """
    A client for operating on Atlan requests (the Metadata Inbox):
    listing, retrieving, creating, approving and rejecting them.

    Note: requests are only visible to the identity behind the API token —
    an API key's service account must be an admin (or the designated
    approver) to see and action requests raised for human users.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def list(
        self,
        status: Optional[AtlanRequestStatus] = None,
        request_type: Optional[AtlanRequestType] = None,
        destination_guid: Optional[str] = None,
        destination_qualified_name: Optional[str] = None,
        entity_type: Optional[str] = None,
        created_by: Optional[str] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> AtlanRequestResponse:
        """
        List requests, optionally filtered by typed arguments.
        Iterate the response to lazily page through ALL matches.

        :param status: only requests with this status (AtlanRequestStatus, e.g. ACTIVE)
        :param request_type: only this type (AtlanRequestType, e.g. ATTRIBUTE, ATLAN_TAG)
        :param destination_guid: only requests against this asset GUID
        :param destination_qualified_name: only requests against this qualified name
        :param entity_type: only requests against this asset type
        :param created_by: only requests raised by this user
        :param post_filter: raw JSON filter (escape hatch — cannot be combined with the typed filters above)
        :param sort: property by which to sort the results, e.g. `-createdAt`
        :param count: whether to include the total number of records
        :param offset: starting point for results, for paging
        :param limit: maximum number of results per page
        :raises AtlanError: on any error during API invocation.
        :returns: a lazily-pageable response of requests
        """
        criteria = AtlanRequestsCriteria(
            post_filter=build_requests_filter(
                status=status,
                request_type=request_type,
                destination_guid=destination_guid,
                destination_qualified_name=destination_qualified_name,
                entity_type=entity_type,
                created_by=created_by,
                post_filter=post_filter,
            ),
            sort=sort,
            count=count,
            offset=offset,
            limit=limit,
        )
        endpoint, query_params = RequestsList.prepare_request(criteria)
        raw_json = self._client._call_api(endpoint, query_params)
        return AtlanRequestResponse(
            client=self._client,
            endpoint=RequestsList.ENDPOINT,
            criteria=criteria,
            start=offset,
            size=limit,
            **raw_json,
        )

    @validate_arguments
    def list_actionable(
        self,
        status: Optional[AtlanRequestStatus] = None,
        request_type: Optional[AtlanRequestType] = None,
        destination_guid: Optional[str] = None,
        destination_qualified_name: Optional[str] = None,
        entity_type: Optional[str] = None,
        created_by: Optional[str] = None,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> AtlanRequestResponse:
        """
        List requests the current identity can approve or reject.
        Iterate the response to lazily page through ALL matches.

        :param status: only requests with this status (AtlanRequestStatus, e.g. ACTIVE)
        :param request_type: only this type (AtlanRequestType, e.g. ATTRIBUTE, ATLAN_TAG)
        :param destination_guid: only requests against this asset GUID
        :param destination_qualified_name: only requests against this qualified name
        :param entity_type: only requests against this asset type
        :param created_by: only requests raised by this user
        :param post_filter: raw JSON filter (escape hatch — cannot be combined with the typed filters above)
        :param sort: property by which to sort the results, e.g. `-createdAt`
        :param count: whether to include the total number of records
        :param offset: starting point for results, for paging
        :param limit: maximum number of results per page
        :raises AtlanError: on any error during API invocation.
        :returns: a lazily-pageable response of requests
        """
        criteria = AtlanRequestsCriteria(
            post_filter=build_requests_filter(
                status=status,
                request_type=request_type,
                destination_guid=destination_guid,
                destination_qualified_name=destination_qualified_name,
                entity_type=entity_type,
                created_by=created_by,
                post_filter=post_filter,
            ),
            sort=sort,
            count=count,
            offset=offset,
            limit=limit,
        )
        endpoint, query_params = RequestsListActionable.prepare_request(criteria)
        raw_json = self._client._call_api(endpoint, query_params)
        return AtlanRequestResponse(
            client=self._client,
            endpoint=RequestsListActionable.ENDPOINT,
            criteria=criteria,
            start=offset,
            size=limit,
            **raw_json,
        )

    @validate_arguments
    def get(self, guid: str) -> Optional[AtlanRequest]:
        """
        Retrieve a single request by its GUID.

        :param guid: unique identifier of the request
        :raises AtlanError: on any error during API invocation.
        :returns: the request, or None if it does not exist
        """
        endpoint = RequestsGetById.prepare_request(guid)
        raw_json = self._client._call_api(endpoint)
        return RequestsGetById.process_response(raw_json)

    def create(self, request: AtlanRequest) -> Optional[AtlanRequest]:
        """
        Create (raise) a new request.

        :param request: the request to create, e.g. via AttributeRequest.creator()
        :raises AtlanError: on any error during API invocation.
        :returns: the created request, including its server-assigned id
        """
        endpoint, request_obj = RequestsCreate.prepare_request(request)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return RequestsCreate.process_response(raw_json)

    @validate_arguments
    def approve(self, guid: str, message: Optional[str] = None) -> bool:
        """
        Approve a request. Approval applies the requested change.

        :param guid: unique identifier of the request to approve
        :param message: optional message to include with the approval
        :raises AtlanError: on any error during API invocation.
        :returns: True if the request was approved
        """
        endpoint, request_obj = RequestsAction.prepare_request(
            guid, "approved", message
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return RequestsAction.process_response(raw_json)

    @validate_arguments
    def reject(self, guid: str, message: Optional[str] = None) -> bool:
        """
        Reject a request.

        :param guid: unique identifier of the request to reject
        :param message: optional message to include with the rejection
        :raises AtlanError: on any error during API invocation.
        :returns: True if the request was rejected
        """
        endpoint, request_obj = RequestsAction.prepare_request(
            guid, "rejected", message
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return RequestsAction.process_response(raw_json)
