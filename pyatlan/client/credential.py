# SPDX-License-Identifier: Apache-2.0
# Copyright 2025 Atlan Pte. Ltd.
from typing import Any, Dict, Optional

from pydantic.v1 import validate_arguments

from pyatlan.client.common import (
    ApiCaller,
    CredentialCreate,
    CredentialGet,
    CredentialGetAll,
    CredentialPurge,
    CredentialTest,
    CredentialTestAndUpdate,
)
from pyatlan.client.constants import TEST_CREDENTIAL
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
    def creator(self, credential: Credential, test: bool = True) -> CredentialResponse:
        """
        Create a new credential.

        :param credential: provide full details of the credential's to be created.
        :param test: whether to validate the credentials (`True`) or skip validation
        (`False`) before creation, defaults to `True`.
        :returns: A CredentialResponse instance.
        :raises ValidationError: If the provided `credential` is invalid.
        :raises InvalidRequestError: If `test` is `False` and the credential contains a `username` or `password`.
        """
        # Validate request using shared logic
        CredentialCreate.validate_request(credential, test)

        # Prepare request using shared logic
        endpoint, query_params = CredentialCreate.prepare_request(test)

        # Make API call
        raw_json = self._client._call_api(
            api=endpoint,
            query_params=query_params,
            request_obj=credential,
        )

        # Process response using shared logic
        return CredentialCreate.process_response(raw_json)

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
        # Prepare request using shared logic
        endpoint = CredentialGet.prepare_request(guid)

        # Make API call
        raw_json = self._client._call_api(endpoint)

        # Process response using shared logic
        return CredentialGet.process_response(raw_json)

    @validate_arguments
    def get_all(
        self,
        filter: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        workflow_name: Optional[str] = None,
    ) -> CredentialListResponse:
        """
        Retrieves all credentials.

        :param filter: (optional) dictionary specifying the filter criteria.
        :param limit: (optional) maximum number of credentials to retrieve.
        :param offset: (optional) number of credentials to skip before starting retrieval.
        :param workflow_name: (optional) name of the workflow to retrieve credentials for.
        :returns: CredentialListResponse instance.
        :raises: AtlanError on any error during API invocation.
        """
        # Prepare request using shared logic
        endpoint, params = CredentialGetAll.prepare_request(
            filter, limit, offset, workflow_name
        )

        # Make API call
        raw_json = self._client._call_api(endpoint, query_params=params)

        # Process response using shared logic
        return CredentialGetAll.process_response(raw_json)

    @validate_arguments
    def purge_by_guid(self, guid: str) -> CredentialResponse:
        """
        Hard-deletes (purges) credential by their unique identifier (GUID).
        This operation is irreversible.

        :param guid: unique identifier(s) (GUIDs) of credential to hard-delete
        :returns: details of the hard-deleted asset(s)
        :raises AtlanError: on any API communication issue
        """
        # Prepare request using shared logic
        endpoint = CredentialPurge.prepare_request(guid)

        # Make API call
        raw_json = self._client._call_api(endpoint)

        return raw_json

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
        # Make API call
        raw_json = self._client._call_api(TEST_CREDENTIAL, request_obj=credential)

        # Process response using shared logic
        return CredentialTest.process_response(raw_json)

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
        # Test credential first
        test_response = self.test(credential=credential)

        # Validate test response using shared logic
        CredentialTestAndUpdate.validate_test_response(test_response, credential)

        # Prepare update request using shared logic
        endpoint = CredentialTestAndUpdate.prepare_request(credential)

        # Make API call
        raw_json = self._client._call_api(endpoint, request_obj=credential)

        # Process response using shared logic
        return CredentialTestAndUpdate.process_response(raw_json)
