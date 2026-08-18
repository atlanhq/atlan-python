# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# Hand-written: bigquery_crawler is a hand-authored builder (see generate_apps
# _HAND_WRITTEN), so this test is preserved across regeneration.
from unittest.mock import Mock

import pytest

from pyatlan.model.apps import BigqueryCrawler, BigqueryCrawlerInputs

WIF = dict(
    project_id="my-project",
    service_account_email="svc@my-project.iam.gserviceaccount.com",
    wif_pool_provider_id="projects/1/locations/global/workloadIdentityPools/p/providers/pr",
    atlan_oauth_id="oauth-client-id",
    atlan_oauth_secret="oauth-secret",
)


def test_bigquery_crawler_inputs_defaults():
    i = BigqueryCrawlerInputs()
    assert BigqueryCrawlerInputs._APP_ID == "bigquery-crawler"
    assert BigqueryCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.enable_nested_columns is True
    assert i.filter_sharded_tables is True


def test_bigquery_crawler_builder_payload():
    out = (
        BigqueryCrawler(Mock())
        .service_account(
            email="svc@my-project.iam.gserviceaccount.com",
            service_account_json="{}",
            project_id="my-project",
        )
        .connection(name="conn", admin_users=["u"])
        .include({"my-project": ["analytics"]})
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "bigquery"
    assert out["extraction_method"] == "direct"
    assert out["include_filter"] == '{"^my-project$": ["^analytics$"]}'


def test_wif_stages_gcp_wif_credential_with_the_five_typed_keys():
    b = BigqueryCrawler(Mock()).workload_identity_federation(**WIF)
    cred = b._raw_creds["credential_guid"]
    assert cred.auth_type == "gcp-wif"
    assert cred.connector_config_name == "atlan-connectors-bigquery"
    # WIF carries no username/password — auth is the token exchange.
    assert cred.username is None and cred.password is None
    assert cred.extras == {
        "project_id": "my-project",
        "connect_type": "public",
        "service_account_email": "svc@my-project.iam.gserviceaccount.com",
        "wif_pool_provider_id": "projects/1/locations/global/workloadIdentityPools/p/providers/pr",
        "atlan_oauth_id": "oauth-client-id",
        "atlan_oauth_secret": "oauth-secret",
    }


def test_wif_keys_land_in_the_previewed_credential_payload():
    out = (
        BigqueryCrawler(Mock())
        .workload_identity_federation(**WIF)
        .connection(name="conn")
        .preview()
    )
    cred = out["credential"]
    assert cred["authType"] == "gcp-wif"
    assert set(cred["extra"]) == {
        "project_id",
        "connect_type",
        "service_account_email",
        "wif_pool_provider_id",
        "atlan_oauth_id",
        "atlan_oauth_secret",
    }


def test_wif_requires_every_credential_field():
    # Each WIF field is required; a missing one is a TypeError, not a silently
    # incomplete credential. A misspelled required field trips the same check.
    with pytest.raises(TypeError):
        BigqueryCrawler(Mock()).workload_identity_federation(project_id="p")


def test_wif_forwards_unknown_extra_keys():
    # Forward-compatible: keys newer than this signature ride through **extra.
    b = BigqueryCrawler(Mock()).workload_identity_federation(**WIF, future_flag="x")
    assert b._raw_creds["credential_guid"].extras["future_flag"] == "x"
