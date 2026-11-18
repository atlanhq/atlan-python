from unittest.mock import Mock

import pytest

from pyatlan.client.asset import IndexSearchResults
from pyatlan.client.common.asset import Search
from pyatlan.model.search import DSL, IndexSearchRequest, Term
from pyatlan_v9.model.search import IndexSearchRequest as V9IndexSearchRequest


def _request(cls=IndexSearchRequest):
    return cls(dsl=DSL(query=Term(field="__typeName.keyword", value="Table")))


@pytest.mark.parametrize(
    "value, expected",
    [(None, False), ("true", True), (" TRUE ", True), ("false", False), ("1", False)],
)
@pytest.mark.parametrize("cls", [IndexSearchRequest, V9IndexSearchRequest])
def test_default_follows_env(monkeypatch, cls, value, expected):
    if value is None:
        monkeypatch.delenv("ATLAN_SAVE_SEARCH_LOG", raising=False)
    else:
        monkeypatch.setenv("ATLAN_SAVE_SEARCH_LOG", value)
    assert _request(cls).request_metadata.save_search_log is expected


def test_explicit_request_metadata_wins_over_env(monkeypatch):
    monkeypatch.setenv("ATLAN_SAVE_SEARCH_LOG", "true")
    request = _request()
    request.request_metadata.save_search_log = False
    assert '"saveSearchLog": false' in request.json(by_alias=True)


def test_later_pages_are_not_logged(monkeypatch):
    monkeypatch.setenv("ATLAN_SAVE_SEARCH_LOG", "true")
    request = _request()
    client = Mock()
    client._call_api.return_value = {"entities": []}
    results = IndexSearchResults(
        client=client,
        criteria=request,
        start=0,
        size=10,
        count=20,
        assets=[],
        aggregations=None,
    )
    assert request.request_metadata.save_search_log is True

    results._get_next_page_json()

    sent = client._call_api.call_args.kwargs["request_obj"]
    assert sent.request_metadata.save_search_log is False


def test_bulk_refetch_of_first_page_is_not_logged(monkeypatch):
    monkeypatch.setenv("ATLAN_SAVE_SEARCH_LOG", "true")
    request = _request()

    refetch = Search._check_for_bulk_search(
        request, IndexSearchResults._MASS_EXTRACT_THRESHOLD + 1
    )

    assert refetch is True
    assert request.request_metadata.save_search_log is False
