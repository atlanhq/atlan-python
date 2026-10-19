# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

import hashlib
from typing import Generator, Type

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    ContextRepository,
    Database,
    DatabricksAIModelContext,
    DatabricksAIModelVersion,
    DatabricksDashboard,
    DatabricksExternalLocation,
    DatabricksExternalLocationPath,
    DatabricksGenieAgent,
    DatabricksMetricView,
    DatabricksNotebook,
    DatabricksUnityCatalogTag,
    DatabricksVolume,
    DatabricksVolumePath,
    Schema,
    Skill,
    SkillArtifact,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("DATABRICKS")
DATABASE_NAME = f"db_{MODULE_NAME}"
SCHEMA_NAME = f"schema_{MODULE_NAME}"
VOLUME_NAME = f"volume_{MODULE_NAME}"
WORKSPACE_ID = "1234567890123456"
SCOPE_OWNER = "someone@example.com"


def _save(client: AtlanClient, to_create, asset_type: Type):
    return client.asset.save(to_create).assets_created(asset_type=asset_type)[0]


def _assert_parent(client: AtlanClient, child, asset_type: Type, rel: str, parent):
    asset = client.asset.get_by_qualified_name(
        qualified_name=child.qualified_name,
        asset_type=asset_type,
        ignore_relationships=False,
    )
    assert asset.guid == child.guid
    assert getattr(asset, rel).guid == parent.guid


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.DATABRICKS
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def database(
    client: AtlanClient, connection: Connection
) -> Generator[Database, None, None]:
    to_create = Database.creator(
        name=DATABASE_NAME, connection_qualified_name=connection.qualified_name
    )
    result = _save(client, to_create, Database)
    yield result
    delete_asset(client, guid=result.guid, asset_type=Database)


@pytest.fixture(scope="module")
def schema(client: AtlanClient, database: Database) -> Generator[Schema, None, None]:
    to_create = Schema.creator(
        name=SCHEMA_NAME, database_qualified_name=database.qualified_name
    )
    result = _save(client, to_create, Schema)
    yield result
    delete_asset(client, guid=result.guid, asset_type=Schema)


@pytest.fixture(scope="module")
def metric_view(
    client: AtlanClient, schema: Schema
) -> Generator[DatabricksMetricView, None, None]:
    to_create = DatabricksMetricView.creator(
        name=f"metric_view_{MODULE_NAME}",
        schema_qualified_name=schema.qualified_name,
    )
    result = _save(client, to_create, DatabricksMetricView)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DatabricksMetricView)


@pytest.fixture(scope="module")
def volume(
    client: AtlanClient, schema: Schema
) -> Generator[DatabricksVolume, None, None]:
    to_create = DatabricksVolume.creator(
        name=VOLUME_NAME, schema_qualified_name=schema.qualified_name
    )
    result = _save(client, to_create, DatabricksVolume)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DatabricksVolume)


@pytest.fixture(scope="module")
def volume_path(
    client: AtlanClient, volume: DatabricksVolume
) -> Generator[DatabricksVolumePath, None, None]:
    to_create = DatabricksVolumePath.creator(
        path=f"/Volumes/{DATABASE_NAME}/{SCHEMA_NAME}/{VOLUME_NAME}/2026/orders.csv",
        volume_qualified_name=volume.qualified_name,
    )
    result = _save(client, to_create, DatabricksVolumePath)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DatabricksVolumePath)


@pytest.fixture(scope="module")
def ai_model(
    client: AtlanClient, schema: Schema
) -> Generator[DatabricksAIModelContext, None, None]:
    to_create = DatabricksAIModelContext.creator(
        name=f"model_{MODULE_NAME}", schema_qualified_name=schema.qualified_name
    )
    result = _save(client, to_create, DatabricksAIModelContext)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DatabricksAIModelContext)


@pytest.fixture(scope="module")
def ai_model_version(
    client: AtlanClient, ai_model: DatabricksAIModelContext
) -> Generator[DatabricksAIModelVersion, None, None]:
    to_create = DatabricksAIModelVersion.creator(
        model_qualified_name=ai_model.qualified_name, version=3
    )
    result = _save(client, to_create, DatabricksAIModelVersion)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DatabricksAIModelVersion)


@pytest.fixture(scope="module")
def external_location(
    client: AtlanClient, connection: Connection
) -> Generator[DatabricksExternalLocation, None, None]:
    to_create = DatabricksExternalLocation.creator(
        name=f"ext_{MODULE_NAME}", connection_qualified_name=connection.qualified_name
    )
    result = _save(client, to_create, DatabricksExternalLocation)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DatabricksExternalLocation)


@pytest.fixture(scope="module")
def external_location_path(
    client: AtlanClient, external_location: DatabricksExternalLocation
) -> Generator[DatabricksExternalLocationPath, None, None]:
    to_create = DatabricksExternalLocationPath.creator(
        path="s3://example-bucket/raw/orders/",
        external_location_qualified_name=external_location.qualified_name,
    )
    result = _save(client, to_create, DatabricksExternalLocationPath)
    yield result
    delete_asset(client, guid=result.guid, asset_type=DatabricksExternalLocationPath)


@pytest.fixture(scope="module")
def workspace_assets(
    client: AtlanClient, connection: Connection
) -> Generator[dict, None, None]:
    conn_qn = connection.qualified_name
    to_create = {
        DatabricksDashboard: DatabricksDashboard.creator(
            name=f"dashboard_{MODULE_NAME}",
            connection_qualified_name=conn_qn,
            workspace_id=WORKSPACE_ID,
            dashboard_id=f"d{MODULE_NAME}",
        ),
        DatabricksNotebook: DatabricksNotebook.creator(
            connection_qualified_name=conn_qn,
            workspace_id=WORKSPACE_ID,
            notebook_path=f"/Users/{SCOPE_OWNER}/{MODULE_NAME}",
        ),
        DatabricksGenieAgent: DatabricksGenieAgent.creator(
            name=f"genie_{MODULE_NAME}",
            connection_qualified_name=conn_qn,
            workspace_id=WORKSPACE_ID,
            space_id=f"g{MODULE_NAME}",
        ),
        DatabricksUnityCatalogTag: DatabricksUnityCatalogTag.creator(
            name=f"tag_{MODULE_NAME}", connection_qualified_name=conn_qn
        ),
    }
    created = {
        asset_type: _save(client, asset, asset_type)
        for asset_type, asset in to_create.items()
    }
    yield created
    for asset_type, asset in created.items():
        delete_asset(client, guid=asset.guid, asset_type=asset_type)


@pytest.fixture(scope="module")
def context_repository(
    client: AtlanClient, connection: Connection
) -> Generator[ContextRepository, None, None]:
    to_create = ContextRepository.creator(
        scope_owner=f"{MODULE_NAME}@example.com",
        connection_qualified_name=connection.qualified_name,
    )
    result = _save(client, to_create, ContextRepository)
    yield result
    delete_asset(client, guid=result.guid, asset_type=ContextRepository)


@pytest.fixture(scope="module")
def skill(
    client: AtlanClient, context_repository: ContextRepository
) -> Generator[Skill, None, None]:
    to_create = Skill.creator(
        name=f"skill-{MODULE_NAME}",
        context_repository_qualified_name=context_repository.qualified_name,
    )
    result = _save(client, to_create, Skill)
    yield result
    delete_asset(client, guid=result.guid, asset_type=Skill)


@pytest.fixture(scope="module")
def skill_artifact(
    client: AtlanClient, skill: Skill
) -> Generator[SkillArtifact, None, None]:
    to_create = SkillArtifact.creator(
        skill_qualified_name=skill.qualified_name,
        relative_path="scripts/run.py",
        # The app maps extensions without an enum value (py, sh) to txt.
        file_type="txt",
    )
    result = _save(client, to_create, SkillArtifact)
    yield result
    delete_asset(client, guid=result.guid, asset_type=SkillArtifact)


@pytest.mark.parametrize(
    "fixture_name, asset_type, rel",
    [
        ("metric_view", DatabricksMetricView, "atlan_schema"),
        ("volume", DatabricksVolume, "databricks_volume_schema"),
        ("ai_model", DatabricksAIModelContext, "databricks_ai_model_schema"),
    ],
)
def test_schema_scoped(
    request, client: AtlanClient, schema: Schema, fixture_name, asset_type, rel
):
    asset = request.getfixturevalue(fixture_name)
    assert asset.guid
    assert asset.qualified_name == f"{schema.qualified_name}/{asset.name}"
    _assert_parent(client, asset, asset_type, rel, schema)


def test_volume_path(
    client: AtlanClient,
    volume: DatabricksVolume,
    volume_path: DatabricksVolumePath,
):
    assert volume_path.guid
    assert volume_path.qualified_name == f"{volume.qualified_name}/2026/orders.csv"
    _assert_parent(
        client, volume_path, DatabricksVolumePath, "databricks_volume", volume
    )


def test_ai_model_version(
    client: AtlanClient,
    ai_model: DatabricksAIModelContext,
    ai_model_version: DatabricksAIModelVersion,
):
    assert ai_model_version.guid
    assert ai_model_version.qualified_name == f"{ai_model.qualified_name}/version/3"
    assert ai_model_version.name == f"{ai_model.name}_v3"
    _assert_parent(
        client,
        ai_model_version,
        DatabricksAIModelVersion,
        "databricks_ai_model_context",
        ai_model,
    )


def test_external_location_path(
    client: AtlanClient,
    connection: Connection,
    external_location: DatabricksExternalLocation,
    external_location_path: DatabricksExternalLocationPath,
):
    assert external_location.qualified_name == (
        f"{connection.qualified_name}/ext_{MODULE_NAME}"
    )
    path_hash = hashlib.md5(
        b"s3://example-bucket/raw/orders/", usedforsecurity=False
    ).hexdigest()
    assert external_location_path.qualified_name == (
        f"{external_location.qualified_name}/{path_hash}"
    )
    _assert_parent(
        client,
        external_location_path,
        DatabricksExternalLocationPath,
        "databricks_external_location",
        external_location,
    )


def test_workspace_assets(connection: Connection, workspace_assets: dict):
    conn_qn = connection.qualified_name
    expected = {
        DatabricksDashboard: f"{conn_qn}/{WORKSPACE_ID}/dashboards/d{MODULE_NAME}",
        DatabricksNotebook: f"{conn_qn}/{WORKSPACE_ID}//Users/{SCOPE_OWNER}/{MODULE_NAME}",
        DatabricksGenieAgent: f"{conn_qn}/{WORKSPACE_ID}/genie-spaces/g{MODULE_NAME}",
        DatabricksUnityCatalogTag: f"{conn_qn}/tag/tag_{MODULE_NAME}",
    }
    for asset_type, qualified_name in expected.items():
        asset = workspace_assets[asset_type]
        assert asset.guid
        assert asset.qualified_name == qualified_name


def test_skills(
    client: AtlanClient,
    connection: Connection,
    context_repository: ContextRepository,
    skill: Skill,
    skill_artifact: SkillArtifact,
):
    conn_qn = connection.qualified_name
    scope_owner = f"{MODULE_NAME}@example.com"
    assert context_repository.qualified_name == f"{conn_qn}/skills/{scope_owner}"
    assert skill.qualified_name == f"{conn_qn}/skill/{scope_owner}/skill-{MODULE_NAME}"
    assert skill_artifact.qualified_name == (
        f"{skill.qualified_name}/artifact/scripts/run.py"
    )
    _assert_parent(
        client, skill, Skill, "context_source_repository", context_repository
    )
    _assert_parent(client, skill_artifact, SkillArtifact, "skill_source", skill)
