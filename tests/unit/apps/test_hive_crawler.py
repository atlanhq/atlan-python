# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import HiveCrawler, HiveCrawlerInputs


def test_hive_crawler_inputs_defaults():
    i = HiveCrawlerInputs()
    assert HiveCrawlerInputs._APP_ID == "hive-crawler"
    assert HiveCrawlerInputs._ENTRYPOINT == "crawler"
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"
    assert i.advanced_config_strategy == "default"
    assert i.allow_partial_success is False


def test_hive_crawler_builder_payload():
    out = (
        HiveCrawler(Mock())
        .connection(name="conn", admin_users=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "hive"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_hive_crawler_credential_basic():
    b = HiveCrawler(Mock()).basic(username="x", password="x")
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_hive_crawler_credential_kerberos():
    b = HiveCrawler(Mock()).kerberos(
        principal="x",
        service_name="x",
        keytab_file="x",
        krb5_conf_file="x",
        kerberos_type="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
