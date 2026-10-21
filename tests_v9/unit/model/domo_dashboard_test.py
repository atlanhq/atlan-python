# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for DomoDashboard model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-domo-app emits today
(``{connectionQN}/dashboard/{domoId}``, FND-3838 census), so a creator change that
would re-key existing dashboards fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import DomoDashboard

CONNECTION_QUALIFIED_NAME = "default/domo/123456789"
CONNECTOR_NAME = "domo"
ASSET_NAME = "Sales dashboard"
DOMO_ID = "1938274650"
ASSET_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/dashboard/{DOMO_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-domo-app's map_dashboard inputs and output."""
    sut = DomoDashboard.creator(
        name="Sales dashboard",
        domo_id="1938274650",
        connection_qualified_name="default/domo/1700000000",
    )

    assert sut.qualified_name == "default/domo/1700000000/dashboard/1938274650"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, domo_id, connection_qualified_name, message",
    [
        (None, DOMO_ID, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", DOMO_ID, CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (ASSET_NAME, None, CONNECTION_QUALIFIED_NAME, "domo_id is required"),
        (ASSET_NAME, " ", CONNECTION_QUALIFIED_NAME, "domo_id cannot be blank"),
        (ASSET_NAME, DOMO_ID, None, "connection_qualified_name is required"),
        (ASSET_NAME, DOMO_ID, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, domo_id: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DomoDashboard.creator(
            name=name,
            domo_id=domo_id,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the Domo id and denormalised connection attributes."""
    sut = DomoDashboard.creator(
        name=ASSET_NAME,
        domo_id=DOMO_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.type_name == "DomoDashboard"
    assert sut.name == ASSET_NAME
    assert sut.domo_id == DOMO_ID
    assert sut.qualified_name == ASSET_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.guid
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ASSET_NAME, "qualified_name is required"),
        (ASSET_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DomoDashboard.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a DomoDashboard for modification."""
    sut = DomoDashboard.updater(qualified_name=ASSET_QUALIFIED_NAME, name=ASSET_NAME)

    assert sut.qualified_name == ASSET_QUALIFIED_NAME
    assert sut.name == ASSET_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = DomoDashboard.creator(
        name=ASSET_NAME,
        domo_id=DOMO_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == ASSET_QUALIFIED_NAME
    assert sut.name == ASSET_NAME
    assert sut.domo_id is UNSET
