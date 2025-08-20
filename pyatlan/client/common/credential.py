# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from json import dumps
from typing import Any, Dict, Optional

from pyatlan.client.constants import (
    CREATE_CREDENTIALS,
    DELETE_CREDENTIALS_BY_GUID,
    GET_ALL_CREDENTIALS,
    GET_CREDENTIAL_BY_GUID,
    UPDATE_CREDENTIAL_BY_GUID,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.credential import (
    Credential,
    CredentialListResponse,
    CredentialResponse,
    CredentialTestResponse,
)


class CredentialCreate:
    """
    Shared business logic for credential creation operations.
    """

    @staticmethod
    def validate_request(credential: Credential, test: bool) -> None:
        """
        Validate credential creation request parameters.

        :param credential: the credential to validate
        :param test: whether testing is enabled
        :raises UNABLE_TO_CREATE_CREDENTIAL: if validation fails
        """
        if not test and any((credential.username, credential.password)):
            raise ErrorCode.UNABLE_TO_CREATE_CREDENTIAL.exception_with_parameters()

    @staticmethod
    def prepare_request(test: bool) -> tuple[str, dict]:
        """
        Prepare the API request for credential creation.

        :param test: whether to test the credential
        :returns: tuple of (endpoint, query_params)
        """
        endpoint = CREATE_CREDENTIALS.format_path_with_params()
        query_params = {"testCredential": test}
        return endpoint, query_params

    @staticmethod
    def process_response(raw_json: dict) -> CredentialResponse:
        """
        Process the response from credential creation.

        :param raw_json: raw API response
        :returns: CredentialResponse object
        """
        return CredentialResponse(**raw_json)


class CredentialGet:
    """
    Shared business logic for retrieving a single credential.
    """

    @staticmethod
    def prepare_request(guid: str) -> str:
        """
        Prepare the API request for retrieving a credential by GUID.

        :param guid: the credential GUID
        :returns: the API endpoint
        """
        return GET_CREDENTIAL_BY_GUID.format_path({"credential_guid": guid})

    @staticmethod
    def process_response(raw_json: Any) -> CredentialResponse:
        """
        Process the response from credential retrieval.

        :param raw_json: raw API response
        :returns: CredentialResponse object or the raw response
        """
        if not isinstance(raw_json, dict):
            return raw_json
        return CredentialResponse(**raw_json)


class CredentialGetAll:
    """
    Shared business logic for retrieving all credentials.
    """

    @staticmethod
    def prepare_request(
        filter: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        workflow_name: Optional[str] = None,
    ) -> tuple[str, dict]:
        """
        Prepare the API request for retrieving all credentials.

        :param filter: optional filter criteria
        :param limit: optional maximum number of credentials
        :param offset: optional number of credentials to skip
        :param workflow_name: optional workflow name filter
        :returns: tuple of (endpoint, query_params)
        """
        params: Dict[str, Any] = {}

        if filter is not None:
            params["filter"] = dumps(filter)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        if workflow_name is not None:
            if filter is None:
                filter = {}

            if workflow_name.startswith("atlan-"):
                workflow_name = "default-" + workflow_name[len("atlan-") :]

            filter["name"] = f"{workflow_name}-0"
            params["filter"] = dumps(filter)

        endpoint = GET_ALL_CREDENTIALS.format_path_with_params()
        return endpoint, params

    @staticmethod
    def process_response(raw_json: Any) -> CredentialListResponse:
        """
        Process the response from retrieving all credentials.

        :param raw_json: raw API response
        :returns: CredentialListResponse object
        :raises JSON_ERROR: if response format is invalid
        """
        if not isinstance(raw_json, dict) or "records" not in raw_json:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                "No records found in response",
                400,
                "API response did not contain the expected 'records' key",
            )
        return CredentialListResponse(records=raw_json.get("records") or [])


class CredentialPurge:
    """
    Shared business logic for purging credentials.
    """

    @staticmethod
    def prepare_request(guid: str) -> str:
        """
        Prepare the API request for purging a credential.

        :param guid: the credential GUID to purge
        :returns: the API endpoint
        """
        return DELETE_CREDENTIALS_BY_GUID.format_path({"credential_guid": guid})


class CredentialTest:
    """
    Shared business logic for testing credentials.
    """

    @staticmethod
    def process_response(raw_json: dict) -> CredentialTestResponse:
        """
        Process the response from credential testing.

        :param raw_json: raw API response
        :returns: CredentialTestResponse object
        """
        return CredentialTestResponse(**raw_json)


class CredentialTestAndUpdate:
    """
    Shared business logic for test-and-update credential operations.
    """

    @staticmethod
    def validate_test_response(
        test_response: CredentialTestResponse, credential: Credential
    ) -> None:
        """
        Validate the test response before updating.

        :param test_response: the test response to validate
        :param credential: the credential to validate
        :raises INVALID_CREDENTIALS: if test was not successful
        :raises MISSING_TOKEN_ID: if credential has no ID
        """
        if not test_response.is_successful:
            raise ErrorCode.INVALID_CREDENTIALS.exception_with_parameters(
                test_response.message
            )
        if not credential.id:
            raise ErrorCode.MISSING_TOKEN_ID.exception_with_parameters()

    @staticmethod
    def prepare_request(credential: Credential) -> str:
        """
        Prepare the API request for updating a credential.

        :param credential: the credential to update
        :returns: the API endpoint
        """
        return UPDATE_CREDENTIAL_BY_GUID.format_path({"credential_guid": credential.id})

    @staticmethod
    def process_response(raw_json: dict) -> CredentialResponse:
        """
        Process the response from credential update.

        :param raw_json: raw API response
        :returns: CredentialResponse object
        """
        return CredentialResponse(**raw_json)
