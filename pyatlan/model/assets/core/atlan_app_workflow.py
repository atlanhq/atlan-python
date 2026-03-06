# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import AtlanAppWorkflowOwnership, AtlanAppWorkflowStatus
from pyatlan.model.fields.atlan_fields import KeywordField, RelationField, TextField
from pyatlan.model.structs import AtlanAppErrorHandling

from .atlan_app import AtlanApp


class AtlanAppWorkflow(AtlanApp):
    """Description"""

    type_name: str = Field(default="AtlanAppWorkflow", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "AtlanAppWorkflow":
            raise ValueError("must be AtlanAppWorkflow")
        return v

    def __setattr__(self, name, value):
        if name in AtlanAppWorkflow._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    ATLAN_APP_WORKFLOW_VERSION: ClassVar[KeywordField] = KeywordField(
        "atlanAppWorkflowVersion", "atlanAppWorkflowVersion"
    )
    """
    Version of the workflow.
    """
    ATLAN_APP_WORKFLOW_SLUG: ClassVar[KeywordField] = KeywordField(
        "atlanAppWorkflowSlug", "atlanAppWorkflowSlug"
    )
    """
    Slug of the workflow.
    """
    ATLAN_APP_WORKFLOW_DAG: ClassVar[TextField] = TextField(
        "atlanAppWorkflowDag", "atlanAppWorkflowDag"
    )
    """
    Map of all activity steps for the workflow (escaped JSON string).
    """
    ATLAN_APP_WORKFLOW_STATUS: ClassVar[KeywordField] = KeywordField(
        "atlanAppWorkflowStatus", "atlanAppWorkflowStatus"
    )
    """
    Status of the workflow.
    """
    ATLAN_APP_WORKFLOW_ERROR_HANDLING: ClassVar[KeywordField] = KeywordField(
        "atlanAppWorkflowErrorHandling", "atlanAppWorkflowErrorHandling"
    )
    """
    Error handling strategy for the workflow.
    """
    ATLAN_APP_WORKFLOW_OWNERSHIP: ClassVar[KeywordField] = KeywordField(
        "atlanAppWorkflowOwnership", "atlanAppWorkflowOwnership"
    )
    """
    Ownership type of the workflow, indicating whether it is managed by Atlan or by a user.
    """
    ATLAN_APP_WORKFLOW_TRIGGERS: ClassVar[TextField] = TextField(
        "atlanAppWorkflowTriggers", "atlanAppWorkflowTriggers"
    )
    """
    Triggers configured for this workflow (escaped JSON string).
    """

    ATLAN_APP: ClassVar[RelationField] = RelationField("atlanApp")
    """
    TBC
    """
    ATLAN_APP_WORKFLOW_RUNS: ClassVar[RelationField] = RelationField(
        "atlanAppWorkflowRuns"
    )
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "atlan_app_workflow_version",
        "atlan_app_workflow_slug",
        "atlan_app_workflow_dag",
        "atlan_app_workflow_status",
        "atlan_app_workflow_error_handling",
        "atlan_app_workflow_ownership",
        "atlan_app_workflow_triggers",
        "atlan_app",
        "atlan_app_workflow_runs",
    ]

    @property
    def atlan_app_workflow_version(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_workflow_version
        )

    @atlan_app_workflow_version.setter
    def atlan_app_workflow_version(self, atlan_app_workflow_version: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow_version = atlan_app_workflow_version

    @property
    def atlan_app_workflow_slug(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.atlan_app_workflow_slug
        )

    @atlan_app_workflow_slug.setter
    def atlan_app_workflow_slug(self, atlan_app_workflow_slug: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow_slug = atlan_app_workflow_slug

    @property
    def atlan_app_workflow_dag(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.atlan_app_workflow_dag
        )

    @atlan_app_workflow_dag.setter
    def atlan_app_workflow_dag(self, atlan_app_workflow_dag: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow_dag = atlan_app_workflow_dag

    @property
    def atlan_app_workflow_status(self) -> Optional[AtlanAppWorkflowStatus]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_workflow_status
        )

    @atlan_app_workflow_status.setter
    def atlan_app_workflow_status(
        self, atlan_app_workflow_status: Optional[AtlanAppWorkflowStatus]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow_status = atlan_app_workflow_status

    @property
    def atlan_app_workflow_error_handling(self) -> Optional[AtlanAppErrorHandling]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_workflow_error_handling
        )

    @atlan_app_workflow_error_handling.setter
    def atlan_app_workflow_error_handling(
        self, atlan_app_workflow_error_handling: Optional[AtlanAppErrorHandling]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow_error_handling = (
            atlan_app_workflow_error_handling
        )

    @property
    def atlan_app_workflow_ownership(self) -> Optional[AtlanAppWorkflowOwnership]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_workflow_ownership
        )

    @atlan_app_workflow_ownership.setter
    def atlan_app_workflow_ownership(
        self, atlan_app_workflow_ownership: Optional[AtlanAppWorkflowOwnership]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow_ownership = atlan_app_workflow_ownership

    @property
    def atlan_app_workflow_triggers(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.atlan_app_workflow_triggers
        )

    @atlan_app_workflow_triggers.setter
    def atlan_app_workflow_triggers(self, atlan_app_workflow_triggers: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow_triggers = atlan_app_workflow_triggers

    @property
    def atlan_app(self) -> Optional[AtlanApp]:
        return None if self.attributes is None else self.attributes.atlan_app

    @atlan_app.setter
    def atlan_app(self, atlan_app: Optional[AtlanApp]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app = atlan_app

    @property
    def atlan_app_workflow_runs(self) -> Optional[List[AppWorkflowRun]]:
        return (
            None if self.attributes is None else self.attributes.atlan_app_workflow_runs
        )

    @atlan_app_workflow_runs.setter
    def atlan_app_workflow_runs(
        self, atlan_app_workflow_runs: Optional[List[AppWorkflowRun]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.atlan_app_workflow_runs = atlan_app_workflow_runs

    class Attributes(AtlanApp.Attributes):
        atlan_app_workflow_version: Optional[str] = Field(default=None, description="")
        atlan_app_workflow_slug: Optional[str] = Field(default=None, description="")
        atlan_app_workflow_dag: Optional[str] = Field(default=None, description="")
        atlan_app_workflow_status: Optional[AtlanAppWorkflowStatus] = Field(
            default=None, description=""
        )
        atlan_app_workflow_error_handling: Optional[AtlanAppErrorHandling] = Field(
            default=None, description=""
        )
        atlan_app_workflow_ownership: Optional[AtlanAppWorkflowOwnership] = Field(
            default=None, description=""
        )
        atlan_app_workflow_triggers: Optional[str] = Field(default=None, description="")
        atlan_app: Optional[AtlanApp] = Field(
            default=None, description=""
        )  # relationship
        atlan_app_workflow_runs: Optional[List[AppWorkflowRun]] = Field(
            default=None, description=""
        )  # relationship

    attributes: AtlanAppWorkflow.Attributes = Field(
        default_factory=lambda: AtlanAppWorkflow.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .app_workflow_run import AppWorkflowRun  # noqa: E402, F401
from .atlan_app import AtlanApp  # noqa: E402, F401
