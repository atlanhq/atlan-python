# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from logging import Logger
from time import sleep
from typing import Optional, Union, overload

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    WORKFLOW_INDEX_RUN_SEARCH,
    WORKFLOW_INDEX_SEARCH,
    WORKFLOW_RUN,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.enums import AtlanWorkflowPhase, WorkflowPackage
from pyatlan.model.search import Bool, NestedQuery, Prefix, Query, Term
from pyatlan.model.workflow import (
    ReRunRequest,
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

    def find_by_type(
        self, prefix: WorkflowPackage, max_results: int = 10
    ) -> list[WorkflowSearchResult]:
        """
        Find workflows based on their type (prefix). Note: Only workflows that have been run will be found.

        :param prefix: name of the specific workflow to find (for example CONNECTION_DELETE)
        :param max_results: the maximum number of results to retrieve
        :returns: the list of workflows of the provided type, with the most-recently created first
        """
        if not isinstance(prefix, WorkflowPackage):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "prefix", "WorkflowPackage"
            )
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
    def rerun(self, workflow: WorkflowPackage) -> WorkflowRunResponse:
        ...

    @overload
    def rerun(self, workflow: WorkflowSearchResultDetail) -> WorkflowRunResponse:
        ...

    @overload
    def rerun(self, workflow: WorkflowSearchResult) -> WorkflowRunResponse:
        ...

    def rerun(
        self,
        workflow: Union[
            WorkflowPackage, WorkflowSearchResultDetail, WorkflowSearchResult
        ],
    ) -> WorkflowRunResponse:
        """
        Rerun the workflow immediately. Note: this must be a workflow that was previously run.
        :param workflow: The workflow to rerun.
        :returns: the details of the workflow run

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
        elif isinstance(workflow, WorkflowSearchResultDetail):
            detail = workflow
        else:
            expected = (
                "WorkflowPackage, WorkflowSearchResult or WorkflowSearchResultDetail"
            )
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "workflow", expected
            )

        request = ReRunRequest(
            namespace=detail.metadata.namespace, resource_name=detail.metadata.name
        )
        raw_json = self._client._call_api(
            WORKFLOW_RUN,
            request_obj=request,
        )
        return WorkflowRunResponse(**raw_json)

    def monitor(
        self, workflow_response: WorkflowResponse, logger: Optional[Logger] = None
    ) -> Optional[AtlanWorkflowPhase]:
        """
        Monitor the status of the workflow's run,
        :param workflow_response: The workflow_response returned from running the workflow
        :param logger: the logger to log status information (logging.INFO for summary info. logging:DEBUG for detail
        info)
        :returns: the status at completion or None if the workflow wasn't run
        """
        if not isinstance(workflow_response, WorkflowResponse):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "workflow_response", "WorkflowResponse"
            )
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
