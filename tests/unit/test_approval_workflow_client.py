# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
from json import loads
from unittest.mock import Mock

import pytest

from pyatlan.client.approval_workflow import ApprovalWorkflowClient
from pyatlan.client.common import ApiCaller
from pyatlan.errors import InvalidRequestError
from pyatlan.model.approval_workflow import ApprovalWorkflowRequest

WF_REQUEST_GUID = "1a2b3c4d-1111-2222-3333-444455556666"
ASSET_GUID = "9c67229e-f345-4de4-b046-c3b6cb2a5c34"

RAW_WF_REQUEST = {
    "guid": WF_REQUEST_GUID,
    "name": "Access request",
    "approval_workflow_request_type": "DATA_ACCESS",
    "request_on_asset_guid": ASSET_GUID,
    "status": "PENDING",
    "created_by": "aryaman-alt",
}


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def client(mock_api_caller) -> ApprovalWorkflowClient:
    return ApprovalWorkflowClient(mock_api_caller)


def test_init_rejects_non_api_caller():
    with pytest.raises(InvalidRequestError, match="ATLAN-PYTHON-400-048.*ApiCaller"):
        ApprovalWorkflowClient("not-a-client")  # type: ignore[arg-type]


def test_get_parses_snake_case_wire(client, mock_api_caller):
    """The approval-workflow API family is snake_case on the wire — fields
    must parse without camelCase aliasing."""
    mock_api_caller._call_api.return_value = RAW_WF_REQUEST
    request = client.get(guid=WF_REQUEST_GUID)

    assert isinstance(request, ApprovalWorkflowRequest)
    assert request.approval_workflow_request_type == "DATA_ACCESS"
    assert request.request_on_asset_guid == ASSET_GUID
    mock_api_caller.reset_mock()


@pytest.mark.parametrize(
    "method, decision",
    [("approve_all", "APPROVED"), ("reject_all", "REJECTED")],
)
def test_bulk_action_body_is_snake_case(client, mock_api_caller, method, decision):
    mock_api_caller._call_api.return_value = {
        "total_tasks": 3,
        "message": "queued",
    }
    result = getattr(client, method)(
        group_key=ASSET_GUID, sub_type="DATA_ACCESS", comment="bulk"
    )

    assert result.total_tasks == 3
    assert result.message == "queued"
    endpoint = mock_api_caller._call_api.call_args[0][0]
    assert endpoint.path.endswith("/actions/bulk")
    body = loads(
        mock_api_caller._call_api.call_args.kwargs["request_obj"].json(
            by_alias=True, exclude_unset=True
        )
    )
    assert body == {
        "group_key": ASSET_GUID,
        "decision": decision,
        "sub_type": "DATA_ACCESS",
        "comment": "bulk",
    }
    mock_api_caller.reset_mock()


def test_bulk_action_omits_optional_fields(client, mock_api_caller):
    """sub_type/comment stay off the wire when not given (exclude_unset)."""
    mock_api_caller._call_api.return_value = {"total_tasks": 1, "message": "ok"}
    client.approve_all(group_key=ASSET_GUID)

    body = loads(
        mock_api_caller._call_api.call_args.kwargs["request_obj"].json(
            by_alias=True, exclude_unset=True
        )
    )
    assert body == {"group_key": ASSET_GUID, "decision": "APPROVED"}
    mock_api_caller.reset_mock()
