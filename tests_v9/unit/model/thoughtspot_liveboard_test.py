# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for ThoughtspotLiveboard model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-thoughtspot-app emits today
(``{connectionQN}/liveboards/{id}``, app/transformers/liveboard.yaml), so a creator
change that would re-key existing assets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import ThoughtspotLiveboard

CONNECTION_QUALIFIED_NAME = "default/thoughtspot/123456789"
CONNECTOR_NAME = "thoughtspot"
ASSET_NAME = "Sales liveboard"
THOUGHTSPOT_ID = "0f5b8f3e-6a4c-4c1e-9d0a-2b7e1c9d4a11"
QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/liveboards/{THOUGHTSPOT_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-thoughtspot-app's liveboard.yaml inputs and output."""
    sut = ThoughtspotLiveboard.creator(
        name="Sales",
        thoughtspot_id="a1b2c3",
        connection_qualified_name="default/thoughtspot/1700000000",
    )

    assert sut.qualified_name == "default/thoughtspot/1700000000/liveboards/a1b2c3"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, thoughtspot_id, connection_qualified_name, message",
    [
        (None, THOUGHTSPOT_ID, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", THOUGHTSPOT_ID, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (ASSET_NAME, None, CONNECTION_QUALIFIED_NAME, "thoughtspot_id is required"),
        (
            ASSET_NAME,
            " ",
            CONNECTION_QUALIFIED_NAME,
            "thoughtspot_id cannot be blank",
        ),
        (ASSET_NAME, THOUGHTSPOT_ID, None, "connection_qualified_name is required"),
        (
            ASSET_NAME,
            THOUGHTSPOT_ID,
            " ",
            "connection_qualified_name cannot be blank",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, thoughtspot_id: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ThoughtspotLiveboard.creator(
            name=name,
            thoughtspot_id=thoughtspot_id,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the qualified name and denormalised connection attributes."""
    sut = ThoughtspotLiveboard.creator(
        name=ASSET_NAME,
        thoughtspot_id=THOUGHTSPOT_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.type_name == "ThoughtspotLiveboard"
    assert sut.name == ASSET_NAME
    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.guid
    sut.validate(for_creation=True)


def test_validate_rejects_other_type_qualified_name():
    """Test validate enforces the /liveboards/ segment from the qualifiedNameFormula."""
    sut = ThoughtspotLiveboard.updater(
        qualified_name=f"{CONNECTION_QUALIFIED_NAME}/other/{THOUGHTSPOT_ID}",
        name=ASSET_NAME,
    )

    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ASSET_NAME, "qualified_name is required"),
        (QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ThoughtspotLiveboard.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a ThoughtspotLiveboard for modification."""
    sut = ThoughtspotLiveboard.updater(qualified_name=QUALIFIED_NAME, name=ASSET_NAME)

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == ASSET_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = ThoughtspotLiveboard.creator(
        name=ASSET_NAME,
        thoughtspot_id=THOUGHTSPOT_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == QUALIFIED_NAME
    assert sut.name == ASSET_NAME
    assert sut.connection_qualified_name is UNSET
