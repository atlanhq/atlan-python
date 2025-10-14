# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Tests for AsyncAtlanClient proxy and SSL configuration.
"""

from pathlib import Path
from unittest.mock import patch

import httpx
import pytest

from pyatlan.client.aio.client import AsyncAtlanClient


@pytest.mark.parametrize(
    "proxy_config",
    [
        # No proxy configuration (default)
        {},
        # Simple proxy
        {"proxy": "http://127.0.0.1:8080"},
        # Proxy with SSL verification disabled
        {"proxy": "http://127.0.0.1:8080", "verify": False},
    ],
)
def test_async_atlan_client_proxy_configurations(monkeypatch, proxy_config):
    """Test various proxy and SSL configurations are properly initialized for async client."""
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")

    # Clear any system proxy/SSL env vars that might interfere with tests
    for var in [
        "HTTP_PROXY",
        "http_proxy",
        "HTTPS_PROXY",
        "https_proxy",
        "SSL_CERT_FILE",
        "REQUESTS_CA_BUNDLE",
    ]:
        monkeypatch.delenv(var, raising=False)

    # Create async client with proxy settings
    client = AsyncAtlanClient(**proxy_config)

    # Verify the async session was created
    assert client._async_session is not None
    assert isinstance(client._async_session, httpx.AsyncClient)

    # Verify proxy is set correctly if provided
    if "proxy" in proxy_config:
        assert client.proxy == proxy_config["proxy"]
    else:
        assert client.proxy is None

    # Verify verify is set correctly if provided
    if "verify" in proxy_config:
        assert client.verify == proxy_config["verify"]
    else:
        assert client.verify is True  # Default value


def test_async_atlan_client_proxy_passed_to_transport(monkeypatch):
    """Test that proxy and verify settings are correctly configured on the async client."""
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")

    # Clear any proxy env vars that might interfere
    for var in [
        "HTTP_PROXY",
        "http_proxy",
        "HTTPS_PROXY",
        "https_proxy",
        "SSL_CERT_FILE",
        "REQUESTS_CA_BUNDLE",
    ]:
        monkeypatch.delenv(var, raising=False)

    # Test with proxy and verify=False (to disable SSL verification for testing)
    proxy_url = "http://127.0.0.1:8080"

    client = AsyncAtlanClient(proxy=proxy_url, verify=False)

    # Verify the client has the correct settings
    assert client.proxy == proxy_url
    assert client.verify is False

    # Verify the transport was created
    assert client._async_session is not None
    assert hasattr(client._async_session, "_transport")


@pytest.mark.parametrize(
    "env_vars, expected_proxy",
    [
        # HTTP_PROXY environment variable
        (
            {"HTTP_PROXY": "http://proxy.example.com:8080"},
            "http://proxy.example.com:8080",
        ),
        # http_proxy (lowercase) environment variable
        (
            {"http_proxy": "http://proxy.example.com:8080"},
            "http://proxy.example.com:8080",
        ),
        # HTTPS_PROXY takes precedence
        (
            {
                "HTTP_PROXY": "http://proxy.example.com:8080",
                "HTTPS_PROXY": "https://proxy.example.com:8443",
            },
            "https://proxy.example.com:8443",
        ),
    ],
)
@patch("httpx.AsyncClient")
def test_async_atlan_client_proxy_from_environment_variables(
    mock_async_httpx_client,
    monkeypatch,
    env_vars,
    expected_proxy,
):
    """Test that proxy settings are picked up from environment variables when not explicitly provided."""
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")

    # Clear any system proxy/SSL env vars that might interfere with tests
    for var in [
        "HTTP_PROXY",
        "http_proxy",
        "HTTPS_PROXY",
        "https_proxy",
        "SSL_CERT_FILE",
        "REQUESTS_CA_BUNDLE",
    ]:
        monkeypatch.delenv(var, raising=False)

    # Set environment variables
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)

    # Create async client without explicit proxy settings
    client = AsyncAtlanClient()

    # Verify proxy configuration
    assert client.proxy == expected_proxy


@patch("httpx_retries.transport.httpx.AsyncHTTPTransport")
@patch("httpx_retries.transport.httpx.HTTPTransport")
@patch("httpx.AsyncClient")
def test_async_atlan_client_proxy_with_ssl_cert_file_from_env(
    mock_async_httpx_client, mock_http_transport, mock_async_http_transport, monkeypatch
):
    """Test that SSL_CERT_FILE environment variable is picked up for async client."""
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")

    # Use the fake certificate file
    fake_cert_path = str(
        Path(__file__).parent.parent / "data" / "fake_certificates" / "fake-cert.pem"
    )
    monkeypatch.setenv("SSL_CERT_FILE", fake_cert_path)

    client = AsyncAtlanClient()

    # Verify SSL cert path was picked up
    assert client.verify == fake_cert_path


@patch("httpx_retries.transport.httpx.AsyncHTTPTransport")
@patch("httpx_retries.transport.httpx.HTTPTransport")
@patch("httpx.AsyncClient")
def test_async_atlan_client_explicit_args_override_env_vars(
    mock_async_httpx_client, mock_http_transport, mock_async_http_transport, monkeypatch
):
    """Test that explicitly provided arguments take precedence over environment variables for async client."""
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")

    # Use the fake certificate file
    fake_cert_path = str(
        Path(__file__).parent.parent / "data" / "fake_certificates" / "fake-cert.pem"
    )

    # Set environment variables
    monkeypatch.setenv("HTTP_PROXY", "http://env-proxy:8080")
    monkeypatch.setenv("SSL_CERT_FILE", fake_cert_path)

    # Explicitly provide different values
    explicit_proxy = "http://explicit-proxy:9090"
    explicit_verify = False

    client = AsyncAtlanClient(proxy=explicit_proxy, verify=explicit_verify)

    # Verify explicit values take precedence
    assert client.proxy == explicit_proxy
    assert client.verify == explicit_verify


def test_async_atlan_client_no_proxy_when_no_env_vars(monkeypatch):
    """Test that no proxy is configured when neither args nor env vars are provided for async client."""
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")

    # Ensure proxy env vars are not set
    for env_var in [
        "HTTP_PROXY",
        "http_proxy",
        "HTTPS_PROXY",
        "https_proxy",
        "SSL_CERT_FILE",
        "REQUESTS_CA_BUNDLE",
    ]:
        monkeypatch.delenv(env_var, raising=False)

    client = AsyncAtlanClient()

    assert client.proxy is None
    assert client.verify is True  # Default value
