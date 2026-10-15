# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Iceberg creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-iceberg-app emits today
(FND-3838 census, ``app/qualified_names.py``), so a creator change that would
re-key existing Iceberg assets fails here. Namespaces and nested columns have
variable depth, so each template is checked at 1, 2 and 3 levels.
"""

import json

import pytest

from pyatlan_v9.model import (
    IcebergCatalog,
    IcebergColumn,
    IcebergNamespace,
    IcebergTable,
)

CONN = "default/iceberg/1712345678"
CATALOG = "lakehouse"
CATALOG_QN = f"{CONN}/{CATALOG}"


# --- the app's qualifiedName grammar, copied from atlan-iceberg-app ----------
# (app/qualified_names.py) so the parity cases below read as the app's inputs.
def _ns_path(namespace):
    return namespace.replace(".", "/") if "." in namespace else namespace


def _app_namespace_qn(namespace):
    return f"{CONN}/{CATALOG}/{_ns_path(namespace)}"


def _app_table_qn(namespace, table):
    return f"{CONN}/{CATALOG}/{_ns_path(namespace)}/{table}"


def _app_column_qn(namespace, table, column_name, column_path=None):
    leaf = column_path if column_path else column_name
    return f"{CONN}/{CATALOG}/{_ns_path(namespace)}/{table}/{leaf}"


def _namespace(dotted):
    """Build a namespace the way a caller adopting the creator would: one level at a time."""
    parent_qn = CATALOG_QN
    ns = None
    for segment in dotted.split("."):
        ns = IcebergNamespace.creator(name=segment, parent_qualified_name=parent_qn)
        parent_qn = ns.qualified_name
    return ns


# --- IcebergCatalog -----------------------------------------------------------


def test_catalog_creator_matches_app_qualified_name():
    sut = IcebergCatalog.creator(name=CATALOG, connection_qualified_name=CONN)

    assert sut.qualified_name == "default/iceberg/1712345678/lakehouse"
    assert sut.name == CATALOG
    assert sut.connection_qualified_name == CONN
    assert sut.connector_name == "iceberg"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONN, "name is required"),
        ("  ", CONN, "name cannot be blank"),
        (CATALOG, None, "connection_qualified_name is required"),
        (CATALOG, "", "connection_qualified_name cannot be blank"),
        (CATALOG, "default/iceberg", "Invalid connection_qualified_name"),
        (CATALOG, f"{CONN}/extra", "Invalid connection_qualified_name"),
    ],
)
def test_catalog_creator_rejects_bad_inputs(name, connection_qualified_name, message):
    with pytest.raises(ValueError, match=message):
        IcebergCatalog.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


# --- IcebergNamespace ---------------------------------------------------------


@pytest.mark.parametrize(
    "dotted, expected_qn",
    [
        ("sales", "default/iceberg/1712345678/lakehouse/sales"),
        ("sales.emea", "default/iceberg/1712345678/lakehouse/sales/emea"),
        ("sales.emea.uk", "default/iceberg/1712345678/lakehouse/sales/emea/uk"),
    ],
)
def test_namespace_creator_matches_app_qualified_name(dotted, expected_qn):
    sut = _namespace(dotted)

    assert sut.qualified_name == expected_qn
    assert sut.qualified_name == _app_namespace_qn(dotted)
    assert sut.name == dotted.split(".")[-1]
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_namespace_first_segment_variant():
    # The app also names a nested namespace's parent from its first segment only:
    # {conn}/{catalog}/{first_namespace_segment}. That is a top-level namespace qn.
    sut = IcebergNamespace.creator(name="sales", parent_qualified_name=CATALOG_QN)

    assert sut.qualified_name == _app_namespace_qn("sales.emea.uk".split(".")[0])


def test_top_level_namespace_attributes():
    sut = IcebergNamespace.creator(name="sales", parent_qualified_name=CATALOG_QN)

    assert sut.connection_qualified_name == CONN
    assert sut.connector_name == "iceberg"
    assert sut.database_name == CATALOG
    assert sut.database_qualified_name == CATALOG_QN
    assert sut.database.qualified_name == CATALOG_QN
    assert sut.database.type_name == "IcebergCatalog"
    assert sut.iceberg_parent_namespace_qualified_name is None
    assert sut.iceberg_namespace_hierarchy == [
        {"qualifiedName": f"{CATALOG_QN}/sales", "name": "sales"}
    ]


def test_nested_namespace_attributes():
    sut = _namespace("sales.emea.uk")

    assert sut.database_name == CATALOG
    assert sut.database_qualified_name == CATALOG_QN
    assert sut.database.qualified_name == CATALOG_QN
    # The immediate parent, as the typedef describes. (The app uses the first
    # segment, {catalog}/sales, which is wrong for 3+ levels.)
    assert sut.iceberg_parent_namespace_qualified_name == f"{CATALOG_QN}/sales/emea"
    assert sut.iceberg_namespace_hierarchy == [
        {"qualifiedName": f"{CATALOG_QN}/sales", "name": "sales"},
        {"qualifiedName": f"{CATALOG_QN}/sales/emea", "name": "emea"},
        {"qualifiedName": f"{CATALOG_QN}/sales/emea/uk", "name": "uk"},
    ]


def test_namespace_serializes_catalog_relationship():
    sut = IcebergNamespace.creator(name="sales", parent_qualified_name=CATALOG_QN)

    payload = json.loads(sut.to_json())
    database = payload["relationshipAttributes"]["database"]

    assert database["typeName"] == "IcebergCatalog"
    assert database["uniqueAttributes"]["qualifiedName"] == CATALOG_QN


@pytest.mark.parametrize(
    "name, parent_qualified_name, message",
    [
        (None, CATALOG_QN, "name is required"),
        ("", CATALOG_QN, "name cannot be blank"),
        ("sales", None, "parent_qualified_name is required"),
        ("sales", " ", "parent_qualified_name cannot be blank"),
        ("sales", CONN, "Invalid parent_qualified_name"),
    ],
)
def test_namespace_creator_rejects_bad_inputs(name, parent_qualified_name, message):
    with pytest.raises(ValueError, match=message):
        IcebergNamespace.creator(name=name, parent_qualified_name=parent_qualified_name)


# --- IcebergTable -------------------------------------------------------------


@pytest.mark.parametrize(
    "dotted, expected_qn",
    [
        ("sales", "default/iceberg/1712345678/lakehouse/sales/orders"),
        ("sales.emea", "default/iceberg/1712345678/lakehouse/sales/emea/orders"),
        ("sales.emea.uk", "default/iceberg/1712345678/lakehouse/sales/emea/uk/orders"),
    ],
)
def test_table_creator_matches_app_qualified_name(dotted, expected_qn):
    sut = IcebergTable.creator(
        name="orders", namespace_qualified_name=_namespace(dotted).qualified_name
    )

    assert sut.qualified_name == expected_qn
    assert sut.qualified_name == _app_table_qn(dotted, "orders")
    assert sut.name == "orders"
    sut.validate(for_creation=True)


def test_table_in_top_level_namespace_attributes():
    ns_qn = f"{CATALOG_QN}/sales"
    sut = IcebergTable.creator(name="orders", namespace_qualified_name=ns_qn)

    assert sut.connection_qualified_name == CONN
    assert sut.connector_name == "iceberg"
    assert sut.database_name == CATALOG
    assert sut.database_qualified_name == CATALOG_QN
    assert sut.schema_name == "sales"
    assert sut.schema_qualified_name == ns_qn
    assert sut.atlan_schema.qualified_name == ns_qn
    assert sut.atlan_schema.type_name == "IcebergNamespace"
    assert sut.iceberg_parent_namespace_qualified_name is None
    assert sut.iceberg_namespace_hierarchy == [
        {"qualifiedName": ns_qn, "name": "sales"}
    ]


def test_table_in_nested_namespace_attributes():
    ns_qn = f"{CATALOG_QN}/sales/emea"
    sut = IcebergTable.creator(name="orders", namespace_qualified_name=ns_qn)

    # Same values the app emits for a nested namespace.
    assert sut.schema_name == "emea"
    assert sut.schema_qualified_name == ns_qn
    assert sut.iceberg_parent_namespace_qualified_name == ns_qn
    assert sut.iceberg_namespace_hierarchy == [
        {"qualifiedName": f"{CATALOG_QN}/sales", "name": "sales"},
        {"qualifiedName": ns_qn, "name": "emea"},
    ]


@pytest.mark.parametrize(
    "name, namespace_qualified_name, message",
    [
        (None, f"{CATALOG_QN}/sales", "name is required"),
        (" ", f"{CATALOG_QN}/sales", "name cannot be blank"),
        ("orders", None, "namespace_qualified_name is required"),
        ("orders", "", "namespace_qualified_name cannot be blank"),
        ("orders", CATALOG_QN, "Invalid namespace_qualified_name"),
    ],
)
def test_table_creator_rejects_bad_inputs(name, namespace_qualified_name, message):
    with pytest.raises(ValueError, match=message):
        IcebergTable.creator(
            name=name, namespace_qualified_name=namespace_qualified_name
        )


# --- IcebergColumn ------------------------------------------------------------

TABLE_QN = f"{CATALOG_QN}/sales/emea/orders"


@pytest.mark.parametrize("dotted", ["sales", "sales.emea", "sales.emea.uk"])
def test_top_level_column_matches_app_qualified_name(dotted):
    table_qn = _app_table_qn(dotted, "orders")
    sut = IcebergColumn.creator(name="id", table_qualified_name=table_qn, order=1)

    # Top-level column: column_path == column_name.
    assert sut.qualified_name == _app_column_qn(dotted, "orders", "id", "id")
    assert sut.qualified_name == _app_column_qn(dotted, "orders", "id")
    assert sut.qualified_name == f"{table_qn}/id"
    sut.validate(for_creation=True)


def test_nested_column_matches_app_qualified_name():
    # address (struct) -> geo (struct) -> lat, built one level at a time.
    address = IcebergColumn.creator(
        name="address", table_qualified_name=TABLE_QN, order=3
    )
    geo = IcebergColumn.creator(
        name="geo",
        table_qualified_name=TABLE_QN,
        order=2,
        parent_column_qualified_name=address.qualified_name,
    )
    lat = IcebergColumn.creator(
        name="lat",
        table_qualified_name=TABLE_QN,
        order=1,
        parent_column_qualified_name=geo.qualified_name,
    )

    expected = "default/iceberg/1712345678/lakehouse/sales/emea/orders/address/geo/lat"
    # {column_path} variant
    assert lat.qualified_name == expected
    assert lat.qualified_name == _app_column_qn(
        "sales.emea", "orders", "lat", "address/geo/lat"
    )
    # {ancestor_path|join('/')} variant: the app's parent column qn
    assert geo.qualified_name == _app_column_qn(
        "sales.emea", "orders", "/".join(["address", "geo"])
    )
    # {conn}{qn} variant: connection-less qn rebased onto the connection
    assert lat.qualified_name == CONN + "/lakehouse/sales/emea/orders/address/geo/lat"


def test_top_level_column_attributes():
    sut = IcebergColumn.creator(name="id", table_qualified_name=TABLE_QN, order=1)

    assert sut.name == "id"
    assert sut.order == 1
    assert sut.connection_qualified_name == CONN
    assert sut.connector_name == "iceberg"
    assert sut.database_name == CATALOG
    assert sut.database_qualified_name == CATALOG_QN
    assert sut.schema_name == "emea"
    assert sut.schema_qualified_name == f"{CATALOG_QN}/sales/emea"
    assert sut.table_name == "orders"
    assert sut.table_qualified_name == TABLE_QN
    assert sut.table.qualified_name == TABLE_QN
    assert sut.table.type_name == "IcebergTable"
    assert sut.column_depth_level == 1
    assert sut.iceberg_parent_namespace_qualified_name == f"{CATALOG_QN}/sales/emea"
    assert sut.iceberg_namespace_hierarchy == [
        {"qualifiedName": f"{CATALOG_QN}/sales", "name": "sales"},
        {"qualifiedName": f"{CATALOG_QN}/sales/emea", "name": "emea"},
    ]
    # Parent-column attributes are left unset for a top-level column.
    assert not sut.parent_column_name
    assert not sut.parent_column_qualified_name
    assert not sut.column_hierarchy


def test_nested_column_attributes():
    sut = IcebergColumn.creator(
        name="lat",
        table_qualified_name=TABLE_QN,
        order=1,
        parent_column_qualified_name=f"{TABLE_QN}/address/geo",
    )

    # The app links nested columns to the table too, not to the parent column.
    assert sut.table.qualified_name == TABLE_QN
    assert sut.table_qualified_name == TABLE_QN
    assert sut.parent_column_name == "geo"
    assert sut.parent_column_qualified_name == f"{TABLE_QN}/address/geo"
    assert sut.column_depth_level == 3
    assert sut.column_hierarchy == [
        {"name": "address", "depth": "1", "qualifiedName": f"{TABLE_QN}/address"},
        {"name": "geo", "depth": "2", "qualifiedName": f"{TABLE_QN}/address/geo"},
    ]


def test_column_in_top_level_namespace_has_no_parent_namespace():
    sut = IcebergColumn.creator(
        name="id", table_qualified_name=f"{CATALOG_QN}/sales/orders", order=1
    )

    assert sut.schema_name == "sales"
    assert sut.iceberg_parent_namespace_qualified_name is None


def test_column_serializes_table_relationship():
    sut = IcebergColumn.creator(name="id", table_qualified_name=TABLE_QN, order=1)

    payload = json.loads(sut.to_json())
    table = payload["relationshipAttributes"]["table"]

    assert table["typeName"] == "IcebergTable"
    assert table["uniqueAttributes"]["qualifiedName"] == TABLE_QN


@pytest.mark.parametrize(
    "kwargs, message",
    [
        ({"name": None}, "name is required"),
        ({"name": " "}, "name cannot be blank"),
        ({"table_qualified_name": None}, "table_qualified_name is required"),
        ({"table_qualified_name": ""}, "table_qualified_name cannot be blank"),
        ({"order": None}, "order is required"),
        ({"order": -1}, "Order must be a non-negative integer"),
        (
            {"table_qualified_name": f"{CATALOG_QN}/orders"},
            "Invalid table_qualified_name",
        ),
        (
            {"parent_column_qualified_name": " "},
            "parent_column_qualified_name cannot be blank",
        ),
        (
            {"parent_column_qualified_name": f"{CATALOG_QN}/sales/other/address"},
            "Invalid parent_column_qualified_name",
        ),
        (
            {"parent_column_qualified_name": f"{TABLE_QN}/"},
            "Invalid parent_column_qualified_name",
        ),
    ],
)
def test_column_creator_rejects_bad_inputs(kwargs, message):
    args = {"name": "id", "table_qualified_name": TABLE_QN, "order": 1, **kwargs}
    with pytest.raises(ValueError, match=message):
        IcebergColumn.creator(**args)


# --- create aliases -----------------------------------------------------------


def test_create_aliases():
    assert (
        IcebergCatalog.create(
            name=CATALOG, connection_qualified_name=CONN
        ).qualified_name
        == CATALOG_QN
    )
    assert (
        IcebergNamespace.create(
            name="sales", parent_qualified_name=CATALOG_QN
        ).qualified_name
        == f"{CATALOG_QN}/sales"
    )
    assert (
        IcebergTable.create(
            name="orders", namespace_qualified_name=f"{CATALOG_QN}/sales"
        ).qualified_name
        == f"{CATALOG_QN}/sales/orders"
    )
    assert (
        IcebergColumn.create(
            name="id", table_qualified_name=TABLE_QN, order=1
        ).qualified_name
        == f"{TABLE_QN}/id"
    )
