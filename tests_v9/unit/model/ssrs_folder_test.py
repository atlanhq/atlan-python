# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SSRSFolder model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-ssrs-app emits today
(``{parentQN}/{name without spaces}``, golden ``ssrs-demo`` fixture), so a
creator change that would re-key existing folders fails here.
"""

import pytest

from pyatlan_v9.model import SSRSFolder

CONNECTION_QUALIFIED_NAME = "default/ssrs/1000000001"
FOLDER_NAME = "Sales Reports"
FOLDER_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/SalesReports"
SUB_FOLDER_QUALIFIED_NAME = f"{FOLDER_QUALIFIED_NAME}/Monthly"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-ssrs-app's map_folder inputs and output."""
    sut = SSRSFolder.creator(
        name="Atlan", connection_qualified_name="default/ssrs/1000000001"
    )

    assert sut.qualified_name == "default/ssrs/1000000001/Atlan"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (FOLDER_NAME, None, "connection_qualified_name is required"),
        (FOLDER_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SSRSFolder.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator_with_parent_outside_connection_raises_value_error():
    """Test creator rejects a parent folder from another connection."""
    with pytest.raises(ValueError, match="parent_folder_qualified_name is invalid"):
        SSRSFolder.creator(
            name=FOLDER_NAME,
            connection_qualified_name=CONNECTION_QUALIFIED_NAME,
            parent_folder_qualified_name="default/ssrs/999/Other",
        )


def test_creator():
    """Test creator builds a root folder with spaces stripped from the qn."""
    sut = SSRSFolder.creator(
        name=FOLDER_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == FOLDER_NAME
    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "ssrs"
    assert not sut.ssrs_parent_folder_qualified_name
    assert not sut.ssrs_parent_folder
    sut.validate(for_creation=True)


def test_creator_with_parent_folder():
    """Test creator nests a folder under its parent folder."""
    sut = SSRSFolder.creator(
        name="Monthly",
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        parent_folder_qualified_name=FOLDER_QUALIFIED_NAME,
    )

    assert sut.qualified_name == SUB_FOLDER_QUALIFIED_NAME
    assert sut.ssrs_parent_folder_qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.ssrs_parent_folder.unique_attributes == {
        "qualifiedName": FOLDER_QUALIFIED_NAME
    }
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
        SSRSFolder.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an SSRSFolder for modification."""
    sut = SSRSFolder.updater(qualified_name=FOLDER_QUALIFIED_NAME, name=FOLDER_NAME)

    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.name == FOLDER_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SSRSFolder.updater(
        qualified_name=FOLDER_QUALIFIED_NAME, name=FOLDER_NAME
    ).trim_to_required()

    assert sut.qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.name == FOLDER_NAME
