# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import PowerbiCrawler, PowerbiCrawlerInputs


def test_powerbi_crawler_inputs_defaults():
    i = PowerbiCrawlerInputs()
    assert PowerbiCrawlerInputs._APP_ID == "powerbi-crawler"
    assert PowerbiCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.dashboard_report_include_regex == ""
    assert i.dashboard_report_exclude_regex == ""
    assert i.fetch_report_definition_extracts is True
    assert i.endorsement_attach_mode == "metastore"
    assert i.incremental_extraction is False
    assert i.sql_connection_info_note == ""
    assert i.enable_odbc_connectivity_mapping == "false"
    assert i.odbc_dsn_config_mapping == "{}"


def test_powerbi_crawler_builder_payload():
    out = (
        PowerbiCrawler(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "powerbi"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_powerbi_crawler_credential_service_principal():
    b = PowerbiCrawler(Mock()).service_principal(
        tenant_id="x",
        client_id="x",
        client_secret="x",
        admin_api="x",
        admin_api_summary="x",
    )
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-powerbi"
    out = (
        PowerbiCrawler(Mock())
        .service_principal(
            tenant_id="x",
            client_id="x",
            client_secret="x",
            admin_api="x",
            admin_api_summary="x",
        )
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_powerbi_crawler_credential_basic():
    b = PowerbiCrawler(Mock()).basic(
        username="x", password="x", tenant_id="x", client_id="x", client_secret="x"
    )
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-powerbi"
    out = (
        PowerbiCrawler(Mock())
        .basic(
            username="x", password="x", tenant_id="x", client_id="x", client_secret="x"
        )
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
