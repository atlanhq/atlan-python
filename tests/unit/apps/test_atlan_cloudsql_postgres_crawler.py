# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import (
    AtlanCloudsqlPostgresCrawler,
    AtlanCloudsqlPostgresCrawlerInputs,
)


def test_atlan_cloudsql_postgres_crawler_inputs_defaults():
    i = AtlanCloudsqlPostgresCrawlerInputs()
    assert AtlanCloudsqlPostgresCrawlerInputs._APP_ID == "atlan-cloudsql-postgres"
    assert AtlanCloudsqlPostgresCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.cloud_provider == ""
    assert i.temp_table_regex == ""
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.redact_sql_text == "false"


def test_atlan_cloudsql_postgres_crawler_builder_payload():
    out = (
        AtlanCloudsqlPostgresCrawler(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "cloudsql-postgres"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_cloudsql_postgres_crawler_credential_basic():
    b = AtlanCloudsqlPostgresCrawler(Mock()).basic(username="x", password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_cloudsql_postgres_crawler_credential_iam_user():
    b = AtlanCloudsqlPostgresCrawler(Mock()).iam_user(
        username="x", password="x", name="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_cloudsql_postgres_crawler_credential_iam_service_account():
    b = AtlanCloudsqlPostgresCrawler(Mock()).iam_service_account(
        username="x", password="x", name="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_cloudsql_postgres_crawler_credential_workload_identity_federation():
    b = AtlanCloudsqlPostgresCrawler(Mock()).workload_identity_federation(
        username="x", name="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
