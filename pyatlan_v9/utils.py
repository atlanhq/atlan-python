# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Utility functions for pyatlan_v9."""

import random
from functools import wraps

from pyatlan.utils import (
    ComparisonCategory,
    get_base_type,
    is_comparable_type,
    list_attributes_to_params,
    unflatten_custom_metadata,
    unflatten_custom_metadata_for_entity,
    validate_type,
)


def init_guid(func):
    """
    Decorator function that can be used on the creator method of an asset to initialize the guid.

    The guid is initialized with a negative random integer to indicate it's a temporary GUID
    for objects being created (not yet persisted to Atlan).
    """

    @wraps(func)
    def call(*args, **kwargs):
        ret_value = func(*args, **kwargs)
        if hasattr(ret_value, "guid"):
            ret_value.guid = str(
                -int(random.random() * 10000000000000000)  # noqa: S311
            )
        return ret_value

    return call


def validate_required_fields(field_names: list[str], field_values: list) -> None:
    """
    Validate that required fields are provided and not empty.

    Args:
        field_names: List of field names
        field_values: List of field values corresponding to field_names

    Raises:
        ValueError: If any required field is missing or empty
    """
    for name, value in zip(field_names, field_values):
        if value is None:
            raise ValueError(f"{name} is required")
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{name} cannot be blank")
        if isinstance(value, list) and len(value) == 0:
            raise ValueError(f"{name} cannot be an empty list")


def validate_optional_fields(field_names: list[str], field_values: list) -> None:
    """
    Validate that optional fields, when provided, are not blank.

    Args:
        field_names: List of field names
        field_values: List of field values corresponding to field_names

    Raises:
        ValueError: If any provided field is blank
    """
    for name, value in zip(field_names, field_values):
        if isinstance(value, str) and not value.strip():
            raise ValueError(f"{name} cannot be blank")


def _check_prefix(name: str, value: str, prefix: str) -> None:
    if not value.startswith(f"{prefix}/"):
        raise ValueError(f"{name} is invalid")


def resolve_connection(connection_qualified_name: str) -> str:
    """
    Validate a connection qualifiedName and return its connector name.

    Args:
        connection_qualified_name: Unique name of the connection (default/<connector>/<epoch>)

    Returns:
        the connector name (second segment)

    Raises:
        ValueError: If the connection qualifiedName is malformed
    """
    fields = connection_qualified_name.split("/")
    if len(fields) != 3 or not all(f.strip() for f in fields):
        raise ValueError("connection_qualified_name is invalid")
    return fields[1]


def resolve_database_parent(
    *,
    database_qualified_name: str | None,
    database_name: str | None = None,
    connection_qualified_name: str | None = None,
) -> tuple[str, str, str | None, str | None]:
    """
    Resolve the connection and database of an asset that sits directly under a database
    (or, when it has none, directly under the connection).

    Without ``connection_qualified_name``, the database qualifiedName must have the standard
    4 segments (default/connector/connection_id/database) and everything is derived from it.
    With ``connection_qualified_name``, no depth is assumed: the database qualifiedName only
    has to start with it, and may be omitted entirely for assets with no database.

    Args:
        database_qualified_name: Unique name of the database, or None if there is none
        database_name: Simple name of the database (defaults to the last segment of its qualifiedName)
        connection_qualified_name: Unique name of the connection

    Returns:
        (connection_qualified_name, connector_name, database_name, database_qualified_name)

    Raises:
        ValueError: If any provided input is blank, or a qualifiedName is malformed
    """
    validate_optional_fields(
        ["database_qualified_name", "database_name", "connection_qualified_name"],
        [database_qualified_name, database_name, connection_qualified_name],
    )
    if connection_qualified_name is None:
        validate_required_fields(["database_qualified_name"], [database_qualified_name])
        fields = database_qualified_name.split("/")  # type: ignore[union-attr]
        if len(fields) != 4:
            raise ValueError(
                f"Invalid database_qualified_name: {database_qualified_name}. "
                "Expected format: default/connector/connection_id/database"
            )
        connection_qualified_name = "/".join(fields[:3])
        return (
            connection_qualified_name,
            fields[1],
            database_name or fields[3],
            database_qualified_name,
        )

    connector_name = resolve_connection(connection_qualified_name)
    if database_qualified_name is None:
        if database_name is not None:
            raise ValueError("database_name requires database_qualified_name")
        return connection_qualified_name, connector_name, None, None
    _check_prefix(
        "database_qualified_name", database_qualified_name, connection_qualified_name
    )
    return (
        connection_qualified_name,
        connector_name,
        database_name or database_qualified_name.rsplit("/", 1)[-1],
        database_qualified_name,
    )


def resolve_sql_parents(
    *,
    schema_qualified_name: str | None,
    schema_name: str | None = None,
    database_name: str | None = None,
    database_qualified_name: str | None = None,
    connection_qualified_name: str | None = None,
) -> tuple[str, str, str | None, str | None, str | None, str | None]:
    """
    Resolve the connection, database and schema of an asset that sits under a schema
    (Table, View, MaterialisedView, Procedure, Function, ...).

    Without ``connection_qualified_name``, the schema qualifiedName must have the standard
    5 segments (default/connector/connection_id/database/schema) and missing names are
    derived from it. With ``connection_qualified_name``, no depth is assumed (Fabric's
    6 segments, db2 z/OS's 4): each parent qualifiedName only has to start with its own
    parent's, names default to the last segment of their qualifiedName, and the database
    is left unset when none is given and the schema qualifiedName is not standard depth.
    ``schema_qualified_name`` may then also be None, for assets directly under the connection.

    Args:
        schema_qualified_name: Unique name of the schema, or None if there is none
        schema_name: Simple name of the schema
        database_name: Simple name of the database
        database_qualified_name: Unique name of the database
        connection_qualified_name: Unique name of the connection

    Returns:
        (connection_qualified_name, connector_name, database_name, database_qualified_name,
        schema_name, schema_qualified_name)

    Raises:
        ValueError: If any provided input is blank, or a qualifiedName is malformed
    """
    validate_optional_fields(
        [
            "schema_qualified_name",
            "schema_name",
            "database_name",
            "database_qualified_name",
            "connection_qualified_name",
        ],
        [
            schema_qualified_name,
            schema_name,
            database_name,
            database_qualified_name,
            connection_qualified_name,
        ],
    )
    if connection_qualified_name is None:
        validate_required_fields(["schema_qualified_name"], [schema_qualified_name])
        fields = schema_qualified_name.split("/")  # type: ignore[union-attr]
        if len(fields) != 5:
            raise ValueError(
                f"Invalid schema_qualified_name: {schema_qualified_name}. "
                "Expected format: default/connector/connection_id/database/schema"
            )
        connection_qualified_name = "/".join(fields[:3])
        db_name = database_name or fields[3]
        return (
            connection_qualified_name,
            fields[1],
            db_name,
            database_qualified_name or f"{connection_qualified_name}/{db_name}",
            schema_name or fields[4],
            schema_qualified_name,
        )

    connector_name = resolve_connection(connection_qualified_name)
    if schema_qualified_name is None:
        if schema_name is not None:
            raise ValueError("schema_name requires schema_qualified_name")
        _, _, db_name, db_qualified_name = resolve_database_parent(
            database_qualified_name=database_qualified_name,
            database_name=database_name,
            connection_qualified_name=connection_qualified_name,
        )
        return (
            connection_qualified_name,
            connector_name,
            db_name,
            db_qualified_name,
            None,
            None,
        )

    _check_prefix(
        "schema_qualified_name", schema_qualified_name, connection_qualified_name
    )
    if database_qualified_name is not None:
        _check_prefix(
            "database_qualified_name",
            database_qualified_name,
            connection_qualified_name,
        )
        _check_prefix(
            "schema_qualified_name", schema_qualified_name, database_qualified_name
        )
        database_name = database_name or database_qualified_name.rsplit("/", 1)[-1]
    elif database_name is not None:
        database_qualified_name = f"{connection_qualified_name}/{database_name}"
        _check_prefix(
            "schema_qualified_name", schema_qualified_name, database_qualified_name
        )
    else:
        fields = schema_qualified_name.split("/")
        if len(fields) == 5:
            database_name = fields[3]
            database_qualified_name = f"{connection_qualified_name}/{database_name}"
    return (
        connection_qualified_name,
        connector_name,
        database_name,
        database_qualified_name,
        schema_name or schema_qualified_name.rsplit("/", 1)[-1],
        schema_qualified_name,
    )


__all__ = [
    "ComparisonCategory",
    "get_base_type",
    "init_guid",
    "is_comparable_type",
    "list_attributes_to_params",
    "resolve_connection",
    "resolve_database_parent",
    "resolve_sql_parents",
    "unflatten_custom_metadata",
    "unflatten_custom_metadata_for_entity",
    "validate_optional_fields",
    "validate_required_fields",
    "validate_type",
]
