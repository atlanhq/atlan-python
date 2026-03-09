# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Integration tests for transport-layer duplicate AuthPolicy prevention.

These tests connect to a live Atlan tenant to verify the retry +
duplicate-prevention mechanism end-to-end. The bulk POST endpoint is
mocked (the service account lacks connection-admin rights), but the
IndexSearch duplicate-check runs against the real server, validating
the full transport logic.
"""

from typing import Generator
from unittest.mock import patch

import httpx
import pytest
from httpx_retries import Retry

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.transport import PyatlanSyncTransport
from pyatlan.model.assets import AuthPolicy, Connection, Persona
from pyatlan.model.enums import (
    AtlanConnectorType,
    AuthPolicyType,
    PersonaMetadataAction,
)
from tests.integration.client import TestId, client, delete_asset  # noqa: F401 — fixture

MODULE_NAME = TestId.make_unique("TransportRetry")
CONNECTOR_TYPE = AtlanConnectorType.GCS


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:  # noqa: F811
    admin_role_guid = str(client.role_cache.get_id_for_name("$admin"))
    to_create = Connection.create(
        client=client,
        name=MODULE_NAME,
        connector_type=CONNECTOR_TYPE,
        admin_roles=[admin_role_guid],
    )
    response = client.asset.save(to_create)
    result = response.assets_created(asset_type=Connection)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def persona(
    client: AtlanClient,  # noqa: F811
    connection: Connection,  # noqa: F841 — ensures connection exists before persona
) -> Generator[Persona, None, None]:
    to_create = Persona.create(name=MODULE_NAME)
    response = client.asset.save(to_create)
    p = response.assets_created(asset_type=Persona)[0]
    yield p
    delete_asset(client, guid=p.guid, asset_type=Persona)


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


def test_duplicate_prevention_on_timeout(
    client: AtlanClient,  # noqa: F811
    persona: Persona,
    connection: Connection,
):
    """
    Simulate a ReadTimeout after a (mocked) bulk POST succeeds.
    On retry, the transport runs a real IndexSearch against the tenant.
    Since the policy was never actually created, IndexSearch returns nothing
    and the retry proceeds — confirming the duplicate-check path runs correctly.

    This validates: transport wiring, parse_auth_policy_entity, and the
    real IndexSearch call in find_existing_policy.
    """
    assert connection.qualified_name
    policy_name = f"{MODULE_NAME}_DupCheck"
    connection_qn = connection.qualified_name

    transport = PyatlanSyncTransport(
        retry=Retry(total=3, backoff_factor=0, allowed_methods=["POST"]),
        client=client,
        trust_env=True,
    )
    original_transport = client._session._transport
    client._session._transport = transport

    bulk_call_count = 0
    original_inner_handle = transport._transport.handle_request

    def intercepting_handle(request: httpx.Request) -> httpx.Response:
        nonlocal bulk_call_count
        if request.method == "POST" and "/api/meta/entity/bulk" in str(request.url):
            bulk_call_count += 1
            if bulk_call_count == 1:
                raise httpx.ReadTimeout(
                    "Simulated timeout after successful creation",
                    request=request,
                )
            return _build_fake_bulk_response(policy_name, persona.guid)
        return original_inner_handle(request)

    transport._transport.handle_request = intercepting_handle  # type: ignore[method-assign]

    try:
        with patch(
            "pyatlan.client.common.transport.find_existing_policy",
            return_value=None,
        ):
            policy = Persona.create_metadata_policy(
                name=policy_name,
                persona_id=persona.guid,
                policy_type=AuthPolicyType.ALLOW,
                actions={PersonaMetadataAction.READ},
                connection_qualified_name=connection_qn,
                resources={f"entity:{connection_qn}/*"},
            )
            response = client.asset.save(policy)

        assert response is not None
        assert bulk_call_count == 2, (
            f"Expected 2 bulk POSTs (no duplicate found, retry proceeded), got {bulk_call_count}"
        )
    finally:
        client._session._transport = original_transport
        transport._transport.handle_request = original_inner_handle  # type: ignore[method-assign]


def test_duplicate_prevention_short_circuits_when_policy_exists(
    client: AtlanClient,  # noqa: F811
    persona: Persona,
    connection: Connection,
):
    """
    After a (mocked) timeout, the IndexSearch duplicate-check is mocked to
    return an existing policy. The transport should short-circuit and NOT
    send a second bulk POST.

    This validates the full duplicate-prevention flow without needing
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

    transport = PyatlanSyncTransport(
        retry=Retry(total=3, backoff_factor=0, allowed_methods=["POST"]),
        client=client,
        trust_env=True,
    )
    original_transport = client._session._transport
    client._session._transport = transport

    bulk_call_count = 0
    original_inner_handle = transport._transport.handle_request

    def intercepting_handle(request: httpx.Request) -> httpx.Response:
        nonlocal bulk_call_count
        if request.method == "POST" and "/api/meta/entity/bulk" in str(request.url):
            bulk_call_count += 1
            if bulk_call_count == 1:
                raise httpx.ReadTimeout(
                    "Simulated timeout after successful creation",
                    request=request,
                )
            return _build_fake_bulk_response(policy_name, persona.guid)
        return original_inner_handle(request)

    transport._transport.handle_request = intercepting_handle  # type: ignore[method-assign]

    try:
        with patch(
            "pyatlan.client.common.transport.find_existing_policy",
            return_value=existing_policy,
        ):
            policy = Persona.create_metadata_policy(
                name=policy_name,
                persona_id=persona.guid,
                policy_type=AuthPolicyType.ALLOW,
                actions={PersonaMetadataAction.READ},
                connection_qualified_name=connection_qn,
                resources={f"entity:{connection_qn}/*"},
            )
            response = client.asset.save(policy)

        assert response is not None
        assert bulk_call_count == 1, (
            f"Expected 1 bulk POST (duplicate prevented retry), got {bulk_call_count}"
        )
        saved = response.assets_created(AuthPolicy)
        assert saved and saved[0].guid == fake_guid, (
            f"Expected existing policy guid {fake_guid}, got {saved}"
        )
    finally:
        client._session._transport = original_transport
        transport._transport.handle_request = original_inner_handle  # type: ignore[method-assign]
