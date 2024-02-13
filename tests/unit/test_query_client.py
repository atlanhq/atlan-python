# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from pydantic.v1 import ValidationError

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.query import QueryClient
from pyatlan.errors import ApiError, InvalidRequestError, LogicError
from pyatlan.model.query import QueryRequest, QueryResponse

QUERY_RESPONSES = Path(__file__).parent / "data" / "query_responses.txt"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")


@pytest.fixture()
def client():
    return AtlanClient()


@pytest.fixture()
def query_request() -> QueryRequest:
    return QueryRequest(
        sql="test-sql", data_source_name="test-ds-name", default_schema="test-schema"
    )


@pytest.fixture()
def query_response() -> QueryResponse:
    return QueryResponse()


@pytest.fixture()
def mock_session():
    with patch.object(AtlanClient, "_session") as mock_session:
        lines_from_file = []
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = "test-content"
        with open(QUERY_RESPONSES, "r", encoding="utf-8") as file:
            lines_from_file = [line.strip() for line in file.readlines()]
        mock_response.iter_lines.return_value = lines_from_file
        mock_session.request.return_value = mock_response
        yield mock_session


@pytest.mark.parametrize("test_api_caller", ["abc", None])
def test_init_when_wrong_class_raises_exception(test_api_caller):
    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-048 Invalid parameter type for client should be ApiCaller",
    ):
        QueryClient(test_api_caller)


@pytest.mark.parametrize(
    "test_request, error_msg",
    [[None, "none is not an allowed value"], ["123", "value is not a valid dict"]],
)
def test_query_stream_wrong_params_raises_validation_error(
    test_request, error_msg, client: AtlanClient
):
    with pytest.raises(ValidationError) as err:
        client.queries.stream(request=test_request)
    assert error_msg in str(err.value)


@pytest.mark.parametrize(
    "test_response, test_error, error_msg",
    [
        [["invalid data"], LogicError, "Unable to deserialize value"],
        [["data: invalid data"], ApiError, "Invalid response object from API"],
    ],
)
def test_stream_get_raises_error(
    client: AtlanClient,
    query_request: QueryRequest,
    test_response,
    test_error,
    error_msg,
    mock_session,
):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = "test-content"
    mock_response.iter_lines.return_value = test_response
    mock_session.request.return_value = mock_response
    with pytest.raises(test_error) as err:
        client.queries.stream(request=query_request)
    assert error_msg in str(err.value)


def test_stream_get_when_given_request(
    client: AtlanClient,
    query_request: QueryRequest,
    mock_session,
):
    response = client.queries.stream(request=query_request)
    assert response.rows
    assert len(response.rows) == 14
    assert response.columns
    assert len(response.columns) == 7
    assert response.request_id
    # Last event is an error
    assert response.query_id is None
    assert response.error_name
    assert response.error_code
    assert response.error_message
    assert response.details
