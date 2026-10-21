# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SalesforceField.creator in pyatlan_v9.

The expected qualifiedName is the exact string atlan-salesforce-app emits today
(app/asset_mapper.py map_field, FND-3838 census), so a creator change that would re-key
existing Salesforce assets fails here.
"""

import pytest

from pyatlan_v9.model import SalesforceField

CONNECTION_QN = "default/salesforce/1712345678"
ORG_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK"
OBJECT_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK/Account"
NAME = "Annual Revenue"
VALID = {
    "name": NAME,
    "api_name": "Annual_Revenue__c",
    "object_qualified_name": OBJECT_QN,
}
EXPECTED_QN = (
    "default/salesforce/1712345678/00D5g000004XyZaEAK/Account/Annual_Revenue__c"
)


def test_creator_matches_app_qualified_name():
    sut = SalesforceField.creator(**VALID)

    assert sut.qualified_name == (
        "default/salesforce/1712345678/00D5g000004XyZaEAK/Account/Annual_Revenue__c"
    )
    assert sut.name == NAME
    assert sut.api_name == "Annual_Revenue__c"
    assert sut.object_qualified_name == OBJECT_QN
    assert sut.organization_qualified_name == ORG_QN
    assert sut.object.qualified_name == OBJECT_QN
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


@pytest.mark.parametrize("value", [ORG_QN, "default/salesforce"])
def test_creator_rejects_too_short_object_qualified_name(value):
    with pytest.raises(ValueError, match="object_qualified_name is invalid"):
        SalesforceField.creator(**{**VALID, "object_qualified_name": value})


def test_creator_derives_connection_qualified_name():
    sut = SalesforceField.creator(**VALID)

    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "salesforce"


def test_creator_keeps_explicit_connection_qualified_name():
    sut = SalesforceField.creator(**VALID, connection_qualified_name=CONNECTION_QN)

    assert sut.connection_qualified_name == CONNECTION_QN


@pytest.mark.parametrize("key", list(VALID))
def test_creator_rejects_missing_input(key):
    with pytest.raises(ValueError, match=f"{key} is required"):
        SalesforceField.creator(**{**VALID, key: None})


@pytest.mark.parametrize("key", list(VALID))
def test_creator_rejects_blank_input(key):
    with pytest.raises(ValueError, match=f"{key} cannot be blank"):
        SalesforceField.creator(**{**VALID, key: "  "})


def test_create_alias():
    assert SalesforceField.create(**VALID).qualified_name == EXPECTED_QN


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        ("", "x", "qualified_name is required"),
        (EXPECTED_QN, "", "name is required"),
    ],
)
def test_updater_rejects_missing_input(qualified_name, name, message):
    with pytest.raises(ValueError, match=message):
        SalesforceField.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = SalesforceField.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = SalesforceField.creator(**VALID).trim_to_required()

    assert isinstance(sut, SalesforceField)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
