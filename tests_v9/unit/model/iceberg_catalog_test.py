# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for IcebergCatalog.creator in pyatlan_v9.

EXPECTED_QN is the exact string atlan-iceberg-app emits for a catalog
(``_build_catalog_qn``, FND-3838 census), so a creator change that would re-key
existing assets fails here.
"""

import pytest

from pyatlan_v9.model import IcebergCatalog

NAME = "lakehouse"
CONNECTION_QN = "default/iceberg/1712345678"
EXPECTED_QN = "default/iceberg/1712345678/lakehouse"


def _creator(**overrides):
    return IcebergCatalog.creator(
        **{"name": NAME, "connection_qualified_name": CONNECTION_QN, **overrides}
    )


def test_creator_matches_app_qualified_name():
    sut = _creator()

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "iceberg"
    sut.validate(for_creation=True)


def test_create_alias():
    assert (
        IcebergCatalog.create(
            name=NAME, connection_qualified_name=CONNECTION_QN
        ).qualified_name
        == EXPECTED_QN
    )


@pytest.mark.parametrize("param", ["name", "connection_qualified_name"])
@pytest.mark.parametrize(
    "value, message", [(None, "is required"), ("  ", "cannot be blank")]
)
def test_creator_rejects_missing_or_blank_inputs(param, value, message):
    with pytest.raises(ValueError, match=f"{param} {message}"):
        _creator(**{param: value})


@pytest.mark.parametrize(
    "bad_qn", ["default/iceberg", "default/iceberg/1712345678/lakehouse"]
)
def test_creator_rejects_malformed_connection_qualified_name(bad_qn):
    with pytest.raises(ValueError, match="Invalid connection_qualified_name"):
        _creator(connection_qualified_name=bad_qn)


def test_updater():
    sut = IcebergCatalog.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


@pytest.mark.parametrize("param", ["qualified_name", "name"])
def test_updater_rejects_missing_inputs(param):
    args = {"qualified_name": EXPECTED_QN, "name": NAME, param: None}
    with pytest.raises(ValueError, match=f"{param} is required"):
        IcebergCatalog.updater(**args)


def test_trim_to_required():
    sut = _creator().trim_to_required()

    assert isinstance(sut, IcebergCatalog)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
