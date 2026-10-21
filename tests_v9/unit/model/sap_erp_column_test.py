# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SapErpColumn model in pyatlan_v9.

The parity tests use the exact qualifiedNames atlan-saperp-app emits today
(``{connectionQN}/column/{cleaned parent}/{cleaned field}``, FND-3838 census),
so a creator change that would re-key existing columns fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SapErpColumn

CONNECTION_QUALIFIED_NAME = "default/sap-ecc/123456789"
CONNECTOR_NAME = "sap-ecc"
TABLE_NAME = "MARA"
TABLE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/table/{TABLE_NAME}"
VIEW_NAME = "V_T001"
VIEW_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/view/{VIEW_NAME}"
CDS_VIEW_NAME = "I_PRODUCT"
CDS_VIEW_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/cdsview/{CDS_VIEW_NAME}"
COLUMN_NAME = "MATNR"
COLUMN_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/column/{TABLE_NAME}/{COLUMN_NAME}"


def test_creator_matches_app_qualified_name_for_table_column():
    """Mirror atlan-saperp-app's get_sapcolumn_sql for a table column."""
    sut = SapErpColumn.creator(
        name="/BIC/ZFIELD",
        parent_qualified_name="default/sap-s4/1700000000/table/_BIC_AZSALES",
        parent_name="/BIC/AZSALES",
    )

    assert (
        sut.qualified_name
        == "default/sap-s4/1700000000/column/_BIC_AZSALES/_BIC_ZFIELD"
    )
    assert sut.name == "/BIC/ZFIELD"
    assert sut.sap_erp_table_name == "/BIC/AZSALES"
    assert (
        sut.sap_erp_table_qualified_name
        == "default/sap-s4/1700000000/table/_BIC_AZSALES"
    )
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_for_view_column():
    """Mirror atlan-saperp-app's get_sapcolumn_sql for a view column."""
    sut = SapErpColumn.creator(
        name="BUKRS",
        parent_qualified_name="default/sap-ecc/1700000000/view/V_T001",
    )

    assert sut.qualified_name == "default/sap-ecc/1700000000/column/V_T001/BUKRS"
    assert sut.sap_erp_view_name == "V_T001"
    assert sut.sap_erp_view_qualified_name == "default/sap-ecc/1700000000/view/V_T001"
    assert sut.sap_erp_table is UNSET
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_for_cds_view_column():
    """Mirror atlan-saperp-app's get_sapcdscolumn_sql for a CDS view column."""
    sut = SapErpColumn.creator(
        name="Product",
        parent_qualified_name="default/sap-s4/1700000000/cdsview/I_PRODUCT",
    )

    assert sut.qualified_name == "default/sap-s4/1700000000/column/I_PRODUCT/Product"
    assert sut.sap_erp_cds_view_name == "I_PRODUCT"
    assert (
        sut.sap_erp_cds_view_qualified_name
        == "default/sap-s4/1700000000/cdsview/I_PRODUCT"
    )
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, parent_qualified_name, message",
    [
        (None, TABLE_QUALIFIED_NAME, "name is required"),
        (" ", TABLE_QUALIFIED_NAME, "name cannot be blank"),
        (COLUMN_NAME, None, "parent_qualified_name is required"),
        (COLUMN_NAME, " ", "parent_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, parent_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapErpColumn.creator(name=name, parent_qualified_name=parent_qualified_name)


@pytest.mark.parametrize(
    "parent_qualified_name",
    [
        "MARA",
        "table/MARA",
        f"{CONNECTION_QUALIFIED_NAME}/MARA",
        f"{CONNECTION_QUALIFIED_NAME}/schema/MARA",
        f"{CONNECTION_QUALIFIED_NAME}/table/",
        f"{CONNECTION_QUALIFIED_NAME}/column/MARA/MATNR",
    ],
)
def test_creator_with_invalid_parent_raises_value_error(parent_qualified_name: str):
    """Test creator rejects a parent qualifiedName that is not a table/view/CDS view."""
    with pytest.raises(ValueError, match="parent_qualified_name is invalid"):
        SapErpColumn.creator(
            name=COLUMN_NAME, parent_qualified_name=parent_qualified_name
        )


def test_creator_with_table_parent():
    """Test creator derives the connection and relates the column to its table."""
    sut = SapErpColumn.creator(
        name=COLUMN_NAME, parent_qualified_name=TABLE_QUALIFIED_NAME
    )

    assert sut.type_name == "SapErpColumn"
    assert sut.name == COLUMN_NAME
    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.sap_erp_table.unique_attributes == {
        "qualifiedName": TABLE_QUALIFIED_NAME
    }
    assert sut.sap_erp_table_name == TABLE_NAME
    assert sut.sap_erp_table_qualified_name == TABLE_QUALIFIED_NAME
    assert sut.sap_erp_view is UNSET
    assert sut.sap_erp_cds_view is UNSET
    assert sut.guid
    sut.validate(for_creation=True)


def test_creator_with_view_parent():
    """Test creator relates the column to its view only."""
    sut = SapErpColumn.creator(
        name=COLUMN_NAME, parent_qualified_name=VIEW_QUALIFIED_NAME
    )

    assert sut.qualified_name == (
        f"{CONNECTION_QUALIFIED_NAME}/column/{VIEW_NAME}/{COLUMN_NAME}"
    )
    assert sut.sap_erp_view.unique_attributes == {"qualifiedName": VIEW_QUALIFIED_NAME}
    assert sut.sap_erp_view_name == VIEW_NAME
    assert sut.sap_erp_table is UNSET
    assert sut.sap_erp_table_name is UNSET
    assert sut.sap_erp_cds_view is UNSET
    sut.validate(for_creation=True)


def test_creator_with_cds_view_parent():
    """Test creator relates the column to its CDS view only."""
    sut = SapErpColumn.creator(
        name=COLUMN_NAME, parent_qualified_name=CDS_VIEW_QUALIFIED_NAME
    )

    assert sut.sap_erp_cds_view.unique_attributes == {
        "qualifiedName": CDS_VIEW_QUALIFIED_NAME
    }
    assert sut.sap_erp_cds_view_name == CDS_VIEW_NAME
    assert sut.sap_erp_table is UNSET
    assert sut.sap_erp_view is UNSET
    sut.validate(for_creation=True)


def test_creator_with_explicit_parent_name():
    """Test an explicit raw parent name overrides the cleaned one from the qn."""
    sut = SapErpColumn.creator(
        name=COLUMN_NAME,
        parent_qualified_name=f"{CONNECTION_QUALIFIED_NAME}/table/_BIC_AZSALES",
        parent_name="/BIC/AZSALES",
    )

    assert sut.sap_erp_table_name == "/BIC/AZSALES"
    assert sut.qualified_name == (
        f"{CONNECTION_QUALIFIED_NAME}/column/_BIC_AZSALES/{COLUMN_NAME}"
    )


def test_validate_for_creation_requires_a_parent():
    """Test validate(for_creation=True) rejects a column with no parent."""
    sut = SapErpColumn(
        name=COLUMN_NAME,
        qualified_name=COLUMN_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    with pytest.raises(ValueError, match="one of sap_erp_table, sap_erp_view"):
        sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, COLUMN_NAME, "qualified_name is required"),
        (COLUMN_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SapErpColumn.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a SapErpColumn for modification."""
    sut = SapErpColumn.updater(qualified_name=COLUMN_QUALIFIED_NAME, name=COLUMN_NAME)

    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SapErpColumn.creator(
        name=COLUMN_NAME, parent_qualified_name=TABLE_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME
    assert sut.sap_erp_table is UNSET
