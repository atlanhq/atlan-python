# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from datetime import datetime
from typing import ClassVar, Dict, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AppWorkflowRunStatus
from pyatlan.model.fields.atlan_fields import (
    BooleanField,
    KeywordField,
    NumericField,
    RelationField,
    TextField,
)
from pyatlan.model.structs import AppWorkflowRunStep, AtlanAppErrorHandling

from .catalog import Catalog


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
    APP_WORKFLOW_RUN_STARTED_BY: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunStartedBy", "appWorkflowRunStartedBy"
    )
    """
    Username of the user who started the workflow run.
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
    APP_WORKFLOW_RUN_APP_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunAppQualifiedName", "appWorkflowRunAppQualifiedName"
    )
    """
    Qualified name of the application this workflow run belongs to.
    """
    APP_WORKFLOW_RUN_APP_NAME: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunAppName", "appWorkflowRunAppName"
    )
    """
    Name of the application this workflow run belongs to.
    """
    APP_WORKFLOW_RUN_APP_WORKFLOW_QUALIFIED_NAME: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunAppWorkflowQualifiedName",
        "appWorkflowRunAppWorkflowQualifiedName",
    )
    """
    Qualified name of the parent workflow.
    """
    APP_WORKFLOW_RUN_APP_WORKFLOW_NAME: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunAppWorkflowName", "appWorkflowRunAppWorkflowName"
    )
    """
    Name of the parent workflow.
    """
    APP_WORKFLOW_RUN_APP_WORKFLOW_SLUG: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunAppWorkflowSlug", "appWorkflowRunAppWorkflowSlug"
    )
    """
    Slug of the parent workflow.
    """
    APP_WORKFLOW_RUN_APP_WORKFLOW_VERSION: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunAppWorkflowVersion", "appWorkflowRunAppWorkflowVersion"
    )
    """
    Version of the parent workflow.
    """
    APP_WORKFLOW_RUN_TEMPORAL_RUN_ID: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunTemporalRunId", "appWorkflowRunTemporalRunId"
    )
    """
    Unique identifier for the temporal run associated with this workflow execution.
    """
    APP_WORKFLOW_RUN_IS_TEST_RUN: ClassVar[BooleanField] = BooleanField(
        "appWorkflowRunIsTestRun", "appWorkflowRunIsTestRun"
    )
    """
    Whether the workflow run is a test run.
    """
    APP_WORKFLOW_RUN_DAG: ClassVar[TextField] = TextField(
        "appWorkflowRunDag", "appWorkflowRunDag"
    )
    """
    Map of all activity steps for the workflow run (escaped JSON string).
    """
    APP_WORKFLOW_RUN_ERROR_HANDLING: ClassVar[KeywordField] = KeywordField(
        "appWorkflowRunErrorHandling", "appWorkflowRunErrorHandling"
    )
    """
    Error handling strategy for the workflow run.
    """

    ATLAN_APP_WORKFLOW: ClassVar[RelationField] = RelationField("atlanAppWorkflow")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "app_workflow_run_label",
        "app_workflow_run_status",
        "app_workflow_run_started_at",
        "app_workflow_run_started_by",
        "app_workflow_run_completed_at",
        "app_workflow_run_outputs",
        "app_workflow_run_steps",
        "app_workflow_run_app_qualified_name",
        "app_workflow_run_app_name",
        "app_workflow_run_app_workflow_qualified_name",
        "app_workflow_run_app_workflow_name",
        "app_workflow_run_app_workflow_slug",
        "app_workflow_run_app_workflow_version",
        "app_workflow_run_temporal_run_id",
        "app_workflow_run_is_test_run",
        "app_workflow_run_dag",
        "app_workflow_run_error_handling",
        "atlan_app_workflow",
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
    def app_workflow_run_started_by(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_started_by
        )

    @app_workflow_run_started_by.setter
    def app_workflow_run_started_by(self, app_workflow_run_started_by: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_started_by = app_workflow_run_started_by

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

    @property
    def app_workflow_run_app_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_app_qualified_name
        )

    @app_workflow_run_app_qualified_name.setter
    def app_workflow_run_app_qualified_name(
        self, app_workflow_run_app_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_app_qualified_name = (
            app_workflow_run_app_qualified_name
        )

    @property
    def app_workflow_run_app_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_app_name
        )

    @app_workflow_run_app_name.setter
    def app_workflow_run_app_name(self, app_workflow_run_app_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_app_name = app_workflow_run_app_name

    @property
    def app_workflow_run_app_workflow_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_app_workflow_qualified_name
        )

    @app_workflow_run_app_workflow_qualified_name.setter
    def app_workflow_run_app_workflow_qualified_name(
        self, app_workflow_run_app_workflow_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_app_workflow_qualified_name = (
            app_workflow_run_app_workflow_qualified_name
        )

    @property
    def app_workflow_run_app_workflow_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_app_workflow_name
        )

    @app_workflow_run_app_workflow_name.setter
    def app_workflow_run_app_workflow_name(
        self, app_workflow_run_app_workflow_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_app_workflow_name = (
            app_workflow_run_app_workflow_name
        )

    @property
    def app_workflow_run_app_workflow_slug(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_app_workflow_slug
        )

    @app_workflow_run_app_workflow_slug.setter
    def app_workflow_run_app_workflow_slug(
        self, app_workflow_run_app_workflow_slug: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_app_workflow_slug = (
            app_workflow_run_app_workflow_slug
        )

    @property
    def app_workflow_run_app_workflow_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_app_workflow_version
        )

    @app_workflow_run_app_workflow_version.setter
    def app_workflow_run_app_workflow_version(
        self, app_workflow_run_app_workflow_version: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_app_workflow_version = (
            app_workflow_run_app_workflow_version
        )

    @property
    def app_workflow_run_temporal_run_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_temporal_run_id
        )

    @app_workflow_run_temporal_run_id.setter
    def app_workflow_run_temporal_run_id(
        self, app_workflow_run_temporal_run_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_temporal_run_id = (
            app_workflow_run_temporal_run_id
        )

    @property
    def app_workflow_run_is_test_run(self) -> Optional[bool]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_is_test_run
        )

    @app_workflow_run_is_test_run.setter
    def app_workflow_run_is_test_run(
        self, app_workflow_run_is_test_run: Optional[bool]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_is_test_run = app_workflow_run_is_test_run

    @property
    def app_workflow_run_dag(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.app_workflow_run_dag

    @app_workflow_run_dag.setter
    def app_workflow_run_dag(self, app_workflow_run_dag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_dag = app_workflow_run_dag

    @property
    def app_workflow_run_error_handling(self) -> Optional[AtlanAppErrorHandling]:
        return (
            None
            if self.attributes is None
            else self.attributes.app_workflow_run_error_handling
        )

    @app_workflow_run_error_handling.setter
    def app_workflow_run_error_handling(
        self, app_workflow_run_error_handling: Optional[AtlanAppErrorHandling]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.app_workflow_run_error_handling = (
            app_workflow_run_error_handling
        )

    @property
    def atlan_app_workflow(self) -> Optional[AtlanAppWorkflow]:
        return None if self.attributes is None else self.attributes.atlan_app_workflow

    @atlan_app_workflow.setter
    def atlan_app_workflow(self, atlan_app_workflow: Optional[AtlanAppWorkflow]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow = atlan_app_workflow

    class Attributes(Catalog.Attributes):
        app_workflow_run_label: Optional[str] = Field(default=None, description="")
        app_workflow_run_status: Optional[AppWorkflowRunStatus] = Field(
            default=None, description=""
        )
        app_workflow_run_started_at: Optional[datetime] = Field(
            default=None, description=""
        )
        app_workflow_run_started_by: Optional[str] = Field(default=None, description="")
        app_workflow_run_completed_at: Optional[datetime] = Field(
            default=None, description=""
        )
        app_workflow_run_outputs: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        app_workflow_run_steps: Optional[List[AppWorkflowRunStep]] = Field(
            default=None, description=""
        )
        app_workflow_run_app_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        app_workflow_run_app_name: Optional[str] = Field(default=None, description="")
        app_workflow_run_app_workflow_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        app_workflow_run_app_workflow_name: Optional[str] = Field(
            default=None, description=""
        )
        app_workflow_run_app_workflow_slug: Optional[str] = Field(
            default=None, description=""
        )
        app_workflow_run_app_workflow_version: Optional[str] = Field(
            default=None, description=""
        )
        app_workflow_run_temporal_run_id: Optional[str] = Field(
            default=None, description=""
        )
        app_workflow_run_is_test_run: Optional[bool] = Field(
            default=None, description=""
        )
        app_workflow_run_dag: Optional[str] = Field(default=None, description="")
        app_workflow_run_error_handling: Optional[AtlanAppErrorHandling] = Field(
            default=None, description=""
        )
        atlan_app_workflow: Optional[AtlanAppWorkflow] = Field(
            default=None, description=""
        )  # relationship

    attributes: AppWorkflowRun.Attributes = Field(
        default_factory=lambda: AppWorkflowRun.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .atlan_app_workflow import AtlanAppWorkflow  # noqa: E402, F401
