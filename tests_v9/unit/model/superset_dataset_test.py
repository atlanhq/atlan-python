# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for SupersetDataset model in pyatlan_v9."""

import pytest

from pyatlan_v9.models import SupersetDataset
from tests_v9.unit.model.constants import (
    SUPERSET_CONNECTION_QUALIFIED_NAME,
    SUPERSET_CONNECTOR_TYPE,
    SUPERSET_DASHBOARD_QUALIFIED_NAME,
    SUPERSET_DATASET_NAME,
    SUPERSET_DATASET_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, superset_dashboard_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (
            SUPERSET_DATASET_NAME,
            None,
            "superset_dashboard_qualified_name is required",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, superset_dashboard_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SupersetDataset.creator(
            name=name,
            superset_dashboard_qualified_name=superset_dashboard_qualified_name,
        )


def test_creator():
    """Test creator initializes expected derived fields."""
    sut = SupersetDataset.creator(
        name=SUPERSET_DATASET_NAME,
        superset_dashboard_qualified_name=SUPERSET_DASHBOARD_QUALIFIED_NAME,
    )

    assert sut.name == SUPERSET_DATASET_NAME
    assert sut.superset_dashboard_qualified_name == SUPERSET_DASHBOARD_QUALIFIED_NAME
    assert sut.connection_qualified_name == SUPERSET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{SUPERSET_DASHBOARD_QUALIFIED_NAME}/{SUPERSET_DATASET_NAME}"
    )
    assert sut.connector_name == SUPERSET_CONNECTOR_TYPE


def test_overload_creator():
    """Test creator accepts explicit connection qualified name."""
    sut = SupersetDataset.creator(
        name=SUPERSET_DATASET_NAME,
        superset_dashboard_qualified_name=SUPERSET_DASHBOARD_QUALIFIED_NAME,
        connection_qualified_name=SUPERSET_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == SUPERSET_DATASET_NAME
    assert sut.superset_dashboard_qualified_name == SUPERSET_DASHBOARD_QUALIFIED_NAME
    assert sut.connection_qualified_name == SUPERSET_CONNECTION_QUALIFIED_NAME
    assert (
        sut.qualified_name
        == f"{SUPERSET_DASHBOARD_QUALIFIED_NAME}/{SUPERSET_DATASET_NAME}"
    )
    assert sut.connector_name == SUPERSET_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, SUPERSET_DATASET_QUALIFIED_NAME, "qualified_name is required"),
        (SUPERSET_DATASET_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SupersetDataset.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates SupersetDataset for modification."""
    sut = SupersetDataset.updater(
        qualified_name=SUPERSET_DATASET_QUALIFIED_NAME, name=SUPERSET_DATASET_NAME
    )

    assert sut.qualified_name == SUPERSET_DATASET_QUALIFIED_NAME
    assert sut.name == SUPERSET_DATASET_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SupersetDataset.updater(
        name=SUPERSET_DATASET_NAME, qualified_name=SUPERSET_DATASET_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == SUPERSET_DATASET_NAME
    assert sut.qualified_name == SUPERSET_DATASET_QUALIFIED_NAME
