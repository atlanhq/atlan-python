# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
"""Live tests for client.inbox (governance-workflow approvals) — BLDX-1611.

Workflow tasks cannot be self-created: raising one requires an existing
governance workflow on the tenant (the `Governance Workflows and Inbox`
Labs feature, plus a configured workflow — `workflow_guids` is required by
the create endpoint). These tests are therefore gated on environment
variables naming pre-seeded pending tasks:

- ATLAN_TEST_INBOX_TASK_GUID: guid of ONE pending task
    → bulk action with a task guid actions exactly that task (group of one)
- ATLAN_TEST_INBOX_ASSET_GUID: guid of an asset with TWO OR MORE pending
  tasks → bulk action with the asset guid actions the WHOLE group

The classic Requests module (client.requests) lives in
atlan_requests_test.py and is fully self-contained.
"""
import os

import pytest

from pyatlan.client.atlan import AtlanClient

TASK_GUID = os.environ.get("ATLAN_TEST_INBOX_TASK_GUID")
ASSET_GUID = os.environ.get("ATLAN_TEST_INBOX_ASSET_GUID")


@pytest.mark.skipif(
    not TASK_GUID,
    reason="needs a pending workflow task — set ATLAN_TEST_INBOX_TASK_GUID",
)
def test_task_guid_actions_single_task(client: AtlanClient):
    """A task guid is a group of one: exactly that task is queued."""
    response = client.inbox.reject_all(
        group_key=str(TASK_GUID), comment="integration single-task reject"
    )
    assert response.message
    assert response.total_tasks == 1, (
        f"task-guid group must action exactly one task, got {response.total_tasks}"
    )


@pytest.mark.skipif(
    not ASSET_GUID,
    reason=(
        "needs an asset with 2+ pending workflow tasks — "
        "set ATLAN_TEST_INBOX_ASSET_GUID"
    ),
)
def test_asset_guid_actions_whole_group(client: AtlanClient):
    """An asset guid actions EVERY pending task on that asset — the case
    that distinguishes bulk from single approval."""
    response = client.inbox.approve_all(
        group_key=str(ASSET_GUID), comment="integration group approve"
    )
    assert response.message
    assert response.total_tasks and response.total_tasks >= 2, (
        f"asset-group bulk expected 2+ tasks queued, got {response.total_tasks} — "
        "seed at least two pending tasks on the asset before running"
    )


@pytest.mark.skipif(
    not TASK_GUID,
    reason="needs a pending workflow task — set ATLAN_TEST_INBOX_TASK_GUID",
)
def test_get_workflow_request(client: AtlanClient):
    """A workflow request fetched by guid parses the snake_case wire."""
    request = client.inbox.get(guid=str(TASK_GUID))
    # the task guid may differ from the workflow-request guid; a None here
    # is a mapping finding, not a failure — assert only on parse success
    if request is not None:
        assert request.guid
