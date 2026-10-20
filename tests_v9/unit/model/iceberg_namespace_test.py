# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for IcebergNamespace.creator in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-iceberg-app emits
(``_build_namespace_qn``: dotted namespace ``a.b`` -> ``{catalog}/a/b``,
FND-3838 census). Namespaces nest to any depth, so each case is checked at 1, 2
and 3 levels.
"""

import pytest

from pyatlan_v9.model import IcebergNamespace

CONNECTION_QN = "default/iceberg/1712345678"
CATALOG_QN = "default/iceberg/1712345678/lakehouse"


def _namespace(dotted):
    """Build a namespace the way a caller adopting the creator would: one level at a time."""
    parent_qn = CATALOG_QN
    sut = None
    for segment in dotted.split("."):
        sut = IcebergNamespace.creator(name=segment, parent_qualified_name=parent_qn)
        parent_qn = sut.qualified_name
    return sut


@pytest.mark.parametrize(
    "dotted, expected_qn",
    [
        ("sales", "default/iceberg/1712345678/lakehouse/sales"),
        ("sales.emea", "default/iceberg/1712345678/lakehouse/sales/emea"),
        ("sales.emea.uk", "default/iceberg/1712345678/lakehouse/sales/emea/uk"),
    ],
)
def test_creator_matches_app_qualified_name(dotted, expected_qn):
    sut = _namespace(dotted)

    assert sut.qualified_name == expected_qn
    assert sut.name == dotted.split(".")[-1]
    sut.validate(for_creation=True)


def test_top_level_namespace_attributes():
    sut = IcebergNamespace.creator(name="sales", parent_qualified_name=CATALOG_QN)

    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "iceberg"
    assert sut.database_name == "lakehouse"
    assert sut.database_qualified_name == CATALOG_QN
    assert sut.database.type_name == "IcebergCatalog"
    assert sut.database.unique_attributes == {"qualifiedName": CATALOG_QN}
    assert sut.iceberg_parent_namespace_qualified_name is None
    assert sut.iceberg_namespace_hierarchy == [
        {"qualifiedName": "default/iceberg/1712345678/lakehouse/sales", "name": "sales"}
    ]


def test_nested_namespace_attributes():
    sut = _namespace("sales.emea.uk")

    assert sut.database_name == "lakehouse"
    assert sut.database_qualified_name == CATALOG_QN
    # The app links every namespace to the catalog, nested or not.
    assert sut.database.unique_attributes == {"qualifiedName": CATALOG_QN}
    # The app sets the first namespace segment here, not the immediate parent
    # (asset_mapper.map_namespace). The creator matches it.
    assert (
        sut.iceberg_parent_namespace_qualified_name
        == "default/iceberg/1712345678/lakehouse/sales"
    )
    assert sut.iceberg_namespace_hierarchy == [
        {
            "qualifiedName": "default/iceberg/1712345678/lakehouse/sales",
            "name": "sales",
        },
        {
            "qualifiedName": "default/iceberg/1712345678/lakehouse/sales/emea",
            "name": "emea",
        },
        {
            "qualifiedName": "default/iceberg/1712345678/lakehouse/sales/emea/uk",
            "name": "uk",
        },
    ]


def test_create_alias():
    assert (
        IcebergNamespace.create(
            name="sales", parent_qualified_name=CATALOG_QN
        ).qualified_name
        == "default/iceberg/1712345678/lakehouse/sales"
    )


@pytest.mark.parametrize("param", ["name", "parent_qualified_name"])
@pytest.mark.parametrize(
    "value, message", [(None, "is required"), ("  ", "cannot be blank")]
)
def test_creator_rejects_missing_or_blank_inputs(param, value, message):
    args = {"name": "sales", "parent_qualified_name": CATALOG_QN, param: value}
    with pytest.raises(ValueError, match=f"{param} {message}"):
        IcebergNamespace.creator(**args)


def test_creator_rejects_malformed_parent_qualified_name():
    # A connection qn: one segment short of a catalog.
    with pytest.raises(ValueError, match="Invalid parent_qualified_name"):
        IcebergNamespace.creator(name="sales", parent_qualified_name=CONNECTION_QN)


def test_updater():
    qn = "default/iceberg/1712345678/lakehouse/sales"
    sut = IcebergNamespace.updater(qualified_name=qn, name="sales")

    assert sut.qualified_name == qn
    assert sut.name == "sales"


@pytest.mark.parametrize("param", ["qualified_name", "name"])
def test_updater_rejects_missing_inputs(param):
    args = {"qualified_name": f"{CATALOG_QN}/sales", "name": "sales", param: None}
    with pytest.raises(ValueError, match=f"{param} is required"):
        IcebergNamespace.updater(**args)


def test_trim_to_required():
    sut = _namespace("sales.emea").trim_to_required()

    assert isinstance(sut, IcebergNamespace)
    assert sut.qualified_name == "default/iceberg/1712345678/lakehouse/sales/emea"
    assert sut.name == "emea"
