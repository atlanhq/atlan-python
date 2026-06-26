# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import PostgresMiner, PostgresMinerInputs


def test_postgres_miner_inputs_defaults():
    i = PostgresMinerInputs()
    assert PostgresMinerInputs._APP_ID == "postgres-miner"
    assert PostgresMinerInputs._ENTRYPOINT == "miner"
    assert isinstance(i.to_inputs(), dict)


def test_postgres_miner_builder_payload():
    out = (
        PostgresMiner(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "postgres"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
