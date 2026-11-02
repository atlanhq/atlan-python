# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for UnstructuredContainer model in pyatlan_v9.

The parity test uses the exact qualifiedName atlan-bridge-app emits today
(``{connectionQN}/{container}``, FND-3838 census), so a creator change that
would re-key existing containers fails here.
"""

import pytest

from pyatlan_v9.model import UnstructuredContainer

CONNECTION_QUALIFIED_NAME = "default/bigid/1700000000"
CONNECTOR_NAME = "bigid"
CONTAINER_NAME = "bucket-x"
CONTAINER_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{CONTAINER_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-bridge-app's transform_generic_unstructured_container_row."""
    sut = UnstructuredContainer.creator(
        name="bucket-x",
        connection_qualified_name="default/unstructured/1700000010",
    )

    assert sut.qualified_name == "default/unstructured/1700000010/bucket-x"
    assert sut.connector_name == "unstructured"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (CONTAINER_NAME, None, "connection_qualified_name is required"),
        (CONTAINER_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        UnstructuredContainer.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    """Test creator sets the connection attributes."""
    sut = UnstructuredContainer.creator(
        name=CONTAINER_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    )

    assert sut.name == CONTAINER_NAME
    assert sut.qualified_name == CONTAINER_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, CONTAINER_NAME, "qualified_name is required"),
        (CONTAINER_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        UnstructuredContainer.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an UnstructuredContainer for modification."""
    sut = UnstructuredContainer.updater(
        qualified_name=CONTAINER_QUALIFIED_NAME, name=CONTAINER_NAME
    )

    assert sut.qualified_name == CONTAINER_QUALIFIED_NAME
    assert sut.name == CONTAINER_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = UnstructuredContainer.updater(
        qualified_name=CONTAINER_QUALIFIED_NAME, name=CONTAINER_NAME
    ).trim_to_required()

    assert sut.qualified_name == CONTAINER_QUALIFIED_NAME
    assert sut.name == CONTAINER_NAME
