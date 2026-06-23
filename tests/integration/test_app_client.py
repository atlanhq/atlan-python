# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Integration tests for the native (v3) App client (BLDX-1472).

Runs against a live tenant (creds from the environment, like the other
integration tests). Workflows are created with ``run=False`` + agent mode so no
crawl is triggered and no central credential is required; each created workflow
is deleted (archived) in teardown.
"""

from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.app import (
    AppInfo,
    AppInputContract,
    AppResponse,
)
from tests.integration.client import TestId

APP_ID = "bigquery-crawler"
ENTRYPOINT = "crawler"
MODULE_NAME = TestId.make_unique("AppClient")


@pytest.fixture(scope="module")
def created(client: AtlanClient) -> Generator[AppResponse, None, None]:
    """Create a workflow (no run), yield it, then archive it."""
    response = client.app.create(
        app_id=APP_ID,
        entrypoint=ENTRYPOINT,
        name=MODULE_NAME,
        inputs={
            "connection": {
                "typeName": "Connection",
                "attributes": {
                    "qualifiedName": f"default/bigquery/{MODULE_NAME}",
                    "connectorName": "bigquery",
                    "adminUsers": ["aryaman.bhushan"],
                },
            },
            # agent mode → routed to the agent; no central credential vaulted
            "agent_json": {
                "agent-name": "pyatlan-itest",
                "secret-manager": "vault",
                "secret-path": "kv/pyatlan-itest",
            },
            "include_filter": "{}",
            "exclude_filter": "{}",
        },
        run=False,
    )
    yield response
    # cleanup — archive the workflow regardless of test outcome
    if response and response.slug:
        try:
            client.app.delete(response.slug)
        except Exception:
            pass


def test_get_app(client: AtlanClient):
    info = client.app.get_app(APP_ID)
    assert isinstance(info, AppInfo)
    assert info.app_id == APP_ID
    assert info.native_ready is True
    assert ENTRYPOINT in {e.name for e in info.entrypoints}


def test_get_input_contract(client: AtlanClient):
    contract = client.app.get_input_contract(APP_ID, entrypoint=ENTRYPOINT)
    assert isinstance(contract, AppInputContract)
    assert contract.title == "AppInputContract"
    names = contract.field_names()
    assert "connection" in names
    # the contract should expose a credential-bearing field
    assert contract.credential_field() is not None


def test_create_returns_slug(created: AppResponse):
    assert created.slug and "appclient" in created.slug
    assert created.execution_mode == "native"
    assert created.version is not None
    # run=False → no run started
    assert created.run_id is None


def test_get_one(client: AtlanClient, created: AppResponse):
    fetched = client.app.get(created.slug)
    assert fetched.slug == created.slug
    assert fetched.name == MODULE_NAME


def test_list_is_paginated(client: AtlanClient, created: AppResponse):
    listing = client.app.get_all(limit=5)
    assert len(listing.workflows) <= 5
    # has_more + next_cursor pagination contract holds
    assert isinstance(listing.has_more, bool)


def test_update_publishes_new_version(client: AtlanClient, created: AppResponse):
    updated = client.app.update(
        created.slug,
        inputs={
            "connection": {
                "typeName": "Connection",
                "attributes": {
                    "qualifiedName": f"default/bigquery/{MODULE_NAME}",
                    "connectorName": "bigquery",
                    "adminUsers": ["aryaman.bhushan"],
                },
            },
            "agent_json": {
                "agent-name": "pyatlan-itest",
                "secret-manager": "vault",
                "secret-path": "kv/pyatlan-itest",
            },
            "include_filter": "{}",
            "exclude_filter": "{}",
        },
        entrypoint=ENTRYPOINT,
    )
    assert updated.slug == created.slug
    assert updated.version is not None


def test_schedule_add_and_remove(client: AtlanClient, created: AppResponse):
    schedule = client.app.add_schedule(
        created.slug, cron="0 9 * * *", timezone="Asia/Kolkata"
    )
    assert schedule.trigger_id
    removed = client.app.remove_schedule(created.slug, trigger_id=schedule.trigger_id)
    assert removed.deleted is True
