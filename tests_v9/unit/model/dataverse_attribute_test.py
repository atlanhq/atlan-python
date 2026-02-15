# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for DataverseAttribute model in pyatlan_v9."""

import pytest

from pyatlan_v9.models import DataverseAttribute
from tests_v9.unit.model.constants import (
    DATAVERSE_ATTRIBUTE_NAME,
    DATAVERSE_ATTRIBUTE_QUALIFIED_NAME,
    DATAVERSE_CONNECTION_QUALIFIED_NAME,
    DATAVERSE_CONNECTOR_TYPE,
    DATAVERSE_ENTITY_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, entity_qualified_name, message",
    [
        (None, "connection/name", "name is required"),
        (DATAVERSE_ATTRIBUTE_NAME, None, "dataverse_entity_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, entity_qualified_name: str, message: str
):
    """Test creator raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        DataverseAttribute.creator(
            name=name, dataverse_entity_qualified_name=entity_qualified_name
        )


def test_creator():
    """Test creator derives connection metadata from entity qualified name."""
    sut = DataverseAttribute.creator(
        name=DATAVERSE_ATTRIBUTE_NAME,
        dataverse_entity_qualified_name=DATAVERSE_ENTITY_QUALIFIED_NAME,
    )

    assert sut.name == DATAVERSE_ATTRIBUTE_NAME
    assert sut.connection_qualified_name == DATAVERSE_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == DATAVERSE_ATTRIBUTE_QUALIFIED_NAME
    assert sut.connector_name == DATAVERSE_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DATAVERSE_ENTITY_QUALIFIED_NAME, "qualified_name is required"),
        (DATAVERSE_ATTRIBUTE_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater raises ValueError when required parameters are missing."""
    with pytest.raises(ValueError, match=message):
        DataverseAttribute.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater returns minimal update payload."""
    sut = DataverseAttribute.updater(
        qualified_name=DATAVERSE_ATTRIBUTE_QUALIFIED_NAME, name=DATAVERSE_ATTRIBUTE_NAME
    )

    assert sut.qualified_name == DATAVERSE_ATTRIBUTE_QUALIFIED_NAME
    assert sut.name == DATAVERSE_ATTRIBUTE_NAME


def test_trim_to_required():
    """Test trim_to_required preserves required update fields."""
    sut = DataverseAttribute.updater(
        name=DATAVERSE_ATTRIBUTE_NAME, qualified_name=DATAVERSE_ATTRIBUTE_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.name == DATAVERSE_ATTRIBUTE_NAME
    assert sut.qualified_name == DATAVERSE_ATTRIBUTE_QUALIFIED_NAME
