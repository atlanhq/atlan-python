# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from unittest.mock import Mock, patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.group import AtlanGroup, GroupResponse
from pyatlan.model.sso import SSOMapper, SSOMapperConfig
from pyatlan.samples.sso.diagnose_orphaned_group_mappings import (
    SSOGroupMappingDiagnostic,
)


@pytest.fixture
def mock_client():
    """Create a mock AtlanClient for testing."""
    return Mock(spec=AtlanClient)


@pytest.fixture
def diagnostic(mock_client):
    """Create a SSOGroupMappingDiagnostic instance."""
    return SSOGroupMappingDiagnostic(mock_client)


@pytest.fixture
def sample_groups():
    """Create sample Atlan groups for testing."""
    return {
        "group-id-1": AtlanGroup(
            id="group-id-1",
            name="test_group_1",
            alias="Test Group 1",
        ),
        "group-id-2": AtlanGroup(
            id="group-id-2",
            name="test_group_2",
            alias="Test Group 2",
        ),
    }


@pytest.fixture
def sample_mappings():
    """Create sample SSO mappings for testing."""
    return [
        # Valid mapping for group-id-1
        SSOMapper(
            id="mapping-1",
            name="group-id-1--1234567890",
            identity_provider_mapper="saml-group-idp-mapper",
            identity_provider_alias="okta",
            config=SSOMapperConfig(
                group_name="test_group_1",
                attribute_value="okta-group-1",
                sync_mode="FORCE",
                attribute_name="memberOf",
            ),
        ),
        # Valid mapping for group-id-2
        SSOMapper(
            id="mapping-2",
            name="group-id-2--1234567891",
            identity_provider_mapper="saml-group-idp-mapper",
            identity_provider_alias="okta",
            config=SSOMapperConfig(
                group_name="test_group_2",
                attribute_value="okta-group-2",
                sync_mode="FORCE",
                attribute_name="memberOf",
            ),
        ),
        # Orphaned mapping - group doesn't exist
        SSOMapper(
            id="mapping-3",
            name="group-id-999--1234567892",
            identity_provider_mapper="saml-group-idp-mapper",
            identity_provider_alias="okta",
            config=SSOMapperConfig(
                group_name="deleted_group",
                attribute_value="okta-group-3",
                sync_mode="FORCE",
                attribute_name="memberOf",
            ),
        ),
        # Orphaned mapping - group ID mismatch
        SSOMapper(
            id="mapping-4",
            name="group-id-old--1234567893",
            identity_provider_mapper="saml-group-idp-mapper",
            identity_provider_alias="okta",
            config=SSOMapperConfig(
                group_name="test_group_1",  # Points to existing group
                attribute_value="okta-group-4",
                sync_mode="FORCE",
                attribute_name="memberOf",
            ),
        ),
    ]


def test_get_all_groups(diagnostic, mock_client, sample_groups):
    """Test retrieving all Atlan groups."""
    # Setup mock
    mock_response = Mock(spec=GroupResponse)
    mock_response.__iter__ = Mock(return_value=iter(sample_groups.values()))
    mock_client.group.get_all.return_value = mock_response

    # Execute
    result = diagnostic.get_all_groups()

    # Verify
    assert len(result) == 2
    assert "group-id-1" in result
    assert "group-id-2" in result
    assert result["group-id-1"].name == "test_group_1"
    mock_client.group.get_all.assert_called_once()


def test_get_all_sso_mappings(diagnostic, mock_client, sample_mappings):
    """Test retrieving all SSO group mappings."""
    # Setup mock
    mock_client.sso.get_all_group_mappings.return_value = sample_mappings

    # Execute
    result = diagnostic.get_all_sso_mappings("okta")

    # Verify
    assert len(result) == 4
    assert result[0].id == "mapping-1"
    mock_client.sso.get_all_group_mappings.assert_called_once_with(sso_alias="okta")


def test_diagnose_finds_orphaned_mappings(
    diagnostic, mock_client, sample_groups, sample_mappings
):
    """Test that diagnose correctly identifies orphaned mappings."""
    # Setup mocks
    mock_group_response = Mock(spec=GroupResponse)
    mock_group_response.__iter__ = Mock(return_value=iter(sample_groups.values()))
    mock_client.group.get_all.return_value = mock_group_response
    mock_client.sso.get_all_group_mappings.return_value = sample_mappings

    # Execute
    results = diagnostic.diagnose_orphaned_mappings("okta")

    # Verify
    assert len(results["valid"]) == 2
    assert len(results["orphaned"]) == 2

    # Check valid mappings
    valid_ids = {m.id for m in results["valid"]}
    assert "mapping-1" in valid_ids
    assert "mapping-2" in valid_ids

    # Check orphaned mappings
    orphaned_ids = {m.id for m in results["orphaned"]}
    assert "mapping-3" in orphaned_ids  # Group doesn't exist
    assert "mapping-4" in orphaned_ids  # Group ID mismatch


def test_diagnose_with_target_group_filter(
    diagnostic, mock_client, sample_groups, sample_mappings
):
    """Test diagnosing a specific group."""
    # Setup mocks
    mock_group_response = Mock(spec=GroupResponse)
    mock_group_response.__iter__ = Mock(return_value=iter(sample_groups.values()))
    mock_client.group.get_all.return_value = mock_group_response
    mock_client.sso.get_all_group_mappings.return_value = sample_mappings

    # Execute - filter for test_group_1
    results = diagnostic.diagnose_orphaned_mappings(
        "okta", target_group_name="test_group_1"
    )

    # Verify - should only check mappings for test_group_1
    # mapping-1 is valid, mapping-4 is orphaned (both reference test_group_1)
    assert len(results["valid"]) == 1
    assert len(results["orphaned"]) == 1
    assert results["valid"][0].id == "mapping-1"
    assert results["orphaned"][0].id == "mapping-4"


def test_diagnose_handles_incomplete_mappings(diagnostic, mock_client, sample_groups):
    """Test handling of mappings with incomplete data."""
    # Create mapping with missing config
    incomplete_mapping = SSOMapper(
        id="mapping-incomplete",
        name=None,  # Missing name
        identity_provider_mapper="saml-group-idp-mapper",
        identity_provider_alias="okta",
        config=None,  # Missing config
    )

    # Setup mocks
    mock_group_response = Mock(spec=GroupResponse)
    mock_group_response.__iter__ = Mock(return_value=iter(sample_groups.values()))
    mock_client.group.get_all.return_value = mock_group_response
    mock_client.sso.get_all_group_mappings.return_value = [incomplete_mapping]

    # Execute
    results = diagnostic.diagnose_orphaned_mappings("okta")

    # Verify - incomplete mapping should be in suspicious list
    assert len(results["suspicious"]) == 1
    assert results["suspicious"][0].id == "mapping-incomplete"


def test_cleanup_orphaned_mappings_interactive(
    diagnostic, mock_client, sample_groups, sample_mappings
):
    """Test interactive cleanup of orphaned mappings."""
    # Setup mocks
    mock_group_response = Mock(spec=GroupResponse)
    mock_group_response.__iter__ = Mock(return_value=iter(sample_groups.values()))
    mock_client.group.get_all.return_value = mock_group_response
    mock_client.sso.get_all_group_mappings.return_value = sample_mappings
    mock_client.sso.delete_group_mapping.return_value = None

    # Mock user input - say yes to first, no to second
    with patch("builtins.input", side_effect=["y", "n"]):
        # Execute
        deleted_count = diagnostic.cleanup_orphaned_mappings("okta", interactive=True)

    # Verify - should delete only the first orphaned mapping
    assert deleted_count == 1
    mock_client.sso.delete_group_mapping.assert_called_once()


def test_cleanup_orphaned_mappings_non_interactive(
    diagnostic, mock_client, sample_groups, sample_mappings
):
    """Test non-interactive cleanup of all orphaned mappings."""
    # Setup mocks
    mock_group_response = Mock(spec=GroupResponse)
    mock_group_response.__iter__ = Mock(return_value=iter(sample_groups.values()))
    mock_client.group.get_all.return_value = mock_group_response
    mock_client.sso.get_all_group_mappings.return_value = sample_mappings
    mock_client.sso.delete_group_mapping.return_value = None

    # Execute
    deleted_count = diagnostic.cleanup_orphaned_mappings("okta", interactive=False)

    # Verify - should delete both orphaned mappings
    assert deleted_count == 2
    assert mock_client.sso.delete_group_mapping.call_count == 2


def test_cleanup_no_orphaned_mappings(diagnostic, mock_client, sample_groups):
    """Test cleanup when there are no orphaned mappings."""
    # Create only valid mappings
    valid_mapping = SSOMapper(
        id="mapping-1",
        name="group-id-1--1234567890",
        identity_provider_mapper="saml-group-idp-mapper",
        identity_provider_alias="okta",
        config=SSOMapperConfig(
            group_name="test_group_1",
            attribute_value="okta-group-1",
            sync_mode="FORCE",
            attribute_name="memberOf",
        ),
    )

    # Setup mocks
    mock_group_response = Mock(spec=GroupResponse)
    mock_group_response.__iter__ = Mock(return_value=iter(sample_groups.values()))
    mock_client.group.get_all.return_value = mock_group_response
    mock_client.sso.get_all_group_mappings.return_value = [valid_mapping]

    # Execute
    deleted_count = diagnostic.cleanup_orphaned_mappings("okta")

    # Verify - no deletions should occur
    assert deleted_count == 0
    mock_client.sso.delete_group_mapping.assert_not_called()


def test_list_all_mappings(diagnostic, mock_client, sample_mappings):
    """Test listing all SSO group mappings."""
    # Setup mock
    mock_client.sso.get_all_group_mappings.return_value = sample_mappings

    # Execute - should not raise any errors
    diagnostic.list_all_mappings("okta")

    # Verify
    mock_client.sso.get_all_group_mappings.assert_called_once_with(sso_alias="okta")


def test_list_all_mappings_empty(diagnostic, mock_client):
    """Test listing when no mappings exist."""
    # Setup mock
    mock_client.sso.get_all_group_mappings.return_value = []

    # Execute - should not raise any errors
    diagnostic.list_all_mappings("okta")

    # Verify
    mock_client.sso.get_all_group_mappings.assert_called_once_with(sso_alias="okta")
