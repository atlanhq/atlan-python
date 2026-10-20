# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for IcebergColumn.creator in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-iceberg-app emits
(``_build_column_qn``, FND-3838 census): ``{table}/{column_path}``, where a
nested column's path is its ancestors' names joined with ``/``. The census lists
three variants (``{column_path}``, ``{ancestor_path|join('/')}`` for the parent,
and ``{conn}{qn}`` for connection-less qns rebased onto the connection); all are
checked below.
"""

import pytest

from pyatlan_v9.model import IcebergColumn

CONNECTION_QN = "default/iceberg/1712345678"
CATALOG_QN = "default/iceberg/1712345678/lakehouse"
NAMESPACE_QN = "default/iceberg/1712345678/lakehouse/sales/emea"
TABLE_QN = "default/iceberg/1712345678/lakehouse/sales/emea/orders"


def _creator(**overrides):
    return IcebergColumn.creator(
        **{"name": "id", "table_qualified_name": TABLE_QN, "order": 1, **overrides}
    )


@pytest.mark.parametrize(
    "table_qn, expected_qn",
    [
        (
            "default/iceberg/1712345678/lakehouse/sales/orders",
            "default/iceberg/1712345678/lakehouse/sales/orders/id",
        ),
        (
            "default/iceberg/1712345678/lakehouse/sales/emea/orders",
            "default/iceberg/1712345678/lakehouse/sales/emea/orders/id",
        ),
        (
            "default/iceberg/1712345678/lakehouse/sales/emea/uk/orders",
            "default/iceberg/1712345678/lakehouse/sales/emea/uk/orders/id",
        ),
    ],
)
def test_top_level_column_matches_app_qualified_name(table_qn, expected_qn):
    sut = _creator(table_qualified_name=table_qn)

    assert sut.qualified_name == expected_qn
    sut.validate(for_creation=True)


def test_nested_column_matches_app_qualified_name():
    # address (struct) -> geo (struct) -> lat, built one level at a time.
    address = _creator(name="address", order=3)
    geo = _creator(
        name="geo", order=2, parent_column_qualified_name=address.qualified_name
    )
    lat = _creator(name="lat", order=1, parent_column_qualified_name=geo.qualified_name)

    # {ancestor_path|join('/')}: the app's parent column qn
    assert (
        geo.qualified_name
        == "default/iceberg/1712345678/lakehouse/sales/emea/orders/address/geo"
    )
    # {column_path}, and {conn}{qn} rebased from "/lakehouse/sales/emea/orders/address/geo/lat"
    assert (
        lat.qualified_name
        == "default/iceberg/1712345678/lakehouse/sales/emea/orders/address/geo/lat"
    )
    lat.validate(for_creation=True)


def test_top_level_column_attributes():
    sut = _creator()

    assert sut.name == "id"
    assert sut.order == 1
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "iceberg"
    assert sut.database_name == "lakehouse"
    assert sut.database_qualified_name == CATALOG_QN
    assert sut.schema_name == "emea"
    assert sut.schema_qualified_name == NAMESPACE_QN
    assert sut.table_name == "orders"
    assert sut.table_qualified_name == TABLE_QN
    assert sut.table.type_name == "IcebergTable"
    assert sut.table.unique_attributes == {"qualifiedName": TABLE_QN}
    assert sut.column_depth_level == 1
    assert sut.iceberg_parent_namespace_qualified_name == NAMESPACE_QN
    assert sut.iceberg_namespace_hierarchy == [
        {
            "qualifiedName": "default/iceberg/1712345678/lakehouse/sales",
            "name": "sales",
        },
        {"qualifiedName": NAMESPACE_QN, "name": "emea"},
    ]
    # Parent-column attributes are left unset for a top-level column.
    assert not sut.parent_column_name
    assert not sut.parent_column_qualified_name
    assert not sut.column_hierarchy


def test_nested_column_attributes():
    sut = _creator(name="lat", parent_column_qualified_name=f"{TABLE_QN}/address/geo")

    # The app links nested columns to the table too, not to the parent column.
    assert sut.table.unique_attributes == {"qualifiedName": TABLE_QN}
    assert sut.table_qualified_name == TABLE_QN
    assert sut.parent_column_name == "geo"
    assert sut.parent_column_qualified_name == f"{TABLE_QN}/address/geo"
    assert sut.column_depth_level == 3
    assert sut.column_hierarchy == [
        {"name": "address", "depth": "1", "qualifiedName": f"{TABLE_QN}/address"},
        {"name": "geo", "depth": "2", "qualifiedName": f"{TABLE_QN}/address/geo"},
    ]


def test_column_in_top_level_namespace_has_no_parent_namespace():
    sut = _creator(table_qualified_name=f"{CATALOG_QN}/sales/orders")

    assert sut.schema_name == "sales"
    assert sut.iceberg_parent_namespace_qualified_name is None


def test_create_alias():
    assert (
        IcebergColumn.create(
            name="id", table_qualified_name=TABLE_QN, order=1
        ).qualified_name
        == f"{TABLE_QN}/id"
    )


@pytest.mark.parametrize("param", ["name", "table_qualified_name"])
@pytest.mark.parametrize(
    "value, message", [(None, "is required"), ("  ", "cannot be blank")]
)
def test_creator_rejects_missing_or_blank_inputs(param, value, message):
    with pytest.raises(ValueError, match=f"{param} {message}"):
        _creator(**{param: value})


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"order": None}, "order is required"),
        ({"order": -1}, "Order must be a non-negative integer"),
        (
            {"parent_column_qualified_name": "  "},
            "parent_column_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_rejects_bad_order_or_parent_column(kwargs, message):
    with pytest.raises(ValueError, match=message):
        _creator(**kwargs)


@pytest.mark.parametrize(
    "param, bad_qn",
    [
        # a namespace qn: one segment short of a table
        ("table_qualified_name", "default/iceberg/1712345678/lakehouse/orders"),
        # a column of another table
        (
            "parent_column_qualified_name",
            "default/iceberg/1712345678/lakehouse/sales/other/address",
        ),
        # the table itself, with no column path
        ("parent_column_qualified_name", f"{TABLE_QN}/"),
    ],
)
def test_creator_rejects_malformed_parent_qualified_name(param, bad_qn):
    with pytest.raises(ValueError, match=f"Invalid {param}"):
        _creator(**{param: bad_qn})


def test_updater():
    sut = IcebergColumn.updater(qualified_name=f"{TABLE_QN}/id", name="id")

    assert sut.qualified_name == f"{TABLE_QN}/id"
    assert sut.name == "id"


@pytest.mark.parametrize("param", ["qualified_name", "name"])
def test_updater_rejects_missing_inputs(param):
    args = {"qualified_name": f"{TABLE_QN}/id", "name": "id", param: None}
    with pytest.raises(ValueError, match=f"{param} is required"):
        IcebergColumn.updater(**args)


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert isinstance(sut, IcebergColumn)
    assert sut.qualified_name == f"{TABLE_QN}/id"
    assert sut.name == "id"
