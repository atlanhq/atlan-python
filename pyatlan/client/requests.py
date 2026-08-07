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
from pyatlan.model.atlan_request import AtlanRequest, AtlanRequestResponse


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
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> AtlanRequestResponse:
        """
        List requests, optionally filtered.

        :param post_filter: JSON filter, e.g. '{"status":"active"}'
        :param sort: property by which to sort the results, e.g. '-createdAt'
        :param count: whether to include the total number of records
        :param offset: starting point for results, for paging
        :param limit: maximum number of results per page
        :raises AtlanError: on any error during API invocation.
        :returns: a page of requests
        """
        endpoint, query_params = RequestsList.prepare_request(
            post_filter, sort, count, offset, limit
        )
        raw_json = self._client._call_api(endpoint, query_params)
        return RequestsList.process_response(raw_json)

    @validate_arguments
    def list_actionable(
        self,
        post_filter: Optional[str] = None,
        sort: Optional[str] = None,
        count: bool = True,
        offset: int = 0,
        limit: int = 20,
    ) -> AtlanRequestResponse:
        """
        List requests the current identity can approve or reject.

        :param post_filter: JSON filter, e.g. '{"status":"active"}'
        :param sort: property by which to sort the results, e.g. '-createdAt'
        :param count: whether to include the total number of records
        :param offset: starting point for results, for paging
        :param limit: maximum number of results per page
        :raises AtlanError: on any error during API invocation.
        :returns: a page of actionable requests
        """
        endpoint, query_params = RequestsListActionable.prepare_request(
            post_filter, sort, count, offset, limit
        )
        raw_json = self._client._call_api(endpoint, query_params)
        return RequestsListActionable.process_response(raw_json)

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
