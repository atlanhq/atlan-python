# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import CsaUberAssetExportBasic, CsaUberAssetExportBasicInputs


def test_csa_uber_asset_export_basic_inputs_defaults():
    i = CsaUberAssetExportBasicInputs()
    assert CsaUberAssetExportBasicInputs._APP_ID == "csa-uber-asset-export-basic"
    assert CsaUberAssetExportBasicInputs._ENTRYPOINT == "asset-export-basic"
    assert i.delivery_type == "DIRECT"
    assert i.email_addresses == ""
    assert i.export_scope == "ENRICHED_ONLY"
    assert i.qn_prefix == "default"
    assert i.include_description is True
    assert i.include_glossaries is False
    assert i.include_products is False
    assert i.include_archived is False
    assert i.export_empty_custom_metadata == "true"


def test_csa_uber_asset_export_basic_builder_payload():
    out = (
        CsaUberAssetExportBasic(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert (
        out["connection"]["attributes"]["connectorName"] == "csa-connectors-objectstore"
    )
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["all_attributes"] is False


def test_csa_uber_asset_export_basic_credential_s3():
    b = CsaUberAssetExportBasic(Mock()).s3(username="x", password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_csa_uber_asset_export_basic_credential_gcs():
    b = CsaUberAssetExportBasic(Mock()).gcs(username="x", password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_csa_uber_asset_export_basic_credential_adls():
    b = CsaUberAssetExportBasic(Mock()).adls(username="x", password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
