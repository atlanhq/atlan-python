# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""HAND-WRITTEN flow tests for the v3 Asset Export builder (AICHAT-1588).

The generator's regen only clears files carrying the AUTO-GENERATED banner,
so this file survives regeneration; it asserts the customer-facing flows
stay stable across regens.
"""

from unittest.mock import Mock

from pyatlan.model.apps import CsaUberAssetExportBasic


def test_direct_download_flow_payload():
    """The DIRECT flow (the customer's sample run shape) assembles the same
    inputs the UI submits, with the hidden defaults riding along."""
    out = (
        CsaUberAssetExportBasic(Mock())
        .export_via("DIRECT")
        .export_scope("GLOSSARIES_ONLY")
        .include_archived(False)
        .preview()
    )
    assert out["delivery_type"] == "DIRECT"
    assert out["export_scope"] == "GLOSSARIES_ONLY"
    assert out["include_archived"] is False
    assert out["all_attributes"] is False  # hidden default the UI submits
    assert out["credential_guid"] == ""  # no object store for direct download


def test_gcs_cloud_delivery_stages_bucket_in_credential():
    """CLOUD delivery parity with the legacy gcs() builder: bucket rides in
    the vaulted credential's extra, project/service-account as user/pass."""
    b = (
        CsaUberAssetExportBasic(Mock())
        .export_via("CLOUD")
        .export_scope("ALL")
        .qualified_name_prefix_for_assets("default/bigquery/123")
        .gcs(username="my-project", password="{...svc json...}", gcs_bucket="exports")
    )
    out = b.preview()
    assert out["delivery_type"] == "CLOUD"
    assert out["qn_prefix"] == "default/bigquery/123"
    cred = out["credential"]
    assert cred["authType"] == "gcs"
    assert cred["connectorConfigName"] == "csa-connectors-objectstore"
    assert cred["extra"] == {"gcs_bucket": "exports"}
    assert cred["password"] == "***"  # preview never exposes the secret


def test_email_delivery_flow_payload():
    out = (
        CsaUberAssetExportBasic(Mock())
        .export_via("EMAIL")
        .recipient_email_addresses("a@example.com,b@example.com")
        .export_scope("PRODUCTS_ONLY")
        .preview()
    )
    assert out["delivery_type"] == "EMAIL"
    assert out["email_addresses"] == "a@example.com,b@example.com"
    assert out["export_scope"] == "PRODUCTS_ONLY"
