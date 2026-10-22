# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SSRSReport model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-ssrs-app emits today
(``{folderQN}/{name without spaces}``, golden ``ssrs-demo`` fixture), so a
creator change that would re-key existing reports fails here.
"""

import pytest

from pyatlan_v9.model import SSRSReport

CONNECTION_QUALIFIED_NAME = "default/ssrs/1000000001"
FOLDER_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/Atlan"
REPORT_NAME = "Sales Report"
REPORT_QUALIFIED_NAME = f"{FOLDER_QUALIFIED_NAME}/SalesReport"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-ssrs-app's map_report inputs and output."""
    sut = SSRSReport.creator(
        name="Order Details by Category",
        connection_qualified_name="default/ssrs/1000000001",
        folder_qualified_name="default/ssrs/1000000001/Atlan",
    )

    assert sut.qualified_name == "default/ssrs/1000000001/Atlan/OrderDetailsbyCategory"
    assert sut.name == "Order Details by Category"
    assert sut.ssrs_parent_folder_qualified_name == "default/ssrs/1000000001/Atlan"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (REPORT_NAME, None, "connection_qualified_name is required"),
        (REPORT_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SSRSReport.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator_with_folder_outside_connection_raises_value_error():
    """Test creator rejects a folder from another connection."""
    with pytest.raises(ValueError, match="folder_qualified_name is invalid"):
        SSRSReport.creator(
            name=REPORT_NAME,
            connection_qualified_name=CONNECTION_QUALIFIED_NAME,
            folder_qualified_name="default/ssrs/999/Other",
        )


def test_creator():
    """Test creator relates the report to its folder."""
    sut = SSRSReport.creator(
        name=REPORT_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        folder_qualified_name=FOLDER_QUALIFIED_NAME,
    )

    assert sut.name == REPORT_NAME
    assert sut.qualified_name == REPORT_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "ssrs"
    assert sut.ssrs_parent_folder_qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.ssrs_folder.unique_attributes == {"qualifiedName": FOLDER_QUALIFIED_NAME}
    sut.validate(for_creation=True)


def test_creator_at_root():
    """Test creator builds a report with no folder, as the app does at the root."""
    sut = SSRSReport.creator(
        name=REPORT_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.qualified_name == f"{CONNECTION_QUALIFIED_NAME}/SalesReport"
    assert not sut.ssrs_parent_folder_qualified_name
    assert not sut.ssrs_folder
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, REPORT_NAME, "qualified_name is required"),
        (REPORT_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SSRSReport.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an SSRSReport for modification."""
    sut = SSRSReport.updater(qualified_name=REPORT_QUALIFIED_NAME, name=REPORT_NAME)

    assert sut.qualified_name == REPORT_QUALIFIED_NAME
    assert sut.name == REPORT_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SSRSReport.updater(
        qualified_name=REPORT_QUALIFIED_NAME, name=REPORT_NAME
    ).trim_to_required()

    assert sut.qualified_name == REPORT_QUALIFIED_NAME
    assert sut.name == REPORT_NAME
