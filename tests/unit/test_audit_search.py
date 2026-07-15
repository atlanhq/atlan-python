from datetime import datetime, timezone
from json import load
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pyatlan.client.audit import AuditClient
from pyatlan.client.common import ApiCaller
from pyatlan.client.common.audit import LOGGER
from pyatlan.errors import InvalidRequestError
from pyatlan.model.audit import AuditSearchRequest, AuditSearchResults
from pyatlan.model.enums import SortOrder
from pyatlan.model.fluent_search import DSL
from pyatlan.model.search import Bool, Range, SortItem, Term

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
    first = response_json["entityAudits"][0]
    for audit in results:
        assert audit.entity_id == first["entityId"]
        assert audit.entity_qualified_name == first["entityQualifiedName"]
        assert audit.type_name == first["typeName"]
        expected_timestamp = datetime.fromtimestamp(
            first["timestamp"] / 1000, tz=timezone.utc
        )
        assert audit.timestamp == expected_timestamp
        expected_created = datetime.fromtimestamp(
            first["created"] / 1000, tz=timezone.utc
        )
        assert audit.created == expected_created
        assert audit.user == first["user"]
        assert audit.action == first["action"]

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


# --- BLDX-1549: bulk AuditSearch must not blow past ES max_result_window ------
def _bulk_results_in_collapse_state(processed=10500, count_at_max_ts=7):
    """An AuditSearchResults mid-bulk-scan whose latest page collapsed to a
    single `created` timestamp (first == last) after >10k audits processed —
    the exact state that triggered the offset fallback in prod."""
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value="some-guid")]),
        sort=[],
        size=300,
        from_=0,
    )
    criteria = AuditSearchRequest(dsl=dsl)
    results = AuditSearchResults(
        client=Mock(spec=ApiCaller),
        criteria=criteria,
        start=0,
        size=300,
        entity_audits=[],
        count=50000,
        bulk=True,
    )
    results._processed_entity_keys = {f"k{i}" for i in range(processed)}
    results._max_processed_ts = datetime(2026, 7, 1, tzinfo=timezone.utc)
    results._count_at_max_ts = count_at_max_ts
    # A page netting <= 1 new record after dedup leaves first == last (sentinel).
    results._first_record_creation_time = results._last_record_creation_time = -2
    return results, criteria


def _gte_created_filters(query):
    return [
        f
        for f in query.filter
        if isinstance(f, Range) and f.field == "created" and f.gte is not None
    ]


def test_bulk_offset_fallback_is_bounded_within_timestamp_bucket():
    """BLDX-1549: with >10k audits processed, the timestamp-paging offset
    fallback must offset WITHIN the current timestamp bucket (bounded), keeping
    the timestamp filter — never `len(processed)` over the whole result set,
    which pushed from_ + size past ES's 10,000 max_result_window and crashed with
    'Result window is too large ... [43504]'."""
    results, criteria = _bulk_results_in_collapse_state(
        processed=10500, count_at_max_ts=7
    )

    results._prepare_query_for_timestamp_paging(criteria.dsl.query)

    # offset is the per-timestamp count, NOT the whole processed set (the old bug)
    assert criteria.dsl.from_ == 7
    assert criteria.dsl.from_ != 10500
    # and it stays within the ES result window
    assert criteria.dsl.from_ + criteria.dsl.size <= 10000
    # the timestamp filter is retained, pinned to the max processed timestamp
    gte = _gte_created_filters(criteria.dsl.query)
    assert len(gte) == 1
    assert gte[0].gte == results._max_processed_ts


def test_bulk_paging_advances_window_on_distinct_timestamps():
    """Fast path unchanged: a page spanning multiple timestamps advances the
    window (gte = last record's created) and resets the offset to 0."""
    results, criteria = _bulk_results_in_collapse_state()
    t_last = datetime(2026, 7, 1, tzinfo=timezone.utc)
    results._first_record_creation_time = datetime(2026, 6, 30, tzinfo=timezone.utc)
    results._last_record_creation_time = t_last

    results._prepare_query_for_timestamp_paging(criteria.dsl.query)

    assert criteria.dsl.from_ == 0
    gte = _gte_created_filters(criteria.dsl.query)
    assert len(gte) == 1
    assert gte[0].gte == t_last
