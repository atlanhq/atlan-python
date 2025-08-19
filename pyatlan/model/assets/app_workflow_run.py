# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AppWorkflowRunStatus
from pyatlan.model.fields.atlan_fields import KeywordField, NumericField
from pyatlan.model.structs import AppWorkflowRunStep

from .core.catalog import Catalog


class AppWorkflowRun(Catalog):
    """Description"""

    type_name: str = Field(default="AppWorkflowRun", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AppWorkflowRun":
            raise ValueError("must be AppWorkflowRun")
        return v

    def __setattr__(self, name, value):
        if name in AppWorkflowRun._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    APP_WORKFLOW_RUN_LABEL: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunLabel", "appWorkflowRunLabel"
    )
    """
    Root name for the workflow run.
    """
    APP_WORKFLOW_RUN_STATUS: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunStatus", "appWorkflowRunStatus"
    )
    """
    Overall execution status of the entire workflow run.
    """
    APP_WORKFLOW_RUN_STARTED_AT: ClassVar[NumericField] = NumericField(
        "appWorkflowRunStartedAt", "appWorkflowRunStartedAt"
    )
    """
    Timestamp when the workflow run began execution.
    """
    APP_WORKFLOW_RUN_COMPLETED_AT: ClassVar[NumericField] = NumericField(
        "appWorkflowRunCompletedAt", "appWorkflowRunCompletedAt"
    )
    """
    Timestamp when the workflow run finished execution.
    """
    APP_WORKFLOW_RUN_OUTPUTS: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunOutputs", "appWorkflowRunOutputs"
    )
    """
    Final results produced by the workflow run.
    """
    APP_WORKFLOW_RUN_STEPS: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunSteps", "appWorkflowRunSteps"
    )
    """
    Collection of individual workflow steps in this run.
    """

    _convenience_properties: ClassVar[List[str]] = [
        "app_workflow_run_label",
        "app_workflow_run_status",
        "app_workflow_run_started_at",
        "app_workflow_run_completed_at",
        "app_workflow_run_outputs",
        "app_workflow_run_steps",
    ]

    @property
    def app_workflow_run_label(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.app_workflow_run_label
        )

    @app_workflow_run_label.setter
    def app_workflow_run_label(self, app_workflow_run_label: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_label = app_workflow_run_label

    @property
    def app_workflow_run_status(self) -> Optional[AppWorkflowRunStatus]:
        return (
            None if self.attributes is None else self.attributes.app_workflow_run_status
        )

    @app_workflow_run_status.setter
    def app_workflow_run_status(
        self, app_workflow_run_status: Optional[AppWorkflowRunStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_status = app_workflow_run_status

    @property
    def app_workflow_run_started_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_started_at
        )

    @app_workflow_run_started_at.setter
    def app_workflow_run_started_at(
        self, app_workflow_run_started_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_started_at = app_workflow_run_started_at

    @property
    def app_workflow_run_completed_at(self) -> Optional[datetime]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_completed_at
        )

    @app_workflow_run_completed_at.setter
    def app_workflow_run_completed_at(
        self, app_workflow_run_completed_at: Optional[datetime]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_completed_at = app_workflow_run_completed_at

    @property
    def app_workflow_run_outputs(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_outputs
        )

    @app_workflow_run_outputs.setter
    def app_workflow_run_outputs(
        self, app_workflow_run_outputs: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_outputs = app_workflow_run_outputs

    @property
    def app_workflow_run_steps(self) -> Optional[List[AppWorkflowRunStep]]:
        return (
            None if self.attributes is None else self.attributes.app_workflow_run_steps
        )

    @app_workflow_run_steps.setter
    def app_workflow_run_steps(
        self, app_workflow_run_steps: Optional[List[AppWorkflowRunStep]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_steps = app_workflow_run_steps

    class Attributes(Catalog.Attributes):
        app_workflow_run_label: Optional[str] = Field(default=None, description="")
        app_workflow_run_status: Optional[AppWorkflowRunStatus] = Field(
            default=None, description=""
        )
        app_workflow_run_started_at: Optional[datetime] = Field(
            default=None, description=""
        )
        app_workflow_run_completed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        app_workflow_run_outputs: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        app_workflow_run_steps: Optional[List[AppWorkflowRunStep]] = Field(
            default=None, description=""
        )

    attributes: AppWorkflowRun.Attributes = Field(
        default_factory=lambda: AppWorkflowRun.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


AppWorkflowRun.Attributes.update_forward_refs()
