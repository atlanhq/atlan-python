# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest
from pydantic.v1 import ValidationError

from pyatlan.client.aio.query import AsyncQueryClient
from pyatlan.client.common import AsyncApiCaller
from pyatlan.errors import InvalidRequestError
from pyatlan.model.query import QueryRequest, QueryResponse

QUERY_RESPONSES = Path(__file__).parent.parent / "data" / "query_responses.txt"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")


@pytest.fixture()
def mock_async_api_caller():
    mock_caller = Mock(spec=AsyncApiCaller)
    mock_caller._call_api = AsyncMock()
    return mock_caller


@pytest.fixture()
def query_request() -> QueryRequest:
    return QueryRequest(
        sql="test-sql", data_source_name="test-ds-name", default_schema="test-schema"
    )


@pytest.fixture()
def query_response() -> QueryResponse:
    return QueryResponse()


@pytest.fixture()
def mock_async_session():
    lines_from_file = []

    with open(QUERY_RESPONSES, "r", encoding="utf-8") as file:
        lines_from_file = [line.strip() for line in file.readlines()]

    # Convert the text lines to the expected JSON format
    import json

    events = []
    for line in lines_from_file:
        if line.startswith("data: "):
            try:
                event_data = json.loads(line[6:])  # Remove "data: " prefix
                events.append(event_data)
            except json.JSONDecodeError:
                pass

    return events


@pytest.mark.parametrize("test_api_caller", ["abc", None])
def test_init_when_wrong_class_raises_exception(test_api_caller):
    with pytest.raises(
        InvalidRequestError,
        match="ATLAN-PYTHON-400-048 Invalid parameter type for client should be AsyncApiCaller",
    ):
        AsyncQueryClient(test_api_caller)


@pytest.mark.parametrize(
    "test_request, error_msg",
    [[None, "none is not an allowed value"], ["123", "value is not a valid dict"]],
)
def test_query_stream_wrong_params_raises_validation_error(
    test_request, error_msg, mock_async_api_caller
):
    client = AsyncQueryClient(client=mock_async_api_caller)
    with pytest.raises(ValidationError) as err:
        client.stream(request=test_request)
    assert error_msg in str(err.value)


@pytest.mark.asyncio
async def test_stream_get_when_given_request(
    mock_async_api_caller,
    query_request: QueryRequest,
    mock_async_session,
):
    mock_async_api_caller._call_api.return_value = mock_async_session
    client = AsyncQueryClient(client=mock_async_api_caller)

    response = await client.stream(request=query_request)
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
