# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""
PyTest configuration and fixtures for pyatlan_v9 unit tests.
These fixtures provide test utilities for msgspec-based models.
"""

from json import load
from pathlib import Path
from unittest.mock import patch

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan_v9.model.serde import Serde, get_serde

# Use the same test data directory as the original tests
TEST_DATA_DIR = Path(__file__).parent.parent.parent / "tests" / "unit" / "data"


@pytest.fixture()
def serde():
    """Provides a Serde instance for msgspec serialization/deserialization."""
    return Serde()


@pytest.fixture()
def shared_serde():
    """Provides the shared singleton Serde instance."""
    return get_serde()


def load_json(responses_dir: Path, filename: str):
    """Load JSON test data from file."""
    with (responses_dir / filename).open() as input_file:
        return load(input_file)


@pytest.fixture()
def mock_role_cache():
    """Mock the role cache on AtlanClient for validation testing."""
    with patch.object(AtlanClient, "role_cache") as cache:
        yield cache


@pytest.fixture()
def mock_user_cache():
    """Mock the user cache on AtlanClient for validation testing."""
    with patch.object(AtlanClient, "user_cache") as cache:
        yield cache


@pytest.fixture()
def mock_group_cache():
    """Mock the group cache on AtlanClient for validation testing."""
    with patch.object(AtlanClient, "group_cache") as cache:
        yield cache


@pytest.fixture()
def mock_custom_metadata_cache():
    """Mock the custom metadata cache on AtlanClient for badge testing."""
    with patch.object(AtlanClient, "custom_metadata_cache") as cache:
        yield cache


@pytest.fixture()
def mock_tag_cache():
    """Mock the atlan tag cache on AtlanClient for event testing."""
    with patch.object(AtlanClient, "atlan_tag_cache") as cache:
        yield cache


@pytest.fixture(autouse=True)
def patch_vcr_http_response_version_string():
    """
    Patch the VCRHTTPResponse class to add a version_string attribute if it doesn't exist.

    This patch is necessary to avoid bumping vcrpy to 7.0.0,
    which drops support for Python 3.8.
    """
    from vcr.stubs import VCRHTTPResponse  # type: ignore[import-untyped]

    if not hasattr(VCRHTTPResponse, "version_string"):
        VCRHTTPResponse.version_string = None


@pytest.fixture()
def glossary_json():
    """Load glossary test data."""
    return load_json(TEST_DATA_DIR, "glossary.json")


@pytest.fixture()
def glossary_term_json():
    """Load glossary term test data."""
    return load_json(TEST_DATA_DIR, "glossary_term.json")


@pytest.fixture()
def glossary_category_json():
    """Load glossary category test data."""
    return load_json(TEST_DATA_DIR, "glossary_category.json")
