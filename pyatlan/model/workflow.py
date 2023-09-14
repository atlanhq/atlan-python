# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/elastic/elasticsearch-dsl-py.git (under Apache-2.0 license)
from typing import Any, Optional

from pydantic import Field

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.constants import WORKFLOW_INDEX_SEARCH
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanWorkflowPhase, SortOrder
from pyatlan.model.search import Bool, NestedQuery, Query, SortItem, Term


class WorkflowMetadata(AtlanObject):
    annotations: dict[str, str]
    creation_timestamp: str
    generate_name: str
    generation: int
    labels: dict[str, str]
    managed_fields: Optional[list[Any]]
    name: str
    namespace: str
    resource_version: str
    uid: str


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
    workflow_template_ref: dict[str, str]
    workflow_metadata: Optional[WorkflowMetadata]


class WorkflowSearchResultStatus(AtlanObject):
    artifact_gc_Status: dict[str, Any] = Field(alias="artifactGCStatus")
    artifact_repository_ref: Optional[Any]
    compressed_nodes: Optional[str]
    estimated_duration: Optional[int]
    conditions: list[Any]
    message: Optional[str]
    finished_at: str
    nodes: Optional[Any]
    outputs: Optional[WorkflowParameters]
    phase: AtlanWorkflowPhase
    progress: str
    resources_duration: dict[str, int]
    startedAt: str
    stored_templates: Any
    storedWorkflowTemplateSpec: Any
    synchronization: Optional[dict[str, Any]]


class WorkflowSearchResultDetail(AtlanObject):
    api_version: str
    kind: str
    metadata: WorkflowMetadata
    spec: WorkflowSpec
    status: WorkflowSearchResultStatus


class WorkflowSearchResult(AtlanObject):
    index: str = Field(alias="_index")
    type: str = Field(alias="_type")
    id: str = Field(alias="_id")
    seq_no: Any = Field(alias="_seq_no")
    primary_term: Any = Field(alias="_primary_term")
    sort: list[Any]
    source: WorkflowSearchResultDetail = Field(alias="_source")


class WorkflowSearchHits(AtlanObject):
    total: dict[str, Any]
    hits: Optional[list[WorkflowSearchResult]]


class WorkflowSearchResponse(AtlanObject):
    took: Optional[int]
    hits: WorkflowSearchHits
    shards: dict[str, Any] = Field(alias="_shards")


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


class WorkflowClient:
    def __init__(self, client: AtlanClient):
        self._client = client

    def find_run_by_name(self, workflow_run_name) -> Optional[WorkflowSearchResult]:
        query = Bool(
            filter=[
                NestedQuery(
                    query=Term(field="metadata.name.keyword", value=workflow_run_name),
                    path="metadata",
                )
            ]
        )
        response = self._find_run(query)
        if results := response.hits.hits:
            return results[0]
        return None

    def _find_run(self, query: Query) -> WorkflowSearchResponse:
        request = WorkflowSearchRequest(query=query, size=1)
        raw_json = self._client._call_api(
            WORKFLOW_INDEX_SEARCH,
            request_obj=request,
        )
        response = WorkflowSearchResponse(**raw_json)
        return response


if __name__ == "__main__":
    client = WorkflowClient(AtlanClient())
    result = client.find_run_by_name("atlan-sigma-1694427200-b6w42")
    print(result)
