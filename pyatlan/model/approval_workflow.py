# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Dict, Optional

from pydantic.v1 import Field

from pyatlan.model.core import AtlanObject


class ApprovalWorkflowObject(AtlanObject):
    """Base for approval-workflow API models: this API family uses snake_case
    on the wire, so the camelCase alias generator is disabled."""

    class Config(AtlanObject.Config):
        alias_generator = staticmethod(  # type: ignore[assignment]
            lambda field_name: field_name
        )


class ApprovalWorkflowRequest(ApprovalWorkflowObject):
    """A governance-workflow approval request (the newer Inbox system,
    enabled by the `Governance Workflows and Inbox` feature)."""

    guid: Optional[str] = Field(default=None, description="Unique identifier.")
    name: Optional[str] = Field(default=None, description="Name of the request.")
    qualified_name: Optional[str] = Field(
        default=None, description="Qualified name of the request."
    )
    description: Optional[str] = Field(
        default=None, description="Description of the request."
    )
    approval_workflow_guid: Optional[str] = Field(
        default=None, description="GUID of the workflow this request instantiates."
    )
    approval_workflow_request_type: Optional[str] = Field(
        default=None,
        description=(
            "Type of the request, e.g. CHANGE_MANAGEMENT, DATA_ACCESS, "
            "PUBLICATION_MANAGEMENT or POLICY_APPROVAL."
        ),
    )
    request_on_asset_guid: Optional[str] = Field(
        default=None, description="GUID of the asset the request was raised on."
    )
    config: Optional[Dict[str, Any]] = Field(
        default=None, description="Configuration of the request."
    )
    status: Optional[str] = Field(default=None, description="Status of the request.")
    expires_at: Optional[str] = Field(
        default=None, description="When the request expires, if it does."
    )
    comment: Optional[str] = Field(
        default=None, description="Comment attached to the request, if any."
    )
    created_by: Optional[str] = Field(
        default=None, description="User who raised the request."
    )
    updated_by: Optional[str] = Field(
        default=None, description="User who last updated the request."
    )
    created_at: Optional[str] = Field(
        default=None, description="When the request was created."
    )
    updated_at: Optional[str] = Field(
        default=None, description="When the request was last updated."
    )
    approval_details: Optional[Any] = Field(
        default=None,
        description=(
            "Details of the approval configuration/stages — wire shape "
            "varies by platform version; kept untyped so every variant parses."
        ),
    )
    action_details: Optional[Any] = Field(
        default=None,
        description=(
            "Details of actions taken on the request — wire shape varies "
            "by platform version; kept untyped so every variant parses."
        ),
    )


class ApprovalWorkflowBulkAction(ApprovalWorkflowObject):
    """Body for bulk-approving or bulk-rejecting workflow tasks."""

    group_key: str = Field(
        description=(
            "Group identifier: the task GUID or the related asset GUID "
            "(taskRelatedAssetGuid) whose pending tasks should be actioned."
        )
    )
    decision: str = Field(description="`APPROVED` or `REJECTED`.")
    sub_type: Optional[str] = Field(
        default=None,
        description=(
            "Optional task sub-type filter: CHANGE_MANAGEMENT, DATA_ACCESS, "
            "PUBLICATION_MANAGEMENT or POLICY_APPROVAL."
        ),
    )
    comment: Optional[str] = Field(
        default=None, description="Optional comment for the approval/rejection."
    )


class ApprovalWorkflowBulkActionResponse(ApprovalWorkflowObject):
    """Response of a bulk action: tasks are queued for async processing."""

    total_tasks: Optional[int] = Field(
        default=None, description="Number of tasks queued for async processing."
    )
    message: Optional[str] = Field(
        default=None, description="Status message from the server."
    )
