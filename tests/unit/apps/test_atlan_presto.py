# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanPresto, AtlanPrestoInputs


def test_atlan_presto_inputs_defaults():
    i = AtlanPrestoInputs()
    assert AtlanPrestoInputs._APP_ID == "atlan-presto"
    assert AtlanPrestoInputs._ENTRYPOINT == ""
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"


def test_atlan_presto_builder_payload():
    out = (
        AtlanPresto(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "presto"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["extraction_method"] == "direct"


def test_atlan_presto_credential_basic():
    b = AtlanPresto(Mock()).basic(username="x", password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-presto"
    out = (
        AtlanPresto(Mock())
        .basic(username="x", password="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
