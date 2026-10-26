# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanAlloydbPostgres, AtlanAlloydbPostgresInputs


def test_atlan_alloydb_postgres_inputs_defaults():
    i = AtlanAlloydbPostgresInputs()
    assert AtlanAlloydbPostgresInputs._APP_ID == "atlan-alloydb-postgres"
    assert AtlanAlloydbPostgresInputs._ENTRYPOINT == "alloydb-postgres"
    assert i.cloud_provider == ""
    assert i.exclude_filter == "{}"
    assert i.include_filter == "{}"
    assert i.temp_table_regex == ""
    assert i.redact_sql_text == "false"


def test_atlan_alloydb_postgres_builder_payload():
    out = (
        AtlanAlloydbPostgres(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "alloydb-postgres"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_alloydb_postgres_credential_basic():
    b = AtlanAlloydbPostgres(Mock()).basic(username="x", password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_alloydb_postgres_credential_iam_user():
    b = AtlanAlloydbPostgres(Mock()).iam_user(username="x", password="x", name="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_alloydb_postgres_credential_iam_service_account():
    b = AtlanAlloydbPostgres(Mock()).iam_service_account(
        username="x", password="x", name="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
