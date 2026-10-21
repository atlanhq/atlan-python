# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SalesforceObject.creator in pyatlan_v9.

The expected qualifiedName is the exact string atlan-salesforce-app emits today
(app/asset_mapper.py map_object, FND-3838 census), so a creator change that would re-key
existing Salesforce assets fails here.
"""

import pytest

from pyatlan_v9.model import SalesforceObject

CONNECTION_QN = "default/salesforce/1712345678"
ORG_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK"
NAME = "Account"
VALID = {
    "name": NAME,
    "api_name": "Account",
    "organization_qualified_name": ORG_QN,
}
EXPECTED_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK/Account"


def test_creator_matches_app_qualified_name():
    sut = SalesforceObject.creator(**VALID)

    assert (
        sut.qualified_name == "default/salesforce/1712345678/00D5g000004XyZaEAK/Account"
    )
    assert sut.name == NAME
    assert sut.api_name == "Account"
    assert sut.organization_qualified_name == ORG_QN
    assert sut.organization.qualified_name == ORG_QN
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_creator_uses_api_name_not_label_in_qualified_name():
    sut = SalesforceObject.creator(
        name="Custom Thing", api_name="My_Thing__c", organization_qualified_name=ORG_QN
    )

    assert sut.qualified_name == f"{ORG_QN}/My_Thing__c"
    assert sut.name == "Custom Thing"


@pytest.mark.parametrize("value", [CONNECTION_QN, "default"])
def test_creator_rejects_too_short_organization_qualified_name(value):
    with pytest.raises(ValueError, match="organization_qualified_name is invalid"):
        SalesforceObject.creator(**{**VALID, "organization_qualified_name": value})


def test_creator_derives_connection_qualified_name():
    sut = SalesforceObject.creator(**VALID)

    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "salesforce"


def test_creator_keeps_explicit_connection_qualified_name():
    sut = SalesforceObject.creator(**VALID, connection_qualified_name=CONNECTION_QN)

    assert sut.connection_qualified_name == CONNECTION_QN


@pytest.mark.parametrize("key", list(VALID))
def test_creator_rejects_missing_input(key):
    with pytest.raises(ValueError, match=f"{key} is required"):
        SalesforceObject.creator(**{**VALID, key: None})


@pytest.mark.parametrize("key", list(VALID))
def test_creator_rejects_blank_input(key):
    with pytest.raises(ValueError, match=f"{key} cannot be blank"):
        SalesforceObject.creator(**{**VALID, key: "  "})


def test_create_alias():
    assert SalesforceObject.create(**VALID).qualified_name == EXPECTED_QN


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        ("", "x", "qualified_name is required"),
        (EXPECTED_QN, "", "name is required"),
    ],
)
def test_updater_rejects_missing_input(qualified_name, name, message):
    with pytest.raises(ValueError, match=message):
        SalesforceObject.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = SalesforceObject.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = SalesforceObject.creator(**VALID).trim_to_required()

    assert isinstance(sut, SalesforceObject)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
