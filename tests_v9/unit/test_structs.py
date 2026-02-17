# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Atlan Pte. Ltd.

"""Unit tests for pyatlan_v9 struct and Atlas conversion behavior."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from pyatlan_v9.model import MCMonitor
from pyatlan_v9.model.transform import from_atlas_format, from_atlas_json

TEST_DATA_DIR = Path(__file__).parents[2] / "tests" / "unit" / "data"
MC_MONITOR_JSON = "mc_monitor.json"
STRUCT_RESPONSES_DIR = TEST_DATA_DIR / "struct_responses"


def load_json(responses_dir: Path, filename: str):
    """Load JSON fixture from disk."""
    with (responses_dir / filename).open() as input_file:
        return json.load(input_file)


@pytest.fixture()
def mc_monitor_response_json():
    """Load legacy MCMonitor fixture JSON."""
    return load_json(STRUCT_RESPONSES_DIR, MC_MONITOR_JSON)


def test_structs_flatten_attributes(mc_monitor_response_json):
    """Ensure Atlas nested payloads flatten consistently through both decode paths."""
    asset_response = {"referredEntities": {}, "entity": mc_monitor_response_json}

    mc_monitor_from_dict = from_atlas_format(mc_monitor_response_json)
    mc_monitor_from_enveloped_json = from_atlas_json(
        json.dumps(asset_response).encode()
    )

    assert isinstance(mc_monitor_from_dict, MCMonitor)
    assert isinstance(mc_monitor_from_enveloped_json, MCMonitor)
    assert mc_monitor_from_dict == mc_monitor_from_enveloped_json
