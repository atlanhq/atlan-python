# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for AnaplanDimension model in pyatlan_v9."""

import pytest

from pyatlan_v9.models import AnaplanDimension
from tests_v9.unit.model.constants import (
    ANAPLAN_CONNECTION_QUALIFIED_NAME,
    ANAPLAN_CONNECTOR_TYPE,
    ANAPLAN_DIMENSION_NAME,
    ANAPLAN_DIMENSION_QUALIFIED_NAME,
    ANAPLAN_MODEL_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, model_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (ANAPLAN_DIMENSION_NAME, None, "model_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, model_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AnaplanDimension.creator(name=name, model_qualified_name=model_qualified_name)


def test_creator():
    """Test creator initializes expected derived fields."""
    sut = AnaplanDimension.creator(
        name=ANAPLAN_DIMENSION_NAME,
        model_qualified_name=ANAPLAN_MODEL_QUALIFIED_NAME,
    )

    assert sut.name == ANAPLAN_DIMENSION_NAME
    assert sut.connection_qualified_name == ANAPLAN_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == ANAPLAN_DIMENSION_QUALIFIED_NAME
    assert sut.connector_name == ANAPLAN_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ANAPLAN_MODEL_QUALIFIED_NAME, "qualified_name is required"),
        (ANAPLAN_DIMENSION_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        AnaplanDimension.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates AnaplanDimension for modification."""
    sut = AnaplanDimension.updater(
        qualified_name=ANAPLAN_DIMENSION_QUALIFIED_NAME, name=ANAPLAN_DIMENSION_NAME
    )

    assert sut.qualified_name == ANAPLAN_DIMENSION_QUALIFIED_NAME
    assert sut.name == ANAPLAN_DIMENSION_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = AnaplanDimension.updater(
        name=ANAPLAN_DIMENSION_NAME, qualified_name=ANAPLAN_DIMENSION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == ANAPLAN_DIMENSION_NAME
    assert sut.qualified_name == ANAPLAN_DIMENSION_QUALIFIED_NAME
