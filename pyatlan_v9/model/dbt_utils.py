# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""qualifiedName helpers shared by the dbt asset creators.

The shapes match what atlan-dbt-app emits today (``DbtUtils.build_qualified_name``
and ``tag_processor.py``), where ``{base}`` is
``{connection_qualified_name}/account/{account_id}/project/{project_id}``:

- DbtSource: ``{base}/{unique_id}``
- env-scoped types: ``{base}/env/{environment_id}/{unique_id}``
- DbtTag: ``{base}/tag/{tag_name}``
"""

from __future__ import annotations

from typing import List, Tuple

from pyatlan.model.enums import AtlanConnectorType
from pyatlan_v9.utils import validate_required_fields


def _validate_ids(field_names: List[str], values: List[str]) -> None:
    validate_required_fields(field_names, values)
    for field_name, value in zip(field_names, values):
        if "/" in value:
            raise ValueError(f"{field_name} cannot contain '/': {value}")


def dbt_project_qualified_name(
    connection_qualified_name: str, account_id: str, project_id: str
) -> Tuple[str, str]:
    """Return ``({base}, connector_name)``, raising on blank or malformed inputs."""
    validate_required_fields(["connection_qualified_name"], [connection_qualified_name])
    connector_name = str(
        AtlanConnectorType.get_connector_name(connection_qualified_name)
    )
    _validate_ids(["account_id", "project_id"], [account_id, project_id])
    return (
        f"{connection_qualified_name}/account/{account_id}/project/{project_id}",
        connector_name,
    )


def dbt_env_qualified_name(
    connection_qualified_name: str,
    account_id: str,
    project_id: str,
    environment_id: str,
    unique_id: str,
) -> Tuple[str, str]:
    """Return ``({base}/env/{environment_id}/{unique_id}, connector_name)``."""
    base, connector_name = dbt_project_qualified_name(
        connection_qualified_name, account_id, project_id
    )
    _validate_ids(["environment_id", "unique_id"], [environment_id, unique_id])
    return f"{base}/env/{environment_id}/{unique_id}", connector_name


def parse_dbt_env_qualified_name(
    qualified_name: str, attribute_name: str
) -> Tuple[str, str, str]:
    """Split an env-scoped dbt qualifiedName.

    :returns: ``(connection_qualified_name, connector_name, unique_id)``
    :raises ValueError: if the qualifiedName is not
        ``<connection>/account/<a>/project/<p>/env/<e>/<unique_id>``
    """
    validate_required_fields([attribute_name], [qualified_name])
    fields = qualified_name.split("/")
    if (
        len(fields) != 10
        or fields[3] != "account"
        or fields[5] != "project"
        or fields[7] != "env"
        or not all(f.strip() for f in fields)
    ):
        raise ValueError(
            f"Invalid {attribute_name}: {qualified_name}. Expected format: "
            "default/dbt/<epoch>/account/<account_id>/project/<project_id>"
            "/env/<environment_id>/<unique_id>"
        )
    connection_qualified_name = "/".join(fields[:3])
    connector_name = str(
        AtlanConnectorType.get_connector_name(connection_qualified_name)
    )
    return connection_qualified_name, connector_name, fields[9]


__all__ = [
    "dbt_env_qualified_name",
    "dbt_project_qualified_name",
    "parse_dbt_env_qualified_name",
]
