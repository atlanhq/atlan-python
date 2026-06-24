# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import DatabricksCrawler, DatabricksCrawlerInputs


def test_databricks_crawler_inputs_defaults():
    i = DatabricksCrawlerInputs()
    assert DatabricksCrawlerInputs._APP_ID == "databricks-crawler"
    assert DatabricksCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.extract_strategy == "system-tables"
    assert i.enable_cross_workspace_discovery == "false"
    assert i.temp_table_regex == ""
    assert i.enable_tags == "false"
    assert i.enable_models == "false"
    assert i.enable_model_lineage == "false"
    assert i.enable_complex_types == "true"
    assert i.advanced_config_strategy == "default"
    assert i.enable_view_lineage == "true"
    assert i.use_source_schema_filtering == "false"
    assert i.incremental_extraction == "false"
    assert i.sql_warehouse == {}
    assert i.asset_selection == "{}"


def test_databricks_crawler_builder_payload():
    out = (
        DatabricksCrawler(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "databricks"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["workspace_credential_overrides"] == "{}"
    assert out["include_filter"] == "{}"
    assert out["exclude_filter"] == "{}"
    assert out["use_parallelize_table_enrichment"] == "true"
    assert out["enable_tag_sync"] == "false"


def test_databricks_crawler_credential_basic():
    b = DatabricksCrawler(Mock()).basic(password="x", http_path="x", host="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-databricks"
    out = (
        DatabricksCrawler(Mock())
        .basic(password="x", http_path="x", host="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_databricks_crawler_credential_aws_service():
    b = DatabricksCrawler(Mock()).aws_service(
        client_id="x", client_secret="x", host="x"
    )
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-databricks"
    out = (
        DatabricksCrawler(Mock())
        .aws_service(client_id="x", client_secret="x", host="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_databricks_crawler_credential_azure_service():
    b = DatabricksCrawler(Mock()).azure_service(
        client_id="x", client_secret="x", tenant_id="x", host="x"
    )
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-databricks"
    out = (
        DatabricksCrawler(Mock())
        .azure_service(client_id="x", client_secret="x", tenant_id="x", host="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
