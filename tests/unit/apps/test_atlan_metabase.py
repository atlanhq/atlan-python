# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanMetabase, AtlanMetabaseInputs


def test_atlan_metabase_inputs_defaults():
    i = AtlanMetabaseInputs()
    assert AtlanMetabaseInputs._APP_ID == "atlan-metabase"
    assert AtlanMetabaseInputs._ENTRYPOINT == ""
    assert i.include_collections == {}
    assert i.exclude_collections == {}


def test_atlan_metabase_builder_payload():
    out = (
        AtlanMetabase(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "metabase"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_metabase_credential_basic():
    b = AtlanMetabase(Mock()).basic(username="x", password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-metabase"
    out = (
        AtlanMetabase(Mock())
        .basic(username="x", password="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
