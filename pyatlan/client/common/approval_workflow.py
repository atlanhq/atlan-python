# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Optional

from pyatlan.client.constants import (
    BULK_ACTION_APPROVAL_WORKFLOW_REQUESTS,
    GET_APPROVAL_WORKFLOW_REQUEST,
)
from pyatlan.model.approval_workflow import (
    ApprovalWorkflowBulkAction,
    ApprovalWorkflowBulkActionResponse,
    ApprovalWorkflowRequest,
)


class ApprovalWorkflowGetRequest:
    """Shared logic for retrieving one approval-workflow request by GUID."""

    @staticmethod
    def prepare_request(guid: str):
        return GET_APPROVAL_WORKFLOW_REQUEST.format_path({"request_guid": guid})

    @staticmethod
    def process_response(raw_json) -> Optional[ApprovalWorkflowRequest]:
        if isinstance(raw_json, list):
            raw_json = raw_json[0] if raw_json else None
        return ApprovalWorkflowRequest(**raw_json) if raw_json else None


class ApprovalWorkflowBulkActionRequests:
    """Shared logic for bulk-approving or bulk-rejecting workflow tasks."""

    @staticmethod
    def prepare_request(
        group_key: str,
        decision: str,
        sub_type: Optional[str] = None,
        comment: Optional[str] = None,
    ) -> tuple:
        body = ApprovalWorkflowBulkAction(group_key=group_key, decision=decision)
        if sub_type is not None:
            body.sub_type = getattr(sub_type, "value", sub_type)
        if comment is not None:
            body.comment = comment
        return BULK_ACTION_APPROVAL_WORKFLOW_REQUESTS.format_path_with_params(), body

    @staticmethod
    def process_response(raw_json) -> ApprovalWorkflowBulkActionResponse:
        if isinstance(raw_json, dict):
            return ApprovalWorkflowBulkActionResponse(**raw_json)
        return ApprovalWorkflowBulkActionResponse(message=str(raw_json))
