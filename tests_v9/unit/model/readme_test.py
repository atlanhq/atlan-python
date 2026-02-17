# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for Readme model in pyatlan_v9."""

import pytest

from pyatlan_v9.model import Readme, Table
from tests_v9.unit.model.constants import SCHEMA_QUALIFIED_NAME, TABLE_NAME

README_NAME = f"{TABLE_NAME}/readme"
README_QUALIFIED_NAME = "2f8d68d2-8cd7-41e0-9d3b-cf27cd30f7ef/readme"


@pytest.mark.parametrize(
    "asset, content, asset_name, error, message",
    [
        (None, "stuff", None, ValueError, "asset is required"),
        (
            Table.creator(
                name=TABLE_NAME,
                schema_qualified_name=SCHEMA_QUALIFIED_NAME,
            ),
            None,
            None,
            ValueError,
            "content is required",
        ),
        (
            Table(),
            "stuff",
            None,
            ValueError,
            "asset_name is required when name is not available from asset",
        ),
    ],
)
def test_creator_without_required_parameters_raises_exception(
    asset, content, asset_name, error, message
):
    """Test creator validation for required asset and content fields."""
    with pytest.raises(error, match=message):
        Readme.creator(asset=asset, content=content, asset_name=asset_name)


@pytest.mark.parametrize(
    "asset, content, asset_name, expected_name",
    [
        (
            Table.creator(
                name=TABLE_NAME,
                schema_qualified_name=SCHEMA_QUALIFIED_NAME,
            ),
            "<h1>stuff</h1>",
            None,
            TABLE_NAME,
        ),
        (
            Table(),
            "<h1>stuff</h1>",
            TABLE_NAME,
            TABLE_NAME,
        ),
    ],
)
def test_creator(asset, content, asset_name, expected_name):
    """Test creator builds readme name, relationship, and content correctly."""
    asset.guid = "test-guid-123"
    readme = Readme.creator(asset=asset, content=content, asset_name=asset_name)
    assert readme.qualified_name == f"{asset.guid}/readme"
    assert readme.name == f"{expected_name} Readme"
    assert readme.asset.guid == asset.guid
    assert readme.description == content


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, README_QUALIFIED_NAME, "qualified_name is required"),
        (README_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        Readme.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater returns minimal update payload for Readme."""
    sut = Readme.updater(qualified_name=README_QUALIFIED_NAME, name=README_NAME)

    assert sut.qualified_name == README_QUALIFIED_NAME
    assert sut.name == README_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only required fields."""
    sut = Readme.updater(
        qualified_name=README_QUALIFIED_NAME, name=README_NAME
    ).trim_to_required()

    assert sut.qualified_name == README_QUALIFIED_NAME
    assert sut.name == README_NAME
