# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""
Unit tests for workflow client — ported from tests/unit/test_workflow_client.py.

Uses v9 msgspec.Struct workflow models for fixture construction.
The WorkflowClient itself still deserializes responses into legacy Pydantic
models, so ``_is_model_instance`` is used for cross-type assertions and
``msgspec.to_builtins()`` replaces ``.dict()`` for mock return values.
"""

from unittest.mock import Mock, patch

import msgspec
import pytest

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    SCHEDULE_QUERY_WORKFLOWS_MISSED,
    SCHEDULE_QUERY_WORKFLOWS_SEARCH,
    WORKFLOW_INDEX_RUN_SEARCH,
    WORKFLOW_INDEX_SEARCH,
)
from pyatlan.client.workflow import WorkflowClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import AtlanWorkflowPhase, WorkflowPackage
from pyatlan.validate import _is_model_instance
from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.search import Range

# v9 models
from pyatlan_v9.model.workflow import (
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
from tests_v9.unit.constants import TEST_WORKFLOW_CLIENT_METHODS


def _to_dict(model):
    """Convert a msgspec.Struct model to a plain dict (for mock return values)."""
    return msgspec.to_builtins(model)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def mock_api_caller():
    mock = Mock(spec=ApiCaller)
    # Add role_cache attribute to the mock
    mock.role_cache = Mock()
    mock.role_cache.is_api_token_user.return_value = (
        False  # Default to non-API token user
    )
    return mock


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
    )


@pytest.fixture()
def search_response(search_result: WorkflowSearchResult) -> WorkflowSearchResponse:
    return WorkflowSearchResponse(
        hits=WorkflowSearchHits(total={"dummy": "dummy"}, hits=[search_result]),
        shards={"dummy": "dummy"},
    )


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


# ---------------------------------------------------------------------------
# Validation-error tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("method, params", TEST_WORKFLOW_CLIENT_METHODS.items())
def test_workflow_client_methods_validation_error(method, params):
    client_method = getattr(AtlanClient().workflow, method)
    for param_values, error_msg in params:
        with pytest.raises(ValueError, match=error_msg):
            client_method(*param_values)


@pytest.mark.parametrize("workflow", ["abc", None])
def test_workflow_rerun_invalid_request_error(client, workflow):
    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-048 Invalid parameter type for workflow should "
            "be WorkflowPackage, WorkflowSearchResultDetail or WorkflowSearchResult. "
            "Suggestion: Check that you have used the correct type of parameter."
        ),
    ):
        client.rerun(workflow)


@pytest.mark.parametrize("workflow, workflow_schedule", [[None, 123], [123, "123"]])
def test_workflow_run_invalid_request_error(client, workflow, workflow_schedule):
    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-048 Invalid parameter type for workflow should be Workflow or str. "
            "Suggestion: Check that you have used the correct type of parameter."
        ),
    ):
        client.run(workflow)

    valid_workflow = Workflow(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
        payload=[PackageParameter(parameter="test-param", type="test-type", body={})],
    )

    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-048 Invalid parameter type for workflow_schedule should be WorkflowSchedule or None. "
            "Suggestion: Check that you have used the correct type of parameter."
        ),
    ):
        client.run(valid_workflow, workflow_schedule)


@pytest.mark.parametrize(
    "workflow, schedule",
    [
        ("abc", WorkflowSchedule(timezone="atlan", cron_schedule="*")),
        (None, WorkflowSchedule(timezone="atlan", cron_schedule="*")),
    ],
)
def test_workflow_add_schedule_invalid_request_error(client, workflow, schedule):
    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-048 Invalid parameter type for workflow should "
            "be WorkflowResponse, WorkflowPackage, WorkflowSearchResult or WorkflowSearchResultDetail. "
            "Suggestion: Check that you have used the correct type of parameter."
        ),
    ):
        client.add_schedule(workflow, schedule)


@pytest.mark.parametrize(
    "workflow",
    [
        "abc",
        None,
    ],
)
def test_workflow_remove_schedule_invalid_request_error(client, workflow):
    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-048 Invalid parameter type for workflow should "
            "be WorkflowResponse, WorkflowPackage, WorkflowSearchResult or WorkflowSearchResultDetail. "
            "Suggestion: Check that you have used the correct type of parameter."
        ),
    ):
        client.add_schedule(workflow, schedule)


@pytest.mark.parametrize("api_caller", ["abc", None])
def test_init_when_wrong_class_raises_exception(api_caller):
    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-048 Invalid parameter type for client should be ApiCaller",
    ):
        WorkflowClient(api_caller)


# ---------------------------------------------------------------------------
# Client method tests
# ---------------------------------------------------------------------------


def test_find_by_type(client: WorkflowClient, mock_api_caller):
    raw_json = {"shards": {"dummy": None}, "hits": {"total": {"dummy": None}}}
    mock_api_caller._call_api.return_value = raw_json

    assert client.find_by_type(prefix=WorkflowPackage.FIVETRAN) == []
    mock_api_caller._call_api.assert_called_once()
    assert mock_api_caller._call_api.call_args.args[0] == WORKFLOW_INDEX_SEARCH
    assert _is_model_instance(
        mock_api_caller._call_api.call_args.kwargs["request_obj"], WorkflowSearchRequest
    )


def test_find_runs_by_status_and_time_range(client: WorkflowClient, mock_api_caller):
    raw_json = {"_shards": {"dummy": None}, "hits": {"total": {"dummy": None}}}
    mock_api_caller._call_api.return_value = raw_json

    status = [AtlanWorkflowPhase.SUCCESS, AtlanWorkflowPhase.FAILED]
    started_at = "now-2h"
    finished_at = "now-1h"
    response = client.find_runs_by_status_and_time_range(
        status=status,
        started_at=started_at,
        finished_at=finished_at,
        from_=10,
        size=5,
    )
    assert _is_model_instance(response, WorkflowSearchResponse)
    mock_api_caller._call_api.assert_called_once()
    request_obj = mock_api_caller._call_api.call_args.kwargs["request_obj"]
    assert _is_model_instance(request_obj, WorkflowSearchRequest)
    assert request_obj.query
    range_filters = [
        clause
        for clause in request_obj.query.must  # type: ignore
        if isinstance(clause, Range)
    ]
    assert any(
        rf.field == "status.startedAt" and rf.gte == started_at for rf in range_filters
    )
    finished_filters = [rf for rf in range_filters if rf.field == "status.finishedAt"]
    assert len(finished_filters) == 1
    finished_filter = finished_filters[0]
    assert finished_filter.lte == finished_at
    assert finished_filter.gte is None


def test_find_by_id(
    client: WorkflowClient, search_response: WorkflowSearchResponse, mock_api_caller
):
    raw_json = _to_dict(search_response)
    mock_api_caller._call_api.return_value = raw_json

    assert search_response.hits and search_response.hits.hits
    result = client.find_by_id(id="atlan-snowflake-miner-1714638976")
    assert _is_model_instance(result, WorkflowSearchResult)
    assert result.id == "id"
    mock_api_caller._call_api.assert_called_once()
    assert mock_api_caller._call_api.call_args.args[0] == WORKFLOW_INDEX_SEARCH
    assert _is_model_instance(
        mock_api_caller._call_api.call_args.kwargs["request_obj"], WorkflowSearchRequest
    )


def test_find_run_by_id(
    client: WorkflowClient, search_response: WorkflowSearchResponse, mock_api_caller
):
    raw_json = _to_dict(search_response)
    mock_api_caller._call_api.return_value = raw_json

    assert search_response and search_response.hits and search_response.hits.hits
    result = client.find_run_by_id(id="atlan-snowflake-miner-1714638976-mzdza")
    assert _is_model_instance(result, WorkflowSearchResult)
    assert result.id == "id"
    mock_api_caller._call_api.assert_called_once()
    assert mock_api_caller._call_api.call_args.args[0] == WORKFLOW_INDEX_RUN_SEARCH
    assert _is_model_instance(
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
        _to_dict(search_response),
        _to_dict(rerun_response),
    ]

    response = client.rerun(WorkflowPackage.FIVETRAN)
    assert _is_model_instance(response, WorkflowRunResponse)
    assert response.metadata.name == "name"
    assert mock_api_caller._call_api.call_count == 2
    mock_api_caller.reset_mock()


def test_re_run_when_given_workflowsearchresultdetail(
    client: WorkflowClient,
    mock_api_caller,
    search_result_detail: WorkflowSearchResultDetail,
    rerun_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(rerun_response)

    response = client.rerun(workflow=search_result_detail)
    assert _is_model_instance(response, WorkflowRunResponse)
    assert response.metadata.name == "name"
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_re_run_when_given_workflowsearchresult(
    client: WorkflowClient,
    mock_api_caller,
    search_result: WorkflowSearchResult,
    rerun_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(rerun_response)

    response = client.rerun(workflow=search_result)
    assert _is_model_instance(response, WorkflowRunResponse)
    assert response.metadata.name == "name"
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
        _to_dict(search_response),
        _to_dict(search_response),
    ]

    response = client.rerun(WorkflowPackage.FIVETRAN, idempotent=True)
    assert _is_model_instance(response, WorkflowRunResponse)
    assert response.metadata.name == "name"
    assert response.status.phase == AtlanWorkflowPhase.RUNNING
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
    mock_api_caller._call_api.return_value = _to_dict(search_response)

    response = client.rerun(workflow=search_result_detail, idempotent=True)
    assert _is_model_instance(response, WorkflowRunResponse)
    assert response.metadata.name == "name"
    assert response.status.phase == AtlanWorkflowPhase.RUNNING
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
    mock_api_caller._call_api.return_value = _to_dict(search_response)

    response = client.rerun(workflow=search_result, idempotent=True)
    assert _is_model_instance(response, WorkflowRunResponse)
    assert response.metadata.name == "name"
    assert response.status.phase == AtlanWorkflowPhase.RUNNING
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_run_when_given_workflow(
    client: WorkflowClient,
    mock_api_caller,
    workflow_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)
    response = client.run(
        Workflow(
            metadata=WorkflowMetadata(name="name", namespace="namespace"),
            spec=WorkflowSpec(),
            payload=[
                PackageParameter(parameter="test-param", type="test-type", body={})
            ],
        )
    )
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_run_when_given_workflow_json(
    client: WorkflowClient,
    mock_api_caller,
    workflow_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)
    workflow_json = r"""
    {
        "metadata": {"name": "name", "namespace": "namespace"},
        "spec": {},
        "payload": [{"parameter": "test-param", "type": "test-type", "body": {}}]
    }
    """
    response = client.run(workflow_json)
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_run_when_given_workflow_with_schedule(
    client: WorkflowClient,
    schedule: WorkflowSchedule,
    mock_api_caller,
    workflow_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)
    response = client.run(
        Workflow(
            metadata=WorkflowMetadata(
                name="name",
                namespace="namespace",
                annotations={"existing": "value"},
            ),
            spec=WorkflowSpec(),
            payload=[
                PackageParameter(parameter="test-param", type="test-type", body={})
            ],
        ),
        workflow_schedule=schedule,
    )
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_run_when_given_workflow_json_with_schedule(
    client: WorkflowClient,
    schedule: WorkflowSchedule,
    mock_api_caller,
    workflow_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)
    workflow_json = r"""
    {
        "metadata": {"name": "name", "namespace": "namespace"},
        "spec": {},
        "payload": [{"parameter": "test-param", "type": "test-type", "body": {}}]
    }
    """
    response = client.run(workflow_json, workflow_schedule=schedule)
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_update_when_given_workflow(
    client: WorkflowClient,
    mock_api_caller,
    search_result: WorkflowSearchResult,
    update_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(update_response)
    assert search_result.to_workflow()
    response = client.update(workflow=search_result.to_workflow())
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_workflow_update_owner(
    client: WorkflowClient,
    mock_api_caller,
    workflow_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)
    response = client.update_owner(workflow_name="test-workflow", username="test-owner")

    assert mock_api_caller._call_api.call_count == 1
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    mock_api_caller.reset_mock()


def test_workflow_get_runs(
    client: WorkflowClient,
    mock_api_caller,
    search_response: WorkflowSearchResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(search_response)
    response = client.get_runs(
        workflow_name="test-workflow",
        workflow_phase=AtlanWorkflowPhase.RUNNING,
    )

    assert _is_model_instance(response, WorkflowSearchResponse)
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()


def test_workflow_stop(
    client: WorkflowClient,
    mock_api_caller,
    workflow_run_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(workflow_run_response)
    response = client.stop(workflow_run_id="test-workflow-run-id")

    assert _is_model_instance(response, WorkflowRunResponse)
    assert response.metadata.name == "name"
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
        _to_dict(workflow_response),
    ]
    response = client.add_schedule(
        workflow=workflow_response, workflow_schedule=schedule
    )

    assert mock_api_caller._call_api.call_count == 1
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    mock_api_caller.reset_mock()

    # Workflow package
    mock_api_caller._call_api.side_effect = [
        _to_dict(search_response),
        _to_dict(workflow_response),
    ]
    response = client.add_schedule(
        workflow=WorkflowPackage.FIVETRAN, workflow_schedule=schedule
    )

    assert mock_api_caller._call_api.call_count == 2
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    mock_api_caller.reset_mock()

    # Workflow search result
    mock_api_caller._call_api.side_effect = [_to_dict(workflow_response)]
    response = client.add_schedule(workflow=search_result, workflow_schedule=schedule)

    assert mock_api_caller._call_api.call_count == 1
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    mock_api_caller.reset_mock()


def test_workflow_find_schedule_query_between(
    client: WorkflowClient, mock_api_caller, workflow_run_response: WorkflowRunResponse
):
    mock_api_caller._call_api.return_value = [_to_dict(workflow_run_response)]
    response = client.find_schedule_query_between(
        ScheduleQueriesSearchRequest(
            start_date="2024-05-03T16:30:00.000+05:30",
            end_date="2024-05-05T00:59:00.000+05:30",
        )
    )

    assert mock_api_caller._call_api.call_count == 1
    assert response and len(response) == 1
    assert _is_model_instance(response[0], WorkflowRunResponse)
    # Ensure it is called by the correct API endpoint
    assert (
        mock_api_caller._call_api.call_args[0][0].path
        == SCHEDULE_QUERY_WORKFLOWS_SEARCH.path
    )
    mock_api_caller.reset_mock()

    # Missed schedule query workflows
    mock_api_caller._call_api.return_value = [_to_dict(workflow_run_response)]
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
    assert response and len(response) == 1
    assert _is_model_instance(response[0], WorkflowRunResponse)
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
    mock_api_caller._call_api.return_value = _to_dict(search_response)
    response = client.find_schedule_query(
        saved_query_id="test-query-id", max_results=50
    )

    assert len(response) == 1
    assert mock_api_caller._call_api.call_count == 1
    assert _is_model_instance(response[0], WorkflowSearchResult)
    assert response[0].id == search_result.id
    mock_api_caller.reset_mock()


def test_workflow_rerun_schedule_query_workflow(
    client,
    mock_api_caller,
    workflow_run_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = _to_dict(workflow_run_response)
    response = client.re_run_schedule_query(schedule_query_id="test-query-id")

    assert mock_api_caller._call_api.call_count == 1
    assert _is_model_instance(response, WorkflowRunResponse)
    assert response.metadata.name == "name"


def test_workflow_remove_schedule(
    client: WorkflowClient,
    workflow_response: WorkflowResponse,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    mock_api_caller,
):
    # Workflow response
    mock_api_caller._call_api.side_effect = [
        _to_dict(workflow_response),
    ]
    response = client.remove_schedule(workflow=workflow_response)

    assert mock_api_caller._call_api.call_count == 1
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    mock_api_caller.reset_mock()

    # Workflow package
    mock_api_caller._call_api.side_effect = [
        _to_dict(search_response),
        _to_dict(workflow_response),
    ]
    response = client.remove_schedule(workflow=WorkflowPackage.FIVETRAN)

    assert mock_api_caller._call_api.call_count == 2
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    mock_api_caller.reset_mock()

    # Workflow search result
    mock_api_caller._call_api.side_effect = [_to_dict(workflow_response)]
    response = client.remove_schedule(workflow=search_result)

    assert mock_api_caller._call_api.call_count == 1
    assert _is_model_instance(response, WorkflowResponse)
    assert response.metadata.name == "name"
    mock_api_caller.reset_mock()


def test_workflow_get_all_scheduled_runs(
    client: WorkflowClient,
    workflow_response: WorkflowResponse,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    schedule_response: WorkflowScheduleResponse,
    mock_api_caller,
):
    mock_api_caller._call_api.return_value = {"items": [_to_dict(schedule_response)]}
    response = client.get_all_scheduled_runs()

    assert mock_api_caller._call_api.call_count == 1
    assert response and len(response) == 1
    assert _is_model_instance(response[0], WorkflowScheduleResponse)
    mock_api_caller.reset_mock()


def test_workflow_get_scheduled_run(
    client: WorkflowClient,
    workflow_response: WorkflowResponse,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    schedule_response: WorkflowScheduleResponse,
    mock_api_caller,
):
    mock_api_caller._call_api.return_value = _to_dict(schedule_response)
    response = client.get_scheduled_run(workflow_name="test-workflow")

    assert mock_api_caller._call_api.call_count == 1
    assert _is_model_instance(response, WorkflowScheduleResponse)
    mock_api_caller.reset_mock()


# ---------------------------------------------------------------------------
# role_cache integration tests
# ---------------------------------------------------------------------------


def test_rerun_with_role_cache_api_token_user(
    client: WorkflowClient,
    mock_api_caller,
    mock_role_cache,
    search_result: WorkflowSearchResult,
    rerun_response: WorkflowRunResponse,
):
    """Test that rerun uses package endpoint when user is API token user."""
    mock_role_cache.is_api_token_user.return_value = True
    mock_api_caller.role_cache = mock_role_cache
    mock_api_caller._call_api.return_value = _to_dict(rerun_response)

    response = client.rerun(search_result)

    mock_role_cache.is_api_token_user.assert_called_once()
    mock_api_caller._call_api.assert_called_once()
    assert _is_model_instance(response, WorkflowRunResponse)
    mock_api_caller.reset_mock()


def test_rerun_with_role_cache_non_api_token_user(
    client: WorkflowClient,
    mock_api_caller,
    mock_role_cache,
    search_result: WorkflowSearchResult,
    rerun_response: WorkflowRunResponse,
):
    """Test that rerun uses non-package endpoint when user is not API token user."""
    mock_role_cache.is_api_token_user.return_value = False
    mock_api_caller.role_cache = mock_role_cache
    mock_api_caller._call_api.return_value = _to_dict(rerun_response)

    response = client.rerun(search_result)

    mock_role_cache.is_api_token_user.assert_called_once()
    mock_api_caller._call_api.assert_called_once()
    assert _is_model_instance(response, WorkflowRunResponse)
    mock_api_caller.reset_mock()


def test_run_with_role_cache_api_token_user(
    client: WorkflowClient,
    mock_api_caller,
    mock_role_cache,
    workflow_response: WorkflowResponse,
):
    """Test that run uses package endpoint when user is API token user."""
    mock_role_cache.is_api_token_user.return_value = True
    mock_api_caller.role_cache = mock_role_cache
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)

    workflow = Workflow(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
        payload=[PackageParameter(parameter="test-param", type="test-type", body={})],
    )

    response = client.run(workflow)

    mock_role_cache.is_api_token_user.assert_called_once()
    mock_api_caller._call_api.assert_called_once()
    assert _is_model_instance(response, WorkflowResponse)
    mock_api_caller.reset_mock()


def test_update_with_role_cache_api_token_user(
    client: WorkflowClient,
    mock_api_caller,
    mock_role_cache,
    workflow_response: WorkflowResponse,
):
    """Test that update uses package endpoint when user is API token user."""
    mock_role_cache.is_api_token_user.return_value = True
    mock_api_caller.role_cache = mock_role_cache
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)

    workflow = Workflow(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
        payload=[PackageParameter(parameter="test-param", type="test-type", body={})],
    )

    response = client.update(workflow)

    mock_role_cache.is_api_token_user.assert_called_once()
    mock_api_caller._call_api.assert_called_once()
    assert _is_model_instance(response, WorkflowResponse)
    mock_api_caller.reset_mock()


def test_delete_with_role_cache_api_token_user(
    client: WorkflowClient,
    mock_api_caller,
    mock_role_cache,
):
    """Test that delete uses package endpoint when user is API token user."""
    mock_role_cache.is_api_token_user.return_value = True
    mock_api_caller.role_cache = mock_role_cache
    mock_api_caller._call_api.return_value = None

    client.delete("test-workflow-name")

    mock_role_cache.is_api_token_user.assert_called_once()
    mock_api_caller._call_api.assert_called_once()
    mock_api_caller.reset_mock()


def test_add_schedule_with_role_cache_api_token_user(
    client: WorkflowClient,
    mock_api_caller,
    mock_role_cache,
    search_result: WorkflowSearchResult,
    schedule: WorkflowSchedule,
    workflow_response: WorkflowResponse,
):
    """Test that add_schedule uses package endpoint when user is API token user."""
    mock_role_cache.is_api_token_user.return_value = True
    mock_api_caller.role_cache = mock_role_cache
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)

    response = client.add_schedule(search_result, schedule)

    mock_role_cache.is_api_token_user.assert_called_once()
    mock_api_caller._call_api.assert_called_once()
    assert _is_model_instance(response, WorkflowResponse)
    mock_api_caller.reset_mock()


def test_remove_schedule_with_role_cache_api_token_user(
    client: WorkflowClient,
    mock_api_caller,
    mock_role_cache,
    search_result: WorkflowSearchResult,
    workflow_response: WorkflowResponse,
):
    """Test that remove_schedule uses package endpoint when user is API token user."""
    mock_role_cache.is_api_token_user.return_value = True
    mock_api_caller.role_cache = mock_role_cache
    mock_api_caller._call_api.return_value = _to_dict(workflow_response)

    response = client.remove_schedule(search_result)

    mock_role_cache.is_api_token_user.assert_called_once()
    mock_api_caller._call_api.assert_called_once()
    assert _is_model_instance(response, WorkflowResponse)
    mock_api_caller.reset_mock()
