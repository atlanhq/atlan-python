# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Any, Optional

from pydantic import Field

from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanWorkflowPhase, SortOrder
from pyatlan.model.search import Query, SortItem


class PackageParameter(AtlanObject):
    parameter: str
    type: str
    body: dict[str, Any]


class WorkflowMetadata(AtlanObject):
    annotations: Optional[dict[str, str]]
    creation_timestamp: Optional[str]
    generate_name: Optional[str]
    generation: Optional[int]
    labels: Optional[dict[str, str]]
    managed_fields: Optional[list[Any]]
    name: Optional[str]
    namespace: Optional[str]
    resource_version: Optional[str]
    uid: Optional[str]


class WorkflowTemplateRef(AtlanObject):
    name: str
    template: str
    cluster_scope: bool


class NameValuePair(AtlanObject):
    name: str
    value: Any


class WorkflowParameters(AtlanObject):
    parameters: list[NameValuePair]


class WorkflowTask(AtlanObject):
    name: str
    arguments: WorkflowParameters
    template_ref: WorkflowTemplateRef


class WorkflowDAG(AtlanObject):
    tasks: list[WorkflowTask]


class WorkflowTemplate(AtlanObject):
    name: str
    inputs: Any
    outputs: Any
    metadata: Any
    dag: WorkflowDAG


class WorkflowSpec(AtlanObject):
    entrypoint: Optional[str]
    arguments: Optional[Any]
    templates: Optional[list[WorkflowTemplate]]
    workflow_template_ref: Optional[dict[str, str]]
    workflow_metadata: Optional[WorkflowMetadata]


class Workflow(AtlanObject):
    metadata: WorkflowMetadata
    spec: WorkflowSpec
    payload: list[PackageParameter] = Field(default_factory=list)


class WorkflowSearchResultStatus(AtlanObject):
    artifact_gc_Status: Optional[dict[str, Any]] = Field(
        default=None, alias="artifactGCStatus"
    )
    artifact_repository_ref: Optional[Any] = Field(default=None)
    compressed_nodes: Optional[str] = Field(default=None)
    estimated_duration: Optional[int] = Field(default=None)
    conditions: Optional[list[Any]] = Field(default=None)
    message: Optional[str] = Field(default=None)
    finished_at: Optional[str] = Field(default=None)
    nodes: Optional[Any] = Field(default=None)
    outputs: Optional[WorkflowParameters] = Field(default=None)
    phase: Optional[AtlanWorkflowPhase] = Field(default=None)
    progress: Optional[str] = Field(default=None)
    resources_duration: Optional[dict[str, int]] = Field(default=None)
    startedAt: Optional[str] = Field(default=None)
    stored_templates: Any = Field(default=None)
    stored_workflow_template_spec: Any = Field(default=None)
    synchronization: Optional[dict[str, Any]] = Field(default=None)


class WorkflowSearchResultDetail(AtlanObject):
    api_version: str
    kind: str
    metadata: WorkflowMetadata
    spec: WorkflowSpec
    status: Optional[WorkflowSearchResultStatus]


class WorkflowSearchResult(AtlanObject):
    index: str = Field(alias="_index")
    type: str = Field(alias="_type")
    id: str = Field(alias="_id")
    seq_no: Any = Field(alias="_seq_no")
    primary_term: Any = Field(alias="_primary_term")
    sort: list[Any]
    source: WorkflowSearchResultDetail = Field(alias="_source")

    @property
    def status(self) -> Optional[AtlanWorkflowPhase]:
        if source := self.source:
            if status := source.status:
                return status.phase
        return None

    def to_workflow(self) -> Workflow:
        return Workflow(spec=self.source.spec, metadata=self.source.metadata)


class WorkflowSearchHits(AtlanObject):
    total: dict[str, Any]
    hits: Optional[list[WorkflowSearchResult]]


class WorkflowSearchResponse(AtlanObject):
    took: Optional[int]
    hits: WorkflowSearchHits
    shards: dict[str, Any] = Field(alias="_shards")


class ReRunRequest(AtlanObject):
    namespace: str = "default"
    resource_kind: str = "WorkflowTemplate"
    resource_name: str

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["resource_kind"])


class WorkflowResponse(AtlanObject):
    metadata: WorkflowMetadata
    spec: WorkflowSpec
    payload: Optional[list[Any]] = Field(default_factory=list)


class WorkflowRunResponse(WorkflowResponse):
    status: WorkflowSearchResultStatus


class WorkflowSchedule(AtlanObject):
    timezone: str
    cron_schedule: str


class WorkflowScheduleSpec(AtlanObject):
    schedule: Optional[str] = Field(default=None)
    timezone: Optional[str] = Field(default=None)
    workflow_spec: Optional[WorkflowSpec] = Field(default=None)
    concurrency_policy: Optional[str] = Field(default=None)
    starting_deadline_seconds: Optional[int] = Field(default=None)
    successful_jobs_history_limit: Optional[int] = Field(default=None)
    failed_jobs_history_limit: Optional[int] = Field(default=None)


class WorkflowScheduleStatus(AtlanObject):
    active: Optional[Any] = Field(default=None)
    conditions: Optional[Any] = Field(default=None)
    last_scheduled_time: Optional[str] = Field(default=None)


class WorkflowScheduleResponse(AtlanObject):
    metadata: Optional[WorkflowMetadata] = Field(default=None)
    spec: Optional[WorkflowScheduleSpec] = Field(default=None)
    status: Optional[WorkflowScheduleStatus] = Field(default=None)
    workflow_metadata: Optional[WorkflowMetadata] = Field(default=None)


class WorkflowSearchRequest(AtlanObject):
    from_: int = Field(0, alias="from")
    size: int = 10
    track_total_hits: bool = Field(True, alias="track_total_hits")
    post_filter: Optional[Query] = Field(alias="post_filter")
    query: Optional[Query]
    sort: list[SortItem] = Field(
        alias="sort",
        default=[
            SortItem(
                order=SortOrder.DESCENDING,
                field="metadata.creationTimestamp",
                nested_path="metadata",
            )
        ],
    )

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(
            ["from_", "size", "track_total_hits", "sort"]
        )
