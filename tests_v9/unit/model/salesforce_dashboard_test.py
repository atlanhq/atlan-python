# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SalesforceDashboard.creator in pyatlan_v9.

The expected qualifiedName is the exact string atlan-salesforce-app emits today
(app/asset_mapper.py map_dashboard, FND-3838 census), so a creator change that would re-key
existing Salesforce assets fails here.
"""

import pytest

from pyatlan_v9.model import SalesforceDashboard

CONNECTION_QN = "default/salesforce/1712345678"
ORG_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK"
NAME = "Quarterly Revenue"
VALID = {
    "name": NAME,
    "source_id": "01Z5g000000AbCdEAF",
    "organization_qualified_name": ORG_QN,
}
EXPECTED_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK/01Z5g000000AbCdEAF"


def test_creator_matches_app_qualified_name():
    sut = SalesforceDashboard.creator(**VALID)

    assert (
        sut.qualified_name
        == "default/salesforce/1712345678/00D5g000004XyZaEAK/01Z5g000000AbCdEAF"
    )
    assert sut.name == NAME
    assert sut.source_id == "01Z5g000000AbCdEAF"
    assert sut.organization_qualified_name == ORG_QN
    assert sut.organization.qualified_name == ORG_QN
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


@pytest.mark.parametrize("value", [CONNECTION_QN, "default"])
def test_creator_rejects_too_short_organization_qualified_name(value):
    with pytest.raises(ValueError, match="organization_qualified_name is invalid"):
        SalesforceDashboard.creator(**{**VALID, "organization_qualified_name": value})


def test_creator_derives_connection_qualified_name():
    sut = SalesforceDashboard.creator(**VALID)

    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "salesforce"


def test_creator_keeps_explicit_connection_qualified_name():
    sut = SalesforceDashboard.creator(**VALID, connection_qualified_name=CONNECTION_QN)

    assert sut.connection_qualified_name == CONNECTION_QN


@pytest.mark.parametrize("key", list(VALID))
def test_creator_rejects_missing_input(key):
    with pytest.raises(ValueError, match=f"{key} is required"):
        SalesforceDashboard.creator(**{**VALID, key: None})


@pytest.mark.parametrize("key", list(VALID))
def test_creator_rejects_blank_input(key):
    with pytest.raises(ValueError, match=f"{key} cannot be blank"):
        SalesforceDashboard.creator(**{**VALID, key: "  "})


def test_create_alias():
    assert SalesforceDashboard.create(**VALID).qualified_name == EXPECTED_QN


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        ("", "x", "qualified_name is required"),
        (EXPECTED_QN, "", "name is required"),
    ],
)
def test_updater_rejects_missing_input(qualified_name, name, message):
    with pytest.raises(ValueError, match=message):
        SalesforceDashboard.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = SalesforceDashboard.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = SalesforceDashboard.creator(**VALID).trim_to_required()

    assert isinstance(sut, SalesforceDashboard)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
