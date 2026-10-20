# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SalesforceOrganization.creator in pyatlan_v9.

The expected qualifiedName is the exact string atlan-salesforce-app emits today
(app/asset_mapper.py map_organization, FND-3838 census), so a creator change that would re-key
existing Salesforce assets fails here.
"""

import pytest

from pyatlan_v9.model import SalesforceOrganization

CONNECTION_QN = "default/salesforce/1712345678"
NAME = "Acme Corp"
VALID = {
    "name": NAME,
    "connection_qualified_name": CONNECTION_QN,
    "source_id": "00D5g000004XyZaEAK",
}
EXPECTED_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK"


def test_creator_matches_app_qualified_name():
    sut = SalesforceOrganization.creator(**VALID)

    assert sut.qualified_name == "default/salesforce/1712345678/00D5g000004XyZaEAK"
    assert sut.name == NAME
    assert sut.source_id == "00D5g000004XyZaEAK"
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "salesforce"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_validate_rejects_qualified_name_without_org_segment():
    sut = SalesforceOrganization.creator(**VALID)
    sut.qualified_name = "00D5g000004XyZaEAK"

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize("key", list(VALID))
def test_creator_rejects_missing_input(key):
    with pytest.raises(ValueError, match=f"{key} is required"):
        SalesforceOrganization.creator(**{**VALID, key: None})


@pytest.mark.parametrize("key", list(VALID))
def test_creator_rejects_blank_input(key):
    with pytest.raises(ValueError, match=f"{key} cannot be blank"):
        SalesforceOrganization.creator(**{**VALID, key: "  "})


def test_create_alias():
    assert SalesforceOrganization.create(**VALID).qualified_name == EXPECTED_QN


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        ("", "x", "qualified_name is required"),
        (EXPECTED_QN, "", "name is required"),
    ],
)
def test_updater_rejects_missing_input(qualified_name, name, message):
    with pytest.raises(ValueError, match=message):
        SalesforceOrganization.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = SalesforceOrganization.updater(qualified_name=EXPECTED_QN, name=NAME)

    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME


def test_trim_to_required():
    sut = SalesforceOrganization.creator(**VALID).trim_to_required()

    assert isinstance(sut, SalesforceOrganization)
    assert sut.qualified_name == EXPECTED_QN
    assert sut.name == NAME
