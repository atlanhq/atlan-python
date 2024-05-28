# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import WorkflowRunStatus, WorkflowRunType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .asset import Asset


class WorkflowRun(Asset, type_name="WorkflowRun"):
    """Description"""

    type_name: str = Field(default="WorkflowRun", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "WorkflowRun":
            raise ValueError("must be WorkflowRun")
        return v

    def __setattr__(self, name, value):
        if name in WorkflowRun._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKFLOW_RUN_WORKFLOW_GUID: ClassVar[KeywordField] = KeywordField(
        "workflowRunWorkflowGuid", "workflowRunWorkflowGuid"
    )
    """
    GUID of the workflow from which this run was created.
    """
    WORKFLOW_RUN_TYPE: ClassVar[KeywordField] = KeywordField(
        "workflowRunType", "workflowRunType"
    )
    """
    Type of the workflow from which this run was created.
    """
    WORKFLOW_RUN_ON_ASSET_GUID: ClassVar[KeywordField] = KeywordField(
        "workflowRunOnAssetGuid", "workflowRunOnAssetGuid"
    )
    """
    The asset for which this run was created.
    """
    WORKFLOW_RUN_COMMENT: ClassVar[KeywordField] = KeywordField(
        "workflowRunComment", "workflowRunComment"
    )
    """
    The comment added by the requester
    """
    WORKFLOW_RUN_CONFIG: ClassVar[KeywordField] = KeywordField(
        "workflowRunConfig", "workflowRunConfig"
    )
    """
    Details of the approval workflow run.
    """
    WORKFLOW_RUN_STATUS: ClassVar[KeywordField] = KeywordField(
        "workflowRunStatus", "workflowRunStatus"
    )
    """
    Status of the run.
    """
    WORKFLOW_RUN_EXPIRES_AT: ClassVar[NumericField] = NumericField(
        "workflowRunExpiresAt", "workflowRunExpiresAt"
    )
    """
    Time at which this run will expire.
    """
    WORKFLOW_RUN_CREATED_BY: ClassVar[KeywordField] = KeywordField(
        "workflowRunCreatedBy", "workflowRunCreatedBy"
    )
    """
    Username of the user who created this workflow run.
    """
    WORKFLOW_RUN_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "workflowRunUpdatedBy", "workflowRunUpdatedBy"
    )
    """
    Username of the user who updated this workflow run.
    """
    WORKFLOW_RUN_DELETED_AT: ClassVar[NumericField] = NumericField(
        "workflowRunDeletedAt", "workflowRunDeletedAt"
    )
    """
    Deletion time of this workflow run.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workflow_run_workflow_guid",
        "workflow_run_type",
        "workflow_run_on_asset_guid",
        "workflow_run_comment",
        "workflow_run_config",
        "workflow_run_status",
        "workflow_run_expires_at",
        "workflow_run_created_by",
        "workflow_run_updated_by",
        "workflow_run_deleted_at",
    ]

    @property
    def workflow_run_workflow_guid(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workflow_run_workflow_guid
        )

    @workflow_run_workflow_guid.setter
    def workflow_run_workflow_guid(self, workflow_run_workflow_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_workflow_guid = workflow_run_workflow_guid

    @property
    def workflow_run_type(self) -> Optional[WorkflowRunType]:
        return None if self.attributes is None else self.attributes.workflow_run_type

    @workflow_run_type.setter
    def workflow_run_type(self, workflow_run_type: Optional[WorkflowRunType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_type = workflow_run_type

    @property
    def workflow_run_on_asset_guid(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.workflow_run_on_asset_guid
        )

    @workflow_run_on_asset_guid.setter
    def workflow_run_on_asset_guid(self, workflow_run_on_asset_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_on_asset_guid = workflow_run_on_asset_guid

    @property
    def workflow_run_comment(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.workflow_run_comment

    @workflow_run_comment.setter
    def workflow_run_comment(self, workflow_run_comment: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_comment = workflow_run_comment

    @property
    def workflow_run_config(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.workflow_run_config

    @workflow_run_config.setter
    def workflow_run_config(self, workflow_run_config: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_config = workflow_run_config

    @property
    def workflow_run_status(self) -> Optional[WorkflowRunStatus]:
        return None if self.attributes is None else self.attributes.workflow_run_status

    @workflow_run_status.setter
    def workflow_run_status(self, workflow_run_status: Optional[WorkflowRunStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_status = workflow_run_status

    @property
    def workflow_run_expires_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.workflow_run_expires_at
        )

    @workflow_run_expires_at.setter
    def workflow_run_expires_at(self, workflow_run_expires_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_expires_at = workflow_run_expires_at

    @property
    def workflow_run_created_by(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workflow_run_created_by
        )

    @workflow_run_created_by.setter
    def workflow_run_created_by(self, workflow_run_created_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_created_by = workflow_run_created_by

    @property
    def workflow_run_updated_by(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workflow_run_updated_by
        )

    @workflow_run_updated_by.setter
    def workflow_run_updated_by(self, workflow_run_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_updated_by = workflow_run_updated_by

    @property
    def workflow_run_deleted_at(self) -> Optional[datetime]:
        return (
            None if self.attributes is None else self.attributes.workflow_run_deleted_at
        )

    @workflow_run_deleted_at.setter
    def workflow_run_deleted_at(self, workflow_run_deleted_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_deleted_at = workflow_run_deleted_at

    class Attributes(Asset.Attributes):
        workflow_run_workflow_guid: Optional[str] = Field(default=None, description="")
        workflow_run_type: Optional[WorkflowRunType] = Field(
            default=None, description=""
        )
        workflow_run_on_asset_guid: Optional[str] = Field(default=None, description="")
        workflow_run_comment: Optional[str] = Field(default=None, description="")
        workflow_run_config: Optional[str] = Field(default=None, description="")
        workflow_run_status: Optional[WorkflowRunStatus] = Field(
            default=None, description=""
        )
        workflow_run_expires_at: Optional[datetime] = Field(
            default=None, description=""
        )
        workflow_run_created_by: Optional[str] = Field(default=None, description="")
        workflow_run_updated_by: Optional[str] = Field(default=None, description="")
        workflow_run_deleted_at: Optional[datetime] = Field(
            default=None, description=""
        )

    attributes: WorkflowRun.Attributes = Field(
        default_factory=lambda: WorkflowRun.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
