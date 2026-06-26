# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanDbt, AtlanDbtInputs


def test_atlan_dbt_inputs_defaults():
    i = AtlanDbtInputs()
    assert AtlanDbtInputs._APP_ID == "atlan-dbt"
    assert AtlanDbtInputs._ENTRYPOINT == ""
    assert i.extraction_type == "api"
    assert i.manifest_source == "atlan"
    assert i.core_extract_output_prefix == ""
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.include_filter_core == "*"
    assert i.exclude_filter_core == "*"
    assert i.enable_dbt_tagsync is False
    assert i.advanced_options_config is False
    assert i.enrich_materialised_sql_assets is True


def test_atlan_dbt_builder_payload():
    out = (
        AtlanDbt(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "dbt"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["extraction_method"] == "direct"


def test_atlan_dbt_credential_api():
    b = AtlanDbt(Mock()).api(password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_dbt_credential_aws():
    b = AtlanDbt(Mock()).aws(bucket="x", prefix="x", region="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_dbt_credential_gcp():
    b = AtlanDbt(Mock()).gcp(
        project_id="x", service_account_json="x", bucket="x", prefix="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_dbt_credential_azure():
    b = AtlanDbt(Mock()).azure(
        tenant_id="x",
        client_id="x",
        client_secret="x",
        account_name="x",
        bucket="x",
        prefix="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
