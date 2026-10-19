# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.

"""Unit tests for the Looker creators in pyatlan_v9.

The expected qualifiedNames are the exact strings atlan-looker-app emits today
(FND-3838 census, the app's tests/unit/test_asset_mapper.py literals), so a creator
change that would re-key existing Looker assets fails here.
"""

import hashlib

import pytest
from msgspec import UNSET

from pyatlan_v9.model import (
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

CONNECTION_QN = "default/looker/test"
PROJECT_QN = f"{CONNECTION_QN}/project/ecom"
MODEL_QN = f"{PROJECT_QN}/model/ecommerce"
EXPLORE_QN = f"{MODEL_QN}/ecommerce::order_items"
VIEW_FILE = "ecom/views/orders.view.lkml"
VIEW_HASH = hashlib.md5(VIEW_FILE.encode("utf-8")).hexdigest()  # noqa: S324
VIEW_QN = f"{PROJECT_QN}/view/{VIEW_HASH}/orders"
FOLDER_QN = f"{CONNECTION_QN}/folder/6"
DASHBOARD_QN = f"{CONNECTION_QN}/dashboard/988"
LOOK_QN = f"{CONNECTION_QN}/look/11"
TILE_QN = f"{CONNECTION_QN}/tile/14"


def _assert_common(asset, expected_qn):
    assert asset.qualified_name == expected_qn
    assert asset.connection_qualified_name == CONNECTION_QN
    assert asset.connector_name == "looker"
    assert asset._QUALIFIED_NAME_PATTERN.match(asset.qualified_name)
    assert int(asset.guid) < 0
    asset.validate(for_creation=True)


def test_project():
    sut = LookerProject.creator(name="ecom", connection_qualified_name=CONNECTION_QN)

    _assert_common(sut, "default/looker/test/project/ecom")
    assert sut.name == "ecom"


def test_model():
    sut = LookerModel.creator(name="ecommerce", project_qualified_name=PROJECT_QN)

    _assert_common(sut, "default/looker/test/project/ecom/model/ecommerce")
    assert sut.project_name == "ecom"
    assert sut.project.qualified_name == PROJECT_QN


def test_explore():
    sut = LookerExplore.creator(name="order_items", model_qualified_name=MODEL_QN)

    _assert_common(
        sut, "default/looker/test/project/ecom/model/ecommerce/ecommerce::order_items"
    )
    assert sut.project_name == "ecom"
    assert sut.model_name == "ecommerce"
    assert sut.project.qualified_name == PROJECT_QN
    assert sut.model.qualified_name == MODEL_QN


@pytest.mark.parametrize(
    "file_path",
    [VIEW_FILE, f"/tmp/workflow/cloned_repos/{VIEW_FILE}"],
)
def test_view_hashes_file_path_relative_to_cloned_repos(file_path):
    sut = LookerView.creator(
        name="orders", project_qualified_name=PROJECT_QN, file_path=file_path
    )

    _assert_common(sut, f"default/looker/test/project/ecom/view/{VIEW_HASH}/orders")
    assert sut.project_name == "ecom"
    assert sut.project.qualified_name == PROJECT_QN
    assert sut.looker_view_file_path == file_path


def test_explore_field():
    sut = LookerField.creator(name="orders.status", explore_qualified_name=EXPLORE_QN)

    # The explore segment drops the "{model}::" prefix, as the app does.
    _assert_common(
        sut,
        "default/looker/test/project/ecom/model/ecommerce/order_items/orders.status",
    )
    assert sut.project_name == "ecom"
    assert sut.model_name == "ecommerce"
    assert sut.project.qualified_name == PROJECT_QN
    assert sut.model.qualified_name == MODEL_QN
    assert sut.explore.qualified_name == EXPLORE_QN
    assert sut.looker_explore_qualified_name == EXPLORE_QN


def test_view_field():
    sut = LookerField.creator(name="status", view_qualified_name=VIEW_QN)

    _assert_common(sut, f"{VIEW_QN}/status")
    assert sut.project_name == "ecom"
    assert sut.project.qualified_name == PROJECT_QN
    assert sut.view.qualified_name == VIEW_QN
    assert sut.looker_view_qualified_name == VIEW_QN
    assert sut.model is UNSET
    assert sut.model_name is UNSET


def test_refined_view_field():
    refinement = hashlib.md5(b"ecom/refinements.lkml:12").hexdigest()  # noqa: S324

    sut = LookerField.creator(
        name="status",
        view_qualified_name=VIEW_QN,
        refinement_file_path="/x/cloned_repos/ecom/refinements.lkml",
        refinement_line_number="12",
    )

    _assert_common(
        sut,
        f"default/looker/test/{refinement}/project/ecom/view/{VIEW_HASH}/orders/status",
    )
    assert sut.view.qualified_name == VIEW_QN
    assert sut.looker_field_is_refined is True
    assert sut.looker_field_refinement_line_number == "12"


def test_refined_explore_field_keeps_its_qualified_name():
    sut = LookerField.creator(
        name="orders.status",
        explore_qualified_name=EXPLORE_QN,
        refinement_file_path="ecom/refinements.lkml",
        refinement_line_number="12",
    )

    assert sut.qualified_name == f"{MODEL_QN}/order_items/orders.status"
    assert sut.looker_field_is_refined is True


@pytest.mark.parametrize("tile_id", ["26", 26, 26.0])
def test_dashboard_field(tile_id):
    sut = LookerField.creator(
        name="orders.count", dashboard_qualified_name=DASHBOARD_QN, tile_id=tile_id
    )

    _assert_common(sut, "default/looker/test/dashboard/988/26/orders.count")
    assert sut.dashboard.qualified_name == DASHBOARD_QN
    assert sut.looker_dashboard_qualified_name == DASHBOARD_QN


def test_look_field():
    sut = LookerField.creator(name="orders.status", look_qualified_name=LOOK_QN)

    _assert_common(sut, "default/looker/test/look/11/orders.status")
    assert sut.look.qualified_name == LOOK_QN
    assert sut.looker_look_qualified_name == LOOK_QN


def test_tile_field():
    sut = LookerField.creator(
        name="order_items.first_purchase_count", tile_qualified_name=TILE_QN
    )

    _assert_common(sut, "default/looker/test/tile/14/order_items.first_purchase_count")
    assert sut.tile.qualified_name == TILE_QN
    assert sut.looker_tile_qualified_name == TILE_QN


@pytest.mark.parametrize("folder_id", ["6", 6, 6.0])
def test_folder(folder_id):
    sut = LookerFolder.creator(
        name="Shared", connection_qualified_name=CONNECTION_QN, folder_id=folder_id
    )

    _assert_common(sut, "default/looker/test/folder/6")


def test_virtual_lookml_folder():
    sut = LookerFolder.creator(
        name="LookML", connection_qualified_name=CONNECTION_QN, folder_id="lookml"
    )

    _assert_common(sut, "default/looker/test/folder/lookml")


def test_subfolder():
    sut = LookerFolder.creator(
        name="Team",
        connection_qualified_name=CONNECTION_QN,
        folder_id=7,
        parent_folder_qualified_name=FOLDER_QN,
    )

    assert sut.looker_parent_folder.qualified_name == FOLDER_QN


@pytest.mark.parametrize(
    "dashboard_id, expected_qn",
    [
        (988, "default/looker/test/dashboard/988"),
        (988.0, "default/looker/test/dashboard/988"),
        ("model::kpis", "default/looker/test/dashboard/model::kpis"),
    ],
)
def test_dashboard(dashboard_id, expected_qn):
    sut = LookerDashboard.creator(
        name="KPIs", connection_qualified_name=CONNECTION_QN, dashboard_id=dashboard_id
    )

    # A LookML dashboard has no folder, so the creator leaves it unset.
    _assert_common(sut, expected_qn)


@pytest.mark.parametrize(
    "look_id, expected_qn",
    [
        ("11", "default/looker/test/look/11"),
        (12.0, "default/looker/test/look/12"),
        ("012", "default/looker/test/look/12"),
    ],
)
def test_look(look_id, expected_qn):
    sut = LookerLook.creator(
        name="Orders", connection_qualified_name=CONNECTION_QN, look_id=look_id
    )

    _assert_common(sut, expected_qn)


@pytest.mark.parametrize(
    "asset_type, id_kwarg", [(LookerDashboard, "dashboard_id"), (LookerLook, "look_id")]
)
def test_folder_parent(asset_type, id_kwarg):
    sut = asset_type.creator(
        name="Orders",
        connection_qualified_name=CONNECTION_QN,
        folder_qualified_name=FOLDER_QN,
        folder_name="Shared",
        **{id_kwarg: 11},
    )

    assert sut.folder.qualified_name == FOLDER_QN
    assert sut.folder_name == "Shared"


def test_tile():
    sut = LookerTile.creator(
        name="Orders by day",
        dashboard_qualified_name=DASHBOARD_QN,
        tile_id=25,
        look_qualified_name=LOOK_QN,
    )

    # Not nested under the dashboard, as the app emits it.
    _assert_common(sut, "default/looker/test/tile/25")
    assert sut.dashboard.qualified_name == DASHBOARD_QN
    assert sut.look.qualified_name == LOOK_QN


@pytest.mark.parametrize(
    "creator, kwargs, message",
    [
        (
            LookerProject.creator,
            {"name": " ", "connection_qualified_name": CONNECTION_QN},
            "name cannot be blank",
        ),
        (
            LookerProject.creator,
            {"name": "ecom", "connection_qualified_name": None},
            "connection_qualified_name is required",
        ),
        (
            LookerProject.creator,
            {"name": "ecom", "connection_qualified_name": "default/looker"},
            "Invalid connection_qualified_name",
        ),
        (
            LookerModel.creator,
            {"name": "m", "project_qualified_name": MODEL_QN},
            "Invalid project_qualified_name",
        ),
        (
            LookerExplore.creator,
            {"name": "e", "model_qualified_name": PROJECT_QN},
            "Invalid model_qualified_name",
        ),
        (
            LookerView.creator,
            {"name": "v", "project_qualified_name": PROJECT_QN, "file_path": ""},
            "file_path cannot be blank",
        ),
        (
            LookerFolder.creator,
            {"name": "f", "connection_qualified_name": CONNECTION_QN, "folder_id": 6.5},
            "folder_id must be a whole number",
        ),
        (
            LookerFolder.creator,
            {
                "name": "f",
                "connection_qualified_name": CONNECTION_QN,
                "folder_id": "a/b",
            },
            "folder_id cannot contain '/'",
        ),
        (
            LookerFolder.creator,
            {
                "name": "f",
                "connection_qualified_name": CONNECTION_QN,
                "folder_id": 7,
                "parent_folder_qualified_name": "default/looker/other/folder/6",
            },
            "must be in connection",
        ),
        (
            LookerDashboard.creator,
            {
                "name": "d",
                "connection_qualified_name": CONNECTION_QN,
                "dashboard_id": None,
            },
            "dashboard_id is required",
        ),
        (
            LookerDashboard.creator,
            {
                "name": "d",
                "connection_qualified_name": CONNECTION_QN,
                "dashboard_id": 1,
                "folder_name": "Shared",
            },
            "folder_name requires folder_qualified_name",
        ),
        (
            LookerLook.creator,
            {"name": "l", "connection_qualified_name": CONNECTION_QN, "look_id": True},
            "look_id must be a string or a number",
        ),
        (
            LookerTile.creator,
            {"name": "t", "dashboard_qualified_name": LOOK_QN, "tile_id": 1},
            "Invalid dashboard_qualified_name",
        ),
        (
            LookerTile.creator,
            {
                "name": "t",
                "dashboard_qualified_name": DASHBOARD_QN,
                "tile_id": 1,
                "look_qualified_name": "default/looker/other/look/1",
            },
            "must be in connection",
        ),
        (LookerField.creator, {"name": "f"}, "Exactly one of"),
        (
            LookerField.creator,
            {
                "name": "f",
                "look_qualified_name": LOOK_QN,
                "tile_qualified_name": TILE_QN,
            },
            "Exactly one of",
        ),
        (
            LookerField.creator,
            {"name": "f", "dashboard_qualified_name": DASHBOARD_QN},
            "tile_id is required",
        ),
        (
            LookerField.creator,
            {"name": "f", "look_qualified_name": LOOK_QN, "tile_id": 1},
            "tile_id is only used",
        ),
        (
            LookerField.creator,
            {
                "name": "f",
                "look_qualified_name": LOOK_QN,
                "refinement_file_path": "a.lkml",
            },
            "refinement_file_path is only used",
        ),
        (
            LookerField.creator,
            {
                "name": "f",
                "view_qualified_name": VIEW_QN,
                "refinement_line_number": "1",
            },
            "refinement_line_number requires",
        ),
        (
            LookerField.creator,
            {"name": "f", "explore_qualified_name": f"{MODEL_QN}/other::order_items"},
            "model before '::'",
        ),
        (
            LookerField.creator,
            {"name": "f", "view_qualified_name": PROJECT_QN},
            "Invalid view_qualified_name",
        ),
    ],
)
def test_creator_rejects_invalid_inputs(creator, kwargs, message):
    with pytest.raises(ValueError, match=message):
        creator(**kwargs)


def test_create_alias():
    sut = LookerProject.create(name="ecom", connection_qualified_name=CONNECTION_QN)

    assert sut.qualified_name == PROJECT_QN
