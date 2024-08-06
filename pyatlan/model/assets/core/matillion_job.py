# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.


from __future__ import annotations

from typing import ClassVar, List, Optional

from pydantic.v1 import Field, validator

from pyatlan.model.enums import MatillionJobType
from pyatlan.model.fields.atlan_fields import (
    KeywordField,
    KeywordTextField,
    NumericField,
    RelationField,
)

from .matillion import Matillion


class MatillionJob(Matillion):
    """Description"""

    type_name: str = Field(default="MatillionJob", allow_mutation=False)

    @validator("type_name")
    def validate_type_name(cls, v):
        if v != "MatillionJob":
            raise ValueError("must be MatillionJob")
        return v

    def __setattr__(self, name, value):
        if name in MatillionJob._convenience_properties:
            return object.__setattr__(self, name, value)
        super().__setattr__(name, value)

    MATILLION_JOB_TYPE: ClassVar[KeywordField] = KeywordField(
        "matillionJobType", "matillionJobType"
    )
    """
    Type of the job, for example: orchestration or transformation.
    """
    MATILLION_JOB_PATH: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionJobPath", "matillionJobPath", "matillionJobPath.text"
    )
    """
    Path of the job within the project. Jobs can be managed at multiple folder levels within a project.
    """
    MATILLION_JOB_COMPONENT_COUNT: ClassVar[NumericField] = NumericField(
        "matillionJobComponentCount", "matillionJobComponentCount"
    )
    """
    Number of components within the job.
    """
    MATILLION_JOB_SCHEDULE: ClassVar[KeywordField] = KeywordField(
        "matillionJobSchedule", "matillionJobSchedule"
    )
    """
    How the job is scheduled, for example: weekly or monthly.
    """
    MATILLION_PROJECT_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionProjectName", "matillionProjectName.keyword", "matillionProjectName"
    )
    """
    Simple name of the project to which the job belongs.
    """
    MATILLION_PROJECT_QUALIFIED_NAME: ClassVar[KeywordTextField] = KeywordTextField(
        "matillionProjectQualifiedName",
        "matillionProjectQualifiedName",
        "matillionProjectQualifiedName.text",
    )
    """
    Unique name of the project to which the job belongs.
    """

    MATILLION_PROJECT: ClassVar[RelationField] = RelationField("matillionProject")
    """
    TBC
    """
    MATILLION_COMPONENTS: ClassVar[RelationField] = RelationField("matillionComponents")
    """
    TBC
    """

    _convenience_properties: ClassVar[List[str]] = [
        "matillion_job_type",
        "matillion_job_path",
        "matillion_job_component_count",
        "matillion_job_schedule",
        "matillion_project_name",
        "matillion_project_qualified_name",
        "matillion_project",
        "matillion_components",
    ]

    @property
    def matillion_job_type(self) -> Optional[MatillionJobType]:
        return None if self.attributes is None else self.attributes.matillion_job_type

    @matillion_job_type.setter
    def matillion_job_type(self, matillion_job_type: Optional[MatillionJobType]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_type = matillion_job_type

    @property
    def matillion_job_path(self) -> Optional[str]:
        return None if self.attributes is None else self.attributes.matillion_job_path

    @matillion_job_path.setter
    def matillion_job_path(self, matillion_job_path: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_path = matillion_job_path

    @property
    def matillion_job_component_count(self) -> Optional[int]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_job_component_count
        )

    @matillion_job_component_count.setter
    def matillion_job_component_count(
        self, matillion_job_component_count: Optional[int]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_component_count = matillion_job_component_count

    @property
    def matillion_job_schedule(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.matillion_job_schedule
        )

    @matillion_job_schedule.setter
    def matillion_job_schedule(self, matillion_job_schedule: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_job_schedule = matillion_job_schedule

    @property
    def matillion_project_name(self) -> Optional[str]:
        return (
            None if self.attributes is None else self.attributes.matillion_project_name
        )

    @matillion_project_name.setter
    def matillion_project_name(self, matillion_project_name: Optional[str]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project_name = matillion_project_name

    @property
    def matillion_project_qualified_name(self) -> Optional[str]:
        return (
            None
            if self.attributes is None
            else self.attributes.matillion_project_qualified_name
        )

    @matillion_project_qualified_name.setter
    def matillion_project_qualified_name(
        self, matillion_project_qualified_name: Optional[str]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project_qualified_name = (
            matillion_project_qualified_name
        )

    @property
    def matillion_project(self) -> Optional[MatillionProject]:
        return None if self.attributes is None else self.attributes.matillion_project

    @matillion_project.setter
    def matillion_project(self, matillion_project: Optional[MatillionProject]):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_project = matillion_project

    @property
    def matillion_components(self) -> Optional[List[MatillionComponent]]:
        return None if self.attributes is None else self.attributes.matillion_components

    @matillion_components.setter
    def matillion_components(
        self, matillion_components: Optional[List[MatillionComponent]]
    ):
        if self.attributes is None:
            self.attributes = self.Attributes()
        self.attributes.matillion_components = matillion_components

    class Attributes(Matillion.Attributes):
        matillion_job_type: Optional[MatillionJobType] = Field(
            default=None, description=""
        )
        matillion_job_path: Optional[str] = Field(default=None, description="")
        matillion_job_component_count: Optional[int] = Field(
            default=None, description=""
        )
        matillion_job_schedule: Optional[str] = Field(default=None, description="")
        matillion_project_name: Optional[str] = Field(default=None, description="")
        matillion_project_qualified_name: Optional[str] = Field(
            default=None, description=""
        )
        matillion_project: Optional[MatillionProject] = Field(
            default=None, description=""
        )  # relationship
        matillion_components: Optional[List[MatillionComponent]] = Field(
            default=None, description=""
        )  # relationship

    attributes: MatillionJob.Attributes = Field(
        default_factory=lambda: MatillionJob.Attributes(),
        description=(
            "Map of attributes in the instance and their values. "
            "The specific keys of this map will vary by type, "
            "so are described in the sub-types of this schema."
        ),
    )


from .matillion_component import MatillionComponent  # noqa
from .matillion_project import MatillionProject  # noqa
