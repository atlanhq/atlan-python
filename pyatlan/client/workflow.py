# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from logging import Logger
from time import sleep
from typing import List, Optional, Union, overload

from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
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
        response = self._find_run(query)
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
        response = self._find_run(query, size=50)
        if results := response.hits.hits:
            for result in results:
                if result.status in {
                    AtlanWorkflowPhase.PENDING,
                    AtlanWorkflowPhase.RUNNING,
                }:
                    return result
        return None

    def _find_run(self, query: Query, size: int = 1) -> WorkflowSearchResponse:
        request = WorkflowSearchRequest(query=query, size=size)
        raw_json = self._client._call_api(
            WORKFLOW_INDEX_RUN_SEARCH,
            request_obj=request,
        )
        return WorkflowSearchResponse(**raw_json)

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
        Rerun the workflow immediately. Note: this must be a workflow that was previously run.
        :param workflow: The workflow to rerun.
        :param idempotent: If `True`, the workflow will only be rerun if it is not already currently running
        :returns: the details of the workflow run (if `idempotent`, will return details of the already-running workflow)
        :raises ValidationError: If the provided workflow is invalid
        :raises InvalidRequestException: If no prior runs are available for the provided workflow
        :raises AtlanError: on any API communication issue
        """
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
    def run(self, workflow: Workflow) -> WorkflowResponse:
        """
        Run the Atlan workflow with a specific configuration.

        Note: This method should only be used to create the workflow for the first time.
        Each invocation creates a new connection and new assets within that connection.
        Running the workflow multiple times with the same configuration may lead to duplicate assets.
        Consider using the "rerun()" method instead to re-execute an existing workflow.

        :param workflow: The workflow to run.
        :returns: Details of the workflow run.
        :raises ValidationError: If the provided `workflow` is invalid.
        :raises AtlanError: on any API communication issue.
        """
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
        Monitor the status of the workflow's run,
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
