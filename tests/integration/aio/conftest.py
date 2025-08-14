# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.

"""Conftest for async integration tests."""

import pytest_asyncio

from pyatlan.client.aio import AsyncAtlanClient


@pytest_asyncio.fixture(scope="module")
async def client():
    """Async Atlan client fixture for integration tests."""
    client = AsyncAtlanClient()
    yield client
