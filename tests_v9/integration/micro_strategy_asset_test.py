# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    MicroStrategyAttribute,
    MicroStrategyColumn,
    MicroStrategyCube,
    MicroStrategyDocument,
    MicroStrategyDossier,
    MicroStrategyFact,
    MicroStrategyMetric,
    MicroStrategyProject,
    MicroStrategyReport,
    MicroStrategyVisualization,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("MSTR")

PROJECT_CHILDREN = [
    (MicroStrategyAttribute, "attributes"),
    (MicroStrategyMetric, "metrics"),
    (MicroStrategyFact, "facts"),
    (MicroStrategyCube, "cubes"),
    (MicroStrategyReport, "reports"),
    (MicroStrategyDocument, "documents"),
    (MicroStrategyDossier, "dossiers"),
]


def _mstr_id(segment: str) -> str:
    return f"{segment}{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client,
        name=MODULE_NAME,
        connector_type=AtlanConnectorType.MICROSTRATEGY,
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def project(
    client: AtlanClient, connection: Connection
) -> Generator[MicroStrategyProject, None, None]:
    to_create = MicroStrategyProject.creator(
        name=f"project_{MODULE_NAME}",
        connection_qualified_name=connection.qualified_name,
        micro_strategy_id=_mstr_id("projects"),
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=MicroStrategyProject
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MicroStrategyProject)


@pytest.fixture(scope="module")
def project_children(
    client: AtlanClient, project: MicroStrategyProject
) -> Generator[dict, None, None]:
    created = {}
    for asset_type, segment in PROJECT_CHILDREN:
        to_create = asset_type.creator(
            name=f"{segment}_{MODULE_NAME}",
            micro_strategy_project_qualified_name=project.qualified_name,
            micro_strategy_project_name=project.name,
            micro_strategy_id=_mstr_id(segment),
        )
        created[asset_type] = client.asset.save(to_create).assets_created(
            asset_type=asset_type
        )[0]
    yield created
    for asset_type, asset in created.items():
        delete_asset(client, guid=asset.guid, asset_type=asset_type)


@pytest.fixture(scope="module")
def visualization(
    client: AtlanClient, project_children: dict
) -> Generator[MicroStrategyVisualization, None, None]:
    dossier = project_children[MicroStrategyDossier]
    to_create = MicroStrategyVisualization.creator(
        name=f"visualization_{MODULE_NAME}",
        micro_strategy_dossier_qualified_name=dossier.qualified_name,
        micro_strategy_dossier_name=dossier.name,
        chapter_key="K53",
        page_key="K66",
        visualization_key="W71",
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=MicroStrategyVisualization
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MicroStrategyVisualization)


@pytest.fixture(scope="module")
def column(
    client: AtlanClient, project_children: dict
) -> Generator[MicroStrategyColumn, None, None]:
    to_create = MicroStrategyColumn.creator(
        name=f"column_{MODULE_NAME}",
        parent_qualified_name=project_children[MicroStrategyAttribute].qualified_name,
        micro_strategy_id=_mstr_id("columns"),
    )
    result = client.asset.save(to_create).assets_created(
        asset_type=MicroStrategyColumn
    )[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MicroStrategyColumn)


def _retrieve(client, asset, asset_type, connection):
    retrieved = client.asset.get_by_guid(
        asset.guid, asset_type=asset_type, ignore_relationships=False
    )
    assert retrieved.name == asset.name
    assert retrieved.connector_name == AtlanConnectorType.MICROSTRATEGY.value
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_project(
    client: AtlanClient, connection: Connection, project: MicroStrategyProject
):
    retrieved = _retrieve(client, project, MicroStrategyProject, connection)
    assert retrieved.qualified_name == (
        f"{connection.qualified_name}/projects/{_mstr_id('projects')}"
    )


def test_project_children(
    client: AtlanClient,
    connection: Connection,
    project: MicroStrategyProject,
    project_children: dict,
):
    for asset_type, segment in PROJECT_CHILDREN:
        retrieved = _retrieve(
            client, project_children[asset_type], asset_type, connection
        )
        assert retrieved.qualified_name == (
            f"{project.qualified_name}/{segment}/{_mstr_id(segment)}"
        )
        assert retrieved.micro_strategy_project_qualified_name == (
            project.qualified_name
        )
        assert retrieved.micro_strategy_project_name == project.name
        assert retrieved.micro_strategy_project.guid == project.guid


def test_visualization(
    client: AtlanClient,
    connection: Connection,
    project_children: dict,
    visualization: MicroStrategyVisualization,
):
    dossier = project_children[MicroStrategyDossier]
    retrieved = _retrieve(client, visualization, MicroStrategyVisualization, connection)
    assert retrieved.qualified_name == (
        f"{dossier.qualified_name}/chapters/K53/pages/K66/visualizations/W71"
    )
    assert retrieved.micro_strategy_dossier_qualified_name == dossier.qualified_name
    assert retrieved.micro_strategy_dossier.guid == dossier.guid


def test_column(
    client: AtlanClient,
    connection: Connection,
    project: MicroStrategyProject,
    project_children: dict,
    column: MicroStrategyColumn,
):
    attribute = project_children[MicroStrategyAttribute]
    retrieved = _retrieve(client, column, MicroStrategyColumn, connection)
    assert retrieved.qualified_name == (
        f"{project.qualified_name}/columns/{_mstr_id('columns')}"
    )
    assert retrieved.micro_strategy_project_qualified_name == project.qualified_name
    assert retrieved.micro_strategy_column_attribute_qualified_name == (
        attribute.qualified_name
    )
    assert retrieved.micro_strategy_attribute.guid == attribute.guid
