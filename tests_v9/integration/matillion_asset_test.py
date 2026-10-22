# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    MatillionComponent,
    MatillionGroup,
    MatillionJob,
    MatillionProject,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("MATILLION")


def _matillion_id(slug: str) -> str:
    return f"i{slug}{MODULE_NAME}"


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.MATILLION
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


# The group, project and job have no creators yet, so they are built directly
# with the qualifiedNames atlan-matillion-app emits.
@pytest.fixture(scope="module")
def group(
    client: AtlanClient, connection: Connection
) -> Generator[MatillionGroup, None, None]:
    to_create = MatillionGroup(
        name=f"group_{MODULE_NAME}",
        qualified_name=f"{connection.qualified_name}/group/{_matillion_id('group')}",
        connection_qualified_name=connection.qualified_name,
        connector_name=AtlanConnectorType.MATILLION.value,
    )
    result = client.asset.save(to_create).assets_created(asset_type=MatillionGroup)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MatillionGroup)


@pytest.fixture(scope="module")
def project(
    client: AtlanClient, connection: Connection, group: MatillionGroup
) -> Generator[MatillionProject, None, None]:
    to_create = MatillionProject(
        name=f"project_{MODULE_NAME}",
        qualified_name=f"{connection.qualified_name}/project/{_matillion_id('project')}",
        connection_qualified_name=connection.qualified_name,
        connector_name=AtlanConnectorType.MATILLION.value,
        matillion_group_name=group.name,
        matillion_group_qualified_name=group.qualified_name,
        matillion_group=group.relate(),
    )
    result = client.asset.save(to_create).assets_created(asset_type=MatillionProject)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MatillionProject)


@pytest.fixture(scope="module")
def job(
    client: AtlanClient, connection: Connection, project: MatillionProject
) -> Generator[MatillionJob, None, None]:
    to_create = MatillionJob(
        name=f"job_{MODULE_NAME}",
        qualified_name=f"{connection.qualified_name}/job/{_matillion_id('job')}",
        connection_qualified_name=connection.qualified_name,
        connector_name=AtlanConnectorType.MATILLION.value,
        matillion_project_name=project.name,
        matillion_project_qualified_name=project.qualified_name,
        matillion_project=project.relate(),
    )
    result = client.asset.save(to_create).assets_created(asset_type=MatillionJob)[0]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MatillionJob)


@pytest.fixture(scope="module")
def component(
    client: AtlanClient, job: MatillionJob
) -> Generator[MatillionComponent, None, None]:
    to_create = MatillionComponent.creator(
        name=f"component_{MODULE_NAME}",
        matillion_component_id=_matillion_id("component"),
        matillion_job_qualified_name=job.qualified_name,
        matillion_job_name=job.name,
    )
    result = client.asset.save(to_create).assets_created(asset_type=MatillionComponent)[
        0
    ]
    yield result
    delete_asset(client, guid=result.guid, asset_type=MatillionComponent)


def test_component(
    client: AtlanClient,
    connection: Connection,
    job: MatillionJob,
    component: MatillionComponent,
):
    expected_qn = f"{connection.qualified_name}/component/{_matillion_id('component')}"
    assert component.guid
    assert component.qualified_name == expected_qn
    assert component.name == f"component_{MODULE_NAME}"
    assert component.connection_qualified_name == connection.qualified_name
    assert component.connector_name == AtlanConnectorType.MATILLION.value

    retrieved = client.asset.get_by_qualified_name(
        qualified_name=expected_qn,
        asset_type=MatillionComponent,
        ignore_relationships=False,
    )
    assert retrieved.guid == component.guid
    assert retrieved.matillion_component_id == _matillion_id("component")
    assert retrieved.matillion_job_qualified_name == job.qualified_name
    assert retrieved.matillion_job_name == job.name
    assert retrieved.matillion_job.guid == job.guid
