# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Async integration tests for transport-layer duplicate AuthPolicy prevention.

These tests connect to a live Atlan tenant to verify the retry +
duplicate-prevention mechanism end-to-end using PyatlanAsyncTransport.
"""

from typing import AsyncGenerator
from unittest.mock import patch

import httpx
import pytest
import pytest_asyncio
from httpx_retries import Retry

from pyatlan.client.aio import AsyncAtlanClient
from pyatlan.client.transport import PyatlanAsyncTransport
from pyatlan.model.assets import AuthPolicy, Persona
from pyatlan.model.enums import AuthPolicyType, PersonaMetadataAction
from tests.integration.client import TestId

PERSONA_NAME = "New"
CONNECTION_QN = "default/redshift/1769838984"
MODULE_NAME = TestId.make_unique("AioTransportRetry")


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncAtlanClient, None]:
    """Async Atlan client fixture."""
    yield AsyncAtlanClient()


async def _find_persona(atlan_client: AsyncAtlanClient, name: str) -> Persona:
    results = await atlan_client.asset.find_personas_by_name(name)
    if not results:
        pytest.skip(f"Persona '{name}' not found on this tenant — skipping.")
    return results[0]


def _build_fake_bulk_response(policy_name: str, persona_guid: str) -> httpx.Response:
    """Return a fake 200 bulk POST response as if the policy was created."""
    fake_guid = f"fake-{policy_name}-guid"
    body = {
        "mutatedEntities": {
            "CREATE": [
                {
                    "typeName": "AuthPolicy",
                    "guid": fake_guid,
                    "attributes": {
                        "name": policy_name,
                        "accessControl": {"guid": persona_guid},
                    },
                }
            ]
        },
        "guidAssignments": {"-1": fake_guid},
    }
    return httpx.Response(200, json=body)


@pytest.mark.asyncio
async def test_async_duplicate_prevention_on_timeout(client: AsyncAtlanClient):
    """
    Simulate a ReadTimeout after a (mocked) async bulk POST succeeds.
    On retry, the transport runs a real IndexSearch against the tenant.
    Since the policy was never actually created, IndexSearch returns nothing
    and the retry proceeds — confirming the async duplicate-check path runs correctly.

    This validates: async transport wiring, parse_auth_policy_entity, and the
    real IndexSearch call in find_existing_policy_async.
    """
    persona = await _find_persona(client, PERSONA_NAME)
    policy_name = f"{MODULE_NAME}_DupCheck"

    transport = PyatlanAsyncTransport(
        retry=Retry(total=3, backoff_factor=0, allowed_methods=["POST"]),
        client=client,
        trust_env=True,
    )
    assert client._async_session is not None
    original_transport = client._async_session._transport
    client._async_session._transport = transport

    bulk_call_count = 0
    original_inner_handle = transport._transport.handle_async_request

    async def intercepting_handle(request: httpx.Request) -> httpx.Response:
        nonlocal bulk_call_count
        if request.method == "POST" and "/api/meta/entity/bulk" in str(request.url):
            bulk_call_count += 1
            if bulk_call_count == 1:
                raise httpx.ReadTimeout(
                    "Simulated timeout after successful creation",
                    request=request,
                )
            # Second attempt — return a real fake success
            return _build_fake_bulk_response(policy_name, persona.guid)
        return await original_inner_handle(request)

    transport._transport.handle_async_request = intercepting_handle  # type: ignore[method-assign]

    try:
        policy = Persona.create_metadata_policy(
            name=policy_name,
            persona_id=persona.guid,
            policy_type=AuthPolicyType.ALLOW,
            actions={PersonaMetadataAction.READ},
            connection_qualified_name=CONNECTION_QN,
            resources={f"entity:{CONNECTION_QN}/*"},
        )
        response = await client.asset.save(policy)

        # Policy wasn't really created so IndexSearch returns nothing →
        # retry proceeds to attempt #2 → fake success returned
        assert response is not None
        assert bulk_call_count == 2, (
            f"Expected 2 bulk POSTs (no duplicate found, retry proceeded), got {bulk_call_count}"
        )
    finally:
        client._async_session._transport = original_transport
        transport._transport.handle_async_request = original_inner_handle  # type: ignore[method-assign]


@pytest.mark.asyncio
async def test_async_duplicate_prevention_short_circuits_when_policy_exists(
    client: AsyncAtlanClient,
):
    """
    After a (mocked) async timeout, the IndexSearch duplicate-check is mocked to
    return an existing policy. The async transport should short-circuit and NOT
    send a second bulk POST.

    This validates the full async duplicate-prevention flow without needing
    connection-admin rights on the tenant.
    """
    persona = await _find_persona(client, PERSONA_NAME)
    policy_name = f"{MODULE_NAME}_ShortCircuit"
    fake_guid = f"existing-{policy_name}-guid"

    existing_policy = {
        "typeName": "AuthPolicy",
        "guid": fake_guid,
        "attributes": {
            "name": policy_name,
            "accessControl": {"guid": persona.guid},
        },
    }

    transport = PyatlanAsyncTransport(
        retry=Retry(total=3, backoff_factor=0, allowed_methods=["POST"]),
        client=client,
        trust_env=True,
    )
    assert client._async_session is not None
    original_transport = client._async_session._transport
    client._async_session._transport = transport

    bulk_call_count = 0
    original_inner_handle = transport._transport.handle_async_request

    async def intercepting_handle(request: httpx.Request) -> httpx.Response:
        nonlocal bulk_call_count
        if request.method == "POST" and "/api/meta/entity/bulk" in str(request.url):
            bulk_call_count += 1
            if bulk_call_count == 1:
                raise httpx.ReadTimeout(
                    "Simulated timeout after successful creation",
                    request=request,
                )
            return _build_fake_bulk_response(policy_name, persona.guid)
        return await original_inner_handle(request)

    transport._transport.handle_async_request = intercepting_handle  # type: ignore[method-assign]

    try:
        # Patch find_existing_policy_async so the duplicate check returns our
        # fake existing policy without a real search
        with patch(
            "pyatlan.client.common.transport.find_existing_policy_async",
            return_value=existing_policy,
        ):
            policy = Persona.create_metadata_policy(
                name=policy_name,
                persona_id=persona.guid,
                policy_type=AuthPolicyType.ALLOW,
                actions={PersonaMetadataAction.READ},
                connection_qualified_name=CONNECTION_QN,
                resources={f"entity:{CONNECTION_QN}/*"},
            )
            response = await client.asset.save(policy)

        assert response is not None
        # Duplicate found → retry short-circuited → only 1 bulk POST
        assert bulk_call_count == 1, (
            f"Expected 1 bulk POST (duplicate prevented retry), got {bulk_call_count}"
        )
        # Response should contain the existing policy's GUID
        saved = response.assets_created(AuthPolicy)
        assert saved and saved[0].guid == fake_guid, (
            f"Expected existing policy guid {fake_guid}, got {saved}"
        )
    finally:
        client._async_session._transport = original_transport
        transport._transport.handle_async_request = original_inner_handle  # type: ignore[method-assign]
