# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanAthena, AtlanAthenaInputs


def test_atlan_athena_inputs_defaults():
    i = AtlanAthenaInputs()
    assert AtlanAthenaInputs._APP_ID == "atlan-athena"
    assert AtlanAthenaInputs._ENTRYPOINT == ""
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.temp_table_regex == ""
    assert i.advanced_config == "default"
    assert i.use_source_schema_filtering == "false"


def test_atlan_athena_builder_payload():
    out = (
        AtlanAthena(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "athena"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["extraction_method"] == "direct"
    assert out["use_jdbc_internal_methods"] == "true"
    assert out["fetch_partitions"] == "false"


def test_atlan_athena_credential_basic():
    b = AtlanAthena(Mock()).basic(
        username="x", password="x", s3_output_location="x", host="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_athena_credential_role():
    b = AtlanAthena(Mock()).role(s3_output_location="x", host="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
