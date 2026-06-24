# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanKnowledgeCatalog, AtlanKnowledgeCatalogInputs


def test_atlan_knowledge_catalog_inputs_defaults():
    i = AtlanKnowledgeCatalogInputs()
    assert AtlanKnowledgeCatalogInputs._APP_ID == "atlan-knowledge-catalog"
    assert AtlanKnowledgeCatalogInputs._ENTRYPOINT == ""
    assert i.include_projects == {}
    assert i.exclude_projects == {}
    assert i.include_aspect_types == {}
    assert i.exclude_aspect_types == {}
    assert i.ingest_aspects == "no"
    assert i.ingest_dq == "no"
    assert i.ingest_profiling == "no"
    assert i.preflight_check == ""


def test_atlan_knowledge_catalog_builder_payload():
    out = (
        AtlanKnowledgeCatalog(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "dataplex"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["enable_aspects_reverse_sync"] == "no"
    assert out["extraction_method"] == "direct"


def test_atlan_knowledge_catalog_credential_basic():
    b = AtlanKnowledgeCatalog(Mock()).basic(service_account_json="x", project_id="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-dataplex"
    out = (
        AtlanKnowledgeCatalog(Mock())
        .basic(service_account_json="x", project_id="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_atlan_knowledge_catalog_credential_gcp_wif():
    b = AtlanKnowledgeCatalog(Mock()).gcp_wif(
        service_account_email="x",
        wif_pool_provider_id="x",
        atlan_oauth_id="x",
        atlan_oauth_secret="x",
        project_id="x",
    )
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-dataplex"
    out = (
        AtlanKnowledgeCatalog(Mock())
        .gcp_wif(
            service_account_email="x",
            wif_pool_provider_id="x",
            atlan_oauth_id="x",
            atlan_oauth_secret="x",
            project_id="x",
        )
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
