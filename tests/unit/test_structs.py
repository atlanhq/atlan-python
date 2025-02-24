# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

from json import load
from pathlib import Path

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import MCMonitor
from pyatlan.model.core import AssetResponse

TEST_DATA_DIR = Path(__file__).parent / "data"
MC_MONITOR_JSON = "mc_monitor.json"
STRUCT_RESPONSES_DIR = TEST_DATA_DIR / "struct_responses"


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")


@pytest.fixture()
def client():
    return AtlanClient()


def load_json(respones_dir, filename):
    with (respones_dir / filename).open() as input_file:
        return load(input_file)


def to_json(model):
    return model.json(by_alias=True, exclude_unset=True)


@pytest.fixture()
def mc_monitor_response_json():
    return load_json(STRUCT_RESPONSES_DIR, MC_MONITOR_JSON)


def test_structs_flatten_attributes(
    client, mock_custom_metadata_cache, mc_monitor_response_json
):
    asset_response = {"referredEntities": {}, "entity": mc_monitor_response_json}
    mc_monitor_model = MCMonitor(**mc_monitor_response_json)
    mc_monitor_asset_response = AssetResponse[MCMonitor](**asset_response).entity

    assert mc_monitor_model == mc_monitor_asset_response
    assert to_json(mc_monitor_model) == to_json(mc_monitor_asset_response)
