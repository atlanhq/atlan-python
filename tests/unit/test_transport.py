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
    def _make_client(self, raw_json):
        client = MagicMock()
        client._call_api.return_value = raw_json
        return client

    def test_returns_policy_when_found(self):
        client = self._make_client({"entities": [EXISTING_POLICY]})
        result = find_existing_policy(client, POLICY_NAME, PERSONA_GUID)
        assert result == EXISTING_POLICY

    def test_returns_none_when_no_entities(self):
        client = self._make_client({"entities": []})
        result = find_existing_policy(client, POLICY_NAME, PERSONA_GUID)
        assert result is None

    def test_returns_none_when_raw_json_is_none(self):
        client = self._make_client(None)
        result = find_existing_policy(client, POLICY_NAME, PERSONA_GUID)
        assert result is None

    def test_returns_none_on_exception(self):
        client = MagicMock()
        client._call_api.side_effect = Exception("search failed")
        result = find_existing_policy(client, POLICY_NAME, PERSONA_GUID)
        assert result is None


# ---------------------------------------------------------------------------
# find_existing_policy_async
# ---------------------------------------------------------------------------


class TestFindExistingPolicyAsync:
    @pytest.mark.asyncio
    async def test_returns_policy_when_found(self):
        client = MagicMock()
        client._call_api = AsyncMock(return_value={"entities": [EXISTING_POLICY]})
        result = await find_existing_policy_async(client, POLICY_NAME, PERSONA_GUID)
        assert result == EXISTING_POLICY

    @pytest.mark.asyncio
    async def test_returns_none_when_no_entities(self):
        client = MagicMock()
        client._call_api = AsyncMock(return_value={"entities": []})
        result = await find_existing_policy_async(client, POLICY_NAME, PERSONA_GUID)
        assert result is None

    @pytest.mark.asyncio
    async def test_returns_none_on_exception(self):
        client = MagicMock()
        client._call_api = AsyncMock(side_effect=Exception("async search failed"))
        result = await find_existing_policy_async(client, POLICY_NAME, PERSONA_GUID)
        assert result is None


# ---------------------------------------------------------------------------
# check_for_duplicate_policy (sync)
# ---------------------------------------------------------------------------


class TestCheckForDuplicatePolicy:
    def _make_client(self, existing=None):
        client = MagicMock()
        client._call_api.return_value = (
            {"entities": [existing]} if existing else {"entities": []}
        )
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
        client._call_api = AsyncMock(return_value={"entities": []})
        req = _make_bulk_request()
        assert await check_for_duplicate_policy_async(client, req) is None

    @pytest.mark.asyncio
    async def test_returns_mock_response_when_duplicate_found(self):
        client = MagicMock()
        client._call_api = AsyncMock(return_value={"entities": [EXISTING_POLICY]})
        req = _make_bulk_request()
        resp = await check_for_duplicate_policy_async(client, req)
        assert resp is not None
        assert resp.status_code == 200
        assert resp.json()["guidAssignments"][TEMP_GUID] == EXISTING_GUID

    @pytest.mark.asyncio
    async def test_returns_none_on_search_error(self):
        client = MagicMock()
        client._call_api = AsyncMock(side_effect=Exception("async search failed"))
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

    def test_duplicate_prevention_short_circuits_retry(self):
        """On retry, duplicate check returns mock response — inner transport not called again."""
        mock_client = MagicMock()
        mock_client._call_api.return_value = {"entities": [EXISTING_POLICY]}
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

        # Inner transport called only once (timeout) — retry short-circuited
        assert call_count == 1
        assert resp.status_code == 200
        assert resp.json()["guidAssignments"][TEMP_GUID] == EXISTING_GUID

    def test_retry_proceeds_when_no_duplicate(self):
        """If no duplicate found, transport retries normally."""
        mock_client = MagicMock()
        mock_client._call_api.return_value = {"entities": []}
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

    def test_no_duplicate_check_on_first_attempt(self):
        """Duplicate check must NOT run on the first attempt."""
        mock_client = MagicMock()
        transport = self._make_transport(client=mock_client)
        transport._transport.handle_request = MagicMock(
            return_value=httpx.Response(200)
        )
        req = _make_bulk_request()
        transport.handle_request(req)
        mock_client._call_api.assert_not_called()


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
    async def test_duplicate_prevention_short_circuits_retry(self):
        mock_client = MagicMock()
        mock_client._call_api = AsyncMock(return_value={"entities": [EXISTING_POLICY]})
        transport = self._make_transport(client=mock_client)

        call_count = 0

        async def side_effect(req):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise httpx.ReadTimeout("timeout", request=req)
            return httpx.Response(200)

        transport._transport.handle_async_request = side_effect
        req = _make_bulk_request()
        resp = await transport.handle_async_request(req)

        assert call_count == 1
        assert resp.status_code == 200
        assert resp.json()["guidAssignments"][TEMP_GUID] == EXISTING_GUID

    @pytest.mark.asyncio
    async def test_no_duplicate_check_on_first_attempt(self):
        mock_client = MagicMock()
        mock_client._call_api = AsyncMock()
        transport = self._make_transport(client=mock_client)
        transport._transport.handle_async_request = AsyncMock(
            return_value=httpx.Response(200)
        )
        req = _make_bulk_request()
        await transport.handle_async_request(req)
        mock_client._call_api.assert_not_called()
