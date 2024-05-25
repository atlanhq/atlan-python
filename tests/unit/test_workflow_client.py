# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import Mock, patch

import pytest
from pydantic.v1 import ValidationError

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    SCHEDULE_QUERY_WORKFLOWS_MISSED,
    SCHEDULE_QUERY_WORKFLOWS_SEARCH,
    WORKFLOW_INDEX_SEARCH,
)
from pyatlan.client.workflow import WorkflowClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import AtlanWorkflowPhase, WorkflowPackage
from pyatlan.model.workflow import (
    PackageParameter,
    ScheduleQueriesSearchRequest,
    Workflow,
    WorkflowMetadata,
    WorkflowResponse,
    WorkflowRunResponse,
    WorkflowSchedule,
    WorkflowScheduleResponse,
    WorkflowScheduleSpec,
    WorkflowScheduleStatus,
    WorkflowSearchHits,
    WorkflowSearchRequest,
    WorkflowSearchResponse,
    WorkflowSearchResult,
    WorkflowSearchResultDetail,
    WorkflowSearchResultStatus,
    WorkflowSpec,
)
from tests.unit.constants import TEST_WORKFLOW_CLIENT_METHODS


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def mock_workflow_time_sleep():
    with patch("pyatlan.client.workflow.sleep") as mock_time_sleep:
        yield mock_time_sleep


@pytest.fixture()
def client(mock_api_caller) -> WorkflowClient:
    return WorkflowClient(mock_api_caller)


@pytest.fixture()
def search_result_status() -> WorkflowSearchResultStatus:
    return WorkflowSearchResultStatus(phase=AtlanWorkflowPhase.RUNNING)


@pytest.fixture()
def search_result_detail(
    search_result_status: WorkflowSearchResultStatus,
) -> WorkflowSearchResultDetail:
    return WorkflowSearchResultDetail(
        api_version="1",
        kind="kind",
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
        status=search_result_status,
    )


@pytest.fixture()
def search_result(search_result_detail) -> WorkflowSearchResult:
    return WorkflowSearchResult(
        index="index",
        type="type",
        id="id",
        seq_no=1,
        primary_term=2,
        sort=["sort"],
        source=search_result_detail,
    )  # type: ignore[call-arg]


@pytest.fixture()
def search_response(search_result: WorkflowSearchResult) -> WorkflowSearchResponse:
    return WorkflowSearchResponse(
        hits=WorkflowSearchHits(total={"dummy": "dummy"}, hits=[search_result]),
        shards={"dummy": "dummy"},
    )  # type: ignore[call-arg]


@pytest.fixture()
def rerun_response() -> WorkflowRunResponse:
    return WorkflowRunResponse(
        status=WorkflowSearchResultStatus(),
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
    )


@pytest.fixture()
def rerun_response_with_idempotent(
    search_result_status: WorkflowSearchResultStatus,
) -> WorkflowRunResponse:
    return WorkflowRunResponse(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
        status=search_result_status,
    )


@pytest.fixture()
def workflow_response() -> WorkflowResponse:
    return WorkflowResponse(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
        payload=[PackageParameter(parameter="test-param", type="test-type", body={})],
    )


@pytest.fixture()
def workflow_run_response() -> WorkflowRunResponse:
    return WorkflowRunResponse(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
        payload=[PackageParameter(parameter="test-param", type="test-type", body={})],
        status=WorkflowSearchResultStatus(phase=AtlanWorkflowPhase.RUNNING),
    )


@pytest.fixture()
def schedule() -> WorkflowSchedule:
    return WorkflowSchedule(timezone="Europe/Paris", cron_schedule="45 4 * * *")


@pytest.fixture()
def schedule_response() -> WorkflowScheduleResponse:
    return WorkflowScheduleResponse(
        spec=WorkflowScheduleSpec(),
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        workflow_metadata=WorkflowMetadata(name="name", namespace="namespace"),
        status=WorkflowScheduleStatus(
            active="test-active",
            conditions="test-conditions",
            last_scheduled_time="test-last-scheduled-time",
        ),
    )


@pytest.fixture()
def update_response() -> WorkflowResponse:
    return WorkflowResponse(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
    )


@pytest.mark.parametrize("method, params", TEST_WORKFLOW_CLIENT_METHODS.items())
def test_workflow_client_methods_validation_error(method, params):
    client_method = getattr(AtlanClient().workflow, method)
    for param_values, error_msg in params:
        with pytest.raises(ValidationError, match=error_msg):
            client_method(*param_values)


@pytest.mark.parametrize("api_caller", ["abc", None])
def test_init_when_wrong_class_raises_exception(api_caller):
    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-048 Invalid parameter type for client should be ApiCaller",
    ):
        WorkflowClient(api_caller)


def test_find_by_type(client: WorkflowClient, mock_api_caller):
    raw_json = {"shards": {"dummy": None}, "hits": {"total": {"dummy": None}}}
    mock_api_caller._call_api.return_value = raw_json

    assert client.find_by_type(prefix=WorkflowPackage.FIVETRAN) == []
    mock_api_caller._call_api.called_once()
    assert mock_api_caller._call_api.call_args.args[0] == WORKFLOW_INDEX_SEARCH
    assert isinstance(
        mock_api_caller._call_api.call_args.kwargs["request_obj"], WorkflowSearchRequest
    )


def test_re_run_when_given_workflowpackage_with_no_prior_runs_raises_invalid_request_error(
    client: WorkflowClient, mock_api_caller
):
    raw_json = {"shards": {"dummy": None}, "hits": {"total": {"dummy": None}}}
    mock_api_caller._call_api.return_value = raw_json

    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-047 No prior runs of atlan-fivetran were available.",
    ):
        client.rerun(WorkflowPackage.FIVETRAN)


def test_re_run_when_given_workflowpackage(
    client: WorkflowClient,
    mock_api_caller,
    search_response: WorkflowSearchResponse,
    rerun_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.side_effect = [
        search_response.dict(),
        rerun_response.dict(),
    ]

    assert client.rerun(WorkflowPackage.FIVETRAN) == rerun_response
    assert mock_api_caller._call_api.call_count == 2
    mock_api_caller.reset_mock()


def test_re_run_when_given_workflowsearchresultdetail(
    client: WorkflowClient,
    mock_api_caller,
    search_result_detail: WorkflowSearchResultDetail,
    rerun_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = rerun_response.dict()

    assert client.rerun(workflow=search_result_detail) == rerun_response
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_re_run_when_given_workflowsearchresult(
    client: WorkflowClient,
    mock_api_caller,
    search_result: WorkflowSearchResult,
    rerun_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = rerun_response.dict()

    assert client.rerun(workflow=search_result) == rerun_response
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_re_run_when_given_workflowpackage_with_idempotent(
    client: WorkflowClient,
    mock_api_caller,
    mock_workflow_time_sleep,
    search_response: WorkflowSearchResponse,
    rerun_response_with_idempotent: WorkflowRunResponse,
):
    mock_api_caller._call_api.side_effect = [
        search_response.dict(),
        search_response.dict(),
    ]

    assert (
        client.rerun(WorkflowPackage.FIVETRAN, idempotent=True)
        == rerun_response_with_idempotent
    )
    assert mock_api_caller._call_api.call_count == 2
    mock_api_caller.reset_mock()


def test_re_run_when_given_workflowsearchresultdetail_with_idempotent(
    client: WorkflowClient,
    mock_api_caller,
    mock_workflow_time_sleep,
    search_response: WorkflowSearchResponse,
    search_result_detail: WorkflowSearchResultDetail,
    rerun_response_with_idempotent: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = search_response.dict()

    assert (
        client.rerun(workflow=search_result_detail, idempotent=True)
        == rerun_response_with_idempotent
    )
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_re_run_when_given_workflowsearchresult_with_idempotent(
    client: WorkflowClient,
    mock_api_caller,
    mock_workflow_time_sleep,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    rerun_response_with_idempotent: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = search_response.dict()

    assert (
        client.rerun(workflow=search_result, idempotent=True)
        == rerun_response_with_idempotent
    )
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_run_when_given_workflow(
    client: WorkflowClient,
    mock_api_caller,
    workflow_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = workflow_response.dict()
    response = client.run(
        Workflow(
            metadata=WorkflowMetadata(name="name", namespace="namespace"),
            spec=WorkflowSpec(),
            payload=[
                PackageParameter(parameter="test-param", type="test-type", body={})
            ],
        )  # type: ignore[call-arg]
    )
    assert response == workflow_response
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_run_when_given_workflow_with_schedule(
    client: WorkflowClient,
    schedule: WorkflowSchedule,
    mock_api_caller,
    workflow_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = workflow_response.dict()
    response = client.run(
        Workflow(
            metadata=WorkflowMetadata(name="name", namespace="namespace"),
            spec=WorkflowSpec(),
            payload=[
                PackageParameter(parameter="test-param", type="test-type", body={})
            ],
        ),  # type: ignore[call-arg]
        workflow_schedule=schedule,
    )
    assert response == workflow_response
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_update_when_given_workflow(
    client: WorkflowClient,
    mock_api_caller,
    search_result: WorkflowSearchResult,
    update_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = update_response.dict()
    response = client.update(workflow=search_result.to_workflow())
    assert response == update_response
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_workflow_update_owner(
    client: WorkflowClient,
    mock_api_caller,
    workflow_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = workflow_response.dict()
    response = client.update_owner(workflow_name="test-workflow", username="test-owner")

    assert mock_api_caller._call_api.call_count == 1
    assert response == WorkflowResponse(**workflow_response.dict())
    mock_api_caller.reset_mock()


def test_workflow_get_runs(
    client: WorkflowClient,
    mock_api_caller,
    search_response: WorkflowSearchResponse,
):
    mock_api_caller._call_api.return_value = search_response.dict()
    response = client.get_runs(
        workflow_name="test-workflow",
        workflow_phase=AtlanWorkflowPhase.RUNNING,
    )

    assert response == search_response.hits.hits
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_workflow_stop(
    client: WorkflowClient,
    mock_api_caller,
    workflow_run_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = workflow_run_response.dict()
    response = client.stop(workflow_run_id="test-workflow-run-id")

    assert response == WorkflowRunResponse(**workflow_run_response.dict())
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_workflow_delete(client: WorkflowClient, mock_api_caller):
    mock_api_caller._call_api.return_value = None
    assert not client.delete(workflow_name="test-workflow")


def test_workflow_add_schedule(
    client: WorkflowClient,
    schedule: WorkflowSchedule,
    workflow_response: WorkflowResponse,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    mock_api_caller,
):
    # Workflow response
    mock_api_caller._call_api.side_effect = [
        workflow_response.dict(),
    ]
    response = client.add_schedule(
        workflow=workflow_response, workflow_schedule=schedule
    )

    assert mock_api_caller._call_api.call_count == 1
    assert response == WorkflowResponse(**workflow_response.dict())
    mock_api_caller.reset_mock()

    # Workflow package
    mock_api_caller._call_api.side_effect = [
        search_response.dict(),
        workflow_response.dict(),
    ]
    response = client.add_schedule(
        workflow=WorkflowPackage.FIVETRAN, workflow_schedule=schedule
    )

    assert mock_api_caller._call_api.call_count == 2
    assert response == WorkflowResponse(**workflow_response.dict())
    mock_api_caller.reset_mock()

    # Workflow search result
    mock_api_caller._call_api.side_effect = [workflow_response.dict()]
    response = client.add_schedule(workflow=search_result, workflow_schedule=schedule)

    assert mock_api_caller._call_api.call_count == 1
    assert response == WorkflowResponse(**workflow_response.dict())
    mock_api_caller.reset_mock()


def test_workflow_find_schedule_query_between(
    client: WorkflowClient, mock_api_caller, workflow_run_response: WorkflowRunResponse
):
    mock_api_caller._call_api.return_value = [workflow_run_response]
    response = client.find_schedule_query_between(
        ScheduleQueriesSearchRequest(
            start_date="2024-05-03T16:30:00.000+05:30",
            end_date="2024-05-05T00:59:00.000+05:30",
        )
    )

    assert mock_api_caller._call_api.call_count == 1
    assert (
        response
        and len(response) == 1
        and response[0] == WorkflowRunResponse(**workflow_run_response.dict())
    )
    # Ensure it is called by the correct API endpoint
    assert (
        mock_api_caller._call_api.call_args[0][0].path
        == SCHEDULE_QUERY_WORKFLOWS_SEARCH.path
    )
    mock_api_caller.reset_mock()

    # Missed schedule query workflows
    mock_api_caller._call_api.return_value = [workflow_run_response]
    response = client.find_schedule_query_between(
        ScheduleQueriesSearchRequest(
            start_date="2024-05-03T16:30:00.000+05:30",
            end_date="2024-05-05T00:59:00.000+05:30",
        ),
        missed=True,
    )

    assert mock_api_caller._call_api.call_count == 1
    # Ensure it is called by the correct API endpoint
    assert (
        mock_api_caller._call_api.call_args[0][0].path
        == SCHEDULE_QUERY_WORKFLOWS_MISSED.path
    )
    assert (
        response
        and len(response) == 1
        and response[0] == WorkflowRunResponse(**workflow_run_response.dict())
    )
    mock_api_caller.reset_mock()

    # None response
    mock_api_caller._call_api.return_value = None
    response = client.find_schedule_query_between(
        ScheduleQueriesSearchRequest(
            start_date="2024-05-03T16:30:00.000+05:30",
            end_date="2024-05-05T00:59:00.000+05:30",
        )
    )

    assert mock_api_caller._call_api.call_count == 1
    assert response is None
    mock_api_caller.reset_mock()


def test_workflow_find_schedule_query(
    client: WorkflowClient,
    mock_api_caller,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
):
    mock_api_caller._call_api.return_value = search_response.dict()
    response = client.find_schedule_query(
        saved_query_id="test-query-id", max_results=50
    )

    assert len(response) == 1
    assert mock_api_caller._call_api.call_count == 1
    assert response[0] == WorkflowSearchResult(**search_result.dict())
    mock_api_caller.reset_mock()


def test_workflow_rerun_schedule_query_workflow(
    client,
    mock_api_caller,
    workflow_run_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = workflow_run_response.dict()
    response = client.re_run_schedule_query(schedule_query_id="test-query-id")

    assert mock_api_caller._call_api.call_count == 1
    assert response == WorkflowRunResponse(**workflow_run_response.dict())


def test_workflow_remove_schedule(
    client: WorkflowClient,
    workflow_response: WorkflowResponse,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    mock_api_caller,
):
    # Workflow response
    mock_api_caller._call_api.side_effect = [
        workflow_response.dict(),
    ]
    response = client.remove_schedule(workflow=workflow_response)

    assert mock_api_caller._call_api.call_count == 1
    assert response == WorkflowResponse(**workflow_response.dict())
    mock_api_caller.reset_mock()

    # Workflow package
    mock_api_caller._call_api.side_effect = [
        search_response.dict(),
        workflow_response.dict(),
    ]
    response = client.remove_schedule(workflow=WorkflowPackage.FIVETRAN)

    assert mock_api_caller._call_api.call_count == 2
    assert response == WorkflowResponse(**workflow_response.dict())
    mock_api_caller.reset_mock()

    # Workflow search result
    mock_api_caller._call_api.side_effect = [workflow_response.dict()]
    response = client.remove_schedule(workflow=search_result)

    assert mock_api_caller._call_api.call_count == 1
    assert response == WorkflowResponse(**workflow_response.dict())
    mock_api_caller.reset_mock()


def test_workflow_get_all_scheduled_runs(
    client: WorkflowClient,
    workflow_response: WorkflowResponse,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    schedule_response: WorkflowScheduleResponse,
    mock_api_caller,
):
    mock_api_caller._call_api.return_value = {"items": [schedule_response]}
    response = client.get_all_scheduled_runs()

    assert mock_api_caller._call_api.call_count == 1
    assert response and len(response) == 1
    assert response[0] == WorkflowScheduleResponse(**schedule_response.dict())
    mock_api_caller.reset_mock()


def test_workflow_get_scheduled_run(
    client: WorkflowClient,
    workflow_response: WorkflowResponse,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    schedule_response: WorkflowScheduleResponse,
    mock_api_caller,
):
    mock_api_caller._call_api.return_value = schedule_response
    response = client.get_scheduled_run(workflow_name="test-workflow")

    assert mock_api_caller._call_api.call_count == 1
    assert response == WorkflowScheduleResponse(**schedule_response.dict())
    mock_api_caller.reset_mock()
