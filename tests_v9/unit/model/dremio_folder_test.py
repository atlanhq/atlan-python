# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for DremioFolder model in pyatlan_v9.

The parity tests use the exact qualifiedNames and linkage atlan-dremio-app emits
today (``{connection_qn}/{path joined by /}``, with the root Source or Space,
parent folder and folder hierarchy derived from the path), so a creator change
that would re-key existing folders fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import DremioFolder

CONNECTION_QUALIFIED_NAME = "default/dremio/1700000000"
SOURCE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/sales-lake"
SPACE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/analytics"
FOLDER_NAME = "raw"
FOLDER_QUALIFIED_NAME = f"{SOURCE_QUALIFIED_NAME}/{FOLDER_NAME}"


def test_creator_matches_app_qualified_name_for_nested_folder():
    """Mirror atlan-dremio-app for path ["sales-lake", "raw", "2024", "orders"]."""
    sut = DremioFolder.creator(
        name="orders",
        parent_qualified_name="default/dremio/1700000000/sales-lake/raw/2024",
        dremio_source_qualified_name="default/dremio/1700000000/sales-lake",
    )

    assert sut.qualified_name == "default/dremio/1700000000/sales-lake/raw/2024/orders"
    assert sut.connection_qualified_name == "default/dremio/1700000000"
    assert sut.dremio_parent_asset_type == "SOURCE"
    assert sut.dremio_source_qualified_name == "default/dremio/1700000000/sales-lake"
    assert sut.dremio_source_name == "sales-lake"
    assert (
        sut.dremio_parent_folder_qualified_name
        == "default/dremio/1700000000/sales-lake/raw/2024"
    )
    assert sut.dremio_folder_hierarchy == [
        {
            "qualifiedName": "default/dremio/1700000000/sales-lake/raw/2024",
            "name": "2024",
        },
        {"qualifiedName": "default/dremio/1700000000/sales-lake/raw", "name": "raw"},
    ]
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_for_space_folder():
    """Mirror atlan-dremio-app for path ["analytics", "marts"]."""
    sut = DremioFolder.creator(
        name="marts",
        parent_qualified_name="default/dremio/1700000000/analytics",
        dremio_space_qualified_name="default/dremio/1700000000/analytics",
    )

    assert sut.qualified_name == "default/dremio/1700000000/analytics/marts"
    assert sut.dremio_parent_asset_type == "SPACE"
    assert sut.dremio_space_qualified_name == "default/dremio/1700000000/analytics"
    assert sut.dremio_space_name == "analytics"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, parent_qualified_name, message",
    [
        (None, SOURCE_QUALIFIED_NAME, "name is required"),
        (" ", SOURCE_QUALIFIED_NAME, "name cannot be blank"),
        (FOLDER_NAME, None, "parent_qualified_name is required"),
        (FOLDER_NAME, " ", "parent_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, parent_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DremioFolder.creator(
            name=name,
            parent_qualified_name=parent_qualified_name,
            dremio_source_qualified_name=SOURCE_QUALIFIED_NAME,
        )


@pytest.mark.parametrize(
    "source_qualified_name, space_qualified_name",
    [
        (None, None),
        ("", ""),
        (SOURCE_QUALIFIED_NAME, SPACE_QUALIFIED_NAME),
    ],
)
def test_creator_requires_exactly_one_root(
    source_qualified_name: str, space_qualified_name: str
):
    """Test creator needs exactly one of the root Source or Space."""
    with pytest.raises(ValueError, match="exactly one of"):
        DremioFolder.creator(
            name=FOLDER_NAME,
            parent_qualified_name=SOURCE_QUALIFIED_NAME,
            dremio_source_qualified_name=source_qualified_name,
            dremio_space_qualified_name=space_qualified_name,
        )


@pytest.mark.parametrize(
    "parent_qualified_name, source_qualified_name, space_qualified_name, message",
    [
        (
            SOURCE_QUALIFIED_NAME,
            "sales-lake",
            None,
            "dremio_source_qualified_name is invalid",
        ),
        (
            SPACE_QUALIFIED_NAME,
            None,
            "analytics",
            "dremio_space_qualified_name is invalid",
        ),
        (
            SPACE_QUALIFIED_NAME,
            SOURCE_QUALIFIED_NAME,
            None,
            "parent_qualified_name is invalid",
        ),
        (
            f"{SOURCE_QUALIFIED_NAME}-2/raw",
            SOURCE_QUALIFIED_NAME,
            None,
            "parent_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_invalid_qualified_names_raise_value_error(
    parent_qualified_name: str,
    source_qualified_name: str,
    space_qualified_name: str,
    message: str,
):
    """Test creator rejects a malformed root or a parent outside the root."""
    with pytest.raises(ValueError, match=message):
        DremioFolder.creator(
            name=FOLDER_NAME,
            parent_qualified_name=parent_qualified_name,
            dremio_source_qualified_name=source_qualified_name,
            dremio_space_qualified_name=space_qualified_name,
        )


def test_creator_under_source():
    """Test a top-level folder links its Source and has no parent folder."""
    sut = DremioFolder.creator(
        name=FOLDER_NAME,
        parent_qualified_name=SOURCE_QUALIFIED_NAME,
        dremio_source_qualified_name=SOURCE_QUALIFIED_NAME,
    )

    assert sut.name == FOLDER_NAME
    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "dremio"
    assert sut.dremio_source.unique_attributes == {
        "qualifiedName": SOURCE_QUALIFIED_NAME
    }
    assert not sut.dremio_space
    assert not sut.dremio_parent_folder
    assert not sut.dremio_parent_folder_qualified_name
    assert not sut.dremio_folder_hierarchy
    sut.validate(for_creation=True)


def test_creator_under_folder_in_space():
    """Test a nested folder links its Space and its parent folder."""
    parent_qualified_name = f"{SPACE_QUALIFIED_NAME}/marts"
    sut = DremioFolder.creator(
        name=FOLDER_NAME,
        parent_qualified_name=parent_qualified_name,
        dremio_space_qualified_name=SPACE_QUALIFIED_NAME,
    )

    assert sut.qualified_name == f"{parent_qualified_name}/{FOLDER_NAME}"
    assert sut.dremio_space.unique_attributes == {"qualifiedName": SPACE_QUALIFIED_NAME}
    assert not sut.dremio_source
    assert sut.dremio_parent_folder.unique_attributes == {
        "qualifiedName": parent_qualified_name
    }
    assert sut.dremio_folder_hierarchy == [
        {"qualifiedName": parent_qualified_name, "name": "marts"}
    ]
    sut.validate(for_creation=True)


def test_validate_for_creation_requires_a_root():
    """Test validate needs the folder to link its Source or Space."""
    sut = DremioFolder.creator(
        name=FOLDER_NAME,
        parent_qualified_name=SOURCE_QUALIFIED_NAME,
        dremio_source_qualified_name=SOURCE_QUALIFIED_NAME,
    )
    sut.dremio_source = UNSET

    with pytest.raises(ValueError, match="one of dremio_source, dremio_space"):
        sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, FOLDER_NAME, "qualified_name is required"),
        (FOLDER_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DremioFolder.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a DremioFolder for modification."""
    sut = DremioFolder.updater(qualified_name=FOLDER_QUALIFIED_NAME, name=FOLDER_NAME)

    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.name == FOLDER_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = DremioFolder.updater(
        qualified_name=FOLDER_QUALIFIED_NAME, name=FOLDER_NAME
    ).trim_to_required()

    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.name == FOLDER_NAME
