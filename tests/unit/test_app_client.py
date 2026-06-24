# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Unit tests for the App workflow client — sync + async."""

from unittest.mock import AsyncMock, Mock

import pytest

from pyatlan.client.aio.app import AsyncAppClient
from pyatlan.client.app import AppClient
from pyatlan.client.common import ApiCaller, AsyncApiCaller
from pyatlan.model.app import (
    AppDeleteResponse,
    AppInfo,
    AppInputContract,
    AppList,
    AppResponse,
    AppRunCancelResponse,
    AppRunResponse,
    AppScheduleResponse,
    AppSummary,
)


@pytest.fixture
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture
def client(mock_api_caller):
    return AppClient(mock_api_caller)


def _path(mock) -> str:
    """The API endpoint path passed to the most recent _call_api call."""
    api = mock._call_api.call_args.args[0]
    return api.path


# --------------------------------------------------------------------------- #
# Construction guard
# --------------------------------------------------------------------------- #
def test_init_rejects_non_apicaller():
    with pytest.raises(Exception) as exc:
        AppClient("not-a-client")
    assert "ApiCaller" in str(exc.value)


# --------------------------------------------------------------------------- #
# Discovery
# --------------------------------------------------------------------------- #
def test_describe(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {
        "app_id": "bigquery-crawler",
        "name": "BigQuery",
        "native_ready": True,
        "execution_mode": "native",
        "entrypoints": [{"name": "crawler"}],
    }
    result = client.describe("bigquery-crawler")
    assert isinstance(result, AppInfo)
    assert result.native_ready is True
    assert [e.name for e in result.entrypoints] == ["crawler"]
    assert _path(mock_api_caller) == "v1/apps/bigquery-crawler"


def test_get_input_contract_passes_entrypoint(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {
        "title": "AppInputContract",
        "type": "object",
        "properties": {"connection": {"type": "object"}, "credential_guid": {}},
        "$defs": {"Foo": {}},
    }
    result = client.get_input_contract("bigquery-crawler", entrypoint="crawler")
    assert isinstance(result, AppInputContract)
    assert result.field_names() == ["connection", "credential_guid"]
    assert result.credential_field() == "credential_guid"
    assert list(result.defs) == ["Foo"]
    # entrypoint forwarded as a query param
    assert mock_api_caller._call_api.call_args.kwargs["query_params"] == {
        "entrypoint": "crawler"
    }


# --------------------------------------------------------------------------- #
# Lifecycle
# --------------------------------------------------------------------------- #
def test_create_builds_request_and_returns_slug(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {
        "execution_mode": "native",
        "slug": "bq-prod-crawl-3f9ab2c1",
        "version": 1717286400,
    }
    result = client.create(
        app_id="bigquery-crawler",
        name="bq-prod-crawl",
        inputs={"connection": {"qualifiedName": "default/bigquery/1"}},
        entrypoint="crawler",
        run=False,
    )
    assert isinstance(result, AppResponse)
    assert result.slug == "bq-prod-crawl-3f9ab2c1"
    assert result.run_id is None  # run=False
    # request_obj serializes snake_case, optional unset fields omitted
    sent = mock_api_caller._call_api.call_args.kwargs["request_obj"].json(
        by_alias=True, exclude_unset=True
    )
    assert '"app_id": "bigquery-crawler"' in sent
    assert '"run": false' in sent
    assert "schedule" not in sent  # omitted


def test_get_all(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {
        "workflows": [{"slug": "a-1", "name": "a"}],
        "has_more": True,
        "next_cursor": "1",
    }
    result = client.get_all(limit=2)
    assert isinstance(result, AppList)
    assert result.has_more is True
    assert result.workflows[0].slug == "a-1"
    assert mock_api_caller._call_api.call_args.kwargs["query_params"] == {"limit": 2}


def test_get_one(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {
        "slug": "a-1",
        "name": "a",
        "version": 7,
        "owner": "jane",
        "app_id": "bigquery-crawler",
    }
    result = client.get("a-1")
    assert isinstance(result, AppSummary)
    assert result.owner == "jane"
    assert _path(mock_api_caller) == "v1/app/a-1"


def test_update_full_replace(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {"slug": "a-1", "version": 99}
    result = client.update("a-1", inputs={"connection": {}})
    assert isinstance(result, AppResponse)
    assert result.version == 99
    assert _path(mock_api_caller) == "v1/app/a-1"


def test_delete(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {"slug": "a-1", "archived": True}
    result = client.delete("a-1")
    assert isinstance(result, AppDeleteResponse)
    assert result.archived is True


# --------------------------------------------------------------------------- #
# Running
# --------------------------------------------------------------------------- #
def test_submit(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {"slug": "a-1", "run_id": "r-1"}
    result = client.submit("a-1")
    assert isinstance(result, AppRunResponse)
    assert result.run_id == "r-1"
    assert _path(mock_api_caller) == "v1/app/a-1/submit"


@pytest.mark.parametrize(
    "status,terminal",
    [
        ("Running", False),
        ("Pending", False),
        ("Succeeded", True),
        ("Failed", True),
        ("Terminated", True),
    ],
)
def test_get_run_is_terminal(client, mock_api_caller, status, terminal):
    mock_api_caller._call_api.return_value = {"run_id": "r-1", "status": status}
    result = client.get_run("r-1")
    assert result.is_terminal is terminal
    assert result.is_success is (status == "Succeeded")
    assert _path(mock_api_caller) == "v1/app/runs/r-1"


def test_cancel_run(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {
        "run_id": "r-1",
        "cancelled": True,
        "status": "Stopped",
    }
    result = client.cancel_run("r-1")
    assert isinstance(result, AppRunCancelResponse)
    assert result.cancelled is True
    assert _path(mock_api_caller) == "v1/app/runs/r-1/cancel"


# --------------------------------------------------------------------------- #
# Scheduling
# --------------------------------------------------------------------------- #
def test_add_schedule(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {
        "trigger_id": "t-1",
        "cron": "0 9 * * *",
        "timezone": "Asia/Kolkata",
    }
    result = client.add_schedule("a-1", cron="0 9 * * *", timezone="Asia/Kolkata")
    assert isinstance(result, AppScheduleResponse)
    assert result.trigger_id == "t-1"
    assert _path(mock_api_caller) == "v1/app/a-1/schedule"


def test_remove_schedule(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {"trigger_id": "t-1", "deleted": True}
    result = client.remove_schedule("a-1", trigger_id="t-1")
    assert result.deleted is True
    assert _path(mock_api_caller) == "v1/app/a-1/schedule/t-1"


# --------------------------------------------------------------------------- #
# Async parity (smoke)
# --------------------------------------------------------------------------- #
@pytest.fixture
def async_mock_api_caller():
    m = Mock(spec=AsyncApiCaller)
    m._call_api = AsyncMock()
    return m


@pytest.mark.asyncio
async def test_async_describe(async_mock_api_caller):
    async_mock_api_caller._call_api.return_value = {
        "app_id": "bigquery-crawler",
        "native_ready": True,
        "entrypoints": [{"name": "crawler"}],
    }
    client = AsyncAppClient(async_mock_api_caller)
    result = await client.describe("bigquery-crawler")
    assert isinstance(result, AppInfo)
    assert result.native_ready is True


@pytest.mark.asyncio
async def test_async_create(async_mock_api_caller):
    async_mock_api_caller._call_api.return_value = {"slug": "x-1", "version": 1}
    client = AsyncAppClient(async_mock_api_caller)
    result = await client.create(app_id="x", name="n", inputs={}, run=False)
    assert isinstance(result, AppResponse)
    assert result.slug == "x-1"
