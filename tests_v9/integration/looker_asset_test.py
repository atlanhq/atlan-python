# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Integration tests for the Looker creators in pyatlan_v9.

Creates every Looker type through its creator, with each parent and field shape the
creators support, then retrieves each asset and checks the exact qualifiedName
atlan-looker-app emits, its denormalised attributes and its parent relationships.
"""

import hashlib
from typing import Generator

import pytest

from pyatlan_v9.client.atlan import AtlanClient
from pyatlan_v9.model.assets import (
    Connection,
    LookerDashboard,
    LookerExplore,
    LookerField,
    LookerFolder,
    LookerLook,
    LookerModel,
    LookerProject,
    LookerTile,
    LookerView,
)
from pyatlan_v9.model.enums import AtlanConnectorType
from tests_v9.integration.client import TestId, delete_asset
from tests_v9.integration.connection_test import create_connection

MODULE_NAME = TestId.make_unique("LOOKER")

PROJECT = "ecom"
MODEL = "ecommerce"
EXPLORE = "order_items"
VIEW = "orders"
VIEW_FILE = "/tmp/workflow/cloned_repos/ecom/views/orders.view.lkml"
VIEW_HASH = hashlib.md5(b"ecom/views/orders.view.lkml").hexdigest()  # noqa: S324
REFINEMENT_FILE = "ecom/refinements.lkml"
REFINEMENT_LINE = "12"
REFINEMENT_HASH = hashlib.md5(b"ecom/refinements.lkml:12").hexdigest()  # noqa: S324
FIELD = "orders.status"


def _save(client: AtlanClient, asset):
    asset_type = type(asset)
    return client.asset.save(asset).assets_created(asset_type=asset_type)[0]


def _get(client: AtlanClient, asset):
    return client.asset.get_by_guid(
        asset.guid, asset_type=type(asset), ignore_relationships=False
    )


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=AtlanConnectorType.LOOKER
    )
    yield result
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def assets(client: AtlanClient, connection: Connection) -> Generator[dict, None, None]:
    """Create every asset under test, parents before children, and purge them after."""
    conn_qn = connection.qualified_name
    created: dict = {}

    def save(key, asset):
        created[key] = _save(client, asset)
        return created[key]

    try:
        project = save(
            "project",
            LookerProject.creator(name=PROJECT, connection_qualified_name=conn_qn),
        )
        model = save(
            "model",
            LookerModel.creator(
                name=MODEL, project_qualified_name=project.qualified_name
            ),
        )
        explore = save(
            "explore",
            LookerExplore.creator(
                name=EXPLORE, model_qualified_name=model.qualified_name
            ),
        )
        view = save(
            "view",
            LookerView.creator(
                name=VIEW,
                project_qualified_name=project.qualified_name,
                file_path=VIEW_FILE,
            ),
        )
        folder = save(
            "folder",
            LookerFolder.creator(
                name=f"folder_{MODULE_NAME}",
                connection_qualified_name=conn_qn,
                folder_id=6.0,
            ),
        )
        save(
            "subfolder",
            LookerFolder.creator(
                name=f"subfolder_{MODULE_NAME}",
                connection_qualified_name=conn_qn,
                folder_id=7,
                parent_folder_qualified_name=folder.qualified_name,
            ),
        )
        dashboard = save(
            "dashboard",
            LookerDashboard.creator(
                name=f"dashboard_{MODULE_NAME}",
                connection_qualified_name=conn_qn,
                dashboard_id=988,
                folder_qualified_name=folder.qualified_name,
                folder_name=folder.name,
            ),
        )
        save(
            "lookml_dashboard",
            LookerDashboard.creator(
                name=f"lookml_dashboard_{MODULE_NAME}",
                connection_qualified_name=conn_qn,
                dashboard_id=f"{MODEL}::kpis",
            ),
        )
        look = save(
            "look",
            LookerLook.creator(
                name=f"look_{MODULE_NAME}",
                connection_qualified_name=conn_qn,
                look_id="011",
                folder_qualified_name=folder.qualified_name,
                folder_name=folder.name,
            ),
        )
        tile = save(
            "tile",
            LookerTile.creator(
                name=f"tile_{MODULE_NAME}",
                dashboard_qualified_name=dashboard.qualified_name,
                tile_id=25,
                look_qualified_name=look.qualified_name,
            ),
        )
        save(
            "explore_field",
            LookerField.creator(
                name=FIELD, explore_qualified_name=explore.qualified_name
            ),
        )
        save(
            "view_field",
            LookerField.creator(name="status", view_qualified_name=view.qualified_name),
        )
        save(
            "refined_view_field",
            LookerField.creator(
                name="status",
                view_qualified_name=view.qualified_name,
                refinement_file_path=REFINEMENT_FILE,
                refinement_line_number=REFINEMENT_LINE,
            ),
        )
        save(
            "dashboard_field",
            LookerField.creator(
                name="orders.count",
                dashboard_qualified_name=dashboard.qualified_name,
                tile_id=26.0,
            ),
        )
        save(
            "look_field",
            LookerField.creator(name=FIELD, look_qualified_name=look.qualified_name),
        )
        save(
            "tile_field",
            LookerField.creator(name=FIELD, tile_qualified_name=tile.qualified_name),
        )
        yield created
    finally:
        # Children were created after their parents, so purge in reverse.
        for asset in reversed(list(created.values())):
            delete_asset(client, guid=asset.guid, asset_type=type(asset))


def _assert_common(client, asset, connection, expected_qn):
    retrieved = _get(client, asset)
    assert retrieved.qualified_name == expected_qn
    assert retrieved.name == asset.name
    assert retrieved.connector_name == "looker"
    assert retrieved.connection_qualified_name == connection.qualified_name
    return retrieved


def test_project(client: AtlanClient, connection: Connection, assets: dict):
    _assert_common(
        client,
        assets["project"],
        connection,
        f"{connection.qualified_name}/project/{PROJECT}",
    )


def test_model(client: AtlanClient, connection: Connection, assets: dict):
    retrieved = _assert_common(
        client,
        assets["model"],
        connection,
        f"{connection.qualified_name}/project/{PROJECT}/model/{MODEL}",
    )
    assert retrieved.project_name == PROJECT
    assert retrieved.project.guid == assets["project"].guid


def test_explore(client: AtlanClient, connection: Connection, assets: dict):
    retrieved = _assert_common(
        client,
        assets["explore"],
        connection,
        f"{connection.qualified_name}/project/{PROJECT}/model/{MODEL}"
        f"/{MODEL}::{EXPLORE}",
    )
    assert retrieved.project_name == PROJECT
    assert retrieved.model_name == MODEL
    assert retrieved.project.guid == assets["project"].guid
    assert retrieved.model.guid == assets["model"].guid


def test_view(client: AtlanClient, connection: Connection, assets: dict):
    retrieved = _assert_common(
        client,
        assets["view"],
        connection,
        f"{connection.qualified_name}/project/{PROJECT}/view/{VIEW_HASH}/{VIEW}",
    )
    assert retrieved.project_name == PROJECT
    assert retrieved.looker_view_file_path == VIEW_FILE
    assert retrieved.project.guid == assets["project"].guid


def test_folders(client: AtlanClient, connection: Connection, assets: dict):
    _assert_common(
        client, assets["folder"], connection, f"{connection.qualified_name}/folder/6"
    )
    subfolder = _assert_common(
        client,
        assets["subfolder"],
        connection,
        f"{connection.qualified_name}/folder/7",
    )
    assert subfolder.looker_parent_folder.guid == assets["folder"].guid


def test_dashboards(client: AtlanClient, connection: Connection, assets: dict):
    dashboard = _assert_common(
        client,
        assets["dashboard"],
        connection,
        f"{connection.qualified_name}/dashboard/988",
    )
    assert dashboard.folder.guid == assets["folder"].guid
    assert dashboard.folder_name == assets["folder"].name

    # A LookML dashboard has no folder.
    lookml = _assert_common(
        client,
        assets["lookml_dashboard"],
        connection,
        f"{connection.qualified_name}/dashboard/{MODEL}::kpis",
    )
    assert not lookml.folder


def test_look(client: AtlanClient, connection: Connection, assets: dict):
    # Leading zeros are dropped from a numeric look id, as the app does.
    retrieved = _assert_common(
        client, assets["look"], connection, f"{connection.qualified_name}/look/11"
    )
    assert retrieved.folder.guid == assets["folder"].guid
    assert retrieved.folder_name == assets["folder"].name


def test_tile(client: AtlanClient, connection: Connection, assets: dict):
    retrieved = _assert_common(
        client, assets["tile"], connection, f"{connection.qualified_name}/tile/25"
    )
    assert retrieved.dashboard.guid == assets["dashboard"].guid
    assert retrieved.look.guid == assets["look"].guid


def test_explore_field(client: AtlanClient, connection: Connection, assets: dict):
    model_qn = assets["model"].qualified_name
    retrieved = _assert_common(
        client,
        assets["explore_field"],
        connection,
        f"{model_qn}/{EXPLORE}/{FIELD}",
    )
    assert retrieved.project_name == PROJECT
    assert retrieved.model_name == MODEL
    assert retrieved.looker_explore_qualified_name == assets["explore"].qualified_name
    assert retrieved.project.guid == assets["project"].guid
    assert retrieved.model.guid == assets["model"].guid
    assert retrieved.explore.guid == assets["explore"].guid


def test_view_fields(client: AtlanClient, connection: Connection, assets: dict):
    view = assets["view"]
    plain = _assert_common(
        client, assets["view_field"], connection, f"{view.qualified_name}/status"
    )
    refined = _assert_common(
        client,
        assets["refined_view_field"],
        connection,
        f"{connection.qualified_name}/{REFINEMENT_HASH}/project/{PROJECT}"
        f"/view/{VIEW_HASH}/{VIEW}/status",
    )
    for retrieved in (plain, refined):
        assert retrieved.project_name == PROJECT
        assert retrieved.looker_view_qualified_name == view.qualified_name
        assert retrieved.project.guid == assets["project"].guid
        assert retrieved.view.guid == view.guid
    assert refined.looker_field_is_refined is True
    assert refined.looker_field_refinement_file_path == REFINEMENT_FILE
    assert refined.looker_field_refinement_line_number == REFINEMENT_LINE


def test_content_fields(client: AtlanClient, connection: Connection, assets: dict):
    dashboard, look, tile = assets["dashboard"], assets["look"], assets["tile"]

    dashboard_field = _assert_common(
        client,
        assets["dashboard_field"],
        connection,
        f"{dashboard.qualified_name}/26/orders.count",
    )
    assert dashboard_field.looker_dashboard_qualified_name == dashboard.qualified_name
    assert dashboard_field.dashboard.guid == dashboard.guid

    look_field = _assert_common(
        client, assets["look_field"], connection, f"{look.qualified_name}/{FIELD}"
    )
    assert look_field.looker_look_qualified_name == look.qualified_name
    assert look_field.look.guid == look.guid

    tile_field = _assert_common(
        client, assets["tile_field"], connection, f"{tile.qualified_name}/{FIELD}"
    )
    assert tile_field.looker_tile_qualified_name == tile.qualified_name
    assert tile_field.tile.guid == tile.guid
