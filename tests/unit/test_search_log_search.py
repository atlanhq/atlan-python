from datetime import datetime, timezone
from json import load
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

from pyatlan.client.common import ApiCaller
from pyatlan.client.search_log import LOGGER, SearchLogClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.enums import SortOrder
from pyatlan.model.search import SortItem
from pyatlan.model.search_log import SearchLogRequest, SearchLogResults

SEARCH_RESPONSES_DIR = Path(__file__).parent / "data" / "search_responses"
SEARCH_LOGS_JSON = "search_log_search_paging.json"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://name.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "abkj")


@pytest.fixture(scope="module")
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def search_logs_json():
    def load_json(filename):
        with (SEARCH_RESPONSES_DIR / filename).open() as input_file:
            return load(input_file)

    return load_json(SEARCH_LOGS_JSON)


def _assert_search_log_results(results, response_json, sorts, bulk=False):
    for log in results:
        assert log.user_name == response_json["logs"][0]["userName"]
        assert log.user_agent == response_json["logs"][0]["userAgent"]
        assert log.ip_address == response_json["logs"][0]["ipAddress"]
        assert log.host == response_json["logs"][0]["host"]
        expected_timestamp = datetime.fromtimestamp(
            response_json["logs"][0]["timestamp"] / 1000, tz=timezone.utc
        )
        assert log.timestamp == expected_timestamp
        assert log.entity_guids_all == response_json["logs"][0]["entityGuidsAll"]

    assert results.count == response_json["approximateCount"]
    assert results._bulk == bulk
    assert results._criteria.dsl.sort == sorts


@patch.object(LOGGER, "debug")
def test_search_log_pagination(mock_logger, mock_api_caller, search_logs_json):
    client = SearchLogClient(mock_api_caller)
    mock_api_caller._call_api.side_effect = [search_logs_json, {}]

    # Test default pagination
    search_log_request = SearchLogRequest.views_by_guid(
        guid="some-guid",
        size=2,
        exclude_users=["atlansupport"],
    )

    response = client.search(criteria=search_log_request, bulk=False)
    expected_sorts = [
        SortItem(field="timestamp", order=SortOrder.ASCENDING),
        SortItem(field="entityGuidsAll", order=SortOrder.ASCENDING),
    ]

    _assert_search_log_results(response, search_logs_json, expected_sorts)
    assert mock_api_caller._call_api.call_count == 2
    assert mock_logger.call_count == 0
    mock_api_caller._call_api.reset_mock()

    # Test bulk pagination
    mock_api_caller._call_api.side_effect = [search_logs_json, {}]
    response = client.search(criteria=search_log_request, bulk=True)
    expected_sorts = [
        SortItem(field="createdAt", order=SortOrder.ASCENDING),
        SortItem(field="entityGuidsAll", order=SortOrder.ASCENDING),
    ]

    _assert_search_log_results(response, search_logs_json, expected_sorts, bulk=True)
    # The call count will be 2 because both
    # log entries are processed in the first API call.
    # In the second API call, self._log_entries
    # becomes 0, which breaks the pagination.
    # This differs from offset-based pagination
    # where an additional API call is needed
    # to verify if the results are empty
    assert mock_api_caller._call_api.call_count == 2
    assert mock_logger.call_count == 1
    assert (
        "Search log bulk search option is enabled."
        in mock_logger.call_args_list[0][0][0]
    )
    mock_logger.reset_mock()
    mock_api_caller._call_api.reset_mock()

    # Test automatic bulk search conversion when exceeding threshold
    with patch.object(SearchLogResults, "_MASS_EXTRACT_THRESHOLD", -1):
        mock_api_caller._call_api.side_effect = [
            # Extra call to re-fetch the first page
            # results with updated timestamp sorting
            search_logs_json,
            search_logs_json,
            {},
        ]
        search_log_request = SearchLogRequest.views_by_guid(  #
            guid="some-guid",
            size=1,
            exclude_users=["atlansupport"],
        )
        response = client.search(criteria=search_log_request)
        _assert_search_log_results(
            response, search_logs_json, expected_sorts, bulk=False
        )
        assert mock_logger.call_count == 1
        assert mock_api_caller._call_api.call_count == 3
        assert (
            "Result size (%s) exceeds threshold (%s)"
            in mock_logger.call_args_list[0][0][0]
        )
    mock_logger.reset_mock()
    mock_api_caller._call_api.reset_mock()

    with patch.object(SearchLogResults, "_MASS_EXTRACT_THRESHOLD", -1):
        mock_api_caller._call_api.side_effect = [search_logs_json]
        # Test exception for bulk=False with user-defined sorting and results exceeding the threshold
        search_log_request = SearchLogRequest.views_by_guid(
            guid="some-guid",
            size=1,
            sort=[SortItem(field="some-sort1", order=SortOrder.ASCENDING)],
            exclude_users=["atlansupport"],
        )
        with pytest.raises(
            InvalidRequestError,
            match=(
                "ATLAN-PYTHON-400-067 Unable to execute "
                "search log bulk search with user-defined sorting options. "
                "Suggestion: Please ensure that no sorting options are "
                "included in your search log search request when performing a bulk search."
            ),
        ):
            client.search(criteria=search_log_request, bulk=False)
            assert mock_api_caller._call_api.call_count == 1

    mock_logger.reset_mock()
    mock_api_caller._call_api.reset_mock()
    # Test exception for bulk=True with user-defined sorting
    search_log_request = SearchLogRequest.views_by_guid(
        guid="some-guid",
        size=1,
        sort=[SortItem(field="some-sort2", order=SortOrder.ASCENDING)],
        exclude_users=["atlansupport"],
    )
    with pytest.raises(
        InvalidRequestError,
        match=(
            "ATLAN-PYTHON-400-067 Unable to execute "
            "search log bulk search with user-defined sorting options. "
            "Suggestion: Please ensure that no sorting options are "
            "included in your search log search request when performing a bulk search."
        ),
    ):
        client.search(criteria=search_log_request, bulk=True)
        assert mock_api_caller._call_api.call_count == 0

    mock_logger.reset_mock()
    mock_api_caller._call_api.reset_mock()
