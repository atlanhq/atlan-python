from unittest.mock import patch

import pytest


@pytest.fixture()
def mock_role_cache():
    with patch("pyatlan.cache.role_cache.RoleCache") as cache:
        yield cache


@pytest.fixture()
def mock_user_cache():
    with patch("pyatlan.cache.user_cache.UserCache") as cache:
        yield cache


@pytest.fixture()
def mock_group_cache():
    with patch("pyatlan.cache.group_cache.GroupCache") as cache:
        yield cache


@pytest.fixture()
def mock_custom_metadata_cache():
    with patch("pyatlan.cache.custom_metadata_cache.CustomMetadataCache") as cache:
        yield cache


@pytest.fixture()
def mock_tag_cache():
    with patch("pyatlan.cache.atlan_tag_cache.AtlanTagCache") as cache:
        yield cache
