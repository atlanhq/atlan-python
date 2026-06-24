# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
# AUTO-GENERATED from the app's UI configmaps — DO NOT EDIT.
# Regenerate: uv run python -m pyatlan.generator.generate_apps
from unittest.mock import Mock

from pyatlan.model.apps import AtlanAzureEventHub, AtlanAzureEventHubInputs


def test_atlan_azure_event_hub_inputs_defaults():
    i = AtlanAzureEventHubInputs()
    assert AtlanAzureEventHubInputs._APP_ID == "atlan-azure-event-hub"
    assert AtlanAzureEventHubInputs._ENTRYPOINT == ""
    assert i.metadata_type == "kafkaandeventhub"
    assert i.skip_internal_topics == "true"
    assert i.exclude_filter == ""
    assert i.include_filter == ""


def test_atlan_azure_event_hub_builder_payload():
    out = (
        AtlanAzureEventHub(Mock())
        .connection(name="conn", admins=["u"])
        .credential_guid("g")
        .preview()
    )
    assert out["connection"]["attributes"]["connectorName"] == "azure-event-hub"
    assert out["credential_guid"] == "g"
    assert out["extraction_method"] == "direct"


def test_atlan_azure_event_hub_credential_basic():
    b = AtlanAzureEventHub(Mock()).basic(username="x", password="x")
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-azure-event-hub"
    out = (
        AtlanAzureEventHub(Mock())
        .basic(username="x", password="x")
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""


def test_atlan_azure_event_hub_credential_service_principal():
    b = AtlanAzureEventHub(Mock()).service_principal(
        username="x", password="x", client_id="x", client_secret="x", tenant_id="x"
    )
    cred = b._credential
    assert cred is not None
    assert cred.connector_config_name == "atlan-connectors-azure-event-hub"
    out = (
        AtlanAzureEventHub(Mock())
        .service_principal(
            username="x", password="x", client_id="x", client_secret="x", tenant_id="x"
        )
        .connection(name="c")
        .preview()
    )
    assert out["credential"]["authType"]
    assert out["credential_guid"] == ""
