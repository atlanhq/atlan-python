# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for MongoDBCollection model in pyatlan_v9."""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import MongoDBCollection

CONNECTION_QUALIFIED_NAME = "default/documentdb/1700000000"
DATABASE_NAME = "sample_db"
DATABASE_QUALIFIED_NAME = "default/documentdb/1700000000/sample_db"
COLLECTION_NAME = "orders"
COLLECTION_QUALIFIED_NAME = "default/documentdb/1700000000/sample_db/orders"


@pytest.mark.parametrize(
    "database_qualified_name, expected_qualified_name, "
    "connection_qualified_name, connector_name",
    [
        # atlan-documentdb-app: transformers/documentdb.py transform_collections
        (
            "default/documentdb/1700000000/sample_db",
            "default/documentdb/1700000000/sample_db/orders",
            "default/documentdb/1700000000",
            "documentdb",
        ),
        # atlan-mongodbatlas-app (Atlas): transformers/collection.yaml
        (
            "default/mongodb/1700000000/sample_db",
            "default/mongodb/1700000000/sample_db/orders",
            "default/mongodb/1700000000",
            "mongodb",
        ),
        # atlan-mongodbatlas-app (on-prem): transformers/collection.yaml
        (
            "default/mongo/1700000000/sample_db",
            "default/mongo/1700000000/sample_db/orders",
            "default/mongo/1700000000",
            "mongo",
        ),
    ],
)
def test_creator_matches_app_qualified_name(
    database_qualified_name: str,
    expected_qualified_name: str,
    connection_qualified_name: str,
    connector_name: str,
):
    """Mirror the qualifiedName, denormalised attributes and parent the apps emit."""
    sut = MongoDBCollection.creator(
        name=COLLECTION_NAME, database_qualified_name=database_qualified_name
    )

    assert sut.qualified_name == expected_qualified_name
    assert sut.name == COLLECTION_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == database_qualified_name
    assert sut.connection_qualified_name == connection_qualified_name
    assert sut.connector_name == connector_name
    assert sut.mongo_db_database.unique_attributes == {
        "qualifiedName": database_qualified_name
    }
    sut.validate(for_creation=True)


def test_creator_with_explicit_parents():
    sut = MongoDBCollection.creator(
        name=COLLECTION_NAME,
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        database_name=DATABASE_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == COLLECTION_QUALIFIED_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == "documentdb"
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, database_qualified_name, message",
    [
        (None, DATABASE_QUALIFIED_NAME, "name is required"),
        (" ", DATABASE_QUALIFIED_NAME, "name cannot be blank"),
        (COLLECTION_NAME, None, "database_qualified_name is required"),
        (COLLECTION_NAME, " ", "database_qualified_name cannot be blank"),
        (
            COLLECTION_NAME,
            CONNECTION_QUALIFIED_NAME,
            "database_qualified_name is invalid",
        ),
    ],
)
def test_creator_with_invalid_parameters_raise_value_error(
    name: str, database_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        MongoDBCollection.creator(
            name=name, database_qualified_name=database_qualified_name
        )


def test_validate_for_creation_requires_parent():
    sut = MongoDBCollection(
        name=COLLECTION_NAME, qualified_name=COLLECTION_QUALIFIED_NAME
    )
    with pytest.raises(ValueError, match="mongo_db_database is required"):
        sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, COLLECTION_NAME, "qualified_name is required"),
        (COLLECTION_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        MongoDBCollection.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = MongoDBCollection.updater(
        qualified_name=COLLECTION_QUALIFIED_NAME, name=COLLECTION_NAME
    )

    assert sut.qualified_name == COLLECTION_QUALIFIED_NAME
    assert sut.name == COLLECTION_NAME


def test_trim_to_required():
    sut = MongoDBCollection.creator(
        name=COLLECTION_NAME, database_qualified_name=DATABASE_QUALIFIED_NAME
    ).trim_to_required()

    assert sut.qualified_name == COLLECTION_QUALIFIED_NAME
    assert sut.name == COLLECTION_NAME
    assert sut.mongo_db_database is UNSET
