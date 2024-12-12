from unittest.mock import patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.audit import LOGGER
from pyatlan.errors import InvalidRequestError
from pyatlan.model.audit import AuditSearchRequest
from pyatlan.model.search import DSL, Bool, SortItem, SortOrder, Term


def _assert_audit_search_results(results, expected_sorts, size, total_count):
    assert results.total_count > size
    assert len(results.current_page()) == size
    assert results.total_count == total_count
    assert results
    assert results._criteria.dsl.sort == expected_sorts


@patch.object(LOGGER, "debug")
def test_audit_search_pagination(mock_logger, client: AtlanClient):
    size = 2

    # Test audit search by GUID with default offset-based pagination
    guid = "2be6f58d-fd8a-44fe-a43e-f97b150cd1dd"
    dsl = DSL(
        query=Bool(filter=[Term(field="entityId", value=guid)]),
        sort=[],
        size=size,
    )
    request = AuditSearchRequest(dsl=dsl)
    results = client.audit.search(criteria=request)
    total_count = results.total_count
    expected_sorts = [SortItem(field="entityId", order=SortOrder.ASCENDING)]
    _assert_audit_search_results(results, expected_sorts, size, total_count)

    # Test audit search by guid with `bulk` option using timestamp-based pagination
    results = client.audit.search(criteria=request, bulk=True)
    total_count = results.total_count
    expected_sorts = [
        SortItem("created", order=SortOrder.ASCENDING),
        SortItem(field="entityId", order=SortOrder.ASCENDING),
    ]
    _assert_audit_search_results(results, expected_sorts, size, total_count)
    assert mock_logger.call_count == 1
    assert "Audit bulk search option is enabled." in mock_logger.call_args_list[0][0][0]
    mock_logger.reset_mock()

    # When the number of results exceeds the predefined threshold and bulk is false and no pre-defined sort.
    # Then SDK automatically switches to a `bulk` search option using timestamp-based pagination
    username = (
        client.user.get_current().username or "default_username"
    )  # Expected to have more than 10,000
    dsl = DSL(
        query=Bool(filter=[Term(field="user", value=username)]),
        sort=[],
        size=size,
    )
    request = AuditSearchRequest(dsl=dsl)
    results = client.audit.search(criteria=request)
    total_count = results.total_count
    expected_sorts = [
        SortItem("created", order=SortOrder.ASCENDING),
        SortItem(field="entityId", order=SortOrder.ASCENDING),
    ]
    _assert_audit_search_results(results, expected_sorts, size, total_count)
    assert mock_logger.call_count < total_count
    assert (
        "Result size (%s) exceeds threshold (%s)."
        in mock_logger.call_args_list[0][0][0]
    )
    mock_logger.reset_mock()

    # When the number of results exceeds the predefined threshold and bulk is true and no pre-defined sort.
    request = AuditSearchRequest(dsl=dsl)
    results = client.audit.search(criteria=request, bulk=True)
    total_count = results.total_count
    expected_sorts = [
        SortItem("created", order=SortOrder.ASCENDING),
        SortItem(field="entityId", order=SortOrder.ASCENDING),
    ]
    _assert_audit_search_results(results, expected_sorts, size, total_count)
    assert mock_logger.call_count < total_count
    assert "Audit bulk search option is enabled." in mock_logger.call_args_list[0][0][0]
    mock_logger.reset_mock()

    # When the number of results exceeds the predefined threshold and bulk is false and no pre-defined sort.
    username = (
        client.user.get_current().username or "default_username"
    )  # Expected to have more than 10,000
    dsl = DSL(
        query=Bool(filter=[Term(field="user", value=username)]),
        sort=[SortItem(field="timestamp", order=SortOrder.ASCENDING)],
        size=size,
    )
    request = AuditSearchRequest(dsl=dsl)
    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-066 Unable to execute "
            "audit bulk search with user-defined sorting options. "
            "Suggestion: Please ensure that no sorting options are "
            "included in your search request when performing a bulk search."
        ),
    ):
        client.audit.search(criteria=request)

    # When the number of results exceeds the predefined threshold and bulk is true and no pre-defined sort.
    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-066 Unable to execute "
            "audit bulk search with user-defined sorting options. "
            "Suggestion: Please ensure that no sorting options are "
            "included in your search request when performing a bulk search."
        ),
    ):
        client.audit.search(criteria=request, bulk=True)
