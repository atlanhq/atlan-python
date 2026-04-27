# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""
Regression tests for GOVFOUN-408: httpcore connection pool deadlock fix.

Root cause: csa-metadata-completeness hung indefinitely on masterc-prd because
two missing configs caused all 100 httpcore connection slots to fill with
CLOSE_WAIT zombies, then 109 worker threads blocked forever in
wait_for_connection(timeout=None).

These tests verify the two SDK-side fixes:
1. httpx.Timeout has pool=30.0 — threads raise PoolTimeout after 30s instead
   of waiting forever.
2. httpx.Limits has keepalive_expiry=30.0 — client retires idle connections
   before nginx's keepalive_timeout=75s FIN, preventing CLOSE_WAIT accumulation.
"""

import contextvars
from unittest.mock import Mock, patch

import httpx
import pytest

from pyatlan.client.atlan import (
    AtlanClient,
    _DEFAULT_POOL_LIMITS,
    _DEFAULT_POOL_TIMEOUT_SECONDS,
)
from pyatlan.client.transport import PyatlanSyncTransport
from pyatlan.model.assets import AtlasGlossary


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def client():
    return AtlanClient()


def _error_response():
    r = Mock()
    r.status_code = 500
    r.text = "internal server error"
    return r


def _trigger_api_call(client: AtlanClient) -> None:
    """Drive any outbound request through _call_api_internal."""
    try:
        client.asset.save(AtlasGlossary.creator(name="t"))
    except Exception:
        pass


def _get_httpcore_pool(client: AtlanClient):
    """Access the underlying httpcore pool. Relies on httpx internals;
    may need updating if httpx changes its internal structure."""
    try:
        transport = client._session._transport
        assert isinstance(transport, PyatlanSyncTransport)
        return transport._transport._pool
    except AttributeError:
        pytest.skip("httpx internal structure changed; update test helper")


# ---------------------------------------------------------------------------
# Pool timeout
# ---------------------------------------------------------------------------


@patch.object(AtlanClient, "_session")
def test_pool_timeout_is_30_seconds(mock_session, client):
    """pool=30.0 must be set — the live deadlock showed pool=None caused infinite blocking."""
    mock_session.request.return_value = _error_response()
    _trigger_api_call(client)
    assert mock_session.request.called, "no HTTP request was made"
    timeout = mock_session.request.call_args.kwargs["timeout"]
    assert timeout.pool == _DEFAULT_POOL_TIMEOUT_SECONDS


@patch.object(AtlanClient, "_session")
def test_pool_timeout_is_not_none(mock_session, client):
    """pool timeout must never be None — threading.Event.wait(timeout=None) blocks forever."""
    mock_session.request.return_value = _error_response()
    _trigger_api_call(client)
    assert mock_session.request.called
    timeout = mock_session.request.call_args.kwargs["timeout"]
    assert timeout.pool is not None


@patch.object(AtlanClient, "_session")
def test_connect_timeout_unchanged(mock_session, client):
    """connect timeout must still equal client.connect_timeout (default 30s)."""
    mock_session.request.return_value = _error_response()
    _trigger_api_call(client)
    assert mock_session.request.called
    timeout = mock_session.request.call_args.kwargs["timeout"]
    assert timeout.connect == client.connect_timeout


@patch.object(AtlanClient, "_session")
def test_read_timeout_unchanged(mock_session, client):
    """read timeout must still equal client.read_timeout (default 900s)."""
    mock_session.request.return_value = _error_response()
    _trigger_api_call(client)
    assert mock_session.request.called
    timeout = mock_session.request.call_args.kwargs["timeout"]
    assert timeout.read == client.read_timeout


@patch.object(AtlanClient, "_session")
def test_pool_timeout_propagates_not_hangs(mock_session, client):
    """httpx.PoolTimeout must propagate — if it were swallowed the workflow would still hang."""
    mock_session.request.side_effect = httpx.PoolTimeout(
        "connection pool exhausted", request=None
    )
    with pytest.raises(Exception):
        client.asset.save(AtlasGlossary.creator(name="t"))


# ---------------------------------------------------------------------------
# Transport limits
# ---------------------------------------------------------------------------


def test_transport_max_connections_is_50(client):
    """max_connections=50 reduces blast radius when CLOSE_WAIT sockets accumulate."""
    assert _get_httpcore_pool(client)._max_connections == _DEFAULT_POOL_LIMITS.max_connections


def test_transport_keepalive_expiry_is_30_seconds(client):
    """keepalive_expiry=30.0 — client closes idle connections before nginx's 75s FIN."""
    assert _get_httpcore_pool(client)._keepalive_expiry == _DEFAULT_POOL_LIMITS.keepalive_expiry


def test_transport_max_keepalive_connections_is_10(client):
    """max_keepalive_connections=10 bounds idle connections held in the pool."""
    assert _get_httpcore_pool(client)._max_keepalive_connections == _DEFAULT_POOL_LIMITS.max_keepalive_connections


# ---------------------------------------------------------------------------
# max_retries context manager
# ---------------------------------------------------------------------------


def _capture_transport_limits(client: AtlanClient) -> httpx.Limits:
    """Enter max_retries, capture the limits used to construct the new transport."""
    captured: dict = {}
    original_init = PyatlanSyncTransport.__init__

    def capturing_init(self_t, retry=None, client=None, **kwargs):  # noqa: ARG001
        if "limits" in kwargs:
            captured["limits"] = kwargs["limits"]
        original_init(self_t, retry=retry, client=client, **kwargs)

    with patch.object(PyatlanSyncTransport, "__init__", capturing_init):
        with client.max_retries():
            pass

    assert "limits" in captured, "max_retries did not pass limits to PyatlanSyncTransport"
    return captured["limits"]


def test_max_retries_transport_max_connections_is_50(client):
    """max_retries context manager must use the same max_connections=50."""
    assert _capture_transport_limits(client).max_connections == 50


def test_max_retries_transport_keepalive_expiry_is_30_seconds(client):
    """max_retries context manager must use keepalive_expiry=30.0."""
    assert _capture_transport_limits(client).keepalive_expiry == 30.0


def test_max_retries_transport_max_keepalive_connections_is_10(client):
    """max_retries context manager must use max_keepalive_connections=10."""
    assert _capture_transport_limits(client).max_keepalive_connections == 10


def test_max_retries_replaces_transport_inside_context(client):
    """max_retries installs a fresh transport for the duration of the context."""
    original = client._session._transport
    with client.max_retries():
        assert client._session._transport is not original


def test_max_retries_restores_original_transport_on_exit(client):
    """max_retries restores the original transport when the context exits."""
    original = client._session._transport
    with client.max_retries():
        pass
    assert client._session._transport is original


# ---------------------------------------------------------------------------
# reset_http_session
# ---------------------------------------------------------------------------


class TestResetHttpSession:
    def test_creates_new_session(self, client):
        """reset_http_session() replaces _session with a brand-new httpx.Client."""
        old_session = client._session
        client.reset_http_session()
        assert client._session is not old_session

    def test_new_session_has_correct_limits(self, client):
        """New session must use the same pool limits as the initial session."""
        client.reset_http_session()
        assert _get_httpcore_pool(client)._max_connections == _DEFAULT_POOL_LIMITS.max_connections
        assert _get_httpcore_pool(client)._keepalive_expiry == _DEFAULT_POOL_LIMITS.keepalive_expiry
        assert _get_httpcore_pool(client)._max_keepalive_connections == _DEFAULT_POOL_LIMITS.max_keepalive_connections

    def test_closes_old_session(self, client):
        """reset_http_session() calls close() on the old session before replacing it."""
        mock_close = Mock()
        client._session.close = mock_close
        client.reset_http_session()
        mock_close.assert_called_once()

    def test_resets_401_retry_flag(self, client):
        """_401_has_retried ContextVar must be reset to False after session rebuild."""
        def _run():
            client._401_has_retried.set(True)
            client.reset_http_session()
            return client._401_has_retried.get()

        result = contextvars.copy_context().run(_run)
        assert result is False

    def test_preserves_proxy_kwargs(self, client):
        """proxy and verify attrs are forwarded to the new PyatlanSyncTransport."""
        client.proxy = "http://proxy.example.com:8080"
        client.verify = "/path/to/cert.pem"

        captured: dict = {}
        original_init = PyatlanSyncTransport.__init__

        def capturing_init(self_t, retry=None, client=None, **kwargs):  # noqa: ARG001
            captured.update(kwargs)
            original_init(self_t, retry=retry, client=client, **kwargs)

        # Patch httpx.HTTPTransport so it doesn't try to load the fake cert file
        # from disk — we only need to verify the kwargs are forwarded correctly.
        with patch.object(PyatlanSyncTransport, "__init__", capturing_init), patch(
            "httpx.HTTPTransport", Mock(return_value=Mock())
        ):
            client.reset_http_session()

        assert captured.get("proxy") == "http://proxy.example.com:8080"
        assert captured.get("verify") == "/path/to/cert.pem"
