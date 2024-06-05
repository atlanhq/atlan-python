# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import BooleanField, KeywordField, NumericField
from pyatlan.model.structs import Action

from .asset import Asset


class Task(Asset, type_name="Task"):
    """Description"""

    type_name: str = Field(default="Task", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Task":
            raise ValueError("must be Task")
        return v

    def __setattr__(self, name, value):
        if name in Task._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    TASK_RECIPIENT: ClassVar[KeywordField] = KeywordField(
        "taskRecipient", "taskRecipient"
    )
    """
    recipient of the task
    """
    TASK_TYPE: ClassVar[KeywordField] = KeywordField("taskType", "taskType")
    """
    type of task
    """
    TASK_REQUESTOR: ClassVar[KeywordField] = KeywordField(
        "taskRequestor", "taskRequestor"
    )
    """
    requestor of the task
    """
    TASK_IS_READ: ClassVar[BooleanField] = BooleanField("taskIsRead", "taskIsRead")
    """
    flag to make task read/unread
    """
    TASK_REQUESTOR_COMMENT: ClassVar[KeywordField] = KeywordField(
        "taskRequestorComment", "taskRequestorComment"
    )
    """
    comment of requestor for the task
    """
    TASK_RELATED_ASSET_GUID: ClassVar[KeywordField] = KeywordField(
        "taskRelatedAssetGuid", "taskRelatedAssetGuid"
    )
    """
    assetId to preview
    """
    TASK_PROPOSALS: ClassVar[KeywordField] = KeywordField(
        "taskProposals", "taskProposals"
    )
    """
    contains the payload that is proposed to the task
    """
    TASK_EXPIRES_AT: ClassVar[NumericField] = NumericField(
        "taskExpiresAt", "taskExpiresAt"
    )
    """
    Time (epoch) at which the task expires .
    """
    TASK_ACTIONS: ClassVar[KeywordField] = KeywordField("taskActions", "taskActions")
    """
    List of actions associated with this task.
    """
    TASK_EXECUTION_COMMENT: ClassVar[KeywordField] = KeywordField(
        "taskExecutionComment", "taskExecutionComment"
    )
    """
    comment for the action executed by user
    """
    TASK_EXECUTION_ACTION: ClassVar[KeywordField] = KeywordField(
        "taskExecutionAction", "taskExecutionAction"
    )
    """
    action executed by the recipient
    """
    TASK_CREATED_BY: ClassVar[KeywordField] = KeywordField(
        "taskCreatedBy", "taskCreatedBy"
    )
    """
    username of the user who created this task
    """
    TASK_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "taskUpdatedBy", "taskUpdatedBy"
    )
    """
    username of the user who updated this task
    """

    _convenience_properties: ClassVar[List[str]] = [
        "task_recipient",
        "task_type",
        "task_requestor",
        "task_is_read",
        "task_requestor_comment",
        "task_related_asset_guid",
        "task_proposals",
        "task_expires_at",
        "task_actions",
        "task_execution_comment",
        "task_execution_action",
        "task_created_by",
        "task_updated_by",
    ]

    @property
    def task_recipient(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.task_recipient

    @task_recipient.setter
    def task_recipient(self, task_recipient: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_recipient = task_recipient

    @property
    def task_type(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.task_type

    @task_type.setter
    def task_type(self, task_type: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_type = task_type

    @property
    def task_requestor(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.task_requestor

    @task_requestor.setter
    def task_requestor(self, task_requestor: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_requestor = task_requestor

    @property
    def task_is_read(self) -> Optional[bool]:
        return None if self.attributes is None else self.attributes.task_is_read

    @task_is_read.setter
    def task_is_read(self, task_is_read: Optional[bool]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_is_read = task_is_read

    @property
    def task_requestor_comment(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.task_requestor_comment
        )

    @task_requestor_comment.setter
    def task_requestor_comment(self, task_requestor_comment: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_requestor_comment = task_requestor_comment

    @property
    def task_related_asset_guid(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.task_related_asset_guid
        )

    @task_related_asset_guid.setter
    def task_related_asset_guid(self, task_related_asset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_related_asset_guid = task_related_asset_guid

    @property
    def task_proposals(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.task_proposals

    @task_proposals.setter
    def task_proposals(self, task_proposals: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_proposals = task_proposals

    @property
    def task_expires_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.task_expires_at

    @task_expires_at.setter
    def task_expires_at(self, task_expires_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_expires_at = task_expires_at

    @property
    def task_actions(self) -> Optional[List[Action]]:
        return None if self.attributes is None else self.attributes.task_actions

    @task_actions.setter
    def task_actions(self, task_actions: Optional[List[Action]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_actions = task_actions

    @property
    def task_execution_comment(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.task_execution_comment
        )

    @task_execution_comment.setter
    def task_execution_comment(self, task_execution_comment: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_execution_comment = task_execution_comment

    @property
    def task_execution_action(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.task_execution_action
        )

    @task_execution_action.setter
    def task_execution_action(self, task_execution_action: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_execution_action = task_execution_action

    @property
    def task_created_by(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.task_created_by

    @task_created_by.setter
    def task_created_by(self, task_created_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_created_by = task_created_by

    @property
    def task_updated_by(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.task_updated_by

    @task_updated_by.setter
    def task_updated_by(self, task_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.task_updated_by = task_updated_by

    class Attributes(Asset.Attributes):
        task_recipient: Optional[str] = Field(default=None, description="")
        task_type: Optional[str] = Field(default=None, description="")
        task_requestor: Optional[str] = Field(default=None, description="")
        task_is_read: Optional[bool] = Field(default=None, description="")
        task_requestor_comment: Optional[str] = Field(default=None, description="")
        task_related_asset_guid: Optional[str] = Field(default=None, description="")
        task_proposals: Optional[str] = Field(default=None, description="")
        task_expires_at: Optional[datetime] = Field(default=None, description="")
        task_actions: Optional[List[Action]] = Field(default=None, description="")
        task_execution_comment: Optional[str] = Field(default=None, description="")
        task_execution_action: Optional[str] = Field(default=None, description="")
        task_created_by: Optional[str] = Field(default=None, description="")
        task_updated_by: Optional[str] = Field(default=None, description="")

    attributes: Task.Attributes = Field(
        default_factory=lambda: Task.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
