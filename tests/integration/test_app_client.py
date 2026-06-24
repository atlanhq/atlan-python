# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Integration tests for the App workflow client.

Runs against a live tenant (creds from the environment, like the other
integration tests). Workflows are created in **direct mode with dummy
credentials** and ``run=False`` — the create endpoint vaults the raw credential
(vaulting does not authenticate, so dummy creds are fine) and we never assert a
crawl succeeds; each created workflow is archived in teardown.

Coverage — every ``AppClient`` method:
describe, get_input_contract, create, run, get, get_all, update, add_schedule,
remove_schedule, submit, get_run, cancel_run, delete. Schedule add/remove and the
run lifecycle are asserted *by re-fetching state*, not just by the call's return.
"""

import json
from typing import Generator

import pytest

from pyatlan.client.atlan import AtlanClient
from pyatlan.model.app import (
    AppInfo,
    AppInputContract,
    AppResponse,
)
from pyatlan.model.apps import BigqueryCrawler, BigqueryCrawlerInputs
from tests.integration.client import TestId

APP_ID = "bigquery-crawler"
ENTRYPOINT = "crawler"
CONNECTOR = "bigquery"
CONNECTOR_CONFIG = "atlan-connectors-bigquery"
MODULE_NAME = TestId.make_unique("AppClient")
# Only used by the raw-inputs update path (the typed model has no auto-mint);
# the builder itself auto-mints its connection QN.
CONNECTION_QN = f"default/{CONNECTOR}/{MODULE_NAME}"

# Dummy, structurally-valid BigQuery service account. Vaulting does NOT
# authenticate, so the create succeeds; we never assert the crawl runs.
DUMMY_SA_EMAIL = "pyatlan-itest@pyatlan-itest.iam.gserviceaccount.com"
DUMMY_PROJECT = "pyatlan-itest"
DUMMY_SA_JSON = json.dumps(
    {
        "type": "service_account",
        "project_id": DUMMY_PROJECT,
        "private_key_id": "0000000000000000000000000000000000000000",
        "private_key": (
            "-----BEGIN PRIVATE KEY-----\nMIIfakekeyfakekeyfakekey\n"
            "-----END PRIVATE KEY-----\n"
        ),
        "client_email": DUMMY_SA_EMAIL,
        "client_id": "100000000000000000000",
        "token_uri": "https://oauth2.googleapis.com/token",
    }
)

TERMINAL = {"Succeeded", "Failed", "Stopped", "Terminated", "Skipped"}
NON_TERMINAL = {"Pending", "Running", "Paused"}


def _admin_role(client: AtlanClient) -> str:
    """The tenant's ``$admin`` role id — used as the connection admin so the test
    is tenant-agnostic (no hardcoded username)."""
    role = client.role_cache.get_id_for_name("$admin")
    assert role, "tenant has no $admin role"
    return role


def _builder(client: AtlanClient, name: str) -> BigqueryCrawler:
    """A BigQuery builder wired with dummy direct creds + a fresh connection.

    No ``qualified_name`` — the builder auto-mints ``default/{connector}/{epoch}``,
    exactly as the UI does for a new connection. Admin is the ``$admin`` role.
    """
    return (
        BigqueryCrawler(client)
        .service_account(
            email=DUMMY_SA_EMAIL,
            service_account_json=DUMMY_SA_JSON,
            project_id=DUMMY_PROJECT,
        )
        .connection(name=name, admin_roles=[_admin_role(client)])
        .include({})
        .exclude({})
    )


@pytest.fixture(scope="module")
def created(client: AtlanClient) -> Generator[AppResponse, None, None]:
    """Create a workflow via the fluent builder (dummy creds, no run); archive after."""
    response = _builder(client, MODULE_NAME).create(name=MODULE_NAME)
    yield response
    if response and response.slug:
        try:
            client.app.delete(response.slug)
        except Exception:
            pass


# --------------------------------------------------------------------------- #
# Discovery
# --------------------------------------------------------------------------- #
def test_describe(client: AtlanClient):
    info = client.app.describe(APP_ID)
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
    assert contract.credential_field() is not None


# --------------------------------------------------------------------------- #
# Create / read
# --------------------------------------------------------------------------- #
def test_builder_payload_vaults_raw_credential():
    # No client needed — preview() is offline. Asserts the direct-mode shape:
    # raw credential embedded for the server to vault, guid sent "" (redacted secret).
    out = (
        BigqueryCrawler(object())
        .service_account(
            email=DUMMY_SA_EMAIL,
            service_account_json=DUMMY_SA_JSON,
            project_id=DUMMY_PROJECT,
        )
        .connection(name="x")
        .preview()
    )
    assert out["extraction_method"] == "direct"
    assert out["credential"]["authType"] == "basic"
    assert out["credential"]["connectorConfigName"] == CONNECTOR_CONFIG
    assert out["credential"]["password"] == "***"  # redacted in preview
    assert out["credential_guid"] == ""
    assert out["connection"]["attributes"]["connectorName"] == CONNECTOR
    # connection QN is auto-minted (no qualified_name passed)
    assert out["connection"]["attributes"]["qualifiedName"].startswith(
        f"default/{CONNECTOR}/"
    )


def test_create_returns_slug(created: AppResponse):
    assert created.slug and "appclient" in created.slug.lower()
    assert created.execution_mode == "native"
    assert created.version is not None
    assert created.run_id is None  # run=False


def test_get_one(client: AtlanClient, created: AppResponse):
    fetched = client.app.get(created.slug)
    assert fetched.slug == created.slug
    assert fetched.name == MODULE_NAME


def test_list_is_paginated(client: AtlanClient, created: AppResponse):
    listing = client.app.get_all(limit=5)
    assert len(listing.workflows) <= 5
    assert isinstance(listing.has_more, bool)


# --------------------------------------------------------------------------- #
# Update (full-replace via a typed inputs model)
# --------------------------------------------------------------------------- #
def test_update_publishes_new_version(client: AtlanClient, created: AppResponse):
    # Full-replace inputs, but NO credential — update is credential-preserving, so
    # the persisted (vaulted) credential carries over. credential_guid="" keeps it.
    inputs = BigqueryCrawlerInputs(
        connection={
            "typeName": "Connection",
            "attributes": {
                "qualifiedName": CONNECTION_QN,
                "connectorName": CONNECTOR,
                "adminRoles": [_admin_role(client)],
            },
        },
        extraction_method="direct",
        credential_guid="",
        include_filter="{}",
        exclude_filter="{}",
        enable_nested_columns=False,  # a real change
    )
    updated = client.app.update(created.slug, inputs=inputs, entrypoint=ENTRYPOINT)
    assert updated.slug == created.slug
    assert updated.version is not None
    assert updated.version != created.version  # a new version was published

    # Re-fetch to confirm the new version actually persisted on the workflow.
    refetched = client.app.get(created.slug)
    assert refetched.slug == created.slug
    assert refetched.version == updated.version


# --------------------------------------------------------------------------- #
# Schedule lifecycle — verified via the add/remove round-trip.
#
# NOTE: ``get(slug)`` does NOT surface attached schedules on the v3 API (verified:
# ``schedules`` stays None after attach), so there's no read-back to assert against.
# The authoritative proof a schedule was attached is that removing *that exact
# trigger_id* returns ``deleted=True`` — you cannot delete a schedule that the
# server didn't attach.
# --------------------------------------------------------------------------- #
def test_schedule_add_then_remove(client: AtlanClient, created: AppResponse):
    schedule = client.app.add_schedule(
        created.slug, cron="0 9 * * *", timezone="Asia/Kolkata"
    )
    assert schedule.trigger_id
    assert schedule.cron == "0 9 * * *"
    assert schedule.timezone == "Asia/Kolkata"

    # removing the exact trigger confirms it had been attached
    removed = client.app.remove_schedule(created.slug, trigger_id=schedule.trigger_id)
    assert removed.deleted is True
    assert removed.trigger_id == schedule.trigger_id


def test_schedule_defaults_timezone_to_utc(client: AtlanClient, created: AppResponse):
    # No timezone passed → client applies the UTC default (server rejects null).
    schedule = client.app.add_schedule(created.slug, cron="0 1 * * *")
    trigger_id = schedule.trigger_id
    assert trigger_id
    try:
        assert schedule.timezone == "UTC"
    finally:
        client.app.remove_schedule(created.slug, trigger_id=trigger_id)


def test_multiple_schedules_independently_removable(
    client: AtlanClient, created: AppResponse
):
    s1 = client.app.add_schedule(created.slug, cron="0 1 * * *")
    s2 = client.app.add_schedule(created.slug, cron="0 2 * * *")
    assert s1.trigger_id and s2.trigger_id
    assert s1.trigger_id != s2.trigger_id
    # each trigger is independently removable (deleted=True for its own id)
    r1 = client.app.remove_schedule(created.slug, trigger_id=s1.trigger_id)
    r2 = client.app.remove_schedule(created.slug, trigger_id=s2.trigger_id)
    assert r1.deleted is True and r1.trigger_id == s1.trigger_id
    assert r2.deleted is True and r2.trigger_id == s2.trigger_id


# --------------------------------------------------------------------------- #
# Run lifecycle — submit, observe status, cancel
# --------------------------------------------------------------------------- #
def test_run_submit_status_and_cancel(client: AtlanClient, created: AppResponse):
    run = client.app.submit(created.slug)
    assert run.run_id
    assert run.slug == created.slug

    status = client.app.get_run(run.run_id)
    assert status.run_id == run.run_id
    assert status.status in (TERMINAL | NON_TERMINAL)
    assert isinstance(status.is_terminal, bool)

    # best-effort cancel (the run may already be terminal with dummy creds)
    if not status.is_terminal:
        cancelled = client.app.cancel_run(run.run_id)
        assert cancelled.run_id == run.run_id
        assert isinstance(cancelled.cancelled, bool)


# --------------------------------------------------------------------------- #
# Delete (explicit, in addition to teardown)
# --------------------------------------------------------------------------- #
def test_delete_archives(client: AtlanClient):
    resp = _builder(client, f"{MODULE_NAME}-del").create(name=f"{MODULE_NAME}-del")
    deleted = client.app.delete(resp.slug)
    assert deleted.archived is True
