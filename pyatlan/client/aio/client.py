"""
Async Atlan Client
==================

Main async client that provides the same API as AtlanClient but with async/await support.
"""

from __future__ import annotations

import asyncio
import contextlib
import copy
import json
import logging
import os
from http import HTTPStatus
from types import SimpleNamespace
from typing import Optional

import httpx
from httpx_retries.retry import Retry
from pydantic.v1 import PrivateAttr

from pyatlan.cache.aio import (
    AsyncAtlanTagCache,
    AsyncConnectionCache,
    AsyncCustomMetadataCache,
    AsyncDQTemplateConfigCache,
    AsyncEnumCache,
    AsyncGroupCache,
    AsyncRoleCache,
    AsyncSourceTagCache,
    AsyncUserCache,
)
from pyatlan.client.aio.admin import AsyncAdminClient
from pyatlan.client.aio.asset import AsyncAssetClient
from pyatlan.client.aio.audit import AsyncAuditClient
from pyatlan.client.aio.contract import AsyncContractClient
from pyatlan.client.aio.credential import AsyncCredentialClient
from pyatlan.client.aio.file import AsyncFileClient
from pyatlan.client.aio.group import AsyncGroupClient
from pyatlan.client.aio.impersonate import AsyncImpersonationClient
from pyatlan.client.aio.open_lineage import AsyncOpenLineageClient
from pyatlan.client.aio.query import AsyncQueryClient
from pyatlan.client.aio.role import AsyncRoleClient
from pyatlan.client.aio.search_log import AsyncSearchLogClient
from pyatlan.client.aio.sso import AsyncSSOClient
from pyatlan.client.aio.task import AsyncTaskClient
from pyatlan.client.aio.token import AsyncTokenClient
from pyatlan.client.aio.typedef import AsyncTypeDefClient
from pyatlan.client.aio.user import AsyncUserClient
from pyatlan.client.aio.workflow import AsyncWorkflowClient
from pyatlan.client.atlan import (
    CONNECTION_RETRY,
    VERSION,
    AtlanClient,
    get_python_version,
)
from pyatlan.client.common import ImpersonateUser
from pyatlan.client.constants import EVENT_STREAM, GET_TOKEN, UPLOAD_IMAGE
from pyatlan.client.transport import PyatlanAsyncTransport  # type: ignore
from pyatlan.errors import ERROR_CODE_FOR_HTTP_STATUS, AtlanError, ErrorCode
from pyatlan.model.aio.core import AsyncAtlanRequest, AsyncAtlanResponse
from pyatlan.model.atlan_image import AtlanImage
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanTypeCategory
from pyatlan.model.response import AccessTokenResponse
from pyatlan.multipart_data_generator import MultipartDataGenerator
from pyatlan.utils import APPLICATION_ENCODED_FORM

LOGGER = logging.getLogger(__name__)


class AsyncAtlanClient(AtlanClient):
    """
    Async Atlan client with the same API as sync AtlanClient.

    This client reuses all existing sync business logic while providing
    async/await support for all operations.

    Usage:
        # Same API as sync, just add await
        async_client = AsyncAtlanClient()
        results = await async_client.asset.search(criteria)  # vs sync: client.asset.search(criteria)

        # Or with context manager
        async with AsyncAtlanClient() as client:
            results = await client.asset.search(criteria)
    """

    _async_session: Optional[httpx.AsyncClient] = PrivateAttr(default=None)
    _async_admin_client: Optional[AsyncAdminClient] = PrivateAttr(default=None)
    _async_asset_client: Optional[AsyncAssetClient] = PrivateAttr(default=None)
    _async_audit_client: Optional[AsyncAuditClient] = PrivateAttr(default=None)
    _async_contract_client: Optional[AsyncContractClient] = PrivateAttr(default=None)
    _async_credential_client: Optional[AsyncCredentialClient] = PrivateAttr(
        default=None
    )
    _async_file_client: Optional[AsyncFileClient] = PrivateAttr(default=None)
    _async_group_client: Optional[AsyncGroupClient] = PrivateAttr(default=None)
    _async_impersonate_client: Optional[AsyncImpersonationClient] = PrivateAttr(
        default=None
    )
    _async_open_lineage_client: Optional[AsyncOpenLineageClient] = PrivateAttr(
        default=None
    )
    _async_query_client: Optional[AsyncQueryClient] = PrivateAttr(default=None)
    _async_role_client: Optional[AsyncRoleClient] = PrivateAttr(default=None)
    _async_search_log_client: Optional[AsyncSearchLogClient] = PrivateAttr(default=None)
    _async_sso_client: Optional[AsyncSSOClient] = PrivateAttr(default=None)
    _async_task_client: Optional[AsyncTaskClient] = PrivateAttr(default=None)
    _async_token_client: Optional[AsyncTokenClient] = PrivateAttr(default=None)
    _async_typedef_client: Optional[AsyncTypeDefClient] = PrivateAttr(default=None)
    _async_user_client: Optional[AsyncUserClient] = PrivateAttr(default=None)
    _async_workflow_client: Optional[AsyncWorkflowClient] = PrivateAttr(default=None)

    # Async cache instances
    _async_atlan_tag_cache: Optional[AsyncAtlanTagCache] = PrivateAttr(default=None)
    _async_connection_cache: Optional[AsyncConnectionCache] = PrivateAttr(default=None)
    _async_custom_metadata_cache: Optional[AsyncCustomMetadataCache] = PrivateAttr(
        default=None
    )
    _async_dq_template_config_cache: Optional[AsyncDQTemplateConfigCache] = PrivateAttr(
        default=None
    )
    _async_enum_cache: Optional[AsyncEnumCache] = PrivateAttr(default=None)
    _async_group_cache: Optional[AsyncGroupCache] = PrivateAttr(default=None)
    _async_role_cache: Optional[AsyncRoleCache] = PrivateAttr(default=None)
    _async_source_tag_cache: Optional[AsyncSourceTagCache] = PrivateAttr(default=None)
    _async_user_cache: Optional[AsyncUserCache] = PrivateAttr(default=None)

    def __init__(self, **kwargs):
        # Initialize sync client (handles all validation, env vars, etc.)
        super().__init__(**kwargs)

        # Build proxy/SSL configuration (reuse from sync client)
        transport_kwargs = self._build_transport_proxy_config(kwargs)

        # Create async session with custom transport that supports retry and proxy
        self._async_session = httpx.AsyncClient(
            transport=PyatlanAsyncTransport(retry=self.retry, **transport_kwargs),
            headers={
                "x-atlan-agent": "sdk",
                "x-atlan-agent-id": "python",
                "x-atlan-client-origin": "product_sdk",
                "x-atlan-python-version": get_python_version(),
                "x-atlan-client-type": "async",
                "User-Agent": f"Atlan-PythonSDK/{VERSION}",
            },
            base_url=str(self.base_url),
        )

    @classmethod
    async def from_token_guid(  # type: ignore[override]
        cls,
        guid: str,
        base_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
    ) -> AsyncAtlanClient:
        """
        Create an AsyncAtlanClient instance using an API token GUID.

        This method performs a multi-step authentication flow:
        1. Obtains Atlan-Argo (superuser) access token
        2. Uses Argo token to retrieve the API token's client credentials
        3. Exchanges those credentials for an access token
        4. Returns a new AsyncAtlanClient authenticated with the resolved token

        :param guid: API token GUID to resolve
        :param base_url: Optional base URL for the Atlan service(overrides ATLAN_BASE_URL environment variable)
        :param client_id: Optional client ID for authentication (overrides CLIENT_ID environment variable)
        :param client_secret: Optional client secret for authentication (overrides CLIENT_SECRET environment variable)
        :returns: a new async client instance authenticated with the resolved token
        :raises: ErrorCode.UNABLE_TO_ESCALATE_WITH_PARAM: If any step in the token resolution fails
        """
        final_base_url = base_url or os.environ.get("ATLAN_BASE_URL", "INTERNAL")

        # Step 1: Initialize base client and get Atlan-Argo credentials
        # Note: Using empty api_key as we're bootstrapping authentication
        client = cls(base_url=final_base_url, api_key="")
        client_info = ImpersonateUser.get_client_info(
            client_id=client_id, client_secret=client_secret
        )

        # Prepare credentials for Atlan-Argo token request
        argo_credentials = {
            "grant_type": "client_credentials",
            "client_id": client_info.client_id,
            "client_secret": client_info.client_secret,
            "scope": "openid",
        }

        # Step 2: Obtain Atlan-Argo (superuser) access token
        try:
            raw_json = await client._call_api(GET_TOKEN, request_obj=argo_credentials)
            argo_token = AccessTokenResponse(**raw_json).access_token
            temp_argo_client = cls(base_url=final_base_url, api_key=argo_token)
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_ESCALATE_WITH_PARAM.exception_with_parameters(
                "Failed to obtain Atlan-Argo token"
            ) from atlan_err

        # Step 3: Use Argo client to retrieve API token's credentials
        # Both endpoints require authentication, hence using the Argo token
        token_secret = await temp_argo_client.impersonate.get_client_secret(
            client_guid=guid
        )
        token_client_id = (
            await temp_argo_client.token.get_by_guid(guid=guid)
        ).client_id  # type: ignore[union-attr]

        # Step 4: Exchange API token credentials for access token
        token_credentials = {
            "grant_type": "client_credentials",
            "client_id": token_client_id,
            "client_secret": token_secret,
            "scope": "openid",
        }

        try:
            raw_json = await client._call_api(GET_TOKEN, request_obj=token_credentials)
            token_api_key = AccessTokenResponse(**raw_json).access_token

            # Step 5: Create and return the authenticated client
            return cls(base_url=final_base_url, api_key=token_api_key)
        except AtlanError as atlan_err:
            raise ErrorCode.UNABLE_TO_ESCALATE_WITH_PARAM.exception_with_parameters(
                "Failed to obtain access token for API token"
            ) from atlan_err

    @property
    def admin(self) -> AsyncAdminClient:  # type: ignore[override]
        """Get async admin client with same API as sync"""
        if self._async_admin_client is None:
            self._async_admin_client = AsyncAdminClient(self)
        return self._async_admin_client

    @property
    def asset(self) -> AsyncAssetClient:  # type: ignore[override]
        """Get async asset client with same API as sync"""
        if self._async_asset_client is None:
            self._async_asset_client = AsyncAssetClient(self)
        return self._async_asset_client

    @property
    def audit(self) -> AsyncAuditClient:  # type: ignore[override]
        """Get async audit client with same API as sync"""
        if self._async_audit_client is None:
            self._async_audit_client = AsyncAuditClient(self)
        return self._async_audit_client

    @property
    def contracts(self) -> AsyncContractClient:  # type: ignore[override]
        """Get async contract client with same API as sync"""
        if self._async_contract_client is None:
            self._async_contract_client = AsyncContractClient(self)
        return self._async_contract_client

    @property
    def credentials(self) -> AsyncCredentialClient:  # type: ignore[override]
        """Get async credential client with same API as sync"""
        if self._async_credential_client is None:
            self._async_credential_client = AsyncCredentialClient(self)
        return self._async_credential_client

    @property
    def files(self) -> AsyncFileClient:  # type: ignore[override]
        """Get async file client with same API as sync"""
        if self._async_file_client is None:
            self._async_file_client = AsyncFileClient(self)
        return self._async_file_client

    @property
    def group(self) -> AsyncGroupClient:  # type: ignore[override]
        """Get async group client with same API as sync"""
        if self._async_group_client is None:
            self._async_group_client = AsyncGroupClient(self)
        return self._async_group_client

    @property
    def impersonate(self) -> AsyncImpersonationClient:  # type: ignore[override]
        """Get async impersonate client with same API as sync"""
        if self._async_impersonate_client is None:
            self._async_impersonate_client = AsyncImpersonationClient(self)
        return self._async_impersonate_client

    @property
    def open_lineage(self) -> AsyncOpenLineageClient:  # type: ignore[override]
        """Get async open lineage client with same API as sync"""
        if self._async_open_lineage_client is None:
            self._async_open_lineage_client = AsyncOpenLineageClient(self)
        return self._async_open_lineage_client

    @property
    def queries(self) -> AsyncQueryClient:  # type: ignore[override]
        """Get async query client with same API as sync"""
        if self._async_query_client is None:
            self._async_query_client = AsyncQueryClient(self)
        return self._async_query_client

    @property
    def role(self) -> AsyncRoleClient:  # type: ignore[override]
        """Get async role client with same API as sync"""
        if self._async_role_client is None:
            self._async_role_client = AsyncRoleClient(self)
        return self._async_role_client

    @property
    def search_log(self) -> AsyncSearchLogClient:  # type: ignore[override]
        """Get async search log client with same API as sync"""
        if self._async_search_log_client is None:
            self._async_search_log_client = AsyncSearchLogClient(self)
        return self._async_search_log_client

    @property
    def sso(self) -> AsyncSSOClient:  # type: ignore[override]
        """Get async SSO client with same API as sync"""
        if self._async_sso_client is None:
            self._async_sso_client = AsyncSSOClient(self)
        return self._async_sso_client

    @property
    def tasks(self) -> AsyncTaskClient:  # type: ignore[override]
        """Get the task client."""
        if self._async_task_client is None:
            self._async_task_client = AsyncTaskClient(client=self)
        return self._async_task_client

    @property
    def token(self) -> AsyncTokenClient:  # type: ignore[override]
        """Get async token client with same API as sync"""
        if self._async_token_client is None:
            self._async_token_client = AsyncTokenClient(self)
        return self._async_token_client

    @property
    def typedef(self) -> AsyncTypeDefClient:  # type: ignore[override]
        """Get async typedef client with same API as sync"""
        if self._async_typedef_client is None:
            self._async_typedef_client = AsyncTypeDefClient(self)
        return self._async_typedef_client

    @property
    def user(self) -> AsyncUserClient:  # type: ignore[override]
        """Get async user client with same API as sync"""
        if self._async_user_client is None:
            self._async_user_client = AsyncUserClient(self)
        return self._async_user_client

    @property
    def workflow(self) -> AsyncWorkflowClient:  # type: ignore[override]
        """Get async workflow client with same API as sync"""
        if self._async_workflow_client is None:
            self._async_workflow_client = AsyncWorkflowClient(self)
        return self._async_workflow_client

    @property
    def atlan_tag_cache(self) -> AsyncAtlanTagCache:  # type: ignore[override]
        """Get async Atlan tag cache with same API as sync"""
        if self._async_atlan_tag_cache is None:
            self._async_atlan_tag_cache = AsyncAtlanTagCache(client=self)
        return self._async_atlan_tag_cache

    @property
    def connection_cache(self) -> AsyncConnectionCache:  # type: ignore[override]
        """Get async connection cache with same API as sync"""
        if self._async_connection_cache is None:
            self._async_connection_cache = AsyncConnectionCache(client=self)
        return self._async_connection_cache

    @property
    def custom_metadata_cache(self) -> AsyncCustomMetadataCache:  # type: ignore[override]
        """Get async custom metadata cache with same API as sync"""
        if self._async_custom_metadata_cache is None:
            self._async_custom_metadata_cache = AsyncCustomMetadataCache(client=self)
        return self._async_custom_metadata_cache

    @property
    def dq_template_config_cache(self) -> AsyncDQTemplateConfigCache:  # type: ignore[override]
        """Get async DQ template config cache with same API as sync"""
        if self._async_dq_template_config_cache is None:
            self._async_dq_template_config_cache = AsyncDQTemplateConfigCache(
                client=self
            )
        return self._async_dq_template_config_cache

    @property
    def enum_cache(self) -> AsyncEnumCache:  # type: ignore[override]
        """Get async enum cache with same API as sync"""
        if self._async_enum_cache is None:
            self._async_enum_cache = AsyncEnumCache(client=self)
        return self._async_enum_cache

    @property
    def group_cache(self) -> AsyncGroupCache:  # type: ignore[override]
        """Get async group cache with same API as sync"""
        if self._async_group_cache is None:
            self._async_group_cache = AsyncGroupCache(client=self)
        return self._async_group_cache

    @property
    def role_cache(self) -> AsyncRoleCache:  # type: ignore[override]
        """Get async role cache with same API as sync"""
        if self._async_role_cache is None:
            self._async_role_cache = AsyncRoleCache(client=self)
        return self._async_role_cache

    @property
    def source_tag_cache(self) -> AsyncSourceTagCache:  # type: ignore[override]
        """Get async source tag cache with same API as sync"""
        if self._async_source_tag_cache is None:
            self._async_source_tag_cache = AsyncSourceTagCache(client=self)
        return self._async_source_tag_cache

    @property
    def user_cache(self) -> AsyncUserCache:  # type: ignore[override]
        """Get async user cache with same API as sync"""
        if self._async_user_cache is None:
            self._async_user_cache = AsyncUserCache(client=self)
        return self._async_user_cache

    def _api_logger(self, api, path):
        """API logging helper - same as sync client."""
        LOGGER.debug("------------------------------------------------------")
        LOGGER.debug("Call         : %s %s", api.method, path)
        LOGGER.debug("Content-type_ : %s", api.consumes)
        LOGGER.debug("Accept       : %s", api.produces)
        LOGGER.debug("Client-Type  : %s", "ASYNC")
        LOGGER.debug("Python-Version: %s", get_python_version())
        LOGGER.debug("User-Agent   : %s", f"Atlan-PythonSDK/{VERSION}")

    async def _create_params(
        self, api, query_params, request_obj, exclude_unset: bool = True
    ):
        """
        Async version of _create_params that uses AsyncAtlanRequest for AtlanObject instances.
        """
        params = copy.deepcopy(self._request_params)
        params["headers"]["Accept"] = api.consumes
        params["headers"]["content-type"] = api.produces
        if query_params is not None:
            params["params"] = query_params
        if request_obj is not None:
            if isinstance(request_obj, AtlanObject):
                # Use AsyncAtlanRequest for async retranslation
                async_request = AsyncAtlanRequest(instance=request_obj, client=self)
                params["data"] = await async_request.json()
            elif api.consumes == APPLICATION_ENCODED_FORM:
                params["data"] = request_obj
            else:
                params["data"] = json.dumps(request_obj)
        return params

    async def _call_api(
        self,
        api,
        query_params=None,
        request_obj=None,
        exclude_unset: bool = True,
        text_response=False,
    ):
        """
        Async version of _call_api - mirrors sync client structure.
        """
        path = self._create_path(api)
        params = await self._create_params(
            api, query_params, request_obj, exclude_unset
        )
        if LOGGER.isEnabledFor(logging.DEBUG):
            self._api_logger(api, path)
        return await self._call_api_internal(
            api, path, params, text_response=text_response
        )

    async def _call_api_internal(
        self,
        api,
        path,
        params,
        binary_data=None,
        download_file_path=None,
        text_response=False,
    ):
        """
        Comprehensive async API call implementation matching sync client's error handling.
        """
        session = self._async_session

        # Make the async HTTP request
        response = await self._make_http_request(
            session, api, path, params, download_file_path, binary_data
        )

        if not response:
            return

        # If response is a string and file download was handled, return it directly
        if isinstance(response, str) and download_file_path:
            return response

        # Reset 401 retry flag if response is not 401 (matching sync logic)
        if (
            self._401_has_retried.get()
            and response.status_code
            != ErrorCode.AUTHENTICATION_PASSTHROUGH.http_error_code
        ):
            self._401_has_retried.set(False)

        if response.status_code == api.expected_status:
            return await self._process_successful_response(response, api, text_response)
        elif response.status_code == HTTPStatus.SERVICE_UNAVAILABLE:
            LOGGER.error(
                "Atlas Service unavailable. HTTP Status: %s",
                HTTPStatus.SERVICE_UNAVAILABLE,
            )
            return None
        else:
            return await self._handle_error_response(
                response,
                api,
                path,
                params,
                binary_data,
                download_file_path,
                text_response,
            )

    async def _make_http_request(
        self, session, api, path, params, download_file_path=None, binary_data=None
    ):
        """Make HTTP request - matches sync client structure exactly."""
        try:
            timeout = httpx.Timeout(
                None, connect=self.connect_timeout, read=self.read_timeout
            )
            if api.consumes == EVENT_STREAM and api.produces == EVENT_STREAM:
                async with session.stream(
                    api.method.value, path, **params, timeout=timeout
                ) as stream_response:
                    if download_file_path:
                        return await self._handle_file_download(
                            stream_response, download_file_path
                        )
                    return await self._create_stream_response(
                        stream_response, api.expected_status
                    )
            else:
                # Prepare request kwargs - add data only if we have binary content
                request_kwargs = {
                    "method": api.method.value,
                    "url": path,
                    **{k: v for k, v in params.items() if k != "headers"},
                    "headers": {**session.headers, **params.get("headers", {})},
                    "timeout": timeout,
                }

                # Add binary data if present
                if binary_data is not None:
                    # Handle both file objects and bytes data
                    if hasattr(binary_data, "read"):
                        # It's a file object, read its content
                        file_content = binary_data.read()
                        binary_data.close()
                        request_kwargs["data"] = file_content
                    else:
                        # It's already bytes data (e.g., from MultipartDataGenerator)
                        request_kwargs["data"] = binary_data

                response = await session.request(**request_kwargs)

            LOGGER.debug("HTTP Status: %s", response.status_code)
            return response

        except Exception as e:
            LOGGER.error("HTTP request failed: %s", e)
            raise

    async def _create_stream_response(self, stream_response, expected_status):
        """Create mock response object for event streams."""
        content = await stream_response.aread()
        text = content.decode("utf-8") if content else ""
        lines = (
            text.splitlines()
            if text and stream_response.status_code == expected_status
            else []
        )

        return SimpleNamespace(
            status_code=stream_response.status_code,
            headers=stream_response.headers,
            text=text,
            content=content,
            _stream_lines=lines,
            json=lambda: json.loads(text) if text else {},
        )

    async def _process_successful_response(self, response, api, text_response=False):
        """Process successful API responses."""
        try:
            if (
                response.content is None
                or response.content == "null"
                or len(response.content) == 0
                or response.status_code == HTTPStatus.NO_CONTENT
            ):
                return None

            events = []
            if LOGGER.isEnabledFor(logging.DEBUG):
                LOGGER.debug("Processing successful response")

            if api.consumes == EVENT_STREAM and api.produces == EVENT_STREAM:
                # Process event stream using stored lines from the streaming response
                if hasattr(response, "_stream_lines"):
                    for line in response._stream_lines:
                        if not line:
                            continue
                        if not line.startswith("data: "):
                            raise ErrorCode.UNABLE_TO_DESERIALIZE.exception_with_parameters(
                                line
                            )
                        events.append(json.loads(line.split("data: ")[1]))

            if text_response:
                response_ = response.text
            else:
                # Use AsyncAtlanResponse for proper async translation
                response_ = (
                    events
                    if events
                    else await AsyncAtlanResponse(
                        raw_json=response.json(), client=self
                    ).to_dict()
                )

            LOGGER.debug("response: %s", response_)
            return response_

        except json.decoder.JSONDecodeError as e:
            raise ErrorCode.JSON_ERROR.exception_with_parameters(
                response.text, response.status_code, str(e)
            ) from e

    async def _handle_error_response(
        self,
        response,
        api,
        path,
        params,
        binary_data,
        download_file_path,
        text_response,
    ):
        """Handle error responses with comprehensive error parsing and token refresh."""
        with contextlib.suppress(ValueError, json.decoder.JSONDecodeError):
            error_info = json.loads(response.text)
            error_code = (
                error_info.get("errorCode", 0)
                or error_info.get("code", 0)
                or error_info.get("status")
            )
            error_message = error_info.get("errorMessage", "") or error_info.get(
                "message", ""
            )
            error_doc = (
                error_info.get("doc")
                or error_info.get("errorDoc")
                or error_info.get("errorDocument")
                or error_info.get("errorDocumentation")
            )
            error_cause = error_info.get("errorCause", [])
            causes = error_info.get("causes", [])
            backend_error_id = error_info.get("errorId")

            # Handle the causes and format them for exception
            error_cause_details = [
                f"ErrorType: {cause.get('errorType', 'Unknown')}, "
                f"Message: {cause.get('errorMessage', 'No additional information provided')}, "
                f"Location: {cause.get('location', 'Unknown location')}"
                for cause in causes
            ]
            error_cause_details_str = (
                "\n".join(error_cause_details) if error_cause_details else ""
            )

            # Retry with impersonation (if _user_id is present) on authentication failure
            if (
                self._user_id
                and not self._401_has_retried.get()
                and response.status_code
                == ErrorCode.AUTHENTICATION_PASSTHROUGH.http_error_code
            ):
                try:
                    LOGGER.debug("Starting async 401 automatic token refresh.")
                    return await self._handle_401_token_refresh(
                        api,
                        path,
                        params,
                        binary_data,
                        download_file_path,
                        text_response,
                    )
                except Exception as e:
                    LOGGER.debug(
                        "Async API call failed after a successful 401 token refresh. Error details: %s",
                        e,
                    )
                    raise

            if error_code and error_message:
                error = ERROR_CODE_FOR_HTTP_STATUS.get(
                    response.status_code, ErrorCode.ERROR_PASSTHROUGH
                )
                # Raise exception with error details and causes
                raise error.exception_with_parameters(
                    error_code,
                    error_message,
                    error_cause_details_str,
                    error_cause=error_cause,
                    backend_error_id=backend_error_id,
                    error_doc=error_doc,
                )

        # Fallback error handling
        raise AtlanError(
            SimpleNamespace(
                http_error_code=response.status_code,
                error_id=f"ATLAN-PYTHON-{response.status_code}-000",
                error_message=response.text,
                user_action=ErrorCode.ERROR_PASSTHROUGH.user_action,
            )
        )

    async def _handle_401_token_refresh(
        self,
        api,
        path,
        params,
        binary_data=None,
        download_file_path=None,
        text_response=False,
    ):
        """
        Async version of token refresh and retry logic.
        Handles token refresh and retries the API request upon a 401 Unauthorized response.
        """
        try:
            # Use sync impersonation call since it's a quick API call
            new_token = await self.impersonate.user(user_id=self._user_id)
        except Exception as e:
            LOGGER.debug(
                "Failed to impersonate user %s for async 401 token refresh. Not retrying. Error: %s",
                self._user_id,
                e,
            )
            raise

        self.api_key = new_token
        self._401_has_retried.set(True)
        params["headers"]["authorization"] = f"Bearer {self.api_key}"
        self._request_params["headers"]["authorization"] = f"Bearer {self.api_key}"
        LOGGER.debug("Successfully completed async 401 automatic token refresh.")

        # Async retry loop to ensure token is active before retrying original request
        retry_count = 1
        while retry_count <= self.retry.total:
            try:
                # Use async typedef call to validate token
                response = await self.typedef.get(
                    type_category=[AtlanTypeCategory.STRUCT]
                )
                if response and response.struct_defs:
                    break
            except Exception as e:
                LOGGER.debug(
                    "Retrying async to get typedefs (to ensure token is active) after token refresh failed: %s",
                    e,
                )
            await asyncio.sleep(retry_count)  # Linear backoff with async sleep
            retry_count += 1

        # Retry the API call with the new token
        return await self._call_api_internal(
            api,
            path,
            params,
            binary_data=binary_data,
            download_file_path=download_file_path,
            text_response=text_response,
        )

    async def _handle_file_download(self, response, file_path: str) -> str:  # type: ignore[override]
        """Handle file download from async streaming response (matches sync _handle_file_download)."""
        try:
            with open(file_path, "wb") as download_file:
                async for chunk in response.aiter_bytes(chunk_size=8192):
                    if chunk:
                        download_file.write(chunk)
        except Exception as err:
            raise ErrorCode.UNABLE_TO_DOWNLOAD_FILE.exception_with_parameters(
                str((hasattr(err, "strerror") and err.strerror) or err), file_path
            )
        return file_path

    def _create_path(self, api):
        """Create URL path from API object (same as sync client)"""
        from urllib.parse import urljoin

        if self.base_url == "INTERNAL":
            return urljoin(api.endpoint.service, api.path)
        else:
            return urljoin(urljoin(self.base_url, api.endpoint.prefix), api.path)

    async def _s3_presigned_url_file_upload(self, api, upload_file):
        """Async version of S3 presigned URL file upload (matches sync exactly)"""
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _azure_blob_presigned_url_file_upload(self, api, upload_file):
        """Async version of Azure Blob presigned URL file upload (matches sync exactly)"""
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        # Add mandatory headers for azure blob storage
        params["headers"]["x-ms-blob-type"] = "BlockBlob"
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _gcs_presigned_url_file_upload(self, api, upload_file):
        """Async version of GCS presigned URL file upload (matches sync exactly)"""
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _presigned_url_file_download(self, api, file_path: str):
        """Async version of presigned URL file download (matches sync exactly)"""
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        return await self._call_api_internal(
            api, path, params, download_file_path=file_path
        )

    async def upload_image(self, file, filename):
        """
        Upload an image to Atlan (async version).

        :param file: local file to upload
        :param filename: name of the file to be uploaded
        :returns: details of the uploaded image
        :raises AtlanError: on any API communication issue
        """
        raw_json = await self._upload_file(UPLOAD_IMAGE, file=file, filename=filename)
        return AtlanImage(**raw_json)

    async def _upload_file(self, api, file=None, filename=None):
        """Async version of _upload_file (matches sync exactly)"""
        generator = MultipartDataGenerator()
        generator.add_file(file=file, filename=filename)
        post_data = generator.get_post_data()
        api.produces = f"multipart/form-data; boundary={generator.boundary}"
        path = self._create_path(api)
        params = await self._create_params(
            api, query_params=None, request_obj=None, exclude_unset=True
        )
        if LOGGER.isEnabledFor(logging.DEBUG):
            self._api_logger(api, path)
        return await self._call_api_internal(api, path, params, binary_data=post_data)

    def update_headers(self, header: dict[str, str]):
        """Update headers for the async session."""
        if self._async_session:
            self._async_session.headers.update(header)

    async def aclose(self):
        """Close async resources"""
        if self._async_session:
            await self._async_session.aclose()
            self._async_session = None
        if self._async_asset_client:
            self._async_asset_client = None
        if self._async_file_client:
            self._async_file_client = None
        if self._async_group_client:
            self._async_group_client = None

    @contextlib.asynccontextmanager
    async def max_retries(  # type: ignore[override]
        self, max_retries: Retry = CONNECTION_RETRY
    ):
        """Creates an async context manager that can be used to temporarily change parameters used for retrying connections.
        The original Retry information will be restored when the context is exited."""
        # Store current transport and create new one with updated retries
        session = self._async_session
        if session is None:
            raise RuntimeError("Async session not initialized")

        current_transport = session._transport

        # Build transport kwargs with current proxy/SSL settings
        transport_kwargs = {}
        if self.proxy:
            transport_kwargs["proxy"] = self.proxy
        if self.verify is not None:
            transport_kwargs["verify"] = self.verify

        new_transport = PyatlanAsyncTransport(retry=max_retries, **transport_kwargs)
        session._transport = new_transport

        LOGGER.debug(
            "max_retries set to total: %s force_list: %s",
            max_retries.total,
            max_retries.status_forcelist,
        )
        try:
            LOGGER.debug("Entering max_retries")
            yield None
            LOGGER.debug("Exiting max_retries")
        except httpx.TransportError as err:
            LOGGER.exception("Exception in max retries")
            from pyatlan.errors import ErrorCode

            raise ErrorCode.RETRY_OVERRUN.exception_with_parameters() from err
        finally:
            # Restore original transport
            session._transport = current_transport

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
