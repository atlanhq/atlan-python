# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for BigqueryRoutine model in pyatlan_v9.

The parity test uses the exact ``{schemaQN}/_routines_/{name}`` qualifiedName that
BigqueryRoutine assets carry and that atlan-dataplex-app aspect-sync parses
(``entry_names._ROUTINES_MARKER``), so a creator change that would re-key existing
routines fails here.
"""

import pytest
from msgspec import UNSET

from pyatlan_v9.model import BigqueryRoutine

CONNECTION_QUALIFIED_NAME = "default/bigquery/123456789"
CONNECTOR_NAME = "bigquery"
DATABASE_NAME = "my-project"
DATABASE_QUALIFIED_NAME = f"{CONNECTION_QUALIFIED_NAME}/{DATABASE_NAME}"
SCHEMA_NAME = "my_dataset"
SCHEMA_QUALIFIED_NAME = f"{DATABASE_QUALIFIED_NAME}/{SCHEMA_NAME}"
ROUTINE_NAME = "clean_orders"
DEFINITION = "CREATE PROCEDURE my_dataset.clean_orders() BEGIN SELECT 1; END"
ROUTINE_QUALIFIED_NAME = f"{SCHEMA_QUALIFIED_NAME}/_routines_/{ROUTINE_NAME}"


def test_creator_matches_app_qualified_name():
    """Mirror the routine qualifiedName atlan-dataplex-app aspect-sync parses."""
    sut = BigqueryRoutine.creator(
        name="clean_orders",
        definition=DEFINITION,
        schema_qualified_name="default/bigquery/1700000000/acme-prod/sales",
    )

    assert (
        sut.qualified_name
        == "default/bigquery/1700000000/acme-prod/sales/_routines_/clean_orders"
    )
    sut.validate(for_creation=True)


@pytest.mark.parametrize(
    "name, definition, schema_qualified_name, message",
    [
        (None, DEFINITION, SCHEMA_QUALIFIED_NAME, "name is required"),
        (" ", DEFINITION, SCHEMA_QUALIFIED_NAME, "name cannot be blank"),
        (ROUTINE_NAME, None, SCHEMA_QUALIFIED_NAME, "definition is required"),
        (ROUTINE_NAME, " ", SCHEMA_QUALIFIED_NAME, "definition cannot be blank"),
        (ROUTINE_NAME, DEFINITION, None, "schema_qualified_name is required"),
        (ROUTINE_NAME, DEFINITION, " ", "schema_qualified_name cannot be blank"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, definition: str, schema_qualified_name: str, message: str
):
    """Test creator validates required parameters."""
    with pytest.raises(ValueError, match=message):
        BigqueryRoutine.creator(
            name=name,
            definition=definition,
            schema_qualified_name=schema_qualified_name,
        )


@pytest.mark.parametrize(
    "schema_qualified_name",
    [CONNECTION_QUALIFIED_NAME, f"{SCHEMA_QUALIFIED_NAME}/extra"],
)
def test_creator_with_malformed_schema_qualified_name_raises_value_error(
    schema_qualified_name: str,
):
    """Test creator rejects a parent qualifiedName that is not a BigQuery dataset."""
    with pytest.raises(ValueError, match="Invalid schema_qualified_name"):
        BigqueryRoutine.creator(
            name=ROUTINE_NAME,
            definition=DEFINITION,
            schema_qualified_name=schema_qualified_name,
        )


def test_creator_derives_parent_attributes():
    """Test creator derives the denormalised parent attributes from the schema qn."""
    sut = BigqueryRoutine.creator(
        name=ROUTINE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    assert sut.type_name == "BigqueryRoutine"
    assert sut.name == ROUTINE_NAME
    assert sut.definition == DEFINITION
    assert sut.qualified_name == ROUTINE_QUALIFIED_NAME
    assert sut.schema_name == SCHEMA_NAME
    assert sut.schema_qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.database_name == DATABASE_NAME
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME
    assert sut.connector_name == CONNECTOR_NAME
    assert sut.atlan_schema.qualified_name == SCHEMA_QUALIFIED_NAME
    assert sut.guid
    sut.validate(for_creation=True)


def test_creator_with_explicit_parent_attributes():
    """Test explicit parent names override the derived ones without changing the qn."""
    sut = BigqueryRoutine.creator(
        name=ROUTINE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
        schema_name="My Dataset",
        database_name="My Project",
        database_qualified_name=DATABASE_QUALIFIED_NAME,
        connection_qualified_name=CONNECTION_QUALIFIED_NAME,
    )

    assert sut.qualified_name == ROUTINE_QUALIFIED_NAME
    assert sut.schema_name == "My Dataset"
    assert sut.database_name == "My Project"
    assert sut.database_qualified_name == DATABASE_QUALIFIED_NAME
    assert sut.connection_qualified_name == CONNECTION_QUALIFIED_NAME


def test_create_alias():
    """Test the deprecated create alias delegates to creator."""
    sut = BigqueryRoutine.create(
        name=ROUTINE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    )

    assert sut.qualified_name == ROUTINE_QUALIFIED_NAME


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, ROUTINE_NAME, "qualified_name is required"),
        (ROUTINE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    """Test updater validates required parameters."""
    with pytest.raises(ValueError, match=message):
        BigqueryRoutine.updater(qualified_name=qualified_name, name=name)


def test_updater():
    """Test updater creates a BigqueryRoutine for modification."""
    sut = BigqueryRoutine.updater(
        qualified_name=ROUTINE_QUALIFIED_NAME, name=ROUTINE_NAME
    )

    assert sut.qualified_name == ROUTINE_QUALIFIED_NAME
    assert sut.name == ROUTINE_NAME


def test_trim_to_required():
    """Test trim_to_required keeps only updater-required fields."""
    sut = BigqueryRoutine.creator(
        name=ROUTINE_NAME,
        definition=DEFINITION,
        schema_qualified_name=SCHEMA_QUALIFIED_NAME,
    ).trim_to_required()

    assert sut.qualified_name == ROUTINE_QUALIFIED_NAME
    assert sut.name == ROUTINE_NAME
    assert sut.definition is UNSET
