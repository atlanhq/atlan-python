# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import DEFAULT, patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossaryTerm, Table


@pytest.mark.parametrize(
    "guid, asset_type, terms, message",
    [
        (
            "123",
            Table,
            None,
            "1 validation error for AppendTerms\\nterms\\n  none is not an allowed value "
            "\(type=type_error.none.not_allowed\)",  # noqa: W605
        ),
        (
            None,
            Table,
            [AtlasGlossaryTerm()],
            "1 validation error for AppendTerms\\nguid\\n  none is not an allowed value "
            "\(type=type_error.none.not_allowed\)",  # noqa: W605
        ),
        (
            "123",
            None,
            [AtlasGlossaryTerm()],
            "1 validation error for AppendTerms\\nasset_type\\n  none is not an allowed value "
            "\(type=type_error.none.not_allowed\)",  # noqa: W605
        ),
    ],
)
def test_append_terms_with_invalid_parameter_raises_valueerror(
    guid,
    asset_type,
    terms,
    message,
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    client = AtlanClient()

    with pytest.raises(ValueError, match=message):
        client.append_terms(guid=guid, asset_type=asset_type, terms=terms)


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
