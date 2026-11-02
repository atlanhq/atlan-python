# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for FivetranConnector model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-fivetran-app emits today
(``{connectionQN}/{sha1(connectorId + "-" + destinationId)}``, FND-3838 census),
so a creator change that would re-key existing connectors fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import FivetranConnector

CONNECTION_QUALIFIED_NAME = "default/fivetran/123456789"
CONNECTOR_NAME = "fivetran"
NAME = "salesforce → snowflake"
CONNECTOR_ID = "wobbly_ferret"
DESTINATION_ID = "hopeful_pigeon"
# sha1("wobbly_ferret-hopeful_pigeon").hexdigest(), computed independently
CONNECTOR_QUALIFIED_NAME = (
    f"{CONNECTION_QUALIFIED_NAME}/bd704c55ea740cfdb7434fe81dab27adc4fe5918"
)


def test_creator_matches_app_qualified_name():
    """Mirror atlan-fivetran-app's _build_connector_qualified_name inputs and output."""
    sut = FivetranConnector.creator(
        name="salesforce → snowflake",
        connector_id="wobbly_ferret",
        destination_id="hopeful_pigeon",
        connection_qualified_name="default/fivetran/1700000000",
    )

    assert (
        sut.qualified_name
        == "default/fivetran/1700000000/bd704c55ea740cfdb7434fe81dab27adc4fe5918"
    )
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connector_id, destination_id, connection_qualified_name, message",
    [
        (
            None,
            CONNECTOR_ID,
            DESTINATION_ID,
            CONNECTION_QUALIFIED_NAME,
            "name is required",
        ),
        (
            " ",
            CONNECTOR_ID,
            DESTINATION_ID,
            CONNECTION_QUALIFIED_NAME,
            "name cannot be blank",
        ),
        (
            NAME,
            None,
            DESTINATION_ID,
            CONNECTION_QUALIFIED_NAME,
            "connector_id is required",
        ),
        (
            NAME,
            " ",
            DESTINATION_ID,
            CONNECTION_QUALIFIED_NAME,
            "connector_id cannot be blank",
        ),
        (
            NAME,
            CONNECTOR_ID,
            None,
            CONNECTION_QUALIFIED_NAME,
            "destination_id is required",
        ),
        (
            NAME,
            CONNECTOR_ID,
            " ",
            CONNECTION_QUALIFIED_NAME,
            "destination_id cannot be blank",
        ),
        (
            NAME,
            CONNECTOR_ID,
            DESTINATION_ID,
            None,
            "connection_qualified_name is required",
        ),
        (
            NAME,
            CONNECTOR_ID,
            DESTINATION_ID,
            " ",
            "connection_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    connector_id: str,
    destination_id: str,
    connection_qualified_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        FivetranConnector.creator(
            name=name,
            connector_id=connector_id,
            destination_id=destination_id,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets denormalised connection attributes and app URLs."""
    sut = FivetranConnector.creator(
        name=NAME,
        connector_id=CONNECTOR_ID,
        destination_id=DESTINATION_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.type_name == "FivetranConnector"
    assert sut.name == NAME
    assert sut.qualified_name == CONNECTOR_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.fivetran_connector_url == (
        "https://fivetran.com/dashboard/connectors/wobbly_ferret"
        "/status?groupId=hopeful_pigeon"
    )
    assert sut.source_url == sut.fivetran_connector_url
    assert sut.fivetran_connector_destination_url == (
        "https://fivetran.com/dashboard/warehouse?groupId=hopeful_pigeon"
    )
    assert sut.guid
    sut.validate(for_creation=True)


def test_creator_hash_depends_on_id_order():
    """connector_id and destination_id are not interchangeable in the hash."""
    swapped = FivetranConnector.creator(
        name=NAME,
        connector_id=DESTINATION_ID,
        destination_id=CONNECTOR_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert swapped.qualified_name != CONNECTOR_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, NAME, "qualified_name is required"),
        (CONNECTOR_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        FivetranConnector.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a FivetranConnector for modification."""
    sut = FivetranConnector.updater(qualified_name=CONNECTOR_QUALIFIED_NAME, name=NAME)

    assert sut.qualified_name == CONNECTOR_QUALIFIED_NAME
    assert sut.name == NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = FivetranConnector.creator(
        name=NAME,
        connector_id=CONNECTOR_ID,
        destination_id=DESTINATION_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == CONNECTOR_QUALIFIED_NAME
    assert sut.name == NAME
    assert sut.fivetran_connector_url is UNSET
