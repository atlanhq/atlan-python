# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for AnomaloCheck model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-anomalo-app emits today
(``{connectionQN}/{warehouseId}/{tableId}/check/{checkId}``, FND-3838 census),
so a creator change that would re-key existing checks fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import AnomaloCheck

CONNECTION_QUALIFIED_NAME = "default/anomalo/123456789"
CONNECTOR_NAME = "anomalo"
CHECK_NAME = "orders row count"
WAREHOUSE_ID = 7
TABLE_ID = "4521"
CHECK_ID = "-105"
CHECK_QUALIFIED_NAME = (
    f"{CONNECTION_QUALIFIED_NAME}/{WAREHOUSE_ID}/{TABLE_ID}/check/{CHECK_ID}"
)
LINKED_QUALIFIED_NAME = "default/snowflake/1700000000/DB/SCHEMA/ORDERS"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-anomalo-app's check_qualified_name / check_entity inputs and output."""
    sut = AnomaloCheck.creator(
        name="orders has rows",
        connection_qualified_name="default/anomalo/1700000000",
        warehouse_id=12,
        table_id="3456",
        check_id="789",
        linked_asset_qualified_name="default/snowflake/1600000000/DB/SCH/ORDERS",
    )

    assert sut.qualified_name == "default/anomalo/1700000000/12/3456/check/789"
    assert sut.connector_name == "anomalo"
    assert (
        sut.anomalo_check_linked_asset_qualified_name
        == "default/snowflake/1600000000/DB/SCH/ORDERS"
    )
    assert sut.anomalo_check_asset.type_name == "Table"
    assert sut.anomalo_check_asset.unique_attributes == {
        "qualifiedName": "default/snowflake/1600000000/DB/SCH/ORDERS"
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, warehouse_id, table_id, check_id, message",
    [
        (
            None,
            CONNECTION_QUALIFIED_NAME,
            WAREHOUSE_ID,
            TABLE_ID,
            CHECK_ID,
            "name is required",
        ),
        (
            " ",
            CONNECTION_QUALIFIED_NAME,
            WAREHOUSE_ID,
            TABLE_ID,
            CHECK_ID,
            "name cannot be blank",
        ),
        (
            CHECK_NAME,
            None,
            WAREHOUSE_ID,
            TABLE_ID,
            CHECK_ID,
            "connection_qualified_name is required",
        ),
        (
            CHECK_NAME,
            " ",
            WAREHOUSE_ID,
            TABLE_ID,
            CHECK_ID,
            "connection_qualified_name cannot be blank",
        ),
        (
            CHECK_NAME,
            CONNECTION_QUALIFIED_NAME,
            None,
            TABLE_ID,
            CHECK_ID,
            "warehouse_id is required",
        ),
        (
            CHECK_NAME,
            CONNECTION_QUALIFIED_NAME,
            " ",
            TABLE_ID,
            CHECK_ID,
            "warehouse_id cannot be blank",
        ),
        (
            CHECK_NAME,
            CONNECTION_QUALIFIED_NAME,
            WAREHOUSE_ID,
            None,
            CHECK_ID,
            "table_id is required",
        ),
        (
            CHECK_NAME,
            CONNECTION_QUALIFIED_NAME,
            WAREHOUSE_ID,
            " ",
            CHECK_ID,
            "table_id cannot be blank",
        ),
        (
            CHECK_NAME,
            CONNECTION_QUALIFIED_NAME,
            WAREHOUSE_ID,
            TABLE_ID,
            None,
            "check_id is required",
        ),
        (
            CHECK_NAME,
            CONNECTION_QUALIFIED_NAME,
            WAREHOUSE_ID,
            TABLE_ID,
            " ",
            "check_id cannot be blank",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    connection_qualified_name: str,
    warehouse_id: int,
    table_id: str,
    check_id: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AnomaloCheck.creator(
            name=name,
            connection_qualified_name=connection_qualified_name,
            warehouse_id=warehouse_id,
            table_id=table_id,
            check_id=check_id,
        )


def test_creator():
    """Test creator sets the qualifiedName and denormalised connection attributes."""
    sut = AnomaloCheck.creator(
        name=CHECK_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        warehouse_id=WAREHOUSE_ID,
        table_id=TABLE_ID,
        check_id=CHECK_ID,
    )

    assert sut.type_name == "AnomaloCheck"
    assert sut.name == CHECK_NAME
    assert sut.qualified_name == CHECK_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.anomalo_check_linked_asset_qualified_name is UNSET
    assert sut.anomalo_check_asset is UNSET
    assert sut.guid
    sut.validate(for_creation=True)


def test_creator_with_linked_asset_type():
    """Test creator links a non-table asset with the given type name."""
    sut = AnomaloCheck.creator(
        name=CHECK_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        warehouse_id=str(WAREHOUSE_ID),
        table_id=TABLE_ID,
        check_id=CHECK_ID,
        linked_asset_qualified_name=LINKED_QUALIFIED_NAME,
        linked_asset_type_name="View",
    )

    assert sut.qualified_name == CHECK_QUALIFIED_NAME
    assert sut.anomalo_check_linked_asset_qualified_name == LINKED_QUALIFIED_NAME
    assert sut.anomalo_check_asset.type_name == "View"
    assert sut.anomalo_check_asset.unique_attributes == {
        "qualifiedName": LINKED_QUALIFIED_NAME
    }


def test_validate_rejects_qualified_name_with_too_few_segments():
    """Test validate enforces the warehouse/table/check segments."""
    sut = AnomaloCheck(
        name=CHECK_NAME,
        qualified_name=f"{TABLE_ID}/check/{CHECK_ID}",
    )

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CHECK_NAME, "qualified_name is required"),
        (CHECK_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AnomaloCheck.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an AnomaloCheck for modification."""
    sut = AnomaloCheck.updater(qualified_name=CHECK_QUALIFIED_NAME, name=CHECK_NAME)

    assert sut.qualified_name == CHECK_QUALIFIED_NAME
    assert sut.name == CHECK_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = AnomaloCheck.creator(
        name=CHECK_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        warehouse_id=WAREHOUSE_ID,
        table_id=TABLE_ID,
        check_id=CHECK_ID,
        linked_asset_qualified_name=LINKED_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == CHECK_QUALIFIED_NAME
    assert sut.name == CHECK_NAME
    assert sut.anomalo_check_linked_asset_qualified_name is UNSET
    assert sut.anomalo_check_asset is UNSET
