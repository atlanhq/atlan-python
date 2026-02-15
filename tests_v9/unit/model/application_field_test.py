# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for ApplicationField model in pyatlan_v9."""

import pytest

from pyatlan_v9.models import ApplicationField
from tests_v9.unit.model.constants import (
    APP_CONNECTION_QUALIFIED_NAME,
    APP_CONNECTOR_TYPE,
    APPLICATION_FIELD_NAME,
    APPLICATION_FIELD_QUALIFIED_NAME,
    APPLICATION_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, application_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (APPLICATION_FIELD_NAME, None, "application_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, application_qualified_name: str, message: str
):
    """Test creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        ApplicationField.creator(
            name=name, application_qualified_name=application_qualified_name
        )


def test_creator():
    """Test creator initializes expected derived fields."""
    sut = ApplicationField.creator(
        name=APPLICATION_FIELD_NAME,
        application_qualified_name=APPLICATION_QUALIFIED_NAME,
    )

    assert sut.name == APPLICATION_FIELD_NAME
    assert sut.connection_qualified_name == APP_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == APPLICATION_FIELD_QUALIFIED_NAME
    assert sut.connector_name == APP_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, APPLICATION_FIELD_QUALIFIED_NAME, "qualified_name is required"),
        (APPLICATION_FIELD_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        ApplicationField.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates ApplicationField for modification."""
    sut = ApplicationField.updater(
        qualified_name=APPLICATION_FIELD_QUALIFIED_NAME,
        name=APPLICATION_FIELD_NAME,
    )

    assert sut.qualified_name == APPLICATION_FIELD_QUALIFIED_NAME
    assert sut.name == APPLICATION_FIELD_NAME


def test_trim_to_required():
    """Test trim_to_required preserves updater-required fields."""
    sut = ApplicationField.updater(
        name=APPLICATION_FIELD_NAME,
        qualified_name=APPLICATION_FIELD_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.name == APPLICATION_FIELD_NAME
    assert sut.qualified_name == APPLICATION_FIELD_QUALIFIED_NAME
