from json import dumps
from typing import Any, Dict, Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import ApiCaller
from pyatlan.client.constants import (
    GET_ALL_CREDENTIALS,
    GET_CREDENTIAL_BY_GUID,
    TEST_CREDENTIAL,
    UPDATE_CREDENTIAL_BY_GUID,
)
from pyatlan.errors import ErrorCode
from pyatlan.model.credential import (
    Credential,
    CredentialListResponse,
    CredentialResponse,
    CredentialTestResponse,
)


class CredentialClient:
    """
    A client for managing credentials within the Atlan platform.

    This class provides functionality for interacting with Atlan's credential objects.
    It allows you to perform operations such as retrieving, testing, and updating given credentials.
    """

    def __init__(self, client: ApiCaller):
        if not isinstance(client, ApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "ApiCaller"
            )
        self._client = client

    @validate_arguments
    def get(self, guid: str) -> CredentialResponse:
        """
        Retrieves a credential by its unique identifier (GUID).
        Note that this will never contain sensitive information
        in the credential, such as usernames, passwords or client secrets or keys.

        :param guid: GUID of the credential.
        :returns: A CredentialResponse instance.
        :raises: AtlanError on any error during API invocation.
        """
        raw_json = self._client._call_api(
            GET_CREDENTIAL_BY_GUID.format_path({"credential_guid": guid})
        )
        if not isinstance(raw_json, dict):
            return raw_json
        return CredentialResponse(**raw_json)

    @validate_arguments
    def get_all(
        self,
        filter: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> CredentialListResponse:
        """
        Retrieves all credentials.

        :param filter: (optional) dictionary specifying the filter criteria.
        :param limit: (optional) maximum number of credentials to retrieve.
        :param offset: (optional) number of credentials to skip before starting retrieval.
        :returns: CredentialListResponse instance.
        :raises: AtlanError on any error during API invocation.
        """
        params: Dict[str, Any] = {}
        if filter is not None:
            params["filter"] = dumps(filter)
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset

        raw_json = self._client._call_api(
            GET_ALL_CREDENTIALS.format_path_with_params(), query_params=params
        )

        if not isinstance(raw_json, dict) or "records" not in raw_json:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                "No records found in response",
                400,
                "API response did not contain the expected 'records' key",
            )
        return CredentialListResponse(records=raw_json.get("records") or [])

    @validate_arguments
    def test(self, credential: Credential) -> CredentialTestResponse:
        """
        Tests the given credential by sending it to Atlan for validation.

        :param credential: The credential to be tested.
        :type credential: A CredentialTestResponse instance.
        :returns: The response indicating the test result.
        :raises ValidationError: If the provided credential is invalid type.
        :raises AtlanError: On any error during API invocation.
        """
        raw_json = self._client._call_api(TEST_CREDENTIAL, request_obj=credential)
        return CredentialTestResponse(**raw_json)

    @validate_arguments
    def test_and_update(self, credential: Credential) -> CredentialResponse:
        """
        Updates this credential in Atlan after first
        testing it to confirm its successful validation.

        :param credential: The credential to be tested and updated.
        :returns: An updated CredentialResponse instance.
        :raises ValidationError: If the provided credential is invalid type.
        :raises InvalidRequestException: if the provided credentials
        cannot be validated successfully.
        :raises InvalidRequestException: If the provided credential
        does not have an ID.
        :raises AtlanError: on any error during API invocation.
        """
        test_response = self.test(credential=credential)
        if not test_response.is_successful:
            raise ErrorCode.INVALID_CREDENTIALS.exception_with_parameters(
                test_response.message
            )
        if not credential.id:
            raise ErrorCode.MISSING_TOKEN_ID.exception_with_parameters()
        raw_json = self._client._call_api(
            UPDATE_CREDENTIAL_BY_GUID.format_path({"credential_guid": credential.id}),
            request_obj=credential,
        )
        return CredentialResponse(**raw_json)
