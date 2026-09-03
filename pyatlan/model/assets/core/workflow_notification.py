# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import WorkflowNotificationAction
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)

from .notification import Notification


class WorkflowNotification(Notification):
    """Description"""

    type_name: str = Field(default="WorkflowNotification", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "WorkflowNotification":
            raise ValueError("must be WorkflowNotification")
        return v

    def __setattr__(self, name, value):
        if name in WorkflowNotification._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKFLOW_NOTIFICATION_WORKFLOW_SLUG: ClassVar[KeywordField] = KeywordField(
        "workflowNotificationWorkflowSlug", "workflowNotificationWorkflowSlug"
    )
    """
    Slug of the workflow this notification is about. What grouping by workflow groups on, and how a check finds the live notification before deciding whether to raise another.
    """  # noqa: E501
    WORKFLOW_NOTIFICATION_LAST_PREFLIGHT_RESULT: ClassVar[TextField] = TextField(
        "workflowNotificationLastPreflightResult",
        "workflowNotificationLastPreflightResult",
    )
    """
    The whole check response as one escaped JSON string, rewritten on every check while the notification is live. Rendered by the widget the interface already has, so nothing is denormalised into attributes.
    """  # noqa: E501
    WORKFLOW_NOTIFICATION_PREFLIGHT_FAILURE_COUNT: ClassVar[NumericField] = (
        NumericField(
            "workflowNotificationPreflightFailureCount",
            "workflowNotificationPreflightFailureCount",
        )
    )
    """
    How many times the check has failed for this notification, counted from the failures that raised it and incremented on every failure since.
    """  # noqa: E501
    WORKFLOW_NOTIFICATION_LAST_PREFLIGHT_FAILED_AT: ClassVar[NumericField] = (
        NumericField(
            "workflowNotificationLastPreflightFailedAt",
            "workflowNotificationLastPreflightFailedAt",
        )
    )
    """
    When the check last failed. Distinct from when it was last checked, which every write already records.
    """
    WORKFLOW_NOTIFICATION_ACTION: ClassVar[KeywordField] = KeywordField(
        "workflowNotificationAction", "workflowNotificationAction"
    )
    """
    Which option the person took. Declared here rather than on the notification supertype because these values only mean anything for a workflow.
    """  # noqa: E501

    WORKFLOW_NOTIFICATION_WORKFLOW: ClassVar[RelationField] = RelationField(
        "workflowNotificationWorkflow"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workflow_notification_workflow_slug",
        "workflow_notification_last_preflight_result",
        "workflow_notification_preflight_failure_count",
        "workflow_notification_last_preflight_failed_at",
        "workflow_notification_action",
        "workflow_notification_workflow",
    ]

    @property
    def workflow_notification_workflow_slug(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workflow_notification_workflow_slug
        )

    @workflow_notification_workflow_slug.setter
    def workflow_notification_workflow_slug(
        self, workflow_notification_workflow_slug: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_notification_workflow_slug = (
            workflow_notification_workflow_slug
        )

    @property
    def workflow_notification_last_preflight_result(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workflow_notification_last_preflight_result
        )

    @workflow_notification_last_preflight_result.setter
    def workflow_notification_last_preflight_result(
        self, workflow_notification_last_preflight_result: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_notification_last_preflight_result = (
            workflow_notification_last_preflight_result
        )

    @property
    def workflow_notification_preflight_failure_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.workflow_notification_preflight_failure_count
        )

    @workflow_notification_preflight_failure_count.setter
    def workflow_notification_preflight_failure_count(
        self, workflow_notification_preflight_failure_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_notification_preflight_failure_count = (
            workflow_notification_preflight_failure_count
        )

    @property
    def workflow_notification_last_preflight_failed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.workflow_notification_last_preflight_failed_at
        )

    @workflow_notification_last_preflight_failed_at.setter
    def workflow_notification_last_preflight_failed_at(
        self, workflow_notification_last_preflight_failed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_notification_last_preflight_failed_at = (
            workflow_notification_last_preflight_failed_at
        )

    @property
    def workflow_notification_action(self) -> Optional[WorkflowNotificationAction]:
        return (
            None
            if self.attributes is None
            else self.attributes.workflow_notification_action
        )

    @workflow_notification_action.setter
    def workflow_notification_action(
        self, workflow_notification_action: Optional[WorkflowNotificationAction]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_notification_action = workflow_notification_action

    @property
    def workflow_notification_workflow(self) -> Optional[AtlanAppWorkflow]:
        return (
            None
            if self.attributes is None
            else self.attributes.workflow_notification_workflow
        )

    @workflow_notification_workflow.setter
    def workflow_notification_workflow(
        self, workflow_notification_workflow: Optional[AtlanAppWorkflow]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_notification_workflow = workflow_notification_workflow

    class Attributes(Notification.Attributes):
        workflow_notification_workflow_slug: Optional[str] = Field(
            default=None, description=""
        )
        workflow_notification_last_preflight_result: Optional[str] = Field(
            default=None, description=""
        )
        workflow_notification_preflight_failure_count: Optional[int] = Field(
            default=None, description=""
        )
        workflow_notification_last_preflight_failed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        workflow_notification_action: Optional[WorkflowNotificationAction] = Field(
            default=None, description=""
        )
        workflow_notification_workflow: Optional[AtlanAppWorkflow] = Field(
            default=None, description=""
        )  # relationship

    attributes: WorkflowNotification.Attributes = Field(
        default_factory=lambda: WorkflowNotification.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlan_app_workflow import AtlanAppWorkflow  # noqa: E402, F401
