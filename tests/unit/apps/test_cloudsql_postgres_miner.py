# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import CloudsqlPostgresMiner, CloudsqlPostgresMinerInputs


def test_cloudsql_postgres_miner_inputs_defaults():
    i = CloudsqlPostgresMinerInputs()
    assert CloudsqlPostgresMinerInputs._APP_ID == "cloudsql-postgres-miner"
    assert CloudsqlPostgresMinerInputs._ENTRYPOINT == "miner"
    assert i.redact_sql_text == "false"


def test_cloudsql_postgres_miner_builder_payload():
    out = (
        CloudsqlPostgresMiner(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "cloudsql-postgres"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "query_history"
