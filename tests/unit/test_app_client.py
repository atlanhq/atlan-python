# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Unit tests for the App workflow client — sync + async."""

import json
from contextlib import nullcontext
from types import SimpleNamespace
from typing import Optional
from unittest.mock import AsyncMock, MagicMock, Mock

import httpx
import pytest

from pyatlan.client.aio.app import AsyncAppClient
from pyatlan.client.app import _APP_NO_500_RETRY, AppClient
from pyatlan.client.common import ApiCaller, AsyncApiCaller
from pyatlan.client.transport import PyatlanSyncTransport
from pyatlan.errors import AtlanError
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
from pyatlan.model.assets import AppWorkflowRun


@pytest.fixture
def mock_api_caller():
    m = Mock(spec=ApiCaller)
    # Every AppClient call is wrapped in max_retries(...) (the no-500 policy);
    # make it a no-op context manager for tests.
    m.max_retries = Mock(side_effect=lambda *a, **k: nullcontext())
    return m


@pytest.fixture
def client(mock_api_caller):
    return AppClient(mock_api_caller)


def _path(mock) -> str:
    """The API endpoint path passed to the most recent _call_api call."""
    api = mock._call_api.call_args.args[0]
    return api.path


def _running_run(slug: str = "a-1") -> AppWorkflowRun:
    """A minimal in-progress AppWorkflowRun asset for the slug."""
    run = AppWorkflowRun()
    run.qualified_name = f"default/apps/automation_engine/workflows/{slug}/1/runs/r-9"
    return run


def _wire_asset_search(mock, active_runs=()):
    """Wire ``mock.asset.search`` so ``current_page()`` returns ``active_runs``."""
    results = Mock()
    results.current_page = Mock(return_value=list(active_runs))
    mock.asset = Mock()
    mock.asset.search = Mock(return_value=results)
    return mock.asset.search


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


def test_get_all_passes_name_filter(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {"workflows": [{"slug": "a-1"}]}
    client.get_all(name="prod-crawler")
    assert mock_api_caller._call_api.call_args.kwargs["query_params"] == {
        "name": "prod-crawler"
    }


def _conflict(slug: Optional[str] = None) -> AtlanError:
    """A realistic duplicate-name 409 — the server body has no code/status field, so
    the transport raises a plain AtlanError (NOT the mapped ConflictError). When
    ``slug`` is given it is embedded in the body, as Heracles actually returns it."""
    body = {"message": "a workflow with that name already exists"}
    if slug:
        body["slug"] = slug
    return AtlanError(
        SimpleNamespace(
            http_error_code=409,
            error_id="ATLAN-PYTHON-409-000",
            error_message=json.dumps(body),
            user_action="resolve the conflict",
        )
    )


def test_create_reuses_slug_from_conflict_body(client, mock_api_caller):
    # The 409 body carries the existing slug -> reuse it directly, no second call.
    mock_api_caller._call_api.side_effect = [_conflict(slug="prod-crawler-9f")]
    result = client.create(app_id="bigquery-crawler", name="prod-crawler", inputs={})
    assert isinstance(result, AppResponse)
    assert result.slug == "prod-crawler-9f"
    assert mock_api_caller._call_api.call_count == 1  # no get_all needed


def test_create_reuses_slug_via_name_lookup(client, mock_api_caller):
    # 409 body without a slug -> fall back to resolving by name.
    mock_api_caller._call_api.side_effect = [
        _conflict(),
        {
            "workflows": [
                {"slug": "prod-crawler-9f", "name": "prod-crawler", "version": 3}
            ]
        },
    ]
    result = client.create(app_id="bigquery-crawler", name="prod-crawler", inputs={})
    assert isinstance(result, AppResponse)
    assert result.slug == "prod-crawler-9f"
    assert mock_api_caller._call_api.call_args.kwargs["query_params"] == {
        "name": "prod-crawler"
    }


def test_create_reraises_conflict_when_name_not_unique(client, mock_api_caller):
    mock_api_caller._call_api.side_effect = [
        _conflict(),
        {"workflows": [{"slug": "a-1", "name": "dup"}, {"slug": "a-2", "name": "dup"}]},
    ]
    with pytest.raises(AtlanError):
        client.create(app_id="x", name="dup", inputs={})


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
def _server_error_500() -> AtlanError:
    return AtlanError(
        SimpleNamespace(
            http_error_code=500,
            error_id="ATLAN-PYTHON-500-000",
            error_message="internal error",
            user_action="check the server message",
        )
    )


def _wire_asset_search_sequence(mock, pages):
    """Wire ``mock.asset.search`` to return a different current_page() per call."""

    def _result(page):
        r = Mock()
        r.current_page = Mock(return_value=list(page))
        return r

    mock.asset = Mock()
    mock.asset.search = Mock(side_effect=[_result(p) for p in pages])
    return mock.asset.search


def test_submit(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {"slug": "a-1", "run_id": "r-1"}
    result = client.submit("a-1")
    assert isinstance(result, AppRunResponse)
    assert result.run_id == "r-1"
    assert _path(mock_api_caller) == "v1/app/a-1/submit"
    # AICHAT-1659: submit runs under the no-500 retry policy.
    mock_api_caller.max_retries.assert_called_once_with(_APP_NO_500_RETRY)


def test_submit_default_is_not_idempotent(client, mock_api_caller):
    """Default idempotent=False: no pre-check search, just submit (opt-in guard)."""
    search = _wire_asset_search(mock_api_caller, active_runs=[_running_run("a-1")])
    mock_api_caller._call_api.return_value = {"slug": "a-1", "run_id": "r-1"}
    result = client.submit("a-1")  # no idempotent arg
    assert result.run_id == "r-1"
    search.assert_not_called()  # no running-run pre-check by default


def test_submit_idempotent_raises_when_already_running(client, mock_api_caller):
    """idempotent=True: an in-progress run blocks a duplicate submit up front."""
    _wire_asset_search(mock_api_caller, active_runs=[_running_run("a-1")])
    with pytest.raises(AtlanError) as exc:
        client.submit("a-1", idempotent=True)
    assert "already has a run in progress" in str(exc.value)
    # No submit POST was sent — we short-circuited before _call_api.
    mock_api_caller._call_api.assert_not_called()


def test_submit_idempotent_recovers_already_running_on_500(client, mock_api_caller):
    """Lag path: pre-check misses, submit 500s, re-check confirms already-running."""
    # First search (pre-check) sees nothing; second (post-500 recovery) sees the run.
    _wire_asset_search_sequence(mock_api_caller, pages=[[], [_running_run("a-1")]])
    mock_api_caller._call_api.side_effect = _server_error_500()
    with pytest.raises(AtlanError) as exc:
        client.submit("a-1", idempotent=True)
    assert "already has a run in progress" in str(exc.value)  # clean error, not raw 500
    mock_api_caller._call_api.assert_called_once()  # exactly one submit attempt


def test_submit_idempotent_reraises_genuine_500(client, mock_api_caller, monkeypatch):
    """A 500 with no active run (genuine server error) is surfaced as-is."""
    monkeypatch.setattr("pyatlan.client.app._RUN_CHECK_TIMEOUT_SECONDS", 0.0)
    _wire_asset_search_sequence(mock_api_caller, pages=[[], []])  # never running
    mock_api_caller._call_api.side_effect = _server_error_500()
    with pytest.raises(AtlanError) as exc:
        client.submit("a-1", idempotent=True)
    assert "internal error" in str(exc.value)
    assert "already has a run in progress" not in str(exc.value)


def test_submit_idempotent_false_skips_check_and_submits(client, mock_api_caller):
    """idempotent=False forces the submit without the running-run pre-check."""
    search = _wire_asset_search(mock_api_caller, active_runs=[_running_run("a-1")])
    mock_api_caller._call_api.return_value = {"slug": "a-1", "run_id": "r-2"}
    result = client.submit("a-1", idempotent=False)
    assert result.run_id == "r-2"
    assert _path(mock_api_caller) == "v1/app/a-1/submit"
    search.assert_not_called()  # pre-check skipped


def test_find_current_run_none_when_no_active(client, mock_api_caller):
    _wire_asset_search(mock_api_caller, active_runs=[])
    assert client._find_current_run("a-1") is None


# --------------------------------------------------------------------------- #
# AICHAT-1659: app management never retries HTTP 500
# --------------------------------------------------------------------------- #
def _attempts_for_status(status: int) -> int:
    """Drive the app retry policy through the real transport; count HTTP attempts."""
    transport = PyatlanSyncTransport(
        retry=_APP_NO_500_RETRY, client=None, trust_env=False
    )
    inner = MagicMock(return_value=httpx.Response(status))
    transport._transport.handle_request = inner  # type: ignore[method-assign]
    transport.handle_request(
        httpx.Request("POST", "https://example.com/api/service/v1/app/a-1/submit")
    )
    return inner.call_count


def test_app_policy_excludes_500():
    assert 500 not in _APP_NO_500_RETRY.status_forcelist


def test_app_policy_does_not_retry_500_on_the_wire():
    # A single HTTP attempt: a 500 from an app-management POST is never retried,
    # so one submit can never spawn duplicate runs.
    assert _attempts_for_status(500) == 1


def test_app_policy_still_retries_transient_statuses():
    # Sanity: the policy isn't "no retries at all" — genuinely transient infra
    # statuses (429/502/503/504) remain retryable; only 500 is excluded.
    for status in (429, 502, 503, 504):
        assert status in _APP_NO_500_RETRY.status_forcelist


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
def _async_noop_cm(*_a, **_k):
    cm = MagicMock()
    cm.__aenter__ = AsyncMock(return_value=None)
    cm.__aexit__ = AsyncMock(return_value=False)
    return cm


@pytest.fixture
def async_mock_api_caller():
    m = Mock(spec=AsyncApiCaller)
    m._call_api = AsyncMock()
    # Every AsyncAppClient call wraps in `async with max_retries(...)`.
    m.max_retries = Mock(side_effect=_async_noop_cm)
    return m


def _wire_async_asset_search(mock, active_runs=()):
    results = Mock()
    results.current_page = Mock(return_value=list(active_runs))
    mock.asset = Mock()
    mock.asset.search = AsyncMock(return_value=results)
    return mock.asset.search


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


@pytest.mark.asyncio
async def test_async_create_reuses_existing_slug_on_conflict(async_mock_api_caller):
    async_mock_api_caller._call_api.side_effect = [
        _conflict(),
        {"workflows": [{"slug": "n-7", "name": "n", "version": 2}]},
    ]
    client = AsyncAppClient(async_mock_api_caller)
    result = await client.create(app_id="x", name="n", inputs={})
    assert isinstance(result, AppResponse)
    assert result.slug == "n-7"


@pytest.mark.asyncio
async def test_async_get_all_passes_name_filter(async_mock_api_caller):
    async_mock_api_caller._call_api.return_value = {"workflows": [{"slug": "n-7"}]}
    client = AsyncAppClient(async_mock_api_caller)
    await client.get_all(name="n")
    assert async_mock_api_caller._call_api.call_args.kwargs["query_params"] == {
        "name": "n"
    }


@pytest.mark.asyncio
async def test_async_submit_default_not_idempotent(async_mock_api_caller):
    search = _wire_async_asset_search(
        async_mock_api_caller, active_runs=[_running_run("a-1")]
    )
    async_mock_api_caller._call_api.return_value = {"slug": "a-1", "run_id": "r-1"}
    client = AsyncAppClient(async_mock_api_caller)
    result = await client.submit("a-1")  # default idempotent=False
    assert result.run_id == "r-1"
    search.assert_not_called()
    async_mock_api_caller.max_retries.assert_called_once_with(_APP_NO_500_RETRY)


@pytest.mark.asyncio
async def test_async_submit_idempotent_raises_when_already_running(
    async_mock_api_caller,
):
    _wire_async_asset_search(async_mock_api_caller, active_runs=[_running_run("a-1")])
    client = AsyncAppClient(async_mock_api_caller)
    with pytest.raises(AtlanError) as exc:
        await client.submit("a-1", idempotent=True)
    assert "already has a run in progress" in str(exc.value)
    async_mock_api_caller._call_api.assert_not_called()


@pytest.mark.asyncio
async def test_async_submit_idempotent_false_forces(async_mock_api_caller):
    search = _wire_async_asset_search(
        async_mock_api_caller, active_runs=[_running_run("a-1")]
    )
    async_mock_api_caller._call_api.return_value = {"slug": "a-1", "run_id": "r-2"}
    client = AsyncAppClient(async_mock_api_caller)
    result = await client.submit("a-1", idempotent=False)
    assert result.run_id == "r-2"
    search.assert_not_called()
