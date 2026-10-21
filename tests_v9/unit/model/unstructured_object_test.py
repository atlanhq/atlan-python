# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for UnstructuredObject model in pyatlan_v9.

The parity tests use the exact qualifiedNames atlan-bridge-app emits today
(``{containerQN}/{name}`` at the container root, ``{containerQN}/{parentPath}/{name}``
when nested; FND-3838 census), so a creator change that would re-key existing
objects fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import UnstructuredObject

CONNECTION_QUALIFIED_NAME = "default/bigid/1700000000"
CONNECTOR_NAME = "bigid"
CONTAINER_NAME = "bucket-x"
CONTAINER_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{CONTAINER_NAME}"
PARENT_FOLDER_QUALIFIED_NAME = f"{CONTAINER_QUALIFIED_NAME}/finance/accounts_payable"
NAME = "invoice.pdf"
TOP_LEVEL_QUALIFIED_NAME = f"{CONTAINER_QUALIFIED_NAME}/{NAME}"
NESTED_QUALIFIED_NAME = f"{PARENT_FOLDER_QUALIFIED_NAME}/{NAME}"


def test_creator_matches_app_qualified_name_at_container_root():
    """Mirror atlan-bridge-app's _build_unstructured_object for a row with no parent_folder_path."""
    sut = UnstructuredObject.creator(
        name="readme.md",
        unstructured_container_qualified_name="default/unstructured/1700000010/bucket-x",
    )

    assert sut.qualified_name == "default/unstructured/1700000010/bucket-x/readme.md"
    assert sut.connection_qualified_name == "default/unstructured/1700000010"
    assert sut.connector_name == "unstructured"
    assert sut.unstructured_container_name == "bucket-x"
    assert sut.unstructured_object_key == "readme.md"
    assert sut.unstructured_parent_folder is UNSET
    assert sut.unstructured_parent_folder_qualified_name is UNSET
    assert sut.unstructured_folder_hierarchy is UNSET
    sut.validate(for_creation=True)


def test_creator_matches_app_qualified_name_when_nested():
    """Mirror atlan-bridge-app's _build_unstructured_object for parent_folder_path="finance/ap"."""
    sut = UnstructuredObject.creator(
        name="readme.md",
        unstructured_container_qualified_name="default/unstructured/1700000010/bucket-x",
        unstructured_parent_folder_qualified_name="default/unstructured/1700000010/bucket-x/finance/ap",
    )

    assert (
        sut.qualified_name
        == "default/unstructured/1700000010/bucket-x/finance/ap/readme.md"
    )
    assert (
        sut.unstructured_parent_folder_qualified_name
        == "default/unstructured/1700000010/bucket-x/finance/ap"
    )
    assert sut.unstructured_folder_hierarchy == [
        {
            "qualifiedName": "default/unstructured/1700000010/bucket-x/finance/ap",
            "name": "ap",
        },
        {
            "qualifiedName": "default/unstructured/1700000010/bucket-x/finance",
            "name": "finance",
        },
    ]
    assert sut.unstructured_object_key == "finance/ap/readme.md"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, container_qualified_name, parent_folder_qualified_name, message",
    [
        (None, CONTAINER_QUALIFIED_NAME, None, "name is required"),
        (" ", CONTAINER_QUALIFIED_NAME, None, "name cannot be blank"),
        (NAME, None, None, "unstructured_container_qualified_name is required"),
        (NAME, " ", None, "unstructured_container_qualified_name cannot be blank"),
        (
            NAME,
            CONNECTION_QUALIFIED_NAME,
            None,
            "unstructured_container_qualified_name is invalid",
        ),
        (
            NAME,
            CONTAINER_QUALIFIED_NAME,
            f"{CONNECTION_QUALIFIED_NAME}/other-bucket/finance",
            "unstructured_parent_folder_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_invalid_parameters_raise_value_error(
    name: str,
    container_qualified_name: str,
    parent_folder_qualified_name: str,
    message: str,
):
    """Test creator validates required and malformed parameters."""
    with pytest.raises(ValueError, match=message):
        UnstructuredObject.creator(
            name=name,
            unstructured_container_qualified_name=container_qualified_name,
            unstructured_parent_folder_qualified_name=parent_folder_qualified_name,
        )


def test_creator_at_container_root():
    """Test creator derives the connection and container from the container qn."""
    sut = UnstructuredObject.creator(
        name=NAME, unstructured_container_qualified_name=CONTAINER_QUALIFIED_NAME
    )

    assert sut.name == NAME
    assert sut.qualified_name == TOP_LEVEL_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.unstructured_container_name == CONTAINER_NAME
    assert sut.unstructured_container_qualified_name == CONTAINER_QUALIFIED_NAME
    assert sut.unstructured_container.unique_attributes == {
        "qualifiedName": CONTAINER_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_creator_under_parent_folder():
    """Test creator relates the parent folder and keeps the container."""
    sut = UnstructuredObject.creator(
        name=NAME,
        unstructured_container_qualified_name=CONTAINER_QUALIFIED_NAME,
        unstructured_parent_folder_qualified_name=PARENT_FOLDER_QUALIFIED_NAME,
    )

    assert sut.qualified_name == NESTED_QUALIFIED_NAME
    assert sut.unstructured_container_qualified_name == CONTAINER_QUALIFIED_NAME
    assert sut.unstructured_container.unique_attributes == {
        "qualifiedName": CONTAINER_QUALIFIED_NAME
    }
    assert sut.unstructured_parent_folder_qualified_name == PARENT_FOLDER_QUALIFIED_NAME
    assert sut.unstructured_parent_folder.unique_attributes == {
        "qualifiedName": PARENT_FOLDER_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit connection qualified name."""
    sut = UnstructuredObject.creator(
        name=NAME,
        unstructured_container_qualified_name=CONTAINER_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == TOP_LEVEL_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME


def test_overload_creator_with_mismatched_connection_raises_value_error():
    """Test creator rejects a container that is not under the given connection."""
    with pytest.raises(
        ValueError, match="unstructured_container_qualified_name is invalid"
    ):
        UnstructuredObject.creator(
            name=NAME,
            unstructured_container_qualified_name=CONTAINER_QUALIFIED_NAME,
            connection_qualified_name="default/bigid/1800000000",
        )


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, NAME, "qualified_name is required"),
        (TOP_LEVEL_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        UnstructuredObject.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates an UnstructuredObject for modification."""
    sut = UnstructuredObject.updater(qualified_name=NESTED_QUALIFIED_NAME, name=NAME)

    assert sut.qualified_name == NESTED_QUALIFIED_NAME
    assert sut.name == NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = UnstructuredObject.updater(
        qualified_name=NESTED_QUALIFIED_NAME, name=NAME
    ).trim_to_required()

    assert sut.qualified_name == NESTED_QUALIFIED_NAME
    assert sut.name == NAME
