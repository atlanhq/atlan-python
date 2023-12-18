# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from json import load, loads
from pathlib import Path
from unittest.mock import DEFAULT, Mock, call, patch

import pytest

from pyatlan.client.asset import AssetClient, Batch, CustomMetadataHandling
from pyatlan.client.atlan import AtlanClient
from pyatlan.client.search_log import SearchLogClient
from pyatlan.errors import AtlanError, ErrorCode, InvalidRequestError, NotFoundError
from pyatlan.model.assets import (
    AtlasGlossary,
    AtlasGlossaryCategory,
    AtlasGlossaryTerm,
    Table,
)
from pyatlan.model.response import AssetMutationResponse
from pyatlan.model.search import Bool, Term
from pyatlan.model.search_log import SearchLogRequest
from tests.unit.model.constants import (
    GLOSSARY_CATEGORY_NAME,
    GLOSSARY_NAME,
    GLOSSARY_QUALIFIED_NAME,
    GLOSSARY_TERM_NAME,
)

GLOSSARY = AtlasGlossary.create(name=GLOSSARY_NAME)
GLOSSARY_CATEGORY = AtlasGlossaryCategory.create(
    name=GLOSSARY_CATEGORY_NAME, anchor=GLOSSARY
)
GLOSSARY_TERM = AtlasGlossaryTerm.create(name=GLOSSARY_TERM_NAME, anchor=GLOSSARY)
UNIQUE_USERS = "uniqueUsers"
UNIQUE_ASSETS = "uniqueAssets"
LOG_IP_ADDRESS = "ipAddress"
LOG_USERNAME = "userName"
SEARCH_PARAMS = "searchParameters"
SEARCH_COUNT = "approximateCount"
DATA_RESPONSES_DIR = Path(__file__).parent / "data" / "search_log_responses"
SL_MOST_RECENT_VIEWERS_JSON = "sl_most_recent_viewers.json"
SL_MOST_VIEWED_ASSETS_JSON = "sl_most_viewed_assets.json"
SL_DETAILED_LOG_ENTRIES_JSON = "sl_detailed_log_entries.json"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")


@pytest.fixture()
def client():
    return AtlanClient()


def load_json(filename):
    with (DATA_RESPONSES_DIR / filename).open() as input_file:
        return load(input_file)


@pytest.fixture()
def sl_most_recent_viewers_json():
    return load_json(SL_MOST_RECENT_VIEWERS_JSON)


@pytest.fixture()
def sl_most_viewed_assets_json():
    return load_json(SL_MOST_VIEWED_ASSETS_JSON)


@pytest.fixture()
def sl_detailed_log_entries_json():
    return load_json(SL_DETAILED_LOG_ENTRIES_JSON)


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, assigned_terms, message, error",
    [
        (
            "123",
            None,
            Table,
            None,
            "1 validation error for AppendTerms\\nterms\\n  none is not an allowed value ",
            ValueError,
        ),
        (
            "123",
            None,
            None,
            [AtlasGlossaryTerm()],
            "1 validation error for AppendTerms\\nasset_type\\n  none is not an allowed value ",
            ValueError,
        ),
        (
            None,
            None,
            Table,
            [AtlasGlossaryTerm()],
            "ATLAN-PYTHON-400-043 Either qualified_name or guid should be provided.",
            InvalidRequestError,
        ),
        (
            "123",
            "default/abc",
            Table,
            [AtlasGlossaryTerm()],
            "ATLAN-PYTHON-400-042 Only qualified_name or guid should be provided but not both.",
            InvalidRequestError,
        ),
    ],
)
def test_append_terms_with_invalid_parameter_raises_error(
    guid,
    qualified_name,
    asset_type,
    assigned_terms,
    message,
    error,
    client: AtlanClient,
):
    with pytest.raises(error, match=message):
        client.asset.append_terms(
            guid=guid,
            qualified_name=qualified_name,
            asset_type=asset_type,
            terms=assigned_terms,
        )


def test_append_with_valid_guid_and_no_terms_returns_asset():
    asset_type = Table
    table = asset_type()

    with patch.object(AssetClient, "get_by_guid", return_value=table) as mock_method:
        client = AtlanClient()
        guid = "123"
        terms = []

        assert (
            client.asset.append_terms(guid=guid, asset_type=asset_type, terms=terms)
            == table
        )
    mock_method.assert_called_once_with(guid=guid, asset_type=asset_type)


def test_append_with_valid_guid_when_no_terms_present_returns_asset_with_given_terms():
    asset_type = Table
    with patch.multiple(AssetClient, get_by_guid=DEFAULT, save=DEFAULT) as mock_methods:
        table = Table()
        mock_methods["get_by_guid"].return_value = table
        mock_methods["save"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"
        terms = [AtlasGlossaryTerm()]

        assert (
            asset := client.asset.append_terms(
                guid=guid, asset_type=asset_type, terms=terms
            )
        )
        assert asset.assigned_terms == terms


def test_append_with_valid_guid_when_deleted_terms_present_returns_asset_with_given_terms():
    asset_type = Table
    with patch.multiple(AssetClient, get_by_guid=DEFAULT, save=DEFAULT) as mock_methods:
        table = Table(attributes=Table.Attributes())
        term = AtlasGlossaryTerm()
        term.relationship_status = "DELETED"
        table.attributes.meanings = [term]
        mock_methods["get_by_guid"].return_value = table
        mock_methods["save"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"
        terms = [AtlasGlossaryTerm()]

        assert (
            asset := client.asset.append_terms(
                guid=guid, asset_type=asset_type, terms=terms
            )
        )
        assert asset.assigned_terms == terms


def test_append_with_valid_guid_when_terms_present_returns_asset_with_combined_terms():
    asset_type = Table
    with patch.multiple(AssetClient, get_by_guid=DEFAULT, save=DEFAULT) as mock_methods:
        table = Table(attributes=Table.Attributes())
        exisiting_term = AtlasGlossaryTerm()
        table.attributes.meanings = [exisiting_term]
        mock_methods["get_by_guid"].return_value = table
        mock_methods["save"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"

        new_term = AtlasGlossaryTerm()
        terms = [new_term]

        assert (
            asset := client.asset.append_terms(
                guid=guid, asset_type=asset_type, terms=terms
            )
        )
        assert (updated_terms := asset.assigned_terms)
        assert len(updated_terms) == 2
        assert exisiting_term in updated_terms
        assert new_term in updated_terms


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, assigned_terms, message, error",
    [
        (
            None,
            None,
            Table,
            [AtlasGlossaryTerm()],
            "ATLAN-PYTHON-400-043 Either qualified_name or guid should be provided.",
            InvalidRequestError,
        ),
        (
            "123",
            None,
            None,
            [AtlasGlossaryTerm()],
            "1 validation error for ReplaceTerms\\nasset_type\\n  none is not an allowed value ",
            ValueError,
        ),
        (
            "123",
            "default/abc",
            Table,
            [AtlasGlossaryTerm()],
            "ATLAN-PYTHON-400-042 Only qualified_name or guid should be provided but not both.",
            InvalidRequestError,
        ),
        (
            "123",
            None,
            Table,
            None,
            "1 validation error for ReplaceTerms\\nterms\\n  none is not an allowed value ",
            ValueError,
        ),
    ],
)
def test_replace_terms_with_invalid_parameter_raises_error(
    guid,
    qualified_name,
    asset_type,
    assigned_terms,
    message,
    error,
    client: AtlanClient,
):
    with pytest.raises(error, match=message):
        client.asset.replace_terms(
            guid=guid,
            qualified_name=qualified_name,
            asset_type=asset_type,
            terms=assigned_terms,
        )


def test_replace_terms():
    asset_type = Table
    with patch.multiple(AssetClient, get_by_guid=DEFAULT, save=DEFAULT) as mock_methods:
        table = Table()
        mock_methods["get_by_guid"].return_value = table
        mock_methods["save"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"
        terms = [AtlasGlossaryTerm()]

        assert (
            asset := client.asset.replace_terms(
                guid=guid, asset_type=asset_type, terms=terms
            )
        )
        assert asset.assigned_terms == terms


@pytest.mark.parametrize(
    "guid, qualified_name, asset_type, assigned_terms, message, error",
    [
        (
            None,
            None,
            Table,
            [AtlasGlossaryTerm()],
            "ATLAN-PYTHON-400-043 Either qualified_name or guid should be provided.",
            InvalidRequestError,
        ),
        (
            "123",
            None,
            None,
            [AtlasGlossaryTerm()],
            "1 validation error for RemoveTerms\\nasset_type\\n  none is not an allowed value ",
            ValueError,
        ),
        (
            "123",
            "default/abc",
            Table,
            [AtlasGlossaryTerm()],
            "ATLAN-PYTHON-400-042 Only qualified_name or guid should be provided but not both.",
            InvalidRequestError,
        ),
        (
            "123",
            None,
            Table,
            None,
            "1 validation error for RemoveTerms\\nterms\\n  none is not an allowed value ",
            ValueError,
        ),
        (
            "123",
            None,
            Table,
            [],
            "ATLAN-PYTHON-400-044 A list of assigned_terms to remove must be specified.",
            InvalidRequestError,
        ),
    ],
)
def test_remove_terms_with_invalid_parameter_raises_error(
    guid,
    qualified_name,
    asset_type,
    assigned_terms,
    message,
    error,
    client: AtlanClient,
):
    with pytest.raises(error, match=message):
        client.asset.remove_terms(
            guid=guid,
            qualified_name=qualified_name,
            asset_type=asset_type,
            terms=assigned_terms,
        )


def test_remove_with_valid_guid_when_terms_present_returns_asset_with_terms_removed():
    asset_type = Table
    with patch.multiple(AssetClient, get_by_guid=DEFAULT, save=DEFAULT) as mock_methods:
        table = Table(attributes=Table.Attributes())
        exisiting_term = AtlasGlossaryTerm()
        exisiting_term.guid = "b4113341-251b-4adc-81fb-2420501c30e6"
        other_term = AtlasGlossaryTerm()
        other_term.guid = "b267858d-8316-4c41-a56a-6e9b840cef4a"
        table.attributes.meanings = [exisiting_term, other_term]
        mock_methods["get_by_guid"].return_value = table
        mock_methods["save"].return_value.assets_updated.return_value = [table]
        client = AtlanClient()
        guid = "123"

        assert (
            asset := client.asset.remove_terms(
                guid=guid, asset_type=asset_type, terms=[exisiting_term]
            )
        )
        assert (updated_terms := asset.assigned_terms)
        assert len(updated_terms) == 1
        assert other_term in updated_terms


def test_register_client_with_bad_parameter_raises_value_error(client):
    with pytest.raises(
        InvalidRequestError, match="client must be an instance of AtlanClient"
    ):
        AtlanClient.set_default_client("")
    assert AtlanClient.get_default_client() is client


def test_register_client(client):
    other = AtlanClient(base_url="http://mark.atlan.com", api_key="123")
    assert AtlanClient.get_default_client() == other

    AtlanClient.set_default_client(client)
    assert AtlanClient.get_default_client() == client


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
        (
            " ",
            None,
            "1 validation error for FindGlossaryByName\nname\n  ensure this value has at least 1 characters",
        ),
    ],
)
def test_find_glossary_by_name_with_bad_values_raises_value_error(
    name, attributes, message, client: AtlanClient
):
    with pytest.raises(ValueError, match=message):
        client.asset.find_glossary_by_name(name=name, attributes=attributes)


@patch.object(AssetClient, "search")
def test_find_glossary_when_none_found_raises_not_found_error(mock_search):
    mock_search.return_value.count = 0

    client = AtlanClient()
    with pytest.raises(
        NotFoundError,
        match=f"The AtlasGlossary asset could not be found by name: {GLOSSARY_NAME}.",
    ):
        client.asset.find_glossary_by_name(GLOSSARY_NAME)


@patch.object(AssetClient, "search")
def test_find_glossary_when_non_glossary_found_raises_not_found_error(mock_search):
    mock_search.return_value.count = 1
    mock_search.return_value.current_page.return_value = [Table()]

    client = AtlanClient()
    with pytest.raises(
        NotFoundError,
        match=f"The AtlasGlossary asset could not be found by name: {GLOSSARY_NAME}.",
    ):
        client.asset.find_glossary_by_name(GLOSSARY_NAME)
    mock_search.return_value.current_page.assert_called_once()


@patch.object(AssetClient, "search")
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

    assert GLOSSARY == client.asset.find_glossary_by_name(
        name=GLOSSARY_NAME, attributes=attributes
    )
    assert (
        f"More than 1 AtlasGlossary found with the name '{GLOSSARY_NAME}', returning only the first."
        in caplog.text
    )
    assert request
    assert request.attributes
    assert attributes == request.attributes
    assert request.dsl
    assert request.dsl.query
    assert isinstance(request.dsl.query, Bool) is True
    assert request.dsl.query.filter
    assert 3 == len(request.dsl.query.filter)
    term1, term2, term3 = request.dsl.query.filter
    assert isinstance(term1, Term) is True
    assert term1.field == "__state"
    assert term1.value == "ACTIVE"
    assert isinstance(term2, Term) is True
    assert term2.field == "__typeName.keyword"
    assert term2.value == "AtlasGlossary"
    assert isinstance(term3, Term) is True
    assert term3.field == "name.keyword"
    assert term3.value == GLOSSARY_NAME


@pytest.mark.parametrize(
    "name, glossary_qualified_name, attributes, message",
    [
        (
            1,
            GLOSSARY_QUALIFIED_NAME,
            None,
            "1 validation error for FindCategoryFastByName\nname\n  str type expected",
        ),
        (
            None,
            GLOSSARY_QUALIFIED_NAME,
            None,
            "1 validation error for FindCategoryFastByName\nname\n  none is not an allowed value",
        ),
        (
            " ",
            GLOSSARY_QUALIFIED_NAME,
            None,
            "1 validation error for FindCategoryFastByName\nname\n  ensure this value has at least 1 characters",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            None,
            None,
            "1 validation error for FindCategoryFastByName\nglossary_qualified_name\n  none is not an allowed value",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            " ",
            None,
            "1 validation error for FindCategoryFastByName\nglossary_qualified_name\n  ensure this value has at "
            "least 1 characters",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            1,
            None,
            "1 validation error for FindCategoryFastByName\nglossary_qualified_name\n  str type expected",
        ),
        (
            GLOSSARY_NAME,
            GLOSSARY_QUALIFIED_NAME,
            1,
            "1 validation error for FindCategoryFastByName\nattributes\n  value is not a valid list",
        ),
    ],
)
def test_find_category_fast_by_name_with_bad_values_raises_value_error(
    name, glossary_qualified_name, attributes, message, client: AtlanClient
):
    with pytest.raises(ValueError, match=message):
        client.asset.find_category_fast_by_name(
            name=name,
            glossary_qualified_name=glossary_qualified_name,
            attributes=attributes,
        )


@patch.object(AssetClient, "search")
def test_find_category_fast_by_name_when_none_found_raises_not_found_error(mock_search):
    mock_search.return_value.count = 0

    client = AtlanClient()
    with pytest.raises(
        NotFoundError,
        match=f"The AtlasGlossaryCategory asset could not be found by name: {GLOSSARY_CATEGORY_NAME}.",
    ):
        client.asset.find_category_fast_by_name(
            name=GLOSSARY_CATEGORY_NAME, glossary_qualified_name=GLOSSARY_QUALIFIED_NAME
        )


@patch.object(AssetClient, "search")
def test_find_category_fast_by_name_when_non_category_found_raises_not_found_error(
    mock_search,
):
    mock_search.return_value.count = 1
    mock_search.return_value.current_page.return_value = [Table()]

    client = AtlanClient()
    with pytest.raises(
        NotFoundError,
        match=f"The AtlasGlossaryCategory asset could not be found by name: {GLOSSARY_CATEGORY_NAME}.",
    ):
        client.asset.find_category_fast_by_name(
            name=GLOSSARY_CATEGORY_NAME, glossary_qualified_name=GLOSSARY_QUALIFIED_NAME
        )
    mock_search.return_value.current_page.assert_called_once()


@patch.object(AssetClient, "search")
def test_find_category_fast_by_name(mock_search, caplog):
    request = None
    attributes = ["name"]

    def get_request(*args, **kwargs):
        nonlocal request
        request = args[0]
        mock = Mock()
        mock.count = 1
        mock.current_page.return_value = [GLOSSARY_CATEGORY, GLOSSARY_CATEGORY]
        return mock

    mock_search.side_effect = get_request

    client = AtlanClient()

    assert (
        GLOSSARY_CATEGORY
        == client.asset.find_category_fast_by_name(
            name=GLOSSARY_CATEGORY_NAME,
            glossary_qualified_name=GLOSSARY_QUALIFIED_NAME,
            attributes=attributes,
        )[0]
    )
    assert request
    assert request.attributes
    assert attributes == request.attributes
    assert request.dsl
    assert request.dsl.query
    assert isinstance(request.dsl.query, Bool) is True
    assert request.dsl.query.filter
    assert 4 == len(request.dsl.query.filter)
    term1, term2, term3, term4 = request.dsl.query.filter
    assert term1.field == "__state"
    assert term1.value == "ACTIVE"
    assert isinstance(term2, Term) is True
    assert term2.field == "__typeName.keyword"
    assert term2.value == "AtlasGlossaryCategory"
    assert isinstance(term3, Term) is True
    assert term3.field == "name.keyword"
    assert term3.value == GLOSSARY_CATEGORY_NAME
    assert isinstance(term4, Term) is True
    assert term4.field == "__glossary"
    assert term4.value == GLOSSARY_QUALIFIED_NAME


@pytest.mark.parametrize(
    "name, glossary_name, attributes, message",
    [
        (
            None,
            GLOSSARY_NAME,
            None,
            "1 validation error for FindCategoryByName\nname\n  none is not an allowed value",
        ),
        (
            " ",
            GLOSSARY_NAME,
            None,
            "1 validation error for FindCategoryByName\nname\n  ensure this value has at least 1 characters",
        ),
        (
            1,
            GLOSSARY_NAME,
            None,
            "1 validation error for FindCategoryByName\nname\n  str type expected",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            None,
            None,
            "1 validation error for FindCategoryByName\nglossary_name\n  none is not an allowed value",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            " ",
            None,
            "1 validation error for FindCategoryByName\nglossary_name\n  ensure this value has at least 1 characters",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            1,
            None,
            "1 validation error for FindCategoryByName\nglossary_name\n  str type expected",
        ),
        (
            GLOSSARY_CATEGORY_NAME,
            GLOSSARY_NAME,
            1,
            "1 validation error for FindCategoryByName\nattributes\n  value is not a valid list",
        ),
    ],
)
def test_find_category_by_name_when_bad_parameter_raises_value_error(
    name, glossary_name, attributes, message, client: AtlanClient
):
    sut = client

    with pytest.raises(ValueError, match=message):
        sut.asset.find_category_by_name(
            name=name, glossary_name=glossary_name, attributes=attributes
        )


def test_find_category_by_name():
    attributes = ["name"]
    with patch.multiple(
        AssetClient, find_glossary_by_name=DEFAULT, find_category_fast_by_name=DEFAULT
    ) as values:
        mock_find_glossary_by_name = values["find_glossary_by_name"]
        mock_find_glossary_by_name.return_value.qualified_name = GLOSSARY_QUALIFIED_NAME
        mock_find_category_fast_by_name = values["find_category_fast_by_name"]

        sut = AtlanClient()

        category = sut.asset.find_category_by_name(
            name=GLOSSARY_CATEGORY_NAME,
            glossary_name=GLOSSARY_NAME,
            attributes=attributes,
        )

        mock_find_glossary_by_name.assert_called_with(name=GLOSSARY_NAME)
        mock_find_category_fast_by_name.assert_called_with(
            name=GLOSSARY_CATEGORY_NAME,
            glossary_qualified_name=GLOSSARY_QUALIFIED_NAME,
            attributes=attributes,
        )
        assert mock_find_category_fast_by_name.return_value == category


@pytest.mark.parametrize(
    "name, glossary_qualified_name, attributes, message",
    [
        (
            1,
            GLOSSARY_QUALIFIED_NAME,
            None,
            "1 validation error for FindTermFastByName\nname\n  str type expected",
        ),
        (
            None,
            GLOSSARY_QUALIFIED_NAME,
            None,
            "1 validation error for FindTermFastByName\nname\n  none is not an allowed value",
        ),
        (
            " ",
            GLOSSARY_QUALIFIED_NAME,
            None,
            "1 validation error for FindTermFastByName\nname\n  ensure this value has at least 1 characters",
        ),
        (
            GLOSSARY_TERM_NAME,
            None,
            None,
            "1 validation error for FindTermFastByName\nglossary_qualified_name\n  none is not an allowed value",
        ),
        (
            GLOSSARY_TERM_NAME,
            " ",
            None,
            "1 validation error for FindTermFastByName\nglossary_qualified_name\n  ensure this value has at "
            "least 1 characters",
        ),
        (
            GLOSSARY_TERM_NAME,
            1,
            None,
            "1 validation error for FindTermFastByName\nglossary_qualified_name\n  str type expected",
        ),
        (
            GLOSSARY_TERM_NAME,
            GLOSSARY_QUALIFIED_NAME,
            1,
            "1 validation error for FindTermFastByName\nattributes\n  value is not a valid list",
        ),
    ],
)
def test_find_term_fast_by_name_with_bad_values_raises_value_error(
    name, glossary_qualified_name, attributes, message, client: AtlanClient
):
    with pytest.raises(ValueError, match=message):
        client.asset.find_term_fast_by_name(
            name=name,
            glossary_qualified_name=glossary_qualified_name,
            attributes=attributes,
        )


@patch.object(AssetClient, "search")
def test_find_term_fast_by_name_when_none_found_raises_not_found_error(mock_search):
    mock_search.return_value.count = 0

    client = AtlanClient()
    with pytest.raises(
        NotFoundError,
        match=f"The AtlasGlossaryTerm asset could not be found by name: {GLOSSARY_TERM_NAME}.",
    ):
        client.asset.find_term_fast_by_name(
            name=GLOSSARY_TERM_NAME, glossary_qualified_name=GLOSSARY_QUALIFIED_NAME
        )


@patch.object(AssetClient, "search")
def test_find_term_fast_by_name_when_non_term_found_raises_not_found_error(
    mock_search,
):
    mock_search.return_value.count = 1
    mock_search.return_value.current_page.return_value = [Table()]

    client = AtlanClient()
    with pytest.raises(
        NotFoundError,
        match=f"The AtlasGlossaryTerm asset could not be found by name: {GLOSSARY_TERM_NAME}.",
    ):
        client.asset.find_term_fast_by_name(
            name=GLOSSARY_TERM_NAME, glossary_qualified_name=GLOSSARY_QUALIFIED_NAME
        )
    mock_search.return_value.current_page.assert_called_once()


@patch.object(AssetClient, "search")
def test_find_term_fast_by_name(mock_search, caplog):
    request = None
    attributes = ["name"]

    def get_request(*args, **kwargs):
        nonlocal request
        request = args[0]
        mock = Mock()
        mock.count = 1
        mock.current_page.return_value = [GLOSSARY_TERM, GLOSSARY_TERM]
        return mock

    mock_search.side_effect = get_request

    client = AtlanClient()

    assert GLOSSARY_TERM == client.asset.find_term_fast_by_name(
        name=GLOSSARY_TERM_NAME,
        glossary_qualified_name=GLOSSARY_QUALIFIED_NAME,
        attributes=attributes,
    )
    assert (
        f"More than 1 AtlasGlossaryTerm found with the name '{GLOSSARY_TERM_NAME}', returning only the first."
        in caplog.text
    )
    assert request
    assert request.attributes
    assert attributes == request.attributes
    assert request.dsl
    assert request.dsl.query
    assert isinstance(request.dsl.query, Bool) is True
    assert request.dsl.query.filter
    assert 4 == len(request.dsl.query.filter)
    term1, term2, term3, term4 = request.dsl.query.filter
    assert term1.field == "__state"
    assert term1.value == "ACTIVE"
    assert isinstance(term2, Term) is True
    assert term2.field == "__typeName.keyword"
    assert term2.value == "AtlasGlossaryTerm"
    assert isinstance(term3, Term) is True
    assert term3.field == "name.keyword"
    assert term3.value == GLOSSARY_TERM_NAME
    assert isinstance(term4, Term) is True
    assert term4.field == "__glossary"
    assert term4.value == GLOSSARY_QUALIFIED_NAME


@pytest.mark.parametrize(
    "name, glossary_name, attributes, message",
    [
        (
            None,
            GLOSSARY_NAME,
            None,
            "1 validation error for FindTermByName\nname\n  none is not an allowed value",
        ),
        (
            " ",
            GLOSSARY_NAME,
            None,
            "1 validation error for FindTermByName\nname\n  ensure this value has at least 1 characters",
        ),
        (
            1,
            GLOSSARY_NAME,
            None,
            "1 validation error for FindTermByName\nname\n  str type expected",
        ),
        (
            GLOSSARY_TERM_NAME,
            None,
            None,
            "1 validation error for FindTermByName\nglossary_name\n  none is not an allowed value",
        ),
        (
            GLOSSARY_TERM_NAME,
            " ",
            None,
            "1 validation error for FindTermByName\nglossary_name\n  ensure this value has at least 1 characters",
        ),
        (
            GLOSSARY_TERM_NAME,
            1,
            None,
            "1 validation error for FindTermByName\nglossary_name\n  str type expected",
        ),
        (
            GLOSSARY_TERM_NAME,
            GLOSSARY_NAME,
            1,
            "1 validation error for FindTermByName\nattributes\n  value is not a valid list",
        ),
    ],
)
def test_find_term_by_name_when_bad_parameter_raises_value_error(
    name, glossary_name, attributes, message, client: AtlanClient
):
    sut = client

    with pytest.raises(ValueError, match=message):
        sut.asset.find_term_by_name(
            name=name, glossary_name=glossary_name, attributes=attributes
        )


def test_find_term_by_name():
    attributes = ["name"]
    with patch.multiple(
        AssetClient, find_glossary_by_name=DEFAULT, find_term_fast_by_name=DEFAULT
    ) as values:
        mock_find_glossary_by_name = values["find_glossary_by_name"]
        mock_find_glossary_by_name.return_value.qualified_name = GLOSSARY_QUALIFIED_NAME
        mock_find_term_fast_by_name = values["find_term_fast_by_name"]

        sut = AtlanClient()

        term = sut.asset.find_term_by_name(
            name=GLOSSARY_TERM_NAME,
            glossary_name=GLOSSARY_NAME,
            attributes=attributes,
        )

        mock_find_glossary_by_name.assert_called_with(name=GLOSSARY_NAME)
        mock_find_term_fast_by_name.assert_called_with(
            name=GLOSSARY_TERM_NAME,
            glossary_qualified_name=GLOSSARY_QUALIFIED_NAME,
            attributes=attributes,
        )
        assert mock_find_term_fast_by_name.return_value == term


@patch.object(SearchLogClient, "_call_search_api")
def test_search_log_most_recent_viewers(mock_sl_api_call, sl_most_recent_viewers_json):
    client = AtlanClient()
    mock_sl_api_call.return_value = sl_most_recent_viewers_json
    recent_viewers_aggs = sl_most_recent_viewers_json["aggregations"]
    recent_viewers_aggs_buckets = recent_viewers_aggs[UNIQUE_USERS]["buckets"]
    request = SearchLogRequest.most_recent_viewers("test-guid-123")
    request_dsl_json = loads(request.dsl.json(by_alias=True, exclude_none=True))
    response = client.search_log.search(request)
    viewers = response.user_views
    assert len(viewers) == 3
    assert response.asset_views is None
    assert request_dsl_json == sl_most_recent_viewers_json[SEARCH_PARAMS]["dsl"]
    assert response.count == sl_most_recent_viewers_json[SEARCH_COUNT]
    assert viewers[0].username == recent_viewers_aggs_buckets[0]["key"]
    assert viewers[0].view_count == recent_viewers_aggs_buckets[0]["doc_count"]
    assert viewers[0].most_recent_view
    assert viewers[1].username == recent_viewers_aggs_buckets[1]["key"]
    assert viewers[1].view_count == recent_viewers_aggs_buckets[1]["doc_count"]
    assert viewers[1].most_recent_view


@patch.object(SearchLogClient, "_call_search_api")
def test_search_log_most_viewed_assets(mock_sl_api_call, sl_most_viewed_assets_json):
    client = AtlanClient()
    mock_sl_api_call.return_value = sl_most_viewed_assets_json
    viewed_assets_aggs = sl_most_viewed_assets_json["aggregations"]
    viewed_assets_aggs_buckets = viewed_assets_aggs[UNIQUE_ASSETS]["buckets"][0]
    request = SearchLogRequest.most_viewed_assets(10)
    request_dsl_json = loads(request.dsl.json(by_alias=True, exclude_none=True))
    response = client.search_log.search(request)
    detail = response.asset_views
    assert len(detail) == 8
    assert response.user_views is None
    assert request_dsl_json == sl_most_viewed_assets_json[SEARCH_PARAMS]["dsl"]
    assert response.count == sl_most_viewed_assets_json[SEARCH_COUNT]
    assert detail[0].guid == viewed_assets_aggs_buckets["key"]
    assert detail[0].total_views == viewed_assets_aggs_buckets["doc_count"]
    assert detail[0].distinct_users == viewed_assets_aggs_buckets[UNIQUE_USERS]["value"]


@patch.object(SearchLogClient, "_call_search_api")
def test_search_log_views_by_guid(mock_sl_api_call, sl_detailed_log_entries_json):
    client = AtlanClient()
    mock_sl_api_call.return_value = sl_detailed_log_entries_json
    sl_detailed_log_entries = sl_detailed_log_entries_json["logs"]
    request = SearchLogRequest.views_by_guid(guid="test-guid-123", size=10)
    request_dsl_json = loads(request.dsl.json(by_alias=True, exclude_none=True))
    response = client.search_log.search(request)
    log_entries = response.current_page()
    assert request_dsl_json == sl_detailed_log_entries_json[SEARCH_PARAMS]["dsl"]
    assert len(response.current_page()) == sl_detailed_log_entries_json[SEARCH_COUNT]
    assert log_entries[0].user_name == sl_detailed_log_entries[0][LOG_USERNAME]
    assert log_entries[0].ip_address == sl_detailed_log_entries[0][LOG_IP_ADDRESS]
    assert log_entries[0].host
    assert log_entries[0].user_agent
    assert log_entries[0].utm_tags
    assert log_entries[0].entity_guids_all
    assert log_entries[0].entity_guids_allowed
    assert log_entries[0].entity_qf_names_all
    assert log_entries[0].entity_qf_names_allowed
    assert log_entries[0].entity_type_names_all
    assert log_entries[0].entity_type_names_allowed
    assert log_entries[0].has_result
    assert log_entries[0].results_count
    assert log_entries[0].response_time
    assert log_entries[0].created_at
    assert log_entries[0].timestamp
    assert log_entries[0].failed is False
    assert log_entries[0].request_dsl
    assert log_entries[0].request_dsl_text
    assert log_entries[0].request_attributes is None
    assert log_entries[0].request_relation_attributes


class TestBatch:
    @pytest.fixture
    def mock_asset_client(self):
        return Mock(AssetClient)

    def test_init(self, mock_asset_client):
        sut = Batch(client=mock_asset_client, max_size=10)

        self.assert_asset_client_not_called(mock_asset_client, sut)

    def assert_asset_client_not_called(self, mock_asset_client, sut):
        assert 0 == len(sut.created)
        assert 0 == len(sut.updated)
        assert 0 == len(sut.failures)
        mock_asset_client.assert_not_called()

    @pytest.mark.parametrize(
        "custom_metadata_handling",
        [
            (CustomMetadataHandling.IGNORE),
            (CustomMetadataHandling.OVERWRITE),
            (CustomMetadataHandling.MERGE),
        ],
    )
    def test_add_when_capture_failure_true(
        self, custom_metadata_handling, mock_asset_client
    ):
        table_1 = Mock(Table)
        table_2 = Mock(Table)
        table_3 = Mock(Table)
        table_4 = Mock(Table)
        mock_response = Mock(spec=AssetMutationResponse)
        mutated_entities = Mock()
        created = [table_1]
        updated = [table_2]
        mutated_entities.CREATE = created
        mutated_entities.UPDATE = updated
        mock_response.attach_mock(mutated_entities, "mutated_entities")

        if custom_metadata_handling == CustomMetadataHandling.IGNORE:
            mock_asset_client.save.return_value = mock_response
        elif custom_metadata_handling == CustomMetadataHandling.OVERWRITE:
            mock_asset_client.save_replacing_cm.return_value = mock_response
        else:
            mock_asset_client.save_merging_cm.return_value = mock_response

        sut = Batch(
            client=mock_asset_client,
            max_size=2,
            capture_failures=True,
            custom_metadata_handling=custom_metadata_handling,
        )
        sut.add(table_1)
        self.assert_asset_client_not_called(mock_asset_client, sut)

        sut.add(table_2)

        assert len(created) == len(sut.created)
        assert len(updated) == len(sut.updated)
        for unsaved, saved in zip(created, sut.created):
            unsaved.trim_to_required.called_once()
            assert unsaved.name == saved.name
        for unsaved, saved in zip(updated, sut.updated):
            unsaved.trim_to_required.called_once()
            assert unsaved.name == saved.name

        exception = ErrorCode.INVALID_REQUEST_PASSTHROUGH.exception_with_parameters(
            "bad", "stuff"
        )
        if custom_metadata_handling == CustomMetadataHandling.IGNORE:
            mock_asset_client.save.side_effect = exception
        elif custom_metadata_handling == CustomMetadataHandling.OVERWRITE:
            mock_asset_client.save_replacing_cm.side_effect = exception
        else:
            mock_asset_client.save_merging_cm.side_effect = exception

        sut.add(table_3)

        sut.add(table_4)

        assert 1 == len(sut.failures)
        failure = sut.failures[0]
        assert [table_3, table_4] == failure.failed_assets
        assert exception == failure.failure_reason
        if custom_metadata_handling == CustomMetadataHandling.IGNORE:
            mock_asset_client.save.has_calls(
                [
                    call([table_1, table_2], replace_atlan_tags=False),
                    call([table_3, table_4], replace_atlan_tags=False),
                ]
            )
        elif custom_metadata_handling == CustomMetadataHandling.OVERWRITE:
            mock_asset_client.save_replacing_cm.has_calls(
                [
                    call([table_1, table_2], replace_atlan_tags=False),
                    call([table_3, table_4], replace_atlan_tags=False),
                ]
            )
        else:
            mock_asset_client.save_merging_cm.has_calls(
                [
                    call([table_1, table_2], replace_atlan_tags=False),
                    call([table_3, table_4], replace_atlan_tags=False),
                ]
            )

    @pytest.mark.parametrize(
        "custom_metadata_handling",
        [
            (CustomMetadataHandling.IGNORE),
            (CustomMetadataHandling.OVERWRITE),
            (CustomMetadataHandling.MERGE),
        ],
    )
    def test_add_when_capture_failure_false_then_exception_raised(
        self, custom_metadata_handling, mock_asset_client
    ):
        exception = ErrorCode.INVALID_REQUEST_PASSTHROUGH.exception_with_parameters(
            "bad", "stuff"
        )
        if custom_metadata_handling == CustomMetadataHandling.IGNORE:
            mock_asset_client.save.side_effect = exception
        elif custom_metadata_handling == CustomMetadataHandling.OVERWRITE:
            mock_asset_client.save_replacing_cm.side_effect = exception
        else:
            mock_asset_client.save_merging_cm.side_effect = exception

        sut = Batch(
            client=mock_asset_client,
            max_size=1,
            capture_failures=False,
            custom_metadata_handling=custom_metadata_handling,
        )
        with pytest.raises(AtlanError):
            sut.add(Mock(Table))

        assert 0 == len(sut.failures)
        assert 0 == len(sut.created)
        assert 0 == len(sut.updated)
