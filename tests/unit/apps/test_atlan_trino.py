# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanTrino, AtlanTrinoInputs


def test_atlan_trino_inputs_defaults():
    i = AtlanTrinoInputs()
    assert AtlanTrinoInputs._APP_ID == "atlan-trino"
    assert AtlanTrinoInputs._ENTRYPOINT == ""
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"


def test_atlan_trino_builder_payload():
    out = (
        AtlanTrino(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "trino"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_trino_credential_basic():
    b = AtlanTrino(Mock()).basic(
        username="x",
        password="x",
        enable_tls_https="x",
        disable_ssl_verification="x",
        host="x",
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name


def test_atlan_trino_credential_jwt():
    b = AtlanTrino(Mock()).jwt(
        jwt_token="x", enable_tls_https="x", disable_ssl_verification="x", host="x"
    )
    assert b._raw_creds  # a credential was staged
    cred = next(iter(b._raw_creds.values()))
    assert cred.auth_type and cred.connector_config_name
