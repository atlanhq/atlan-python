# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import TeradataCrawler, TeradataCrawlerInputs


def test_teradata_crawler_inputs_defaults():
    i = TeradataCrawlerInputs()
    assert TeradataCrawlerInputs._APP_ID == "teradata-crawler"
    assert TeradataCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.temp_table_regex == ""
    assert i.advanced_config_strategy == "default"
    assert i.use_source_schema_filtering == "false"


def test_teradata_crawler_builder_payload():
    out = (
        TeradataCrawler(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "teradata"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_teradata_crawler_credential_basic():
    b = TeradataCrawler(Mock()).basic(username="x", password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-teradata"
    out = (
        TeradataCrawler(Mock())
        .basic(username="x", password="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_teradata_crawler_credential_ldap():
    b = TeradataCrawler(Mock()).ldap(username="x", password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-teradata"
    out = (
        TeradataCrawler(Mock())
        .ldap(username="x", password="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
