# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Salesforce creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-salesforce-app emits today
(FND-3838 census), so a creator change that would re-key existing Salesforce assets
fails here.
"""

import pytest

from pyatlan_v9.model import (
    SalesforceDashboard,
    SalesforceField,
    SalesforceObject,
    SalesforceOrganization,
    SalesforceReport,
)

CONNECTION_QN = "default/salesforce/1712345678"
ORG_ID = "00D5g000004XyZaEAK"
ORG_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK"
OBJECT_API_NAME = "Account"
OBJECT_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK/Account"
FIELD_API_NAME = "Annual_Revenue__c"
FIELD_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK/Account/Annual_Revenue__c"
REPORT_ID = "00O5g000004AbCdEAF"
REPORT_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK/00O5g000004AbCdEAF"
DASHBOARD_ID = "01Z5g000000AbCdEAF"
DASHBOARD_QN = "default/salesforce/1712345678/00D5g000004XyZaEAK/01Z5g000000AbCdEAF"
NAME = "Quarterly Revenue"


def _assert_common(sut, expected_qn):
    assert sut.qualified_name == expected_qn
    assert sut.name == NAME
    assert sut.connection_qualified_name == CONNECTION_QN
    assert sut.connector_name == "salesforce"
    # SalesforceOrganization has no containment parent, so it has no pattern.
    pattern = getattr(sut, "_QUALIFIED_NAME_PATTERN", None)
    if pattern is not None:
        assert pattern.match(sut.qualified_name)
    sut.validate()


def test_organization_creator_matches_app_qualified_name():
    sut = SalesforceOrganization.creator(
        name=NAME, connection_qualified_name=CONNECTION_QN, source_id=ORG_ID
    )

    _assert_common(sut, ORG_QN)
    assert sut.source_id == ORG_ID
    sut.validate(for_creation=True)


def test_object_creator_matches_app_qualified_name():
    sut = SalesforceObject.creator(
        name=NAME, api_name=OBJECT_API_NAME, organization_qualified_name=ORG_QN
    )

    _assert_common(sut, OBJECT_QN)
    assert sut.api_name == OBJECT_API_NAME
    assert sut.organization_qualified_name == ORG_QN
    assert sut.organization.qualified_name == ORG_QN
    sut.validate(for_creation=True)


def test_field_creator_matches_app_qualified_name():
    sut = SalesforceField.creator(
        name=NAME, api_name=FIELD_API_NAME, object_qualified_name=OBJECT_QN
    )

    _assert_common(sut, FIELD_QN)
    assert sut.api_name == FIELD_API_NAME
    assert sut.object_qualified_name == OBJECT_QN
    assert sut.organization_qualified_name == ORG_QN
    assert sut.object.qualified_name == OBJECT_QN
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "asset_type, source_id, expected_qn",
    [
        (SalesforceReport, REPORT_ID, REPORT_QN),
        (SalesforceDashboard, DASHBOARD_ID, DASHBOARD_QN),
    ],
)
def test_report_and_dashboard_creator_matches_app_qualified_name(
    asset_type, source_id, expected_qn
):
    sut = asset_type.creator(
        name=NAME, source_id=source_id, organization_qualified_name=ORG_QN
    )

    _assert_common(sut, expected_qn)
    assert sut.source_id == source_id
    assert sut.organization_qualified_name == ORG_QN
    assert sut.organization.qualified_name == ORG_QN
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "asset_type, kwargs",
    [
        (
            SalesforceObject,
            {"api_name": OBJECT_API_NAME, "organization_qualified_name": ORG_QN},
        ),
        (
            SalesforceField,
            {"api_name": FIELD_API_NAME, "object_qualified_name": OBJECT_QN},
        ),
        (
            SalesforceReport,
            {"source_id": REPORT_ID, "organization_qualified_name": ORG_QN},
        ),
        (
            SalesforceDashboard,
            {"source_id": DASHBOARD_ID, "organization_qualified_name": ORG_QN},
        ),
    ],
)
def test_explicit_connection_qualified_name_is_kept(asset_type, kwargs):
    sut = asset_type.creator(
        name=NAME, connection_qualified_name=CONNECTION_QN, **kwargs
    )

    assert sut.connection_qualified_name == CONNECTION_QN


VALID_KWARGS = {
    SalesforceOrganization: {
        "name": NAME,
        "connection_qualified_name": CONNECTION_QN,
        "source_id": ORG_ID,
    },
    SalesforceObject: {
        "name": NAME,
        "api_name": OBJECT_API_NAME,
        "organization_qualified_name": ORG_QN,
    },
    SalesforceField: {
        "name": NAME,
        "api_name": FIELD_API_NAME,
        "object_qualified_name": OBJECT_QN,
    },
    SalesforceReport: {
        "name": NAME,
        "source_id": REPORT_ID,
        "organization_qualified_name": ORG_QN,
    },
    SalesforceDashboard: {
        "name": NAME,
        "source_id": DASHBOARD_ID,
        "organization_qualified_name": ORG_QN,
    },
}

REQUIRED = [
    (asset_type, key) for asset_type, kwargs in VALID_KWARGS.items() for key in kwargs
]


@pytest.mark.parametrize("asset_type, key", REQUIRED)
def test_creator_rejects_missing_input(asset_type, key):
    kwargs = {**VALID_KWARGS[asset_type], key: None}

    with pytest.raises(ValueError, match=f"{key} is required"):
        asset_type.creator(**kwargs)


@pytest.mark.parametrize("asset_type, key", REQUIRED)
def test_creator_rejects_blank_input(asset_type, key):
    kwargs = {**VALID_KWARGS[asset_type], key: "  "}

    with pytest.raises(ValueError, match=f"{key} cannot be blank"):
        asset_type.creator(**kwargs)


@pytest.mark.parametrize(
    "asset_type, key, value",
    [
        (SalesforceObject, "organization_qualified_name", CONNECTION_QN),
        (SalesforceReport, "organization_qualified_name", CONNECTION_QN),
        (SalesforceDashboard, "organization_qualified_name", CONNECTION_QN),
        (SalesforceField, "object_qualified_name", ORG_QN),
    ],
)
def test_creator_rejects_too_short_parent_qualified_name(asset_type, key, value):
    kwargs = {**VALID_KWARGS[asset_type], key: value}

    with pytest.raises(ValueError, match=f"{key} is invalid"):
        asset_type.creator(**kwargs)


@pytest.mark.parametrize("asset_type", list(VALID_KWARGS))
def test_create_alias(asset_type):
    kwargs = VALID_KWARGS[asset_type]

    assert (
        asset_type.create(**kwargs).qualified_name
        == asset_type.creator(**kwargs).qualified_name
    )
