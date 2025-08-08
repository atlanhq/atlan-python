# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
"""
Async-specific test configuration and fixtures.
"""

import pytest
import pytest_asyncio

from pyatlan.client.aio.client import AsyncAtlanClient


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    """Set up environment variables for async tests."""
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest_asyncio.fixture
async def async_client():
    """Create an async client for testing."""
    async with AsyncAtlanClient() as client:
        yield client


@pytest.fixture()
def mock_async_client():
    """Create a mock async client for testing."""
    return AsyncAtlanClient()
