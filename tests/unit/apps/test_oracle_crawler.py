# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import OracleCrawler, OracleCrawlerInputs


def test_oracle_crawler_inputs_defaults():
    i = OracleCrawlerInputs()
    assert OracleCrawlerInputs._APP_ID == "oracle-crawler"
    assert OracleCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.temp_table_regex == ""
    assert i.advanced_config_strategy == "default"


def test_oracle_crawler_builder_payload():
    out = (
        OracleCrawler(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "oracle"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["workflow_type"] == "extract-metadata"
    assert out["incremental_extraction"] == "false"
    assert out["system_schema_name"] == "SYS"


def test_oracle_crawler_credential_basic():
    b = OracleCrawler(Mock()).basic(
        username="x", password="x", sid="x", database_name="x"
    )
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-oracle"
    out = (
        OracleCrawler(Mock())
        .basic(username="x", password="x", sid="x", database_name="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
