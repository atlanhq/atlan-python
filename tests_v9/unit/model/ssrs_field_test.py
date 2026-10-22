# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SSRSField model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-ssrs-app emits today
(``{dataSetQN}/{name without spaces}``, golden ``ssrs-demo`` fixture), so a
creator change that would re-key existing fields fails here.
"""

import pytest

from pyatlan_v9.model import SSRSField

CONNECTION_QUALIFIED_NAME = "default/ssrs/1000000001"
FOLDER_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/Atlan"
REPORT_QUALIFIED_NAME = f"{FOLDER_QUALIFIED_NAME}/SalesReport"
DATA_SET_QUALIFIED_NAME = f"{REPORT_QUALIFIED_NAME}/SalesData"
FIELD_NAME = "Line Total"
FIELD_QUALIFIED_NAME = f"{DATA_SET_QUALIFIED_NAME}/LineTotal"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-ssrs-app's map_field inputs and output."""
    sut = SSRSField.creator(
        name="CustomerId",
        ssrs_data_set_qualified_name="default/ssrs/1000000001/Atlan/OrderDetailsbyCategory/OrderDetails",
    )

    assert (
        sut.qualified_name
        == "default/ssrs/1000000001/Atlan/OrderDetailsbyCategory/OrderDetails/CustomerId"
    )
    assert sut.ssrs_data_set_name == "OrderDetails"
    assert (
        sut.ssrs_report_qualified_name
        == "default/ssrs/1000000001/Atlan/OrderDetailsbyCategory"
    )
    assert sut.ssrs_report_name == "OrderDetailsbyCategory"
    assert sut.ssrs_parent_folder_qualified_name == "default/ssrs/1000000001/Atlan"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, data_set_qualified_name, message",
    [
        (None, DATA_SET_QUALIFIED_NAME, "name is required"),
        (" ", DATA_SET_QUALIFIED_NAME, "name cannot be blank"),
        (FIELD_NAME, None, "ssrs_data_set_qualified_name is required"),
        (FIELD_NAME, " ", "ssrs_data_set_qualified_name cannot be blank"),
        (
            FIELD_NAME,
            f"{CONNECTION_QUALIFIED_NAME}/SalesReport",
            "ssrs_data_set_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, data_set_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SSRSField.creator(
            name=name, ssrs_data_set_qualified_name=data_set_qualified_name
        )


def test_creator_with_data_set_outside_connection_raises_value_error():
    """Test creator rejects a data set that is not under the given connection."""
    with pytest.raises(ValueError, match="ssrs_data_set_qualified_name is invalid"):
        SSRSField.creator(
            name=FIELD_NAME,
            ssrs_data_set_qualified_name=DATA_SET_QUALIFIED_NAME,
            connection_qualified_name="default/ssrs/999",
        )


def test_creator():
    """Test creator derives the connection, report and data set from the data set qn."""
    sut = SSRSField.creator(
        name=FIELD_NAME, ssrs_data_set_qualified_name=DATA_SET_QUALIFIED_NAME
    )

    assert sut.name == FIELD_NAME
    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "ssrs"
    assert sut.ssrs_data_set_qualified_name == DATA_SET_QUALIFIED_NAME
    assert sut.ssrs_data_set_name == "SalesData"
    assert sut.ssrs_report_qualified_name == REPORT_QUALIFIED_NAME
    assert sut.ssrs_report_name == "SalesReport"
    assert sut.ssrs_parent_folder_qualified_name == FOLDER_QUALIFIED_NAME
    assert sut.ssrs_data_set.unique_attributes == {
        "qualifiedName": DATA_SET_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_creator_in_root_report():
    """Test creator leaves the folder unset when the report is at the root."""
    sut = SSRSField.creator(
        name=FIELD_NAME,
        ssrs_data_set_qualified_name=f"{CONNECTION_QUALIFIED_NAME}/SalesReport/SalesData",
    )

    assert sut.ssrs_report_qualified_name == f"{CONNECTION_QUALIFIED_NAME}/SalesReport"
    assert not sut.ssrs_parent_folder_qualified_name
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit connection qualified name."""
    sut = SSRSField.creator(
        name=FIELD_NAME,
        ssrs_data_set_qualified_name=DATA_SET_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, FIELD_NAME, "qualified_name is required"),
        (FIELD_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SSRSField.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an SSRSField for modification."""
    sut = SSRSField.updater(qualified_name=FIELD_QUALIFIED_NAME, name=FIELD_NAME)

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.name == FIELD_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SSRSField.updater(
        qualified_name=FIELD_QUALIFIED_NAME, name=FIELD_NAME
    ).trim_to_required()

    assert sut.qualified_name == FIELD_QUALIFIED_NAME
    assert sut.name == FIELD_NAME
