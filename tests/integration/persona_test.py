# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
import time
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossary, AuthPolicy, Connection, Persona
from pyatlan.model.enums import (
    AssetSidebarTab,
    AtlanConnectorType,
    AuthPolicyType,
    DataAction,
    PersonaGlossaryAction,
    PersonaMetadataAction,
)
from tests.integration.client import TestId, delete_asset
from tests.integration.connection_test import create_connection
from tests.integration.glossary_test import create_glossary

MODULE_NAME = TestId.make_unique("Persona")

CONNECTOR_TYPE = AtlanConnectorType.GCS


@pytest.fixture(scope="module")
def connection(client: AtlanClient) -> Generator[Connection, None, None]:
    result = create_connection(
        client=client, name=MODULE_NAME, connector_type=CONNECTOR_TYPE
    )
    yield result
    # TODO: proper connection delete workflow
    delete_asset(client, guid=result.guid, asset_type=Connection)


@pytest.fixture(scope="module")
def glossary(
    client: AtlanClient,
) -> Generator[AtlasGlossary, None, None]:
    g = create_glossary(client, name=MODULE_NAME)
    yield g
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


@pytest.fixture(scope="module")
def persona(
    client: AtlanClient,
    connection: Connection,
    glossary: AtlasGlossary,
) -> Generator[Persona, None, None]:
    to_create = Persona.create(name=MODULE_NAME)
    response = client.asset.save(to_create)
    p = response.assets_created(asset_type=Persona)[0]
    yield p
    delete_asset(client, guid=p.guid, asset_type=Persona)


def test_persona(
    client: AtlanClient,
    persona: Persona,
    connection: Connection,
    glossary: AtlasGlossary,
):
    assert persona
    assert persona.guid
    assert persona.qualified_name
    assert persona.name == MODULE_NAME
    assert persona.display_name == MODULE_NAME
    assert persona.qualified_name != MODULE_NAME


@pytest.mark.order(after="test_persona")
def test_update_persona(
    client: AtlanClient,
    persona: Persona,
    connection: Connection,
    glossary: AtlasGlossary,
):
    assert persona.qualified_name
    assert persona.name
    to_update = Persona.create_for_modification(
        persona.qualified_name, persona.name, True
    )
    to_update.description = "Now with a description!"
    to_update.deny_asset_tabs = {
        AssetSidebarTab.LINEAGE.value,
        AssetSidebarTab.RELATIONS.value,
        AssetSidebarTab.QUERIES.value,
    }
    response = client.asset.save(to_update)
    assert response
    updated = response.assets_updated(asset_type=Persona)
    assert updated
    assert len(updated) == 1
    assert updated[0]
    assert updated[0].guid == persona.guid
    assert updated[0].description == "Now with a description!"
    assert updated[0].deny_asset_tabs
    assert len(updated[0].deny_asset_tabs) == 3


@pytest.mark.order(after="test_update_persona")
def test_find_persona_by_name(
    client: AtlanClient,
    persona: Persona,
    connection: Connection,
    glossary: AtlasGlossary,
):
    result = client.asset.find_personas_by_name(MODULE_NAME)
    count = 0
    # TODO: replace with exponential back-off and jitter
    while not result and count < 10:
        time.sleep(2)
        result = client.asset.find_personas_by_name(MODULE_NAME)
        count += 1
    assert result
    assert len(result) == 1
    assert result[0].guid == persona.guid


@pytest.mark.order(after="test_find_persona_by_name")
def test_add_policies_to_persona(
    client: AtlanClient,
    persona: Persona,
    connection: Connection,
    glossary: AtlasGlossary,
):
    assert connection.qualified_name
    metadata = Persona.create_metadata_policy(
        name="Simple read access",
        persona_id=persona.guid,
        policy_type=AuthPolicyType.ALLOW,
        actions={PersonaMetadataAction.READ},
        connection_qualified_name=connection.qualified_name,
        resources={f"entity:{connection.qualified_name}"},
    )
    assert connection.qualified_name
    data = Persona.create_data_policy(
        name="Allow access to data",
        persona_id=persona.guid,
        policy_type=AuthPolicyType.ALLOW,
        connection_qualified_name=connection.qualified_name,
        resources={f"entity:{connection.qualified_name}"},
    )
    glossary_policy = Persona.create_glossary_policy(
        name="All glossaries",
        persona_id=persona.guid,
        policy_type=AuthPolicyType.ALLOW,
        actions={PersonaGlossaryAction.CREATE, PersonaGlossaryAction.UPDATE},
        resources={f"entity:{glossary.qualified_name}"},
    )
    response = client.asset.save([metadata, data, glossary_policy])
    assert response
    personas = response.assets_updated(asset_type=Persona)
    assert personas
    assert len(personas) == 1
    assert personas[0].guid == persona.guid
    policies = response.assets_created(asset_type=AuthPolicy)
    assert policies
    assert len(policies) == 3


@pytest.mark.order(after="test_add_policies_to_persona")
def test_retrieve_persona(
    client: AtlanClient,
    persona: Persona,
    connection: Connection,
    glossary: AtlasGlossary,
):
    assert persona.qualified_name
    one = client.asset.get_by_qualified_name(
        qualified_name=persona.qualified_name, asset_type=Persona
    )
    assert one
    assert one.guid == persona.guid
    assert one.description == "Now with a description!"
    denied = one.deny_asset_tabs
    assert denied
    assert len(denied) == 3
    assert AssetSidebarTab.LINEAGE.value in denied
    assert AssetSidebarTab.RELATIONS.value in denied
    assert AssetSidebarTab.QUERIES.value in denied
    policies = one.policies
    assert policies
    assert len(policies) == 3
    for policy in policies:
        # Need to retrieve the full policy if we want to see any info about it
        # (what comes back on the Persona itself are just policy references)
        full = client.asset.get_by_guid(guid=policy.guid, asset_type=AuthPolicy)
        assert full
        sub_cat = full.policy_sub_category
        assert sub_cat
        assert sub_cat in ["metadata", "data", "glossary"]
        assert full.policy_type == AuthPolicyType.ALLOW
        if sub_cat == "metadata":
            assert full.policy_actions
            assert len(full.policy_actions) == 1
            assert PersonaMetadataAction.READ in full.policy_actions
            assert full.policy_resources
            assert f"entity:{connection.qualified_name}" in full.policy_resources
        elif sub_cat == "data":
            assert full.policy_actions
            assert len(full.policy_actions) == 1
            assert DataAction.SELECT in full.policy_actions
            assert full.policy_resources
            assert f"entity:{connection.qualified_name}" in full.policy_resources
        elif sub_cat == "glossary":
            assert full.policy_actions
            assert len(full.policy_actions) == 2
            assert PersonaGlossaryAction.CREATE in full.policy_actions
            assert PersonaGlossaryAction.UPDATE in full.policy_actions
            assert full.policy_resources
            assert f"entity:{glossary.qualified_name}" in full.policy_resources
