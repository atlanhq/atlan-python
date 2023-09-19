# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
# Based on original code from https://github.com/elastic/elasticsearch-dsl-py.git (under Apache-2.0 license)
from enum import Enum
from logging import Logger
from time import sleep
from typing import Any, Optional, Protocol, Union, overload

from pydantic import Field

from pyatlan.client.constants import (
    WORKFLOW_INDEX_RUN_SEARCH,
    WORKFLOW_INDEX_SEARCH,
    WORKFLOW_RUN,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanWorkflowPhase, SortOrder
from pyatlan.model.search import Bool, NestedQuery, Prefix, Query, SortItem, Term


class WorkflowPackage(str, Enum):
    ATLAN_AIRFLOW = "atlan-airflow"
    ATLAN_ATHENA = "atlan-athena"
    ATLAN_AWS_LAMBDA_TRIGGER = "atlan-aws-lambda-trigger"
    ATLAN_AZURE_EVENT_HUB = "atlan-azure-event-hub"
    ATLAN_BIGQUERY = "atlan-bigquery"
    ATLAN_BIGQUERY_MINER = "atlan-bigquery-miner"
    ATLAN_CONNECTION_DELETE = "atlan-connection-delete"
    ATLAN_DATABRICKS = "atlan-databricks"
    ATLAN_DATABRICKS_LINEAGE = "atlan-databricks-lineage"
    ATLAN_DBT = "atlan-dbt"
    ATLAN_FIVETRAN = "atlan-fivetran"
    ATLAN_GLUE = "atlan-glue"
    ATLAN_HIVE = "atlan-hive"
    ATLAN_HIVE_MINER = "atlan-hive-miner"
    ATLAN_KAFKA = "atlan-kafka"
    ATLAN_KAFKA_AIVEN = "atlan-kafka-aiven"
    ATLAN_KAFKA_CONFLUENT_CLOUD = "atlan-kafka-confluent-cloud"
    ATLAN_KAFKA_REDPANDA = "atlan-kafka-redpanda"
    ATLAN_LOOKER = "atlan-looker"
    ATLAN_MATILLION = "atlan-matillion"
    ATLAN_METABASE = "atlan-metabase"
    ATLAN_MICROSTRATEGY = "atlan-microstrategy"
    ATLAN_MODE = "atlan-mode"
    ATLAN_MONTE_CARLO = "atlan-monte-carlo"
    ATLAN_MSSQL = "atlan-mssql"
    ATLAN_MSSQL_MINER = "atlan-mssql-miner"
    ATLAN_MYSQL = "atlan-mysql"
    ATLAN_ORACLE = "atlan-oracle"
    ATLAN_POSTGRES = "atlan-postgres"
    ATLAN_POWERBI = "atlan-powerbi"
    ATLAN_POWERBI_MINER = "atlan-powerbi-miner"
    ATLAN_PRESTO = "atlan-presto"
    ATLAN_QLIK_SENSE = "atlan-qlik-sense"
    ATLAN_QLIK_SENSE_ENTERPRISE_WINDOWS = "atlan-qlik-sense-enterprise-windows"
    ATLAN_QUICKSIGHT = "atlan-quicksight"
    ATLAN_REDASH = "atlan-redash"
    ATLAN_REDSHIFT = "atlan-redshift"
    ATLAN_REDSHIFT_MINER = "atlan-redshift-miner"
    ATLAN_SALESFORCE = "atlan-salesforce"
    ATLAN_SAP_HANA = "atlan-sap-hana"
    ATLAN_SCHEMA_REGISTRY_CONFLUENT = "atlan-schema-registry-confluent"
    ATLAN_SIGMA = "atlan-sigma"
    ATLAN_SNOWFLAKE = "atlan-snowflake"
    ATLAN_SNOWFLAKE_MINER = "atlan-snowflake-miner"
    ATLAN_SODA = "atlan-soda"
    ATLAN_SYNAPSE = "atlan-synapse"
    ATLAN_TABLEAU = "atlan-tableau"
    ATLAN_TERADATA = "atlan-teradata"
    ATLAN_TERADATA_MINER = "atlan-teradata-miner"
    ATLAN_THOUGHTSPOT = "atlan-thoughtspot"
    ATLAN_TRINO = "atlan-trino"


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
    workflow_template_ref: Optional[dict[str, str]]
    workflow_metadata: Optional[WorkflowMetadata]


class Workflow(AtlanObject):
    metadata: WorkflowMetadata
    spec: WorkflowSpec
    payload: list[PackageParameter]


class WorkflowSearchResultStatus(AtlanObject):
    artifact_gc_Status: Optional[dict[str, Any]] = Field(alias="artifactGCStatus")
    artifact_repository_ref: Optional[Any]
    compressed_nodes: Optional[str]
    estimated_duration: Optional[int]
    conditions: Optional[list[Any]]
    message: Optional[str]
    finished_at: Optional[str]
    nodes: Optional[Any]
    outputs: Optional[WorkflowParameters]
    phase: Optional[AtlanWorkflowPhase]
    progress: Optional[str]
    resources_duration: Optional[dict[str, int]]
    startedAt: Optional[str]
    stored_templates: Any
    storedWorkflowTemplateSpec: Any
    synchronization: Optional[dict[str, Any]]


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
    payload: Optional[list[Any]]


class WorkflowRunResponse(WorkflowResponse):
    status: WorkflowSearchResultStatus


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


class ApiCaller(Protocol):
    def _call_api(
        self, api, query_params=None, request_obj=None, exclude_unset: bool = True
    ):
        pass


class WorkflowClient:
    """
    This class can be used to retrieve information and re_run workflows. This class does not need to be instantiated
    directly by can be obtained thru the workflow propery of AtlanClient.
    """

    def __init__(self, client: ApiCaller):
        self._client = client

    def find_by_type(
        self, prefix: WorkflowPackage, max_results: int = 10
    ) -> list[WorkflowSearchResult]:
        """
        Find workflows based on their type (prefix).

        :param prefix: name of the specific workflow re_run to find (for example ATLAN_CONNECTION_DELETE)
        :param max_results: the maximum number of results to retrieve
        :returns: the list of workflows of the provided type, with the most-recently created first
        """
        query = Bool(
            filter=[
                NestedQuery(
                    query=Prefix(field="metadata.name.keyword", value=prefix.value),
                    path="metadata",
                )
            ]
        )
        request = WorkflowSearchRequest(query=query, size=max_results)
        raw_json = self._client._call_api(
            WORKFLOW_INDEX_SEARCH,
            request_obj=request,
        )
        response = WorkflowSearchResponse(**raw_json)
        return response.hits.hits or []

    def _find_latest_run(self, workflow_name: str) -> Optional[WorkflowSearchResult]:
        query = Bool(
            filter=[
                NestedQuery(
                    query=Term(
                        field="metadata.name.keyword",
                        value=workflow_name,
                    ),
                    path="metadata",
                )
            ]
        )
        response = self._find_run(query)
        return results[0] if (results := response.hits.hits) else None

    def _find_run(self, query: Query, size=1) -> WorkflowSearchResponse:
        request = WorkflowSearchRequest(query=query, size=size)
        raw_json = self._client._call_api(
            WORKFLOW_INDEX_RUN_SEARCH,
            request_obj=request,
        )
        return WorkflowSearchResponse(**raw_json)

    @overload
    def re_run(self, workflow: WorkflowPackage) -> WorkflowRunResponse:
        ...

    @overload
    def re_run(self, workflow: WorkflowSearchResultDetail) -> WorkflowRunResponse:
        ...

    @overload
    def re_run(self, workflow: WorkflowSearchResult) -> WorkflowRunResponse:
        ...

    def re_run(
        self,
        workflow: Union[
            WorkflowPackage, WorkflowSearchResultDetail, WorkflowSearchResult
        ],
    ) -> WorkflowRunResponse:
        """
        Run the workflow immediately.
        :param workflow: The workflow to re_run.
        :returns: the details of the workflow run

        """
        if isinstance(workflow, WorkflowPackage):
            results = self.find_by_type(workflow)
            if not results:
                raise ErrorCode.NO_PRIOR_RUN_AVAILABLE.exception_with_parameters(
                    workflow
                )
            detail = results[0].source
        elif isinstance(workflow, WorkflowSearchResult):
            detail = workflow.source
        elif isinstance(workflow, WorkflowSearchResultDetail):
            detail = workflow
        request = ReRunRequest(
            namespace=detail.metadata.namespace, resource_name=detail.metadata.name
        )
        raw_json = self._client._call_api(
            WORKFLOW_RUN,
            request_obj=request,
        )
        return WorkflowRunResponse(**raw_json)

    def monitor(
        self, workflow_response: WorkflowResponse, log: Logger
    ) -> Optional[AtlanWorkflowPhase]:
        if workflow_response.metadata and workflow_response.metadata.name:
            name = workflow_response.metadata.name
            status: Optional[AtlanWorkflowPhase] = None
            while status not in {
                AtlanWorkflowPhase.SUCCESS,
                AtlanWorkflowPhase.ERROR,
                AtlanWorkflowPhase.FAILED,
            }:
                sleep(5)
                if run_details := self._get_run_details(name):
                    status = run_details.status
                if log:
                    log.debug("Workflow status: %s", status)
            if log:
                log.info("Workflow completion status: %s", status)
            return status
        if log:
            log.info("Skipping workflow monitoring — nothing to monitor.")
        return None

    def _get_run_details(self, name: str) -> Optional[WorkflowSearchResult]:
        return self._find_latest_run(workflow_name=name)
