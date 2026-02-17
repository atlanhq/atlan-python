# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for APISpec model in pyatlan_v9."""

import pytest

from pyatlan_v9.model import APISpec
from tests_v9.unit.model.constants import (
    API_CONNECTION_QUALIFIED_NAME,
    API_CONNECTOR_TYPE,
    API_QUALIFIED_NAME,
    API_SPEC_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (API_SPEC_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        APISpec.creator(name=name, connection_qualified_name=connection_qualified_name)


def test_creator():
    """Test creator initializes expected derived fields."""
    sut = APISpec.creator(
        name=API_SPEC_NAME, connection_qualified_name=API_CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == API_SPEC_NAME
    assert sut.connection_qualified_name == API_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == API_QUALIFIED_NAME
    assert sut.connector_name == API_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, API_QUALIFIED_NAME, "qualified_name is required"),
        (API_SPEC_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        APISpec.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates APISpec for modification."""
    sut = APISpec.updater(qualified_name=API_QUALIFIED_NAME, name=API_SPEC_NAME)

    assert sut.qualified_name == API_QUALIFIED_NAME
    assert sut.name == API_SPEC_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = APISpec.updater(
        name=API_SPEC_NAME, qualified_name=API_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == API_SPEC_NAME
    assert sut.qualified_name == API_QUALIFIED_NAME
