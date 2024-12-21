from datetime import datetime, timezone
from json import load
from pathlib import Path
from unittest.mock import Mock, patch

import pytest

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
    return Mock()


@pytest.fixture()
def search_logs_json():
    def load_json(filename):
        with (SEARCH_RESPONSES_DIR / filename).open() as input_file:
            return load(input_file)

    return load_json(SEARCH_LOGS_JSON)


def _assert_search_log_results(results, response_json, sorts, bulk=False):
    for i, log in enumerate(results.current_page()):
        assert log.user_name == response_json["logs"][i]["userName"]
        assert log.user_agent == response_json["logs"][i]["userAgent"]
        assert log.ip_address == response_json["logs"][i]["ipAddress"]
        assert log.host == response_json["logs"][i]["host"]
        expected_timestamp = datetime.fromtimestamp(
            response_json["logs"][i]["timestamp"] / 1000, tz=timezone.utc
        )
        assert log.timestamp == expected_timestamp
        assert log.entity_guids_all == response_json["logs"][i]["entityGuidsAll"]

    assert results.count == response_json["approximateCount"]
    assert results._bulk == bulk
    assert results._criteria.dsl.sort == sorts


@patch.object(LOGGER, "debug")
def test_search_log_pagination(mock_logger, mock_api_caller, search_logs_json):
    client = SearchLogClient(mock_api_caller)
    mock_api_caller._call_api.side_effect = [search_logs_json, search_logs_json, {}]

    # Test default pagination
    search_log_request = SearchLogRequest.views_by_guid(  #
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
    assert mock_api_caller._call_api.call_count == 1
    mock_logger.reset_mock()
    mock_api_caller.reset_mock()

    # Test bulk pagination
    response = client.search(criteria=search_log_request, bulk=True)
    expected_sorts = [
        SortItem(field="createdAt", order=SortOrder.ASCENDING),
        SortItem(field="entityGuidsAll", order=SortOrder.ASCENDING),
    ]

    _assert_search_log_results(response, search_logs_json, expected_sorts, bulk=True)
    assert mock_logger.call_count == 1
    assert (
        "Search log bulk search option is enabled."
        in mock_logger.call_args_list[0][0][0]
    )
    mock_logger.reset_mock()
    mock_api_caller.reset_mock()

    # Test automatic bulk search conversion when exceeding threshold
    with patch.object(SearchLogResults, "_MASS_EXTRACT_THRESHOLD", -1):
        mock_api_caller._call_api.side_effect = [
            search_logs_json,
            search_logs_json,
            {},
        ]
        search_log_request = SearchLogRequest.views_by_guid(  #
            guid="some-guid",
            size=2,
            exclude_users=["atlansupport"],
        )
        response = client.search(criteria=search_log_request)
        _assert_search_log_results(
            response, search_logs_json, expected_sorts, bulk=False
        )
        assert mock_logger.call_count == 1
        assert (
            "Result size (%s) exceeds threshold (%s)"
            in mock_logger.call_args_list[0][0][0]
        )

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

    mock_logger.reset_mock()
    mock_api_caller.reset_mock()
