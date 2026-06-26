# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import PowerbiMiner, PowerbiMinerInputs


def test_powerbi_miner_inputs_defaults():
    i = PowerbiMinerInputs()
    assert PowerbiMinerInputs._APP_ID == "powerbi-miner"
    assert PowerbiMinerInputs._ENTRYPOINT == "miner"
    assert i.advanced_config == "default"
    assert i.miner_start_timestamp == 0
    assert i.popularity_exclude_user_config == ""


def test_powerbi_miner_builder_payload():
    out = (
        PowerbiMiner(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "powerbi"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
