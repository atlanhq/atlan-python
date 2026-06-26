# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import SnowflakeCrawler, SnowflakeCrawlerInputs


def test_snowflake_crawler_inputs_defaults():
    i = SnowflakeCrawlerInputs()
    assert SnowflakeCrawlerInputs._APP_ID == "snowflake-crawler"
    assert SnowflakeCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.extract_strategy == "information-schema"
    assert i.account_usage_database_name == "SNOWFLAKE"
    assert i.account_usage_schema_name == "ACCOUNT_USAGE"
    assert i.temp_table_regex == ""
    assert i.exclude_empty_tables is False
    assert i.exclude_views is False
    assert i.enable_lineage is True
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.asset_selection == "{}"
    assert i.preflight_check == ""
    assert i.enable_snowflake_tags is False
    assert i.enable_stages is False
    assert i.incremental_extraction is True
    assert i.control_config_strategy == "default"
    assert i.control_config == ""
    assert i.enable_semantic_views is False


def test_snowflake_crawler_builder_payload():
    out = (
        SnowflakeCrawler(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "snowflake"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_snowflake_crawler_credential_keypair():
    b = SnowflakeCrawler(Mock()).keypair(username="x", password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_snowflake_crawler_credential_okta():
    b = SnowflakeCrawler(Mock()).okta(username="x", password="x", authenticator="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_snowflake_crawler_credential_entra_id():
    b = SnowflakeCrawler(Mock()).entra_id(
        username="x", password="x", tenant_id="x", oauth_scope="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_snowflake_crawler_credential_basic():
    b = SnowflakeCrawler(Mock()).basic(username="x", password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
