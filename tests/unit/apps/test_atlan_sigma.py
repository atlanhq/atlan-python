# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanSigma, AtlanSigmaInputs


def test_atlan_sigma_inputs_defaults():
    i = AtlanSigmaInputs()
    assert AtlanSigmaInputs._APP_ID == "atlan-sigma"
    assert AtlanSigmaInputs._ENTRYPOINT == ""
    assert i.include_filter == "{}"
    assert i.exclude_filter == "{}"


def test_atlan_sigma_builder_payload():
    out = (
        AtlanSigma(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "sigma"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"
    assert out["extraction_method"] == "direct"


def test_atlan_sigma_credential_api_token():
    b = AtlanSigma(Mock()).api_token(username="x", password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-sigma"
    out = (
        AtlanSigma(Mock())
        .api_token(username="x", password="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
