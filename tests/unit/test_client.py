# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import os
from unittest.mock import DEFAULT, Mock, patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.error import NotFoundError
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm, Table
from pyatlan.model.search import Bool, Term

GLOSSARY_NAME = "MyGlossary"
GLOSSARY = AtlasGlossary.create(name=GLOSSARY_NAME)


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, assigned_terms, message",
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
    assigned_terms,
    message,
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    client = AtlanClient()

    with pytest.raises(ValueError, match=message):
        client.append_terms(
            guid=guid,
            qualified_name=qualified_name,
            asset_type=asset_type,
            terms=assigned_terms,
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
        assert asset.assigned_terms == terms


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
        assert asset.assigned_terms == terms


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
        assert (updated_terms := asset.assigned_terms)
        assert len(updated_terms) == 2
        assert exisiting_term in updated_terms
        assert new_term in updated_terms


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, assigned_terms, message",
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
    assigned_terms,
    message,
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    client = AtlanClient()

    with pytest.raises(ValueError, match=message):
        client.replace_terms(
            guid=guid,
            qualified_name=qualified_name,
            asset_type=asset_type,
            terms=assigned_terms,
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
        assert asset.assigned_terms == terms


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, assigned_terms, message",
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
            "A list of assigned_terms to remove must be specified",
        ),
    ],
)
def test_remove_terms_with_invalid_parameter_raises_valueerror(
    guid,
    qualified_name,
    asset_type,
    assigned_terms,
    message,
    monkeypatch,
):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")
    client = AtlanClient()

    with pytest.raises(ValueError, match=message):
        client.remove_terms(
            guid=guid,
            qualified_name=qualified_name,
            asset_type=asset_type,
            terms=assigned_terms,
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
        assert (updated_terms := asset.assigned_terms)
        assert len(updated_terms) == 1
        assert other_term in updated_terms


def test_register_client_with_bad_parameter_raises_value_error():
    with pytest.raises(ValueError, match="client must be an instance of AtlanClient"):
        AtlanClient.register_client("")
    assert AtlanClient.get_default_client() is None


def test_register_client():
    client = AtlanClient(base_url="http://mark.atlan.com", api_key="123")
    AtlanClient.register_client(client)
    assert AtlanClient.get_default_client() == client


def test_reset_client():
    client = AtlanClient(base_url="http://mark.atlan.com", api_key="123")
    AtlanClient.register_client(client)
    AtlanClient.reset_default_client()
    assert AtlanClient.get_default_client() is None


@pytest.mark.parametrize(
    "name, attributes, message",
    [
        (
            1,
            None,
            "1 validation error for FindGlossaryByName\nname\n  str type expected",
        ),
        (
            None,
            None,
            "1 validation error for FindGlossaryByName\nname\n  none is not an allowed value",
        ),
        (
            "Bob",
            1,
            "1 validation error for FindGlossaryByName\nattributes\n  value is not a valid list",
        ),
    ],
)
@patch.dict(
    os.environ,
    {"ATLAN_BASE_URL": "https://dummy.atlan.com", "ATLAN_API_KEY": "123"},
)
def test_find_glossary_by_name_with_bad_values_raises_value_error(
    name, attributes, message
):
    client = AtlanClient()
    with pytest.raises(ValueError, match=message):
        client.find_glossary_by_name(name=name, attributes=attributes)


@patch.dict(
    os.environ,
    {"ATLAN_BASE_URL": "https://dummy.atlan.com", "ATLAN_API_KEY": "123"},
)
@patch.object(AtlanClient, "search")
def test_find_glossary_when_none_found_raises_not_found_error(mock_search):

    mock_search.return_value.count = 0

    client = AtlanClient()
    with pytest.raises(
        NotFoundError,
        match=f"The AtlasGlossy asset could not be found by name: {GLOSSARY_NAME}.",
    ):
        client.find_glossary_by_name(GLOSSARY_NAME)


@patch.dict(
    os.environ,
    {"ATLAN_BASE_URL": "https://dummy.atlan.com", "ATLAN_API_KEY": "123"},
)
@patch.object(AtlanClient, "search")
def test_find_glossary_when_non_glossary_found_raises_not_found_error(mock_search):

    mock_search.return_value.count = 1
    mock_search.return_value.current_page.return_value = [Table()]

    client = AtlanClient()
    with pytest.raises(
        NotFoundError,
        match=f"The AtlasGlossy asset could not be found by name: {GLOSSARY_NAME}.",
    ):
        client.find_glossary_by_name(GLOSSARY_NAME)
    mock_search.return_value.current_page.assert_called_once()


@patch.dict(
    os.environ,
    {"ATLAN_BASE_URL": "https://dummy.atlan.com", "ATLAN_API_KEY": "123"},
)
@patch.object(AtlanClient, "search")
def test_find_glossary(mock_search, caplog):
    request = None
    attributes = ["name"]

    def get_request(*args, **kwargs):
        nonlocal request
        request = args[0]
        mock = Mock()
        mock.count = 1
        mock.current_page.return_value = [GLOSSARY, GLOSSARY]
        return mock

    mock_search.side_effect = get_request

    client = AtlanClient()

    assert GLOSSARY == client.find_glossary_by_name(
        name=GLOSSARY_NAME, attributes=attributes
    )
    assert (
        f"Multiple glossaries found with the name '{GLOSSARY_NAME}', returning only the first."
        in caplog.text
    )
    assert request
    assert request.attributes
    assert attributes == request.attributes
    assert request.dsl
    assert request.dsl.query
    assert isinstance(request.dsl.query, Bool) is True
    assert request.dsl.query.must
    assert 3 == len(request.dsl.query.must)
    term1, term2, term3 = request.dsl.query.must
    assert isinstance(term1, Term) is True
    assert term1.field == "__state"
    assert term1.value == "ACTIVE"
    assert isinstance(term2, Term) is True
    assert term2.field == "__typeName.keyword"
    assert term2.value == "AtlasGlossary"
    assert isinstance(term3, Term) is True
    assert term3.field == "name.keyword"
    assert term3.value == GLOSSARY_NAME
