# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Any, Generator, Union

import msgspec

from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanWorkflowPhase


class PackageParameter(msgspec.Struct, kw_only=True):
    """Parameter for a workflow package."""

    parameter: Union[str, None] = None
    type: Union[str, None] = None
    body: Union[dict[str, Any], None] = None


class WorkflowMetadata(msgspec.Struct, kw_only=True):
    """Metadata for a workflow."""

    annotations: Union[dict[str, str], None] = None
    creation_timestamp: Union[str, None] = None
    generate_name: Union[str, None] = None
    generation: Union[int, None] = None
    labels: Union[dict[str, str], None] = None
    managed_fields: Union[list[Any], None] = None
    name: Union[str, None] = None
    namespace: Union[str, None] = None
    resource_version: Union[str, None] = None
    uid: Union[str, None] = None


class WorkflowTemplateRef(msgspec.Struct, kw_only=True):
    """Reference to a workflow template."""

    name: Union[str, None] = None
    template: Union[str, None] = None
    cluster_scope: Union[bool, None] = None


class NameValuePair(msgspec.Struct, kw_only=True):
    """Simple name-value pair."""

    name: Union[str, None] = None
    value: Union[Any, None] = None


class WorkflowParameters(msgspec.Struct, kw_only=True):
    """Parameters for a workflow."""

    parameters: Union[list[NameValuePair], None] = None


class WorkflowTask(msgspec.Struct, kw_only=True):
    """Task within a workflow DAG."""

    name: Union[str, None] = None
    arguments: Union[WorkflowParameters, None] = None
    template_ref: Union[WorkflowTemplateRef, None] = None


class WorkflowDAG(msgspec.Struct, kw_only=True):
    """Directed acyclic graph of workflow tasks."""

    tasks: Union[list[WorkflowTask], None] = None


class WorkflowTemplate(msgspec.Struct, kw_only=True):
    """Template for a workflow."""

    name: Union[str, None] = None
    inputs: Union[Any, None] = None
    outputs: Union[Any, None] = None
    metadata: Union[Any, None] = None
    dag: Union[WorkflowDAG, None] = None


class WorkflowSpec(msgspec.Struct, kw_only=True):
    """Specification for a workflow."""

    entrypoint: Union[str, None] = None
    arguments: Union[Any, None] = None
    templates: Union[list[WorkflowTemplate], None] = None
    workflow_template_ref: Union[dict[str, str], None] = None
    workflow_metadata: Union[WorkflowMetadata, None] = None


class Workflow(msgspec.Struct, kw_only=True):
    """A workflow definition."""

    metadata: Union[WorkflowMetadata, None] = None
    spec: Union[WorkflowSpec, None] = None
    payload: list[PackageParameter] = msgspec.field(default_factory=list)


class WorkflowSearchResultStatus(msgspec.Struct, kw_only=True):
    """Status of a workflow search result."""

    artifact_gc_status: Union[dict[str, Any], None] = msgspec.field(
        default=None, name="artifactGCStatus"
    )
    artifact_repository_ref: Union[Any, None] = None
    compressed_nodes: Union[str, None] = None
    estimated_duration: Union[int, None] = None
    conditions: Union[list[Any], None] = None
    message: Union[str, None] = None
    finished_at: Union[str, None] = None
    nodes: Union[Any, None] = None
    outputs: Union[WorkflowParameters, None] = None
    phase: Union[AtlanWorkflowPhase, None] = None
    progress: Union[str, None] = None
    resources_duration: Union[dict[str, int], None] = None
    started_at: Union[str, None] = msgspec.field(default=None, name="startedAt")
    stored_templates: Union[Any, None] = None
    stored_workflow_template_spec: Union[Any, None] = None
    synchronization: Union[dict[str, Any], None] = None


class WorkflowSearchResultDetail(msgspec.Struct, kw_only=True):
    """Details of a workflow search result."""

    api_version: Union[str, None] = None
    kind: Union[str, None] = None
    metadata: Union[WorkflowMetadata, None] = None
    spec: Union[WorkflowSpec, None] = None
    status: Union[WorkflowSearchResultStatus, None] = None


class WorkflowSearchResult(msgspec.Struct, kw_only=True):
    """Individual result from a workflow search."""

    index: Union[str, None] = msgspec.field(default=None, name="_index")
    type: Union[str, None] = msgspec.field(default=None, name="_type")
    id: Union[str, None] = msgspec.field(default=None, name="_id")
    seq_no: Union[Any, None] = msgspec.field(default=None, name="_seq_no")
    primary_term: Union[Any, None] = msgspec.field(default=None, name="_primary_term")
    sort: Union[list[Any], None] = None
    source: Union[WorkflowSearchResultDetail, None] = msgspec.field(
        default=None, name="_source"
    )

    @property
    def status(self) -> Union[AtlanWorkflowPhase, None]:
        """Phase/status of the workflow."""
        if source := self.source:
            if status := source.status:
                return status.phase
        return None

    def to_workflow(self) -> Workflow:
        """Convert search result to a Workflow."""
        return Workflow(
            spec=self.source.spec if self.source else None,
            metadata=self.source.metadata if self.source else None,
        )


class WorkflowSearchHits(msgspec.Struct, kw_only=True):
    """Hits from a workflow search."""

    total: Union[dict[str, Any], None] = None
    hits: Union[list[WorkflowSearchResult], None] = None


class ReRunRequest(msgspec.Struct, kw_only=True):
    """Request to re-run a workflow."""

    namespace: Union[str, None] = "default"
    resource_kind: Union[str, None] = "WorkflowTemplate"
    resource_name: Union[str, None] = None


class WorkflowResponse(msgspec.Struct, kw_only=True):
    """Response from a workflow operation."""

    metadata: Union[WorkflowMetadata, None] = None
    spec: Union[WorkflowSpec, None] = None
    payload: list[Any] = msgspec.field(default_factory=list)


class WorkflowRunResponse(msgspec.Struct, kw_only=True):
    """Response from a workflow run operation."""

    metadata: Union[WorkflowMetadata, None] = None
    spec: Union[WorkflowSpec, None] = None
    payload: list[Any] = msgspec.field(default_factory=list)
    status: Union[WorkflowSearchResultStatus, None] = None


class ScheduleQueriesSearchRequest(msgspec.Struct, kw_only=True):
    """Request for searching schedule queries."""

    start_date: str
    """Start date in ISO 8601 format."""
    end_date: str
    """End date in ISO 8601 format."""


class WorkflowSchedule(msgspec.Struct, kw_only=True):
    """Schedule for a workflow."""

    timezone: str
    cron_schedule: str


class WorkflowScheduleSpec(msgspec.Struct, kw_only=True):
    """Specification for a workflow schedule."""

    schedule: Union[str, None] = None
    timezone: Union[str, None] = None
    workflow_spec: Union[WorkflowSpec, None] = None
    concurrency_policy: Union[str, None] = None
    starting_deadline_seconds: Union[int, None] = None
    successful_jobs_history_limit: Union[int, None] = None
    failed_jobs_history_limit: Union[int, None] = None


class WorkflowScheduleStatus(msgspec.Struct, kw_only=True):
    """Status of a workflow schedule."""

    active: Union[Any, None] = None
    conditions: Union[Any, None] = None
    last_scheduled_time: Union[str, None] = None


class WorkflowScheduleResponse(msgspec.Struct, kw_only=True):
    """Response from a workflow schedule operation."""

    metadata: Union[WorkflowMetadata, None] = None
    spec: Union[WorkflowScheduleSpec, None] = None
    status: Union[WorkflowScheduleStatus, None] = None
    workflow_metadata: Union[WorkflowMetadata, None] = None


class WorkflowSearchResponse(msgspec.Struct, kw_only=True):
    """Response from a workflow search with pagination support."""

    took: Union[int, None] = None
    hits: Union[WorkflowSearchHits, None] = None
    shards: Union[dict[str, Any], None] = msgspec.field(default=None, name="_shards")

    # Pagination state (not from JSON — set after construction)
    _size: int = 10
    _start: int = 0
    _endpoint: Any = None
    _client: Any = None
    _criteria: Any = None

    @property
    def count(self) -> int:
        """Total count of workflow search results."""
        return self.hits.total.get("value", 0) if self.hits and self.hits.total else 0

    def current_page(self) -> Union[list[WorkflowSearchResult], None]:
        """Return the current page of results."""
        return self.hits.hits if self.hits else None

    def next_page(self, start=None, size=None) -> bool:
        """Advance to the next page of results."""
        self._start = start or self._start + self._size
        if size:
            self._size = size
        if self.hits and self.hits.hits:
            return self._get_next_page()
        return False

    def _get_next_page(self) -> bool:
        """Fetch the next page of results."""
        from pyatlan_v9.model.workflow import WorkflowSearchRequest

        request = WorkflowSearchRequest(
            query=self._criteria, from_=self._start, size=self._size
        )
        raw_json = self._client._call_api(
            api=self._endpoint,
            request_obj=request,
        )
        if not raw_json.get("hits", {}).get("hits"):
            if self.hits:
                self.hits.hits = []
            return False
        try:
            if self.hits:
                self.hits.hits = msgspec.convert(
                    raw_json["hits"]["hits"], list[WorkflowSearchResult], strict=False
                )
        except Exception as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    def __iter__(self) -> Generator[WorkflowSearchResult, None, None]:  # type: ignore[override]
        """Iterate through all pages of results."""
        while True:
            yield from self.current_page() or []
            if not self.next_page():
                break


class WorkflowSearchRequest(msgspec.Struct, kw_only=True):
    """Request to search for workflows."""

    from_: int = msgspec.field(default=0, name="from")
    """Starting offset for results."""
    size: int = 10
    """Page size for results."""
    track_total_hits: bool = True
    """Whether to track total hit count."""
    post_filter: Union[Any, None] = None
    """Post-search filter."""
    query: Union[Any, None] = None
    """Search query."""
    sort: Union[list[Any], None] = None
    """Sort criteria."""
    source: Union[WorkflowSearchResultDetail, None] = msgspec.field(
        default=None, name="_source"
    )
