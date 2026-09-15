# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    ApprovalWorkflowBulkActionRequests,
    ApprovalWorkflowGetRequest,
)
from pyatlan.errors import ErrorCode, InvalidRequestError
from pyatlan.model.approval_workflow import (
    ApprovalWorkflowBulkActionResponse,
    ApprovalWorkflowRequest,
)
from pyatlan.model.enums import ApprovalWorkflowRequestType


def _raise_if_recipient_scoped(err: InvalidRequestError, group_key: str):
    """Translate the server's misleading 1003 into an actionable message.

    Bulk actions are RECIPIENT-scoped: the server reports "No pending tasks
    found for the specified group" even when the group visibly has pending
    tasks — whenever none of them are addressed to the calling identity.
    """
    if "No pending tasks found" not in str(err):
        return
    raise ErrorCode.INVALID_REQUEST_PASSTHROUGH.exception_with_parameters(
        "1003",
        (
            f"no actionable pending tasks in group '{group_key}' for the "
            "calling identity. Two common causes: (1) every task in the "
            "group is already actioned (approved/rejected/withdrawn) — "
            "check task_execution_action via a Task search; (2) the pending "
            "tasks are addressed to a different user — bulk approvals are "
            "recipient-scoped, and an admin role does not override this. "
            "To automate approvals, the token's identity must be the "
            "workflow's approver (the workflow builder currently supports "
            "only human users and groups as approvers, so automation may "
            "require a user token)."
        ),
        "",
    ) from err


class ApprovalWorkflowClient:
    """
    A client for the governance-workflow approval system (the newer Inbox,
    enabled via the `Governance Workflows and Inbox` feature). For the classic
    Requests module use `client.requests` instead — tenants can have both.

    Inbox tasks are `Task` assets: list them with FluentSearch on the `Task`
    type, then action them here using the task GUID (or the related asset
    GUID) as the group key.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def get(self, guid: str) -> Optional[ApprovalWorkflowRequest]:
        """
        Retrieve one approval-workflow request by its GUID.

        :param guid: unique identifier of the workflow request
        :raises AtlanError: on any error during API invocation.
        :returns: the workflow request, or None if it does not exist
        """
        endpoint = ApprovalWorkflowGetRequest.prepare_request(guid)
        raw_json = self._client._call_api(endpoint)
        return ApprovalWorkflowGetRequest.process_response(raw_json)

    @validate_arguments
    def approve_all(
        self,
        group_key: str,
        sub_type: Optional[ApprovalWorkflowRequestType] = None,
        comment: Optional[str] = None,
    ) -> ApprovalWorkflowBulkActionResponse:
        """
        Bulk-approve all pending workflow tasks in a group.

        :param group_key: task GUID or related asset GUID whose pending tasks
            should be approved
        :param sub_type: optional filter (CHANGE_MANAGEMENT, DATA_ACCESS,
            PUBLICATION_MANAGEMENT, POLICY_APPROVAL)
        :param comment: optional comment for the approval
        :raises AtlanError: on any error during API invocation.
        :returns: number of tasks queued for (async) processing
        """
        endpoint, request_obj = ApprovalWorkflowBulkActionRequests.prepare_request(
            group_key, "APPROVED", sub_type, comment
        )
        try:
            raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        except InvalidRequestError as err:
            _raise_if_recipient_scoped(err, group_key)
            raise
        return ApprovalWorkflowBulkActionRequests.process_response(raw_json)

    @validate_arguments
    def reject_all(
        self,
        group_key: str,
        sub_type: Optional[ApprovalWorkflowRequestType] = None,
        comment: Optional[str] = None,
    ) -> ApprovalWorkflowBulkActionResponse:
        """
        Bulk-reject all pending workflow tasks in a group.

        :param group_key: task GUID or related asset GUID whose pending tasks
            should be rejected
        :param sub_type: optional filter (CHANGE_MANAGEMENT, DATA_ACCESS,
            PUBLICATION_MANAGEMENT, POLICY_APPROVAL)
        :param comment: optional comment for the rejection
        :raises AtlanError: on any error during API invocation.
        :returns: number of tasks queued for (async) processing
        """
        endpoint, request_obj = ApprovalWorkflowBulkActionRequests.prepare_request(
            group_key, "REJECTED", sub_type, comment
        )
        try:
            raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        except InvalidRequestError as err:
            _raise_if_recipient_scoped(err, group_key)
            raise
        return ApprovalWorkflowBulkActionRequests.process_response(raw_json)
