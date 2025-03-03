from datetime import datetime, timezone
from json import load
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pyatlan.client.audit import LOGGER, AuditClient
from pyatlan.client.common import ApiCaller
from pyatlan.errors import InvalidRequestError
from pyatlan.model.audit import AuditSearchRequest, AuditSearchResults
from pyatlan.model.enums import SortOrder
from pyatlan.model.fluent_search import DSL
from pyatlan.model.search import Bool, SortItem, Term

SEARCH_RESPONSES_DIR = Path(__file__).parent / "data" / "search_responses"
AUDIT_SEARCH_PAGING_JSON = "audit_search_paging.json"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")


@pytest.fixture(scope="module")
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def audit_search_paging_json():
    def load_json(filename):
        with (SEARCH_RESPONSES_DIR / filename).open() as input_file:
            return load(input_file)

    return load_json(AUDIT_SEARCH_PAGING_JSON)


def _assert_audit_search_results(
    results: AuditSearchResults, response_json, sorts, bulk=False
):
    for audit in results:
        assert audit.entity_id == response_json["entityAudits"][0]["entity_id"]
        assert (
            audit.entity_qualified_name
            == response_json["entityAudits"][0]["entity_qualified_name"]
        )
        assert audit.type_name == response_json["entityAudits"][0]["type_name"]
        expected_timestamp = datetime.fromtimestamp(
            response_json["entityAudits"][0]["timestamp"] / 1000, tz=timezone.utc
        )
        assert audit.timestamp == expected_timestamp
        expected_created = datetime.fromtimestamp(
            response_json["entityAudits"][0]["created"] / 1000, tz=timezone.utc
        )
        assert audit.created == expected_created
        assert audit.user == response_json["entityAudits"][0]["user"]
        assert audit.action == response_json["entityAudits"][0]["action"]

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
        sort=[],
        size=1,
        from_=0,
    )
    audit_search_request = AuditSearchRequest(dsl=dsl)
    response = client.search(criteria=audit_search_request, bulk=False)

    assert response and response.aggregations
    assert audit_search_paging_json["aggregations"] == response.aggregations
    expected_sorts = [SortItem(field="entityId", order=SortOrder.ASCENDING)]

    _assert_audit_search_results(response, audit_search_paging_json, expected_sorts)
    assert mock_api_caller._call_api.call_count == 3
    assert mock_logger.call_count == 0
    mock_api_caller.reset_mock()

    # Test bulk pagination
    mock_api_caller._call_api.side_effect = [
        audit_search_paging_json,
        audit_search_paging_json,
        {},
    ]
    audit_search_request = AuditSearchRequest(dsl=dsl)
    response = client.search(criteria=audit_search_request, bulk=True)
    expected_sorts = [
        SortItem(field="created", order=SortOrder.ASCENDING),
        SortItem(field="entityId", order=SortOrder.ASCENDING),
    ]

    _assert_audit_search_results(
        response, audit_search_paging_json, expected_sorts, bulk=True
    )
    # The call count will be 2 because
    # audit search entries are processed in the first API call.
    # In the second API call, self._entity_audits
    # becomes 0, which breaks the pagination.
    # This differs from offset-based pagination
    # where an additional API call is needed
    # to verify if the results are empty
    assert mock_api_caller._call_api.call_count == 2
    assert mock_logger.call_count == 1
    assert "Audit bulk search option is enabled." in mock_logger.call_args_list[0][0][0]
    mock_logger.reset_mock()
    mock_api_caller.reset_mock()

    # Test automatic bulk search conversion when exceeding threshold
    with patch.object(AuditSearchResults, "_MASS_EXTRACT_THRESHOLD", -1):
        mock_api_caller._call_api.side_effect = [
            # Extra call to re-fetch the first page
            # results with updated timestamp sorting
            audit_search_paging_json,
            audit_search_paging_json,
            audit_search_paging_json,
            {},
        ]
        audit_search_request = AuditSearchRequest(dsl=dsl)
        response = client.search(criteria=audit_search_request)
        _assert_audit_search_results(
            response, audit_search_paging_json, expected_sorts, bulk=False
        )
        assert mock_logger.call_count == 1
        assert mock_api_caller._call_api.call_count == 3
        assert (
            "Result size (%s) exceeds threshold (%s)"
            in mock_logger.call_args_list[0][0][0]
        )

        # Test exception for bulk=False with user-defined sorting and results exceeds the predefined threshold
        dsl.sort = dsl.sort + [SortItem(field="some-sort1", order=SortOrder.ASCENDING)]
        audit_search_request = AuditSearchRequest(dsl=dsl)
        with pytest.raises(
            InvalidRequestError,
            match=(
                "ATLAN-PYTHON-400-066 Unable to execute "
                "audit bulk search with user-defined sorting options. "
                "Suggestion: Please ensure that no sorting options are "
                "included in your audit search request when performing a bulk search."
            ),
        ):
            client.search(criteria=audit_search_request, bulk=False)

        # Test exception for bulk=True with user-defined sorting
        dsl.sort = dsl.sort + [SortItem(field="some-sort2", order=SortOrder.ASCENDING)]
        audit_search_request = AuditSearchRequest(dsl=dsl)
        with pytest.raises(
            InvalidRequestError,
            match=(
                "ATLAN-PYTHON-400-066 Unable to execute "
                "audit bulk search with user-defined sorting options. "
                "Suggestion: Please ensure that no sorting options are "
                "included in your audit search request when performing a bulk search."
            ),
        ):
            client.search(criteria=audit_search_request, bulk=True)

    mock_logger.reset_mock()
    mock_api_caller.reset_mock()
