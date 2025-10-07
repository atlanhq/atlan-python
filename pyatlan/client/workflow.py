# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from logging import Logger
from time import sleep
from typing import List, Optional, Union, overload

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    WorkflowDelete,
    WorkflowFindById,
    WorkflowFindByType,
    WorkflowFindCurrentRun,
    WorkflowFindLatestRun,
    WorkflowFindRuns,
    WorkflowFindScheduleQuery,
    WorkflowFindScheduleQueryBetween,
    WorkflowGetAllScheduledRuns,
    WorkflowGetScheduledRun,
    WorkflowParseResponse,
    WorkflowRerun,
    WorkflowReRunScheduleQuery,
    WorkflowRun,
    WorkflowScheduleUtils,
    WorkflowStop,
    WorkflowUpdate,
    WorkflowUpdateOwner,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanWorkflowPhase, WorkflowPackage
from pyatlan.model.search import Bool, Exists, NestedQuery, Range, Term, Terms
from pyatlan.model.workflow import (
    ScheduleQueriesSearchRequest,
    Workflow,
    WorkflowResponse,
    WorkflowRunResponse,
    WorkflowSchedule,
    WorkflowScheduleResponse,
    WorkflowSearchResponse,
    WorkflowSearchResult,
    WorkflowSearchResultDetail,
)
from pyatlan.utils import validate_type

MONITOR_SLEEP_SECONDS = 5


class WorkflowClient:
    """
    This class can be used to retrieve information and rerun workflows. This class does not need to be instantiated
    directly but can be obtained through the workflow property of AtlanClient.
    """

    _WORKFLOW_RUN_SCHEDULE = "orchestration.atlan.com/schedule"
    _WORKFLOW_RUN_TIMEZONE = "orchestration.atlan.com/timezone"

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def find_by_type(
        self, prefix: WorkflowPackage, max_results: int = 10
    ) -> List[WorkflowSearchResult]:
        """
        Find workflows based on their type (prefix). Note: Only workflows that have been run will be found.

        :param prefix: name of the specific workflow to find (for example CONNECTION_DELETE)
        :param max_results: the maximum number of results to retrieve
        :returns: the list of workflows of the provided type, with the most-recently created first
        :raises ValidationError: If the provided prefix is invalid workflow package
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowFindByType.prepare_request(prefix, max_results)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowFindByType.process_response(raw_json)

    @validate_arguments
    def find_by_id(self, id: str) -> Optional[WorkflowSearchResult]:
        """
        Find workflows based on their ID (e.g: `atlan-snowflake-miner-1714638976`)
        Note: Only workflows that have been run will be found

        :param id: the ID of the workflow to find
        :returns: the workflow with the provided ID, or None if none is found
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowFindById.prepare_request(id)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowFindById.process_response(raw_json)

    @validate_arguments
    def find_run_by_id(self, id: str) -> Optional[WorkflowSearchResult]:
        """
        Find workflows runs based on their ID (e.g: `atlan-snowflake-miner-1714638976-t7s8b`)
        Note: Only workflow runs will be found

        :param id: the ID of the workflow run to find
        :returns: the workflow run with the provided ID, or None if none is found
        :raises AtlanError: on any API communication issue
        """

        query = Bool(
            filter=[
                Term(
                    field="_id",
                    value=id,
                ),
            ]
        )
        response = self._find_runs(query, size=1)
        return results[0] if (results := response.hits and response.hits.hits) else None

    @validate_arguments
    def find_runs_by_status_and_time_range(
        self,
        status: List[AtlanWorkflowPhase],
        started_at: Optional[str] = None,
        finished_at: Optional[str] = None,
        from_: int = 0,
        size: int = 100,
    ) -> WorkflowSearchResponse:
        """
        Retrieves a WorkflowSearchResponse object containing workflow runs based on their status and time range.

        :param status: list of the workflow statuses to filter
        :param started_at: (optional) lower bound on 'status.startedAt' (e.g 'now-2h')
        :param finished_at: (optional) lower bound on 'status.finishedAt' (e.g 'now-1h')
        :param from_:(optional) starting index of the search results (default: `0`).
        :param size: (optional) maximum number of search results to return (default: `100`).
        :returns: a WorkflowSearchResponse object containing a list of workflows matching the filters
        :raises ValidationError: if inputs are invalid
        :raises AtlanError: on any API communication issue
        """
        # Use the original implementation since this has a complex custom query

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
        run_lookup_results = self._find_runs(
            query=run_lookup_query, from_=from_, size=size
        )
        return run_lookup_results

    @validate_arguments
    def _find_latest_run(self, workflow_name: str) -> Optional[WorkflowSearchResult]:
        """
        Find the most recent run for a given workflow

        :param name: name of the workflow for which to find the current run
        :returns: the singular result giving the latest run of the workflow
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowFindLatestRun.prepare_request(workflow_name)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        response_data = WorkflowFindRuns.process_response(raw_json)

        # Create response with minimal parameters needed for pagination
        response = WorkflowSearchResponse(
            client=self._client,
            endpoint=endpoint,
            criteria=request_obj.query,
            start=0,
            size=1,
            **response_data,
        )
        return WorkflowFindLatestRun.process_response(response)

    @validate_arguments
    def _find_current_run(self, workflow_name: str) -> Optional[WorkflowSearchResult]:
        """
        Find the most current, still-running run of a given workflow

        :param name: name of the workflow for which to find the current run
        :returns: the singular result giving the latest currently-running
        run of the workflow, or `None` if it is not currently running
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowFindCurrentRun.prepare_request(workflow_name)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        response_data = WorkflowFindRuns.process_response(raw_json)

        # Create response with minimal parameters needed for pagination
        response = WorkflowSearchResponse(
            client=self._client,
            endpoint=endpoint,
            criteria=request_obj.query,
            start=0,
            size=50,
            **response_data,
        )
        return WorkflowFindCurrentRun.process_response(response)

    def _find_runs(
        self,
        query,
        from_: int = 0,
        size: int = 100,
    ) -> WorkflowSearchResponse:
        """
        Retrieve existing workflow runs.

        :param query: query object to filter workflow runs.
        :param from_: starting point for pagination
        :param size: maximum number of results to retrieve
        :returns: the workflow runs
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowFindRuns.prepare_request(query, from_, size)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        response_data = WorkflowFindRuns.process_response(raw_json)

        return WorkflowSearchResponse(
            client=self._client,
            endpoint=endpoint,
            criteria=query,
            start=from_,
            size=size,
            **response_data,
        )

    def _add_schedule(
        self,
        workflow: Workflow,
        workflow_schedule: WorkflowSchedule,
    ):
        """
        Adds required schedule parameters to the workflow object.
        """
        workflow.metadata and workflow.metadata.annotations and workflow.metadata.annotations.update(
            {
                self._WORKFLOW_RUN_SCHEDULE: workflow_schedule.cron_schedule,
                self._WORKFLOW_RUN_TIMEZONE: workflow_schedule.timezone,
            }
        )

    def _handle_workflow_types(self, workflow):
        if isinstance(workflow, WorkflowPackage):
            if results := self.find_by_type(workflow):
                detail = results[0].source
            else:
                raise ErrorCode.NO_PRIOR_RUN_AVAILABLE.exception_with_parameters(
                    workflow.value
                )
        elif isinstance(workflow, WorkflowSearchResult):
            detail = workflow.source
        else:
            detail = workflow
        return detail

    @overload
    def rerun(
        self, workflow: WorkflowPackage, idempotent: bool = False
    ) -> WorkflowRunResponse: ...

    @overload
    def rerun(
        self, workflow: WorkflowSearchResultDetail, idempotent: bool = False
    ) -> WorkflowRunResponse: ...

    @overload
    def rerun(
        self, workflow: WorkflowSearchResult, idempotent: bool = False
    ) -> WorkflowRunResponse: ...

    def rerun(
        self,
        workflow: Union[
            WorkflowPackage, WorkflowSearchResultDetail, WorkflowSearchResult
        ],
        idempotent: bool = False,
    ) -> WorkflowRunResponse:
        """
        Rerun the workflow immediately.
        Note: this must be a workflow that was previously run.

        :param workflow: The workflow to rerun.
        :param idempotent: If `True`, the workflow will only be rerun if it is not already currently running
        :returns: the details of the workflow run (if `idempotent`, will return details of the already-running workflow)
        :raises ValidationError: If the provided workflow is invalid
        :raises InvalidRequestException: If no prior runs are available for the provided workflow
        :raises AtlanError: on any API communication issue
        """
        validate_type(
            name="workflow",
            _type=(WorkflowPackage, WorkflowSearchResultDetail, WorkflowSearchResult),
            value=workflow,
        )
        detail = self._handle_workflow_types(workflow)
        if idempotent and detail and detail.metadata and detail.metadata.name:
            # Introducing a delay before checking the current workflow run
            # since it takes some time to start or stop
            sleep(10)
            if (
                (
                    current_run_details := self._find_current_run(
                        workflow_name=detail.metadata.name
                    )
                )
                and current_run_details.source
                and current_run_details.source.metadata
                and current_run_details.source.spec
                and current_run_details.source.status
            ):
                return WorkflowParseResponse.parse_response(
                    {
                        "metadata": current_run_details.source.metadata,
                        "spec": current_run_details.source.spec,
                        "status": current_run_details.source.status,
                    },
                    WorkflowRunResponse,
                )
        # Check if user is API token user to determine endpoint
        use_package_endpoint = not self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        endpoint, request_obj = WorkflowRerun.prepare_request(
            detail, use_package_endpoint
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowRerun.process_response(raw_json)

    @overload
    def run(
        self, workflow: Workflow, workflow_schedule: Optional[WorkflowSchedule] = None
    ) -> WorkflowResponse: ...

    @overload
    def run(
        self, workflow: str, workflow_schedule: Optional[WorkflowSchedule] = None
    ) -> WorkflowResponse: ...

    def run(
        self,
        workflow: Union[Workflow, str],
        workflow_schedule: Optional[WorkflowSchedule] = None,
    ) -> WorkflowResponse:
        """
        Run the Atlan workflow with a specific configuration.

        Note: This method should only be used to create the workflow for the first time.
        Each invocation creates a new connection and new assets within that connection.
        Running the workflow multiple times with the same configuration may lead to duplicate assets.
        Consider using the "rerun()" method instead to re-execute an existing workflow.

        :param workflow: workflow object to run or a raw workflow JSON string.
        :param workflow_schedule: (Optional) a WorkflowSchedule object containing:
            - A cron schedule expression, e.g: `5 4 * * *`.
            - The time zone for the cron schedule, e.g: `Europe/Paris`.

        :returns: Details of the workflow run.
        :raises ValidationError: If the provided `workflow` is invalid.
        :raises AtlanError: on any API communication issue.
        """
        validate_type(name="workflow", _type=(Workflow, str), value=workflow)
        validate_type(
            name="workflow_schedule",
            _type=(WorkflowSchedule, None),
            value=workflow_schedule,
        )
        if isinstance(workflow, str):
            workflow = Workflow.parse_raw(workflow)
        if workflow_schedule:
            self._add_schedule(workflow, workflow_schedule)
        # Check if user is API token user to determine endpoint
        use_package_endpoint = not self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        endpoint, request_obj = WorkflowRun.prepare_request(
            workflow, workflow_schedule, use_package_endpoint
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowRun.process_response(raw_json)

    @validate_arguments
    def update(self, workflow: Workflow) -> WorkflowResponse:
        """
        Update a given workflow's configuration.

        :param workflow: request full details of the workflow's revised configuration.
        :returns: the updated workflow configuration.
        :raises ValidationError: If the provided `workflow` is invalid.
        :raises AtlanError: on any API communication issue
        """
        # Check if user is API token user to determine endpoint
        use_package_endpoint = not self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        endpoint, request_obj = WorkflowUpdate.prepare_request(
            workflow, use_package_endpoint
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowUpdate.process_response(raw_json)

    @validate_arguments
    def update_owner(self, workflow_name: str, username: str) -> WorkflowResponse:
        """
        Update the owner of a workflow.

        :param workflow_name: name of the workflow for which we want to update owner
        :param username: new username of the user who should own the workflow
        :returns: workflow response details
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowUpdateOwner.prepare_request(
            workflow_name, username
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowUpdateOwner.process_response(raw_json)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def monitor(
        self,
        workflow_response: Optional[WorkflowResponse] = None,
        logger: Optional[Logger] = None,
        workflow_name: Optional[str] = None,
    ) -> Optional[AtlanWorkflowPhase]:
        """
        Monitor a workflow until its completion (or the script terminates).

        :param workflow_response: The workflow_response returned from running the workflow
        :param logger: the logger to log status information
        (logging.INFO for summary info. logging.DEBUG for detail info)
        :param workflow_name: name of the workflow to be monitored
        :returns: the status at completion or None if the workflow wasn't run
        :raises ValidationError: If the provided `workflow_response`, `logger` is invalid
        :raises AtlanError: on any API communication issue
        """
        name = workflow_name or (
            workflow_response.metadata.name
            if workflow_response and workflow_response.metadata
            else None
        )

        if not name:
            if logger:
                logger.info("Skipping workflow monitoring — nothing to monitor.")
            return None

        status: Optional[AtlanWorkflowPhase] = None
        while status not in {
            AtlanWorkflowPhase.SUCCESS,
            AtlanWorkflowPhase.ERROR,
            AtlanWorkflowPhase.FAILED,
        }:
            sleep(MONITOR_SLEEP_SECONDS)
            if run_details := self._get_run_details(name):
                status = run_details.status
                if logger:
                    logger.debug("Workflow status: %s", status)

        if logger:
            logger.info("Workflow completion status: %s", status)
        return status

    def _get_run_details(self, name: str) -> Optional[WorkflowSearchResult]:
        return self._find_latest_run(workflow_name=name)

    def get_runs(
        self,
        workflow_name: str,
        workflow_phase: AtlanWorkflowPhase,
        from_: int = 0,
        size: int = 100,
    ) -> Optional[WorkflowSearchResponse]:
        """
        Retrieves all workflow runs.

        :param workflow_name: name of the workflow as displayed
        in the UI (e.g: `atlan-snowflake-miner-1714638976`).
        :param workflow_phase: phase of the given workflow (e.g: Succeeded, Running, Failed, etc).
        :param from_: starting index of the search results (default: `0`).
        :param size: maximum number of search results to return (default: `100`).
        :returns: a list of runs of the given workflow.
        :raises AtlanError: on any API communication issue.
        """
        # Note: this method uses a custom query, so we'll keep the existing implementation

        query = Bool(
            must=[
                NestedQuery(
                    query=Term(
                        field="spec.workflowTemplateRef.name.keyword",
                        value=workflow_name,
                    ),
                    path="spec",
                )
            ],
            filter=[Term(field="status.phase.keyword", value=workflow_phase.value)],
        )
        response = self._find_runs(query, from_=from_, size=size)
        return response

    @validate_arguments
    def stop(
        self,
        workflow_run_id: str,
    ) -> WorkflowRunResponse:
        """
        Stop the provided, running workflow.

        :param workflow_run_id: identifier of the specific workflow run
        :returns: the stopped workflow run
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowStop.prepare_request(workflow_run_id)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowStop.process_response(raw_json)

    @validate_arguments
    def delete(
        self,
        workflow_name: str,
    ) -> None:
        """
        Archive (delete) the provided workflow.

        :param workflow_name: name of the workflow as displayed
        in the UI (e.g: `atlan-snowflake-miner-1714638976`).
        :raises AtlanError: on any API communication issue.
        """
        # Check if user is API token user to determine endpoint
        use_package_endpoint = not self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        endpoint, request_obj = WorkflowDelete.prepare_request(
            workflow_name, use_package_endpoint
        )
        self._client._call_api(endpoint, request_obj=request_obj)

    @overload
    def add_schedule(
        self, workflow: WorkflowResponse, workflow_schedule: WorkflowSchedule
    ) -> WorkflowResponse: ...

    @overload
    def add_schedule(
        self, workflow: WorkflowPackage, workflow_schedule: WorkflowSchedule
    ) -> WorkflowResponse: ...

    @overload
    def add_schedule(
        self, workflow: WorkflowSearchResult, workflow_schedule: WorkflowSchedule
    ) -> WorkflowResponse: ...

    @overload
    def add_schedule(
        self, workflow: WorkflowSearchResultDetail, workflow_schedule: WorkflowSchedule
    ) -> WorkflowResponse: ...

    def add_schedule(
        self,
        workflow: Union[
            WorkflowResponse,
            WorkflowPackage,
            WorkflowSearchResult,
            WorkflowSearchResultDetail,
        ],
        workflow_schedule: WorkflowSchedule,
    ) -> WorkflowResponse:
        """
        Add a schedule for an existing workflow run.

        :param workflow: existing workflow run to schedule.
        :param workflow_schedule: a WorkflowSchedule object containing:
            - A cron schedule expression, e.g: `5 4 * * *`.
            - The time zone for the cron schedule, e.g: `Europe/Paris`.

        :returns: a scheduled workflow.
        :raises AtlanError: on any API communication issue.
        """
        validate_type(
            name="workflow",
            _type=(
                WorkflowResponse,
                WorkflowPackage,
                WorkflowSearchResult,
                WorkflowSearchResultDetail,
            ),
            value=workflow,
        )
        workflow_to_update = self._handle_workflow_types(workflow)
        self._add_schedule(workflow_to_update, workflow_schedule)
        # Check if user is API token user to determine endpoint
        use_package_endpoint = not self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        endpoint, request_obj = WorkflowScheduleUtils.prepare_request(
            workflow_to_update, use_package_endpoint
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowScheduleUtils.process_response(raw_json)

    @overload
    def remove_schedule(self, workflow: WorkflowResponse) -> WorkflowResponse: ...

    @overload
    def remove_schedule(self, workflow: WorkflowPackage) -> WorkflowResponse: ...

    @overload
    def remove_schedule(self, workflow: WorkflowSearchResult) -> WorkflowResponse: ...

    @overload
    def remove_schedule(
        self, workflow: WorkflowSearchResultDetail
    ) -> WorkflowResponse: ...

    def remove_schedule(
        self,
        workflow: Union[
            WorkflowResponse,
            WorkflowPackage,
            WorkflowSearchResult,
            WorkflowSearchResultDetail,
        ],
    ) -> WorkflowResponse:
        """
        Remove a scheduled run from an existing workflow run.

        :param workflow_run: existing workflow run to remove the schedule from.
        :returns: a workflow.
        :raises AtlanError: on any API communication issue.
        """
        validate_type(
            name="workflow",
            _type=(
                WorkflowResponse,
                WorkflowPackage,
                WorkflowSearchResult,
                WorkflowSearchResultDetail,
            ),
            value=workflow,
        )
        workflow_to_update = self._handle_workflow_types(workflow)
        WorkflowScheduleUtils.remove_schedule(workflow_to_update)
        # Check if user is API token user to determine endpoint
        use_package_endpoint = not self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        endpoint, request_obj = WorkflowScheduleUtils.prepare_request(
            workflow_to_update, use_package_endpoint
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowScheduleUtils.process_response(raw_json)

    def get_all_scheduled_runs(self) -> List[WorkflowScheduleResponse]:
        """
        Get the details of scheduled run for all workflow.

        :returns: list of all the workflow schedules
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowGetAllScheduledRuns.prepare_request()
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowGetAllScheduledRuns.process_response(raw_json)

    @validate_arguments
    def get_scheduled_run(self, workflow_name: str) -> WorkflowScheduleResponse:
        """
        Get the details of scheduled run for a specific workflow.

        :param workflow_name: name of the workflow for which we want the scheduled run details
        :returns: details of the workflow schedule
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowGetScheduledRun.prepare_request(workflow_name)
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowGetScheduledRun.process_response(raw_json)

    @validate_arguments
    def find_schedule_query(
        self, saved_query_id: str, max_results: int = 10
    ) -> List[WorkflowSearchResult]:
        """
        Find scheduled query workflows by their saved query identifier.

        :param saved_query_id: identifier of the saved query.
        :param max_results: maximum number of results to retrieve. Defaults to `10`.
        :raises AtlanError: on any API communication issue.
        :returns: a list of scheduled query workflows.
        """
        endpoint, request_obj = WorkflowFindScheduleQuery.prepare_request(
            saved_query_id, max_results
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowFindScheduleQuery.process_response(raw_json)

    @validate_arguments
    def re_run_schedule_query(self, schedule_query_id: str) -> WorkflowRunResponse:
        """
        Re-run a scheduled query.

        :param schedule_query_id: ID of the scheduled query to re-run
        :returns: the workflow run response
        :raises AtlanError: on any API communication issue
        """
        endpoint, request_obj = WorkflowReRunScheduleQuery.prepare_request(
            schedule_query_id
        )
        raw_json = self._client._call_api(endpoint, request_obj=request_obj)
        return WorkflowReRunScheduleQuery.process_response(raw_json)

    @validate_arguments
    def find_schedule_query_between(
        self, request: ScheduleQueriesSearchRequest, missed: bool = False
    ) -> Optional[List[WorkflowRunResponse]]:
        """
        Find scheduled query workflows within the specified duration.

        :param request: a `ScheduleQueriesSearchRequest` object containing
        start and end dates in ISO 8601 format (e.g: `2024-03-25T16:30:00.000+05:30`).
        :param missed: if `True`, perform a search for missed
        scheduled query workflows. Defaults to `False`.
        :raises AtlanError: on any API communication issue.
        :returns: a list of scheduled query workflows found within the specified duration.
        """
        endpoint, request_obj = WorkflowFindScheduleQueryBetween.prepare_request(
            request, missed
        )
        raw_json = self._client._call_api(endpoint, query_params=request_obj)
        return WorkflowFindScheduleQueryBetween.process_response(raw_json)
