# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SnowflakeShare model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-snowflake-app emits today
(``{connectionQN}/share/{ownerAccount}/{name}``, ``share.yaml``), so a creator
change that would re-key existing shares fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import SnowflakeShare

CONNECTION_QUALIFIED_NAME = "default/snowflake/123456789"
CONNECTOR_NAME = "snowflake"
SHARE_NAME = "SALES_SHARE"
OWNER_ACCOUNT = "ORG1.PROVIDER_ACCT"
SHARE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/share/{OWNER_ACCOUNT}/{SHARE_NAME}"
LISTING_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/listing/GZ1M2N3O4P5"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-snowflake-app's share.yaml inputs and output."""
    sut = SnowflakeShare.creator(
        name="MARKETING_SHARE",
        owner_account="ACME.PROD",
        connection_qualified_name="default/snowflake/1700000000",
    )

    assert (
        sut.qualified_name
        == "default/snowflake/1700000000/share/ACME.PROD/MARKETING_SHARE"
    )
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, owner_account, connection_qualified_name, message",
    [
        (None, OWNER_ACCOUNT, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", OWNER_ACCOUNT, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (SHARE_NAME, None, CONNECTION_QUALIFIED_NAME, "owner_account is required"),
        (SHARE_NAME, " ", CONNECTION_QUALIFIED_NAME, "owner_account cannot be blank"),
        (SHARE_NAME, OWNER_ACCOUNT, None, "connection_qualified_name is required"),
        (SHARE_NAME, OWNER_ACCOUNT, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, owner_account: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SnowflakeShare.creator(
            name=name,
            owner_account=owner_account,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the owner account and denormalised connection attributes."""
    sut = SnowflakeShare.creator(
        name=SHARE_NAME,
        owner_account=OWNER_ACCOUNT,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.type_name == "SnowflakeShare"
    assert sut.name == SHARE_NAME
    assert sut.qualified_name == SHARE_QUALIFIED_NAME
    assert sut.snowflake_share_owner_account == OWNER_ACCOUNT
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.snowflake_share_kind is UNSET
    assert sut.snowflake_listing is UNSET
    assert sut.guid
    sut.validate(for_creation=True)


def test_creator_with_optional_kind_and_listing():
    """Test creator sets the share kind and relates the share to its listing."""
    sut = SnowflakeShare.creator(
        name=SHARE_NAME,
        owner_account=OWNER_ACCOUNT,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
        kind="INBOUND",
        snowflake_listing_qualified_name=LISTING_QUALIFIED_NAME,
    )

    assert sut.qualified_name == SHARE_QUALIFIED_NAME
    assert sut.snowflake_share_kind == "INBOUND"
    assert sut.snowflake_listing.unique_attributes == {
        "qualifiedName": LISTING_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, SHARE_NAME, "qualified_name is required"),
        (SHARE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SnowflakeShare.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a SnowflakeShare for modification."""
    sut = SnowflakeShare.updater(qualified_name=SHARE_QUALIFIED_NAME, name=SHARE_NAME)

    assert sut.qualified_name == SHARE_QUALIFIED_NAME
    assert sut.name == SHARE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SnowflakeShare.creator(
        name=SHARE_NAME,
        owner_account=OWNER_ACCOUNT,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == SHARE_QUALIFIED_NAME
    assert sut.name == SHARE_NAME
    assert sut.snowflake_share_owner_account is UNSET
