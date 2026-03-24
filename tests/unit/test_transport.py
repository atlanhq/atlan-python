# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""Unit tests for pyatlan.client.transport and pyatlan.client.common.transport."""

from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest
from httpx_retries import Retry

from pyatlan.client.common.transport import (
    check_for_duplicate_policy,
    check_for_duplicate_policy_async,
    create_mock_response,
    find_existing_policy,
    find_existing_policy_async,
    parse_auth_policy_entity,
)
from pyatlan.client.constants import BULK_UPDATE
from pyatlan.client.transport import PyatlanAsyncTransport, PyatlanSyncTransport

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

BULK_URL = f"https://example.atlan.com/api/meta/{BULK_UPDATE.path}"
POLICY_NAME = "Test Policy"
PERSONA_GUID = "persona-guid-123"
TEMP_GUID = "-1"
EXISTING_GUID = "real-guid-abc"

EXISTING_POLICY = {
    "typeName": "AuthPolicy",
    "guid": EXISTING_GUID,
    "attributes": {"name": POLICY_NAME, "qualifiedName": f"default/{POLICY_NAME}"},
}


def _make_bulk_request(
    policy_name: str = POLICY_NAME,
    persona_guid: str = PERSONA_GUID,
    temp_guid: str = TEMP_GUID,
    method: str = "POST",
    url: str = BULK_URL,
) -> httpx.Request:
    import json

    body = {
        "entities": [
            {
                "typeName": "AuthPolicy",
                "guid": temp_guid,
                "attributes": {
                    "name": policy_name,
                    "accessControl": {"guid": persona_guid},
                },
            }
        ]
    }
    return httpx.Request(method, url, content=json.dumps(body).encode())


# ---------------------------------------------------------------------------
# parse_auth_policy_entity
# ---------------------------------------------------------------------------


class TestParseAuthPolicyEntity:
    def test_returns_none_for_non_post(self):
        req = httpx.Request("GET", BULK_URL)
        assert parse_auth_policy_entity(req) is None

    def test_returns_none_for_non_bulk_url(self):
        req = httpx.Request("POST", "https://example.com/other/endpoint")
        assert parse_auth_policy_entity(req) is None

    def test_returns_none_for_empty_body(self):
        req = httpx.Request("POST", BULK_URL)
        assert parse_auth_policy_entity(req) is None

    def test_returns_none_when_no_auth_policy_entity(self):
        import json

        body = {"entities": [{"typeName": "Table", "guid": "-1", "attributes": {}}]}
        req = httpx.Request("POST", BULK_URL, content=json.dumps(body).encode())
        assert parse_auth_policy_entity(req) is None

    def test_returns_none_when_missing_persona_guid(self):
        import json

        body = {
            "entities": [
                {
                    "typeName": "AuthPolicy",
                    "guid": TEMP_GUID,
                    "attributes": {"name": POLICY_NAME},
                }
            ]
        }
        req = httpx.Request("POST", BULK_URL, content=json.dumps(body).encode())
        assert parse_auth_policy_entity(req) is None

    def test_returns_tuple_for_valid_auth_policy(self):
        req = _make_bulk_request()
        result = parse_auth_policy_entity(req)
        assert result == (POLICY_NAME, PERSONA_GUID, TEMP_GUID)

    def test_uses_custom_temp_guid(self):
        req = _make_bulk_request(temp_guid="-3")
        policy_name, persona_guid, temp_guid = parse_auth_policy_entity(req)
        assert temp_guid == "-3"

    def test_returns_none_for_invalid_json(self):
        req = httpx.Request("POST", BULK_URL, content=b"{not valid json")
        assert parse_auth_policy_entity(req) is None

    def test_returns_none_for_invalid_utf8(self):
        req = httpx.Request("POST", BULK_URL, content=b"\xff\xfe")
        assert parse_auth_policy_entity(req) is None


# ---------------------------------------------------------------------------
# create_mock_response
# ---------------------------------------------------------------------------


class TestCreateMockResponse:
    def test_status_200(self):
        resp = create_mock_response(EXISTING_POLICY, TEMP_GUID)
        assert resp.status_code == 200

    def test_mutated_entities_contains_policy(self):
        resp = create_mock_response(EXISTING_POLICY, TEMP_GUID)
        body = resp.json()
        assert body["mutatedEntities"]["CREATE"][0] == EXISTING_POLICY

    def test_guid_assignments_uses_temp_guid(self):
        resp = create_mock_response(EXISTING_POLICY, "-2")
        body = resp.json()
        assert body["guidAssignments"]["-2"] == EXISTING_GUID

    def test_default_temp_guid_is_minus_one(self):
        resp = create_mock_response(EXISTING_POLICY)
        body = resp.json()
        assert "-1" in body["guidAssignments"]

    def test_request_url_uses_bulk_update_path(self):
        resp = create_mock_response(EXISTING_POLICY, TEMP_GUID)
        assert BULK_UPDATE.path in str(resp.request.url)


# ---------------------------------------------------------------------------
# find_existing_policy (sync)
# ---------------------------------------------------------------------------


class TestFindExistingPolicy:
    def _make_client(self, persona_response, policy_response):
        """Mock client with two API calls: persona lookup + policy search."""
        client = MagicMock()
        client._call_api.side_effect = [persona_response, policy_response]
        return client

    def test_returns_policy_when_found(self):
        # First call: persona lookup, Second call: policy search
        client = self._make_client(
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            {"entities": [EXISTING_POLICY]},
        )
        result = find_existing_policy(client, POLICY_NAME, PERSONA_GUID)
        assert result == EXISTING_POLICY

    def test_returns_none_when_no_entities(self):
        # First call: persona lookup, Second call: empty entities
        client = self._make_client(
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            {"entities": []},
        )
        result = find_existing_policy(client, POLICY_NAME, PERSONA_GUID)
        assert result is None

    def test_returns_none_when_raw_json_is_none(self):
        # First call: persona lookup, Second call: None
        client = self._make_client(
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            None,
        )
        result = find_existing_policy(client, POLICY_NAME, PERSONA_GUID)
        assert result is None

    def test_raises_error_code_on_exception(self):
        client = MagicMock()
        # First call: persona lookup succeeds, Second call: policy search fails
        client._call_api.side_effect = [
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            Exception("search failed"),
        ]
        with pytest.raises(Exception) as exc_info:
            find_existing_policy(client, POLICY_NAME, PERSONA_GUID)
        assert "ATLAN-PYTHON-500-007" in str(exc_info.value)


# ---------------------------------------------------------------------------
# find_existing_policy_async
# ---------------------------------------------------------------------------


class TestFindExistingPolicyAsync:
    @pytest.mark.asyncio
    async def test_returns_policy_when_found(self):
        client = MagicMock()
        # First call: persona lookup, Second call: policy search
        client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                {"entities": [EXISTING_POLICY]},
            ]
        )
        result = await find_existing_policy_async(client, POLICY_NAME, PERSONA_GUID)
        assert result == EXISTING_POLICY

    @pytest.mark.asyncio
    async def test_returns_none_when_no_entities(self):
        client = MagicMock()
        # First call: persona lookup, Second call: empty entities
        client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                {"entities": []},
            ]
        )
        result = await find_existing_policy_async(client, POLICY_NAME, PERSONA_GUID)
        assert result is None

    @pytest.mark.asyncio
    async def test_raises_error_code_on_exception(self):
        client = MagicMock()
        # First call: persona lookup succeeds, Second call: policy search fails
        client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                Exception("async search failed"),
            ]
        )
        with pytest.raises(Exception) as exc_info:
            await find_existing_policy_async(client, POLICY_NAME, PERSONA_GUID)
        assert "ATLAN-PYTHON-500-007" in str(exc_info.value)


# ---------------------------------------------------------------------------
# check_for_duplicate_policy (sync)
# ---------------------------------------------------------------------------


class TestCheckForDuplicatePolicy:
    def _make_client(self, existing=None):
        """Mock client with two API calls: persona lookup + policy search."""
        client = MagicMock()
        # First call: persona lookup, Second call: policy search
        client._call_api.side_effect = [
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            {"entities": [existing]} if existing else {"entities": []},
        ]
        return client

    def test_returns_none_for_non_bulk_request(self):
        client = self._make_client()
        req = httpx.Request("GET", "https://example.com/other")
        assert check_for_duplicate_policy(client, req) is None

    def test_returns_none_when_no_duplicate_found(self):
        client = self._make_client()
        req = _make_bulk_request()
        assert check_for_duplicate_policy(client, req) is None

    def test_returns_mock_response_when_duplicate_found(self):
        client = self._make_client(existing=EXISTING_POLICY)
        req = _make_bulk_request()
        resp = check_for_duplicate_policy(client, req)
        assert resp is not None
        assert resp.status_code == 200
        body = resp.json()
        assert body["guidAssignments"][TEMP_GUID] == EXISTING_GUID

    def test_returns_none_on_search_error(self):
        """Search failures must not propagate — degrade gracefully so the save can proceed."""
        client = MagicMock()
        client._call_api.side_effect = Exception("search failed")
        req = _make_bulk_request()
        assert check_for_duplicate_policy(client, req) is None


# ---------------------------------------------------------------------------
# check_for_duplicate_policy_async
# ---------------------------------------------------------------------------


class TestCheckForDuplicatePolicyAsync:
    @pytest.mark.asyncio
    async def test_returns_none_for_non_bulk_request(self):
        client = MagicMock()
        req = httpx.Request("GET", "https://example.com/other")
        assert await check_for_duplicate_policy_async(client, req) is None

    @pytest.mark.asyncio
    async def test_returns_none_when_no_duplicate_found(self):
        client = MagicMock()
        # First call: persona lookup, Second call: empty policy search
        client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                {"entities": []},
            ]
        )
        req = _make_bulk_request()
        assert await check_for_duplicate_policy_async(client, req) is None

    @pytest.mark.asyncio
    async def test_returns_mock_response_when_duplicate_found(self):
        client = MagicMock()
        # First call: persona lookup, Second call: existing policy found
        client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                {"entities": [EXISTING_POLICY]},
            ]
        )
        req = _make_bulk_request()
        resp = await check_for_duplicate_policy_async(client, req)
        assert resp is not None
        assert resp.status_code == 200
        assert resp.json()["guidAssignments"][TEMP_GUID] == EXISTING_GUID

    @pytest.mark.asyncio
    async def test_returns_none_on_search_error(self):
        """Search failures must not propagate — degrade gracefully so the save can proceed."""
        client = MagicMock()
        # First call: persona lookup succeeds, Second call: search fails
        client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                Exception("async search failed"),
            ]
        )
        req = _make_bulk_request()
        assert await check_for_duplicate_policy_async(client, req) is None


# ---------------------------------------------------------------------------
# PyatlanSyncTransport retry + duplicate prevention
# ---------------------------------------------------------------------------


class TestPyatlanSyncTransportRetry:
    def _make_transport(self, client=None):
        transport = PyatlanSyncTransport(
            retry=Retry(total=3, backoff_factor=0, allowed_methods=["POST"]),
            client=client,
            trust_env=False,
        )
        return transport

    def test_no_retry_on_success(self):
        transport = self._make_transport()
        mock_inner = MagicMock(return_value=httpx.Response(200))
        transport._transport.handle_request = mock_inner
        req = httpx.Request("POST", "https://example.com")
        resp = transport.handle_request(req)
        assert resp.status_code == 200
        assert mock_inner.call_count == 1

    def test_retries_on_timeout(self):
        transport = self._make_transport()
        call_count = 0

        def side_effect(req):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise httpx.ReadTimeout("timeout", request=req)
            return httpx.Response(200)

        transport._transport.handle_request = side_effect
        req = httpx.Request("POST", "https://example.com")
        resp = transport.handle_request(req)
        assert resp.status_code == 200
        assert call_count == 2

    def test_duplicate_prevention_short_circuits_on_first_attempt(self):
        """When a duplicate exists the inner transport is never called at all."""
        mock_client = MagicMock()
        # First call: persona lookup, Second call: existing policy found
        mock_client._call_api.side_effect = [
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            {"entities": [EXISTING_POLICY]},
        ]
        transport = self._make_transport(client=mock_client)
        inner_mock = MagicMock(return_value=httpx.Response(200))
        transport._transport.handle_request = inner_mock
        req = _make_bulk_request()
        resp = transport.handle_request(req)

        inner_mock.assert_not_called()
        assert resp.status_code == 200
        assert resp.json()["guidAssignments"][TEMP_GUID] == EXISTING_GUID

    def test_retry_proceeds_when_no_duplicate(self):
        """If no duplicate found, transport retries normally."""
        mock_client = MagicMock()
        # Mock multiple calls for duplicate checks before each attempt
        # First attempt: persona + policy (no duplicate)
        # Second attempt: persona + policy (no duplicate)
        mock_client._call_api.side_effect = [
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            {"entities": []},
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            {"entities": []},
        ]
        transport = self._make_transport(client=mock_client)

        call_count = 0

        def side_effect(req):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise httpx.ReadTimeout("timeout", request=req)
            return httpx.Response(200)

        transport._transport.handle_request = side_effect
        req = _make_bulk_request()
        resp = transport.handle_request(req)

        assert call_count == 2
        assert resp.status_code == 200

    def test_duplicate_check_runs_on_first_attempt(self):
        """Duplicate check must run before the first attempt to catch automation re-runs."""
        mock_client = MagicMock()
        # First call: persona lookup, Second call: policy search
        mock_client._call_api.side_effect = [
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            {"entities": []},
        ]
        transport = self._make_transport(client=mock_client)
        transport._transport.handle_request = MagicMock(
            return_value=httpx.Response(200)
        )
        req = _make_bulk_request()
        transport.handle_request(req)
        # Should be called twice: persona lookup + policy search
        assert mock_client._call_api.call_count == 2

    def test_automation_rerun_prevented_on_first_attempt(self):
        """Automation runs the same policy creation twice; second run must not create a duplicate."""
        mock_client = MagicMock()
        # First call: persona lookup, Second call: existing policy found
        mock_client._call_api.side_effect = [
            {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
            {"entities": [EXISTING_POLICY]},
        ]
        transport = self._make_transport(client=mock_client)
        inner_mock = MagicMock(return_value=httpx.Response(200))
        transport._transport.handle_request = inner_mock
        req = _make_bulk_request()
        resp = transport.handle_request(req)

        # Inner transport never called — existing policy returned immediately
        inner_mock.assert_not_called()
        assert resp.status_code == 200
        assert resp.json()["guidAssignments"][TEMP_GUID] == EXISTING_GUID


# ---------------------------------------------------------------------------
# PyatlanAsyncTransport retry + duplicate prevention
# ---------------------------------------------------------------------------


class TestPyatlanAsyncTransportRetry:
    def _make_transport(self, client=None):
        transport = PyatlanAsyncTransport(
            retry=Retry(total=3, backoff_factor=0, allowed_methods=["POST"]),
            client=client,
            trust_env=False,
        )
        return transport

    @pytest.mark.asyncio
    async def test_duplicate_prevention_short_circuits_on_first_attempt(self):
        """When a duplicate exists the inner transport is never called at all."""
        mock_client = MagicMock()
        # First call: persona lookup, Second call: existing policy found
        mock_client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                {"entities": [EXISTING_POLICY]},
            ]
        )
        transport = self._make_transport(client=mock_client)
        inner_mock = AsyncMock(return_value=httpx.Response(200))
        transport._transport.handle_async_request = inner_mock
        req = _make_bulk_request()
        resp = await transport.handle_async_request(req)

        inner_mock.assert_not_called()
        assert resp.status_code == 200
        assert resp.json()["guidAssignments"][TEMP_GUID] == EXISTING_GUID

    @pytest.mark.asyncio
    async def test_duplicate_check_runs_on_first_attempt(self):
        """Duplicate check must run before the first attempt to catch automation re-runs."""
        mock_client = MagicMock()
        # First call: persona lookup, Second call: policy search
        mock_client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                {"entities": []},
            ]
        )
        transport = self._make_transport(client=mock_client)
        transport._transport.handle_async_request = AsyncMock(
            return_value=httpx.Response(200)
        )
        req = _make_bulk_request()
        await transport.handle_async_request(req)
        # Should be called twice: persona lookup + policy search
        assert mock_client._call_api.call_count == 2

    @pytest.mark.asyncio
    async def test_automation_rerun_prevented_on_first_attempt(self):
        """Automation runs the same policy creation twice; second run must not create a duplicate."""
        mock_client = MagicMock()
        # First call: persona lookup, Second call: existing policy found
        mock_client._call_api = AsyncMock(
            side_effect=[
                {"entities": [{"attributes": {"qualifiedName": "default/persona"}}]},
                {"entities": [EXISTING_POLICY]},
            ]
        )
        transport = self._make_transport(client=mock_client)
        inner_mock = AsyncMock(return_value=httpx.Response(200))
        transport._transport.handle_async_request = inner_mock
        req = _make_bulk_request()
        resp = await transport.handle_async_request(req)

        # Inner transport never called — existing policy returned immediately
        inner_mock.assert_not_called()
        assert resp.status_code == 200
        assert resp.json()["guidAssignments"][TEMP_GUID] == EXISTING_GUID
