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
from http import HTTPStatus
from types import SimpleNamespace
from typing import Optional

import httpx
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
from pyatlan.client.atlan import VERSION, AtlanClient, get_python_version
from pyatlan.client.constants import EVENT_STREAM
from pyatlan.errors import ERROR_CODE_FOR_HTTP_STATUS, AtlanError, ErrorCode
from pyatlan.model.aio.core import AsyncAtlanRequest, AsyncAtlanResponse
from pyatlan.model.core import AtlanObject
from pyatlan.model.enums import AtlanTypeCategory
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

    @property
    def admin(self) -> AsyncAdminClient:
        """Get async admin client with same API as sync"""
        if self._async_admin_client is None:
            self._async_admin_client = AsyncAdminClient(self)
        return self._async_admin_client

    @property
    def asset(self) -> AsyncAssetClient:
        """Get async asset client with same API as sync"""
        if self._async_asset_client is None:
            self._async_asset_client = AsyncAssetClient(self)
        return self._async_asset_client

    @property
    def audit(self) -> AsyncAuditClient:
        """Get async audit client with same API as sync"""
        if self._async_audit_client is None:
            self._async_audit_client = AsyncAuditClient(self)
        return self._async_audit_client

    @property
    def contracts(self) -> AsyncContractClient:
        """Get async contract client with same API as sync"""
        if self._async_contract_client is None:
            self._async_contract_client = AsyncContractClient(self)
        return self._async_contract_client

    @property
    def credentials(self) -> AsyncCredentialClient:
        """Get async credential client with same API as sync"""
        if self._async_credential_client is None:
            self._async_credential_client = AsyncCredentialClient(self)
        return self._async_credential_client

    @property
    def files(self) -> AsyncFileClient:
        """Get async file client with same API as sync"""
        if self._async_file_client is None:
            self._async_file_client = AsyncFileClient(self)
        return self._async_file_client

    @property
    def group(self) -> AsyncGroupClient:
        """Get async group client with same API as sync"""
        if self._async_group_client is None:
            self._async_group_client = AsyncGroupClient(self)
        return self._async_group_client

    @property
    def impersonate(self) -> AsyncImpersonationClient:
        """Get async impersonate client with same API as sync"""
        if self._async_impersonate_client is None:
            self._async_impersonate_client = AsyncImpersonationClient(self)
        return self._async_impersonate_client

    @property
    def open_lineage(self) -> AsyncOpenLineageClient:
        """Get async open lineage client with same API as sync"""
        if self._async_open_lineage_client is None:
            self._async_open_lineage_client = AsyncOpenLineageClient(self)
        return self._async_open_lineage_client

    @property
    def queries(self) -> AsyncQueryClient:
        """Get async query client with same API as sync"""
        if self._async_query_client is None:
            self._async_query_client = AsyncQueryClient(self)
        return self._async_query_client

    @property
    def role(self) -> AsyncRoleClient:
        """Get async role client with same API as sync"""
        if self._async_role_client is None:
            self._async_role_client = AsyncRoleClient(self)
        return self._async_role_client

    @property
    def search_log(self) -> AsyncSearchLogClient:
        """Get async search log client with same API as sync"""
        if self._async_search_log_client is None:
            self._async_search_log_client = AsyncSearchLogClient(self)
        return self._async_search_log_client

    @property
    def sso(self) -> AsyncSSOClient:
        """Get async SSO client with same API as sync"""
        if self._async_sso_client is None:
            self._async_sso_client = AsyncSSOClient(self)
        return self._async_sso_client

    @property
    def tasks(self) -> AsyncTaskClient:
        """Get the task client."""
        if self._async_task_client is None:
            self._async_task_client = AsyncTaskClient(client=self)
        return self._async_task_client

    @property
    def token(self) -> AsyncTokenClient:
        """Get async token client with same API as sync"""
        if self._async_token_client is None:
            self._async_token_client = AsyncTokenClient(self)
        return self._async_token_client

    @property
    def typedef(self) -> AsyncTypeDefClient:
        """Get async typedef client with same API as sync"""
        if self._async_typedef_client is None:
            self._async_typedef_client = AsyncTypeDefClient(self)
        return self._async_typedef_client

    @property
    def user(self) -> AsyncUserClient:
        """Get async user client with same API as sync"""
        if self._async_user_client is None:
            self._async_user_client = AsyncUserClient(self)
        return self._async_user_client

    @property
    def workflow(self) -> AsyncWorkflowClient:
        """Get async workflow client with same API as sync"""
        if self._async_workflow_client is None:
            self._async_workflow_client = AsyncWorkflowClient(self)
        return self._async_workflow_client

    @property
    def atlan_tag_cache(self) -> AsyncAtlanTagCache:
        """Get async Atlan tag cache with same API as sync"""
        if self._async_atlan_tag_cache is None:
            self._async_atlan_tag_cache = AsyncAtlanTagCache(client=self)
        return self._async_atlan_tag_cache

    @property
    def connection_cache(self) -> AsyncConnectionCache:
        """Get async connection cache with same API as sync"""
        if self._async_connection_cache is None:
            self._async_connection_cache = AsyncConnectionCache(client=self)
        return self._async_connection_cache

    @property
    def custom_metadata_cache(self) -> AsyncCustomMetadataCache:
        """Get async custom metadata cache with same API as sync"""
        if self._async_custom_metadata_cache is None:
            self._async_custom_metadata_cache = AsyncCustomMetadataCache(client=self)
        return self._async_custom_metadata_cache

    @property
    def dq_template_config_cache(self) -> AsyncDQTemplateConfigCache:
        """Get async DQ template config cache with same API as sync"""
        if self._async_dq_template_config_cache is None:
            self._async_dq_template_config_cache = AsyncDQTemplateConfigCache(
                client=self
            )
        return self._async_dq_template_config_cache

    @property
    def enum_cache(self) -> AsyncEnumCache:
        """Get async enum cache with same API as sync"""
        if self._async_enum_cache is None:
            self._async_enum_cache = AsyncEnumCache(client=self)
        return self._async_enum_cache

    @property
    def group_cache(self) -> AsyncGroupCache:
        """Get async group cache with same API as sync"""
        if self._async_group_cache is None:
            self._async_group_cache = AsyncGroupCache(client=self)
        return self._async_group_cache

    @property
    def role_cache(self) -> AsyncRoleCache:
        """Get async role cache with same API as sync"""
        if self._async_role_cache is None:
            self._async_role_cache = AsyncRoleCache(client=self)
        return self._async_role_cache

    @property
    def source_tag_cache(self) -> AsyncSourceTagCache:
        """Get async source tag cache with same API as sync"""
        if self._async_source_tag_cache is None:
            self._async_source_tag_cache = AsyncSourceTagCache(client=self)
        return self._async_source_tag_cache

    @property
    def user_cache(self) -> AsyncUserCache:
        """Get async user cache with same API as sync"""
        if self._async_user_cache is None:
            self._async_user_cache = AsyncUserCache(client=self)
        return self._async_user_cache

    def _get_async_session(self) -> httpx.AsyncClient:
        """Get or create async HTTP session"""
        if self._async_session is None:
            self._async_session = httpx.AsyncClient(
                timeout=httpx.Timeout(30.0),
                headers={
                    "authorization": f"Bearer {self.api_key}",
                    "x-atlan-agent": "sdk",
                    "x-atlan-agent-id": "python",
                    "x-atlan-client-origin": "product_sdk",
                    "x-atlan-python-version": get_python_version(),
                    "x-atlan-client-type": "async",
                    "User-Agent": f"Atlan-PythonSDK/{VERSION}",
                },
                base_url=str(self.base_url),
            )
        return self._async_session

    def _api_logger(self, api, path):
        """API logging helper - same as sync client."""
        LOGGER.debug("------------------------------------------------------")
        LOGGER.debug("Call         : %s %s", api.method, path)
        LOGGER.debug("Content-type_ : %s", api.consumes)
        LOGGER.debug("Accept       : %s", api.produces)
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
        session = self._get_async_session()

        # Make the async HTTP request
        response = await self._make_http_request(session, api, path, params)

        if response is None:
            return None

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

    async def _make_http_request(self, session, api, path, params):
        """Make the actual HTTP request."""
        try:
            # Handle EVENT_STREAM APIs differently
            if api.consumes == EVENT_STREAM and api.produces == EVENT_STREAM:
                return await self._call_event_stream_api(session, api, path, params)
            else:
                # Standard API call
                response = await session.request(
                    api.method.value,
                    path,
                    **{k: v for k, v in params.items() if k != "headers"},
                    headers={**session.headers, **params.get("headers", {})},
                    timeout=httpx.Timeout(self.read_timeout),
                )
                LOGGER.debug("HTTP Status: %s", response.status_code)
                return response
        except Exception as e:
            LOGGER.error("HTTP request failed: %s", e)
            raise

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

    async def _call_event_stream_api(self, session, api, path, params):
        """
        Handle EVENT_STREAM APIs with async streaming.

        :param session: async HTTP session
        :param api: API definition with EVENT_STREAM consumes/produces
        :param path: API path
        :param params: request parameters
        :returns: list of parsed events from the stream
        """
        async with session.stream(
            api.method.value,
            path,
            **{k: v for k, v in params.items() if k != "headers"},
            headers={**session.headers, **params.get("headers", {})},
            timeout=httpx.Timeout(self.read_timeout),
        ) as response:
            response.raise_for_status()

            # Read stream content and parse event lines
            content = await response.aread()
            text = content.decode("utf-8") if content else ""
            lines = text.splitlines() if text else []

            # Process event stream lines (similar to sync client)
            events = []
            for line in lines:
                if not line:
                    continue
                if not line.startswith("data: "):
                    raise ErrorCode.UNABLE_TO_DESERIALIZE.exception_with_parameters(
                        line
                    )
                events.append(json.loads(line.split("data: ")[1]))

            return events

    def _create_path(self, api):
        """Create URL path from API object (same as sync client)"""
        from urllib.parse import urljoin

        if self.base_url == "INTERNAL":
            return urljoin(api.endpoint.service, api.path)
        else:
            return urljoin(urljoin(self.base_url, api.endpoint.prefix), api.path)

    async def _s3_presigned_url_file_upload(self, api, upload_file):
        """Async version of S3 presigned URL file upload"""
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _azure_blob_presigned_url_file_upload(self, api, upload_file):
        """Async version of Azure Blob presigned URL file upload"""
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        # Add mandatory headers for azure blob storage
        params["headers"]["x-ms-blob-type"] = "BlockBlob"
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _gcs_presigned_url_file_upload(self, api, upload_file):
        """Async version of GCS presigned URL file upload"""
        path = self._create_path(api)
        params = copy.deepcopy(self._request_params)
        # No need of Atlan's API token here
        params["headers"].pop("authorization", None)
        return await self._call_api_internal(api, path, params, binary_data=upload_file)

    async def _presigned_url_file_download(self, api, file_path: str):
        """Async version of presigned URL file download"""
        path = self._create_path(api)
        session = self._get_async_session()
        # For presigned URLs, we make direct HTTP calls (not through Atlan)
        async with session.stream(
            "GET", path, timeout=httpx.Timeout(self.read_timeout)
        ) as response:
            response.raise_for_status()

            # Handle file download async
            try:
                with open(file_path, "wb") as download_file:
                    async for chunk in response.aiter_bytes():
                        download_file.write(chunk)
            except Exception as err:
                raise ErrorCode.UNABLE_TO_DOWNLOAD_FILE.exception_with_parameters(
                    str((hasattr(err, "strerror") and err.strerror) or err), file_path
                )
            return file_path

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

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.aclose()
