# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for SchemaRegistryVersion model in pyatlan_v9.

The parity test uses the exact qualifiedName and name atlan-kafka-app emits
today (``{connectionQN}/subject/{subject}/version/{N}`` and ``{subject}.v{N}``,
``schema_registry_versions.yaml``), so a creator change that would re-key
existing versions fails here.
"""

import pytest

from pyatlan_v9.model import SchemaRegistryVersion

CONNECTION_QUALIFIED_NAME = "default/apache-kafka/1770801720"
SUBJECT_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/subject/orders-value"
VERSION_QUALIFIED_NAME = f"{SUBJECT_QUALIFIED_NAME}/version/3"


def test_creator_matches_app_qualified_name():
    """Mirror atlan-kafka-app's schema_registry_versions transform."""
    sut = SchemaRegistryVersion.creator(
        schema_registry_version_number=3,
        schema_registry_subject_qualified_name="default/apache-kafka/1770801720/subject/orders-value",
    )

    assert (
        sut.qualified_name
        == "default/apache-kafka/1770801720/subject/orders-value/version/3"
    )
    assert sut.name == "orders-value.v3"
    assert sut.schema_registry_version_number == "3"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "version_number, subject_qualified_name, message",
    [
        (None, SUBJECT_QUALIFIED_NAME, "schema_registry_version_number is required"),
        (" ", SUBJECT_QUALIFIED_NAME, "schema_registry_version_number cannot be blank"),
        (3, None, "schema_registry_subject_qualified_name is required"),
        (3, " ", "schema_registry_subject_qualified_name cannot be blank"),
        (
            3,
            CONNECTION_QUALIFIED_NAME,
            "schema_registry_subject_qualified_name is invalid",
        ),
        (
            3,
            f"{CONNECTION_QUALIFIED_NAME}/topic/orders",
            "schema_registry_subject_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    version_number, subject_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SchemaRegistryVersion.creator(
            schema_registry_version_number=version_number,
            schema_registry_subject_qualified_name=subject_qualified_name,
        )


def test_creator():
    """Test creator derives the name and connection from the subject."""
    sut = SchemaRegistryVersion.creator(
        schema_registry_version_number="3",
        schema_registry_subject_qualified_name=SUBJECT_QUALIFIED_NAME,
    )

    assert sut.name == "orders-value.v3"
    assert sut.qualified_name == VERSION_QUALIFIED_NAME
    assert sut.schema_registry_version_number == "3"
    assert sut.schema_registry_subject_qualified_name == SUBJECT_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "apache-kafka"
    assert sut.schema_registry_subject.unique_attributes == {
        "qualifiedName": SUBJECT_QUALIFIED_NAME
    }
    sut.validate(for_creation=True)


def test_overload_creator():
    """Test creator accepts an explicit name and connection qualified name."""
    sut = SchemaRegistryVersion.creator(
        schema_registry_version_number=3,
        schema_registry_subject_qualified_name=SUBJECT_QUALIFIED_NAME,
        name="orders v3",
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == "orders v3"
    assert sut.qualified_name == VERSION_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "apache-kafka"


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, "orders-value.v3", "qualified_name is required"),
        (VERSION_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        SchemaRegistryVersion.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a SchemaRegistryVersion for modification."""
    sut = SchemaRegistryVersion.updater(
        qualified_name=VERSION_QUALIFIED_NAME, name="orders-value.v3"
    )

    assert sut.qualified_name == VERSION_QUALIFIED_NAME
    assert sut.name == "orders-value.v3"


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = SchemaRegistryVersion.updater(
        qualified_name=VERSION_QUALIFIED_NAME, name="orders-value.v3"
    ).trim_to_required()

    assert sut.qualified_name == VERSION_QUALIFIED_NAME
    assert sut.name == "orders-value.v3"
