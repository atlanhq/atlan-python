from json import load
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pyatlan.client.audit import LOGGER, AuditClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.audit import AuditSearchRequest, AuditSearchResults
from pyatlan.model.enums import SortOrder
from pyatlan.model.fluent_search import DSL
from pyatlan.model.search import Bool, SortItem, Term

# Constants
SEARCH_RESPONSES_DIR = Path(__file__).parent / "data" / "search_responses"
AUDIT_SEARCH_PAGING_JSON = "audit_search_paging.json"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")


@pytest.fixture(scope="module")
def mock_api_caller():
    return Mock()


@pytest.fixture()
def audit_search_paging_json():
    def load_json(filename):
        with (SEARCH_RESPONSES_DIR / filename).open() as input_file:
            return load(input_file)

    return load_json(AUDIT_SEARCH_PAGING_JSON)


TEST_THRESHOLD = 1


def create_dsl(entity_id, sort=None, size=1, from_=0):
    return DSL(
        query=Bool(filter=[Term(field="entityId", value=entity_id)]),
        sort=sort or [],
        size=size,
        from_=from_,
    )


def _assert_audit_search_results(results, response_json, sorts, bulk=False):
    for i, result in enumerate(results.current_page()):
        assert result
        assert result.entity_id == response_json["entityAudits"][i]["entity_id"]
        assert (
            result.entity_qualified_name
            == response_json["entityAudits"][i]["entity_qualified_name"]
        )
        assert result.type_name == response_json["entityAudits"][i]["type_name"]

    assert results.total_count == response_json["totalCount"]
    assert results._bulk == bulk
    assert results._criteria.dsl.sort == sorts


@patch.object(LOGGER, "debug")
def test_audit_search_pagination(
    mock_logger, mock_api_caller, audit_search_paging_json
):
    client = AuditClient(mock_api_caller)
    mock_api_caller._call_api.side_effect = [
        audit_search_paging_json,
        audit_search_paging_json,
        {},
    ]

    # Test default pagination
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value="some-guid")]),
        sort=[SortItem(field="entityId", order=SortOrder.ASCENDING)],
        size=2,
        from_=0,
    )
    audit_search_request = AuditSearchRequest(dsl=dsl)
    response = client.search(criteria=audit_search_request)
    expected_sorts = [SortItem(field="entityId", order=SortOrder.ASCENDING)]

    _assert_audit_search_results(response, audit_search_paging_json, expected_sorts)
    assert mock_api_caller._call_api.call_count == 1
    mock_api_caller.reset_mock()

    # Test bulk pagination
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value="some-guid")]),
        sort=[],
        size=2,
        from_=0,
    )
    audit_search_request = AuditSearchRequest(dsl=dsl)
    response = client.search(criteria=audit_search_request, bulk=True)
    expected_sorts = [
        SortItem(field="created", order=SortOrder.ASCENDING),
        SortItem(field="entityId", order=SortOrder.ASCENDING),
    ]

    _assert_audit_search_results(
        response, audit_search_paging_json, expected_sorts, bulk=True
    )
    assert mock_logger.call_count == 1
    assert "Bulk search option is enabled." in mock_logger.call_args_list[0][0][0]
    mock_logger.reset_mock()
    mock_api_caller.reset_mock()

    # Test automatic bulk conversion when exceeding threshold
    with patch.object(AuditSearchResults, "_MASS_EXTRACT_THRESHOLD", TEST_THRESHOLD):
        mock_api_caller._call_api.side_effect = [
            audit_search_paging_json,
            audit_search_paging_json,
            {},
        ]
        dsl = create_dsl("some-guid")
        audit_search_request = AuditSearchRequest(dsl=dsl)
        response = client.search(criteria=audit_search_request)
        _assert_audit_search_results(
            response, audit_search_paging_json, expected_sorts, bulk=False
        )
        assert mock_logger.call_count == 1
        assert (
            "Result size (%s) exceeds threshold (%s)"
            in mock_logger.call_args_list[0][0][0]
        )
    mock_logger.reset_mock()
    mock_api_caller.reset_mock()

    # Test exception for bulk=True with user-defined sorting
    dsl = create_dsl(
        "some-guid", sort=[SortItem(field="user", order=SortOrder.ASCENDING)]
    )
    audit_search_request = AuditSearchRequest(dsl=dsl)
    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-063 Unable to execute "
            "bulk search with user-defined sorting options. "
            "Suggestion: Please ensure that no sorting options are "
            "included in your search request when performing a bulk search."
        ),
    ):
        client.search(criteria=audit_search_request, bulk=True)
