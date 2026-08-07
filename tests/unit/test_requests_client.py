# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 Atlan Pte. Ltd.
from json import loads
from unittest.mock import Mock

import pytest

from pyatlan.client.common import ApiCaller
from pyatlan.client.requests import RequestsClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.atlan_request import AtlanRequest, AttributeRequest

REQUEST_ID = "070c46dc-734b-4bed-b89f-54ae752ec589"
TERM_GUID = "9c67229e-f345-4de4-b046-c3b6cb2a5c34"

RAW_REQUEST = {
    "id": REQUEST_ID,
    "version": "bold-bonus-8934",
    "isActive": True,
    "createdAt": 1786102423732,
    "updatedAt": 1786102423732,
    "createdBy": "service-account-example",
    "tenantId": "default",
    "sourceType": "static",
    "destinationGuid": TERM_GUID,
    "destinationQualifiedName": "abc@def",
    "destinationAttribute": "userDescription",
    "destinationValue": "requested value",
    "entityType": "AtlasGlossaryTerm",
    "requestType": "attribute",
    "status": "active",
    "approvalType": "single",
}

RAW_LIST = {"totalRecord": 2, "filterRecord": 1, "records": [RAW_REQUEST]}


@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    monkeypatch.setenv("ATLAN_BASE_URL", "https://test.atlan.com")
    monkeypatch.setenv("ATLAN_API_KEY", "test-api-key")


@pytest.fixture()
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def client(mock_api_caller) -> RequestsClient:
    return RequestsClient(mock_api_caller)


def test_init_rejects_non_api_caller():
    with pytest.raises(
        InvalidRequestError, match="ATLAN-PYTHON-400-048.*ApiCaller"
    ):
        RequestsClient("not-a-client")  # type: ignore[arg-type]


def test_list_parses_paged_response(client, mock_api_caller):
    mock_api_caller._call_api.return_value = RAW_LIST
    response = client.list(post_filter='{"status":"active"}')

    assert response.total_record == 2
    assert response.filter_record == 1
    assert len(response.records) == 1
    record = response.records[0]
    assert record.id == REQUEST_ID
    assert record.status == "active"
    assert record.destination_attribute == "userDescription"
    # the filter reached the query params
    query_params = mock_api_caller._call_api.call_args[0][1]
    assert query_params["filter"] == '{"status":"active"}'
    mock_api_caller.reset_mock()


def test_list_actionable_uses_actionable_route(client, mock_api_caller):
    mock_api_caller._call_api.return_value = RAW_LIST
    response = client.list_actionable()

    assert response.total_record == 2
    endpoint = mock_api_caller._call_api.call_args[0][0]
    assert "actionable" in endpoint.path
    mock_api_caller.reset_mock()


def test_get_unwraps_single_element_list(client, mock_api_caller):
    """The by-id endpoint may wrap the request in a single-element list."""
    mock_api_caller._call_api.return_value = [RAW_REQUEST]
    request = client.get(guid=REQUEST_ID)

    assert isinstance(request, AtlanRequest)
    assert request.id == REQUEST_ID
    mock_api_caller.reset_mock()


def test_create_sends_all_wire_required_fields(client, mock_api_caller):
    """createRequest requires requestType/approvalType/sourceType/entityType —
    the creator must set them explicitly so exclude_unset serialization keeps
    them (the BLDX-1589 default-stripping trap)."""
    mock_api_caller._call_api.return_value = RAW_REQUEST
    request = AttributeRequest.creator(
        destination_guid=TERM_GUID,
        destination_qualified_name="abc@def",
        destination_attribute="userDescription",
        destination_value="requested value",
        entity_type="AtlasGlossaryTerm",
    )
    created = client.create(request)

    assert created and created.id == REQUEST_ID
    sent = loads(
        mock_api_caller._call_api.call_args.kwargs["request_obj"].json(
            by_alias=True, exclude_unset=True
        )
    )
    for required in ("requestType", "approvalType", "sourceType", "entityType"):
        assert required in sent, f"{required} missing from the wire payload"
    assert sent["requestType"] == "attribute"
    assert sent["approvalType"] == "single"
    mock_api_caller.reset_mock()


@pytest.mark.parametrize(
    "method, expected_action",
    [("approve", "approved"), ("reject", "rejected")],
)
def test_action_posts_expected_body(client, mock_api_caller, method, expected_action):
    mock_api_caller._call_api.return_value = "success"
    result = getattr(client, method)(guid=REQUEST_ID, message="because")

    assert result is True
    endpoint = mock_api_caller._call_api.call_args[0][0]
    assert REQUEST_ID in endpoint.path and endpoint.path.endswith("/action")
    body = loads(
        mock_api_caller._call_api.call_args.kwargs["request_obj"].json(
            by_alias=True, exclude_unset=True
        )
    )
    assert body == {"action": expected_action, "message": "because"}
    mock_api_caller.reset_mock()


def test_action_non_success_is_false(client, mock_api_caller):
    mock_api_caller._call_api.return_value = {"unexpected": "shape"}
    assert client.approve(guid=REQUEST_ID) is False
    mock_api_caller.reset_mock()
