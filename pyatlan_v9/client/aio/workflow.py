# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

from __future__ import annotations

import asyncio
import json
from logging import Logger
from typing import List, Optional, Union, overload

import msgspec

from pyatlan.client.common import (
    AsyncApiCaller,
    WorkflowDelete,
    WorkflowFindScheduleQueryBetween,
    WorkflowGetAllScheduledRuns,
    WorkflowGetScheduledRun,
    WorkflowStop,
    WorkflowUpdateOwner,
)
from pyatlan.client.constants import (
    PACKAGE_WORKFLOW_RERUN,
    PACKAGE_WORKFLOW_RUN,
    PACKAGE_WORKFLOW_UPDATE,
    WORKFLOW_INDEX_RUN_SEARCH,
    WORKFLOW_INDEX_SEARCH,
    WORKFLOW_OWNER_RERUN,
    WORKFLOW_RERUN,
    WORKFLOW_RUN,
    WORKFLOW_UPDATE,
)
from pyatlan.errors import ErrorCode
from pyatlan.utils import validate_type
from pyatlan_v9.model.aio.workflow import AsyncWorkflowSearchResponse
from pyatlan_v9.model.enums import AtlanWorkflowPhase, WorkflowPackage
from pyatlan_v9.model.search import (
    Bool,
    Exists,
    NestedQuery,
    Prefix,
    Range,
    Regexp,
    Term,
    Terms,
)
from pyatlan_v9.model.workflow import (
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
from pyatlan_v9.validate import validate_arguments

MONITOR_SLEEP_SECONDS = 5

_DEFAULT_SORT = [
    {"metadata.creationTimestamp": {"order": "desc", "nested": {"path": "metadata"}}}
]

_LATEST_RUN_SORT = [{"status.startedAt": {"order": "desc"}}]


class V9AsyncWorkflowClient:
    """
    This class can be used to retrieve information and rerun workflows. This class does not need to be instantiated
    directly but can be obtained through the workflow property of AsyncAtlanClient.
    """

    _WORKFLOW_RUN_SCHEDULE = "orchestration.atlan.com/schedule"
    _WORKFLOW_RUN_TIMEZONE = "orchestration.atlan.com/timezone"

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def find_by_type(
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
        regex = prefix.value.replace("-", "[-]") + "[-][0-9]{10}"
        query = Bool(
            filter=[
                NestedQuery(
                    query=Regexp(field="metadata.name.keyword", value=regex),
                    path="metadata",
                )
            ]
        )
        request = WorkflowSearchRequest(
            query=query.to_dict(), size=max_results, sort=_DEFAULT_SORT
        )
        raw_json = await self._client._call_api(
            WORKFLOW_INDEX_SEARCH, request_obj=request
        )
        response = msgspec.convert(raw_json, WorkflowSearchResponse, strict=False)
        return response.hits and response.hits.hits or []

    @validate_arguments
    async def find_by_id(self, id: str) -> Optional[WorkflowSearchResult]:
        """
        Find workflows based on their ID (e.g: `atlan-snowflake-miner-1714638976`)
        Note: Only workflows that have been run will be found

        :param id: the ID of the workflow to find
        :returns: the workflow with the provided ID, or None if none is found
        :raises AtlanError: on any API communication issue
        """
        query = Bool(
            filter=[
                NestedQuery(
                    query=Bool(must=[Term(field="metadata.name.keyword", value=id)]),
                    path="metadata",
                )
            ]
        )
        request = WorkflowSearchRequest(
            query=query.to_dict(), size=1, sort=_DEFAULT_SORT
        )
        raw_json = await self._client._call_api(
            WORKFLOW_INDEX_SEARCH, request_obj=request
        )
        response = msgspec.convert(raw_json, WorkflowSearchResponse, strict=False)
        results = response.hits and response.hits.hits
        return results[0] if results else None

    @validate_arguments
    async def find_run_by_id(self, id: str) -> Optional[WorkflowSearchResult]:
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
        response = await self._find_runs(query, size=1)
        return results[0] if (results := response.hits and response.hits.hits) else None

    @validate_arguments
    async def find_runs_by_status_and_time_range(
        self,
        status: List[AtlanWorkflowPhase],
        started_at: Optional[str] = None,
        finished_at: Optional[str] = None,
        from_: int = 0,
        size: int = 100,
    ) -> AsyncWorkflowSearchResponse:
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
        time_filters = []
        if started_at:
            time_filters.append(Range(field="status.startedAt", gte=started_at))
        if finished_at:
            time_filters.append(Range(field="status.finishedAt", lte=finished_at))

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
        return await self._find_runs(query=run_lookup_query, from_=from_, size=size)

    async def _find_latest_run(
        self, workflow_name: str
    ) -> Optional[WorkflowSearchResult]:
        """
        Find the most recent run for a given workflow

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
        query_dict = query.to_dict()
        request = WorkflowSearchRequest(
            query=query_dict, from_=0, size=1, sort=_LATEST_RUN_SORT
        )
        raw_json = await self._client._call_api(
            WORKFLOW_INDEX_RUN_SEARCH, request_obj=request
        )
        response = msgspec.convert(raw_json, AsyncWorkflowSearchResponse, strict=False)
        response._client = self._client
        response._endpoint = WORKFLOW_INDEX_RUN_SEARCH
        response._criteria = query_dict
        response._start = 0
        response._size = 1
        return response.hits.hits[0] if response.hits and response.hits.hits else None

    async def _find_current_run(
        self, workflow_name: str
    ) -> Optional[WorkflowSearchResult]:
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
        query_dict = query.to_dict()
        request = WorkflowSearchRequest(
            query=query_dict, from_=0, size=50, sort=_DEFAULT_SORT
        )
        raw_json = await self._client._call_api(
            WORKFLOW_INDEX_RUN_SEARCH, request_obj=request
        )
        response = msgspec.convert(raw_json, AsyncWorkflowSearchResponse, strict=False)
        response._client = self._client
        response._endpoint = WORKFLOW_INDEX_RUN_SEARCH
        response._criteria = query_dict
        response._start = 0
        response._size = 50
        if results := response.hits and response.hits.hits:
            for result in results:
                if result.status in {
                    AtlanWorkflowPhase.PENDING,
                    AtlanWorkflowPhase.RUNNING,
                }:
                    return result
        return None

    async def _find_runs(
        self,
        query,
        from_: int = 0,
        size: int = 100,
    ) -> AsyncWorkflowSearchResponse:
        """
        Retrieve existing workflow runs.

        :param query: query object to filter workflow runs.
        :param from_: starting point for pagination
        :param size: maximum number of results to retrieve
        :returns: the workflow runs
        :raises AtlanError: on any API communication issue
        """
        query_dict = query.to_dict() if hasattr(query, "to_dict") else query
        request = WorkflowSearchRequest(
            query=query_dict, from_=from_, size=size, sort=_DEFAULT_SORT
        )
        raw_json = await self._client._call_api(
            WORKFLOW_INDEX_RUN_SEARCH, request_obj=request
        )
        response = msgspec.convert(raw_json, AsyncWorkflowSearchResponse, strict=False)
        response._client = self._client
        response._endpoint = WORKFLOW_INDEX_RUN_SEARCH
        response._criteria = query_dict
        response._start = from_
        response._size = size
        return response

    def _add_schedule(
        self,
        workflow,
        workflow_schedule: WorkflowSchedule,
    ):
        """
        Adds required schedule parameters to the workflow object.
        """
        if workflow.metadata and workflow.metadata.annotations:
            workflow.metadata.annotations.update(
                {
                    self._WORKFLOW_RUN_SCHEDULE: workflow_schedule.cron_schedule,
                    self._WORKFLOW_RUN_TIMEZONE: workflow_schedule.timezone,
                }
            )

    async def _handle_workflow_types(self, workflow):
        """Handle different workflow types and return the appropriate workflow object."""
        if isinstance(workflow, WorkflowPackage):
            if results := await self.find_by_type(workflow):
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
    async def rerun(
        self, workflow: WorkflowPackage, idempotent: bool = False
    ) -> WorkflowRunResponse: ...

    @overload
    async def rerun(
        self, workflow: WorkflowSearchResultDetail, idempotent: bool = False
    ) -> WorkflowRunResponse: ...

    @overload
    async def rerun(
        self, workflow: WorkflowSearchResult, idempotent: bool = False
    ) -> WorkflowRunResponse: ...

    async def rerun(
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
        detail = await self._handle_workflow_types(workflow)

        if idempotent and detail and detail.metadata and detail.metadata.name:
            await asyncio.sleep(10)
            if (
                (
                    current_run_details := await self._find_current_run(
                        workflow_name=detail.metadata.name
                    )
                )
                and current_run_details.source
                and current_run_details.source.metadata
                and current_run_details.source.spec
                and current_run_details.source.status
            ):
                return WorkflowRunResponse(
                    metadata=current_run_details.source.metadata,
                    spec=current_run_details.source.spec,
                    status=current_run_details.source.status,
                )
        use_package_endpoint = not await self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        request = None
        if detail and detail.metadata:
            request = ReRunRequest(
                namespace=detail.metadata.namespace,
                resource_name=detail.metadata.name,
            )
        endpoint = PACKAGE_WORKFLOW_RERUN if use_package_endpoint else WORKFLOW_RERUN
        raw_json = await self._client._call_api(endpoint, request_obj=request)
        return msgspec.convert(raw_json, WorkflowRunResponse, strict=False)

    @overload
    async def run(
        self, workflow: Workflow, workflow_schedule: Optional[WorkflowSchedule] = None
    ) -> WorkflowResponse: ...

    @overload
    async def run(
        self, workflow: str, workflow_schedule: Optional[WorkflowSchedule] = None
    ) -> WorkflowResponse: ...

    async def run(
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
            workflow = msgspec.convert(json.loads(workflow), Workflow, strict=False)
        if workflow_schedule:
            self._add_schedule(workflow, workflow_schedule)
        use_package_endpoint = not await self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        endpoint = PACKAGE_WORKFLOW_RUN if use_package_endpoint else WORKFLOW_RUN
        raw_json = await self._client._call_api(endpoint, request_obj=workflow)
        return msgspec.convert(raw_json, WorkflowResponse, strict=False)

    @validate_arguments
    async def updater(self, workflow: Workflow) -> WorkflowResponse:
        """
        Update a given workflow's configuration.

        :param workflow: request full details of the workflow's revised configuration.
        :returns: the updated workflow configuration.
        :raises ValidationError: If the provided `workflow` is invalid.
        :raises AtlanError: on any API communication issue
        """
        use_package_endpoint = not await self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        workflow_name = workflow.metadata and workflow.metadata.name
        if use_package_endpoint:
            endpoint = PACKAGE_WORKFLOW_UPDATE.format_path(
                {"workflow_name": workflow_name}
            )
        else:
            endpoint = WORKFLOW_UPDATE.format_path({"workflow_name": workflow_name})
        raw_json = await self._client._call_api(endpoint, request_obj=workflow)
        return msgspec.convert(raw_json, WorkflowResponse, strict=False)

    @validate_arguments
    async def update_owner(self, workflow_name: str, username: str) -> WorkflowResponse:
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
        raw_json = await self._client._call_api(endpoint, request_obj=request_obj)
        return msgspec.convert(raw_json, WorkflowResponse, strict=False)

    @validate_arguments(config=dict(arbitrary_types_allowed=True))
    async def monitor(
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
            await asyncio.sleep(MONITOR_SLEEP_SECONDS)
            if run_details := await self._find_latest_run(workflow_name=name):
                status = run_details.status
                if logger:
                    logger.debug("Workflow status: %s", status)

        if logger:
            logger.info("Workflow completion status: %s", status)
        return status

    async def get_runs(
        self,
        workflow_name: str,
        workflow_phase: AtlanWorkflowPhase,
        from_: int = 0,
        size: int = 100,
    ) -> Optional[AsyncWorkflowSearchResponse]:
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
        return await self._find_runs(query, from_=from_, size=size)

    @validate_arguments
    async def stop(
        self,
        workflow_run_id: str,
    ) -> WorkflowRunResponse:
        """
        Stop the provided, running workflow.

        :param workflow_run_id: identifier of the specific workflow run
        :returns: the stopped workflow run
        :raises AtlanError: on any API communication issue
        """
        endpoint, _ = WorkflowStop.prepare_request(workflow_run_id)
        raw_json = await self._client._call_api(endpoint, request_obj=None)
        return msgspec.convert(raw_json, WorkflowRunResponse, strict=False)

    @validate_arguments
    async def delete(
        self,
        workflow_name: str,
    ) -> None:
        """
        Archive (delete) the provided workflow.

        :param workflow_name: name of the workflow as displayed
        in the UI (e.g: `atlan-snowflake-miner-1714638976`).
        :raises AtlanError: on any API communication issue.
        """
        use_package_endpoint = not await self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        endpoint, _ = WorkflowDelete.prepare_request(
            workflow_name, use_package_endpoint
        )
        await self._client._call_api(endpoint, request_obj=None)

    @overload
    async def add_schedule(
        self, workflow: WorkflowResponse, workflow_schedule: WorkflowSchedule
    ) -> WorkflowResponse: ...

    @overload
    async def add_schedule(
        self, workflow: WorkflowPackage, workflow_schedule: WorkflowSchedule
    ) -> WorkflowResponse: ...

    @overload
    async def add_schedule(
        self, workflow: WorkflowSearchResult, workflow_schedule: WorkflowSchedule
    ) -> WorkflowResponse: ...

    @overload
    async def add_schedule(
        self, workflow: WorkflowSearchResultDetail, workflow_schedule: WorkflowSchedule
    ) -> WorkflowResponse: ...

    async def add_schedule(
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
        workflow_to_update = await self._handle_workflow_types(workflow)

        self._add_schedule(workflow_to_update, workflow_schedule)
        use_package_endpoint = not await self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        workflow_name = workflow_to_update.metadata and workflow_to_update.metadata.name
        if use_package_endpoint:
            endpoint = PACKAGE_WORKFLOW_UPDATE.format_path(
                {"workflow_name": workflow_name}
            )
        else:
            endpoint = WORKFLOW_UPDATE.format_path({"workflow_name": workflow_name})
        raw_json = await self._client._call_api(
            endpoint, request_obj=workflow_to_update
        )
        return msgspec.convert(raw_json, WorkflowResponse, strict=False)

    @overload
    async def remove_schedule(self, workflow: WorkflowResponse) -> WorkflowResponse: ...

    @overload
    async def remove_schedule(self, workflow: WorkflowPackage) -> WorkflowResponse: ...

    @overload
    async def remove_schedule(
        self, workflow: WorkflowSearchResult
    ) -> WorkflowResponse: ...

    @overload
    async def remove_schedule(
        self, workflow: WorkflowSearchResultDetail
    ) -> WorkflowResponse: ...

    async def remove_schedule(
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
        workflow_to_update = await self._handle_workflow_types(workflow)

        if workflow_to_update.metadata and workflow_to_update.metadata.annotations:
            workflow_to_update.metadata.annotations.pop(
                self._WORKFLOW_RUN_SCHEDULE, None
            )
        use_package_endpoint = not await self._client.role_cache.is_api_token_user()  # type: ignore[attr-defined]
        workflow_name = workflow_to_update.metadata and workflow_to_update.metadata.name
        if use_package_endpoint:
            endpoint = PACKAGE_WORKFLOW_UPDATE.format_path(
                {"workflow_name": workflow_name}
            )
        else:
            endpoint = WORKFLOW_UPDATE.format_path({"workflow_name": workflow_name})
        raw_json = await self._client._call_api(
            endpoint, request_obj=workflow_to_update
        )
        return msgspec.convert(raw_json, WorkflowResponse, strict=False)

    async def get_all_scheduled_runs(self) -> List[WorkflowScheduleResponse]:
        """
        Get the details of scheduled run for all workflow.

        :returns: list of all the workflow schedules
        :raises AtlanError: on any API communication issue
        """
        endpoint, _ = WorkflowGetAllScheduledRuns.prepare_request()
        raw_json = await self._client._call_api(endpoint, request_obj=None)
        items = raw_json.get("items") if raw_json else None
        if not items:
            return []
        return msgspec.convert(items, list[WorkflowScheduleResponse], strict=False)

    @validate_arguments
    async def get_scheduled_run(self, workflow_name: str) -> WorkflowScheduleResponse:
        """
        Get the details of scheduled run for a specific workflow.

        :param workflow_name: name of the workflow for which we want the scheduled run details
        :returns: details of the workflow schedule
        :raises AtlanError: on any API communication issue
        """
        endpoint, _ = WorkflowGetScheduledRun.prepare_request(workflow_name)
        raw_json = await self._client._call_api(endpoint, request_obj=None)
        return msgspec.convert(raw_json, WorkflowScheduleResponse, strict=False)

    @validate_arguments
    async def find_schedule_query(
        self, saved_query_id: str, max_results: int = 10
    ) -> List[WorkflowSearchResult]:
        """
        Find scheduled query workflows by their saved query identifier.

        :param saved_query_id: identifier of the saved query.
        :param max_results: maximum number of results to retrieve. Defaults to `10`.
        :raises AtlanError: on any API communication issue.
        :returns: a list of scheduled query workflows.
        """
        query = Bool(
            filter=[
                NestedQuery(
                    path="metadata",
                    query=Prefix(
                        field="metadata.name.keyword",
                        value=f"asq-{saved_query_id}",
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
        request = WorkflowSearchRequest(
            query=query.to_dict(), size=max_results, sort=_DEFAULT_SORT
        )
        raw_json = await self._client._call_api(
            WORKFLOW_INDEX_SEARCH, request_obj=request
        )
        response = msgspec.convert(raw_json, WorkflowSearchResponse, strict=False)
        return response.hits and response.hits.hits or []

    @validate_arguments
    async def re_run_schedule_query(
        self, schedule_query_id: str
    ) -> WorkflowRunResponse:
        """
        Re-run a scheduled query.

        :param schedule_query_id: ID of the scheduled query to re-run
        :returns: the workflow run response
        :raises AtlanError: on any API communication issue
        """
        request = ReRunRequest(namespace="default", resource_name=schedule_query_id)
        raw_json = await self._client._call_api(
            WORKFLOW_OWNER_RERUN, request_obj=request
        )
        return msgspec.convert(raw_json, WorkflowRunResponse, strict=False)

    @validate_arguments
    async def find_schedule_query_between(
        self,
        request: ScheduleQueriesSearchRequest,
        missed: bool = False,
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
        endpoint, query_params = WorkflowFindScheduleQueryBetween.prepare_request(
            request, missed
        )
        raw_json = await self._client._call_api(endpoint, query_params=query_params)
        if not raw_json:
            return None
        if isinstance(raw_json, list):
            return msgspec.convert(raw_json, list[WorkflowRunResponse], strict=False)
        return msgspec.convert(raw_json, WorkflowRunResponse, strict=False)
