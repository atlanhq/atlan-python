# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanStandardLineage, AtlanStandardLineageInputs


def test_atlan_standard_lineage_inputs_defaults():
    i = AtlanStandardLineageInputs()
    assert AtlanStandardLineageInputs._APP_ID == "atlan-standard-lineage"
    assert AtlanStandardLineageInputs._ENTRYPOINT == "standard-lineage"
    assert i.connector == "bigquery"
    assert i.cross_connection_qualified_names == ""


def test_atlan_standard_lineage_builder_payload():
    out = (
        AtlanStandardLineage(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "standard-lineage"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["run_role"] == "standard-lineage"
