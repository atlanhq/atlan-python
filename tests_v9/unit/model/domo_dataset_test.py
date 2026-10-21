# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for DomoDataset model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-domo-app emits today
(``{connectionQN}/dataset/{domoId}``, FND-3838 census), so a creator change that
would re-key existing datasets fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import DomoDataset

CONNECTION_QUALIFIED_NAME = "default/domo/123456789"
CONNECTOR_NAME = "domo"
ASSET_NAME = "Sales dataset"
DOMO_ID = "4f2a9c1e-77b0-4d3e-9a51-0c6e2b8d1f3a"
ASSET_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/dataset/{DOMO_ID}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-domo-app's map_dataset inputs and output."""
    sut = DomoDataset.creator(
        name="Sales dataset",
        domo_id="4f2a9c1e-77b0-4d3e-9a51-0c6e2b8d1f3a",
        connection_qualified_name="default/domo/1700000000",
    )

    assert (
        sut.qualified_name
        == "default/domo/1700000000/dataset/4f2a9c1e-77b0-4d3e-9a51-0c6e2b8d1f3a"
    )
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
        DomoDataset.creator(
            name=name,
            domo_id=domo_id,
            connection_qualified_name=connection_qualified_name,
        )


def test_creator():
    """Test creator sets the Domo id and denormalised connection attributes."""
    sut = DomoDataset.creator(
        name=ASSET_NAME,
        domo_id=DOMO_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.type_name == "DomoDataset"
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
        DomoDataset.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a DomoDataset for modification."""
    sut = DomoDataset.updater(qualified_name=ASSET_QUALIFIED_NAME, name=ASSET_NAME)

    assert sut.qualified_name == ASSET_QUALIFIED_NAME
    assert sut.name == ASSET_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = DomoDataset.creator(
        name=ASSET_NAME,
        domo_id=DOMO_ID,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == ASSET_QUALIFIED_NAME
    assert sut.name == ASSET_NAME
    assert sut.domo_id is UNSET
