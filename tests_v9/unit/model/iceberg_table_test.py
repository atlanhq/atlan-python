# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for IcebergTable.creator in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-iceberg-app emits
(``_build_table_qn``: ``{catalog}/{namespace with . -> /}/{table}``, FND-3838
census), checked in namespaces 1, 2 and 3 levels deep.
"""

import pytest

from pyatlan_v9.model import IcebergTable

CONNECTION_QN = "default/iceberg/1712345678"
CATALOG_QN = "default/iceberg/1712345678/lakehouse"
NAMESPACE_QN = "default/iceberg/1712345678/lakehouse/sales/emea"
EXPECTED_QN = "default/iceberg/1712345678/lakehouse/sales/emea/orders"


def _creator(**overrides):
    return IcebergTable.creator(
        **{"name": "orders", "namespace_qualified_name": NAMESPACE_QN, **overrides}
    )


@pytest.mark.parametrize(
    "namespace_qn, expected_qn",
    [
        (
            "default/iceberg/1712345678/lakehouse/sales",
            "default/iceberg/1712345678/lakehouse/sales/orders",
        ),
        (
            "default/iceberg/1712345678/lakehouse/sales/emea",
            "default/iceberg/1712345678/lakehouse/sales/emea/orders",
        ),
        (
            "default/iceberg/1712345678/lakehouse/sales/emea/uk",
            "default/iceberg/1712345678/lakehouse/sales/emea/uk/orders",
        ),
    ],
)
def test_creator_matches_app_qualified_name(namespace_qn, expected_qn):
    sut = _creator(namespace_qualified_name=namespace_qn)

    assert sut.qualified_name == expected_qn
    assert sut.name == "orders"
    sut.validate(for_creation=True)


def test_table_in_top_level_namespace_attributes():
    ns_qn = "default/iceberg/1712345678/lakehouse/sales"
    sut = _creator(namespace_qualified_name=ns_qn)

    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "iceberg"
    assert sut.database_name == "lakehouse"
    assert sut.database_qualified_name == CATALOG_QN
    assert sut.schema_name == "sales"
    assert sut.schema_qualified_name == ns_qn
    assert sut.atlan_schema.type_name == "IcebergNamespace"
    assert sut.atlan_schema.unique_attributes == {"qualifiedName": ns_qn}
    assert sut.iceberg_parent_namespace_qualified_name is None
    assert sut.iceberg_namespace_hierarchy == [
        {"qualifiedName": ns_qn, "name": "sales"}
    ]


def test_table_in_nested_namespace_attributes():
    sut = _creator()

    # Same values the app emits for a table in a nested namespace.
    assert sut.schema_name == "emea"
    assert sut.schema_qualified_name == NAMESPACE_QN
    assert sut.atlan_schema.unique_attributes == {"qualifiedName": NAMESPACE_QN}
    assert sut.iceberg_parent_namespace_qualified_name == NAMESPACE_QN
    assert sut.iceberg_namespace_hierarchy == [
        {
            "qualifiedName": "default/iceberg/1712345678/lakehouse/sales",
            "name": "sales",
        },
        {"qualifiedName": NAMESPACE_QN, "name": "emea"},
    ]


def test_create_alias():
    assert (
        IcebergTable.create(
            name="orders", namespace_qualified_name=NAMESPACE_QN
        ).qualified_name
        == EXPECTED_QN
    )


@pytest.mark.parametrize("param", ["name", "namespace_qualified_name"])
@pytest.mark.parametrize(
    "value, message", [(None, "is required"), ("  ", "cannot be blank")]
)
def test_creator_rejects_missing_or_blank_inputs(param, value, message):
    with pytest.raises(ValueError, match=f"{param} {message}"):
        _creator(**{param: value})


def test_creator_rejects_malformed_namespace_qualified_name():
    # A catalog qn: one segment short of a namespace.
    with pytest.raises(ValueError, match="Invalid namespace_qualified_name"):
        _creator(namespace_qualified_name=CATALOG_QN)


def test_updater():
    sut = IcebergTable.updater(qualified_name=EXPECTED_QN, name="orders")

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == "orders"


@pytest.mark.parametrize("param", ["qualified_name", "name"])
def test_updater_rejects_missing_inputs(param):
    args = {"qualified_name": EXPECTED_QN, "name": "orders", param: None}
    with pytest.raises(ValueError, match=f"{param} is required"):
        IcebergTable.updater(**args)


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert isinstance(sut, IcebergTable)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == "orders"
