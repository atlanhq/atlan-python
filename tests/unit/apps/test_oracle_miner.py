# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import OracleMiner, OracleMinerInputs


def test_oracle_miner_inputs_defaults():
    i = OracleMinerInputs()
    assert OracleMinerInputs._APP_ID == "oracle-miner"
    assert OracleMinerInputs._ENTRYPOINT == "miner"
    assert i.miner_start_time_epoch == 0


def test_oracle_miner_builder_payload():
    out = (
        OracleMiner(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "oracle"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["workflow_type"] == "miner"
