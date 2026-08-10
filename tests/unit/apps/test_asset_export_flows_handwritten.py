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


def test_native_document_matches_ui_submission():
    """CSA uber apps submit via POST /package-workflows with the Argo-shaped
    native document — this pins the exact shape captured from a working UI
    submission on a live tenant (AICHAT-1588). The /v1/app inputs route 500s
    for these apps ("No manifest available")."""
    client = Mock()
    client.app.describe.side_effect = Exception("registry not readable")
    doc = (
        CsaUberAssetExportBasic(client)
        .export_via("DIRECT")
        .export_scope("GLOSSARIES_ONLY")
        .include_archived(False)
        ._native_document(name="sdk validation", epoch=1786351666)
    )

    assert doc["execution_mode"] == "native"
    md = doc["metadata"]
    assert md["name"] == "csa-uber-asset-export-basic-1786351666"
    assert md["entrypoint"] == "asset-export-basic"
    assert md["app_service_url"] == "http://csa-uber.csa-uber-app.svc.cluster.local"
    assert (
        md["annotations"]["package.argoproj.io/name"]
        == "@atlan/csa-uber-asset-export-basic"
    )
    assert md["annotations"]["orchestration.atlan.com/atlanName"] == "sdk validation"

    task = doc["spec"]["templates"][0]["dag"]["tasks"][0]
    assert task["templateRef"] == {
        "name": "csa-uber-asset-export-basic",
        "template": "main",
        "clusterScope": True,
    }
    params = {p["name"]: p["value"] for p in task["arguments"]["parameters"]}
    assert params["delivery-type"] == "DIRECT"
    assert params["export-scope"] == "GLOSSARIES_ONLY"
    assert params["all-attributes"] is False  # hidden default, kebab on the wire
    assert params["_internal_workflow_name"] == "sdk validation"


def test_native_create_posts_to_package_workflows():
    """run()/create() for CSA apps go through POST /package-workflows with
    submit reflecting run-vs-create — never the /v1/app inputs route."""
    client = Mock()
    client.app.describe.side_effect = Exception("registry not readable")
    client._call_api.return_value = {"data": {"name": "csa-uber-asset-export-basic-1", "slug": "csa-uber-asset-export-basic-1-XXXX"}}

    resp = (
        CsaUberAssetExportBasic(client)
        .export_via("DIRECT")
        .export_scope("GLOSSARIES_ONLY")
        .run(name="sdk validation")
    )

    client.app.create.assert_not_called()
    endpoint = client._call_api.call_args[0][0]
    assert "package-workflows" in endpoint.path
    assert client._call_api.call_args.kwargs["query_params"] == {"submit": "true"}
    body = client._call_api.call_args.kwargs["request_obj"]
    assert body["execution_mode"] == "native"
    assert resp.slug == "csa-uber-asset-export-basic-1-XXXX"
