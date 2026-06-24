# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanMssql, AtlanMssqlInputs


def test_atlan_mssql_inputs_defaults():
    i = AtlanMssqlInputs()
    assert AtlanMssqlInputs._APP_ID == "atlan-mssql"
    assert AtlanMssqlInputs._ENTRYPOINT == ""
    assert i.agent_name == ""
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.temp_table_regex == ""


def test_atlan_mssql_builder_payload():
    out = (
        AtlanMssql(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "mssql"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
