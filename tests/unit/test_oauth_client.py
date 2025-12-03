# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Comprehensive Sync OAuth Client Tests

Tests for OAuth authentication in the synchronous AtlanClient:
- Authentication method precedence
- Environment variable handling
- Token lifecycle (fetch, cache, refresh, expiry)
- Error handling and edge cases
- Thread safety
- Resource cleanup
- URL construction
"""

import os
import threading
import time
from unittest.mock import Mock, patch
from urllib.parse import urlparse

import httpx
import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.client.oauth import OAuthTokenManager


@pytest.fixture
def clear_env_vars():
    """Clear OAuth-related environment variables before each test"""
    env_vars = [
        "ATLAN_BASE_URL",
        "ATLAN_API_KEY",
        "ATLAN_OAUTH_CLIENT_ID",
        "ATLAN_OAUTH_CLIENT_SECRET",
    ]
    original_values = {}
    for var in env_vars:
        original_values[var] = os.environ.get(var)
        if var in os.environ:
            del os.environ[var]

    yield

    for var, value in original_values.items():
        if value is not None:
            os.environ[var] = value
        elif var in os.environ:
            del os.environ[var]


@pytest.fixture
def mock_oauth_response():
    """Mock successful OAuth token response with camelCase"""
    return {
        "accessToken": "test-access-token-12345",
        "tokenType": "Bearer",
        "expiresIn": 600,
    }


@pytest.fixture
def mock_oauth_response_snake_case():
    """Mock successful OAuth token response with snake_case"""
    return {
        "access_token": "test-access-token-67890",
        "token_type": "Bearer",
        "expires_in": 600,
    }


class TestOAuthTokenManagerInit:
    """Test OAuth token manager initialization"""

    def test_init_with_external_url(self, clear_env_vars):
        """Initialize with external URL"""
        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        assert manager.base_url == "https://test.atlan.com"
        assert manager.client_id == "test-client-id"
        assert manager.client_secret == "test-client-secret"
        assert (
            manager.token_url
            == "https://test.atlan.com/api/service/oauth-clients/token"
        )
        assert manager._token is None
        assert manager._owns_client is True

        manager.close()

    def test_init_with_internal_url(self, clear_env_vars):
        """Initialize with INTERNAL mode"""
        manager = OAuthTokenManager(
            base_url="INTERNAL",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        assert manager.base_url == "INTERNAL"
        expected_url = (
            "http://heracles-service.heracles.svc.cluster.local/oauth-clients/token"
        )
        assert manager.token_url == expected_url

        manager.close()

    def test_init_with_external_http_client(self, clear_env_vars):
        """Initialize with externally provided HTTP client"""
        external_client = httpx.Client()

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
            http_client=external_client,
        )

        assert manager._http_client is external_client
        assert manager._owns_client is False

        manager.close()
        assert not external_client.is_closed
        external_client.close()

    def test_init_creates_http_client_when_not_provided(self, clear_env_vars):
        """Initialize without HTTP client should create one"""
        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        assert manager._http_client is not None
        assert isinstance(manager._http_client, httpx.Client)
        assert manager._owns_client is True

        manager.close()


class TestTokenFetchingAndCaching:
    """Test token fetching and caching behavior"""

    @patch("httpx.Client.post")
    def test_first_token_fetch(self, mock_post, clear_env_vars, mock_oauth_response):
        """First call should fetch token from API"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        token = manager.get_token()

        assert token == "test-access-token-12345"
        assert mock_post.call_count == 1

        call_args = mock_post.call_args
        assert call_args[1]["json"]["clientId"] == "test-client-id"
        assert call_args[1]["json"]["clientSecret"] == "test-client-secret"
        assert call_args[1]["headers"]["Content-Type"] == "application/json"

        manager.close()

    @patch("httpx.Client.post")
    def test_token_caching(self, mock_post, clear_env_vars, mock_oauth_response):
        """Subsequent calls should use cached token"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        token1 = manager.get_token()
        assert token1 == "test-access-token-12345"
        assert mock_post.call_count == 1

        token2 = manager.get_token()
        assert token2 == "test-access-token-12345"
        assert mock_post.call_count == 1

        token3 = manager.get_token()
        assert token3 == "test-access-token-12345"
        assert mock_post.call_count == 1

        manager.close()

    @patch("httpx.Client.post")
    def test_snake_case_response(
        self, mock_post, clear_env_vars, mock_oauth_response_snake_case
    ):
        """Should handle snake_case field names in response"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_response_snake_case
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        token = manager.get_token()
        assert token == "test-access-token-67890"

        manager.close()


class TestTokenExpiryAndRefresh:
    """Test token expiry detection and automatic refresh"""

    @patch("httpx.Client.post")
    def test_token_refresh_on_expiry(self, mock_post, clear_env_vars):
        """Expired token should trigger automatic refresh"""
        first_response = Mock()
        first_response.json.return_value = {
            "accessToken": "token-1",
            "tokenType": "Bearer",
            "expiresIn": 1,
        }
        first_response.raise_for_status = Mock()

        second_response = Mock()
        second_response.json.return_value = {
            "accessToken": "token-2",
            "tokenType": "Bearer",
            "expiresIn": 600,
        }
        second_response.raise_for_status = Mock()

        mock_post.side_effect = [first_response, second_response]

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        token1 = manager.get_token()
        assert token1 == "token-1"
        assert mock_post.call_count == 1

        time.sleep(2)

        token2 = manager.get_token()
        assert token2 == "token-2"
        assert mock_post.call_count == 2

        manager.close()

    @patch("httpx.Client.post")
    def test_manual_token_invalidation(
        self, mock_post, clear_env_vars, mock_oauth_response
    ):
        """Manual invalidation should force refresh on next call"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        manager.get_token()
        assert mock_post.call_count == 1

        manager.invalidate_token()
        assert manager._token is None

        manager.get_token()
        assert mock_post.call_count == 2

        manager.close()


class TestErrorHandling:
    """Test error handling in various failure scenarios"""

    @patch("httpx.Client.post")
    def test_missing_access_token(self, mock_post, clear_env_vars):
        """Missing accessToken should raise ValueError"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "tokenType": "Bearer",
            "expiresIn": 600,
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        with pytest.raises(
            ValueError, match="OAuth token response missing 'accessToken' field"
        ):
            manager.get_token()

        manager.close()

    @patch("httpx.Client.post")
    def test_http_401_error(self, mock_post, clear_env_vars):
        """401 error should be propagated"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "401 Unauthorized",
            request=Mock(),
            response=Mock(status_code=401),
        )
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        with pytest.raises(httpx.HTTPStatusError):
            manager.get_token()

        manager.close()

    @patch("httpx.Client.post")
    def test_http_500_error(self, mock_post, clear_env_vars):
        """500 error should be propagated"""
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "500 Internal Server Error",
            request=Mock(),
            response=Mock(status_code=500),
        )
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        with pytest.raises(httpx.HTTPStatusError):
            manager.get_token()

        manager.close()

    @patch("httpx.Client.post")
    def test_network_error(self, mock_post, clear_env_vars):
        """Network errors should be propagated"""
        mock_post.side_effect = httpx.ConnectError("Connection refused")

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        with pytest.raises(httpx.ConnectError):
            manager.get_token()

        manager.close()

    @patch("httpx.Client.post")
    def test_timeout_error(self, mock_post, clear_env_vars):
        """Timeout errors should be propagated"""
        mock_post.side_effect = httpx.TimeoutException("Request timeout")

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        with pytest.raises(httpx.TimeoutException):
            manager.get_token()

        manager.close()

    @patch("httpx.Client.post")
    def test_invalid_json_response(self, mock_post, clear_env_vars):
        """Invalid JSON in response should raise error"""
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        with pytest.raises(ValueError, match="Invalid JSON"):
            manager.get_token()

        manager.close()


class TestThreadSafety:
    """Test thread safety of OAuth token management"""

    @patch("httpx.Client.post")
    def test_concurrent_token_requests(
        self, mock_post, clear_env_vars, mock_oauth_response
    ):
        """Multiple threads requesting token simultaneously should result in single fetch"""
        call_count = {"count": 0}
        lock = threading.Lock()

        def mock_post_with_delay(*args, **kwargs):
            with lock:
                call_count["count"] += 1
            time.sleep(0.1)
            mock_response = Mock()
            mock_response.json.return_value = mock_oauth_response
            mock_response.raise_for_status = Mock()
            return mock_response

        mock_post.side_effect = mock_post_with_delay

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        tokens = []

        def get_token():
            token = manager.get_token()
            tokens.append(token)

        threads = [threading.Thread(target=get_token) for _ in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(tokens) == 10
        assert all(token == tokens[0] for token in tokens)

        assert call_count["count"] <= 2

        manager.close()

    @patch("httpx.Client.post")
    def test_concurrent_invalidation_and_fetch(
        self, mock_post, clear_env_vars, mock_oauth_response
    ):
        """Concurrent invalidation and fetch should be thread-safe"""
        mock_response = Mock()
        mock_response.json.return_value = mock_oauth_response
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        manager.get_token()

        def invalidate_repeatedly():
            for _ in range(5):
                manager.invalidate_token()
                time.sleep(0.01)

        def fetch_repeatedly():
            for _ in range(5):
                manager.get_token()
                time.sleep(0.01)

        threads = [
            threading.Thread(target=invalidate_repeatedly),
            threading.Thread(target=fetch_repeatedly),
            threading.Thread(target=fetch_repeatedly),
        ]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        manager.close()


class TestResourceCleanup:
    """Test proper cleanup of resources"""

    def test_close_http_client(self, clear_env_vars):
        """Close should close owned HTTP client"""
        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        http_client = manager._http_client
        assert not http_client.is_closed

        manager.close()
        assert http_client.is_closed

    def test_dont_close_external_client(self, clear_env_vars):
        """Should not close externally provided HTTP client"""
        external_client = httpx.Client()

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
            http_client=external_client,
        )

        manager.close()

        assert not external_client.is_closed

        external_client.close()


class TestAtlanClientAuthPrecedence:
    """Test authentication method precedence in AtlanClient"""

    def test_api_key_only(self, clear_env_vars):
        """API key authentication"""
        client = AtlanClient(
            base_url="https://test.atlan.com",
            api_key="test-api-key",
        )

        assert client.api_key == "test-api-key"
        assert client._oauth_token_manager is None
        assert "authorization" in client._request_params["headers"]
        assert (
            client._request_params["headers"]["authorization"] == "Bearer test-api-key"
        )

    def test_oauth_only(self, clear_env_vars):
        """OAuth authentication"""
        client = AtlanClient(
            base_url="https://test.atlan.com",
            oauth_client_id="test-client-id",
            oauth_client_secret="test-client-secret",
        )

        assert client.api_key is None
        assert client._oauth_token_manager is not None
        assert client._oauth_token_manager.client_id == "test-client-id"
        assert client._oauth_token_manager.client_secret == "test-client-secret"

        client._oauth_token_manager.close()

    def test_api_key_takes_precedence(self, clear_env_vars):
        """API key takes precedence when both provided"""
        client = AtlanClient(
            base_url="https://test.atlan.com",
            api_key="test-api-key",
            oauth_client_id="test-client-id",
            oauth_client_secret="test-client-secret",
        )

        assert client.api_key == "test-api-key"
        assert client._oauth_token_manager is None
        assert (
            client._request_params["headers"]["authorization"] == "Bearer test-api-key"
        )

    def test_empty_api_key(self, clear_env_vars):
        """Empty API key should not create OAuth manager"""
        client = AtlanClient(
            base_url="https://test.atlan.com",
            api_key="",
            oauth_client_id="test-client-id",
            oauth_client_secret="test-client-secret",
        )

        assert client.api_key == ""
        assert client._oauth_token_manager is None
        assert "authorization" not in client._request_params["headers"]

    def test_no_authentication(self, clear_env_vars):
        """No authentication provided"""
        client = AtlanClient(base_url="https://test.atlan.com")

        assert client.api_key is None
        assert client._oauth_token_manager is None
        assert "authorization" not in client._request_params["headers"]


class TestEnvironmentVariables:
    """Test environment variable handling"""

    def test_oauth_from_env(self, clear_env_vars):
        """OAuth credentials from environment variables"""
        os.environ["ATLAN_BASE_URL"] = "https://env.atlan.com"
        os.environ["ATLAN_OAUTH_CLIENT_ID"] = "env-client-id"
        os.environ["ATLAN_OAUTH_CLIENT_SECRET"] = "env-client-secret"

        client = AtlanClient()

        assert client._oauth_token_manager is not None
        assert client._oauth_token_manager.client_id == "env-client-id"
        assert client._oauth_token_manager.client_secret == "env-client-secret"

        client._oauth_token_manager.close()

    def test_explicit_overrides_env(self, clear_env_vars):
        """Explicit parameters override environment variables"""
        os.environ["ATLAN_BASE_URL"] = "https://env.atlan.com"
        os.environ["ATLAN_OAUTH_CLIENT_ID"] = "env-client-id"
        os.environ["ATLAN_OAUTH_CLIENT_SECRET"] = "env-client-secret"

        client = AtlanClient(
            base_url="https://explicit.atlan.com",
            oauth_client_id="explicit-client-id",
            oauth_client_secret="explicit-client-secret",
        )

        assert urlparse(str(client.base_url)).hostname == "explicit.atlan.com"
        assert client._oauth_token_manager.client_id == "explicit-client-id"
        assert client._oauth_token_manager.client_secret == "explicit-client-secret"

        client._oauth_token_manager.close()

    def test_api_key_env_precedence(self, clear_env_vars):
        """API key from env takes precedence over OAuth"""
        os.environ["ATLAN_BASE_URL"] = "https://test.atlan.com"
        os.environ["ATLAN_API_KEY"] = "env-api-key"
        os.environ["ATLAN_OAUTH_CLIENT_ID"] = "env-client-id"
        os.environ["ATLAN_OAUTH_CLIENT_SECRET"] = "env-client-secret"

        client = AtlanClient()

        assert client.api_key == "env-api-key"
        assert client._oauth_token_manager is None
        assert (
            client._request_params["headers"]["authorization"] == "Bearer env-api-key"
        )

    def test_partial_oauth_credentials(self, clear_env_vars):
        """Partial OAuth credentials should not create manager"""
        os.environ["ATLAN_BASE_URL"] = "https://test.atlan.com"
        os.environ["ATLAN_OAUTH_CLIENT_ID"] = "env-client-id"

        client = AtlanClient()

        assert client._oauth_token_manager is None


class TestEdgeCases:
    """Test edge cases and unusual scenarios"""

    @patch("httpx.Client.post")
    def test_default_expires_in(self, mock_post, clear_env_vars):
        """Missing expiresIn should use default"""
        mock_response = Mock()
        mock_response.json.return_value = {
            "accessToken": "test-token",
            "tokenType": "Bearer",
        }
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response

        manager = OAuthTokenManager(
            base_url="https://test.atlan.com",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        token = manager.get_token()
        assert token == "test-token"

        manager.close()

    def test_url_with_trailing_slash(self, clear_env_vars):
        """Base URL with trailing slash"""
        manager = OAuthTokenManager(
            base_url="https://test.atlan.com/",
            client_id="test-client-id",
            client_secret="test-client-secret",
        )

        assert "/api/service/oauth-clients/token" in manager.token_url

        manager.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
