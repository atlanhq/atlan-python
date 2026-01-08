# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Integration tests for OAuth client CRUD operations."""

import time
from typing import Generator, Optional

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import NotFoundError
from pyatlan.model.oauth_client import OAuthClientCreateResponse, OAuthClientResponse
from tests.integration.client import TestId

MODULE_NAME = TestId.make_unique("OAuthClient")

# Test data
OAUTH_CLIENT_NAME = f"{MODULE_NAME}_test_client"
OAUTH_CLIENT_DESCRIPTION = "Integration test OAuth client"
OAUTH_CLIENT_DESCRIPTION_UPDATED = "Updated integration test OAuth client"
OAUTH_CLIENT_ROLE = "Admin"  # Role description
DATA_ASSETS_PERSONA_NAME = "Data Assets"  # Pre-existing persona


def delete_oauth_client(client: AtlanClient, client_id: str) -> None:
    """Helper to delete an OAuth client."""
    client.oauth_client.purge(client_id)


@pytest.fixture(scope="module")
def persona_qualified_name(client: AtlanClient) -> str:
    """
    Fixture to retrieve the qualified name of the pre-existing 'Data Assets' persona.
    """
    personas = client.asset.find_personas_by_name(DATA_ASSETS_PERSONA_NAME)
    assert len(personas) >= 1, f"Persona '{DATA_ASSETS_PERSONA_NAME}' not found"
    persona_qn = personas[0].qualified_name
    assert persona_qn is not None
    return persona_qn


@pytest.fixture(scope="module")
def oauth_client_response(
    client: AtlanClient,
    persona_qualified_name: str,
) -> Generator[OAuthClientCreateResponse, None, None]:
    """
    Fixture to create an OAuth client for testing with persona association.
    Yields the create response (which includes client_secret).
    Cleans up by deleting the OAuth client after tests.
    """
    # Create OAuth client with persona
    response = client.oauth_client.create(
        name=OAUTH_CLIENT_NAME,
        role=OAUTH_CLIENT_ROLE,
        description=OAUTH_CLIENT_DESCRIPTION,
        persona_qualified_names=[persona_qualified_name],
    )
    assert response is not None
    assert response.client_id is not None
    assert response.client_secret is not None

    yield response

    # Cleanup
    if response.client_id:
        delete_oauth_client(client, response.client_id)


def _assert_oauth_client_create_response(response: OAuthClientCreateResponse):
    """Assert the OAuth client create response has expected values."""
    assert response is not None
    assert response.id is not None
    assert response.client_id is not None
    assert response.client_id.startswith("oauth-client-")
    assert response.client_secret is not None
    assert response.display_name == OAUTH_CLIENT_NAME
    assert response.description == OAUTH_CLIENT_DESCRIPTION
    assert response.created_by is not None
    assert response.created_at is not None
    assert response.token_expiry_seconds is not None


def _assert_oauth_client(
    oauth_client: OAuthClientResponse,
    persona_qn: Optional[str] = None,
    is_updated: bool = False,
):
    """Assert the OAuth client has expected values."""
    assert oauth_client is not None
    assert oauth_client.id is not None
    assert oauth_client.client_id is not None
    assert oauth_client.client_id.startswith("oauth-client-")
    assert oauth_client.display_name == OAUTH_CLIENT_NAME
    if is_updated:
        assert oauth_client.description == OAUTH_CLIENT_DESCRIPTION_UPDATED
    else:
        assert oauth_client.description == OAUTH_CLIENT_DESCRIPTION
    # Validate persona association if provided
    if persona_qn:
        assert oauth_client.persona_qualified_names is not None
        assert persona_qn in oauth_client.persona_qualified_names


def test_oauth_client_create(
    client: AtlanClient,
    oauth_client_response: OAuthClientCreateResponse,
):
    """Test creating an OAuth client."""
    _assert_oauth_client_create_response(oauth_client_response)


@pytest.mark.order(after="test_oauth_client_create")
def test_oauth_client_get_by_id(
    client: AtlanClient,
    oauth_client_response: OAuthClientCreateResponse,
    persona_qualified_name: str,
):
    """Test retrieving an OAuth client by ID and validate persona association."""
    assert oauth_client_response.client_id is not None
    time.sleep(2)  # Allow time for eventual consistency

    oauth_client = client.oauth_client.get_by_id(oauth_client_response.client_id)
    _assert_oauth_client(oauth_client, persona_qn=persona_qualified_name)


@pytest.mark.order(after="test_oauth_client_get_by_id")
def test_oauth_client_get_all(
    client: AtlanClient,
    oauth_client_response: OAuthClientCreateResponse,
    persona_qualified_name: str,
):
    """Test retrieving all OAuth clients and validate persona association."""
    assert oauth_client_response.client_id is not None
    time.sleep(2)

    response = client.oauth_client.get_all()
    assert response is not None
    assert response.records is not None
    assert len(response.records) >= 1

    # Find our test client and validate persona
    found = False
    for oauth_client in response.records:
        if oauth_client.client_id == oauth_client_response.client_id:
            found = True
            _assert_oauth_client(oauth_client, persona_qn=persona_qualified_name)
            break
    assert found, f"OAuth client {oauth_client_response.client_id} not found"


@pytest.mark.order(after="test_oauth_client_get_all")
def test_oauth_client_get_with_pagination(
    client: AtlanClient,
    oauth_client_response: OAuthClientCreateResponse,
):
    """Test retrieving OAuth clients with pagination."""
    assert oauth_client_response.client_id is not None

    response = client.oauth_client.get(limit=10, offset=0, sort="createdAt")
    assert response is not None
    assert response.total_record is not None
    assert response.total_record >= 1


@pytest.mark.order(after="test_oauth_client_get_with_pagination")
def test_oauth_client_update_description(
    client: AtlanClient,
    oauth_client_response: OAuthClientCreateResponse,
    persona_qualified_name: str,
):
    """Test updating an OAuth client's description."""
    assert oauth_client_response.client_id is not None
    time.sleep(2)

    updated = client.oauth_client.update(
        client_id=oauth_client_response.client_id,
        description=OAUTH_CLIENT_DESCRIPTION_UPDATED,
    )
    _assert_oauth_client(updated, persona_qn=persona_qualified_name, is_updated=True)


@pytest.mark.order(after="test_oauth_client_update_description")
def test_oauth_client_verify_update_persisted(
    client: AtlanClient,
    oauth_client_response: OAuthClientCreateResponse,
    persona_qualified_name: str,
):
    """Verify that the update was persisted and persona association is maintained."""
    assert oauth_client_response.client_id is not None
    time.sleep(2)

    oauth_client = client.oauth_client.get_by_id(oauth_client_response.client_id)
    _assert_oauth_client(
        oauth_client, persona_qn=persona_qualified_name, is_updated=True
    )


def test_oauth_client_create_with_invalid_role_raises_error(
    client: AtlanClient,
):
    """Test that creating an OAuth client with an invalid role raises an error."""

    with pytest.raises(NotFoundError) as exc_info:
        client.oauth_client.create(
            name="test-invalid-role",
            role="InvalidRole",
        )
    assert "does not exist" in str(exc_info.value)
    assert "Available roles:" in str(exc_info.value)
