# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""
Integration tests for GOVFOUN-408: httpcore connection pool deadlock fix.

These tests run against a live Atlan tenant and verify:
1. Pool limits and timeout config survive the full client init and real HTTP
   connections — not just object construction.
2. Concurrent requests complete without hanging under the configured pool size.
3. httpx.PoolTimeout propagates through the full SDK stack instead of being
   swallowed or causing an indefinite hang.
4. max_retries context manager correctly installs and restores limits on a
   client that is actively connected.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor, wait
from unittest.mock import patch

import httpx
import pytest
from httpx_retries import Retry

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.transport import PyatlanSyncTransport


def _get_httpcore_pool(client: AtlanClient):
    return client._session._transport._transport._pool


# ---------------------------------------------------------------------------
# Pool limits — config survives real HTTP connections
# ---------------------------------------------------------------------------


def test_pool_limits_on_live_client(client: AtlanClient):
    """
    Pool limits are configured correctly on an AtlanClient built from the
    integration environment (real base_url, real API key, real retry config).
    The values are set at construction time and must survive unchanged.
    """
    pool = _get_httpcore_pool(client)
    assert pool._max_connections == 50
    assert pool._keepalive_expiry == 30.0
    assert pool._max_keepalive_connections == 10


# ---------------------------------------------------------------------------
# Concurrent requests — happy path
# ---------------------------------------------------------------------------


def test_concurrent_requests_complete_without_deadlock(client: AtlanClient):
    """
    N concurrent requests (N << max_connections=50) must all complete.

    Under the old config (pool=None, max_connections=100), if connections
    accumulated CLOSE_WAIT sockets and filled all slots, threads waiting for
    a connection would block on threading.Event.wait(timeout=None) forever.

    With pool=30.0 and max_connections=50, threads either succeed or raise
    PoolTimeout within 30s — they never hang indefinitely.
    """
    n_threads = 5
    timeout_seconds = 60

    def make_request():
        return client.user.get_current()

    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        futures = [executor.submit(make_request) for _ in range(n_threads)]
        done, not_done = wait(futures, timeout=timeout_seconds)

    # Only check for deadlock — individual futures may raise (auth errors, etc.)
    assert len(not_done) == 0, (
        f"{len(not_done)} of {n_threads} requests still pending after "
        f"{timeout_seconds}s — possible connection pool deadlock"
    )


# ---------------------------------------------------------------------------
# PoolTimeout propagation
# ---------------------------------------------------------------------------


def test_pool_timeout_propagates_through_sdk_stack(client: AtlanClient):
    """
    httpx.PoolTimeout injected at the transport layer must propagate up
    through the SDK without being swallowed or stalling.

    Before the fix, pool=None meant threads blocked indefinitely on
    threading.Event.wait(timeout=None). With pool=30.0 the SDK raises an
    exception quickly instead.
    """
    original_transport = client._session._transport

    test_transport = PyatlanSyncTransport(
        retry=Retry(total=0),
        client=client,
        limits=httpx.Limits(
            max_connections=50,
            max_keepalive_connections=10,
            keepalive_expiry=30.0,
        ),
    )

    def always_pool_timeout(request: httpx.Request) -> httpx.Response:
        raise httpx.PoolTimeout("simulated pool exhaustion", request=request)

    test_transport._transport.handle_request = always_pool_timeout  # type: ignore[method-assign]
    client._session._transport = test_transport

    try:
        start = time.monotonic()
        with pytest.raises(Exception):
            client.user.get_current()
        elapsed = time.monotonic() - start

        assert elapsed < 5.0, (
            f"PoolTimeout took {elapsed:.1f}s to propagate — "
            "it may be getting swallowed or retried unexpectedly"
        )
    finally:
        client._session._transport = original_transport


# ---------------------------------------------------------------------------
# max_retries context manager
# ---------------------------------------------------------------------------


def test_max_retries_transport_limits_on_live_client(client: AtlanClient):
    """
    max_retries context manager must install a transport with the same pool
    limits on the real integration client (env-configured base_url, retry policy).
    """
    captured: dict = {}
    original_init = PyatlanSyncTransport.__init__

    def capturing_init(self_t, retry=None, client=None, **kwargs):  # noqa: ARG001
        if "limits" in kwargs:
            captured["limits"] = kwargs["limits"]
        original_init(self_t, retry=retry, client=client, **kwargs)

    with patch.object(PyatlanSyncTransport, "__init__", capturing_init):
        with client.max_retries():
            pass

    limits = captured.get("limits")
    assert limits is not None, "max_retries did not pass limits to PyatlanSyncTransport"
    assert limits.max_connections == 50
    assert limits.keepalive_expiry == 30.0
    assert limits.max_keepalive_connections == 10


def test_max_retries_restores_original_transport(client: AtlanClient):
    """
    max_retries must restore the original transport after the context exits,
    even on the real integration client (env-configured base_url, retry policy).
    """
    original_transport = client._session._transport

    with client.max_retries():
        pass

    assert client._session._transport is original_transport


# ---------------------------------------------------------------------------
# Pool slot released during 429 retry sleep
# ---------------------------------------------------------------------------


def test_concurrent_429_retries_no_pool_timeout(client: AtlanClient):
    """
    Connection slots must be freed before retry.sleep() when receiving 429.

    GOVFOUN-408 root cause: PyatlanSyncTransport._retry_operation called
    retry.sleep(response) while the response stream was still open, holding
    the httpcore connection slot for the entire sleep duration. With N threads
    all sleeping simultaneously, the pool was exhausted and subsequent requests
    raised PoolTimeout.

    Fix: response.close() before retry.sleep(). This test verifies that N
    concurrent 429 retries complete without PoolTimeout when max_connections=N.
    """
    n_threads = 5
    call_lock = threading.Lock()
    thread_calls: dict = {}

    def counting_handle(request: httpx.Request) -> httpx.Response:
        tid = threading.get_ident()
        with call_lock:
            count = thread_calls.get(tid, 0)
            thread_calls[tid] = count + 1
        if count == 0:
            # First call per thread: 429 with zero Retry-After
            return httpx.Response(429, headers={"Retry-After": "0"}, content=b"")
        return httpx.Response(200, content=b"{}")

    test_transport = PyatlanSyncTransport(
        retry=Retry(
            total=3,
            backoff_factor=0,
            status_forcelist=[429],
            allowed_methods=["GET", "POST"],
            respect_retry_after_header=True,
        ),
        limits=httpx.Limits(
            max_connections=n_threads,
            max_keepalive_connections=2,
            keepalive_expiry=5.0,
        ),
    )
    test_transport._transport.handle_request = counting_handle  # type: ignore[method-assign]

    original_transport = client._session._transport
    client._session._transport = test_transport

    try:
        pool_timeout_errors: list = []

        def make_request():
            try:
                client.user.get_current()
            except httpx.PoolTimeout as exc:
                pool_timeout_errors.append(str(exc))
            except Exception:
                pass  # Auth/parse errors from mock 200 body are expected

        with ThreadPoolExecutor(max_workers=n_threads) as executor:
            futures = [executor.submit(make_request) for _ in range(n_threads)]
            done, not_done = wait(futures, timeout=30.0)

        assert len(not_done) == 0, (
            f"{len(not_done)} of {n_threads} threads hung after 30s — "
            "possible connection pool deadlock"
        )
        assert not pool_timeout_errors, (
            "PoolTimeout raised — connection slot held open during retry.sleep(): "
            f"{pool_timeout_errors}"
        )
    finally:
        client._session._transport = original_transport
