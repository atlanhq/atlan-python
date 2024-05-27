# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import WorkflowStatus, WorkflowType
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField

from .asset import Asset


class Workflow(Asset, type_name="Workflow"):
    """Description"""

    type_name: str = Field(default="Workflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "Workflow":
            raise ValueError("must be Workflow")
        return v

    def __setattr__(self, name, value):
        if name in Workflow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    WORKFLOW_TEMPLATE_GUID: ClassVar[KeywordField] = KeywordField(
        "workflowTemplateGuid", "workflowTemplateGuid"
    )
    """
    GUID of the workflow template from which this workflow was created.
    """
    WORKFLOW_TYPE: ClassVar[KeywordField] = KeywordField("workflowType", "workflowType")
    """
    Type of the workflow.
    """
    WORKFLOW_CONFIG: ClassVar[KeywordField] = KeywordField(
        "workflowConfig", "workflowConfig"
    )
    """
    Details of the workflow.
    """
    WORKFLOW_STATUS: ClassVar[KeywordField] = KeywordField(
        "workflowStatus", "workflowStatus"
    )
    """
    Status of the workflow.
    """
    WORKFLOW_RUN_EXPIRES_IN: ClassVar[KeywordField] = KeywordField(
        "workflowRunExpiresIn", "workflowRunExpiresIn"
    )
    """
    Time duration after which a run of this workflow will expire.
    """
    WORKFLOW_CREATED_BY: ClassVar[KeywordField] = KeywordField(
        "workflowCreatedBy", "workflowCreatedBy"
    )
    """
    Username of the user who created this workflow.
    """
    WORKFLOW_UPDATED_BY: ClassVar[KeywordField] = KeywordField(
        "workflowUpdatedBy", "workflowUpdatedBy"
    )
    """
    Username of the user who updated this workflow.
    """
    WORKFLOW_DELETED_AT: ClassVar[NumericField] = NumericField(
        "workflowDeletedAt", "workflowDeletedAt"
    )
    """
    Deletion time of this workflow.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "workflow_template_guid",
        "workflow_type",
        "workflow_config",
        "workflow_status",
        "workflow_run_expires_in",
        "workflow_created_by",
        "workflow_updated_by",
        "workflow_deleted_at",
    ]

    @property
    def workflow_template_guid(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workflow_template_guid
        )

    @workflow_template_guid.setter
    def workflow_template_guid(self, workflow_template_guid: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_template_guid = workflow_template_guid

    @property
    def workflow_type(self) -> Optional[WorkflowType]:
        return None if self.attributes is None else self.attributes.workflow_type

    @workflow_type.setter
    def workflow_type(self, workflow_type: Optional[WorkflowType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_type = workflow_type

    @property
    def workflow_config(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.workflow_config

    @workflow_config.setter
    def workflow_config(self, workflow_config: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_config = workflow_config

    @property
    def workflow_status(self) -> Optional[WorkflowStatus]:
        return None if self.attributes is None else self.attributes.workflow_status

    @workflow_status.setter
    def workflow_status(self, workflow_status: Optional[WorkflowStatus]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_status = workflow_status

    @property
    def workflow_run_expires_in(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.workflow_run_expires_in
        )

    @workflow_run_expires_in.setter
    def workflow_run_expires_in(self, workflow_run_expires_in: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_run_expires_in = workflow_run_expires_in

    @property
    def workflow_created_by(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.workflow_created_by

    @workflow_created_by.setter
    def workflow_created_by(self, workflow_created_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_created_by = workflow_created_by

    @property
    def workflow_updated_by(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.workflow_updated_by

    @workflow_updated_by.setter
    def workflow_updated_by(self, workflow_updated_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_updated_by = workflow_updated_by

    @property
    def workflow_deleted_at(self) -> Optional[datetime]:
        return None if self.attributes is None else self.attributes.workflow_deleted_at

    @workflow_deleted_at.setter
    def workflow_deleted_at(self, workflow_deleted_at: Optional[datetime]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.workflow_deleted_at = workflow_deleted_at

    class Attributes(Asset.Attributes):
        workflow_template_guid: Optional[str] = Field(default=None, description="")
        workflow_type: Optional[WorkflowType] = Field(default=None, description="")
        workflow_config: Optional[str] = Field(default=None, description="")
        workflow_status: Optional[WorkflowStatus] = Field(default=None, description="")
        workflow_run_expires_in: Optional[str] = Field(default=None, description="")
        workflow_created_by: Optional[str] = Field(default=None, description="")
        workflow_updated_by: Optional[str] = Field(default=None, description="")
        workflow_deleted_at: Optional[datetime] = Field(default=None, description="")

    attributes: Workflow.Attributes = Field(
        default_factory=lambda: Workflow.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )
