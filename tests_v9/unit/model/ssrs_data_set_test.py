# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SSRSDataSet model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-ssrs-app emits today
(``{reportQN}/{name without spaces}``, golden ``ssrs-demo`` fixture), so a
creator change that would re-key existing data sets fails here.
"""

import pytest

from pyatlan_v9.model import SSRSDataSet

CONNECTION_QUALIFIED_NAME = "default/ssrs/1000000001"
FOLDER_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/Atlan"
REPORT_QUALIFIED_NAME = f"{FOLDER_QUALIFIED_NAME}/SalesReport"
DATA_SET_NAME = "Sales Data"
DATA_SET_QUALIFIED_NAME = f"{REPORT_QUALIFIED_NAME}/SalesData"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-ssrs-app's map_dataset inputs and output."""
    sut = SSRSDataSet.creator(
        name="OrderDetails",
        ssrs_report_qualified_name="default/ssrs/1000000001/Atlan/OrderDetailsbyCategory",
    )

    assert (
        sut.qualified_name
        == "default/ssrs/1000000001/Atlan/OrderDetailsbyCategory/OrderDetails"
    )
    assert (
        sut.ssrs_report_qualified_name
        == "default/ssrs/1000000001/Atlan/OrderDetailsbyCategory"
    )
    assert sut.ssrs_report_name == "OrderDetailsbyCategory"
    assert sut.ssrs_parent_folder_qualified_name == "default/ssrs/1000000001/Atlan"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, report_qualified_name, message",
    [
        (None, REPORT_QUALIFIED_NAME, "name is required"),
        (" ", REPORT_QUALIFIED_NAME, "name cannot be blank"),
        (DATA_SET_NAME, None, "ssrs_report_qualified_name is required"),
        (DATA_SET_NAME, " ", "ssrs_report_qualified_name cannot be blank"),
        (
            DATA_SET_NAME,
            CONNECTION_QUALIFIED_NAME,
            "ssrs_report_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, report_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SSRSDataSet.creator(name=name, ssrs_report_qualified_name=report_qualified_name)


def test_creator_with_report_outside_connection_raises_value_error():
    """Test creator rejects a report that is not under the given connection."""
    with pytest.raises(ValueError, match="ssrs_report_qualified_name is invalid"):
        SSRSDataSet.creator(
            name=DATA_SET_NAME,
            ssrs_report_qualified_name=REPORT_QUALIFIED_NAME,
            connection_qualified_name="default/ssrs/999",
        )


def test_creator():
    """Test creator derives the connection and report from the report qn."""
    sut = SSRSDataSet.creator(
        name=DATA_SET_NAME, ssrs_report_qualified_name=REPORT_QUALIFIED_NAME
    )

    assert sut.name == DATA_SET_NAME
    assert sut.qualified_name == DATA_SET_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "ssrs"
    assert sut.ssrs_report_qualified_name == REPORT_QUALIFIED_NAME
    assert sut.ssrs_report_name == "SalesReport"
    assert sut.ssrs_parent_folder_qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.ssrs_report.unique_attributes == {"qualifiedName": REPORT_QUALIFIED_NAME}
    sut.validate(for_creation=True)


def test_creator_in_root_report():
    """Test creator leaves the folder unset when the report is at the root."""
    sut = SSRSDataSet.creator(
        name=DATA_SET_NAME,
        ssrs_report_qualified_name=f"{CONNECTION_QUALIFIED_NAME}/SalesReport",
    )

    assert sut.qualified_name == f"{CONNECTION_QUALIFIED_NAME}/SalesReport/SalesData"
    assert not sut.ssrs_parent_folder_qualified_name
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit connection qualified name."""
    sut = SSRSDataSet.creator(
        name=DATA_SET_NAME,
        ssrs_report_qualified_name=REPORT_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == DATA_SET_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DATA_SET_NAME, "qualified_name is required"),
        (DATA_SET_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SSRSDataSet.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an SSRSDataSet for modification."""
    sut = SSRSDataSet.updater(
        qualified_name=DATA_SET_QUALIFIED_NAME, name=DATA_SET_NAME
    )

    assert sut.qualified_name == DATA_SET_QUALIFIED_NAME
    assert sut.name == DATA_SET_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SSRSDataSet.updater(
        qualified_name=DATA_SET_QUALIFIED_NAME, name=DATA_SET_NAME
    ).trim_to_required()

    assert sut.qualified_name == DATA_SET_QUALIFIED_NAME
    assert sut.name == DATA_SET_NAME
