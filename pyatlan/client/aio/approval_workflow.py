# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApprovalWorkflowBulkActionRequests,
    ApprovalWorkflowGetRequest,
    AsyncApiCaller,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import ApprovalWorkflowRequestType
from pyatlan.model.approval_workflow import (
    ApprovalWorkflowBulkActionResponse,
    ApprovalWorkflowRequest,
)


class AsyncApprovalWorkflowClient:
    """
    Async client for the governance-workflow approval system (the newer
    Inbox). For the classic Requests module use `client.requests` instead —
    tenants can have both.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def get(self, guid: str) -> Optional[ApprovalWorkflowRequest]:
        """
        Retrieve one approval-workflow request by its GUID.

        :param guid: unique identifier of the workflow request
        :raises AtlanError: on any error during API invocation.
        :returns: the workflow request, or None if it does not exist
        """
        endpoint = ApprovalWorkflowGetRequest.prepare_request(guid)
        raw_json = await self._client._call_api(endpoint)
        return ApprovalWorkflowGetRequest.process_response(raw_json)

    @validate_arguments
    async def approve_all(
        self,
        group_key: str,
        sub_type: Optional[ApprovalWorkflowRequestType] = None,
        comment: Optional[str] = None,
    ) -> ApprovalWorkflowBulkActionResponse:
        """Bulk-approve all pending workflow tasks in a group."""
        endpoint, request_obj = ApprovalWorkflowBulkActionRequests.prepare_request(
            group_key, "APPROVED", sub_type, comment
        )
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return ApprovalWorkflowBulkActionRequests.process_response(raw_json)

    @validate_arguments
    async def reject_all(
        self,
        group_key: str,
        sub_type: Optional[ApprovalWorkflowRequestType] = None,
        comment: Optional[str] = None,
    ) -> ApprovalWorkflowBulkActionResponse:
        """Bulk-reject all pending workflow tasks in a group."""
        endpoint, request_obj = ApprovalWorkflowBulkActionRequests.prepare_request(
            group_key, "REJECTED", sub_type, comment
        )
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return ApprovalWorkflowBulkActionRequests.process_response(raw_json)
