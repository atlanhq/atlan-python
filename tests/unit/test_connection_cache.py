# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.
from unittest.mock import Mock, patch

import pytest

from pyatlan.cache.connection_cache import ConnectionCache, ConnectionName
from pyatlan.client.atlan import AtlanClient
from pyatlan.errors import ErrorCode, InvalidRequestError, NotFoundError
from pyatlan.model.assets import Connection


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


def test_get_by_guid_with_not_found_error(monkeypatch):
    with pytest.raises(InvalidRequestError, match=ErrorCode.MISSING_ID.error_message):
        ConnectionCache.get_by_guid("")


@patch.object(ConnectionCache, "lookup_by_guid")
@patch.object(
    ConnectionCache, "get_cache", return_value=ConnectionCache(client=AtlanClient())
)
def test_get_by_guid_with_no_invalid_request_error(mock_get_cache, mock_lookup_by_guid):
    test_guid = "test-guid-123"
    with pytest.raises(
        NotFoundError,
        match=ErrorCode.ASSET_NOT_FOUND_BY_GUID.error_message.format(test_guid),
    ):
        ConnectionCache.get_by_guid(test_guid)
    mock_get_cache.assert_called_once()


def test_get_by_qualified_name_with_not_found_error(monkeypatch):
    with pytest.raises(InvalidRequestError, match=ErrorCode.MISSING_ID.error_message):
        ConnectionCache.get_by_qualified_name("")


@patch.object(ConnectionCache, "lookup_by_qualified_name")
@patch.object(
    ConnectionCache, "get_cache", return_value=ConnectionCache(client=AtlanClient())
)
def test_get_by_qualified_name_with_no_invalid_request_error(
    mock_get_cache, mock_lookup_by_qualified_name
):
    test_qn = "default/snowflake/123456789"
    test_connector = "snowflake"
    with pytest.raises(
        NotFoundError,
        match=ErrorCode.ASSET_NOT_FOUND_BY_QN.error_message.format(
            test_qn, test_connector
        ),
    ):
        ConnectionCache.get_by_qualified_name(test_qn)
    mock_get_cache.assert_called_once()


def test_get_by_name_with_not_found_error(monkeypatch):
    with pytest.raises(InvalidRequestError, match=ErrorCode.MISSING_NAME.error_message):
        ConnectionCache.get_by_name("")


@patch.object(ConnectionCache, "lookup_by_name")
@patch.object(
    ConnectionCache, "get_cache", return_value=ConnectionCache(client=AtlanClient())
)
def test_get_by_name_with_no_invalid_request_error(mock_get_cache, mock_lookup_by_name):
    test_name = ConnectionName("snowflake/test")
    with pytest.raises(
        NotFoundError,
        match=ErrorCode.ASSET_NOT_FOUND_BY_NAME.error_message.format(
            ConnectionName._TYPE_NAME,
            test_name,
        ),
    ):
        ConnectionCache.get_by_name(test_name)
    mock_get_cache.assert_called_once()


@patch.object(ConnectionCache, "lookup_by_guid")
@patch.object(
    ConnectionCache, "get_cache", return_value=ConnectionCache(client=AtlanClient())
)
def test_get_by_guid(mock_get_cache, mock_lookup_by_guid):
    test_guid = "test-guid-123"
    test_qn = "test-qualified-name"
    conn = Connection()
    conn.guid = test_guid
    conn.qualified_name = test_qn
    test_asset = conn

    mock_guid_to_asset = Mock()
    mock_name_to_guid = Mock()
    mock_qualified_name_to_guid = Mock()

    # 1 - Not found in the cache, triggers a lookup call
    # 2, 3, 4 - Uses the cached entry from the map
    mock_guid_to_asset.get.side_effect = [
        None,
        test_asset,
        test_asset,
        test_asset,
    ]
    mock_name_to_guid.get.side_effect = [test_guid, test_guid, test_guid, test_guid]
    mock_qualified_name_to_guid.get.side_effect = [
        test_guid,
        test_guid,
        test_guid,
        test_guid,
    ]

    # Assign mock caches to the return value of get_cache
    mock_get_cache.return_value.guid_to_asset = mock_guid_to_asset
    mock_get_cache.return_value.name_to_guid = mock_name_to_guid
    mock_get_cache.return_value.qualified_name_to_guid = mock_qualified_name_to_guid

    connection = ConnectionCache.get_by_guid(test_guid)

    # Multiple calls with the same GUID result in no additional API lookups
    # as the object is already cached
    connection = ConnectionCache.get_by_guid(test_guid)
    connection = ConnectionCache.get_by_guid(test_guid)

    assert test_guid == connection.guid
    assert test_qn == connection.qualified_name

    # The method is called three times, but the lookup is triggered only once
    assert mock_get_cache.call_count == 3
    mock_lookup_by_guid.assert_called_once()


@patch.object(ConnectionCache, "lookup_by_guid")
@patch.object(ConnectionCache, "lookup_by_qualified_name")
@patch.object(
    ConnectionCache, "get_cache", return_value=ConnectionCache(client=AtlanClient())
)
def test_get_by_qualified_name(mock_get_cache, mock_lookup_by_qn, mock_lookup_by_guid):
    test_guid = "test-guid-123"
    test_qn = "test-qualified-name"
    conn = Connection()
    conn.guid = test_guid
    conn.qualified_name = test_qn
    test_asset = conn

    mock_guid_to_asset = Mock()
    mock_name_to_guid = Mock()
    mock_qualified_name_to_guid = Mock()

    # 1 - Not found in the cache, triggers a lookup call
    # 2, 3, 4 - Uses the cached entry from the map
    mock_qualified_name_to_guid.get.side_effect = [
        None,
        test_guid,
        test_guid,
        test_guid,
    ]

    # Other caches will be populated once
    # the lookup call for get_by_qualified_name is made
    mock_guid_to_asset.get.side_effect = [
        test_asset,
        test_asset,
        test_asset,
        test_asset,
    ]
    mock_name_to_guid.get.side_effect = [test_guid, test_guid, test_guid, test_guid]

    mock_get_cache.return_value.guid_to_asset = mock_guid_to_asset
    mock_get_cache.return_value.name_to_guid = mock_name_to_guid
    mock_get_cache.return_value.qualified_name_to_guid = mock_qualified_name_to_guid

    connection = ConnectionCache.get_by_qualified_name(test_qn)

    # Multiple calls with the same
    # qualified name result in no additional API lookups
    # as the object is already cached
    connection = ConnectionCache.get_by_qualified_name(test_qn)
    connection = ConnectionCache.get_by_qualified_name(test_qn)

    assert test_guid == connection.guid
    assert test_qn == connection.qualified_name

    # The method is called three times
    # but the lookup is triggered only once
    assert mock_get_cache.call_count == 3
    mock_lookup_by_qn.assert_called_once()

    # No call to guid lookup since the object is already in the cache
    assert mock_lookup_by_guid.call_count == 0


@patch.object(ConnectionCache, "lookup_by_guid")
@patch.object(ConnectionCache, "lookup_by_name")
@patch.object(
    ConnectionCache, "get_cache", return_value=ConnectionCache(client=AtlanClient())
)
def test_get_by_name(mock_get_cache, mock_lookup_by_name, mock_lookup_by_guid):
    test_name = ConnectionName("snowflake/test")
    test_guid = "test-guid-123"
    test_qn = "test-qualified-name"
    conn = Connection()
    conn.guid = test_guid
    conn.qualified_name = test_qn
    test_asset = conn

    mock_guid_to_asset = Mock()
    mock_name_to_guid = Mock()
    mock_qualified_name_to_guid = Mock()

    # 1 - Not found in the cache, triggers a lookup call
    # 2, 3, 4 - Uses the cached entry from the map
    mock_name_to_guid.get.side_effect = [
        None,
        test_guid,
        test_guid,
        test_guid,
    ]

    # Other caches will be populated once
    # the lookup call for get_by_qualified_name is made
    mock_guid_to_asset.get.side_effect = [
        test_asset,
        test_asset,
        test_asset,
        test_asset,
    ]
    mock_qualified_name_to_guid.get.side_effect = [
        test_guid,
        test_guid,
        test_guid,
        test_guid,
    ]

    mock_get_cache.return_value.guid_to_asset = mock_guid_to_asset
    mock_get_cache.return_value.name_to_guid = mock_name_to_guid
    mock_get_cache.return_value.qualified_name_to_guid = mock_qualified_name_to_guid

    connection = ConnectionCache.get_by_name(test_name)

    # Multiple calls with the same
    # qualified name result in no additional API lookups
    # as the object is already cached
    connection = ConnectionCache.get_by_name(test_name)
    connection = ConnectionCache.get_by_name(test_name)

    assert test_guid == connection.guid
    assert test_qn == connection.qualified_name

    # The method is called three times
    # but the lookup is triggered only once
    assert mock_get_cache.call_count == 3
    mock_lookup_by_name.assert_called_once()

    # No call to guid lookup since the object is already in the cache
    assert mock_lookup_by_guid.call_count == 0
