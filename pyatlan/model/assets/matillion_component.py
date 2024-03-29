# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, Dict, List, Optional, Set

from pydantic.v1 import Field, validator

from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    RelationField,
)

from .matillion import Matillion


class MatillionComponent(Matillion):
    """Description"""

    type_name: str = Field(default="MatillionComponent", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MatillionComponent":
            raise ValueError("must be MatillionComponent")
        return v

    def __setattr__(self, name, value):
        if name in MatillionComponent._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_COMPONENT_ID: ClassVar[KeywordField] = KeywordField(
        "matillionComponentId", "matillionComponentId"
    )
    """
    Unique identifier of the component in Matillion.
    """
    MATILLION_COMPONENT_IMPLEMENTATION_ID: ClassVar[KeywordField] = KeywordField(
        "matillionComponentImplementationId", "matillionComponentImplementationId"
    )
    """
    Unique identifier for the type of the component in Matillion.
    """
    MATILLION_COMPONENT_LINKED_JOB: ClassVar[KeywordField] = KeywordField(
        "matillionComponentLinkedJob", "matillionComponentLinkedJob"
    )
    """
    Job details of the job to which the component internally links.
    """
    MATILLION_COMPONENT_LAST_RUN_STATUS: ClassVar[KeywordField] = KeywordField(
        "matillionComponentLastRunStatus", "matillionComponentLastRunStatus"
    )
    """
    Latest run status of the component within a job.
    """
    MATILLION_COMPONENT_LAST_FIVE_RUN_STATUS: ClassVar[KeywordField] = KeywordField(
        "matillionComponentLastFiveRunStatus", "matillionComponentLastFiveRunStatus"
    )
    """
    Last five run statuses of the component within a job.
    """
    MATILLION_COMPONENT_SQLS: ClassVar[KeywordField] = KeywordField(
        "matillionComponentSqls", "matillionComponentSqls"
    )
    """
    SQL queries used by the component.
    """
    MATILLION_JOB_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionJobName", "matillionJobName.keyword", "matillionJobName"
    )
    """
    Simple name of the job to which the component belongs.
    """
    MATILLION_JOB_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionJobQualifiedName",
        "matillionJobQualifiedName",
        "matillionJobQualifiedName.text",
    )
    """
    Unique name of the job to which the component belongs.
    """

    MATILLION_PROCESS: ClassVar[RelationField] = RelationField("matillionProcess")
    """
    TBC
    """
    MATILLION_JOB: ClassVar[RelationField] = RelationField("matillionJob")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "matillion_component_id",
        "matillion_component_implementation_id",
        "matillion_component_linked_job",
        "matillion_component_last_run_status",
        "matillion_component_last_five_run_status",
        "matillion_component_sqls",
        "matillion_job_name",
        "matillion_job_qualified_name",
        "matillion_process",
        "matillion_job",
    ]

    @property
    def matillion_component_id(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.matillion_component_id
        )

    @matillion_component_id.setter
    def matillion_component_id(self, matillion_component_id: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_id = matillion_component_id

    @property
    def matillion_component_implementation_id(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_implementation_id
        )

    @matillion_component_implementation_id.setter
    def matillion_component_implementation_id(
        self, matillion_component_implementation_id: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_implementation_id = (
            matillion_component_implementation_id
        )

    @property
    def matillion_component_linked_job(self) -> Optional[Dict[str, str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_linked_job
        )

    @matillion_component_linked_job.setter
    def matillion_component_linked_job(
        self, matillion_component_linked_job: Optional[Dict[str, str]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_linked_job = matillion_component_linked_job

    @property
    def matillion_component_last_run_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_last_run_status
        )

    @matillion_component_last_run_status.setter
    def matillion_component_last_run_status(
        self, matillion_component_last_run_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_last_run_status = (
            matillion_component_last_run_status
        )

    @property
    def matillion_component_last_five_run_status(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_last_five_run_status
        )

    @matillion_component_last_five_run_status.setter
    def matillion_component_last_five_run_status(
        self, matillion_component_last_five_run_status: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_last_five_run_status = (
            matillion_component_last_five_run_status
        )

    @property
    def matillion_component_sqls(self) -> Optional[Set[str]]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_component_sqls
        )

    @matillion_component_sqls.setter
    def matillion_component_sqls(self, matillion_component_sqls: Optional[Set[str]]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_component_sqls = matillion_component_sqls

    @property
    def matillion_job_name(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.matillion_job_name

    @matillion_job_name.setter
    def matillion_job_name(self, matillion_job_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_name = matillion_job_name

    @property
    def matillion_job_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_job_qualified_name
        )

    @matillion_job_qualified_name.setter
    def matillion_job_qualified_name(self, matillion_job_qualified_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_qualified_name = matillion_job_qualified_name

    @property
    def matillion_process(self) -> Optional[Process]:
        return None if self.attributes is None else self.attributes.matillion_process

    @matillion_process.setter
    def matillion_process(self, matillion_process: Optional[Process]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_process = matillion_process

    @property
    def matillion_job(self) -> Optional[MatillionJob]:
        return None if self.attributes is None else self.attributes.matillion_job

    @matillion_job.setter
    def matillion_job(self, matillion_job: Optional[MatillionJob]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job = matillion_job

    class Attributes(Matillion.Attributes):
        matillion_component_id: Optional[str] = Field(default=None, description="")
        matillion_component_implementation_id: Optional[str] = Field(
            default=None, description=""
        )
        matillion_component_linked_job: Optional[Dict[str, str]] = Field(
            default=None, description=""
        )
        matillion_component_last_run_status: Optional[str] = Field(
            default=None, description=""
        )
        matillion_component_last_five_run_status: Optional[str] = Field(
            default=None, description=""
        )
        matillion_component_sqls: Optional[Set[str]] = Field(
            default=None, description=""
        )
        matillion_job_name: Optional[str] = Field(default=None, description="")
        matillion_job_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        matillion_process: Optional[Process] = Field(
            default=None, description=""
        )  # relationship
        matillion_job: Optional[MatillionJob] = Field(
            default=None, description=""
        )  # relationship

    attributes: MatillionComponent.Attributes = Field(
        default_factory=lambda: MatillionComponent.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .matillion_job import MatillionJob  # noqa
from .process import Process  # noqa
