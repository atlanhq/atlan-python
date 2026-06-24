# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import Anaplan, AnaplanInputs


def test_anaplan_inputs_defaults():
    i = AnaplanInputs()
    assert AnaplanInputs._APP_ID == "anaplan-anaplan"
    assert AnaplanInputs._ENTRYPOINT == "anaplan"
    assert i.include_metadata == {}
    assert i.exclude_metadata == {}
    assert i.exclude_empty_modules is False
    assert i.ingest_system_dimension == "individual"


def test_anaplan_builder_payload():
    out = (
        Anaplan(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "anaplan"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_anaplan_credential_basic():
    b = Anaplan(Mock()).basic(username="x", password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-anaplan"
    out = (
        Anaplan(Mock()).basic(username="x", password="x").connection(name="c").preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_anaplan_credential_ca_cert():
    b = Anaplan(Mock()).ca_cert(username="x", password="x", ca_certificate="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-anaplan"
    out = (
        Anaplan(Mock())
        .ca_cert(username="x", password="x", ca_certificate="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
