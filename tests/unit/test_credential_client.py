# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Atlan Pte. Ltd.
from unittest.mock import Mock

import pytest
from pydantic.v1 import ValidationError

from pyatlan.client.common import ApiCaller
from pyatlan.client.credential import CredentialClient
from pyatlan.errors import InvalidRequestError
from pyatlan.model.credential import (
    Credential,
    CredentialListResponse,
    CredentialResponse,
    CredentialTestResponse,
)

TEST_MISSING_TOKEN_ID = (
    "ATLAN-PYTHON-400-032 No ID was provided when attempting to update the API token."
)
TEST_INVALID_CREDENTIALS = (
    "ATLAN-PYTHON-400-054 Credentials provided did not work: failed"
)
TEST_INVALID_GUID_GET_VALIDATION_ERR = (
    "1 validation error for Get\nguid\n  str type expected (type=type_error.str)"
)
TEST_INVALID_GUID_PURGE_BY_GUID_VALIDATION_ERR = "1 validation error for PurgeByGuid\nguid\n  str type expected (type=type_error.str)"
TEST_INVALID_CRED_TEST_VALIDATION_ERR = "1 validation error for Test\ncredential\n  value is not a valid dict (type=type_error.dict)"
TEST_INVALID_CRED_TEST_UPDATE_VALIDATION_ERR = "1 validation error for TestAndUpdate\ncredential\n  value is not a valid dict (type=type_error.dict)"
TEST_INVALID_CRED_CREATOR_VALIDATION_ERR = "1 validation error for Creator\ncredential\n  value is not a valid dict (type=type_error.dict)"
TEST_INVALID_API_CALLER_PARAMETER_TYPE = (
    "ATLAN-PYTHON-400-048 Invalid parameter type for client should be ApiCaller"
)


@pytest.fixture()
def mock_api_caller():
    return Mock(spec=ApiCaller)


@pytest.fixture()
def client(mock_api_caller) -> CredentialClient:
    return CredentialClient(mock_api_caller)


@pytest.fixture()
def credential_response() -> CredentialResponse:
    return CredentialResponse(  # type: ignore[call-arg]
        id="test-id",
        version="1.2.3",
        is_active=True,
        created_at=1704186290006,
        updated_at=1704218661848,
        created_by="test-acc",
        tenant_id="default",
        name="test-name",
        description="test-desc",
        connector_config_name="test-ccn",
        connector="test-conn",
        connector_type="test-ct",
        auth_type="test-at",
        host="test-host",
        port=123,
        metadata=None,
        level=None,
        connection=None,
        username="test-username",
        extras={"some": "value"},
    )


def _assert_cred_response(cred: Credential, cred_response: CredentialResponse):
    assert cred.id == cred_response.id
    assert cred.name == cred_response.name
    assert cred.port == cred_response.port
    assert cred.auth_type == cred_response.auth_type
    assert cred.connector_type == cred_response.connector_type
    assert cred.connector_config_name == cred_response.connector_config_name
    assert cred.username == cred_response.username
    assert cred.extras == cred_response.extras


@pytest.mark.parametrize("test_api_caller", ["abc", None])
def test_init_when_wrong_class_raises_exception(test_api_caller):
    with pytest.raises(
        InvalidRequestError,
        match=TEST_INVALID_API_CALLER_PARAMETER_TYPE,
    ):
        CredentialClient(test_api_caller)


@pytest.mark.parametrize("test_guid", [[123], set(), dict()])
def test_cred_get_wrong_params_raises_validation_error(
    test_guid, client: CredentialClient
):
    with pytest.raises(ValidationError) as err:
        client.get(guid=test_guid)
    assert TEST_INVALID_GUID_GET_VALIDATION_ERR == str(err.value)


@pytest.mark.parametrize("test_credentials", ["invalid_cred", 123])
def test_cred_test_wrong_params_raises_validation_error(
    test_credentials, client: CredentialClient
):
    with pytest.raises(ValidationError) as err:
        client.test(credential=test_credentials)
    assert TEST_INVALID_CRED_TEST_VALIDATION_ERR == str(err.value)


@pytest.mark.parametrize("test_credentials", ["invalid_cred", 123])
def test_cred_test_and_update_wrong_params_raises_validation_error(
    test_credentials, client: CredentialClient
):
    with pytest.raises(ValidationError) as err:
        client.test_and_update(credential=test_credentials)
    assert TEST_INVALID_CRED_TEST_UPDATE_VALIDATION_ERR == str(err.value)


@pytest.mark.parametrize(
    "test_credentials, test_response",
    [
        [Credential(), "successful"],
        [Credential(id="test-id"), "failed"],
    ],
)
def test_cred_test_update_raises_invalid_request_error(
    test_credentials, test_response, mock_api_caller, client: CredentialClient
):
    mock_api_caller._call_api.return_value = {"message": test_response}
    with pytest.raises(InvalidRequestError) as err:
        client.test_and_update(credential=test_credentials)
    if test_response == "successful":
        assert TEST_MISSING_TOKEN_ID in str(err.value)
    else:
        assert TEST_INVALID_CREDENTIALS in str(err.value)


def test_cred_get_when_given_guid(
    client: CredentialClient,
    mock_api_caller,
    credential_response: CredentialResponse,
):
    mock_api_caller._call_api.return_value = credential_response.dict()
    assert client.get(guid="test-id") == credential_response
    cred = client.get(guid="test-id").to_credential()
    assert isinstance(cred, Credential)
    _assert_cred_response(cred, credential_response)


def test_cred_get_when_given_wrong_guid(
    client: CredentialClient,
    mock_api_caller,
    credential_response: CredentialResponse,
):
    mock_api_caller._call_api.return_value = None
    assert client.get(guid="test-wrong-id") is None


def test_cred_test_when_given_cred(
    client: CredentialClient,
    mock_api_caller,
    credential_response: CredentialResponse,
):
    mock_api_caller._call_api.return_value = {"message": "successful"}
    cred_test_response = client.test(credential=Credential())
    assert isinstance(cred_test_response, CredentialTestResponse)
    assert cred_test_response.message == "successful"
    assert cred_test_response.code is None
    assert cred_test_response.error is None
    assert cred_test_response.info is None
    assert cred_test_response.request_id is None


def test_cred_test_update_when_given_cred(
    client: CredentialClient,
    mock_api_caller,
    credential_response: CredentialResponse,
):
    mock_api_caller._call_api.side_effect = [
        {"message": "successful"},
        credential_response.dict(),
    ]
    cred_response = client.test_and_update(
        credential=Credential(id=credential_response.id)
    )
    assert isinstance(cred_response, CredentialResponse)
    cred = cred_response.to_credential()
    _assert_cred_response(cred, credential_response)


@pytest.mark.parametrize(
    "test_filter, test_limit, test_offset, test_response",
    [
        (None, None, None, {"records": [{"id": "cred1"}, {"id": "cred2"}]}),
        ({"name": "test"}, 5, 0, {"records": [{"id": "cred3"}]}),
        ({"invalid": "field"}, 10, 0, {"records": []}),
    ],
)
def test_cred_get_all_success(
    test_filter, test_limit, test_offset, test_response, mock_api_caller
):
    mock_api_caller._call_api.return_value = test_response
    client = CredentialClient(mock_api_caller)

    result = client.get_all(filter=test_filter, limit=test_limit, offset=test_offset)

    assert isinstance(result, CredentialListResponse)
    assert len(result.records) == len(test_response["records"])
    for record, expected in zip(result.records, test_response["records"]):
        assert record.id == expected["id"]


def test_cred_get_all_empty_response(mock_api_caller):
    mock_api_caller._call_api.return_value = {"records": []}
    client = CredentialClient(mock_api_caller)

    result = client.get_all()

    assert isinstance(result, CredentialListResponse)
    assert len(result.records) == 0


def test_cred_get_all_invalid_response(mock_api_caller):
    mock_api_caller._call_api.return_value = {}
    client = CredentialClient(mock_api_caller)

    with pytest.raises(Exception, match="No records found in response"):
        client.get_all()


@pytest.mark.parametrize(
    "test_filter, test_limit, test_offset",
    [
        ("invalid_filter", None, None),
        (None, "invalid_limit", None),
        (None, None, "invalid_offset"),
    ],
)
def test_cred_get_all_invalid_params_raises_validation_error(
    test_filter, test_limit, test_offset, client: CredentialClient
):
    with pytest.raises(ValidationError):
        client.get_all(filter=test_filter, limit=test_limit, offset=test_offset)


def test_cred_get_all_timeout(mock_api_caller):
    mock_api_caller._call_api.side_effect = TimeoutError("Request timed out")
    client = CredentialClient(mock_api_caller)

    with pytest.raises(TimeoutError, match="Request timed out"):
        client.get_all()


def test_cred_get_all_partial_response(mock_api_caller):
    mock_api_caller._call_api.return_value = {
        "records": [
            {
                "id": "cred1",
                "name": "Test Credential",
                "level": "user",
                "connection": "default/bigquery/1697545730",
            }
        ]
    }
    client = CredentialClient(mock_api_caller)

    result = client.get_all()

    assert isinstance(result, CredentialListResponse)
    assert result.records[0].host is None
    assert result.records[0].id == "cred1"
    assert result.records[0].name == "Test Credential"
    assert result.records[0].level == "user"
    assert result.records[0].connection == "default/bigquery/1697545730"


def test_cred_get_all_invalid_filter_type(mock_api_caller):
    client = CredentialClient(mock_api_caller)

    with pytest.raises(ValidationError, match="value is not a valid dict"):
        client.get_all(filter="invalid_filter")


def test_cred_get_all_no_results(mock_api_caller):
    mock_api_caller._call_api.return_value = {"records": None}
    client = CredentialClient(mock_api_caller)

    result = client.get_all(filter={"name": "nonexistent"})

    assert isinstance(result, CredentialListResponse)
    assert result.records == []
    assert len(result.records) == 0


@pytest.mark.parametrize("create_credentials", ["invalid_cred", 123])
def test_cred_creator_wrong_params_raises_validation_error(
    create_credentials, client: CredentialClient
):
    with pytest.raises(ValidationError) as err:
        client.creator(credential=create_credentials)
    assert TEST_INVALID_CRED_CREATOR_VALIDATION_ERR == str(err.value)


@pytest.mark.parametrize(
    "credential_data",
    [
        (
            Credential(
                name="test-name",
                description="test-desc",
                connector_config_name="test-ccn",
                connector="test-conn",
                connector_type="test-ct",
                auth_type="test-at",
                host="test-host",
                port=123,
                username="test-username",
                extra={"some": "value"},
            )
        ),
    ],
)
def test_creator_success(
    credential_data,
    credential_response: CredentialResponse,
    mock_api_caller,
    client: CredentialClient,
):
    mock_api_caller._call_api.return_value = credential_response.dict()
    client = CredentialClient(mock_api_caller)

    response = client.creator(credential=credential_data)

    assert isinstance(response, CredentialResponse)
    assert credential_data.name == response.name
    assert credential_data.description == response.description
    assert credential_data.port == response.port
    assert credential_data.auth_type == response.auth_type
    assert credential_data.connector_type == response.connector_type
    assert credential_data.connector_config_name == response.connector_config_name
    assert credential_data.username == response.username
    assert credential_data.extras == response.extras
    assert response.level is None


@pytest.mark.parametrize(
    "credential_data",
    [
        (
            Credential(
                name="test-name",
                description="test-desc",
                connector_config_name="test-ccn",
                connector="test-conn",
                connector_type="test-ct",
                auth_type="test-at",
                host="test-host",
                port=123,
                username="test-user",
                password="test-password",
                extra={"some": "value"},
            )
        ),
    ],
)
def test_cred_creator_with_test_false_with_username_password(
    credential_data, client: CredentialClient
):
    with pytest.raises(Exception, match="ATLAN-PYTHON-400-071"):
        client.creator(credential=credential_data, test=False)


@pytest.mark.parametrize("test_guid", [[123], set(), dict()])
def test_cred_purge_by_guid_wrong_params_raises_validation_error(
    test_guid, client: CredentialClient
):
    with pytest.raises(ValidationError) as err:
        client.purge_by_guid(guid=test_guid)
    assert TEST_INVALID_GUID_PURGE_BY_GUID_VALIDATION_ERR == str(err.value)


def test_cred_purge_by_guid_when_given_guid(
    client: CredentialClient,
    mock_api_caller,
):
    mock_api_caller._call_api.return_value = None
    assert client.purge_by_guid(guid="test-id") is None
