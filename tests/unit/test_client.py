# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import DEFAULT, patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossaryTerm, Table


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, terms, message",
    [
        (
            "123",
            None,
            Table,
            None,
            "1 validation error for AppendTerms\\nterms\\n  none is not an allowed value ",
        ),
        (
            None,
            None,
            Table,
            [AtlasGlossaryTerm()],
            "Either guid or qualified name must be specified",
        ),
        (
            "123",
            None,
            None,
            [AtlasGlossaryTerm()],
            "1 validation error for AppendTerms\\nasset_type\\n  none is not an allowed value ",
        ),
        (
            "123",
            "default/abc",
            Table,
            [AtlasGlossaryTerm()],
            "Either guid or qualified_name can be be specified not both",
        ),
    ],
)
def test_append_terms_with_invalid_parameter_raises_valueerror(
    guid,
    qualified_name,
    asset_type,
    terms,
    message,
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    client = AtlanClient()

    with pytest.raises(ValueError, match=message):
        client.append_terms(
            guid=guid, qualified_name=qualified_name, asset_type=asset_type, terms=terms
        )


def test_append_with_valid_guid_and_no_terms_returns_asset(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    asset_type = Table
    table = asset_type()

    with patch.object(
        AtlanClient, "get_asset_by_guid", return_value=table
    ) as mock_method:
        client = AtlanClient()
        guid = "123"
        terms = []

        assert (
            client.append_terms(guid=guid, asset_type=asset_type, terms=terms) == table
        )
    mock_method.assert_called_once_with(guid=guid, asset_type=asset_type)


def test_append_with_valid_guid_when_no_terms_present_returns_asset_with_given_terms(
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    asset_type = Table
    with patch.multiple(
        AtlanClient, get_asset_by_guid=DEFAULT, upsert=DEFAULT
    ) as mock_methods:
        table = Table()
        mock_methods["get_asset_by_guid"].return_value = table
        mock_methods["upsert"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"
        terms = [AtlasGlossaryTerm()]

        assert (
            asset := client.append_terms(guid=guid, asset_type=asset_type, terms=terms)
        )
        assert asset.terms == terms


def test_append_with_valid_guid_when_deleted_terms_present_returns_asset_with_given_terms(
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    asset_type = Table
    with patch.multiple(
        AtlanClient, get_asset_by_guid=DEFAULT, upsert=DEFAULT
    ) as mock_methods:
        table = Table(attributes=Table.Attributes())
        term = AtlasGlossaryTerm()
        term.relationship_status = "DELETED"
        table.attributes.meanings = [term]
        mock_methods["get_asset_by_guid"].return_value = table
        mock_methods["upsert"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"
        terms = [AtlasGlossaryTerm()]

        assert (
            asset := client.append_terms(guid=guid, asset_type=asset_type, terms=terms)
        )
        assert asset.terms == terms


def test_append_with_valid_guid_when_terms_present_returns_asset_with_combined_terms(
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    asset_type = Table
    with patch.multiple(
        AtlanClient, get_asset_by_guid=DEFAULT, upsert=DEFAULT
    ) as mock_methods:
        table = Table(attributes=Table.Attributes())
        exisiting_term = AtlasGlossaryTerm()
        table.attributes.meanings = [exisiting_term]
        mock_methods["get_asset_by_guid"].return_value = table
        mock_methods["upsert"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"

        new_term = AtlasGlossaryTerm()
        terms = [new_term]

        assert (
            asset := client.append_terms(guid=guid, asset_type=asset_type, terms=terms)
        )
        assert (updated_terms := asset.terms)
        assert len(updated_terms) == 2
        assert exisiting_term in updated_terms
        assert new_term in updated_terms


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, terms, message",
    [
        (
            None,
            None,
            Table,
            [AtlasGlossaryTerm()],
            "Either guid or qualified name must be specified",
        ),
        (
            "123",
            None,
            None,
            [AtlasGlossaryTerm()],
            "1 validation error for ReplaceTerms\\nasset_type\\n  none is not an allowed value ",
        ),
        (
            "123",
            "default/abc",
            Table,
            [AtlasGlossaryTerm()],
            "Either guid or qualified_name can be be specified not both",
        ),
        (
            "123",
            None,
            Table,
            None,
            "1 validation error for ReplaceTerms\\nterms\\n  none is not an allowed value ",
        ),
    ],
)
def test_replace_terms_with_invalid_parameter_raises_valueerror(
    guid,
    qualified_name,
    asset_type,
    terms,
    message,
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    client = AtlanClient()

    with pytest.raises(ValueError, match=message):
        client.replace_terms(
            guid=guid, qualified_name=qualified_name, asset_type=asset_type, terms=terms
        )


def test_replace_terms(
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    asset_type = Table
    with patch.multiple(
        AtlanClient, get_asset_by_guid=DEFAULT, upsert=DEFAULT
    ) as mock_methods:
        table = Table()
        mock_methods["get_asset_by_guid"].return_value = table
        mock_methods["upsert"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"
        terms = [AtlasGlossaryTerm()]

        assert (
            asset := client.replace_terms(guid=guid, asset_type=asset_type, terms=terms)
        )
        assert asset.terms == terms


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, terms, message",
    [
        (
            None,
            None,
            Table,
            [AtlasGlossaryTerm()],
            "Either guid or qualified name must be specified",
        ),
        (
            "123",
            None,
            None,
            [AtlasGlossaryTerm()],
            "1 validation error for RemoveTerms\\nasset_type\\n  none is not an allowed value ",
        ),
        (
            "123",
            "default/abc",
            Table,
            [AtlasGlossaryTerm()],
            "Either guid or qualified_name can be be specified not both",
        ),
        (
            "123",
            None,
            Table,
            None,
            "1 validation error for RemoveTerms\\nterms\\n  none is not an allowed value ",
        ),
        (
            "123",
            None,
            Table,
            [],
            "A list of terms to remove must be specified",
        ),
    ],
)
def test_remove_terms_with_invalid_parameter_raises_valueerror(
    guid,
    qualified_name,
    asset_type,
    terms,
    message,
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    client = AtlanClient()

    with pytest.raises(ValueError, match=message):
        client.remove_terms(
            guid=guid, qualified_name=qualified_name, asset_type=asset_type, terms=terms
        )


def test_remove_with_valid_guid_when_terms_present_returns_asset_with_terms_removed(
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    asset_type = Table
    with patch.multiple(
        AtlanClient, get_asset_by_guid=DEFAULT, upsert=DEFAULT
    ) as mock_methods:
        table = Table(attributes=Table.Attributes())
        exisiting_term = AtlasGlossaryTerm()
        exisiting_term.guid = "b4113341-251b-4adc-81fb-2420501c30e6"
        other_term = AtlasGlossaryTerm()
        other_term.guid = "b267858d-8316-4c41-a56a-6e9b840cef4a"
        table.attributes.meanings = [exisiting_term, other_term]
        mock_methods["get_asset_by_guid"].return_value = table
        mock_methods["upsert"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"

        assert (
            asset := client.remove_terms(
                guid=guid, asset_type=asset_type, terms=[exisiting_term]
            )
        )
        assert (updated_terms := asset.terms)
        assert len(updated_terms) == 1
        assert other_term in updated_terms
