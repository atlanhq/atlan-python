# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from json import load, loads
from pathlib import Path
from unittest.mock import Mock

import pytest
from pydantic.v1 import ValidationError

from pyatlan.client.common import ApiCaller
from pyatlan.client.task import TaskClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import AtlanTaskStatus, AtlanTaskType
from pyatlan.model.fluent_tasks import FluentTasks
from pyatlan.model.task import AtlanTask, TaskSearchRequest, TaskSearchResponse

TEST_DATA_DIR = Path(__file__).parent / "data"
TASK_SEARCH_JSON = "task_search.json"
TASK_RESPONSES_DIR = TEST_DATA_DIR / "task_responses"
FLUENT_TASKS_REQUEST_JSON = "fluent_tasks.json"
TASK_REQUESTS_DIR = TEST_DATA_DIR / "task_requests"


def load_json(respones_dir, filename):
    with (respones_dir / filename).open() as input_file:
        return load(input_file)


def to_json(model):
    return model.json(by_alias=True, exclude_none=True)


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture(scope="module")
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def task_search_request() -> TaskSearchRequest:
    return (
        FluentTasks()
        .page_size(1)
        .where(AtlanTask.STATUS.match(AtlanTaskStatus.COMPLETE.value))
        .to_request()
    )


@pytest.fixture()
def task_search_response_json():
    return load_json(TASK_RESPONSES_DIR, TASK_SEARCH_JSON)


@pytest.fixture()
def task_search_request_json():
    return load_json(TASK_REQUESTS_DIR, FLUENT_TASKS_REQUEST_JSON)


@pytest.mark.parametrize("test_api_caller", ["abc", None])
def test_init_when_wrong_class_raises_exception(test_api_caller):
    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-048 Invalid parameter type for client should be ApiCaller",
    ):
        TaskClient(test_api_caller)


@pytest.mark.parametrize(
    "test_request, error_msg",
    [[None, "none is not an allowed value"], ["123", "value is not a valid dict"]],
)
def test_task_seaech_wrong_params_raises_validation_error(test_request, error_msg):
    with pytest.raises(ValidationError) as err:
        TaskClient.search(request=test_request)
    assert error_msg in str(err.value)


@pytest.mark.parametrize(
    "test_method, test_client",
    [["count", [None, 123, "abc"]], ["execute", [None, 123, "abc"]]],
)
def test_fluent_tasks_invalid_client_raises_invalid_request_error(
    test_method,
    test_client,
):
    client_method = getattr(FluentTasks(), test_method)
    for invalid_client in test_client:
        with pytest.raises(
            InvalidRequestError, match="No Atlan client has been provided."
        ):
            client_method(client=invalid_client)


def test_task_search_get_when_given_request(
    mock_api_caller,
    task_search_request,
    task_search_request_json: TaskSearchRequest,
    task_search_response_json: TaskSearchResponse,
):
    last_page_response = {"tasks": [], "approximateCount": 1}
    mock_api_caller._call_api.side_effect = [
        task_search_response_json,
        last_page_response,
    ]
    client = TaskClient(client=mock_api_caller)
    response = client.search(request=task_search_request)
    request_dsl_json = to_json(response._criteria)

    assert loads(request_dsl_json) == task_search_request_json
    assert response
    assert response.count == 1
    for task in response:
        assert task.guid
        assert task.end_time
        assert task.start_time
        assert task.updated_time
        assert task.created_by
        assert task.parameters
        assert task.attempt_count == 0
        assert task.entity_guid
        assert task.time_taken_in_seconds
        assert task.classification_id
        assert task.status == AtlanTaskStatus.COMPLETE
        assert task.type == AtlanTaskType.CLASSIFICATION_PROPAGATION_ADD
    assert mock_api_caller._call_api.call_count == 2
    mock_api_caller.reset_mock()
