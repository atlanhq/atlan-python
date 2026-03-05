from __future__ import annotations

from typing import Any, Dict, Optional

import msgspec

from pyatlan.client.common import (
    AsyncApiCaller,
    CredentialCreate,
    CredentialGet,
    CredentialGetAll,
    CredentialPurge,
    CredentialTestAndUpdate,
)
from pyatlan.client.constants import TEST_CREDENTIAL
from pyatlan.errors import ErrorCode
from pyatlan_v9.model.credential import (
    Credential,
    CredentialListResponse,
    CredentialResponse,
    CredentialTestResponse,
)
from pyatlan_v9.validate import validate_arguments


class V9AsyncCredentialClient:
    """
    Async version of CredentialClient for managing credentials within the Atlan platform.
    This class does not need to be instantiated directly but can be obtained through the credentials property of AsyncAtlanClient.
    """

    def __init__(self, client: AsyncApiCaller):
        if not isinstance(client, AsyncApiCaller):
            raise ErrorCode.INVALID_PARAMETER_TYPE.exception_with_parameters(
                "client", "AsyncApiCaller"
            )
        self._client = client

    @validate_arguments
    async def creator(
        self, credential: Credential, test: bool = True
    ) -> CredentialResponse:
        """
        Create a new credential (async version).

        :param credential: provide full details of the credential's to be created.
        :param test: whether to validate the credentials (`True`) or skip validation
        (`False`) before creation, defaults to `True`.
        :returns: A CredentialResponse instance.
        :raises ValidationError: If the provided `credential` is invalid.
        :raises InvalidRequestError: If `test` is `False` and the credential contains a `username` or `password`.
        """
        CredentialCreate.validate_request(credential, test)
        endpoint, query_params = CredentialCreate.prepare_request(test)
        raw_json = await self._client._call_api(
            api=endpoint,
            query_params=query_params,
            request_obj=credential,
        )
        return msgspec.convert(raw_json, CredentialResponse, strict=False)

    @validate_arguments
    async def get(self, guid: str) -> CredentialResponse:
        """
        Retrieves a credential by its unique identifier (GUID) (async version).
        Note that this will never contain sensitive information
        in the credential, such as usernames, passwords or client secrets or keys.

        :param guid: GUID of the credential.
        :returns: A CredentialResponse instance.
        :raises: AtlanError on any error during API invocation.
        """
        endpoint = CredentialGet.prepare_request(guid)
        raw_json = await self._client._call_api(endpoint)
        if not isinstance(raw_json, dict):
            return raw_json
        return msgspec.convert(raw_json, CredentialResponse, strict=False)

    @validate_arguments
    async def get_all(
        self,
        filter: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        workflow_name: Optional[str] = None,
    ) -> CredentialListResponse:
        """
        Retrieves all credentials (async version).

        :param filter: (optional) dictionary specifying the filter criteria.
        :param limit: (optional) maximum number of credentials to retrieve.
        :param offset: (optional) number of credentials to skip before starting retrieval.
        :param workflow_name: (optional) name of the workflow to retrieve credentials for.
        :returns: CredentialListResponse instance.
        :raises: AtlanError on any error during API invocation.
        """
        endpoint, params = CredentialGetAll.prepare_request(
            filter, limit, offset, workflow_name
        )
        raw_json = await self._client._call_api(endpoint, query_params=params)
        if not isinstance(raw_json, dict) or "records" not in raw_json:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                "No records found in response",
                400,
                "API response did not contain the expected 'records' key",
            )
        if raw_json.get("records") is None:
            raw_json["records"] = []
        return msgspec.convert(raw_json, CredentialListResponse, strict=False)

    @validate_arguments
    async def purge_by_guid(self, guid: str) -> CredentialResponse:
        """
        Hard-deletes (purges) credential by their unique identifier (GUID) (async version).
        This operation is irreversible.

        :param guid: unique identifier(s) (GUIDs) of credential to hard-delete
        :returns: details of the hard-deleted asset(s)
        :raises AtlanError: on any API communication issue
        """
        endpoint = CredentialPurge.prepare_request(guid)
        raw_json = await self._client._call_api(endpoint)
        return raw_json

    @validate_arguments
    async def test(self, credential: Credential) -> CredentialTestResponse:
        """
        Tests the given credential by sending it to Atlan for validation (async version).

        :param credential: The credential to be tested.
        :type credential: A CredentialTestResponse instance.
        :returns: The response indicating the test result.
        :raises ValidationError: If the provided credential is invalid type.
        :raises AtlanError: On any error during API invocation.
        """
        raw_json = await self._client._call_api(TEST_CREDENTIAL, request_obj=credential)
        return msgspec.convert(raw_json, CredentialTestResponse, strict=False)

    @validate_arguments
    async def test_and_update(self, credential: Credential) -> CredentialResponse:
        """
        Updates this credential in Atlan after first
        testing it to confirm its successful validation (async version).

        :param credential: The credential to be tested and updated.
        :returns: An updated CredentialResponse instance.
        :raises ValidationError: If the provided credential is invalid type.
        :raises InvalidRequestException: if the provided credentials
        cannot be validated successfully.
        :raises InvalidRequestException: If the provided credential
        does not have an ID.
        :raises AtlanError: on any error during API invocation.
        """
        test_response = await self.test(credential=credential)
        CredentialTestAndUpdate.validate_test_response(test_response, credential)
        endpoint = CredentialTestAndUpdate.prepare_request(credential)
        raw_json = await self._client._call_api(endpoint, request_obj=credential)
        return msgspec.convert(raw_json, CredentialResponse, strict=False)
