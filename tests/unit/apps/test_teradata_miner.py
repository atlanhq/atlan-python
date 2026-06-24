# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import TeradataMiner, TeradataMinerInputs


def test_teradata_miner_inputs_defaults():
    i = TeradataMinerInputs()
    assert TeradataMinerInputs._APP_ID == "teradata-miner"
    assert TeradataMinerInputs._ENTRYPOINT == "miner"
    assert i.miner_start_time_epoch == 0
    assert i.advanced_config == "default"
    assert i.cross_connection == "false"
    assert i.control_config_strategy == "default"
    assert i.control_config == ""


def test_teradata_miner_builder_payload():
    out = (
        TeradataMiner(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "teradata"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
