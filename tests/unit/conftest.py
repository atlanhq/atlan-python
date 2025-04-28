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

    yield
