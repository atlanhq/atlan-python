# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for MongoDBDatabase model in pyatlan_v9."""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import MongoDBDatabase

CONNECTION_QUALIFIED_NAME = "default/documentdb/1700000000"
DATABASE_NAME = "sample_db"
DATABASE_QUALIFIED_NAME = "default/documentdb/1700000000/sample_db"


@pytest.mark.parametrize(
    "connection_qualified_name, expected_qualified_name, connector_name",
    [
        # atlan-documentdb-app: transformers/documentdb.py transform_databases
        (
            "default/documentdb/1700000000",
            "default/documentdb/1700000000/sample_db",
            "documentdb",
        ),
        # atlan-mongodbatlas-app (Atlas): transformers/database.yaml
        (
            "default/mongodb/1700000000",
            "default/mongodb/1700000000/sample_db",
            "mongodb",
        ),
        # atlan-mongodbatlas-app (on-prem): transformers/database.yaml
        (
            "default/mongo/1700000000",
            "default/mongo/1700000000/sample_db",
            "mongo",
        ),
    ],
)
def test_creator_matches_app_qualified_name(
    connection_qualified_name: str, expected_qualified_name: str, connector_name: str
):
    """Mirror the qualifiedName and denormalised attributes the apps emit."""
    sut = MongoDBDatabase.creator(
        name=DATABASE_NAME, connection_qualified_name=connection_qualified_name
    )

    assert sut.qualified_name == expected_qualified_name
    assert sut.name == DATABASE_NAME
    assert sut.connection_qualified_name == connection_qualified_name
    assert sut.connector_name == connector_name
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, CONNECTION_QUALIFIED_NAME, "name is required"),
        (" ", CONNECTION_QUALIFIED_NAME, "name cannot be blank"),
        (DATABASE_NAME, None, "connection_qualified_name is required"),
        (DATABASE_NAME, " ", "connection_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        MongoDBDatabase.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_validate_rejects_malformed_qualified_name():
    sut = MongoDBDatabase(name=DATABASE_NAME, qualified_name=DATABASE_NAME)
    with pytest.raises(ValueError, match="does not match expected pattern"):
        sut.validate()


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DATABASE_NAME, "qualified_name is required"),
        (DATABASE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        MongoDBDatabase.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = MongoDBDatabase.updater(
        qualified_name=DATABASE_QUALIFIED_NAME, name=DATABASE_NAME
    )

    assert sut.qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.name == DATABASE_NAME


def test_trim_to_required():
    sut = MongoDBDatabase.creator(
        name=DATABASE_NAME, connection_qualified_name=CONNECTION_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.name == DATABASE_NAME
    assert sut.connection_qualified_name is UNSET
