# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

from typing import Dict, List, Optional

from pydantic.v1 import ValidationError, parse_obj_as

from pyatlan.client.constants import (
    GET_ALL_SCHEDULE_RUNS,
    GET_SCHEDULE_RUN,
    PACKAGE_WORKFLOW_ARCHIVE,
    PACKAGE_WORKFLOW_RERUN,
    PACKAGE_WORKFLOW_RUN,
    PACKAGE_WORKFLOW_UPDATE,
    SCHEDULE_QUERY_WORKFLOWS_MISSED,
    SCHEDULE_QUERY_WORKFLOWS_SEARCH,
    STOP_WORKFLOW_RUN,
    WORKFLOW_ARCHIVE,
    WORKFLOW_CHANGE_OWNER,
    WORKFLOW_INDEX_RUN_SEARCH,
    WORKFLOW_INDEX_SEARCH,
    WORKFLOW_OWNER_RERUN,
    WORKFLOW_RERUN,
    WORKFLOW_RUN,
    WORKFLOW_UPDATE,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanWorkflowPhase, WorkflowPackage
from pyatlan.model.search import (
    Bool,
    Exists,
    NestedQuery,
    Prefix,
    Query,
    Range,
    Regexp,
    Term,
    Terms,
)
from pyatlan.model.workflow import (
    ReRunRequest,
    ScheduleQueriesSearchRequest,
    Workflow,
    WorkflowResponse,
    WorkflowRunResponse,
    WorkflowSchedule,
    WorkflowScheduleResponse,
    WorkflowSearchRequest,
    WorkflowSearchResponse,
    WorkflowSearchResult,
    WorkflowSearchResultDetail,
)

MONITOR_SLEEP_SECONDS = 5


class WorkflowParseResponse:
    """Shared utility for parsing workflow responses."""

    @staticmethod
    def parse_response(raw_json, response_type):
        """Parse raw JSON response into specified type."""
        try:
            if not raw_json:
                return
            elif isinstance(raw_json, list):
                return parse_obj_as(List[response_type], raw_json)
            return parse_obj_as(response_type, raw_json)
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err


class WorkflowFindByType:
    """Shared logic for finding workflows by type."""

    @staticmethod
    def prepare_request(prefix: WorkflowPackage, max_results: int = 10) -> tuple:
        """
        Prepare the request for finding workflows by type.

        :param prefix: name of the specific workflow to find
        :param max_results: the maximum number of results to retrieve
        :returns: tuple of (endpoint, request_obj)
        """
        regex = prefix.value.replace("-", "[-]") + "[-][0-9]{10}"
        query = Bool(
            filter=[
                NestedQuery(
                    query=Regexp(field="metadata.name.keyword", value=regex),
                    path="metadata",
                )
            ]
        )
        request = WorkflowSearchRequest(query=query, size=max_results)
        return WORKFLOW_INDEX_SEARCH, request

    @staticmethod
    def process_response(raw_json: Dict) -> List[WorkflowSearchResult]:
        """
        Process the API response into a list of WorkflowSearchResult.

        :param raw_json: raw response from the API
        :returns: list of WorkflowSearchResult objects
        """
        response = WorkflowSearchResponse(**raw_json)
        return response.hits and response.hits.hits or []


class WorkflowFindById:
    """Shared logic for finding workflows by ID."""

    @staticmethod
    def prepare_request(id: str) -> tuple:
        """
        Prepare the request for finding workflow by ID.

        :param id: identifier of the specific workflow to find
        :returns: tuple of (endpoint, request_obj)
        """
        query = Bool(
            filter=[
                NestedQuery(
                    query=Bool(must=[Term(field="metadata.name.keyword", value=id)]),
                    path="metadata",
                )
            ]
        )
        request = WorkflowSearchRequest(query=query, size=1)
        return WORKFLOW_INDEX_SEARCH, request

    @staticmethod
    def process_response(raw_json: Dict) -> Optional[WorkflowSearchResult]:
        """
        Process the API response into a WorkflowSearchResult.

        :param raw_json: raw response from the API
        :returns: WorkflowSearchResult object or None
        """
        response = WorkflowSearchResponse(**raw_json)
        results = response.hits and response.hits.hits
        return results[0] if results else None


class WorkflowFindRunsByStatusAndTimeRange:
    """Shared logic for finding workflow runs by status and time range."""

    @staticmethod
    def prepare_request(
        status: List[AtlanWorkflowPhase],
        started_at: Optional[str] = None,
        finished_at: Optional[str] = None,
        from_: int = 0,
        size: int = 100,
    ) -> tuple:
        """
        Prepare the request for finding workflow runs by status and time range.

        :param status: list of the workflow statuses to filter
        :param started_at: (optional) lower bound on 'status.startedAt'
        :param finished_at: (optional) lower bound on 'status.finishedAt'
        :param from_: starting index of the search results
        :param size: maximum number of search results to return
        :returns: tuple of (endpoint, request_obj)
        """
        time_filters = []
        if started_at:
            time_filters.append(Range(field="status.startedAt", gte=started_at))
        if finished_at:
            time_filters.append(Range(field="status.finishedAt", gte=finished_at))

        run_lookup_query = Bool(
            must=[
                NestedQuery(
                    query=Terms(
                        field="metadata.labels.workflows.argoproj.io/phase.keyword",
                        values=[s.value for s in status],
                    ),
                    path="metadata",
                ),
                *time_filters,
                NestedQuery(
                    query=Exists(field="metadata.labels.workflows.argoproj.io/creator"),
                    path="metadata",
                ),
            ],
        )
        request = WorkflowSearchRequest(query=run_lookup_query, from_=from_, size=size)
        return WORKFLOW_INDEX_RUN_SEARCH, request


class WorkflowFindRuns:
    """Shared logic for finding workflow runs."""

    @staticmethod
    def prepare_request(query: Query, from_: int = 0, size: int = 100) -> tuple:
        """
        Prepare the request for finding workflow runs.

        :param query: query object to filter workflow runs
        :param from_: starting index of the search results
        :param size: maximum number of search results to return
        :returns: tuple of (endpoint, request_obj)
        """
        request = WorkflowSearchRequest(query=query, from_=from_, size=size)
        return WORKFLOW_INDEX_RUN_SEARCH, request

    @staticmethod
    def process_response(raw_json: Dict) -> Dict:
        """
        Process the API response and return the raw data for client-side model creation.

        :param raw_json: raw response from the API
        :returns: dictionary containing response data
        """
        return {
            "took": raw_json.get("took"),
            "hits": raw_json.get("hits"),
            "shards": raw_json.get("_shards"),
        }


class WorkflowRerun:
    """Shared logic for rerunning workflows."""

    @staticmethod
    def prepare_request(
        detail: WorkflowSearchResultDetail, use_package_endpoint: bool = False
    ) -> tuple:
        """
        Prepare the request for rerunning a workflow.

        :param detail: workflow details
        :param use_package_endpoint: whether to use package-workflows endpoint
        :returns: tuple of (endpoint, request_obj)
        """
        request = None
        if detail and detail.metadata:
            request = ReRunRequest(
                namespace=detail.metadata.namespace, resource_name=detail.metadata.name
            )
        endpoint = PACKAGE_WORKFLOW_RERUN if use_package_endpoint else WORKFLOW_RERUN
        return endpoint, request

    @staticmethod
    def process_response(raw_json: Dict) -> WorkflowRunResponse:
        """
        Process the API response into a WorkflowRunResponse.

        :param raw_json: raw response from the API
        :returns: WorkflowRunResponse object
        """
        return WorkflowRunResponse(**raw_json)


class WorkflowRun:
    """Shared logic for running workflows."""

    @staticmethod
    def prepare_request(
        workflow: Workflow,
        workflow_schedule: Optional[WorkflowSchedule] = None,
        use_package_endpoint: bool = False,
    ) -> tuple:
        """
        Prepare the request for running a workflow.

        :param workflow: workflow object to run
        :param workflow_schedule: optional schedule for the workflow
        :param use_package_endpoint: whether to use package-workflows endpoint
        :returns: tuple of (endpoint, request_obj)
        """
        if workflow_schedule:
            WorkflowScheduleUtils.add_schedule(workflow, workflow_schedule)
        endpoint = PACKAGE_WORKFLOW_RUN if use_package_endpoint else WORKFLOW_RUN
        return endpoint, workflow

    @staticmethod
    def process_response(raw_json: Dict) -> WorkflowResponse:
        """
        Process the API response into a WorkflowResponse.

        :param raw_json: raw response from the API
        :returns: WorkflowResponse object
        """
        return WorkflowResponse(**raw_json)


class WorkflowUpdate:
    """Shared logic for updating workflows."""

    @staticmethod
    def prepare_request(
        workflow: Workflow, use_package_endpoint: bool = False
    ) -> tuple:
        """
        Prepare the request for updating a workflow.

        :param workflow: workflow with revised configuration
        :param use_package_endpoint: whether to use package-workflows endpoint
        :returns: tuple of (endpoint, request_obj)
        """
        if use_package_endpoint:
            endpoint = PACKAGE_WORKFLOW_UPDATE.format_path(
                {"workflow_name": workflow.metadata and workflow.metadata.name}
            )
        else:
            endpoint = WORKFLOW_UPDATE.format_path(
                {"workflow_name": workflow.metadata and workflow.metadata.name}
            )
        return endpoint, workflow

    @staticmethod
    def process_response(raw_json: Dict) -> WorkflowResponse:
        """
        Process the API response into a WorkflowResponse.

        :param raw_json: raw response from the API
        :returns: WorkflowResponse object
        """
        return WorkflowResponse(**raw_json)


class WorkflowUpdateOwner:
    """Shared logic for updating workflow owner."""

    @staticmethod
    def prepare_request(workflow_name: str, username: str) -> tuple:
        """
        Prepare the request for updating workflow owner.

        :param workflow_name: name of the workflow to update
        :param username: username of the new owner
        :returns: tuple of (endpoint, query_params)
        """
        endpoint = WORKFLOW_CHANGE_OWNER.format_path({"workflow_name": workflow_name})
        query_params = {"username": username}
        return endpoint, query_params

    @staticmethod
    def process_response(raw_json: Dict) -> WorkflowResponse:
        """
        Process the API response into a WorkflowResponse.

        :param raw_json: raw response from the API
        :returns: WorkflowResponse object
        """
        return WorkflowResponse(**raw_json)


class WorkflowStop:
    """Shared logic for stopping workflows."""

    @staticmethod
    def prepare_request(workflow_run_id: str) -> tuple:
        """
        Prepare the request for stopping a workflow.

        :param workflow_run_id: identifier of the specific workflow run to stop
        :returns: tuple of (endpoint, request_obj)
        """
        endpoint = STOP_WORKFLOW_RUN.format_path({"workflow_run_id": workflow_run_id})
        return endpoint, None

    @staticmethod
    def process_response(raw_json: Dict) -> WorkflowRunResponse:
        """
        Process the API response into a WorkflowRunResponse.

        :param raw_json: raw response from the API
        :returns: WorkflowRunResponse object
        """
        return WorkflowParseResponse.parse_response(raw_json, WorkflowRunResponse)


class WorkflowDelete:
    """Shared logic for deleting workflows."""

    @staticmethod
    def prepare_request(
        workflow_name: str, use_package_endpoint: bool = False
    ) -> tuple:
        """
        Prepare the request for deleting a workflow.

        :param workflow_name: name of the workflow to delete
        :param use_package_endpoint: whether to use package-workflows endpoint
        :returns: tuple of (endpoint, request_obj)
        """
        if use_package_endpoint:
            endpoint = PACKAGE_WORKFLOW_ARCHIVE.format_path(
                {"workflow_name": workflow_name}
            )
        else:
            endpoint = WORKFLOW_ARCHIVE.format_path({"workflow_name": workflow_name})
        return endpoint, None


class WorkflowGetAllScheduledRuns:
    """Shared logic for getting all scheduled runs."""

    @staticmethod
    def prepare_request() -> tuple:
        """
        Prepare the request for getting all scheduled runs.

        :returns: tuple of (endpoint, request_obj)
        """
        return GET_ALL_SCHEDULE_RUNS, None

    @staticmethod
    def process_response(raw_json: Dict) -> List[WorkflowScheduleResponse]:
        """
        Process the API response into a list of WorkflowScheduleResponse.

        :param raw_json: raw response from the API
        :returns: list of WorkflowScheduleResponse objects
        """
        return WorkflowParseResponse.parse_response(
            raw_json.get("items"), WorkflowScheduleResponse
        )


class WorkflowGetScheduledRun:
    """Shared logic for getting a scheduled run."""

    @staticmethod
    def prepare_request(workflow_name: str) -> tuple:
        """
        Prepare the request for getting a scheduled run.

        :param workflow_name: name of the workflow
        :returns: tuple of (endpoint, request_obj)
        """
        endpoint = GET_SCHEDULE_RUN.format_path(
            {"workflow_name": f"{workflow_name}-cron"}
        )
        return endpoint, None

    @staticmethod
    def process_response(raw_json: Dict) -> WorkflowScheduleResponse:
        """
        Process the API response into a WorkflowScheduleResponse.

        :param raw_json: raw response from the API
        :returns: WorkflowScheduleResponse object
        """
        return WorkflowParseResponse.parse_response(raw_json, WorkflowScheduleResponse)


class WorkflowFindScheduleQuery:
    """Shared logic for finding scheduled query workflows."""

    @staticmethod
    def prepare_request(saved_query_id: str, max_results: int = 10) -> tuple:
        """
        Prepare the request for finding scheduled query workflows.

        :param saved_query_id: identifier of the saved query
        :param max_results: maximum number of results to retrieve
        :returns: tuple of (endpoint, request_obj)
        """
        query = Bool(
            filter=[
                NestedQuery(
                    path="metadata",
                    query=Prefix(
                        field="metadata.name.keyword", value=f"asq-{saved_query_id}"
                    ),
                ),
                NestedQuery(
                    path="metadata",
                    query=Term(
                        field="metadata.annotations.package.argoproj.io/name.keyword",
                        value="@atlan/schedule-query",
                    ),
                ),
            ]
        )
        request = WorkflowSearchRequest(query=query, size=max_results)
        return WORKFLOW_INDEX_SEARCH, request

    @staticmethod
    def process_response(raw_json: Dict) -> List[WorkflowSearchResult]:
        """
        Process the API response into a list of WorkflowSearchResult.

        :param raw_json: raw response from the API
        :returns: list of WorkflowSearchResult objects
        """
        response = WorkflowSearchResponse(**raw_json)
        return response.hits and response.hits.hits or []


class WorkflowReRunScheduleQuery:
    """Shared logic for re-running scheduled query workflows."""

    @staticmethod
    def prepare_request(schedule_query_id: str) -> tuple:
        """
        Prepare the request for re-running a scheduled query workflow.

        :param schedule_query_id: identifier of the schedule query
        :returns: tuple of (endpoint, request_obj)
        """
        request = ReRunRequest(namespace="default", resource_name=schedule_query_id)
        return WORKFLOW_OWNER_RERUN, request

    @staticmethod
    def process_response(raw_json: Dict) -> WorkflowRunResponse:
        """
        Process the API response into a WorkflowRunResponse.

        :param raw_json: raw response from the API
        :returns: WorkflowRunResponse object
        """
        return WorkflowRunResponse(**raw_json)


class WorkflowFindScheduleQueryBetween:
    """Shared logic for finding scheduled query workflows within a time range."""

    @staticmethod
    def prepare_request(
        request: ScheduleQueriesSearchRequest, missed: bool = False
    ) -> tuple:
        """
        Prepare the request for finding scheduled query workflows within a time range.

        :param request: request containing start and end dates
        :param missed: if True, search for missed scheduled query workflows
        :returns: tuple of (endpoint, query_params)
        """
        query_params = {
            "startDate": request.start_date,
            "endDate": request.end_date,
        }
        endpoint = (
            SCHEDULE_QUERY_WORKFLOWS_MISSED
            if missed
            else SCHEDULE_QUERY_WORKFLOWS_SEARCH
        )
        return endpoint, query_params

    @staticmethod
    def process_response(raw_json: Dict) -> Optional[List[WorkflowRunResponse]]:
        """
        Process the API response into a list of WorkflowRunResponse.

        :param raw_json: raw response from the API
        :returns: list of WorkflowRunResponse objects or None
        """
        return WorkflowParseResponse.parse_response(raw_json, WorkflowRunResponse)


class WorkflowScheduleUtils:
    """Utility functions for workflow scheduling."""

    _WORKFLOW_RUN_SCHEDULE = "orchestration.atlan.com/schedule"
    _WORKFLOW_RUN_TIMEZONE = "orchestration.atlan.com/timezone"

    @staticmethod
    def prepare_request(
        workflow: WorkflowSearchResultDetail, use_package_endpoint: bool = False
    ) -> tuple:
        """
        Prepare the request for workflow scheduling operations.

        :param workflow: workflow to schedule
        :param use_package_endpoint: whether to use package-workflows endpoint
        :returns: tuple of (endpoint, request_obj)
        """
        workflow_name = workflow.metadata and workflow.metadata.name
        if use_package_endpoint:
            endpoint = PACKAGE_WORKFLOW_UPDATE.format_path(
                {"workflow_name": workflow_name}
            )
        else:
            endpoint = WORKFLOW_UPDATE.format_path({"workflow_name": workflow_name})
        return endpoint, workflow

    @staticmethod
    def process_response(raw_json: Dict) -> WorkflowResponse:
        """
        Process the API response into a WorkflowResponse.

        :param raw_json: raw response from the API
        :returns: WorkflowResponse object
        """
        return WorkflowResponse(**raw_json)

    @classmethod
    def add_schedule(cls, workflow: Workflow, workflow_schedule: WorkflowSchedule):
        """
        Add required schedule parameters to the workflow object.

        :param workflow: workflow to add schedule to
        :param workflow_schedule: schedule configuration
        """
        if workflow.metadata and workflow.metadata.annotations:
            workflow.metadata.annotations.update(
                {
                    cls._WORKFLOW_RUN_SCHEDULE: workflow_schedule.cron_schedule,
                    cls._WORKFLOW_RUN_TIMEZONE: workflow_schedule.timezone,
                }
            )

    @classmethod
    def remove_schedule(cls, workflow: WorkflowSearchResultDetail):
        """
        Remove schedule parameters from the workflow object.

        :param workflow: workflow to remove schedule from
        """
        if workflow.metadata and workflow.metadata.annotations:
            workflow.metadata.annotations.pop(cls._WORKFLOW_RUN_SCHEDULE, None)


class WorkflowFindLatestRun:
    """Shared logic for finding the latest workflow run."""

    @staticmethod
    def prepare_request(workflow_name: str) -> tuple:
        """
        Prepare request for finding the latest run of a workflow.

        :param workflow_name: name of the workflow
        :returns: tuple of (endpoint, request_obj)
        """
        from pyatlan.model.search import Bool, NestedQuery, SortItem, SortOrder, Term

        query = Bool(
            filter=[
                NestedQuery(
                    query=Term(
                        field="spec.workflowTemplateRef.name.keyword",
                        value=workflow_name,
                    ),
                    path="spec",
                )
            ]
        )
        endpoint, request_obj = WorkflowFindRuns.prepare_request(query, size=1)
        # Add sorting to get the latest run
        request_obj.sort = [
            SortItem(field="status.startedAt", order=SortOrder.DESCENDING)
        ]
        return endpoint, request_obj

    @staticmethod
    def process_response(search_response) -> Optional[WorkflowSearchResult]:
        """
        Process the search response to extract the latest run.

        :param search_response: workflow search response object
        :returns: latest workflow run or None
        """
        return (
            search_response.hits.hits[0]
            if search_response.hits and search_response.hits.hits
            else None
        )


class WorkflowFindCurrentRun:
    """Shared logic for finding the current running workflow."""

    @staticmethod
    def prepare_request(workflow_name: str) -> tuple:
        """
        Prepare request for finding the current running run of a workflow.

        :param workflow_name: name of the workflow
        :returns: tuple of (endpoint, request_obj)
        """
        from pyatlan.model.search import Bool, NestedQuery, Term

        query = Bool(
            filter=[
                NestedQuery(
                    query=Term(
                        field="spec.workflowTemplateRef.name.keyword",
                        value=workflow_name,
                    ),
                    path="spec",
                )
            ]
        )
        endpoint, request_obj = WorkflowFindRuns.prepare_request(query, size=50)
        return endpoint, request_obj

    @staticmethod
    def process_response(search_response) -> Optional[WorkflowSearchResult]:
        """
        Process the search response to extract the current running workflow.

        :param search_response: workflow search response object
        :returns: current running workflow or None
        """
        from pyatlan.model.enums import AtlanWorkflowPhase

        if results := search_response.hits and search_response.hits.hits:
            for result in results:
                if result.status in {
                    AtlanWorkflowPhase.PENDING,
                    AtlanWorkflowPhase.RUNNING,
                }:
                    return result
        return None
