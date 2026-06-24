# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanRedash, AtlanRedashInputs


def test_atlan_redash_inputs_defaults():
    i = AtlanRedashInputs()
    assert AtlanRedashInputs._APP_ID == "atlan-redash"
    assert AtlanRedashInputs._ENTRYPOINT == ""
    assert i.include_queries_tags == {}
    assert i.exclude_queries_tags == {}
    assert i.include_dashboards_tags == {}
    assert i.exclude_dashboards_tags == {}
    assert i.advanced_config_strategy == "default"
    assert i.include_unpublished_queries == "true"
    assert i.queries_without_tags == "true"
    assert i.dashboards_without_tags == "true"
    assert i.redash_alternate_host == ""


def test_atlan_redash_builder_payload():
    out = (
        AtlanRedash(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "redash"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["extraction_method"] == "direct"


def test_atlan_redash_credential_api_key():
    b = AtlanRedash(Mock()).api_key(password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-redash"
    out = AtlanRedash(Mock()).api_key(password="x").connection(name="c").preview()
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
