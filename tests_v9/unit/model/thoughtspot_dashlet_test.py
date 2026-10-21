# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for ThoughtspotDashlet model in pyatlan_v9.

The parity test uses the exact qualifiedName and liveboard reference
atlan-thoughtspot-app emits today (``{connectionQN}/dashlets/{id}`` under
``{connectionQN}/liveboards/{liveboardId}``, app/transformers/dashlet.yaml), so
a creator change that would re-key existing dashlets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import ThoughtspotDashlet

CONNECTION_QUALIFIED_NAME = "default/thoughtspot/123456789"
CONNECTOR_NAME = "thoughtspot"
DASHLET_NAME = "Revenue by region"
THOUGHTSPOT_ID = "7c1d2e3f-4a5b-4c6d-8e9f-0a1b2c3d4e5f"
LIVEBOARD_NAME = "Sales liveboard"
LIVEBOARD_QUALIFIED_NAME = (
    f"{CONNECTION_QUALIFIED_NAME}/liveboards/0f5b8f3e-6a4c-4c1e-9d0a-2b7e1c9d4a11"
)
DASHLET_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/dashlets/{THOUGHTSPOT_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-thoughtspot-app's dashlet.yaml inputs and output."""
    sut = ThoughtspotDashlet.creator(
        name="Revenue",
        thoughtspot_id="d4e5f6",
        thoughtspot_liveboard_qualified_name="default/thoughtspot/1700000000/liveboards/a1b2c3",
        thoughtspot_liveboard_name="Sales",
    )

    assert sut.qualified_name == "default/thoughtspot/1700000000/dashlets/d4e5f6"
    assert sut.connection_qualified_name == "default/thoughtspot/1700000000"
    assert sut.thoughtspot_liveboard_qualified_name == (
        "default/thoughtspot/1700000000/liveboards/a1b2c3"
    )
    assert sut.thoughtspot_liveboard.unique_attributes == {
        "qualifiedName": "default/thoughtspot/1700000000/liveboards/a1b2c3"
    }
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, thoughtspot_id, liveboard_qualified_name, liveboard_name, message",
    [
        (
            None,
            THOUGHTSPOT_ID,
            LIVEBOARD_QUALIFIED_NAME,
            LIVEBOARD_NAME,
            "name is required",
        ),
        (
            " ",
            THOUGHTSPOT_ID,
            LIVEBOARD_QUALIFIED_NAME,
            LIVEBOARD_NAME,
            "name cannot be blank",
        ),
        (
            DASHLET_NAME,
            None,
            LIVEBOARD_QUALIFIED_NAME,
            LIVEBOARD_NAME,
            "thoughtspot_id is required",
        ),
        (
            DASHLET_NAME,
            " ",
            LIVEBOARD_QUALIFIED_NAME,
            LIVEBOARD_NAME,
            "thoughtspot_id cannot be blank",
        ),
        (
            DASHLET_NAME,
            THOUGHTSPOT_ID,
            None,
            LIVEBOARD_NAME,
            "thoughtspot_liveboard_qualified_name is required",
        ),
        (
            DASHLET_NAME,
            THOUGHTSPOT_ID,
            " ",
            LIVEBOARD_NAME,
            "thoughtspot_liveboard_qualified_name cannot be blank",
        ),
        (
            DASHLET_NAME,
            THOUGHTSPOT_ID,
            LIVEBOARD_QUALIFIED_NAME,
            None,
            "thoughtspot_liveboard_name is required",
        ),
        (
            DASHLET_NAME,
            THOUGHTSPOT_ID,
            LIVEBOARD_QUALIFIED_NAME,
            " ",
            "thoughtspot_liveboard_name cannot be blank",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str,
    thoughtspot_id: str,
    liveboard_qualified_name: str,
    liveboard_name: str,
    message: str,
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ThoughtspotDashlet.creator(
            name=name,
            thoughtspot_id=thoughtspot_id,
            thoughtspot_liveboard_qualified_name=liveboard_qualified_name,
            thoughtspot_liveboard_name=liveboard_name,
        )


def test_creator_with_malformed_liveboard_qualified_name_raises_value_error():
    """Test creator rejects a liveboard qualified name with too few segments."""
    with pytest.raises(
        ValueError, match="thoughtspot_liveboard_qualified_name is invalid"
    ):
        ThoughtspotDashlet.creator(
            name=DASHLET_NAME,
            thoughtspot_id=THOUGHTSPOT_ID,
            thoughtspot_liveboard_qualified_name="default/thoughtspot/123456789",
            thoughtspot_liveboard_name=LIVEBOARD_NAME,
        )


def test_creator():
    """Test creator derives the connection and sets the liveboard relationship."""
    sut = ThoughtspotDashlet.creator(
        name=DASHLET_NAME,
        thoughtspot_id=THOUGHTSPOT_ID,
        thoughtspot_liveboard_qualified_name=LIVEBOARD_QUALIFIED_NAME,
        thoughtspot_liveboard_name=LIVEBOARD_NAME,
    )

    assert sut.type_name == "ThoughtspotDashlet"
    assert sut.name == DASHLET_NAME
    assert sut.qualified_name == DASHLET_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.thoughtspot_liveboard_name == LIVEBOARD_NAME
    assert sut.thoughtspot_liveboard_qualified_name == LIVEBOARD_QUALIFIED_NAME
    assert sut.thoughtspot_liveboard.unique_attributes == {
        "qualifiedName": LIVEBOARD_QUALIFIED_NAME
    }
    assert sut.guid
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection_qualified_name():
    """Test an explicit connection qualified name overrides the derived one."""
    sut = ThoughtspotDashlet.creator(
        name=DASHLET_NAME,
        thoughtspot_id=THOUGHTSPOT_ID,
        thoughtspot_liveboard_qualified_name=LIVEBOARD_QUALIFIED_NAME,
        thoughtspot_liveboard_name=LIVEBOARD_NAME,
        connection_qualified_name="default/thoughtspot/987654321",
    )

    assert sut.connection_qualified_name == "default/thoughtspot/987654321"
    assert (
        sut.qualified_name == f"default/thoughtspot/987654321/dashlets/{THOUGHTSPOT_ID}"
    )


def test_validate_for_creation_requires_liveboard():
    """Test validate(for_creation=True) enforces the liveboard containment."""
    sut = ThoughtspotDashlet.updater(
        qualified_name=DASHLET_QUALIFIED_NAME, name=DASHLET_NAME
    )
    sut.connection_qualified_name = CONNECTION_QUALIFIED_NAME

    with pytest.raises(ValueError, match="thoughtspot_liveboard is required"):
        sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DASHLET_NAME, "qualified_name is required"),
        (DASHLET_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        ThoughtspotDashlet.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a ThoughtspotDashlet for modification."""
    sut = ThoughtspotDashlet.updater(
        qualified_name=DASHLET_QUALIFIED_NAME, name=DASHLET_NAME
    )

    assert sut.qualified_name == DASHLET_QUALIFIED_NAME
    assert sut.name == DASHLET_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = ThoughtspotDashlet.creator(
        name=DASHLET_NAME,
        thoughtspot_id=THOUGHTSPOT_ID,
        thoughtspot_liveboard_qualified_name=LIVEBOARD_QUALIFIED_NAME,
        thoughtspot_liveboard_name=LIVEBOARD_NAME,
    ).trim_to_required()

    assert sut.qualified_name == DASHLET_QUALIFIED_NAME
    assert sut.name == DASHLET_NAME
    assert sut.thoughtspot_liveboard is UNSET
