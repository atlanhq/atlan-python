# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for DomoDatasetColumn model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-domo-app emits today
(``{datasetQN}/column/{name}``, FND-3838 census), so a creator change that
would re-key existing dataset columns fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import DomoDatasetColumn

CONNECTION_QUALIFIED_NAME = "default/domo/123456789"
CONNECTOR_NAME = "domo"
DATASET_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/dataset/4f2a9c1e"
COLUMN_NAME = "order_total"
COLUMN_QUALIFIED_NAME = f"{DATASET_QUALIFIED_NAME}/column/{COLUMN_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-domo-app's map_dataset_column inputs and output."""
    sut = DomoDatasetColumn.creator(
        name="order_total",
        domo_dataset_qualified_name="default/domo/1700000000/dataset/4f2a9c1e",
    )

    assert (
        sut.qualified_name
        == "default/domo/1700000000/dataset/4f2a9c1e/column/order_total"
    )
    assert sut.connection_qualified_name == "default/domo/1700000000"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, domo_dataset_qualified_name, message",
    [
        (None, DATASET_QUALIFIED_NAME, "name is required"),
        (" ", DATASET_QUALIFIED_NAME, "name cannot be blank"),
        (COLUMN_NAME, None, "domo_dataset_qualified_name is required"),
        (COLUMN_NAME, " ", "domo_dataset_qualified_name cannot be blank"),
        (
            COLUMN_NAME,
            CONNECTION_QUALIFIED_NAME,
            "domo_dataset_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, domo_dataset_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DomoDatasetColumn.creator(
            name=name,
            domo_dataset_qualified_name=domo_dataset_qualified_name,
        )


def test_creator():
    """Test creator derives the connection and relates the parent dataset."""
    sut = DomoDatasetColumn.creator(
        name=COLUMN_NAME,
        domo_dataset_qualified_name=DATASET_QUALIFIED_NAME,
    )

    assert sut.type_name == "DomoDatasetColumn"
    assert sut.name == COLUMN_NAME
    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.domo_dataset_qualified_name == DATASET_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.domo_dataset.unique_attributes == {
        "qualifiedName": DATASET_QUALIFIED_NAME
    }
    assert sut.guid
    sut.validate(for_creation=True)


def test_creator_with_explicit_connection_qualified_name():
    """Test an explicit connection qualifiedName overrides the derived one."""
    sut = DomoDatasetColumn.creator(
        name=COLUMN_NAME,
        domo_dataset_qualified_name=DATASET_QUALIFIED_NAME,
        connection_qualified_name="default/domo/987654321",
    )

    assert sut.connection_qualified_name == "default/domo/987654321"
    assert sut.qualified_name == COLUMN_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, COLUMN_NAME, "qualified_name is required"),
        (COLUMN_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        DomoDatasetColumn.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a DomoDatasetColumn for modification."""
    sut = DomoDatasetColumn.updater(
        qualified_name=COLUMN_QUALIFIED_NAME, name=COLUMN_NAME
    )

    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = DomoDatasetColumn.creator(
        name=COLUMN_NAME,
        domo_dataset_qualified_name=DATASET_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == COLUMN_QUALIFIED_NAME
    assert sut.name == COLUMN_NAME
    assert sut.domo_dataset is UNSET
