# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanTableau, AtlanTableauInputs


def test_atlan_tableau_inputs_defaults():
    i = AtlanTableauInputs()
    assert AtlanTableauInputs._APP_ID == "atlan-tableau"
    assert AtlanTableauInputs._ENTRYPOINT == ""
    assert i.include_filter == {}
    assert i.exclude_filter == {}
    assert i.exclude_projects_regex == ""
    assert i.tableau_alternate_host == "https://alternate.tableau.com"
    assert i.crawl_unpublished_worksheets_dashboards is True
    assert i.crawl_hidden_datasource_fields is True
    assert i.crawl_embedded_dashboards is False
    assert i.incremental_enabled is False
    assert i.force_full_extraction is False


def test_atlan_tableau_builder_payload():
    out = (
        AtlanTableau(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "tableau"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_tableau_credential_basic():
    b = AtlanTableau(Mock()).basic(username="x", password="x", protocol="x", host="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_tableau_credential_personal_access_token():
    b = AtlanTableau(Mock()).personal_access_token(
        username="x", password="x", protocol="x", host="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_tableau_credential_jwt():
    b = AtlanTableau(Mock()).jwt(
        username="x",
        client_id="x",
        private_id="x",
        private_key="x",
        protocol="x",
        host="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
