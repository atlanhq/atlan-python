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
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-trino"
    out = (
        AtlanTrino(Mock())
        .basic(
            username="x",
            password="x",
            enable_tls_https="x",
            disable_ssl_verification="x",
            host="x",
        )
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_atlan_trino_credential_jwt():
    b = AtlanTrino(Mock()).jwt(
        jwt_token="x", enable_tls_https="x", disable_ssl_verification="x", host="x"
    )
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-trino"
    out = (
        AtlanTrino(Mock())
        .jwt(
            jwt_token="x", enable_tls_https="x", disable_ssl_verification="x", host="x"
        )
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
