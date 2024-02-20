# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import Mock, patch

import pytest
from pydantic.v1 import ValidationError

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import WORKFLOW_INDEX_SEARCH
from pyatlan.client.workflow import WorkflowClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import AtlanWorkflowPhase, WorkflowPackage
from pyatlan.model.workflow import (
    PackageParameter,
    Workflow,
    WorkflowMetadata,
    WorkflowResponse,
    WorkflowRunResponse,
    WorkflowSearchHits,
    WorkflowSearchRequest,
    WorkflowSearchResponse,
    WorkflowSearchResult,
    WorkflowSearchResultDetail,
    WorkflowSearchResultStatus,
    WorkflowSpec,
)


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
def run_response() -> WorkflowResponse:
    return WorkflowResponse(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
        payload=[PackageParameter(parameter="test-param", type="test-type", body={})],
    )


@pytest.fixture()
def update_response() -> WorkflowResponse:
    return WorkflowResponse(
        metadata=WorkflowMetadata(name="name", namespace="namespace"),
        spec=WorkflowSpec(),
    )


@pytest.mark.parametrize("api_caller", ["abc", None])
def test_init_when_wrong_class_raises_exception(api_caller):
    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-048 Invalid parameter type for client should be ApiCaller",
    ):
        WorkflowClient(api_caller)


@pytest.mark.parametrize(
    "prefix, error_msg",
    [
        ["abc", "value is not a valid enumeration member"],
        [None, "none is not an allowed value"],
    ],
)
def test_find_by_type_when_given_wrong_parameters_raises_validation_error(
    prefix, error_msg, client: WorkflowClient
):
    with pytest.raises(ValidationError) as err:
        client.find_by_type(prefix=prefix)
    assert error_msg in str(err.value)


def test_find_by_type(client: WorkflowClient, mock_api_caller):
    raw_json = {"shards": {"dummy": None}, "hits": {"total": {"dummy": None}}}
    mock_api_caller._call_api.return_value = raw_json

    assert client.find_by_type(prefix=WorkflowPackage.FIVETRAN) == []
    mock_api_caller._call_api.called_once()
    assert mock_api_caller._call_api.call_args.args[0] == WORKFLOW_INDEX_SEARCH
    assert isinstance(
        mock_api_caller._call_api.call_args.kwargs["request_obj"], WorkflowSearchRequest
    )


@pytest.mark.parametrize(
    "workflow, error_msg",
    [
        ["abc", "value is not a valid enumeration member"],
        [None, "none is not an allowed value"],
    ],
)
def test_re_run_when_given_wrong_parameter_raises_validation_error(
    workflow, error_msg, client: WorkflowClient
):
    with pytest.raises(ValidationError) as err:
        client.rerun(workflow=workflow)
    assert error_msg in str(err.value)


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


def test_re_run_when_given_workflowsearchresultdetail(
    client: WorkflowClient,
    mock_api_caller,
    search_result_detail: WorkflowSearchResultDetail,
    rerun_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = rerun_response.dict()

    assert client.rerun(workflow=search_result_detail) == rerun_response


def test_re_run_when_given_workflowsearchresult(
    client: WorkflowClient,
    mock_api_caller,
    search_result: WorkflowSearchResult,
    rerun_response: WorkflowRunResponse,
):
    mock_api_caller._call_api.return_value = rerun_response.dict()

    assert client.rerun(workflow=search_result) == rerun_response


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
        rerun_response_with_idempotent.dict(),
    ]

    assert (
        client.rerun(WorkflowPackage.FIVETRAN, idempotent=True)
        == rerun_response_with_idempotent
    )


def test_re_run_when_given_workflowsearchresultdetail_with_idempotent(
    client: WorkflowClient,
    mock_api_caller,
    mock_workflow_time_sleep,
    search_response: WorkflowSearchResponse,
    search_result_detail: WorkflowSearchResultDetail,
    rerun_response_with_idempotent: WorkflowRunResponse,
):
    mock_api_caller._call_api.side_effect = [
        search_response.dict(),
        rerun_response_with_idempotent.dict(),
    ]

    assert (
        client.rerun(workflow=search_result_detail, idempotent=True)
        == rerun_response_with_idempotent
    )


def test_re_run_when_given_workflowsearchresult_with_idempotent(
    client: WorkflowClient,
    mock_api_caller,
    mock_workflow_time_sleep,
    search_response: WorkflowSearchResponse,
    search_result: WorkflowSearchResult,
    rerun_response_with_idempotent: WorkflowRunResponse,
):
    mock_api_caller._call_api.side_effect = [
        search_response.dict(),
        rerun_response_with_idempotent.dict(),
    ]

    assert (
        client.rerun(workflow=search_result, idempotent=True)
        == rerun_response_with_idempotent
    )


@pytest.mark.parametrize(
    "workflow_response, logger, error_msg",
    [
        ["abc", "test-logger", "value is not a valid dict"],
        [
            WorkflowResponse(metadata=WorkflowMetadata(), spec=WorkflowSpec()),
            "test-logger",
            "instance of Logger expected",
        ],
        [None, "test-logger", "none is not an allowed value"],
    ],
)
def test_monitor_when_given_wrong_parameter_raises_validation_error(
    workflow_response, logger, error_msg, client: WorkflowClient
):
    with pytest.raises(ValidationError) as err:
        client.monitor(workflow_response, logger=logger)
    assert error_msg in str(err.value)


def test_run_when_given_workflow(
    client: WorkflowClient,
    mock_api_caller,
    run_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = run_response.dict()
    response = client.run(
        Workflow(
            metadata=WorkflowMetadata(name="name", namespace="namespace"),
            spec=WorkflowSpec(),
            payload=[
                PackageParameter(parameter="test-param", type="test-type", body={})
            ],
        )  # type: ignore[call-arg]
    )
    assert response == run_response


@pytest.mark.parametrize(
    "workflow, error_msg",
    [
        ["abc", "value is not a valid dict"],
        [None, "none is not an allowed value"],
    ],
)
def test_run_when_given_wrong_parameter_raises_validation_error(
    workflow, error_msg, client: WorkflowClient
):
    with pytest.raises(ValidationError) as err:
        client.run(workflow)
    assert error_msg in str(err.value)


def test_update_when_given_workflow(
    client: WorkflowClient,
    mock_api_caller,
    search_result: WorkflowSearchResult,
    update_response: WorkflowResponse,
):
    mock_api_caller._call_api.return_value = update_response.dict()
    response = client.update(workflow=search_result.to_workflow())
    assert response == update_response


@pytest.mark.parametrize(
    "workflow, error_msg",
    [
        ["abc", "value is not a valid dict"],
        [None, "none is not an allowed value"],
    ],
)
def test_update_when_given_wrong_parameter_raises_validation_error(
    workflow, error_msg, client: WorkflowClient
):
    with pytest.raises(ValidationError) as err:
        client.update(workflow=workflow)
    assert error_msg in str(err.value)
