# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from typing import Any, Dict, Generator, List, Optional

from pydantic.v1 import Field, PrivateAttr, ValidationError, parse_obj_as

from pyatlan.client.common import ApiCaller
from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanWorkflowPhase, SortOrder
from pyatlan.model.search import Query, SortItem
from pyatlan.utils import API


class PackageParameter(AtlanObject):
    parameter: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    body: Optional[Dict[str, Any]] = Field(default=None)


class WorkflowMetadata(AtlanObject):
    annotations: Optional[Dict[str, str]] = Field(default=None)
    creation_timestamp: Optional[str] = Field(default=None)
    generate_name: Optional[str] = Field(default=None)
    generation: Optional[int] = Field(default=None)
    labels: Optional[Dict[str, str]] = Field(default=None)
    managed_fields: Optional[List[Any]] = Field(default=None)
    name: Optional[str] = Field(default=None)
    namespace: Optional[str] = Field(default=None)
    resource_version: Optional[str] = Field(default=None)
    uid: Optional[str] = Field(default=None)


class WorkflowTemplateRef(AtlanObject):
    name: Optional[str] = Field(default=None)
    template: Optional[str] = Field(default=None)
    cluster_scope: Optional[bool] = Field(default=None)


class NameValuePair(AtlanObject):
    name: Optional[str] = Field(default=None)
    value: Optional[Any] = Field(default=None)


class WorkflowParameters(AtlanObject):
    parameters: Optional[List[NameValuePair]] = Field(default=None)


class WorkflowTask(AtlanObject):
    name: Optional[str] = Field(default=None)
    arguments: Optional[WorkflowParameters] = Field(default=None)
    template_ref: Optional[WorkflowTemplateRef] = Field(default=None)


class WorkflowDAG(AtlanObject):
    tasks: Optional[List[WorkflowTask]] = Field(default=None)


class WorkflowTemplate(AtlanObject):
    name: Optional[str] = Field(default=None)
    inputs: Any = Field(default=None)
    outputs: Any = Field(default=None)
    metadata: Any = Field(default=None)
    dag: Optional[WorkflowDAG] = Field(default=None)


class WorkflowSpec(AtlanObject):
    entrypoint: Optional[str] = Field(default=None)
    arguments: Optional[Any] = Field(default=None)
    templates: Optional[List[WorkflowTemplate]] = Field(default=None)
    workflow_template_ref: Optional[Dict[str, str]] = Field(default=None)
    workflow_metadata: Optional[WorkflowMetadata] = Field(default=None)


class Workflow(AtlanObject):
    metadata: Optional[WorkflowMetadata] = Field(default=None)
    spec: Optional[WorkflowSpec] = Field(default=None)
    payload: List[PackageParameter] = Field(default_factory=list)


class WorkflowSearchResultStatus(AtlanObject):
    artifact_gc_Status: Optional[Dict[str, Any]] = Field(
        default=None, alias="artifactGCStatus"
    )
    artifact_repository_ref: Optional[Any] = Field(default=None)
    compressed_nodes: Optional[str] = Field(default=None)
    estimated_duration: Optional[int] = Field(default=None)
    conditions: Optional[List[Any]] = Field(default=None)
    message: Optional[str] = Field(default=None)
    finished_at: Optional[str] = Field(default=None)
    nodes: Optional[Any] = Field(default=None)
    outputs: Optional[WorkflowParameters] = Field(default=None)
    phase: Optional[AtlanWorkflowPhase] = Field(default=None)
    progress: Optional[str] = Field(default=None)
    resources_duration: Optional[Dict[str, int]] = Field(default=None)
    startedAt: Optional[str] = Field(default=None)
    stored_templates: Any = Field(default=None)
    stored_workflow_template_spec: Any = Field(default=None)
    synchronization: Optional[Dict[str, Any]] = Field(default=None)


class WorkflowSearchResultDetail(AtlanObject):
    api_version: Optional[str] = Field(default=None)
    kind: Optional[str] = Field(default=None)
    metadata: Optional[WorkflowMetadata] = Field(default=None)
    spec: Optional[WorkflowSpec] = Field(default=None)
    status: Optional[WorkflowSearchResultStatus] = Field(default=None)


class WorkflowSearchResult(AtlanObject):
    index: Optional[str] = Field(default=None, alias="_index")
    type: Optional[str] = Field(default=None, alias="_type")
    id: Optional[str] = Field(default=None, alias="_id")
    seq_no: Optional[Any] = Field(default=None, alias="_seq_no")
    primary_term: Optional[Any] = Field(default=None, alias="_primary_term")
    sort: Optional[List[Any]] = Field(default=None)
    source: Optional[WorkflowSearchResultDetail] = Field(default=None, alias="_source")

    @property
    def status(self) -> Optional[AtlanWorkflowPhase]:
        if source := self.source:
            if status := source.status:
                return status.phase
        return None

    def to_workflow(self) -> Workflow:
        return Workflow(
            spec=self.source and self.source.spec or None,
            metadata=self.source and self.source.metadata or None,
        )


class WorkflowSearchHits(AtlanObject):
    total: Optional[Dict[str, Any]] = Field(default=None)
    hits: Optional[List[WorkflowSearchResult]] = Field(default=None)


class ReRunRequest(AtlanObject):
    namespace: Optional[str] = Field(default="default")
    resource_kind: Optional[str] = Field(default="WorkflowTemplate")
    resource_name: Optional[str] = Field(default=None)

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(["resource_kind"])


class WorkflowResponse(AtlanObject):
    metadata: Optional[WorkflowMetadata] = Field(default=None)
    spec: Optional[WorkflowSpec] = Field(default=None)
    payload: Optional[List[Any]] = Field(default_factory=list)


class WorkflowRunResponse(WorkflowResponse):
    status: Optional[WorkflowSearchResultStatus] = Field(default=None)


class ScheduleQueriesSearchRequest(AtlanObject):
    start_date: str = Field(description="Start date in ISO 8601 format")
    end_date: str = Field(description="End date in ISO 8601 format")


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
    post_filter: Optional[Query] = Field(default=None, alias="post_filter")
    query: Optional[Query] = Field(default=None)
    sort: List[SortItem] = Field(
        alias="sort",
        default=[
            SortItem(
                order=SortOrder.DESCENDING,
                field="metadata.creationTimestamp",
                nested_path="metadata",
            )
        ],
    )
    source: Optional[WorkflowSearchResultDetail] = Field(default=None, alias="_source")

    class Config:
        json_encoders = {Query: lambda v: v.to_dict(), SortItem: lambda v: v.to_dict()}

    def __init__(__pydantic_self__, **data: Any) -> None:
        super().__init__(**data)
        __pydantic_self__.__fields_set__.update(
            ["from_", "size", "track_total_hits", "sort"]
        )


class WorkflowSearchResponse(AtlanObject):
    _size: int = PrivateAttr()
    _start: int = PrivateAttr()
    _endpoint: API = PrivateAttr()
    _client: ApiCaller = PrivateAttr()
    _criteria: WorkflowSearchRequest = PrivateAttr()
    took: Optional[int] = Field(default=None)
    hits: Optional[WorkflowSearchHits] = Field(default=None)
    shards: Optional[Dict[str, Any]] = Field(alias="_shards", default=None)

    def __init__(self, **data: Any):
        super().__init__(**data)
        self._endpoint = data.get("endpoint")  # type: ignore[assignment]
        self._client = data.get("client")  # type: ignore[assignment]
        self._criteria = data.get("criteria")  # type: ignore[assignment]
        self._size = data.get("size")  # type: ignore[assignment]
        self._start = data.get("start")  # type: ignore[assignment]

    @property
    def count(self):
        return self.hits.total.get("value", 0) if self.hits and self.hits.total else 0

    def current_page(self) -> Optional[List[WorkflowSearchResult]]:
        return self.hits.hits  # type: ignore

    def next_page(self, start=None, size=None) -> bool:
        self._start = start or self._start + self._size
        if size:
            self._size = size
        return self._get_next_page() if self.hits.hits else False  # type: ignore

    def _get_next_page(self):
        request = WorkflowSearchRequest(
            query=self._criteria, from_=self._start, size=self._size
        )
        raw_json = self._client._call_api(
            api=self._endpoint,
            request_obj=request,
        )
        if not raw_json.get("hits", {}).get("hits"):
            self.hits.hits = []
            return False
        try:
            self.hits.hits = parse_obj_as(
                List[WorkflowSearchResult], raw_json["hits"]["hits"]
            )
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err
        return True

    def __iter__(self) -> Generator[WorkflowSearchResult, None, None]:  # type: ignore[override]
        while True:
            yield from self.current_page() or []
            if not self.next_page():
                break
