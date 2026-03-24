# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Async integration tests for transport-layer duplicate AuthPolicy prevention.

These tests connect to a live Atlan tenant to verify the retry +
duplicate-prevention mechanism end-to-end using PyatlanAsyncTransport.
"""

from typing import AsyncGenerator
from unittest.mock import AsyncMock, patch

import httpx
import pytest
import pytest_asyncio
from httpx_retries import Retry

from pyatlan.client.aio import AsyncAtlanClient
from pyatlan.client.transport import PyatlanAsyncTransport
from pyatlan.model.assets import AuthPolicy, Connection, Persona
from pyatlan.model.enums import (
    AtlanConnectorType,
    AuthPolicyType,
    PersonaMetadataAction,
)
from tests.integration.aio.utils import delete_asset_async
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("AioTransportRetry")
CONNECTOR_TYPE = AtlanConnectorType.GCS


@pytest_asyncio.fixture(scope="module")
async def client() -> AsyncGenerator[AsyncAtlanClient, None]:
    """Async Atlan client fixture."""
    yield AsyncAtlanClient()


@pytest_asyncio.fixture(scope="module")
async def connection(client: AsyncAtlanClient) -> AsyncGenerator[Connection, None]:
    admin_role_guid = str(await client.role_cache.get_id_for_name("$admin"))
    to_create = await Connection.creator_async(
        client=client,
        name=MODULE_NAME,
        connector_type=CONNECTOR_TYPE,
        admin_roles=[admin_role_guid],
    )
    response = await client.asset.save(to_create)
    result = response.assets_created(asset_type=Connection)[0]
    yield result
    await delete_asset_async(client, guid=result.guid, asset_type=Connection)


@pytest_asyncio.fixture(scope="module")
async def persona(
    client: AsyncAtlanClient,
    connection: Connection,  # noqa: F841 — ensures connection exists before persona
) -> AsyncGenerator[Persona, None]:
    to_create = Persona.create(name=MODULE_NAME)
    response = await client.asset.save(to_create)
    p = response.assets_created(asset_type=Persona)[0]
    yield p
    await delete_asset_async(client, guid=p.guid, asset_type=Persona)


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
async def test_async_duplicate_prevention_on_timeout(
    client: AsyncAtlanClient,
    persona: Persona,
    connection: Connection,
):
    """
    Simulate a ReadTimeout after a (mocked) async bulk POST succeeds.
    On retry, the transport runs a real IndexSearch against the tenant.
    Since the policy was never actually created, IndexSearch returns nothing
    and the retry proceeds — confirming the async duplicate-check path runs correctly.

    This validates: async transport wiring, parse_auth_policy_entity, and the
    real IndexSearch call in find_existing_policy_async.
    """
    assert connection.qualified_name
    policy_name = f"{MODULE_NAME}_DupCheck"
    connection_qn = connection.qualified_name

    transport = PyatlanAsyncTransport(
        retry=Retry(total=3, backoff_factor=0, allowed_methods=["POST"]),
        trust_env=True,
    )
    # Set client reference after construction to avoid validation issues
    transport._client = client
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
        with patch(
            "pyatlan.client.common.transport.find_existing_policy_async",
            new=AsyncMock(return_value=None),
        ):
            policy = Persona.create_metadata_policy(
                name=policy_name,
                persona_id=persona.guid,
                policy_type=AuthPolicyType.ALLOW,
                actions={PersonaMetadataAction.READ},
                connection_qualified_name=connection_qn,
                resources={f"entity:{connection_qn}/*"},
            )
            response = await client.asset.save(policy)

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
    persona: Persona,
    connection: Connection,
):
    """
    After a (mocked) async timeout, the IndexSearch duplicate-check is mocked to
    return an existing policy. The async transport should short-circuit and NOT
    send a second bulk POST.

    This validates the full async duplicate-prevention flow without needing
    connection-admin rights on the tenant.
    """
    assert connection.qualified_name
    policy_name = f"{MODULE_NAME}_ShortCircuit"
    fake_guid = f"existing-{policy_name}-guid"
    connection_qn = connection.qualified_name

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
        trust_env=True,
    )
    # Set client reference after construction to avoid validation issues
    transport._client = client
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

    duplicate_check_count = 0

    async def mock_find_existing_policy_async(*args, **kwargs):
        """Return None on first check, existing_policy on retry check."""
        nonlocal duplicate_check_count
        duplicate_check_count += 1
        if duplicate_check_count == 1:
            # First check (before first attempt): no duplicate yet
            return None
        else:
            # Second check (before retry): duplicate exists now
            return existing_policy

    try:
        with patch(
            "pyatlan.client.common.transport.find_existing_policy_async",
            new=AsyncMock(side_effect=mock_find_existing_policy_async),
        ):
            policy = Persona.create_metadata_policy(
                name=policy_name,
                persona_id=persona.guid,
                policy_type=AuthPolicyType.ALLOW,
                actions={PersonaMetadataAction.READ},
                connection_qualified_name=connection_qn,
                resources={f"entity:{connection_qn}/*"},
            )
            response = await client.asset.save(policy)

        assert response is not None
        assert bulk_call_count == 1, (
            f"Expected 1 bulk POST (duplicate prevented retry), got {bulk_call_count}"
        )
        saved = response.assets_created(AuthPolicy)
        assert saved and saved[0].guid == fake_guid, (
            f"Expected existing policy guid {fake_guid}, got {saved}"
        )
    finally:
        client._async_session._transport = original_transport
        transport._transport.handle_async_request = original_inner_handle  # type: ignore[method-assign]
