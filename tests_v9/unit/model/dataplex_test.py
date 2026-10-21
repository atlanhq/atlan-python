# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Dataplex creators in pyatlan_v9 (GCPDataplexAspectType, BigqueryRoutine).

The expected qualifiedNames are the exact strings the connectors emit:
GCPDataplexAspectType from atlan-dataplex-app (``aspect_type_qn``), BigqueryRoutine in the
``_routines_`` shape that atlan-dataplex-app aspect-sync parses and existing tenant assets carry.
A creator change that would re-key existing assets fails here.
"""

import pytest

from pyatlan_v9.model import BigqueryRoutine, GCPDataplexAspectType

DATAPLEX_CONNECTION_QN = "default/dataplex/1712345678"
RESOURCE_NAME = "projects/my-project/locations/us-central1/aspectTypes/data-owner"
ASPECT_TYPE_QN = (
    "default/dataplex/1712345678/aspect-type/"
    "projects/my-project/locations/us-central1/aspectTypes/data-owner"
)

BQ_CONNECTION_QN = "default/bigquery/1712345678"
SCHEMA_QN = "default/bigquery/1712345678/my-project/my_dataset"
ROUTINE_NAME = "clean_orders"
DEFINITION = "CREATE PROCEDURE my_dataset.clean_orders() BEGIN SELECT 1; END"
ROUTINE_QN = "default/bigquery/1712345678/my-project/my_dataset/_routines_/clean_orders"


def test_aspect_type_creator_matches_app_qualified_name():
    sut = GCPDataplexAspectType.creator(
        resource_name=RESOURCE_NAME,
        connection_qualified_name=DATAPLEX_CONNECTION_QN,
    )

    assert sut.qualified_name == ASPECT_TYPE_QN
    assert sut.name == "data-owner"
    assert sut.connection_qualified_name == DATAPLEX_CONNECTION_QN
    assert sut.connector_name == "dataplex"
    assert sut.gcp_dataplex_aspect_type_resource_name == RESOURCE_NAME
    assert sut.gcp_dataplex_aspect_type_project == "my-project"
    assert sut.gcp_dataplex_aspect_type_location == "us-central1"
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "resource_name, connection_qualified_name, message",
    [
        (None, DATAPLEX_CONNECTION_QN, "resource_name is required"),
        (RESOURCE_NAME, None, "connection_qualified_name is required"),
        ("  ", DATAPLEX_CONNECTION_QN, "resource_name"),
        (RESOURCE_NAME, "", "connection_qualified_name"),
        ("data-owner", DATAPLEX_CONNECTION_QN, "Invalid resource_name"),
        (
            "projects/p/locations/l/entryTypes/data-owner",
            DATAPLEX_CONNECTION_QN,
            "Invalid resource_name",
        ),
        (
            "projects/p/locations/ /aspectTypes/data-owner",
            DATAPLEX_CONNECTION_QN,
            "Invalid resource_name",
        ),
    ],
)
def test_aspect_type_creator_rejects_missing_or_invalid_inputs(
    resource_name, connection_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        GCPDataplexAspectType.creator(
            resource_name=resource_name,
            connection_qualified_name=connection_qualified_name,
        )


def test_aspect_type_create_alias():
    sut = GCPDataplexAspectType.create(
        resource_name=RESOURCE_NAME,
        connection_qualified_name=DATAPLEX_CONNECTION_QN,
    )

    assert sut.qualified_name == ASPECT_TYPE_QN


def test_routine_creator_matches_app_qualified_name():
    sut = BigqueryRoutine.creator(
        name=ROUTINE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QN,
    )

    assert sut.qualified_name == ROUTINE_QN
    assert sut.name == ROUTINE_NAME
    assert sut.definition == DEFINITION
    assert sut.connection_qualified_name == BQ_CONNECTION_QN
    assert sut.connector_name == "bigquery"
    assert sut.database_name == "my-project"
    assert sut.database_qualified_name == f"{BQ_CONNECTION_QN}/my-project"
    assert sut.schema_name == "my_dataset"
    assert sut.schema_qualified_name == SCHEMA_QN
    assert sut.atlan_schema.qualified_name == SCHEMA_QN
    assert sut._QUALIFIED_NAME_PATTERN.match(sut.qualified_name)
    sut.validate(for_creation=True)


def test_routine_creator_uses_explicit_parent_names():
    sut = BigqueryRoutine.creator(
        name=ROUTINE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QN,
        schema_name="My Dataset",
        database_name="My Project",
        database_qualified_name=f"{BQ_CONNECTION_QN}/my-project",
        connection_qualified_name=BQ_CONNECTION_QN,
    )

    assert sut.qualified_name == ROUTINE_QN
    assert sut.schema_name == "My Dataset"
    assert sut.database_name == "My Project"
    assert sut.database_qualified_name == f"{BQ_CONNECTION_QN}/my-project"


@pytest.mark.parametrize(
    "name, definition, schema_qualified_name, message",
    [
        (None, DEFINITION, SCHEMA_QN, "name is required"),
        (ROUTINE_NAME, None, SCHEMA_QN, "definition is required"),
        (ROUTINE_NAME, DEFINITION, None, "schema_qualified_name is required"),
        ("  ", DEFINITION, SCHEMA_QN, "name"),
        (ROUTINE_NAME, DEFINITION, "", "schema_qualified_name"),
        (ROUTINE_NAME, DEFINITION, BQ_CONNECTION_QN, "Invalid schema_qualified_name"),
    ],
)
def test_routine_creator_rejects_missing_or_invalid_inputs(
    name, definition, schema_qualified_name, message
):
    with pytest.raises(ValueError, match=message):
        BigqueryRoutine.creator(
            name=name,
            definition=definition,
            schema_qualified_name=schema_qualified_name,
        )


def test_routine_create_alias():
    sut = BigqueryRoutine.create(
        name=ROUTINE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QN,
    )

    assert sut.qualified_name == ROUTINE_QN
