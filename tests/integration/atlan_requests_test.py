# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Live tests for client.requests (classic Metadata Inbox) and client.inbox
(governance-workflow approvals) — BLDX-1611.

The classic lifecycle is fully self-contained: it creates its own request
against a disposable term and verifies approval applies the change on the
backend. The inbox tests need a governance workflow to exist on the tenant
(the `Governance Workflows and Inbox` Labs feature), so they are gated on
ATLAN_TEST_WORKFLOW_GROUP_KEY.
"""
import os
import time
from typing import Generator

import pytest
from pydantic.v1 import StrictStr

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.assets import AtlasGlossary, AtlasGlossaryTerm
from pyatlan.model.atlan_request import AttributeRequest
from pyatlan.model.enums import AtlanRequestStatus, AtlanRequestType
from tests.integration.client import TestId, delete_asset

MODULE_NAME = TestId.make_unique("REQS")


@pytest.fixture(scope="module")
def glossary(client: AtlanClient) -> Generator[AtlasGlossary, None, None]:
    g = AtlasGlossary.create(name=StrictStr(MODULE_NAME))
    g = client.asset.save(g).assets_created(AtlasGlossary)[0]
    yield g
    delete_asset(client, guid=g.guid, asset_type=AtlasGlossary)


@pytest.fixture(scope="module")
def term(
    client: AtlanClient, glossary: AtlasGlossary
) -> Generator[AtlasGlossaryTerm, None, None]:
    t = AtlasGlossaryTerm.create(
        name=StrictStr(f"{MODULE_NAME}-term"), glossary_guid=glossary.guid
    )
    t = client.asset.save(t).assets_created(AtlasGlossaryTerm)[0]
    yield t
    delete_asset(client, guid=t.guid, asset_type=AtlasGlossaryTerm)


def _create_request(client: AtlanClient, term: AtlasGlossaryTerm, value: str):
    request = AttributeRequest.creator(
        destination_guid=term.guid,
        destination_qualified_name=term.qualified_name,
        destination_attribute="userDescription",
        destination_value=value,
        entity_type="AtlasGlossaryTerm",
    )
    created = client.requests.create(request)
    assert created and created.id
    assert created.status == AtlanRequestStatus.ACTIVE.value
    return created


def test_create_list_get_request(client: AtlanClient, term: AtlasGlossaryTerm):
    created = _create_request(client, term, "requests-test-listed")

    # typed filter finds it without knowing the JSON filter grammar
    response = client.requests.list(
        destination_guid=term.guid, status=AtlanRequestStatus.ACTIVE
    )
    found = [r for r in response.records or [] if r.id == created.id]
    assert found, "created request not returned by typed-filter list()"
    assert found[0].request_type == AtlanRequestType.ATTRIBUTE.value

    fetched = client.requests.get(guid=created.id)
    assert fetched and fetched.id == created.id


@pytest.mark.order(after="test_create_list_get_request")
def test_approve_applies_the_change(client: AtlanClient, term: AtlasGlossaryTerm):
    created = _create_request(client, term, "requests-test-approved")

    assert client.requests.approve(guid=created.id, message="integration approve")

    def _applied() -> bool:
        asset = client.asset.get_by_guid(term.guid, ignore_relationships=True)
        return asset.user_description == "requests-test-approved"

    deadline = time.time() + 30
    applied = False
    while time.time() < deadline:
        if _applied():
            applied = True
            break
        time.sleep(2)
    assert applied, "approved request did not apply the attribute change"


@pytest.mark.order(after="test_approve_applies_the_change")
def test_reject_does_not_apply(client: AtlanClient, term: AtlasGlossaryTerm):
    created = _create_request(client, term, "requests-test-rejected")

    assert client.requests.reject(guid=created.id, message="integration reject")
    time.sleep(3)
    asset = client.asset.get_by_guid(term.guid, ignore_relationships=True)
    assert asset.user_description != "requests-test-rejected", (
        "rejected request must not apply its change"
    )


@pytest.mark.skipif(
    not os.environ.get("ATLAN_TEST_WORKFLOW_GROUP_KEY"),
    reason=(
        "inbox bulk-action needs a tenant with the Governance Workflows Labs "
        "feature and a pending task group — set ATLAN_TEST_WORKFLOW_GROUP_KEY"
    ),
)
def test_inbox_bulk_action(client: AtlanClient):
    group_key = os.environ["ATLAN_TEST_WORKFLOW_GROUP_KEY"]
    response = client.inbox.reject_all(
        group_key=group_key, comment="integration bulk reject"
    )
    assert response.total_tasks is not None
    assert response.message
