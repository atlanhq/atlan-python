# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import PostgresCrawler, PostgresCrawlerInputs


def test_postgres_crawler_inputs_defaults():
    i = PostgresCrawlerInputs()
    assert PostgresCrawlerInputs._APP_ID == "postgres-crawler"
    assert PostgresCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.temp_table_regex == ""
    assert i.advanced_config == "default"
    assert i.use_source_schema_filtering == "false"
    assert i.control_config_strategy == "default"
    assert i.control_config == "{}"


def test_postgres_crawler_builder_payload():
    out = (
        PostgresCrawler(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "postgres"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["use_jdbc_internal_methods"] == "true"


def test_postgres_crawler_credential_basic():
    b = PostgresCrawler(Mock()).basic(username="x", password="x", database="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_postgres_crawler_credential_iam_user():
    b = PostgresCrawler(Mock()).iam_user(
        username="x", password="x", username_2="x", aws_region="x", database="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_postgres_crawler_credential_iam_role():
    b = PostgresCrawler(Mock()).iam_role(
        username="x", aws_role_arn="x", aws_region="x", database="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
