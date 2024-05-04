# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from logging import Logger
from time import sleep
from typing import List, Optional, Union, overload

from pydantic.v1 import ValidationError, parse_obj_as, validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    GET_ALL_SCHEDULE_RUNS,
    GET_SCHEDULE_RUN,
    STOP_WORKFLOW_RUN,
    WORKFLOW_ARCHIVE,
    WORKFLOW_INDEX_RUN_SEARCH,
    WORKFLOW_INDEX_SEARCH,
    WORKFLOW_RERUN,
    WORKFLOW_RUN,
    WORKFLOW_UPDATE,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanWorkflowPhase, WorkflowPackage
from pyatlan.model.search import Bool, NestedQuery, Prefix, Query, Term
from pyatlan.model.workflow import (
    ReRunRequest,
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

    @staticmethod
    def _parse_response(raw_json, response_type):
        try:
            if isinstance(raw_json, List):
                return parse_obj_as(List[response_type], raw_json)
            return parse_obj_as(response_type, raw_json)
        except ValidationError as err:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                raw_json, 200, str(err)
            ) from err

    @validate_arguments
    def _find_latest_run(self, workflow_name: str) -> Optional[WorkflowSearchResult]:
        """
        Find the latest run of a given workflow
        :param name: name of the workflow for which to find the current run
        :returns: the singular result giving the latest run of the workflow
        :raises AtlanError: on any API communication issue
        """
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
        response = self._find_runs(query, size=1)
        return results[0] if (results := response.hits.hits) else None

    @validate_arguments
    def _find_current_run(self, workflow_name: str) -> Optional[WorkflowSearchResult]:
        """
        Find the most current, still-running run of a given workflow

        :param name: name of the workflow for which to find the current run
        :returns: the singular result giving the latest currently-running
        run of the workflow, or `None` if it is not currently running
        :raises AtlanError: on any API communication issue
        """
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
        response = self._find_runs(query, size=50)
        if results := response.hits.hits:
            for result in results:
                if result.status in {
                    AtlanWorkflowPhase.PENDING,
                    AtlanWorkflowPhase.RUNNING,
                }:
                    return result
        return None

    def _find_runs(
        self,
        query: Query,
        from_: int = 0,
        size: int = 100,
    ) -> WorkflowSearchResponse:
        """
        Retrieve existing workflow runs.

        :param query: query object to filter workflow runs.
        :param from_: starting index of the search results (default: `0`).
        :param size: maximum number of search results to return (default: `100`).
        :returns: a response containing the matching workflow runs.
        :raises AtlanError: on any API communication issue
        """
        request = WorkflowSearchRequest(query=query, from_=from_, size=size)
        raw_json = self._client._call_api(
            WORKFLOW_INDEX_RUN_SEARCH,
            request_obj=request,
        )
        return WorkflowSearchResponse(**raw_json)

    def _add_schedule(
        self,
        workflow: Workflow,
        workflow_schedule: WorkflowSchedule,
    ):
        """
        Adds required schedule parameters to the workflow object.
        """
        workflow.metadata.annotations and workflow.metadata.annotations.update(
            {
                self._WORKFLOW_RUN_SCHEDULE: workflow_schedule.cron_schedule,
                self._WORKFLOW_RUN_TIMEZONE: workflow_schedule.timezone,
            }
        )

    @validate_arguments
    def find_by_type(
        self, prefix: WorkflowPackage, max_results: int = 10
    ) -> List[WorkflowSearchResult]:
        """
        Find workflows based on their type (prefix).
        Note: Only workflows that have been run will be found.

        :param prefix: name of the specific workflow to find (for example CONNECTION_DELETE)
        :param max_results: the maximum number of results to retrieve
        :returns: the list of workflows of the provided type, with the most-recently created first
        :raises ValidationError: If the provided prefix is invalid workflow package
        :raises AtlanError: on any API communication issue
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

    def _handle_workflow_types(self, workflow):
        if isinstance(workflow, WorkflowPackage):
            if results := self.find_by_type(workflow):
                detail = results[0].source
            else:
                raise ErrorCode.NO_PRIOR_RUN_AVAILABLE.exception_with_parameters(
                    workflow
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

    @validate_arguments
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
        detail = self._handle_workflow_types(workflow)
        if idempotent and detail.metadata.name:
            # Introducing a delay before checking the current workflow run
            # since it takes some time to start or stop
            sleep(10)
            if (
                current_run_details := self._find_current_run(
                    workflow_name=detail.metadata.name
                )
            ) and current_run_details.source.status:
                return WorkflowRunResponse(
                    metadata=current_run_details.source.metadata,
                    spec=current_run_details.source.spec,
                    status=current_run_details.source.status,
                )

        request = ReRunRequest(
            namespace=detail.metadata.namespace, resource_name=detail.metadata.name
        )
        raw_json = self._client._call_api(
            WORKFLOW_RERUN,
            request_obj=request,
        )
        return WorkflowRunResponse(**raw_json)

    @validate_arguments
    def run(
        self, workflow: Workflow, workflow_schedule: Optional[WorkflowSchedule] = None
    ) -> WorkflowResponse:
        """
        Run the Atlan workflow with a specific configuration.

        Note: This method should only be used to create the workflow for the first time.
        Each invocation creates a new connection and new assets within that connection.
        Running the workflow multiple times with the same configuration may lead to duplicate assets.
        Consider using the "rerun()" method instead to re-execute an existing workflow.

        :param workflow: The workflow to run.
        :param workflow_schedule: (Optional) a WorkflowSchedule object containing:
            - A cron schedule expression, e.g: `5 4 * * *`.
            - The time zone for the cron schedule, e.g: `Europe/Paris`.

        :returns: Details of the workflow run.
        :raises ValidationError: If the provided `workflow` is invalid.
        :raises AtlanError: on any API communication issue.
        """
        if workflow_schedule:
            self._add_schedule(workflow, workflow_schedule)
        raw_json = self._client._call_api(
            WORKFLOW_RUN,
            request_obj=workflow,
        )
        return WorkflowResponse(**raw_json)

    @validate_arguments
    def update(self, workflow: Workflow) -> WorkflowResponse:
        """
        Update a given workflow's configuration.

        :param workflow: request full details of the workflow's revised configuration.
        :returns: the updated workflow configuration.
        :raises ValidationError: If the provided `workflow` is invalid.
        :raises AtlanError: on any API communication issue.
        """
        raw_json = self._client._call_api(
            WORKFLOW_UPDATE.format_path({"workflow_name": workflow.metadata.name}),
            request_obj=workflow,
        )
        return WorkflowResponse(**raw_json)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    def monitor(
        self, workflow_response: WorkflowResponse, logger: Optional[Logger] = None
    ) -> Optional[AtlanWorkflowPhase]:
        """
        Monitor the status of the workflow's run.

        :param workflow_response: The workflow_response returned from running the workflow
        :param logger: the logger to log status information
        (logging.INFO for summary info. logging:DEBUG for detail info)
        :returns: the status at completion or None if the workflow wasn't run
        :raises ValidationError: If the provided `workflow_response`, `logger` is invalid
        :raises AtlanError: on any API communication issue
        """
        if workflow_response.metadata and workflow_response.metadata.name:
            name = workflow_response.metadata.name
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
        if logger:
            logger.info("Skipping workflow monitoring — nothing to monitor.")
        return None

    def _get_run_details(self, name: str) -> Optional[WorkflowSearchResult]:
        return self._find_latest_run(workflow_name=name)

    @validate_arguments
    def get_runs(
        self,
        workflow_name: str,
        workflow_phase: AtlanWorkflowPhase,
        from_: int = 0,
        size: int = 100,
    ) -> Optional[List[WorkflowSearchResult]]:
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
        response = self._find_runs(query)
        return results if (results := response.hits.hits) else None

    @validate_arguments
    def stop(
        self,
        workflow_run_id: str,
    ) -> WorkflowRunResponse:
        """
        Stop the provided, running workflow.

        :param workflow_run_id: identifier of the specific workflow run
        to stop eg: `atlan-snowflake-miner-1714638976-9wfxz`.
        :returns: details of the stopped workflow.
        :raises AtlanError: on any API communication issue.
        """
        raw_json = self._client._call_api(
            STOP_WORKFLOW_RUN.format_path({"workflow_run_id": workflow_run_id}),
        )
        return self._parse_response(raw_json, WorkflowRunResponse)

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
        self._client._call_api(
            WORKFLOW_ARCHIVE.format_path({"workflow_name": workflow_name}),
        )

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

    @validate_arguments
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

        workflow_to_update = self._handle_workflow_types(workflow)
        self._add_schedule(workflow_to_update, workflow_schedule)
        raw_json = self._client._call_api(
            WORKFLOW_UPDATE.format_path(
                {"workflow_name": workflow_to_update.metadata.name}
            ),
            request_obj=workflow_to_update,
        )
        return WorkflowResponse(**raw_json)

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

    @validate_arguments
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
        workflow_to_update = self._handle_workflow_types(workflow)
        workflow_to_update.metadata.annotations and workflow_to_update.metadata.annotations.pop(
            self._WORKFLOW_RUN_SCHEDULE, None
        )
        raw_json = self._client._call_api(
            WORKFLOW_UPDATE.format_path(
                {"workflow_name": workflow_to_update.metadata.name}
            ),
            request_obj=workflow_to_update,
        )
        return WorkflowResponse(**raw_json)

    @validate_arguments
    def get_all_scheduled_runs(self) -> List[WorkflowScheduleResponse]:
        """
        Retrieve all scheduled runs for workflows.

        :returns: a list of scheduled workflow runs.
        :raises AtlanError: on any API communication issue.
        """
        raw_json = self._client._call_api(GET_ALL_SCHEDULE_RUNS)
        return self._parse_response(raw_json.get("items"), WorkflowScheduleResponse)

    @validate_arguments
    def get_scheduled_run(self, workflow_name: str) -> WorkflowScheduleResponse:
        """
        Retrieve existing scheduled run for a workflow.

        :param workflow_name: name of the workflow as displayed
        in the UI (e.g: `atlan-snowflake-miner-1714638976`).
        :returns: a list of scheduled workflow runs.
        :raises AtlanError: on any API communication issue.
        """
        raw_json = self._client._call_api(
            GET_SCHEDULE_RUN.format_path({"workflow_name": f"{workflow_name}-cron"}),
        )
        return self._parse_response(raw_json, WorkflowScheduleResponse)
