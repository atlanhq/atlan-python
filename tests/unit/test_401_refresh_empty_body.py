# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""A 401 must trigger the token refresh whether or not its body is JSON."""

from unittest.mock import Mock, patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.constants import DELETE_ENTITY_BY_GUID


@pytest.fixture()
def client(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")
    return AtlanClient()


@pytest.mark.parametrize("body", ["", "<html>unauthorized</html>"])
def test_401_with_non_json_body_refreshes_token_and_retries(client, body):
    first = Mock(status_code=401, text=body, content=body.encode())
    second = Mock(status_code=200, text="", content=b"")
    token_manager = Mock()
    token_manager.get_token.return_value = "fresh-token"
    client._oauth_token_manager = token_manager

    with patch.object(
        client._session, "request", side_effect=[first, second]
    ) as request:
        result = client._call_api(DELETE_ENTITY_BY_GUID.format_path_with_params("g"))

    token_manager.invalidate_token.assert_called_once()
    assert request.call_count == 2
    assert result is None
