# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanGlue, AtlanGlueInputs


def test_atlan_glue_inputs_defaults():
    i = AtlanGlueInputs()
    assert AtlanGlueInputs._APP_ID == "atlan-glue"
    assert AtlanGlueInputs._ENTRYPOINT == ""
    assert i.catalog_id == "AwsDataCatalog"
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.exclude_table_regex == ""


def test_atlan_glue_builder_payload():
    out = (
        AtlanGlue(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "glue"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_glue_credential_iam():
    b = AtlanGlue(Mock()).iam(username="x", password="x", region="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_glue_credential_role():
    b = AtlanGlue(Mock()).role(region="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
